#!/usr/bin/env python3
"""MONKED scenario lab: run the REAL bot (Bot.act) on manufactured tactical states.

Not a simulator. A scenario is one observation plus the bot's memory just before that observation:

  {"name", "category", "obs": {...}, "state": {attr: encoded value}, "flat": false,
   "source": {...}, "expect": {"action": ..., "label": ...}}

* state  - a snapshot of the bot's own attributes (last_hits, tracks, cover/unstick memory, ...), encoded so
           tuples/sets/int-keyed dicts survive JSON. Map geometry is never stored; it comes from the real map.
* flat   - true removes all buildings/roofs (used by metamorphic tests where geometry would break symmetry).

Corpus lives in experiments/corpus/<category>/*.jsonl (one scenario per line).

  python tools/scenario_lab.py harvest --ref c8e98e1 --seeds 1000-1023      # real states from local matches
  python tools/scenario_lab.py synth                                         # rare-combination families
  python tools/scenario_lab.py verify                                        # replay fidelity vs stored base action
  python tools/scenario_lab.py stats
"""
import argparse
import copy
import json
import math
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS = os.path.join(ROOT, "experiments", "corpus")
SIM_DIR = os.environ.get("MONKED_SIM_DIR", r"C:\Users\julia\MONKED\monked-mech-royale\sim")
CATEGORIES = ("multi-threat", "laser-crossfire", "dodge-conflict", "cover-conflict", "unstick-conflict",
              "sound-boundaries", "zone-pressure", "combat-misc", "regression")
GEOMETRY = {"buildings", "los_buildings", "roofs", "_los_cache", "nav_grid", "edge_spots", "nav_paths"}
EMERGENCY = ("dodge", "ldodge", "wedge", "tp-cover", "cover", "zone-run")

_SIM = None
_BOTS = {}


def load_sim():
    global _SIM
    if _SIM is None:
        sys.path.insert(0, SIM_DIR)
        import sim  # noqa: E402
        _SIM = sim
    return _SIM


class Runner:
    """One loaded bot version: a template instance (geometry loaded once) + a fresh-state snapshot."""

    def __init__(self, ref):
        sim = load_sim()
        self.ref = ref
        self.Bot, self.mf = sim.load_bot_class(ref)
        self.hello = sim.load_hello()
        self.mf.draw.caps = dict(self.hello["config"]["debug"])
        self.module_file = self.Bot.__init__.__code__.co_filename
        self.template = self.Bot(self.hello)
        self.fresh = snapshot(self.template)
        self.label = ""
        orig = self.mf.draw.label

        def label(text, *a, **k):
            self.label = str(text)
            return orig(text, *a, **k)
        self.mf.draw.label = label

    def new_bot(self, state=None, flat=False):
        b = copy.copy(self.template)
        restore(b, self.fresh)
        if state:
            restore(b, state)
        b._los_cache = {}
        if flat:
            b.buildings, b.los_buildings, b.roofs = [], [], []
        return b

    def run(self, sc, bot=None):
        b = bot or self.new_bot(sc.get("state"), sc.get("flat", False))
        obs = copy.deepcopy(sc["obs"])
        self.label = ""
        t0 = time.perf_counter()
        act = b.act(obs)
        ms = (time.perf_counter() - t0) * 1000
        self.mf.draw.take()
        return {"action": json.loads(json.dumps(act, default=str)), "label": self.label, "ms": ms, "bot": b}


def runner(ref):
    if ref not in _BOTS:
        _BOTS[ref] = Runner(ref)
    return _BOTS[ref]


# ---------------------------------------------------------------- state encode / decode
def enc(v):
    if isinstance(v, (bool, int, str)) or v is None:
        return v
    if isinstance(v, float):
        return v if math.isfinite(v) else {"__f__": repr(v)}
    if isinstance(v, tuple):
        return {"__t__": [enc(x) for x in v]}
    if isinstance(v, (set, frozenset)):
        return {"__s__": [enc(x) for x in sorted(v, key=repr)]}
    if isinstance(v, list):
        return [enc(x) for x in v]
    if isinstance(v, dict):
        if all(isinstance(k, str) for k in v) and not any(k.startswith("__") for k in v):
            return {k: enc(x) for k, x in v.items()}
        return {"__d__": [[enc(k), enc(x)] for k, x in v.items()]}
    raise TypeError(type(v))


def dec(v):
    if isinstance(v, list):
        return [dec(x) for x in v]
    if isinstance(v, dict):
        if "__f__" in v:
            return float(v["__f__"])
        if "__t__" in v:
            return tuple(dec(x) for x in v["__t__"])
        if "__s__" in v:
            return set(dec(x) for x in v["__s__"])
        if "__d__" in v:
            return {dec(k): dec(x) for k, x in v["__d__"]}
        return {k: dec(x) for k, x in v.items()}
    return v


def snapshot(bot):
    out = {}
    for k, v in vars(bot).items():
        if k in GEOMETRY or callable(v):
            continue
        try:
            out[k] = enc(v)
        except TypeError:
            continue
    return out


def restore(bot, state):
    for k, v in state.items():
        if k in GEOMETRY:
            continue
        setattr(bot, k, dec(copy.deepcopy(v)))


# ---------------------------------------------------------------- corpus IO
def corpus_files(cats=None):
    for cat in cats or CATEGORIES:
        d = os.path.join(CORPUS, cat)
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                if fn.endswith(".jsonl"):
                    yield cat, os.path.join(d, fn)


def load_corpus(cats=None, limit=None):
    out = []
    for _cat, path in corpus_files(cats):
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    out.append(json.loads(line))
                    if limit and len(out) >= limit:
                        return out
    return out


def write_jsonl(cat, name, scenarios):
    d = os.path.join(CORPUS, cat)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, name + ".jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for sc in scenarios:
            f.write(json.dumps(sc, separators=(",", ":")) + "\n")
    return path


# ---------------------------------------------------------------- harvesting real states from local matches
def classify(bot, obs, label):
    """Tactical categories this decision belongs to (cheap, from label tokens + observable state)."""
    toks = set(label.split())
    t = obs["t"]
    cats = []
    att = {k for k, v in (getattr(bot, "last_hits", {}) or {}).items()
           if isinstance(k, int) and 0 <= k < 16 and t - v[0] <= 3.0}
    if len(att) >= 2 or "wedge" in toks or "aggregate" in toks:
        cats.append("multi-threat")
    if any(m.get("charging") for m in obs.get("mechs") or [] if m.get("kind") == "mech"):
        cats.append("laser-crossfire")
    if toks & {"dodge", "ldodge"}:
        cats.append("dodge-conflict")
    if toks & {"tp-cover", "cover"}:
        cats.append("cover-conflict")
    if t < getattr(bot, "unstick_until", -math.inf):
        cats.append("unstick-conflict")
    ns = getattr(bot, "last_near_sound", None)
    if ns and t - ns[0] <= 1.2 and "face" in toks:
        cats.append("sound-boundaries")
    if "zone-run" in toks or not obs["self"].get("in_zone", True):
        cats.append("zone-pressure")
    return cats


def harvest(ref, seeds, per_cat=25, every=3, regression_window=None):
    sim = load_sim()
    rn = runner(ref)
    kept = {c: [] for c in CATEGORIES}
    seen = {}

    for seed in seeds:
        counts = {c: 0 for c in CATEGORIES}

        class Harvest(rn.Bot):
            def act(self, obs):
                pre = snapshot(self)
                obs_copy = copy.deepcopy(obs)
                rn.label = ""
                a = super().act(obs)
                label = rn.label
                in_win = regression_window and regression_window[0] == seed and                     regression_window[1] <= obs["t"] <= regression_window[2]
                for cat in (classify(self, obs, label) or (["regression"] if in_win else [])):
                    counts[cat] += 1
                    win = regression_window and regression_window[0] == seed and \
                        regression_window[1] <= obs["t"] <= regression_window[2]
                    if win:
                        cat_out = "regression"
                    elif counts[cat] % every or len([s for s in kept[cat] if s["source"]["seed"] == seed]) >= per_cat:
                        continue
                    else:
                        cat_out = cat
                    key = (seed, obs["tick"], cat_out)
                    if key in seen:
                        continue
                    seen[key] = 1
                    kept[cat_out].append({
                        "name": f"{cat_out}-s{seed}-t{obs['t']:.1f}", "category": cat_out, "obs": obs_copy,
                        "state": pre, "flat": False,
                        "source": {"kind": "harvest", "ref": ref, "seed": seed, "t": obs["t"]},
                        "expect": {"ref": ref, "action": json.loads(json.dumps(a, default=str)), "label": label}})
                return a

        sim.Match(seed, Harvest, rn.mf, rn.hello, sim.Map()).run()
        print(f"harvest seed {seed}: " + ", ".join(f"{c} {len([s for s in kept[c] if s['source']['seed'] == seed])}"
                                                    for c in CATEGORIES if kept[c]), flush=True)
    return kept


# ---------------------------------------------------------------- synthetic rare-combination families
def _fight_bases(n=None):
    base = [s for s in load_corpus(["multi-threat", "cover-conflict", "laser-crossfire"]) if s["source"]["kind"] == "harvest"
            and "fight" in s["expect"]["label"].split()]
    return base[:n] if n else base


def _me(sc):
    return sc["obs"]["self"]


def _target_id(sc):
    toks = sc["expect"]["label"].split()
    try:
        return int(toks[toks.index("fight") + 1])
    except (ValueError, IndexError):
        return None


def _add_mech(obs, mid, dist, bearing, *, charging=False, aim_err=0.0, hp=1400, weapons=("gun", "laser")):
    me = obs["self"]
    x, y, z = me["pos"]
    mx, my = x + dist * math.cos(bearing), y + dist * math.sin(bearing)
    to_me = math.atan2(y - my, x - mx)
    obs["mechs"] = [m for m in obs.get("mechs") or [] if m.get("id") != mid]
    obs["mechs"].append({"id": mid, "kind": "mech", "pos": [mx, my, z], "vel": [0.0, 0.0, 0.0],
                         "aim": [to_me + aim_err, 0.0], "hp": hp, "max_hp": 1400, "cubes": 0,
                         "weapons": list(weapons), "charging": charging})


def _set_hit(sc, mid, age, bearing):
    st = sc["state"]
    hits = dec(st.get("last_hits", {"__d__": []}))
    hits[mid] = (sc["obs"]["t"] - age, bearing)
    st["last_hits"] = enc(hits)


def _derive(base, cat, tag, mutate):
    sc = copy.deepcopy(base)
    sc["category"], sc["name"] = cat, f"{cat}-{tag}-{base['name']}"
    sc["source"] = {"kind": "synth", "family": tag, "from": base["name"]}
    sc.pop("expect", None)
    mutate(sc)
    return sc


def synth(seed=7):
    rng = random.Random(seed)
    bases = _fight_bases()
    idle = [s for s in load_corpus(["sound-boundaries"]) if s["source"]["kind"] == "harvest"]
    out = {c: [] for c in CATEGORIES}
    free_ids = list(range(1, 16))

    def other_ids(sc, k):
        used = {m.get("id") for m in sc["obs"].get("mechs") or []} | {_me(sc).get("id"), _target_id(sc)}
        return [i for i in free_ids if i not in used][:k]

    for b in bases:
        tid = _target_id(b)
        b1 = rng.uniform(-math.pi, math.pi)
        ids = other_ids(b, 3)
        if len(ids) < 3 or tid is None:
            continue
        # multi-threat: second/third recent attacker, some unseen
        out["multi-threat"].append(_derive(b, "multi-threat", "2att", lambda s: (
            _add_mech(s["obs"], ids[0], rng.uniform(40, 180), b1), _set_hit(s, ids[0], rng.uniform(0, 2.5), b1),
            _set_hit(s, tid, rng.uniform(0, 1.5), None))))
        out["multi-threat"].append(_derive(b, "multi-threat", "3att-unseen", lambda s: (
            _add_mech(s["obs"], ids[0], rng.uniform(40, 180), b1), _set_hit(s, ids[0], rng.uniform(0, 2.5), b1),
            _set_hit(s, ids[1], rng.uniform(0, 2.9), b1 + rng.uniform(1.5, 3.0)))))
        # laser crossfire: one or two charging lasers aimed at us (+ a gun attacker)
        out["laser-crossfire"].append(_derive(b, "laser-crossfire", "laser+gun", lambda s: (
            _add_mech(s["obs"], ids[0], rng.uniform(60, 220), b1, charging=True, aim_err=rng.uniform(-0.01, 0.01)),
            _set_hit(s, tid, rng.uniform(0, 1.0), None))))
        out["laser-crossfire"].append(_derive(b, "laser-crossfire", "2lasers", lambda s: (
            _add_mech(s["obs"], ids[0], rng.uniform(60, 220), b1, charging=True),
            _add_mech(s["obs"], ids[1], rng.uniform(60, 220), b1 + rng.uniform(1.0, 2.6), charging=True))))
        # dodge conflict: a bullet inbound + multi-threat
        def bullet(s):
            me = _me(s)
            x, y, z = me["pos"]
            ang = rng.uniform(-math.pi, math.pi)
            px, py = x + 30 * math.cos(ang), y + 30 * math.sin(ang)
            sp = 250.0
            s["obs"]["projectiles"] = [{"id": 900, "kind": "gun", "pos": [px, py, z + 4.0],
                                        "vel": [-sp * math.cos(ang), -sp * math.sin(ang), 0.0]}]
            _add_mech(s["obs"], ids[0], rng.uniform(40, 160), ang)
            _set_hit(s, ids[0], rng.uniform(0, 2.0), ang)
        out["dodge-conflict"].append(_derive(b, "dodge-conflict", "bullet+2att", bullet))
        out["dodge-conflict"].append(_derive(b, "dodge-conflict", "laser-sidestep+unseen", lambda s: (
            _add_mech(s["obs"], ids[0], rng.uniform(60, 200), b1, charging=True),
            _set_hit(s, ids[1], rng.uniform(0, 2.5), b1 + 2.0))))
        # cover conflict: reload cover + second attacker; tp-cover while charging-laser enemy
        def reload_case(s):
            for w in _me(s).get("weapons") or []:
                if w and w.get("kind") == "gun":
                    w["reload"], w["ammo"] = 1.2, 0
                if w and w.get("kind") == "laser":
                    w["cooldown"] = 1.0
            _set_hit(s, tid, 0.5, None)
            _add_mech(s["obs"], ids[0], rng.uniform(60, 180), b1)
            _set_hit(s, ids[0], rng.uniform(0, 2.4), b1)
        out["cover-conflict"].append(_derive(b, "cover-conflict", "reload+2nd", reload_case))
        out["cover-conflict"].append(_derive(b, "cover-conflict", "tp+charging", lambda s: (
            _add_mech(s["obs"], ids[0], rng.uniform(60, 180), b1, charging=True), _set_hit(s, ids[0], 1.0, b1))))
        # unstick: stationary history while moving + multi-threat
        def stuck(s):
            me = _me(s)
            t = s["obs"]["t"]
            s["state"]["pos_history"] = enc([(t - 0.6 + 0.1 * i, me["pos"][0], me["pos"][1]) for i in range(6)])
            s["state"]["unstick_until"] = enc(-math.inf)
            _add_mech(s["obs"], ids[0], rng.uniform(40, 160), b1)
            _set_hit(s, ids[0], 1.0, b1)
        out["unstick-conflict"].append(_derive(b, "unstick-conflict", "stalled+2att", stuck))
        # zone pressure: next circle edge right behind/in front of us, shrink soon
        def edge(s):
            me = _me(s)
            z = s["obs"]["zone"]
            ang = rng.uniform(-math.pi, math.pi)
            r = z.get("next_radius", 100.0)
            off = r + rng.uniform(-6, 6)
            z["next_center"] = [me["pos"][0] - off * math.cos(ang), me["pos"][1] - off * math.sin(ang)]
            z["shrink_end"] = s["obs"]["t"] + rng.uniform(3, 15)
            _add_mech(s["obs"], ids[0], rng.uniform(40, 160), b1)
            _set_hit(s, ids[0], 1.0, b1)
        out["zone-pressure"].append(_derive(b, "zone-pressure", "edge+2att", edge))

    for b in idle:
        for age in (0.59, 0.60, 0.61, 0.89, 0.90, 0.91):
            def ns(s, age=age):
                hist = dec(s["state"].get("last_near_sound")) if s["state"].get("last_near_sound") else (0, 0.0)
                s["state"]["last_near_sound"] = enc((s["obs"]["t"] - age, hist[1] if hist else 0.0))
            out["sound-boundaries"].append(_derive(b, "sound-boundaries", f"age{age:.2f}", ns))
    return out


def cmd_harvest(a):
    lo, hi = (int(x) for x in a.seeds.split("-"))
    reg = None
    if a.regression:
        s, t0, t1 = a.regression.split(":")
        reg = (int(s), float(t0), float(t1))
    kept = harvest(a.ref, range(lo, hi + 1), per_cat=a.per_cat, every=a.every, regression_window=reg)
    for cat, scs in kept.items():
        if scs:
            print(write_jsonl(cat, f"harvest-{a.ref[:7]}-{lo}-{hi}" if cat != "regression" else a.reg_name, scs), len(scs))


def cmd_synth(a):
    for cat, scs in synth(a.seed).items():
        if scs:
            print(write_jsonl(cat, f"synth-s{a.seed}", scs), len(scs))


def cmd_verify(a):
    corpus = [s for s in load_corpus() if s.get("expect")]
    bad = 0
    for s in corpus:
        rn = runner(s["expect"]["ref"])
        r = rn.run(s)
        if r["action"] != s["expect"]["action"]:
            bad += 1
            if bad <= 5:
                print("MISMATCH", s["name"], r["label"], "|", s["expect"]["label"])
    print(f"replay fidelity: {len(corpus) - bad}/{len(corpus)} scenarios reproduce the recorded action exactly")
    return bad


def cmd_stats(_a):
    tot = 0
    for cat, path in corpus_files():
        n = sum(1 for line in open(path, encoding="utf-8") if line.strip())
        tot += n
        print(f"{cat:18s} {os.path.basename(path):40s} {n}")
    print("total", tot)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    h = sp.add_parser("harvest")
    h.add_argument("--ref", default="c8e98e1")
    h.add_argument("--seeds", default="1000-1023")
    h.add_argument("--per-cat", type=int, default=25)
    h.add_argument("--every", type=int, default=3)
    h.add_argument("--regression", help="seed:t0:t1 window saved whole into the regression category")
    h.add_argument("--reg-name", default="regression")
    s = sp.add_parser("synth")
    s.add_argument("--seed", type=int, default=7)
    sp.add_parser("verify")
    sp.add_parser("stats")
    a = ap.parse_args()
    r = {"harvest": cmd_harvest, "synth": cmd_synth, "verify": cmd_verify, "stats": cmd_stats}[a.cmd](a)
    sys.exit(1 if (a.cmd == "verify" and r) else 0)


if __name__ == "__main__":
    main()
