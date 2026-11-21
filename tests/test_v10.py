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
    o = make_obs(mechs=[mech(5, 30, 0), mech(7, 0, 270, hp=200)], events=[hit(5)])
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


# ----------------------------------------------------------------- Build B: laser discipline
LASER = 1  # slot index of the laser in make_obs' default loadout


def deg(x):
    return math.radians(x)


def direct_yaw(x, y):
    return math.atan2(y, x)


@test
def b1_charge_begins():
    b = bot()
    a = b.act(make_obs(mechs=[mech(5, 100, 0)], events=[hit(5)]))
    assert a["fire"][LASER] is True, a["fire"]
    assert abs(a["aim"][0] - direct_yaw(100, 0)) < 1e-6


@test
def b2_release_when_charged_and_aligned():
    b = bot()
    a = b.act(make_obs(mechs=[mech(5, 100, 0)], events=[hit(5)], weapons=[gun(), laser(charge=0.75)],
                       aim=(0.0, 0.0)))
    assert a["fire"][LASER] is False, a["fire"]


@test
def b3_far_target_needs_tight_aim():
    b = bot()
    w = [gun(), laser(charge=0.75)]
    # 250 m away, torso 1.0 deg off: v8's fixed 1.5 deg gate would fire and miss (4.4 m off a 2.5 m body).
    a = b.act(make_obs(mechs=[mech(5, 0, 250, hp=500)], weapons=w, aim=(direct_yaw(0, 250) + deg(1.0), 0)))
    assert a["fire"][LASER] is True, "should keep holding"
    a = b.act(make_obs(t=20.1, mechs=[mech(5, 0, 250, hp=500)], weapons=w,
                       aim=(direct_yaw(0, 250) + deg(0.2), 0)))
    assert a["fire"][LASER] is False, "should release when on target"


@test
def b5_target_changes_mid_charge():
    b = bot()
    b.act(make_obs(t=20.0, mechs=[mech(5, 100, 0)], events=[hit(5)], weapons=[gun(), laser(charge=0.3)]))
    # Mech 5 died; mech 6 shoots us from the other side.
    a = b.act(make_obs(t=20.1, mechs=[mech(6, -80, 0)], events=[hit(6, math.pi),
                       {"type": "kill", "target": 5}], weapons=[gun(), laser(charge=0.4)],
                       aim=(0.0, 0.0)))
    assert a["fire"][LASER] is True, a["fire"]
    assert abs(math.remainder(a["aim"][0] - math.pi, math.tau)) < 1e-6


@test
def b7_gun_does_not_fire_unled_during_laser_aim():
    b = bot()
    # 150 m, crossing at 11.7 m/s: the bullet lead is ~2.7 deg off the laser's direct aim.
    m = mech(5, 150, 0, vel=(0.0, 11.7, 0.0))
    a = b.act(make_obs(mechs=[m], events=[hit(5)], weapons=[gun(), laser(charge=0.3)], aim=(0.0, 0.0)))
    assert a["fire"][LASER] is True
    assert a["fire"][0] is False, "gun would fly ~7 m behind the target"
    lead = a["aim"][0]
    assert lead > deg(2.0), "early in the charge the torso follows the gun lead"
    # Torso now on the lead: gun fires while the laser keeps charging (DeepSeek checkpoint 1, T3).
    a = b.act(make_obs(t=20.1, mechs=[m], weapons=[gun(), laser(charge=0.4)], aim=(lead, 0.0)))
    assert a["fire"][0] is True and a["fire"][LASER] is True, a["fire"]
    # Charge nearly full: swing to the laser line, don't release while still on the lead.
    a = b.act(make_obs(t=20.2, mechs=[m], weapons=[gun(), laser(charge=0.75)], aim=(lead, 0.0)))
    assert a["fire"][LASER] is True and abs(a["aim"][0]) < deg(0.5), a
    a = b.act(make_obs(t=20.3, mechs=[m], weapons=[gun(), laser(charge=0.75)], aim=(a["aim"][0], 0.0)))
    assert a["fire"][LASER] is False, "on the laser line at full charge: fire"


@test
def b12_laser_cooldown_uses_gun_lead():
    b = bot()
    m = mech(5, 150, 0, vel=(0.0, 11.7, 0.0))
    o = make_obs(mechs=[m], events=[hit(5)], weapons=[gun(), laser(cooldown=1.0)])
    a = b.act(o)
    assert a["fire"][LASER] is False
    lead = a["aim"][0]
    assert lead > deg(2.0), lead
    a = b.act(make_obs(t=20.1, mechs=[m], weapons=[gun(), laser(cooldown=0.9)], aim=(lead, 0.0)))
    assert a["fire"][0] is True, "gun fires once the torso is on the lead"


@test
def b13_gun_close_range_gate_not_too_tight():
    b = bot()
    a = b.act(make_obs(mechs=[mech(5, 25, 0)], events=[hit(5)], weapons=[gun(), None], aim=(deg(2.5), 0)))
    assert a["fire"][0] is True, "at 25 m a 2.5 deg error still hits"


@test
def b15_no_target_no_fire():
    b = bot()
    a = b.act(make_obs(weapons=[gun(), laser()]))
    assert a["fire"] == [False, False]


@test
def b11_no_forced_early_release_when_misaligned():
    b = bot()
    a = b.act(make_obs(mechs=[mech(5, 100, 0)], events=[hit(5)], weapons=[gun(), laser(charge=0.75)],
                       aim=(deg(10), 0)))
    assert a["fire"][LASER] is True, "turning onto target; the game's own 2 s hold limit is the backstop"


@test
def b17_torso_still_turning():
    b = bot()
    a = b.act(make_obs(mechs=[mech(5, 0, 100)], events=[hit(5)], weapons=[gun(), laser(charge=0.75)],
                       aim=(0.0, 0.0)))
    assert a["fire"][LASER] is True
    assert abs(a["aim"][0] - math.pi / 2) < 1e-6


@test
def b4_target_steps_out_of_candidates_keeps_charge_then_gone_releases():
    b = bot()
    b.act(make_obs(t=20.0, mechs=[mech(5, 40, 0)], weapons=[gun(), laser(charge=0.3)], aim=(0.0, 0.0)))
    # Steps to 50 m (no longer a target: not shooting us, not wounded) but still tracked.
    a = b.act(make_obs(t=20.1, mechs=[mech(5, 50, 0)], weapons=[gun(), laser(charge=0.4)], aim=(0.0, 0.0)))
    assert b.target_id is None
    assert a["fire"][LASER] is True, "keep the charge for the mech we were charging at"
    a = b.act(make_obs(t=20.2, mechs=[], weapons=[gun(), laser(charge=0.5)], aim=(0.0, 0.0)))
    assert a["fire"][LASER] is False, "nobody tracked: let it go and walk at full speed (v8 behaviour)"


@test
def b6_heal_mode_lets_charge_go():
    b = bot()
    b.act(make_obs(t=20.0, mechs=[mech(5, 120, 0)], events=[hit(5)], weapons=[gun(), laser(charge=0.3)]))
    a = b.act(make_obs(t=25.5, hp=600, mechs=[mech(5, 120, 0)], weapons=[gun(), laser(charge=0.4)]))
    assert b.healing
    assert a["fire"][LASER] is False, "retreating: don't crawl at half speed"


@test
def b18_target_in_and_out_of_candidates_no_spam():
    """Torso follows commands; target hops between 40 m (a target) and 50 m (not). Game rules modelled:
    charge +0.1/decision up to 0.75, auto-fire 2 s after full, 1.65 s cooldown."""
    b = bot()
    releases = 0
    charge, cooldown, full_for, aim = 0.0, 0.0, 0.0, (0.0, 0.0)
    t = 20.0
    for k in range(60):
        x = 40 if k % 4 < 2 else 50
        w = [gun(), laser(charge=charge, cooldown=cooldown)]
        a = b.act(make_obs(t=t, mechs=[mech(5, x, 0)], weapons=w, aim=aim))
        aim = tuple(a.get("aim") or aim)
        fire = a["fire"][LASER]
        if charge > 0 and (not fire or full_for >= 2.0):
            releases += 1
            charge, cooldown, full_for = 0.0, 1.65, 0.0
        elif fire and cooldown <= 0:
            charge = min(0.75, charge + 0.1)
            if charge >= 0.75:
                full_for += 0.1
        cooldown = max(0.0, cooldown - 0.1)
        t += 0.1
    # 6 s: each cycle is >= 0.8 s charge + 1.65 s cooldown, so at most 3 shots.
    assert 2 <= releases <= 3, releases


@test
def d1_no_spin_onto_a_bystander():
    """DeepSeek checkpoint 2, item 1: last target died, a bystander sits at 60 m behind us."""
    b = bot()
    b.act(make_obs(t=19.8, mechs=[mech(4, -30, 5)], events=[hit(4, 2.95), hit(11, 2.95)],
                   weapons=[gun(), laser(charge=0.45)], aim=(2.95, 0.0)))
    a = b.act(make_obs(t=20.0, mechs=[mech(9, 60, 0)], events=[{"type": "kill", "target": 4}],
                       weapons=[gun(), laser(charge=0.55)], aim=(2.95, 0.0)))
    assert a["fire"][LASER] is False, "let it go; don't spin 180 deg at half speed onto a bystander"
    assert abs(math.remainder(a["aim"][0] - 2.95, math.tau)) < deg(1), a["aim"]


@test
def d2_outside_zone_lets_charge_go():
    b = bot()
    b.act(make_obs(t=20.0, mechs=[mech(5, 40, 0)], weapons=[gun(), laser(charge=0.3)]))
    a = b.act(make_obs(t=20.1, mechs=[mech(5, 50, 0)], weapons=[gun(), laser(charge=0.4)], in_zone=False))
    assert a["fire"][LASER] is False


@test
def d3_close_crossing_target_released_quickly():
    """DeepSeek checkpoint 2, item 5: 25 m, crossing at 11.7 m/s, torso one decision behind."""
    b = bot()
    px, py, vy = 25.0, -5.0, 11.7
    charge, aim, t = 0.0, (0.0, 0.0), 20.0
    full_at = None
    for k in range(30):
        m = mech(5, px, py, vel=(0.0, vy, 0.0))
        a = b.act(make_obs(t=t, mechs=[m], events=[hit(5)] if k == 0 else [],
                           weapons=[gun(), laser(charge=charge)], aim=aim))
        if charge >= 0.93 * 0.75 and full_at is None:
            full_at = k
        if charge > 0 and not a["fire"][LASER]:
            break
        if a["fire"][LASER]:
            charge = min(0.75, charge + 0.1)
        aim = tuple(a["aim"])
        py += vy * 0.1
        t += 0.1
    else:
        raise AssertionError("never released")
    assert k - full_at <= 2, (k, full_at)


@test
def d4_long_hold_never_releases_outside_body():
    """DeepSeek checkpoint 4: after 0.8 s at full the gate widens, but never past the body width."""
    b = bot()
    w = [gun(), laser(charge=0.75)]
    b.act(make_obs(t=20.0, mechs=[mech(5, 100, 0)], events=[hit(5)], weapons=w, aim=(deg(10), 0)))
    a = b.act(make_obs(t=20.9, mechs=[mech(5, 100, 0)], weapons=w, aim=(deg(1.8), 0)))
    assert a["fire"][LASER] is True, "1.8 deg at 100 m is 3.1 m off a 2.5 m body: keep holding"
    a = b.act(make_obs(t=21.0, mechs=[mech(5, 100, 0)], weapons=w, aim=(deg(1.3), 0)))
    assert a["fire"][LASER] is False, "1.3 deg (2.3 m) is on the body: take it"


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
