#!/usr/bin/env python3
"""Coverage-gap scenarios designed by the DeepSeek Flash red team (see experiments/results/DEEPSEEK_GAPS.md).

Hand-built states that reach tactical branches the harvested/synthetic corpus missed (mortar shells, dodge gates,
NPC bullets during a drop hold, lightning, blocked-laser alternates, beam return fire, attacking drones, finals
detection and silent walk, target-selection edge cases, roof heal/cover/claim) plus the six subsystem interactions
it flagged (I1-I6). Written to experiments/corpus/<category>/gaps-deepseek.jsonl.

  python tools/gap_scenarios.py
"""
import copy
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scenario_lab as lab  # noqa: E402

GUN = {"kind": "gun", "ammo": 12, "reload": 0.0, "cooldown": 0.0,
       "stats": {"damage": 45, "cooldown": 0.24, "speed": 252, "range": 230, "spread_deg": 0.6, "mag": 12, "reload": 2.4}}


def base(t=60.0, pos=(0.0, 0.0, 0.0), flat=True, **me_kw):
    me = {"id": 0, "pos": list(pos), "vel": [0.0, 0.0, 0.0], "aim": [0.0, 0.0], "hp": 1400.0, "max_hp": 1400.0,
          "energy": 100.0, "max_energy": 100.0, "grounded": True, "cubes": 0, "upgrades": [], "in_zone": True,
          "weapons": [copy.deepcopy(GUN), None], "stats": {}}
    me.update(me_kw)
    obs = {"type": "obs", "tick": int(t * 20) // 2 * 2 + 1, "t": t, "alive": 16, "self": me, "mechs": [], "projectiles": [],
           "crates": [], "cubes": [], "pickups": [], "sounds": [], "beams": [], "events": [], "drops": [],
           "zone": {"center": [pos[0], pos[1]], "radius": 500.0, "next_center": [pos[0], pos[1]], "next_radius": 350.0,
                    "shrink_start": t - 5, "shrink_end": t + 30, "dps": 10}, "offer": None}
    return {"obs": obs, "state": {}, "flat": flat}


def mech(mid, pos, *, hp=1000.0, aim=None, charging=False, weapons=("gun",), kind="mech", **kw):
    m = {"id": mid, "kind": kind, "pos": list(pos), "vel": [0.0, 0.0, 0.0], "aim": aim or [math.pi, 0.0],
         "hp": hp, "max_hp": 1400.0 if kind == "mech" else 350.0, "cubes": 0, "weapons": list(weapons), "charging": charging}
    m.update(kw)
    return m


def sc(name, cat, s, **state):
    s = copy.deepcopy(s)
    for k, v in state.items():
        s["state"][k] = lab.enc(v)
    s.update(name=f"gap-{name}", category=cat, source={"kind": "deepseek-gap", "item": name})
    return s


def build():
    out = []
    t = 60.0
    # 1 finals trip / suppression (I6)
    b = base(t, alive=6)
    b["obs"]["alive"] = 6
    out.append(sc("finals-trip", "combat-misc", b, prev_alive=8, non_our_deaths=0, is_finals=False, recent_dealt={}))
    b2 = copy.deepcopy(b)
    b2["obs"]["events"] = [{"type": "kill", "target": 5}]
    out.append(sc("finals-one-kill-ours", "combat-misc", b2, prev_alive=8, non_our_deaths=0, is_finals=False, recent_dealt={}))
    out.append(sc("I6-finals-suppressed-by-dealt", "combat-misc", b, prev_alive=8, non_our_deaths=1, is_finals=False,
                  recent_dealt={2: t - 1.0}))
    # 2 finals silent walk; + zone-run overwrite
    b = base(200.0)
    b["obs"]["self"]["stats"] = {"walk_speed": 11.7}
    out.append(sc("finals-silent", "zone-pressure", b, is_finals=True, finals_t=180.0))
    b2 = base(200.0, pos=(45.0, 0.0, 0.0))
    b2["obs"]["self"]["stats"] = {"walk_speed": 11.7}
    b2["obs"]["zone"].update(next_center=[200.0, 0.0], next_radius=50.0, shrink_end=202.0)
    out.append(sc("finals-silent-vs-zone-run", "zone-pressure", b2, is_finals=True, finals_t=180.0))
    # 3 mortar dodge, urgency ordering, zone validation (I5)
    b = base(t)
    b["obs"]["projectiles"] = [{"id": 901, "kind": "mortar", "pos": [20.0, 0.0, 10.0], "vel": [-26.0, 0.0, -5.0]}]
    out.append(sc("mortar-dodge", "dodge-conflict", b))
    b2 = copy.deepcopy(b)
    b2["obs"]["projectiles"].append({"id": 902, "kind": "gun", "pos": [60.0, 0.0, 4.5], "vel": [-250.0, 0.0, 0.0]})
    out.append(sc("mortar-vs-gun-urgency", "dodge-conflict", b2))
    b3 = base(t, pos=(9.5, 0.0, 0.0))
    b3["obs"]["zone"].update(next_center=[0.0, 0.0], next_radius=10.0)
    b3["obs"]["projectiles"] = [{"id": 903, "kind": "mortar", "pos": [30.0, 0.0, 10.0], "vel": [-26.0, 0.0, -5.0]}]
    out.append(sc("I5-zone-edge-dodge-into-blast", "dodge-conflict", b3))
    # 4 dodge rejection gates
    for nm, proj, vel in (("vertical-miss", {"pos": [60.0, 0.0, 14.5], "vel": [-250.0, 0.0, 0.0]}, [0.0, 0.0, 0.0]),
                          ("co-moving", {"pos": [30.0, 0.0, 4.5], "vel": [5.0, 0.0, 0.0]}, [5.0, 0.0, 0.0]),
                          ("too-close", {"pos": [10.0, 0.0, 4.5], "vel": [-250.0, 0.0, 0.0]}, [0.0, 0.0, 0.0]),
                          ("too-far", {"pos": [200.0, 0.0, 4.5], "vel": [-250.0, 0.0, 0.0]}, [0.0, 0.0, 0.0]),
                          ("malformed", {"pos": None, "vel": None}, [0.0, 0.0, 0.0])):
        b = base(t)
        b["obs"]["self"]["vel"] = vel
        b["obs"]["projectiles"] = [dict(id=904, kind="gun", **proj)]
        out.append(sc(f"dodge-gate-{nm}", "dodge-conflict", b))
    # 5 NPC bullet ignored during a drop hold (+ gun bullet still dodged)
    b = base(t, hp=400.0)
    b["obs"]["drops"] = [{"id": 20000, "pos": [0.0, 0.0, 0.0], "radius": 8, "lands_in": 0, "capture_s": 4, "progress": 1.0,
                          "holder": None}]
    b["obs"]["projectiles"] = [{"id": 905, "kind": "npc", "pos": [60.0, 0.0, 4.5], "vel": [-250.0, 0.0, 0.0]}]
    out.append(sc("drop-hold-npc-bullet", "dodge-conflict", b, drop_id=20000))
    b2 = copy.deepcopy(b)
    b2["obs"]["projectiles"].append({"id": 906, "kind": "gun", "pos": [0.0, 60.0, 4.5], "vel": [0.0, -250.0, 0.0]})
    out.append(sc("drop-hold-gun-bullet", "dodge-conflict", b2, drop_id=20000))
    # 7 lightning
    for nm, dist, energy in (("in-range", 30.0, 100.0), ("no-energy", 30.0, 9.0), ("out-of-range", 42.0, 100.0)):
        b = base(t, energy=energy, aim=[0.0, -0.083])
        b["obs"]["self"]["weapons"][1] = {"kind": "lightning", "cooldown": 0.0, "stats": {}}
        b["obs"]["mechs"] = [mech(1, (dist, 0.0, 0.0))]
        out.append(sc(f"lightning-{nm}", "laser-crossfire", b, last_hits={1: (t - 1.0, 0.0)}))
    # 8A laser sidestep with aim None
    b = base(t)
    b["obs"]["mechs"] = [mech(1, (60.0, 0.0, 0.0), aim=[None, 0.0], charging=True, weapons=("gun", "laser"))]
    out.append(sc("ldodge-aim-none", "laser-crossfire", b))
    # 12 target selection: unknown hp, sticky switch / stick / unknown current, late gate
    b = base(t)
    m = mech(1, (30.0, 0.0, 0.0))
    del m["hp"], m["max_hp"]
    b["obs"]["mechs"] = [m]
    out.append(sc("target-unknown-hp", "combat-misc", b))
    b = base(t)
    b["obs"]["mechs"] = [mech(1, (30.0, 0.0, 0.0), hp=1200.0), mech(2, (60.0, 20.0, 0.0), hp=100.0)]
    out.append(sc("target-switch-wounded", "combat-misc", b, target_id=1))
    b2 = copy.deepcopy(b)
    b2["obs"]["mechs"][1]["hp"] = 800.0
    out.append(sc("target-stick", "combat-misc", b2, target_id=1, last_hits={2: (t - 1.0, 0.3)}))
    b = base(240.0)
    b["obs"]["mechs"] = [mech(1, (100.0, 0.0, 0.0), hp=500.0)]
    out.append(sc("target-late-no-chase", "combat-misc", b))
    # 13 beam return fire / stale beam face / out of range
    for nm, origin, age in (("fresh", [120.0, 0.0, 7.0], 0.3), ("stale", [120.0, 0.0, 7.0], 1.5), ("far", [300.0, 0.0, 7.0], 0.3)):
        b = base(t)
        b["obs"]["beams"] = [{"by": 5, "kind": "laser", "path": [origin, [0.0, 0.0, 7.0]], "age": age}]
        out.append(sc(f"beam-{nm}", "combat-misc", b))
    # 14 drones: attacking, farm, priority, dz, outside circle
    b = base(t, aim=[0.0, -0.1736])
    b["obs"]["mechs"] = [mech(101, (30.0, 0.0, 0.0), kind="npc", hp=350.0)]
    out.append(sc("drone-attacking", "combat-misc", b, last_hits={101: (t - 1.0, 0.0)}))
    out.append(sc("drone-farm", "combat-misc", b))
    b2 = copy.deepcopy(b)
    b2["obs"]["mechs"] = [mech(101, (40.0, 0.0, 0.0), kind="npc", hp=350.0), mech(102, (10.0, 5.0, 0.0), kind="npc", hp=350.0)]
    out.append(sc("drone-priority", "combat-misc", b2, last_hits={101: (t - 1.0, 0.0)}))
    b3 = copy.deepcopy(b)
    b3["obs"]["mechs"][0]["pos"] = [30.0, 0.0, 6.0]
    out.append(sc("drone-dz", "combat-misc", b3))
    # I1 unstick vs active dodge; I2 laser guard while healing; I3 zone-run vs wedge
    b = base(t)
    b["obs"]["projectiles"] = [{"id": 907, "kind": "gun", "pos": [60.0, 0.0, 4.5], "vel": [-250.0, 0.0, 0.0]}]
    out.append(sc("I1-unstick-vs-dodge", "unstick-conflict", b, pos_history=[(t - 0.6 + 0.1 * k, 0.0, 0.0) for k in range(6)],
                  unstick_until=-math.inf, unstick_started=-math.inf, unstick_sign=1.0))
    b = base(t, hp=500.0)
    b["obs"]["self"]["weapons"][1] = {"kind": "laser", "charge": 0.6, "cooldown": 0.0, "stats": {}}
    out.append(sc("I2-laser-guard-while-healing", "combat-misc", b))
    b = base(t, pos=(45.0, 0.0, 0.0))
    b["obs"]["zone"].update(next_center=[100.0, 0.0], next_radius=60.0, shrink_end=t + 0.7)
    b["obs"]["mechs"] = [mech(1, (15.0, 0.0, 0.0), hp=1000.0),
                         mech(2, (45.0 + 80 * math.cos(math.pi + 1.4), 80 * math.sin(math.pi + 1.4), 0.0)),
                         mech(3, (45.0 + 80 * math.cos(math.pi - 1.4), 80 * math.sin(math.pi - 1.4), 0.0))]
    out.append(sc("I3-zone-run-vs-wedge", "multi-threat", b, last_hits={1: (t - 0.5, math.pi), 2: (t - 0.5, None),
                                                                         3: (t - 0.5, None)}))
    # map scenarios: blocked laser alternate / roof heal / roof tp-cover / roof claim (real geometry)
    rn = lab.runner("c8e98e1")
    tall = [bd for bd in rn.template.buildings if bd[5] - bd[4] >= 12 and bd[1] >= 12]
    if tall:
        (cx, cy), r, _ring, _h, bz, _top = tall[0]
        me_p = (cx - r - 15.0, cy, bz)
        b = base(t, pos=me_p, flat=False)
        b["obs"]["self"]["weapons"][1] = {"kind": "laser", "charge": 0.4, "cooldown": 0.0, "stats": {}}
        b["obs"]["mechs"] = [mech(1, (cx + r + 15.0, cy, bz), hp=300.0),
                             mech(2, (me_p[0] + 10 * math.cos(0.2 + math.pi), me_p[1] + 10 * math.sin(0.2 + math.pi), bz),
                                  hp=1400.0)]
        out.append(sc("blocked-laser-alt", "laser-crossfire", b, target_id=1, last_hits={1: (t - 1.0, 0.0)}))
        b2 = copy.deepcopy(b)
        b2["obs"]["mechs"] = b2["obs"]["mechs"][:1]
        b2["obs"]["self"]["weapons"][1]["charge"] = 0.9
        out.append(sc("blocked-laser-full-release", "laser-crossfire", b2, target_id=1, last_hits={1: (t - 1.0, 0.0)},
                      laser_full_since=t - 1.7))
        b3 = copy.deepcopy(b2)
        b3["obs"]["self"]["weapons"] = [dict(GUN, ammo=4), None]
        out.append(sc("blocked-gun-reload", "laser-crossfire", b3, target_id=1, last_hits={1: (t - 1.0, 0.0)}))
    if rn.template.roofs:
        _idx, (rx, ry), rr, _ring, _holes, rbase, rtop, climbs = rn.template.roofs[0]
        b = base(t, pos=(rx + 1.0, ry, rtop), flat=False, hp=600.0)
        b["obs"]["zone"].update(next_center=[rx, ry], next_radius=300.0)
        out.append(sc("roof-heal", "combat-misc", b))
        b = base(t, pos=(rx + min(6.0, rr - 2), ry, rtop), flat=False)
        b["obs"]["zone"].update(next_center=[rx, ry], next_radius=300.0)
        b["obs"]["mechs"] = [mech(1, (rx + 36.0, ry, rtop), hp=1000.0)]
        out.append(sc("roof-tp-cover-unseen", "cover-conflict", b, is_finals=True, target_id=1,
                      last_hits={1: (t - 0.5, 0.0), 2: (t - 0.5, 2.0)}))
        b2 = copy.deepcopy(b)
        b2["obs"]["self"]["weapons"] = [dict(GUN, ammo=0, reload=1.2), None]
        out.append(sc("roof-reload-cover", "cover-conflict", b2, is_finals=True, target_id=1, last_hits={1: (t - 0.5, 0.0)}))
        b3 = base(t, pos=(climbs[0][0], climbs[0][1], rbase), flat=False)
        b3["obs"]["self"]["weapons"][1] = {"kind": "laser", "charge": 0.0, "cooldown": 0.0, "stats": {}}
        b3["obs"]["zone"].update(next_center=[rx, ry], next_radius=300.0)
        out.append(sc("roof-claim-climb", "combat-misc", b3, is_finals=True))
    return out


def main():
    groups = {}
    for s in build():
        groups.setdefault(s["category"], []).append(s)
    for cat, scs in groups.items():
        print(lab.write_jsonl(cat, "gaps-deepseek", scs), len(scs))


if __name__ == "__main__":
    main()
