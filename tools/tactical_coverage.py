#!/usr/bin/env python3
"""Tactical branch coverage: which decision branches of the bot does the scenario corpus actually reach?

  python tools/tactical_coverage.py --ref c8e98e1                 # corpus only
  python tools/tactical_coverage.py --ref c8e98e1 --hypothesis 400 # + Hypothesis-generated combat states

Writes experiments/results/COVERAGE.md (and COVERAGE.json). Branch coverage per tactical function, plus the
source lines of branches the corpus never takes. Not a quality score: a map of blind spots.
"""
import argparse
import ast
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import scenario_lab as lab  # noqa: E402

TACTICAL = ["_act", "_fight", "_projectile_dodge", "_laser_sidestep", "_anti_sandwich_move", "_find_cover", "_heal",
            "_should_push", "_choose_target", "_apply_unstick", "_face_bearing", "_movement", "_laser_guard",
            "_shoot_drone", "_shoot_crate", "_shoot_beam_origin", "_drop_goal", "_cube_goal", "_rotate_move_safe",
            "_on_body", "_laser_ready", "_aggregate_threat_move"]


def function_ranges(src):
    tree = ast.parse(src)
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "Bot":
            for f in node.body:
                if isinstance(f, ast.FunctionDef):
                    out[f.name] = (f.lineno, f.end_lineno)
    return out


def measure(ref, scenarios, hypothesis_n=0, changed_lines=None):
    import coverage
    rn = lab.runner(ref)
    cov = coverage.Coverage(branch=True, data_file=None, include=[rn.module_file])
    cov.start()
    try:
        for sc in scenarios:
            rn.run(sc)
        if hypothesis_n:
            sys.path.insert(0, os.path.join(ROOT, "tests"))
            import combat_strategies as cs  # noqa: E402
            for sc in cs.sample_scenarios(hypothesis_n):
                rn.run(sc)
    finally:
        cov.stop()
    an = cov._analyze(rn.module_file)
    src = open(rn.module_file, encoding="utf-8").read()
    lines = src.splitlines()
    ranges = function_ranges(src)
    possible = {}
    for a, b in an.arc_possibilities_set:
        possible.setdefault(a, set()).add(b)
    missing = an.missing_branch_arcs()
    report = {"ref": ref, "scenarios": len(scenarios), "hypothesis": hypothesis_n, "functions": {}}
    tot_b = tot_hit = 0
    for name in TACTICAL:
        if name not in ranges:
            continue
        lo, hi = ranges[name]
        blines = [ln for ln in an._branch_lines() if lo <= ln <= hi]
        arcs = sum(len(possible.get(ln, ())) for ln in blines)
        miss = sum(len(missing.get(ln, ())) for ln in blines)
        never = [ln for ln in blines if ln in missing]
        report["functions"][name] = {
            "lines": [lo, hi], "branch_arcs": arcs, "taken": arcs - miss,
            "pct": round(100.0 * (arcs - miss) / arcs, 1) if arcs else None,
            "untaken": [{"line": ln, "src": lines[ln - 1].strip()[:110], "missing_to": sorted(missing[ln])} for ln in never]}
        tot_b += arcs
        tot_hit += arcs - miss
    report["tactical_pct"] = round(100.0 * tot_hit / tot_b, 1) if tot_b else None
    report["tactical_arcs"] = [tot_hit, tot_b]
    if changed_lines:
        executed = set(an.executed)
        stmt_changed = [ln for ln in changed_lines if ln in an.statements]
        report["changed_lines_reached"] = [len([ln for ln in stmt_changed if ln in executed]), len(stmt_changed)]
    return report


def write_md(rep, path):
    out = [f"# Tactical branch coverage - {rep['ref']}", "",
           f"Scenarios: {rep['scenarios']} corpus" + (f" + {rep['hypothesis']} Hypothesis states" if rep["hypothesis"] else ""),
           f"Tactical branch arcs taken: {rep['tactical_arcs'][0]}/{rep['tactical_arcs'][1]} ({rep['tactical_pct']}%)", "",
           "| Function | Branch arcs taken | % |", "|---|---|---|"]
    for name, f in sorted(rep["functions"].items(), key=lambda kv: (kv[1]["pct"] if kv[1]["pct"] is not None else 101)):
        out.append(f"| {name} (L{f['lines'][0]}-{f['lines'][1]}) | {f['taken']}/{f['branch_arcs']} | {f['pct']} |")
    out += ["", "## Branches never taken (first 8 per function)", ""]
    for name, f in rep["functions"].items():
        if f["untaken"]:
            out.append(f"### {name}")
            for u in f["untaken"][:8]:
                out.append(f"- L{u['line']} -> {u['missing_to']}: `{u['src']}`")
            if len(f["untaken"]) > 8:
                out.append(f"- ... {len(f['untaken']) - 8} more")
            out.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="c8e98e1")
    ap.add_argument("--hypothesis", type=int, default=0)
    ap.add_argument("--out", default=os.path.join(ROOT, "experiments", "results", "COVERAGE"))
    a = ap.parse_args()
    rep = measure(a.ref, lab.load_corpus(), a.hypothesis)
    with open(a.out + ".json", "w", encoding="utf-8") as fh:
        json.dump(rep, fh, indent=1)
    write_md(rep, a.out + ".md")
    print(f"tactical branch arcs {rep['tactical_arcs'][0]}/{rep['tactical_arcs'][1]} ({rep['tactical_pct']}%) -> {a.out}.md")
    for name, f in sorted(rep["functions"].items(), key=lambda kv: (kv[1]["pct"] if kv[1]["pct"] is not None else 101)):
        print(f"  {name:24s} {f['taken']:4d}/{f['branch_arcs']:<4d} {f['pct']}")


if __name__ == "__main__":
    main()
