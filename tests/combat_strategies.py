"""Semantic combat-state generators shared by Hypothesis tests and coverage sampling.

One builder, two backends: `combat(family)` is a Hypothesis strategy (shrinks to minimal tactical states);
`sample_scenarios(n)` draws the same space with `random` (for coverage runs). States are flat-world (no buildings)
unless noted, so geometry never hides a decision bug and metamorphic transforms stay exact.

Families force the rare combinations: "any", "multi", "crossfire", "dodge", "cover", "unstick", "zone", "sound".
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import scenario_lab as lab  # noqa: E402

TAU = math.tau
FAMILIES = ("any", "multi", "crossfire", "dodge", "cover", "unstick", "zone", "sound")


def build(draw, family="any"):
    """draw(kind, *args): kind in float(lo,hi) | int(lo,hi) | choice(seq) | bool()."""
    t = draw("float", 8.0, 280.0)
    me_hp = draw("float", 80.0, 1400.0)
    speed = draw("float", 0.0, 19.5)
    vb = draw("float", -math.pi, math.pi)
    aim = draw("float", -math.pi, math.pi)
    in_zone = draw("choice", (True,) * 9 + (False,)) if family != "zone" else True
    gun = {"kind": "gun", "cooldown": draw("choice", (0.0, 0.0, 0.1)),
           "ammo": draw("int", 0, 12), "reload": draw("choice", (0.0, 0.0, 0.0, 0.4, 1.2)),
           "stats": {"damage": 45, "cooldown": 0.24, "speed": 252, "range": 230, "spread_deg": 0.6, "mag": 12, "reload": 2.4}}
    slot1 = draw("choice", ("none", "laser", "laser", "lightning"))
    if family in ("cover",):
        gun["reload"], gun["ammo"] = 1.2, 0
    weapons = [gun, None]
    if slot1 == "laser":
        weapons[1] = {"kind": "laser", "charge": draw("choice", (0.0, 0.0, 0.0, 0.3, 0.7)),
                      "cooldown": draw("choice", (0.0, 0.0, 0.8)) if family != "cover" else 1.0, "stats": {}}
    elif slot1 == "lightning":
        weapons[1] = {"kind": "lightning", "cooldown": 0.0, "stats": {}}
    me = {"id": 0, "pos": [0.0, 0.0, 0.0], "vel": [speed * math.cos(vb), speed * math.sin(vb), 0.0],
          "aim": [aim, 0.0], "hp": me_hp, "max_hp": 1400.0, "energy": draw("float", 0.0, 100.0), "max_energy": 100.0,
          "grounded": True, "cubes": draw("int", 0, 16), "upgrades": [], "in_zone": in_zone, "weapons": weapons,
          "stats": {}}

    min_e = {"multi": 2, "crossfire": 2, "dodge": 1, "cover": 2, "unstick": 1, "zone": 1}.get(family, 0)
    n = draw("int", min_e, 4)
    ids = list(range(1, 16))
    mechs, hits = [], {}
    for i in range(n):
        mid = ids[i]
        dist = draw("float", 12.0, 260.0) + 0.37 * i   # exact distance ties are a known v39 tie-break sensitivity
        bearing = draw("float", -math.pi, math.pi)
        x, y = dist * math.cos(bearing), dist * math.sin(bearing)
        to_me = math.atan2(-y, -x)
        wpn = draw("choice", (("gun",), ("gun", "laser"), ("gun", "lightning"), ("gun", "mortar")))
        if family == "crossfire" and i < 2:
            wpn = ("gun", "laser")
        err = draw("choice", (0.003, -0.003, 0.02, 0.1, 0.6))   # exactly 0: v39's sidestep side = sign of a ~0 offset
        charging = "laser" in wpn and (draw("bool") or (family == "crossfire" and i < 2))
        mechs.append({"id": mid, "kind": "mech", "pos": [x, y, 0.0], "vel": [0.0, 0.0, 0.0], "aim": [to_me + err, 0.0],
                      "hp": draw("float", 40.0, 1400.0), "max_hp": 1400.0, "cubes": draw("int", 0, 10),
                      "weapons": list(wpn), "charging": charging})
        hit_age = draw("choice", (None, None, 0.2, 1.0, 2.0, 2.9, 3.5))
        if family in ("multi", "cover") and i < 2:
            hit_age = draw("choice", (0.2, 0.8, 1.6, 2.4))
        if hit_age is not None:
            hits[mid] = (t - hit_age, bearing)
    if draw("bool"):  # an unseen recent attacker
        hb = draw("float", -math.pi, math.pi)
        hits[ids[n]] = (t - draw("float", 0.0, 2.9), hb)

    projectiles = []
    if family == "dodge" or draw("choice", (False,) * 4 + (True,)):
        pa = draw("float", -math.pi, math.pi)
        pd = draw("float", 12.0, 60.0)
        miss = draw("float", -0.08, 0.08)
        projectiles.append({"id": 900, "kind": "gun", "pos": [pd * math.cos(pa), pd * math.sin(pa), 4.0],
                            "vel": [-250 * math.cos(pa + miss), -250 * math.sin(pa + miss), 0.0]})

    nr = draw("float", 30.0, 300.0)
    frac = draw("float", 0.02, 1.15) if family != "zone" else draw("float", 0.85, 1.1)  # 0 = exactly on the zone centre: atan2(+-0,+-0) is sign-of-zero dependent
    za = draw("float", -math.pi, math.pi)
    nc = [-frac * nr * math.cos(za), -frac * nr * math.sin(za)]
    zone = {"center": nc, "radius": nr * 1.6, "next_center": nc, "next_radius": nr,
            "shrink_start": t - 5.0, "shrink_end": t + draw("float", 1.0, 40.0), "dps": 10}
    me["in_zone"] = in_zone

    state = {"last_hits": lab.enc(hits), "is_finals": draw("choice", (False,) * 9 + (True,))}
    if family == "sound" or draw("bool"):
        sb = draw("float", -math.pi, math.pi)
        age = draw("choice", (0.1, 0.59, 0.6, 0.61, 0.89, 0.9, 0.91, 1.5))
        state["last_near_sound"] = lab.enc((t - age, sb))
        state["last_sound"] = lab.enc((t - age, sb))
    if draw("bool"):
        state["last_mech_bearing"] = lab.enc((t - draw("float", 0.0, 6.0), draw("float", -math.pi, math.pi)))
    if family == "unstick" or draw("choice", (False,) * 5 + (True,)):
        state["pos_history"] = lab.enc([(t - 0.6 + 0.1 * k, 0.0, 0.0) for k in range(6)])
    tick = int(t * 20) // 2 * 2 + draw("choice", (0, 40))
    obs = {"type": "obs", "tick": tick, "t": round(t, 2), "alive": 16, "self": me, "mechs": mechs,
           "projectiles": projectiles, "crates": [], "cubes": [], "pickups": [], "sounds": [], "beams": [],
           "events": [], "drops": [], "zone": zone, "offer": None}
    return {"name": f"hyp-{family}", "category": "hypothesis", "obs": obs, "state": state, "flat": True,
            "source": {"kind": "hypothesis", "family": family}}


def combat(family="any"):
    from hypothesis import strategies as st

    @st.composite
    def strat(draw_):
        def draw(kind, *args):
            if kind == "float":
                return draw_(st.floats(args[0], args[1], allow_nan=False, allow_infinity=False))
            if kind == "int":
                return draw_(st.integers(args[0], args[1]))
            if kind == "choice":
                return draw_(st.sampled_from(args[0]))
            return draw_(st.booleans())
        return build(draw, family)
    return strat()


def sample_scenarios(n, seed=11):
    rng = random.Random(seed)

    def draw(kind, *args):
        if kind == "float":
            return rng.uniform(args[0], args[1])
        if kind == "int":
            return rng.randint(args[0], args[1])
        if kind == "choice":
            return rng.choice(args[0])
        return rng.random() < 0.5
    return [build(draw, FAMILIES[i % len(FAMILIES)]) for i in range(n)]
