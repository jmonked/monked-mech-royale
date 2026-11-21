"""Scenario tests for v10 (attacker-first targeting and laser discipline).

Run from the repo root:  python tests/test_v10.py
"""
import gzip
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
KIT = ROOT.parent / "buildathon" / "kit" / "mechfight-kit"
if not KIT.is_dir():  # Linked worktrees share the main checkout's sibling kit.
    common = subprocess.check_output(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                                     cwd=ROOT, text=True).strip()
    KIT = Path(common).parent.parent / "buildathon" / "kit" / "mechfight-kit"

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
    assert math.hypot(*a["move"]) > 0.5, "retreat movement still happens"


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


# ----------------------------------------------------------------- Build C: heal fight-back
@test
def c1_heal_shoots_back_at_active_attacker():
    b = bot()
    o = make_obs(hp=600, mechs=[mech(5, 120, 0)], events=[hit(5)], weapons=[gun(), laser()], aim=(0.0, 0.0))
    a = b.act(o)
    assert b.healing
    assert a["fire"][0] is True, "gun shoots back at the mech that is shooting us"
    assert a["fire"][LASER] is False, "no new laser charge: it would halve our retreat speed"
    ref = bot().act(make_obs(hp=600, mechs=[mech(5, 120, 0)], events=[hit(5)], weapons=[gun(), None]))
    assert ref["move"] == a["move"], "retreat path must not change"


@test
def c2_heal_quiet_after_damage_stops():
    b = bot()
    b.act(make_obs(t=20.0, hp=600, mechs=[mech(5, 120, 0)], events=[hit(5)], weapons=[gun(), None]))
    a = b.act(make_obs(t=22.5, hp=600, mechs=[mech(5, 120, 0)], weapons=[gun(), None], aim=(0.0, 0.0)))
    assert b.healing
    assert a["fire"] == [False, False], "no damage for 2.5 s: hold fire so regen can start"


@test
def c3_close_enemy_means_fight_not_heal():
    b = bot()
    a = b.act(make_obs(hp=600, mechs=[mech(5, 30, 0)], events=[hit(5)], weapons=[gun(), None], aim=(0.0, 0.0)))
    assert not b.healing
    assert a["fire"][0] is True


@test
def c4_sudden_attack_during_heal():
    b = bot()
    b.act(make_obs(t=20.0, hp=600, mechs=[mech(5, 150, 0)], weapons=[gun(), None]))
    assert b.healing
    a = b.act(make_obs(t=20.1, hp=560, mechs=[mech(5, 150, 0)], events=[hit(5)], weapons=[gun(), None],
                       aim=(0.0, 0.0)))
    assert b.healing and a["fire"][0] is True


@test
def c5_heal_outside_zone_does_not_engage():
    b = bot()
    a = b.act(make_obs(hp=600, in_zone=False, mechs=[mech(5, 120, 0)], events=[hit(5)], weapons=[gun(), None]))
    assert not b.healing  # v8 rule: never heal outside the zone (regen is off there)


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


# ----------------------------------------------------------------- v15: no chasing late
@test
def h1_late_wounded_far_not_chased():
    b = bot()
    b.act(make_obs(t=240.0, mechs=[mech(7, 0, 200, hp=500)]))
    assert b.target_id is None


@test
def h2_late_attacker_still_fought():
    b = bot()
    a = b.act(make_obs(t=240.0, mechs=[mech(5, 150, 0)], events=[hit(5)], aim=(0.0, 0.0)))
    assert b.target_id == 5


@test
def h3_early_wounded_still_chased():
    b = bot()
    b.act(make_obs(t=200.0, mechs=[mech(7, 0, 200, hp=500)]))
    assert b.target_id == 7


# ----------------------------------------------------------------- v22: become the biggest mech
def crate(cid, x, y, z=0.0):
    return {"id": cid, "pos": [x, y, z], "hp": 300}


@test
def l1_gun_breaks_nearby_crate_when_aimed():
    b = bot()
    o = make_obs(t=30.0, weapons=[gun(), None], aim=(0.0, 0.0)); o["crates"] = [crate(1001, 20, 0)]
    a = b.act(o)
    assert a["fire"][0] is True and abs(a["aim"][0]) < 1e-6, a


@test
def l2_laser_crate_shot_waits_for_full_charge():
    b = bot()
    o = make_obs(t=30.0, weapons=[gun(), laser(charge=0.7)], aim=(0.0, 0.0)); o["crates"] = [crate(1001, 20, 0)]
    assert b.act(o)["fire"][LASER] is True, "0.7 s charge does ~301: too close to 300 HP"
    o = make_obs(t=30.1, weapons=[gun(), laser(charge=0.75)], aim=(0.0, 0.0)); o["crates"] = [crate(1001, 20, 0)]
    assert b.act(o)["fire"][LASER] is False, "full charge and aimed: fire"


@test
def l3_roof_crate_and_far_crate_ignored():
    b = bot()
    o = make_obs(t=30.0, weapons=[gun(), None], aim=(0.0, 0.0)); o["crates"] = [crate(1001, 20, 0, z=12), crate(1002, 80, 0)]
    a = b.act(o)
    assert a["fire"] == [False, False]


@test
def l4_no_crate_while_a_mech_is_in_view():
    b = bot()
    o = make_obs(t=30.0, weapons=[gun(), None], mechs=[mech(5, 0, 150)], aim=(0.0, 0.0)); o["crates"] = [crate(1001, 20, 0)]
    a = b.act(o)
    assert a["fire"][0] is False and abs(a["aim"][0] - math.pi / 2) < 1e-6


@test
def l5_cubes_past_the_cap_still_collected():
    b = bot()
    o = make_obs(t=30.0, cubes=12); o["zone"]["next_center"] = [0, -100]; o["cubes"] = [{"id": 5001, "pos": [30.0, 0.0, 0.0]}]
    a = b.act(o)
    assert a["move"][0] > 0.99, a["move"]


@test
def l6_idle_cube_reach_60m():
    b = bot()
    o = make_obs(t=30.0); o["zone"]["next_center"] = [0, -100]; o["cubes"] = [{"id": 5001, "pos": [55.0, 0.0, 0.0]}]
    a = b.act(o)
    assert a["move"][0] > 0.99, a["move"]


# ----------------------------------------------------------------- v26: collect our kills' cubes
def kill_setup(b, t=40.0, at=(150.0, 0.0)):
    b.act(make_obs(t=t - 0.1, mechs=[mech(9, at[0], at[1], hp=100)]))


def loot_obs(t, cube_at=(150.0, 2.0), events=(), mechs=()):
    o = make_obs(t=t, events=list(events), mechs=list(mechs))
    o["zone"]["next_center"] = [0, -100]
    o["cubes"] = [{"id": 5001, "pos": [cube_at[0], cube_at[1], 0.0]}]
    return o


@test
def m1_walk_to_our_kill_cubes_150m():
    b = bot(); kill_setup(b)
    a = b.act(loot_obs(40.0, events=[{"type": "kill", "target": 9}]))
    assert a["move"][0] > 0.99, a["move"]


@test
def m2_not_while_being_shot():
    b = bot(); kill_setup(b)
    a = b.act(loot_obs(40.0, events=[{"type": "kill", "target": 9}, hit(5)], mechs=[mech(5, 0, -60)]))
    assert a["move"][0] < 0.9, a["move"]


@test
def m3_old_kill_forgotten():
    b = bot(); kill_setup(b)
    b.act(loot_obs(40.0, events=[{"type": "kill", "target": 9}]))
    a = b.act(loot_obs(70.0))
    assert a["move"][0] < 0.9, a["move"]


@test
def m4_far_random_cube_still_ignored():
    b = bot()
    a = b.act(loot_obs(40.0))
    assert a["move"][0] < 0.9, a["move"]
# v24: trace the commanded ray to the target's x-plane, independently of the intercept solver.
def gun_impact(distance, target_vel, own_vel, delay, target_cubes=0, own_cubes=0, z=0):
    target = mech(5, distance, 0, hp=500, vel=target_vel)
    target.update(pos=[distance, 0, z], cubes=target_cubes)
    obs = make_obs(mechs=[target], weapons=[gun(cooldown=delay), None], cubes=own_cubes)
    obs["self"]["vel"] = own_vel
    b = bot()
    yaw, pitch = b.act(obs)["aim"]
    obs["self"]["aim"] = [yaw, pitch]
    assert b.act(obs)["fire"][0]
    ray = (math.cos(pitch)*math.cos(yaw), math.cos(pitch)*math.sin(yaw), math.sin(pitch))
    scale = 1 + 0.05 * own_cubes
    origin = [v * delay + (2.5 * scale + 0.5) * r for v, r in zip(own_vel, ray)]
    origin[2] += 7 * scale
    flight = (distance + target_vel[0] * delay - origin[0]) / (252 * ray[0] - target_vel[0])
    impact = [p + 252 * r * flight for p, r in zip(origin, ray)]
    center = [p + v * (delay + flight) for p, v in zip(target["pos"], target_vel)]
    center[2] += 4.5 * (1 + 0.05 * target_cubes)
    assert 0 < 252 * flight <= 230
    assert math.dist(impact, center) < 1e-7, (impact, center)
    return pitch


@test
def stationary_cube_scaled_target():
    gun_impact(80, (0, 0, 0), (0, 0, 0), 0.05, target_cubes=14, own_cubes=4)


@test
def crossing_target_with_moving_shooter():
    for distance in (50, 150, 220):
        for delay in (0.05, 0.1):
            gun_impact(distance, (0, 19.5, 0), (4, -10, 2), delay)


@test
def jumping_target_pitch():
    assert gun_impact(150, (0, 0, 11), (0, 0, 2), 0.05, z=2) > 0


@test
def gun_rejects_off_body_actual_aim():
    target = mech(5, 150, 0, hp=500)
    pitch = math.atan2(-2.5, 150)
    for aim in [(0, pitch + deg(2)), (deg(1.1), pitch)]:
        assert not bot().act(make_obs(mechs=[target], weapons=[gun(), None], aim=aim))["fire"][0]


@test
def laser_requires_pitch_to_release():
    obs = make_obs(mechs=[mech(5, 100, 0, hp=500)], weapons=[gun(), laser(charge=0.70)], aim=(0, deg(5)))
    b = bot()
    act = b.act(obs)
    assert act["fire"][LASER]
    obs["self"]["aim"] = act["aim"]
    assert not b.act(obs)["fire"][LASER]


@test
def position_history_refines_both_leads():
    for weapon in (gun(), laser(charge=0.75)):
        b = bot()
        for t, y in [(20, -1), (20.1, 0)]:
            obs = make_obs(t=t, mechs=[mech(5, 100, y, hp=500)], weapons=[weapon, None])
            tracked = b.act(obs)["aim"][0]
        assert tracked > bot().act(obs)["aim"][0]
        obs["t"] += 1  # Reacquisition drops the old position difference.
        assert b.act(obs)["aim"][0] == 0


# ----------------------------------------------------------------- v29: push weaker isolated targets
@test
def p1_push_weaker_target():
    b = bot()
    o = make_obs(t=60.0, mechs=[mech(5, 120, 0, hp=600)], events=[hit(5)]); o["zone"]["next_center"] = [0, -100]
    a = b.act(o)
    assert a["move"][0] > 0.99, a["move"]


@test
def p2_no_push_when_second_mech_close():
    b = bot()
    o = make_obs(t=60.0, mechs=[mech(5, 120, 0, hp=600), mech(6, -50, 0)], events=[hit(5)])
    o["zone"]["next_center"] = [0, -100]
    a = b.act(o)
    assert a["move"][0] < 0.9, a["move"]


@test
def p3_no_push_equal_target_or_low_hp_or_late():
    for kw, m in ((dict(t=60.0), mech(5, 120, 0, hp=1400)), (dict(t=60.0, hp=700), mech(5, 120, 0, hp=300)),
                  (dict(t=240.0), mech(5, 120, 0, hp=600))):
        b = bot()
        o = make_obs(mechs=[m], events=[hit(5)], **kw); o["zone"]["next_center"] = [0, -100]
        a = b.act(o)
        assert a["move"][0] < 0.9, (kw, a["move"])


@test
def p4_push_smaller_by_cubes():
    b = bot()
    m = mech(5, 120, 0, hp=1400); m["cubes"] = 0
    o = make_obs(t=60.0, mechs=[m], events=[hit(5)], cubes=4); o["zone"]["next_center"] = [0, -100]
    o["self"]["max_hp"] = 1624; o["self"]["hp"] = 1624
    a = b.act(o)
    assert a["move"][0] > 0.99, a["move"]


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
