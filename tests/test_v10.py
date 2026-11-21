"""Scenario tests for v10 (attacker-first targeting and laser discipline).

Run from the repo root:  python tests/test_v10.py
"""
import gzip
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
KIT = ROOT.parent / "buildathon" / "kit" / "mechfight-kit"

import example_bot  # noqa: E402

with gzip.open(KIT / "check" / "stream.jsonl.gz", "rt", encoding="utf-8") as f:
    HELLO = json.loads(f.readline())
HELLO["map"]["dir"] = str(KIT / "arena")


def gun(cooldown=0.0, ammo=12):
    return {"kind": "gun", "cooldown": cooldown, "ammo": ammo, "reload": 0,
            "stats": {"damage": 45, "speed": 252, "range": 230, "mag": 12}}


def laser(charge=0.0, cooldown=0.0):
    return {"kind": "laser", "cooldown": cooldown, "charge": charge,
            "stats": {"damage": 315, "charge": 0.75, "range": 280, "hold_s": 2, "cooldown": 1.65}}


def mech(mid, x, y, hp=1400, charging=False, vel=(0.0, 0.0, 0.0), kind="mech"):
    return {"id": mid, "kind": kind, "pos": [x, y, 0.0], "vel": list(vel), "aim": [0.0, 0.0],
            "hp": hp, "max_hp": 1400 if kind == "mech" else 350, "cubes": 0,
            "weapons": ["gun", "laser"], "charging": charging}


def hit(by, bearing=0.0):
    return {"type": "damaged", "amount": 45, "weapon": "gun", "bearing": bearing, "by": by}


def make_obs(t=20.0, mechs=(), events=(), weapons=None, hp=1400, aim=(0.0, 0.0), pos=(0.0, 0.0, 0.0),
             in_zone=True, cubes=0):
    me = {"id": 3, "pos": list(pos), "vel": [0, 0, 0], "aim": list(aim), "hp": hp, "max_hp": 1400,
          "energy": 100, "in_zone": in_zone, "cubes": cubes,
          "weapons": weapons if weapons is not None else [gun(), laser()], "stats": {}}
    return {"type": "obs", "tick": int(round(t * 20)), "t": t, "alive": 16, "self": me,
            "mechs": list(mechs), "events": list(events), "projectiles": [], "crates": [], "cubes": [],
            "pickups": [], "drops": [], "beams": [], "sounds": [],
            "zone": {"center": [0, 0], "radius": 560, "next_center": [0, 0], "next_radius": 380,
                     "shrink_start": 60, "shrink_end": 120}}


def bot():
    return example_bot.Bot(HELLO)


def bearing_to(x, y):
    return math.atan2(y, x)


TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


# ----------------------------------------------------------------- Build A: targeting
@test
def a1_attacker_beats_distant_wounded():
    b = bot()
    o = make_obs(mechs=[mech(5, 30, 0), mech(7, 0, 270, hp=500)], events=[hit(5)])
    b.act(o)
    assert b.target_id == 5, b.target_id


@test
def a2_no_recent_damage_wounded_still_chased():
    b = bot()
    o = make_obs(mechs=[mech(5, 50, 0), mech(7, 0, 270, hp=500)])
    b.act(o)
    assert b.target_id == 7, b.target_id


@test
def a3_attacker_out_of_threat_range():
    b = bot()
    # The attacker hit us, then walked to 150 m: it no longer blocks the wounded mech.
    b.act(make_obs(t=20.0, mechs=[mech(5, 150, 0)], events=[hit(5)]))
    o = make_obs(t=21.0, mechs=[mech(5, 150, 0), mech(7, 0, 270, hp=500)])
    b.act(o)
    assert b.target_id == 7, b.target_id


@test
def a4_two_attackers_lower_hp_first():
    b = bot()
    o = make_obs(mechs=[mech(5, 30, 0, hp=1400, charging=True), mech(6, -40, 0, hp=900)],
                 events=[hit(5), hit(6, math.pi)])
    b.act(o)
    assert b.target_id == 6, b.target_id


@test
def a5_nearly_dead_close_mech_finished():
    b = bot()
    o = make_obs(mechs=[mech(5, 30, 0), mech(8, 0, 40, hp=200)], events=[hit(5)])
    b.act(o)
    assert b.target_id == 8, b.target_id


@test
def a5b_one_shot_distant_kill_still_allowed():
    b = bot()
    o = make_obs(mechs=[mech(5, 30, 0), mech(7, 0, 270, hp=250)], events=[hit(5)])
    b.act(o)
    assert b.target_id == 7, b.target_id


@test
def a6_target_behind_cover_still_tracked():
    b = bot()
    b.act(make_obs(t=20.0, mechs=[mech(5, 30, 0)], events=[hit(5)]))
    # Memory keeps listing the mech for 5 s after it ducks out of view.
    b.act(make_obs(t=22.0, mechs=[mech(5, 35, 10), mech(7, 0, 270, hp=500)]))
    assert b.target_id == 5, b.target_id


@test
def a7_emergency_heal_still_possible():
    b = bot()
    # Low HP, attacker at 120 m (no mech within 45 m): v8 retreats to heal; v10 must not block that.
    o = make_obs(hp=500, mechs=[mech(5, 120, 0)], events=[hit(5)])
    a = b.act(o)
    assert b.healing, "expected heal mode"
    assert a["fire"] == [False, False], a["fire"]


@test
def a8_no_enemy():
    b = bot()
    a = b.act(make_obs())
    assert b.target_id is None
    assert a["fire"] == [False, False]


@test
def a9_npc_and_zone_damage_dont_count():
    b = bot()
    o = make_obs(mechs=[mech(104, 20, 0, kind="npc"), mech(7, 0, 270, hp=500)],
                 events=[hit(104), {"type": "damaged", "amount": 10, "weapon": "zone",
                                    "bearing": None, "by": None}])
    b.act(o)
    assert b.target_id == 7, b.target_id


def run():
    failed = 0
    for fn in TESTS:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL {fn.__name__}: {exc!r}")
    print(f"{len(TESTS) - failed}/{len(TESTS)} passed")
    return failed


if __name__ == "__main__":
    sys.exit(1 if run() else 0)
