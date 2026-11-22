#!/usr/bin/env python3
"""MONKED experiment harness: exactly where, why and how does candidate X behave differently from base?

Offline development tooling only. It never edits example_bot.py; bots are loaded read-only from git refs
(or a file path) through the local simulator's loader.

Two passes per seed, both on the local simulator (sim/sim.py):
  1. shared world  - the candidate drives; the base bot sees the identical observation every decision and its
                     action is compared field by field (counterfactual decision differences, activation counts).
  2. paired worlds - base and candidate each play the same seed in their own world. Both are identical up to the
                     first differing action, so this gives the first-divergence record, a short downstream window
                     and the end-of-match local outcome.

Everything from the simulator is LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR.

  python tools/experiment_harness.py compare --base c8e98e1 --candidate 1c4827e --name v71-nearsound-0p9 \
         --detector nearsound --matches 6
  python tools/experiment_harness.py record-score 1c4827e 4.75 --submission BB-XXXX
  python tools/experiment_harness.py table
"""
import argparse
import copy
import datetime
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(ROOT, "experiments", "results")
SIM_DIR = os.environ.get("MONKED_SIM_DIR", r"C:\Users\julia\MONKED\monked-mech-royale\sim")
BASE_OFFICIAL = {"c8e98e18b1471388bdeee6f2e090568393af446b": 4.73}
LOCAL_NOTE = "LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR"
WINDOWS_S = (1.0, 3.0)
RECONVERGE_N = 10          # identical consecutive decisions after a difference = reconverged

# Official history known before this harness existed (no local activation data: shown as unknown).
HISTORY = [
    ("c8e98e1", "v39 base", 4.73), ("5bab1a0", "v60 wedge priority over cover", 4.71),
    ("cca2fdd", "v61 push more (v30 thresholds)", 4.52), ("2a72fc1", "v63 threat gate on push", 4.69),
    ("5c11581", "v64 no farming past 10 cubes", 4.73), ("1390727", "v65 no third-party cover", 4.72),
    ("b465f38", "v66 no near-sound override", 4.54), ("84ea2fd", "v70 no lightning-short guard", 4.73),
    ("a023e35", "v62 aggregate multi-threat movement", None), ("e7c4c5f", "v67 no reload cover", None),
    ("6f9ffa8", "v68 no early zone-run", None), ("80a2182", "v69 no FFA third-party", None),
    ("1c4827e", "v71 near-sound 0.9 s", None),
]


# ---------------------------------------------------------------- detectors (optional, generic)
def _det_nearsound(bot, obs):
    """Bucket each decision by the age of the bot's last near sound (attribute read after act)."""
    ns = getattr(bot, "last_near_sound", None)
    if not ns:
        return None
    age = obs["t"] - ns[0]
    if age <= 0.6:
        return "age<=0.6"
    if age <= 0.9:
        return "0.6<age<=0.9"
    return None


DETECTORS = {"nearsound": _det_nearsound}


def load_detector_file(path):
    scope = {}
    with open(path, encoding="utf-8") as f:
        exec(compile(f.read(), path, "exec"), scope)
    return scope["DETECTORS"]


# ---------------------------------------------------------------- helpers
def git_full(ref):
    if os.path.isfile(ref):
        return os.path.abspath(ref)
    repo = os.path.dirname(SIM_DIR)
    return subprocess.run(["git", "-C", repo, "rev-parse", ref], capture_output=True, text=True, check=True).stdout.strip()


def load_sim():
    sys.path.insert(0, SIM_DIR)
    import sim  # noqa: E402
    return sim


def diff_fields(a, b):
    out = []
    for k in sorted(set(a) | set(b)):
        if k == "tick":
            continue
        va, vb = a.get(k), b.get(k)
        if k == "fire":
            va, vb = list(va or [False, False]), list(vb or [False, False])
            for i in (0, 1):
                if bool(va[i]) != bool(vb[i]):
                    out.append(f"fire{i}")
        elif va != vb:
            out.append(k)
    return out


def r3(v):
    return [round(x, 3) for x in v] if isinstance(v, (list, tuple)) else (round(v, 3) if isinstance(v, float) else v)


def summarize(obs, label, attackers):
    me = obs["self"]
    x, y = me["pos"][0], me["pos"][1]
    mechs = [m for m in obs.get("mechs") or [] if m.get("kind") == "mech" and m.get("pos")]
    near = []
    for m in sorted(mechs, key=lambda m: math.dist((x, y), m["pos"][:2]))[:4]:
        d = math.dist((x, y), m["pos"][:2])
        aim = m.get("aim")
        aimed = None
        if aim and aim[0] is not None:
            to_me = math.atan2(y - m["pos"][1], x - m["pos"][0])
            aimed = round(math.degrees(abs(math.remainder(aim[0] - to_me, math.tau))), 1)
        near.append({"id": m["id"], "dist": round(d, 1), "hp": m.get("hp"), "charging": bool(m.get("charging")),
                     "aim_err_deg": aimed, "weapons": m.get("weapons")})
    weapons = []
    for w in me.get("weapons") or []:
        if not w:
            weapons.append(None)
            continue
        weapons.append({k: r3(w[k]) for k in ("kind", "ammo", "reload", "charge", "cooldown") if k in w})
    zone = obs.get("zone") or {}
    return {
        "tick": obs.get("tick"), "t": round(obs["t"], 2), "pos": r3(me["pos"]), "vel": r3(me.get("vel") or []),
        "hp": round(me["hp"], 1), "max_hp": me["max_hp"], "energy": round(me.get("energy", 0), 1),
        "cubes": me.get("cubes"), "grounded": me.get("grounded"), "in_zone": me.get("in_zone"),
        "aim": r3(me.get("aim") or []), "weapons": weapons, "visible_enemies": len(mechs), "nearest": near,
        "charging_ids": [m["id"] for m in mechs if m.get("charging")],
        "recent_attackers": {str(k): round(obs["t"] - v, 2) for k, v in attackers.items() if obs["t"] - v <= 3.0},
        "zone": {k: r3(zone[k]) for k in ("center", "radius", "next_center", "next_radius") if k in zone},
        "label": label,
    }


class LabelTap:
    def __init__(self, mf):
        self.mf, self.last = mf, ""
        orig = mf.draw.label

        def label(text, *a, **k):
            self.last = str(text)
            return orig(text, *a, **k)
        mf.draw.label = label


def note_attackers(obs, attackers):
    for e in obs.get("events") or []:
        if e.get("type") == "damaged" and e.get("by") is not None:
            attackers[e["by"]] = obs["t"]


# ---------------------------------------------------------------- pass 1: shared world
def shared_world(sim, mf, tap, B, C, seed, hello, world, detectors):
    st = {"decisions": 0, "differing": 0, "cats": {}, "first": None, "reconverged_after": None,
          "act": {name: {} for name in detectors}}
    state = {"since_diff": None}

    class Dual:
        def __init__(self, h):
            self.c = C(copy.deepcopy(h))
            self.b = B(copy.deepcopy(h))
            self.att = {}

        def act(self, obs):
            note_attackers(obs, self.att)
            o2 = copy.deepcopy(obs)
            tap.last = ""
            ac = self.c.act(obs)
            mf.draw.take()
            tap.last = ""
            ab = self.b.act(o2)
            label = tap.last
            st["decisions"] += 1
            fields = diff_fields(ab, ac)
            for name, fn in detectors.items():
                bucket = fn(self.b, o2)
                if bucket:
                    s = st["act"][name].setdefault(bucket, {"decisions": 0, "aim_differs": 0, "any_differs": 0})
                    s["decisions"] += 1
                    s["aim_differs"] += "aim" in fields
                    s["any_differs"] += bool(fields)
            if fields:
                st["differing"] += 1
                cat = "+".join(fields)
                st["cats"][cat] = st["cats"].get(cat, 0) + 1
                if st["first"] is None:
                    st["first"] = {"seed": seed, **summarize(o2, label, self.att), "fields": fields,
                                   "base_action": json.loads(json.dumps(ab, default=str)),
                                   "candidate_action": json.loads(json.dumps(ac, default=str))}
                state["since_diff"] = 0
            elif state["since_diff"] is not None:
                state["since_diff"] += 1
                if state["since_diff"] == RECONVERGE_N and st["reconverged_after"] is None:
                    st["reconverged_after"] = round(obs["t"] - st["first"]["t"], 2)
            return ac

    sim.Match(seed, Dual, mf, hello, world).run()
    return st


# ---------------------------------------------------------------- pass 2: paired worlds
def traced_match(sim, mf, tap, Bot, seed, hello, world):
    trace = []
    box = {}

    class Traced(Bot):
        def act(self, obs):
            tap.last = ""
            a = super().act(obs)
            me = obs["self"]
            dmg_in = sum(e.get("amount", 0) for e in obs.get("events") or [] if e.get("type") == "damaged")
            dmg_out = sum(e.get("amount", 0) for e in obs.get("events") or [] if e.get("type") == "hit")
            new_att = sorted({e["by"] for e in obs.get("events") or [] if e.get("type") == "damaged" and e.get("by") is not None})
            trace.append({"t": obs["t"], "pos": me["pos"][:2], "hp": me["hp"], "energy": me.get("energy", 0),
                          "cubes": me.get("cubes"), "label": tap.last, "a": json.dumps(a, sort_keys=True, default=str),
                          "dmg_in": dmg_in, "dmg_out": dmg_out, "att": new_att})
            return a

    m = sim.Match(seed, Traced, mf, hello, world)
    res = m.run()
    box.update(res, end_hp=round(m.us.hp, 1), end_cubes=m.us.cubes,
               dmg_taken=round(sum(r["dmg_in"] for r in trace), 1), dmg_dealt=round(sum(r["dmg_out"] for r in trace), 1))
    return trace, box


def target_of(label):
    toks = (label or "").split()
    return toks[toks.index("fight") + 1] if "fight" in toks and toks.index("fight") + 1 < len(toks) else None


def window(trace, i0, secs):
    t0 = trace[i0]["t"]
    seg = [r for r in trace[i0:] if r["t"] - t0 <= secs + 1e-9]
    end = seg[-1]
    seen = set(a for r in trace[:i0] for a in r["att"])
    moved_last_1s = None
    tail = [r for r in seg if end["t"] - r["t"] <= 1.0]
    if len(tail) > 1:
        moved_last_1s = round(math.dist(tail[0]["pos"], tail[-1]["pos"]), 1)
    return {"covered_s": round(end["t"] - t0, 2), "hp_delta": round(end["hp"] - trace[i0]["hp"], 1),
            "pos_delta": round(math.dist(end["pos"], trace[i0]["pos"]), 1),
            "energy_delta": round(end["energy"] - trace[i0]["energy"], 1),
            "targets": sorted({t for t in (target_of(r["label"]) for r in seg) if t}),
            "new_attackers": sorted({a for r in seg for a in r["att"]} - seen),
            "stuck": moved_last_1s is not None and moved_last_1s < 1.5,
            "died_in_window": end is trace[-1] and end["t"] - t0 < secs - 0.15}


def paired(sim, mf, tap, B, C, seed, hello, world):
    tb, rb = traced_match(sim, mf, tap, B, seed, hello, world)
    tc, rc = traced_match(sim, mf, tap, C, seed, hello, world)
    i0 = next((i for i, (x, y) in enumerate(zip(tb, tc)) if x["a"] != y["a"]), None)
    if i0 is None and len(tb) != len(tc):
        i0 = min(len(tb), len(tc))
    out = {"seed": seed, "first_divergence_t": None, "windows": {},
           "base_outcome": rb, "candidate_outcome": rc}
    if i0 is not None and i0 < len(tb) and i0 < len(tc):
        out["first_divergence_t"] = round(tb[i0]["t"], 2)
        for s in WINDOWS_S:
            out["windows"][f"{s:g}s"] = {"base": window(tb, i0, s), "candidate": window(tc, i0, s)}
    return out


# ---------------------------------------------------------------- report
def write_reports(data):
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, data["name"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    s = data["summary"]
    cats = sorted(s["categories"].items(), key=lambda kv: -kv[1])
    firsts = [m["first_divergence"] for m in data["matches"] if m["first_divergence"]]
    fpat = {}
    for fd in firsts:
        key = "+".join(fd["fields"]) + " | " + (fd["label"].split(" hp")[0] if fd["label"] else "?")
        fpat[key] = fpat.get(key, 0) + 1
    outs = [(m["paired"]["base_outcome"], m["paired"]["candidate_outcome"]) for m in data["matches"]]
    better = sum(1 for b, c in outs if c["place"] < b["place"])
    worse = sum(1 for b, c in outs if c["place"] > b["place"])
    ob, oc = data.get("official_base"), data.get("official_candidate")
    lines = [
        f"# {data['name']}", "",
        f"- Baseline: `{data['base']}`",
        f"- Candidate: `{data['candidate']}`",
        f"- Official baseline: {ob if ob is not None else 'unknown'}",
        f"- Official candidate: {oc if oc is not None else 'not recorded'}"
        + (f" (delta {oc - ob:+.2f})" if oc is not None and ob is not None else "")
        + (f", submission {data['submission']}" if data.get("submission") else ""),
        f"- Matches tested: {s['matches']} (seeds {data['seeds'][0]}..{data['seeds'][-1]})",
        f"- Decisions compared: {s['decisions']}",
        f"- Differing decisions: {s['differing']}",
        f"- Matches diverged: {s['matches_diverged']}/{s['matches']}",
        f"- Most common action difference: {cats[0][0] + f' ({cats[0][1]})' if cats else 'none'}",
        f"- First-divergence pattern: " + ("; ".join(f"{k} x{v}" for k, v in sorted(fpat.items(), key=lambda kv: -kv[1])) or "none"),
        f"- Local outcome direction ({LOCAL_NOTE}): candidate placed better in {better}, worse in {worse}, "
        f"same in {len(outs) - better - worse} of {len(outs)} matches",
        "- Confidence / limitations: local sim only (no jumping/jets, no beams, guessed house bots); "
        "shared-world counts are counterfactual per decision; paired worlds stop being comparable after divergence.",
        "", "## Action-difference categories", "",
    ]
    lines += [f"- {k}: {v}" for k, v in cats] or ["- none"]
    if data["activation"]:
        lines += ["", "## Activation windows", ""]
        for name, buckets in data["activation"].items():
            for b, v in sorted(buckets.items()):
                lines.append(f"- {name} {b}: {v['decisions']} decisions, aim differs {v['aim_differs']}, "
                             f"any field differs {v['any_differs']}")
    lines += ["", "## First divergence per match", ""]
    for m in data["matches"]:
        fd, p = m["first_divergence"], m["paired"]
        if not fd:
            lines.append(f"- seed {m['seed']}: no divergence")
            continue
        w1 = p["windows"].get("1s", {})
        w3 = p["windows"].get("3s", {})
        lines.append(f"- seed {m['seed']} t={fd['t']}s [{'+'.join(fd['fields'])}] label `{fd['label']}` hp {fd['hp']}/"
                     f"{fd['max_hp']} visible {fd['visible_enemies']} attackers {fd['recent_attackers'] or '-'}")
        lines.append(f"  - base {json.dumps({k: fd['base_action'].get(k) for k in fd['fields'] if not k.startswith('fire')} or fd['base_action'].get('fire'))}"
                     f" vs candidate {json.dumps({k: fd['candidate_action'].get(k) for k in fd['fields'] if not k.startswith('fire')} or fd['candidate_action'].get('fire'))}")
        if w3:
            lines.append(f"  - +3 s base: hp {w3['base']['hp_delta']:+}, moved {w3['base']['pos_delta']} m, new attackers "
                         f"{w3['base']['new_attackers'] or '-'}; candidate: hp {w3['candidate']['hp_delta']:+}, moved "
                         f"{w3['candidate']['pos_delta']} m, new attackers {w3['candidate']['new_attackers'] or '-'}"
                         f"; reconverged after {m['reconverged_after']} s" if m["reconverged_after"] is not None else
                         f"  - +3 s base: hp {w3['base']['hp_delta']:+}; candidate: hp {w3['candidate']['hp_delta']:+}; no reconvergence")
        bo, co = p["base_outcome"], p["candidate_outcome"]
        lines.append(f"  - end ({LOCAL_NOTE}): base place {bo['place']} t {bo['t']}s cause {bo['cause']}; "
                     f"candidate place {co['place']} t {co['t']}s cause {co['cause']}")
    with open(os.path.join(RESULTS, data["name"] + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def cmd_compare(a):
    sim = load_sim()
    base, cand = git_full(a.base), git_full(a.candidate)
    detectors = {}
    for name in a.detector or []:
        detectors[name] = DETECTORS[name]
    if a.detector_file:
        detectors.update(load_detector_file(a.detector_file))
    B, mf = sim.load_bot_class(base)
    C, _ = sim.load_bot_class(cand)
    hello = sim.load_hello()
    world = sim.Map()
    mf.draw.caps = dict(hello["config"]["debug"])
    tap = LabelTap(mf)
    seeds = list(range(a.seed0, a.seed0 + a.matches))
    data = {"name": a.name, "base": base, "candidate": cand,
            "timestamp": datetime.datetime.now().isoformat(timespec="seconds"), "seeds": seeds,
            "official_base": BASE_OFFICIAL.get(base), "official_candidate": None, "submission": None,
            "local_note": LOCAL_NOTE, "matches": [], "activation": {}}
    tot = {"matches": len(seeds), "decisions": 0, "differing": 0, "matches_diverged": 0, "categories": {}}
    for seed in seeds:
        sw = shared_world(sim, mf, tap, B, C, seed, hello, world, detectors)
        pw = paired(sim, mf, tap, B, C, seed, hello, world)
        data["matches"].append({"seed": seed, "decisions": sw["decisions"], "differing": sw["differing"],
                                "categories": sw["cats"], "first_divergence": sw["first"],
                                "reconverged_after": sw["reconverged_after"], "paired": pw})
        tot["decisions"] += sw["decisions"]
        tot["differing"] += sw["differing"]
        tot["matches_diverged"] += sw["differing"] > 0
        for k, v in sw["cats"].items():
            tot["categories"][k] = tot["categories"].get(k, 0) + v
        for name, buckets in sw["act"].items():
            agg = data["activation"].setdefault(name, {})
            for b, v in buckets.items():
                s = agg.setdefault(b, {"decisions": 0, "aim_differs": 0, "any_differs": 0})
                for k in s:
                    s[k] += v[k]
        print(f"seed {seed}: decisions {sw['decisions']} differing {sw['differing']}"
              + (f" first t={sw['first']['t']} [{'+'.join(sw['first']['fields'])}]" if sw["first"] else ""), flush=True)
    data["summary"] = tot
    path = write_reports(data)
    print(f"decisions {tot['decisions']}  differing {tot['differing']}  matches diverged {tot['matches_diverged']}/{tot['matches']}")
    print(f"categories {tot['categories']}")
    if data["activation"]:
        print(f"activation {data['activation']}")
    print(f"wrote {path} and .md  ({LOCAL_NOTE})")


def cmd_record(a):
    os.makedirs(RESULTS, exist_ok=True)
    hits = []
    for fn in os.listdir(RESULTS):
        if fn.endswith(".json"):
            p = os.path.join(RESULTS, fn)
            with open(p, encoding="utf-8") as f:
                d = json.load(f)
            if d.get("candidate", "").startswith(a.candidate):
                hits.append((p, d))
    if not hits:
        sys.exit(f"no result file has candidate {a.candidate}; run compare first")
    for p, d in hits:
        d["official_candidate"] = a.score
        if a.base_score is not None:
            d["official_base"] = a.base_score
        d["submission"] = a.submission or d.get("submission")
        ob = d.get("official_base")
        d["official_delta"] = round(a.score - ob, 2) if ob is not None else None
        write_reports(d)
        print(f"recorded {a.score} for {d['candidate'][:12]} in {os.path.basename(p)} (delta {d['official_delta']})")


def cmd_table(_a):
    os.makedirs(RESULTS, exist_ok=True)
    runs = {}
    for fn in sorted(os.listdir(RESULTS)):
        if fn.endswith(".json"):
            with open(os.path.join(RESULTS, fn), encoding="utf-8") as f:
                d = json.load(f)
            runs[d["candidate"][:7]] = d
    rows = ["| Commit | Mechanism | Decisions changed locally | Matches diverged | Official score | Δ vs 4.73 |",
            "|---|---|---|---|---|---|"]
    listed = set()
    for short, mech, score in HISTORY:
        d = runs.get(short)
        listed.add(short)
        sc = d.get("official_candidate") if d and d.get("official_candidate") is not None else score
        loc = (f"{d['summary']['differing']}/{d['summary']['decisions']}", f"{d['summary']['matches_diverged']}/{d['summary']['matches']}") if d else ("unknown", "unknown")
        rows.append(f"| {short} | {mech} | {loc[0]} | {loc[1]} | {sc if sc is not None else 'not scored'} | "
                    f"{f'{sc - 4.73:+.2f}' if sc is not None else '-'} |")
    for short, d in runs.items():
        if short not in listed:
            sc = d.get("official_candidate")
            rows.append(f"| {short} | {d['name']} | {d['summary']['differing']}/{d['summary']['decisions']} | "
                        f"{d['summary']['matches_diverged']}/{d['summary']['matches']} | {sc if sc is not None else 'not scored'} | "
                        f"{f'{sc - 4.73:+.2f}' if sc is not None else '-'} |")
    text = "# Experiment history\n\nLocal columns: " + LOCAL_NOTE + ". `unknown` = never run through the harness.\n\n" + "\n".join(rows) + "\n"
    with open(os.path.join(RESULTS, "HISTORY.md"), "w", encoding="utf-8") as f:
        f.write(text)
    print(text)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("compare")
    c.add_argument("--base", default="c8e98e1")
    c.add_argument("--candidate", required=True)
    c.add_argument("--name", required=True)
    c.add_argument("--matches", type=int, default=6)
    c.add_argument("--seed0", type=int, default=1000)
    c.add_argument("--detector", action="append", choices=sorted(DETECTORS))
    c.add_argument("--detector-file", help="python file defining DETECTORS = {name: fn(bot, obs) -> bucket or None}")
    r = sp.add_parser("record-score")
    r.add_argument("candidate")
    r.add_argument("score", type=float)
    r.add_argument("--submission")
    r.add_argument("--base-score", type=float)
    sp.add_parser("table")
    a = ap.parse_args()
    {"compare": cmd_compare, "record-score": cmd_record, "table": cmd_table}[a.cmd](a)


if __name__ == "__main__":
    main()
