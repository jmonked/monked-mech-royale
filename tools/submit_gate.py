#!/usr/bin/env python3
"""MONKED submit gate: every official submission must pass this. It never submits anything.

  python tools/submit_gate.py --candidate 7b8bcd3 --hypothesis "aggregate threat v2" \
         [--base c8e98e1] [--focused "python C:/path/test_v72.py"] [--quick]

Checks
  git       candidate resolves; parent == intended base; candidate worktree (if any) clean; a remote ref points at it
  gameplay  example_bot.py differs from base (REFUSES tooling/docs/results-only commits, e.g. e02ddaaa);
            no tooling/test/result files in the gameplay commit
  tests     focused test command (optional); pytest -n auto with MONKED_CANDIDATE; corpus check: 0 catastrophic
  runtime   check.py: PASS, 0 late, p99 < 10 ms, max < 50 ms; 6-match sim crash check: errors 0, no hang
Writes experiments/results/gate-<short>.md and prints the card. Exit 0 = READY.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.environ.get("MONKED_REPO", r"C:\Users\julia\MONKED\monked-mech-royale")
KIT = os.environ.get("MECH_KIT", r"C:\Users\julia\MONKED\buildathon\kit\mechfight-kit")
NON_GAMEPLAY = re.compile(r"^(tools/|tests/|experiments/|docs/|\.claude/|.*\.md$|requirements.*\.txt$|pytest\.ini$)")


def git(*args, cwd=REPO):
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True).stdout.strip()


def run(cmd, cwd=None, env=None, timeout=1800):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout, shell=isinstance(cmd, str))
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--base", default="c8e98e1")
    ap.add_argument("--hypothesis", default="(not stated)")
    ap.add_argument("--focused", help="shell command for the candidate's focused test (exit 0 = pass)")
    ap.add_argument("--quick", action="store_true", help="skip pytest/corpus (git + gameplay + runtime only)")
    ap.add_argument("--dynamic-matches", type=int, default=24, help="local match profile size (0 = skip)")
    ap.add_argument("--dynamic-from", help="reuse an existing experiments/results/<compare>.json for this candidate")
    a = ap.parse_args()
    card, fails = {}, []

    cand = git("rev-parse", a.candidate)
    base = git("rev-parse", a.base)
    parent = git("log", "-1", "--format=%P", cand)
    card["Candidate"] = cand or f"UNRESOLVED {a.candidate}"
    card["Parent"] = f"{parent} ({'= intended base' if parent == base else 'NOT the intended base ' + base})"
    if not cand:
        fails.append("candidate does not resolve")
    if parent != base:
        fails.append("parent is not the intended base")

    wt = None
    for block in git("worktree", "list", "--porcelain").split("\n\n"):
        if f"HEAD {cand}" in block:
            wt = block.splitlines()[0].replace("worktree ", "")
    dirty = git("status", "--porcelain", cwd=wt) if wt else ""
    card["Worktree"] = f"{wt or 'none checked out'}{' - DIRTY' if dirty else ' - clean' if wt else ''}"
    if dirty:
        fails.append("candidate worktree is dirty")
    remote_refs = [ln.split("\t")[1] for ln in git("ls-remote", "origin").splitlines() if ln.startswith(cand)]
    card["Remote"] = ", ".join(remote_refs) if remote_refs else "NOT on origin"
    if not remote_refs:
        fails.append("no remote ref points at the candidate")

    files = [f for f in git("diff", "--name-only", base, cand).splitlines() if f]
    card["Gameplay files changed"] = ", ".join(files) or "none"
    if "example_bot.py" not in files:
        fails.append("REFUSED: example_bot.py identical to base - not an official gameplay candidate")
    extra = [f for f in files if NON_GAMEPLAY.match(f)]
    if extra:
        fails.append(f"tooling/test/doc files in the gameplay commit: {extra}")
    card["Remote diff"] = git("diff", "--shortstat", base, cand) or "no diff"
    card["Hypothesis"] = a.hypothesis

    with tempfile.TemporaryDirectory() as tmp:
        bot = os.path.join(tmp, "example_bot.py")
        for name in ("example_bot.py", "mechfight.py"):   # the bot imports mechfight from its own folder
            with open(os.path.join(tmp, name), "wb") as f:
                f.write(subprocess.run(["git", "-C", REPO, "show", f"{cand}:{name}"], capture_output=True).stdout)

        if a.focused:
            rc, out = run(a.focused)
            card["Focused test"] = "PASS" if rc == 0 else "FAIL"
            if rc:
                fails.append("focused test failed")

        if not a.quick:
            env = dict(os.environ, MONKED_CANDIDATE=bot)
            rc, out = run([sys.executable, "-m", "pytest", "-n", "auto", "-q"], cwd=ROOT, env=env)
            m = re.findall(r"(\d+) (passed|failed|skipped|error)", out)
            card["Scenario tests (pytest -n auto)"] = (", ".join(f"{n} {w}" for n, w in m) or out[-200:])
            if rc:
                failed = re.findall(r"FAILED (\S+)", out)
                fails.append(f"pytest failed: {failed[:5]}")
                with open(os.path.join(ROOT, "experiments", "results", f"gate-{cand[:7]}-pytest.txt"), "w", encoding="utf-8") as fh:
                    fh.write(out[-20000:])
            rc, out = run([sys.executable, os.path.join(HERE, "experiment_harness.py"), "corpus", "--base", base,
                           "--candidate", bot, "--name", f"gate-{cand[:7]}", "--hypothesis", "1000"], cwd=ROOT)
            g = lambda k: (re.search(rf"- {k}: (\S+)", out) or [None, "?"])[1]  # noqa: E731
            card["Scenario corpus size"] = g("Scenario corpus")
            card["Candidate divergences"] = g("Candidate diverged")
            card["Clearly safer / worse / uncertain"] = f"{g('Clearly safer')} / {g('Clearly worse')} / {g('Neutral/uncertain')}"
            card["Catastrophic regressions"] = g("Catastrophic regressions")
            if card["Catastrophic regressions"] != "0":
                fails.append(f"catastrophic regressions: {card['Catastrophic regressions']}")

        rc, out = run([sys.executable, "check/check.py", "--map-dir", "arena", "--", sys.executable, "-u", bot], cwd=KIT,
                      timeout=300)
        late = re.search(r"missed the 50 ms budget: (\d+)", out)
        times = re.search(r"p99 ([\d.]+)\s+max ([\d.]+)", out)
        p50 = re.search(r"p50 ([\d.]+)", out)
        ok = "PASS" in out and late and late.group(1) == "0" and times and float(times.group(1)) < 10 and float(times.group(2)) < 50
        card["check.py"] = (f"{'PASS' if 'PASS' in out else 'FAIL'}, late {late.group(1) if late else '?'}, "
                            f"p50 {p50.group(1) if p50 else '?'} p99 {times.group(1) if times else '?'} max {times.group(2) if times else '?'} ms")
        if not ok:
            fails.append("check.py gate (PASS, 0 late, p99<10, max<50)")

        try:
            rc, out = run([sys.executable, "sim/sim.py", "--compare", cand, "--matches", "6", "--workers", "4"], cwd=REPO,
                          timeout=900)
            errs = re.findall(r"errors (\d+)", out)
            card["Crash check (6 matches)"] = f"errors {errs[-1] if errs else '?'}, exit {rc}"
            if rc or not errs or errs[-1] != "0":
                fails.append("crash check")
        except subprocess.TimeoutExpired:
            card["Crash check (6 matches)"] = "HUNG (timeout)"
            fails.append("crash check hung")

    dyn = {}
    if a.dynamic_from or a.dynamic_matches:
        import json
        path = a.dynamic_from
        if not path:
            name = f"gate-dynamic-{cand[:7]}"
            run([sys.executable, os.path.join(HERE, "experiment_harness.py"), "compare", "--base", base, "--candidate",
                 cand, "--name", name, "--matches", str(a.dynamic_matches)], cwd=ROOT, timeout=7200)
            path = os.path.join(ROOT, "experiments", "results", name + ".json")
        with open(path, encoding="utf-8") as fh:
            dd = json.load(fh)
        if dd.get("candidate") != cand:
            fails.append(f"dynamic profile {path} is for {dd.get('candidate')}, not the candidate")
        better = worse = same = pb = pw = large = 0
        for m in dd["matches"]:
            pw_ = m["paired"]
            if not m["first_divergence"] or not pw_["windows"].get("3s"):
                continue
            w = pw_["windows"]["3s"]
            dlt = w["candidate"]["hp_delta"] - w["base"]["hp_delta"]
            better += dlt > 0
            worse += dlt < 0
            same += dlt == 0
            bp, cp = pw_["base_outcome"]["place"], pw_["candidate_outcome"]["place"]
            pb += cp < bp
            pw += cp > bp
            large += (dlt < -200 or (w["candidate"]["died_in_window"] and not w["base"]["died_in_window"]) or cp - bp >= 2)
        dyn = {"profile": f"{os.path.basename(path)} ({dd['summary']['matches']} matches, "
                          f"{dd['summary']['matches_diverged']} diverged, {dd['summary']['differing']} decisions differ)",
               "better (+3 s HP)": better, "worse (+3 s HP)": worse, "same (+3 s HP)": same,
               "local placement better": pb, "local placement worse": pw, "large regressions": large}
        if large:
            fails.append(f"dynamic: {large} large local regressions (>200 HP worse at +3 s, died in window, or 2+ places)")

    verdict = "READY" if not fails else "NOT READY"
    lines = [f"{k}: {v}" for k, v in card.items()]
    if dyn:
        lines += ["", "Dynamic downstream (LOCAL ONLY - not an official score predictor; separate from static verdicts):"]
        lines += [f"  {k}: {v}" for k, v in dyn.items()]
    lines += ["", verdict] + [f"  - {f}" for f in fails]
    text = "\n".join(lines)
    print(text)
    os.makedirs(os.path.join(ROOT, "experiments", "results"), exist_ok=True)
    with open(os.path.join(ROOT, "experiments", "results", f"gate-{(cand or a.candidate)[:7]}.md"), "w", encoding="utf-8") as f:
        f.write("# Submit gate\n\n```text\n" + text + "\n```\n")
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
