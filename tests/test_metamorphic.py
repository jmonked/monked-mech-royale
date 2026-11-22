"""Metamorphic tests: strategically equivalent states must give equivalent decisions (flat world, real Bot.act).

* rotation   - rotate every position, velocity, aim, bearing and the zone about our mech; move/aim must rotate too
               (skipped when the base is idle-scanning: that sweep is an absolute, time-based yaw by design)
* translation- shift the whole state; the decision must not change
* ordering   - shuffle obs["mechs"]; the decision must not change
* timing     - probe ages around v39 thresholds; a tiny age change that flips the move by > 120 degrees or toggles
               boost is recorded in experiments/results/BOUNDARIES.md (a finding, not automatically a bug)
"""
import copy
import json
import math
import os
import random

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

import combat_strategies as cs
import scenario_lab as lab
from conftest import BASE, CANDIDATE, EXAMPLES, ROOT, save_found

SET = settings(max_examples=EXAMPLES, deadline=None, derandomize=True, database=None,
               suppress_health_check=[HealthCheck.too_slow, HealthCheck.data_too_large])
REFS = [BASE] + ([CANDIDATE] if CANDIDATE else [])
REF_IDS = ["base"] + (["candidate"] if CANDIDATE else [])   # stable ids: Hypothesis seeds from the test id
EPS = 1e-6


def _rot(v, th):
    c, s = math.cos(th), math.sin(th)
    return [v[0] * c - v[1] * s, v[0] * s + v[1] * c] + list(v[2:])


def rotate(sc, th):
    sc = copy.deepcopy(sc)
    o = sc["obs"]
    me = o["self"]
    me["pos"], me["vel"] = _rot(me["pos"], th), _rot(me["vel"], th)
    me["aim"][0] += th
    for m in o["mechs"]:
        m["pos"], m["vel"] = _rot(m["pos"], th), _rot(m["vel"], th)
        m["aim"][0] += th
    for p in o["projectiles"]:
        p["pos"], p["vel"] = _rot(p["pos"], th), _rot(p["vel"], th)
    for k in ("center", "next_center"):
        o["zone"][k] = _rot(o["zone"][k], th)
    st_ = sc["state"]
    hits = lab.dec(st_["last_hits"])
    st_["last_hits"] = lab.enc({k: (v[0], None if v[1] is None else v[1] + th) for k, v in hits.items()})
    for k in ("last_near_sound", "last_sound", "last_mech_bearing"):
        if k in st_:
            t, b = lab.dec(st_[k])
            st_[k] = lab.enc((t, b + th))
    if "pos_history" in st_:
        st_["pos_history"] = lab.enc([(t, *_rot([x, y], th)) for t, x, y in lab.dec(st_["pos_history"])])
    return sc


def translate(sc, dx, dy):
    sc = copy.deepcopy(sc)
    o = sc["obs"]
    for p in [o["self"]] + o["mechs"] + o["projectiles"]:
        p["pos"][0] += dx
        p["pos"][1] += dy
    for k in ("center", "next_center"):
        o["zone"][k] = [o["zone"][k][0] + dx, o["zone"][k][1] + dy]
    if "pos_history" in sc["state"]:
        sc["state"]["pos_history"] = lab.enc([(t, x + dx, y + dy) for t, x, y in lab.dec(sc["state"]["pos_history"])])
    return sc


def _ang(a, b):
    return abs(math.remainder(a - b, math.tau))


def same(a, b, th=0.0):
    ma, mb = _rot(a["move"], th), b["move"]
    if max(abs(ma[0] - mb[0]), abs(ma[1] - mb[1])) > EPS:
        return False, f"move {a['move']} vs {b['move']}"
    if _ang(a["aim"][0] + th, b["aim"][0]) > EPS or abs(a["aim"][1] - b["aim"][1]) > EPS:
        return False, f"aim {a['aim']} vs {b['aim']}"
    for k in ("fire", "boost", "jump", "reload"):
        if a.get(k) != b.get(k):
            return False, f"{k} {a.get(k)} vs {b.get(k)}"
    return True, ""


@pytest.mark.parametrize("ref", REFS, ids=REF_IDS)
@SET
@given(data=st.data(), th=st.floats(-math.pi, math.pi))
def test_rotation(ref, data, th):
    sc = data.draw(cs.combat(data.draw(st.sampled_from(("any", "multi", "crossfire", "dodge", "cover")))))
    rn = lab.runner(ref)
    a = rn.run(sc)
    if "scan" in a["label"].split():
        return
    b = rn.run(rotate(sc, th))
    ok, why = same(a["action"], b["action"], th)
    if not ok:
        save_found("metamorphic-rotation", sc, [why, a["label"], b["label"]])
    assert ok, f"{why} | {a['label']} | {b['label']}"


@pytest.mark.parametrize("ref", REFS, ids=REF_IDS)
@SET
@given(data=st.data(), dx=st.floats(-300, 300), dy=st.floats(-300, 300))
def test_translation(ref, data, dx, dy):
    sc = data.draw(cs.combat(data.draw(st.sampled_from(cs.FAMILIES))))
    rn = lab.runner(ref)
    a, b = rn.run(sc), rn.run(translate(sc, dx, dy))
    ok, why = same(a["action"], b["action"])
    if not ok:
        save_found("metamorphic-translation", sc, [why, a["label"], b["label"]])
    assert ok, f"{why} | {a['label']} | {b['label']}"


@pytest.mark.parametrize("ref", REFS, ids=REF_IDS)
@SET
@given(data=st.data(), seed=st.integers(0, 10 ** 6))
def test_enemy_order(ref, data, seed):
    sc = data.draw(cs.combat(data.draw(st.sampled_from(("multi", "crossfire", "cover", "any")))))
    sc2 = copy.deepcopy(sc)
    random.Random(seed).shuffle(sc2["obs"]["mechs"])
    rn = lab.runner(ref)
    a, b = rn.run(sc), rn.run(sc2)
    ok, why = same(a["action"], b["action"])
    if not ok:
        save_found("metamorphic-order", sc, [why, a["label"], b["label"]])
    assert ok, f"{why} | {a['label']} | {b['label']}"


BOUNDARY_PROBES = {
    "near_sound_0.6": ("last_near_sound", (0.59, 0.60, 0.61)),
    "near_sound_0.9": ("last_near_sound", (0.89, 0.90, 0.91)),
    "sound_2.0": ("last_sound", (1.99, 2.00, 2.01)),
    "hit_2.0": ("last_hits", (1.99, 2.00, 2.01)),
    "hit_2.5": ("last_hits", (2.49, 2.50, 2.51)),
    "hit_3.0": ("last_hits", (2.99, 3.00, 3.01)),
    "mech_bearing_5.0": ("last_mech_bearing", (4.99, 5.00, 5.01)),
}


def _with_age(sc, key, age):
    sc = copy.deepcopy(sc)
    t = sc["obs"]["t"]
    st_ = sc["state"]
    if key == "last_hits":
        hits = lab.dec(st_["last_hits"])
        if not hits:
            return None
        k0 = sorted(hits)[0]
        hits[k0] = (t - age, hits[k0][1])
        st_["last_hits"] = lab.enc(hits)
    else:
        b = lab.dec(st_[key])[1] if key in st_ else 0.7
        st_[key] = lab.enc((t - age, b))
    return sc


@pytest.mark.parametrize("ref", REFS, ids=REF_IDS)
def test_timing_boundaries(ref):
    rn = lab.runner(ref)
    findings, probes = [], 0
    for sc in cs.sample_scenarios(240, seed=5):
        for name, (key, ages) in BOUNDARY_PROBES.items():
            acts = []
            for age in ages:
                s2 = _with_age(sc, key, age)
                if s2 is None:
                    break
                acts.append(rn.run(s2))
            if len(acts) < 3:
                continue
            probes += 1
            for (x, y), (a1, a2) in zip(zip(ages, ages[1:]), zip(acts, acts[1:])):
                m1, m2 = a1["action"]["move"], a2["action"]["move"]
                n1, n2 = math.hypot(*m1), math.hypot(*m2)
                flip = n1 > 0.3 and n2 > 0.3 and (m1[0] * m2[0] + m1[1] * m2[1]) / (n1 * n2) < -0.5
                boost = a1["action"].get("boost") != a2["action"].get("boost")
                if flip or boost:
                    findings.append({"probe": name, "ages": [x, y], "flip_gt_120deg": flip, "boost_toggle": boost,
                                     "labels": [a1["label"], a2["label"]], "family": sc["source"]["family"]})
    out = os.path.join(ROOT, "experiments", "results", f"BOUNDARIES-{ref[:12].replace(os.sep, '_').replace(':', '')}.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    by = {}
    for f in findings:
        by[f["probe"]] = by.get(f["probe"], 0) + 1
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(f"# Timing-boundary probe ({ref})\n\nProbes: {probes}; discontinuities (move flip > 120 deg or boost toggle "
                 f"within 0.01 s of age): {len(findings)}\n\n" + "\n".join(f"- {k}: {v}" for k, v in sorted(by.items())) +
                 "\n\n## Examples\n\n" + "\n".join(f"- {json.dumps(f)}" for f in findings[:25]) + "\n")
    assert probes > 0
