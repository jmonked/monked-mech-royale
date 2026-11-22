# v39 tactical coverage gaps — adversarial scenario recipes

Bot under test: `c8e98e1:example_bot.py` (1631 lines; line numbers below are that file).
Coverage input: `COVERAGE-corpus-only.md` (3472 corpus scenarios, 316/490 arcs) and
`COVERAGE.md` (same corpus + 800 Hypothesis states, 355/490).
Recipes are one `Bot.act()` call. `state` is the bot memory snapshot restored by
`scenario_lab.restore()`; build it as Python literals and run `scenario_lab.enc()` on it
(tuples become `{"__t__": [...]}`, int-keyed dicts become `{"__d__": ...}`).
`flat: true` removes `buildings/los_buildings/roofs`; `flat: false` loads
`buildathon/kit/mechfight-kit/arena/v2/world.json` via `_load_prisms()`.

## Shared flat base (override per recipe)

```python
obs = {
  "type": "obs", "tick": 1001, "t": 50.0, "alive": 16,
  "self": {"id": 0, "pos": [0.0, 0.0, 0.0], "vel": [0.0, 0.0, 0.0],
           "aim": [0.0, 0.0], "hp": 1400.0, "max_hp": 1400.0,
           "energy": 100.0, "max_energy": 100.0, "grounded": True,
           "cubes": 0, "upgrades": [], "in_zone": True,
           "weapons": [{"kind": "gun", "cooldown": 0.0, "ammo": 12, "reload": 0.0,
                        "stats": {"damage": 45, "cooldown": 0.24, "speed": 252,
                                  "range": 230, "spread_deg": 0.6, "mag": 12,
                                  "reload": 2.4}}, None],
           "stats": {}},
  "mechs": [], "projectiles": [], "crates": [], "cubes": [], "pickups": [],
  "sounds": [], "beams": [], "events": [], "drops": [],
  "zone": {"center": [0.0, 0.0], "radius": 400.0,
           "next_center": [0.0, 0.0], "next_radius": 350.0,
           "shrink_start": 0.0, "shrink_end": 400.0, "dps": 10},
  "offer": None}
state = {}
```

Map helper (for `[map]` recipes):

```python
R = runner("c8e98e1").template.roofs[k]     # (idx, center, radius, ring, holes, base, top, climbs)
B = runner("c8e98e1").template.buildings[k] # (center, radius, ring, holes, base, top)
# R[1]=center, R[2]=radius, R[5]=base, R[6]=top, R[7]=climb points
# B[0]=center, B[1]=radius, B[4]=base, B[5]=top
```

---

## 1. Finals trip: non-our deaths, and the `recent_dealt` suppressor  `[flat]`

**Gap:** `_act` L1420–1428. Corpus never takes L1424→[1425] (`not recently_hit_any`) or
L1426→[1427] (`non_our_deaths >= 2`). This enables Finals FFA mode (silent walk, FFA
targeting, aggressive push rules), so missing it changes the whole late game.

**Recipe A — trip:**
```python
obs["t"] = 60.0; obs["alive"] = 6
obs["self"]["stats"] = {"walk_speed": 4.0}   # keep silent-walk out of this recipe
state.update(prev_alive=8, non_our_deaths=0, is_finals=False, finals_t=None,
             recent_dealt={}, killed=set())
```
`alive 8→6`, no kill event, no recent dealt damage → `delta_deaths=2`; L1425/1427 true.
**Expected:** `bot.is_finals is True`, `bot.non_our_deaths == 2`, `bot.finals_t == 60.0`,
`bot.prev_alive == 6`; no exception, normal action.
**Safe behavior:** switch to FFA only for deaths that cannot be explained by our kills.

**Recipe B — our kill explains one death:** add
`obs["events"] = [{"type": "kill", "target": 5}]`; `new_kills=1`, so
`delta_deaths=1`; `non_our_deaths=1`, **no** trip.

**Recipe C — suppressor bug:** `state.recent_dealt = {2: 59.0}` with the same 8→6 drop.
`recently_hit_any` is true, so L1425 is skipped; `prev_alive` still becomes 6 and the two
deaths are lost forever (`is_finals` stays False). This is the dangerous interaction in §I6.

---

## 2. Finals silent walk, and zone-run overriding it  `[flat]`

**Gap:** `_act` L1580–1587, L1583→[1584]. Corpus never scales move by
`(step_speed-0.2)/walk_speed`. Needed so Finals approaches are not heard at full walk speed.

**Recipe:**
```python
obs["t"] = 200.0; obs["tick"] = 4001
obs["zone"].update(next_center=[0.0, 0.0], next_radius=300.0, shrink_end=400.0)
obs["self"]["stats"] = {"walk_speed": 11.7}
state.update(is_finals=True, finals_t=180.0, drop_id=None)
# no mechs, cubes, drops, pickups; hp full so _heal is false
```
`_movement` returns `"zone"`, `act["move"]` is unit length, boost false; L1583 true →
scale `(5-0.2)/11.7 = 0.410`.
**Expected:** `action["move"] ≈ [0.410, 0]` (direction of `next_center`), `boost` false,
label contains `"silent"`; `bot.is_finals` stays True.
**Safe behavior:** silent only while not time-critical and not being shot.

**Variant — silent defeated by zone-run:** set
`zone.next_center=[200,0]`, `zone.next_radius=50`, `zone.shrink_end=202.0`,
`me.pos=[45,0,0]` (inside current zone). Zone-run at L1591-1600 sets a full-speed
move and `boost=True` after the silent scaling. Expected label contains both `silent`
and `zone-run`, net move `[1,0]`, boost true. This is the Finals-approach/zone-run conflict.

---

## 3. Mortar dodge, urgency ordering, and zone-edge validation  `[flat]`

**Gap:** `_projectile_dodge` L412–434 (mortar branch entirely absent: corpus only reaches
gun bullets); L428 urgency ordering; L470–472 (`_validate_dodge_vec` returning `None`).
Mortars do 200 + splash and concuss; never dodging them is the largest survival gap.

**Recipe A — dodge one shell:**
```python
obs["self"]["pos"] = [0.0, 0.0, 0.0]; obs["self"]["vel"] = [0.0, 0.0, 0.0]
obs["projectiles"] = [{"id": 900, "kind": "mortar",
                       "pos": [20.0, 0.0, 10.0], "vel": [-26.0, 0.0, -5.0]}]
```
`disc = 25 + 2*22*10 = 465`, `t_land = (-5+21.56)/22 = 0.753`, impact `[0.42,0,0]`,
`d=0.42 < mortar_splash (8.2)` → urgency `3/0.753 = 3.98`, vector away from impact
`[-1,0]`, `need_boost = t_land<=0.9 and energy>=20` → true.
**Expected:** `action["move"] == [-1,0]`, `boost` true, label `"zone dodge"`.

**Recipe B — urgency ordering:** add a gun bullet that would hit in 0.24 s
`{"id":901,"kind":"gun","pos":[60,0,4.5],"vel":[-250,0,0]}` and make the mortar land in
1.0 s (e.g. shell `pos [20,0,10]`, `vel [-10,0,-5]`). Gun urgency `1.6/0.24=6.67` beats
mortar `3.0/1.0=3.0` → move perpendicular to the bullet (`[0,-1]`), boost false.
Invert the times (mortar 0.4 s, gun 0.5 s) → mortar vector wins. This pins L428–433.

**Recipe C — dodge rejected at the zone edge (L471 true):** me `[10,0,0]`, zone
`next_center=[0,0]`, `next_radius=10.0`, gun bullet `pos [-50,0,4.5]`, `vel [250,0,0]`
(impact in 0.24 s). Perpendicular candidates `[0,±1]` put the 5 m look-ahead at distance
`11.18 > 10`, both rejected → `_validate_dodge_vec` returns None.
**Expected:** no dodge override (label has no `dodge`), bot stays rather than leaving the
zone. **Safe behavior should be** a tangential/inward move that stays inside the circle,
not stand still.

**Recipe D — reversal into the blast:** me `[9.5,0,0]`, zone radius 10; shell impact at
`[10.5,0]` (outside). Away vector `[+1,0]` is rejected, `[-1,0]` is accepted.
**Expected:** `action["move"] == [-1,0]` (toward the impact) even though the blast is
outside the zone. This is interaction §I5; the validator checks only the circle, not
blast safety.

---

## 4. Bullet-dodge rejection gates: vertical miss, co-moving, time window  `[flat]`

**Gap:** corpus never takes L440→[441] (`rv2 <= 1`), L449→[450] (vertical miss),
L444→[446] (t_hit outside 0.20–0.65); also L408→[409] (missing pos/vel). These gates stop
the bot wasting a sidestep on bullets that cannot hit.

**Recipe A — vertical miss:**
```python
obs["self"]["pos"] = [0.0,0.0,0.0]; obs["self"]["vel"] = [0.0,0.0,0.0]
obs["projectiles"] = [{"id":901,"kind":"gun","pos":[60.0,0.0,14.5],
                       "vel":[-250.0,0.0,0.0]}]
```
`t_hit=0.24`, horizontal miss 0, but `dz = 4.5-14.5 = -10`, threshold
`0.5*my_h+1.0 = 5.5` → skip at L449.
**Expected:** no `dodge` label, no move override.

**Recipe B — co-moving projectile:** me `vel=[5,0,0]`, projectile
`pos=[40,0,4.5]`, `vel=[5,0,0]` → `rv2=0 <=1` → skip at L440.

**Recipe C — timing window:** with me at origin, gun bullets at 10 m (`t=0.04`) and 200 m
(`t=0.80`) both pass the vertical test but fail `0.20 <= t_hit <= 0.65`.
**Expected:** no dodge for either; do not thrash when the bullet is already too close or
still too far.

**Recipe D — malformed projectile:** `{"id":902,"kind":"gun","pos":null,"vel":[0,0,0]}`
and one with `vel:null` → skipped at L408 without exception.

---

## 5. NPC bullets are ignored while drop-holding/pushing  `[flat]`

**Gap:** `_projectile_dodge` L436→[437] (`kind == "npc" and ignore_npc`) never taken.
The call site L1605 passes `ignore_npc=(pushing or holding_drop)`, so a drone can chip the
bot while it protects a supply drop. Drones do 25 damage per second and are otherwise
ignored by `_choose_target`.

**Recipe — hold a drop at low HP under drone fire:**
```python
obs["self"].update(pos=[0.0,0.0,0.0], hp=400.0, in_zone=True,
                   stats={"walk_speed": 11.7})
obs["drops"] = [{"id": 20000, "pos": [0.0,0.0,0.0], "radius": 8.0,
                 "lands_in": 0.0, "capture_s": 4.0, "progress": 1.0,
                 "holder": None}]
obs["projectiles"] = [{"id": 901, "kind": "npc",
                       "pos": [60.0,0.0,4.5], "vel": [-250.0,0.0,0.0]}]
state.update(drop_id=20000, drop_retry_at={}, drop_contested_since={})
```
`_drop_goal` L719 returns the active in-ring drop; `_movement` returns
`"drop-hold 1.0/4s"`; `holding_drop=True`; `progress 1.0 < 2.5` so the dodge call is not
skipped; NPC projectile is discarded at L436.
**Expected:** `action["move"] == [0,0]`, label contains `"drop-hold"`, no `dodge`.
**Safe behavior:** deliberately ignore NPC chip while capturing (current design), but it
should abort at low HP or when a second drone joins; test hp 400 here documents the risk.
**Variant:** add a gun projectile with the same trajectory → gun dodge still fires while
the NPC bullet is ignored (`ignore_npc=True`, `ignore_mortar=False`).

---

## 6. Blocked-target laser package: alternate target, full-charge release, gun reload  `[map]`

**Gap:** `_fight` L1102–1107 (blocked charging laser switches to an alternate visible
target), L1113–1114 (blocked + full charge ≥1.6 s releases), L1093–1094 (blocked gun with
ammo ≤6 starts reload). All three need real geometry because `_target_blocked` only uses
`los_buildings`; flat worlds can never take them.

**Geometry:**
```python
B = runner("c8e98e1").template.buildings[k]      # height >= 9
me["pos"]     = [B[0][0] - B[1] - 15.0, B[0][1], B[4]]
target["pos"] = [B[0][0] + B[1] + 15.0, B[0][1], B[4]]
me["aim"] = [0.0, 0.0]                           # facing the blocked target
target.update(id=1, kind="mech", hp=300.0, max_hp=1400.0, cubes=0,
              weapons=["gun"], charging=False)
state["last_hits"] = {1: (t - 1.0, 0.0)}
assert bot._target_blocked(me, target) is True
```

**A — alternate target:** add alt `id=2` at `me.pos + [10*cos(0.2), 10*sin(0.2), 0]`
(in front of the building, clear LOS), hp 1400, visible. `me.weapons = [gun,
{"kind":"laser","charge":0.4,"cooldown":0.0,"stats":{}}]`, `state["target_id"]=1`.
`_choose_target` picks the 300-HP blocked target; `_fight` finds alt within 30° and flips
`blocked=False`.
**Expected:** `bot.laser_target == 2`, `action["fire"][1] is True` (hold charge), action aim
toward alt; no beam dumped into the wall.

**B — full charge behind the wall:** remove the alt, set laser `charge=0.9`,
`cooldown=0`, `state["laser_full_since"] = t - 1.7`.
L1113 true → `charging=False` → release.
**Expected:** `action["fire"][1] is False`, `bot.laser_released is True`; do not hold a
full charge forever behind cover.

**C — blocked gun reload:** weapons `[{"kind":"gun","ammo":4,"reload":0.0,
"cooldown":0.0,"stats":{}}, None]`, same blocked target. L1093 true.
**Expected:** `action["reload"] is True`, `fire[0] is False`; reload while the target is
unhittable instead of standing with 4 rounds.

---

## 7. Lightning branch  `[flat]`

**Gap:** `_fight` L1119–1124 never entered in corpus (no scenario gives the bot lightning).
Lightning is the anti-laser weapon (short) and costs 3 energy/shot; the bot must use it only
inside 0.9×range and inside 0.4×cone of its *actual* aim.

**Recipe:**
```python
obs["self"]["aim"] = [0.0, -0.083]
obs["self"]["weapons"] = [base_gun,
    {"kind": "lightning", "cooldown": 0.0, "stats": {}}]
obs["mechs"] = [{"id": 1, "kind": "mech", "pos": [30.0,0.0,0.0],
                 "vel": [0,0,0], "aim": [math.pi,0.0], "hp": 1000.0,
                 "max_hp": 1400.0, "cubes": 0, "weapons": ["gun","laser"],
                 "charging": False}]
```
Distance 30 ≤ `0.9*45=40.5`, energy 100 ≥10, LOS clear; `aligned(direct_yaw, 12°)` true.
**Expected:** `action["fire"][1] is True`, action aim yaw 0, gun also fires.
**Variants:** energy 9 → `fire[1]` false and no direct aim; distance 42 m → no lightning;
blocked target `[map]` → no lightning and no gun through the wall. **Safe behavior:** save
energy outside the effective envelope; the 0.9 factor and 12° gate prevent wasted arcs.

---

## 8. Laser sidestep: `aim=None`, rooftop preference, invalid candidate  `[flat + map]`

**Gap:** `_laser_sidestep` L489→[490] (`aim` missing/None), L504→[505] and L506→[507]
(roof branch and roof-center preference), L512→[513] candidate rejected. A charging enemy
laser is the highest-damage threat (315); standing still is usually fatal.

**A — `aim=None` robustness `[flat]`:**
```python
obs["mechs"] = [{"id":1,"kind":"mech","pos":[60.0,0.0,0.0],"vel":[0,0,0],
                 "aim":[None,0.0],"hp":1000.0,"max_hp":1400.0,"cubes":0,
                 "weapons":["gun","laser"],"charging":True}]
```
Distance 60 > `near_range` 45, no hits/wound → target is None; `_laser_sidestep` skips at
L489. **Expected:** no exception, no `ldodge`, normal zone movement. Do not crash on a
partially visible mech.

**B — rooftop sidestep `[map]`:** `R` with radius ≥8; me
`[R[1][0]+6, R[1][1], R[6]]` (on roof, 6 m from center), enemy at
`[R[1][0]+66, R[1][1], R[6]]`, `charging=True`, `aim=[math.pi,0]` (pointing at me),
hp 1000, `weapons=["gun","laser"]`. Zone `next_center=R[1]`, `next_radius=300`.
`_current_roof` is not None → L504 true; the candidate whose 5 m point is closer to the
roof center is chosen at L506.
**Expected:** lateral move (`[0,±1]`), `boost` true if energy ≥35 and distance ≤160,
label `"ldodge"`; never step off the roof to dodge.

**C — no valid candidate at the roof edge `[map]`:** me `[R[1][0]+7.5, R[1][1], R[6]]`
with roof radius 8. Both 5 m lateral candidates are at distance `9.01 > 8` and are
rejected at L512. **Expected:** no `ldodge`, bot holds position/keeps its previous move
rather than walking off the edge; document the cost (may eat the beam).

---

## 9. Third-party cover on a roof, and its distance gate  `[map]`

**Gap:** `_act` L1513–1520 (roof branch) and L1517→[1518] (`d > 2.0`) never taken. When a
second mech hits us mid-duel, the correct move on a roof is to pull to the roof center, not
to chase or to run off the edge.

**Recipe:**
```python
R = ...; me["pos"] = [R[1][0]+6, R[1][1], R[6]]
obs["mechs"] = [{"id":1,"kind":"mech","pos":[R[1][0]+36,R[1][1],R[6]],
                 "vel":[0,0,0],"aim":[math.pi,0],"hp":1000.0,"max_hp":1400.0,
                 "cubes":0,"weapons":["gun"],"charging":False}]
state.update(is_finals=True, target_id=1,
             last_hits={1:(t-0.5, math.pi), 2:(t-0.5, 2.0)})
# id 2 is deliberately not in obs["mechs"]: only its damage bearing is known
obs["zone"].update(next_center=R[1], next_radius=300.0)
```
Target 1 is selected; `movement` returns `"roof"`; `tp_hit` id 2 is within 2.5 s and not the
target; `tp_m` is None but the bearing is available → threat point 80 m along 2.0 rad.
`on_roof` is not None and `d=6 > 2` → move to roof center, `boost=False`.
**Expected:** `action["move"]` toward `R[1]`, `boost` false, label contains `"tp-cover"`.
**Variant — already centered:** me at `R[1]` + 1.5 m; L1517 false → no `tp-cover`; keep
fighting. **Safe behavior:** only reposition when there is room to do so; never run toward a
third party whose position is unknown.

---

## 10. Reload cover: rooftop and ground distance gates  `[map]`

**Gap:** `_act` L1537→[1539] (on-roof), L1541→[1542] (`d > 2`), L1549→[1550]
(`2.0 < d <= 40.0` on the ground) never taken. With an empty gun and the laser on cooldown,
standing in the open is a free kill.

**A — rooftop reload cover:** me `[R[1][0]+6,R[1][1],R[6]]`, target
`[R[1][0]+36,R[1][1],R[6]]` hp 1000, `state.last_hits={1:(t-0.5, math.pi)}`,
weapons `[{"kind":"gun","ammo":0,"reload":1.2,"cooldown":0.0,"stats":{}}, None]`,
`state.is_finals=True`, zone centered on `R[1]`.
`reloading=True`, `laser_busy=True`, `being_shot=True`, target not blocked, `on_roof` true,
`d=6 > 2`. **Expected:** move toward roof center, `boost` false, label contains `"cover"`.

**B — ground reload cover:** flat false; choose `B` (height ≥9), me at
`[B[0][0]+B[1]+5, B[0][1], B[4]]`, target 20 m further out on the same side (visible, not
blocked), same reload state. `_find_cover` returns the far-side spot;
`2 < dist(me, spot) <= 40`.
**Expected:** move toward the cover spot, `boost` true if energy ≥30 and distance >10,
label `"cover"`.
**C — already safe:** put the target behind `B` so `_target_blocked` is true; L1535 false →
no cover move (stay behind the wall and finish the reload).
**Safe behavior:** never walk off a roof for reload cover; on the ground only move if the
spot is within 40 m and inside the next circle (`_find_cover` already enforces the circle).

---

## 11. Heal geometry: rooftop heal, safe-above, cover walk distance gate  `[map]`

**Gap:** `_heal` L567→[568] (roof branch), L587→[595] (`distance <= 3` hold-at-spot),
L590→[595] (no cover spot fallback), L576→[577] (`threat is None`), L563→[567]
(last-mech-bearing fallback). Corpus only tests flat, full-HP-ish heals.

**A — rooftop heal:** `R`; me `[R[1][0],R[1][1],R[6]]`, hp 600/1400, in_zone, no mechs,
`state.healing=False`, `is_finals=False`, weapons `[gun,None]`.
`_heal` L547 on_roof; nearest None; L567 true → healing True, move `[0,0]` if within 2.5 m
of center, aim `[me.aim[0],0]`.
**Expected:** `bot.healing is True`, label `"roof-heal 43%"`, no dodge/fight.
**Variant — move to center:** me at `R[1] + 6 m`; move is the unit vector toward center.

**B — safe above:** add NPC/mech `id=1` at `[R[1][0], R[1][1], R[5]]` (inside the building
footprint below the roof), hp 1000. 3D distance is within `near_range`, so a normal heal
would abort, but `pos.z - enemy.z >= 7` and `_target_blocked(me, enemy)` is true →
`safe_above` true. **Expected:** still heal on the roof. If the enemy is placed just
outside the footprint (LOS clear), `safe_above` false → heal aborts; target is selected and
the bot fights instead. **Safe behavior:** healing is allowed only when the roof actually
breaks the enemy's line of fire.

**C — ground cover walk:** `B`; me at `[B[0][0]+B[1]+30, B[0][1], B[4]]`, hp 600, threat
mech at `[B[0][0]-B[1]-30, B[0][1], B[4]]` (60 m, no hits, hp 1000 so `_choose_target`
returns None), zone centered near me radius 300. `_heal` proceeds (nearest >45 m);
`_find_cover` returns the far-side spot; `distance > 3` → move to spot, boost true if
energy ≥30 and distance >20.
**Expected:** label `"heal 43%"`, move toward the cover spot.
**D — close gate:** after computing the spot, place me 2 m from it; L587 false → move
`[0,0]`, no boost, still `healing=True`. **E — no threat:** no mechs and no
`last_mech_bearing` → L576 true, hold still and heal.

---

## 12. Target selection: unknown HP (`eff_hp is None`) and sticky switching  `[flat]`

**Gap:** `_choose_target` L690→[691] (`eff_hp is None`) and L700→[702] (the switch branch)
never taken. The protocol only shows enemy `hp` when `vision.show_enemy_hp` is enabled, so
unknown-HP targets are a real match state. Sticky targeting prevents thrash but can keep
the bot on a full-HP target while a nearly dead one escapes.

**A — unknown HP:** one mech `id=1` at 30 m with **no `hp`/`max_hp` keys** (or `null`),
no hits. Distance ≤ `near_range` makes it eligible; `_eff_hp` returns None; rank is
`(inf, 0, distance)`.
**Expected:** `bot.target_id == 1`; label `"fight 1 hp ?"`; gun still fires at the body
(`_fight` uses geometry, not hp). Do not skip an enemy just because hp is hidden.

**B — switch on a much weaker target:** `state.target_id=1`; mech 1 at 30 m hp 1200;
mech 2 at 60 m hp 100 (wounded ≤50% and within gun range 230, so eligible).
`cur_eff=1200`, `best_eff=100 < 0.6*1200` → switch.
**Expected:** `bot.target_id == 2`, label `fight 2`; do not stay glued to the healthy target.

**C — stick when the new target is not weak enough:** same but mech 2 hp 800 with a recent
hit (to be eligible). `800 >= 0.6*1200=720` → keep current.
**Expected:** `bot.target_id == 1`; prevents target thrash between two similar targets.

**D — unknown current HP sticks:** `target_id=1`; mech 1 at 30 m with no hp; mech 2 at
60 m hp 50. `cur_eff is None` → keep current, even though mech 2 is nearly dead.
**Expected:** `bot.target_id == 1`. Document this as a deliberate conservative rule (or a
bug if the weak target is escaping).

**E — LATE_T gate:** `t=240`, mech at 100 m, hp 500 (wounded, within laser reach), no
recent hit. L685 true → skipped. **Expected:** no target/chase after 230 s for a distant
wounded target; only nearby or recently-shooting targets are engaged.

---

## 13. Beam threat: return fire at the origin, then face it  `[flat, blocked variant map]`

**Gap:** `_shoot_beam_origin` is 1/10 arcs; corpus never has `last_beam_threat`.
`_face_bearing` L1351→[1352] (beam-threat fallback) is also never taken. A laser/lightning
beam reveals the shooter's muzzle; the bot should return gun fire if it is in range and
unblocked, and at least face the origin when the window has passed.

**A — return fire:** keep `mechs=[]` (so `_shoot_beam_origin` is reached), gun ammo 12,
reload 0, `me.aim=[0,0]`; `obs["beams"] = [{"by": 5, "kind": "laser",
"path": [[120.0,0.0,7.0],[0.0,0.0,7.0]], "age": 0.3}]`.
`_remember_beams` sets `last_beam_threat=(t-0.3, 0.0, [120,0,7])`; age ≤0.8, origin length
3, distance 120 ∈ [5,230], no building in flat world. Aim point `[120,0,4.5]`; yaw 0,
pitch −0.0208; actual aim [0,0] passes the 1.19°/2.15° gates.
**Expected:** label `"beam-ret"`, `action["aim"] ≈ [0,-0.021]`, `fire[0] is True`.
**B — stale beam:** same with `age=1.5`; `_shoot_beam_origin` returns False (>0.8), then
`_face_bearing` uses `last_beam_threat` (≤3 s) → `action["aim"]=[bearing,0]`, state
`"face"`. This is L1351.
**C — out of gun range:** origin `[300,0,7]`, age 0.3 → no fire; face the origin only.
**D — blocked origin `[map]`:** place the shooter's muzzle on the far side of `B`; assert
`bot._building_blocked(muzzle_pos, aim_pt)` true. `_shoot_beam_origin` returns False; the
bot may face the origin but must **not** fire through the wall.
**Safe behavior:** return fire only with a current, in-range, unblocked origin; never
blind-fire at a stale beam.

---

## 14. Drone that is attacking us, and drone gates  `[flat, blocked variant map]`

**Gap:** `_shoot_drone` L1176/L1178/L1184 (`attacking_us` path and rank preference),
L1180 (height/zone gate), L1182 (LOS), L1187 (best None) mostly untaken.
NPCs are ignored by `_choose_target`; a drone that shot us must be handled here or it keeps
chipping 25 damage/s.

**A — attacking drone:** `mechs=[{"id":101,"kind":"npc","pos":[30,0,0],"vel":[0,0,0],
"aim":[math.pi,0],"hp":350,"max_hp":350}]`, `state.last_hits={101:(t-1.0, math.pi)}`,
`me.aim=[0,-0.1736]`, gun ready. `attacking_us=True`, `abs(dz)=0`, inside next circle, LOS
clear; rank `(0,30)`.
**Expected:** label `"drone"`, `fire[0] is True` at the drone; no chase of a mech.
**B — farm path:** no `last_hits`, cubes 0, `t=50` (<230), distance 30 ≤55 → `farm_ok`,
rank `(1,30)`; fire for the 2 cubes.
**C — priority:** add drone 102 at 10 m (no hit) and drone 101 at 40 m (hit). Rank 0 wins
over rank 0/1 distance, so the attacker is shot first even though it is farther.
**D — height gate:** drone z=6 (dz 6 >4) → skipped; no drone fire.
**E — zone gate:** drone at 100 m while `next_center=[0,0]`, `next_radius=50` → skipped.
**F — blocked `[map]`:** drone behind `B`; `_target_blocked` true → skipped; do not waste a
magazine on a wall.
**Safe behavior:** prioritize the drone that hit us, then farm only inside 55 m and inside
the next circle; never chase above/below by more than 4 m.

---

## 15. Roof claim/climb/walk/hold  `[map]`

**Gap:** `_movement` L899→[900], L901→[902], L927→[928], L937→[938/945] never taken; the
whole roof-fortress plan is absent from the corpus. In Finals/late game the bot should use
a rooftop laser position instead of standing in the open.

**Setup:** `flat=false`, `state.is_finals=True`, `me.hp=1400`, weapons `[gun, laser]`,
`zone.next_center=R[1]`, `zone.next_radius=300`, no mechs/cubes/drops/pickups,
`me.energy=100`, `me.grounded=True`.

**A — claim and climb:** choose `R` with `top-base` in 9..45 and a valid climb point;
place me at `[R[7][0][0], R[7][0][1], R[5]]` (ground at a climb point) so `d_climb=0`.
`_pick_roof_goal` accepts (height ≤45, energy ≥max(45, climb_h/0.6+10), roof center inside
`next_radius-radius-4`, climb ≤140). L899 true, roof_goal set, L937 true.
**Expected:** `bot.roof_goal` is not None; label `"roof-climb"`;
`action.jump is True`, `action.boost is True` (energy ≥15), move toward `R[1]`;
`roof_goal[4]` (climb_started) is set.
**B — hold the roof:** me `[R[1][0],R[1][1],R[6]]` → `_current_roof` true, center inside
next circle, `d<=4`: L901/902 → roof_goal None, move `[0,0]`, label `"roof"`.
**C — walk to the climb point:** me on the ground 30 m from a climb point,
`state.roof_goal=[R[0], R[7][0], R[1], R[6], None, 100.0, t-1.0]`. L927 false,
`d_climb=30 >6` → L945 true.
**Expected:** label `"roof-walk"`, move toward the climb point, `boost` false.
**D — timeout:** same but `climb_started=t-7` and me below `top-1` → L922 true, L924
marks `R[0]` unreachable and clears the goal; `_pick_roof_goal` then skips that roof.
**Expected:** `R[0] in bot.unreachable_roofs`; no infinite climb. **Safe behavior:** do not
burn jet energy on a roof outside the next circle; give up after 8 s of no progress or 6 s
of failed climb.

---

## 16. Weapon pickup: take a laser / swap out lightning  `[flat]` (lower priority)

**Gap:** `_movement` L834→[836] (`take`) and L837→[838] (drop lightning to make room)
never taken. Laser acquisition is survival-critical, but this is lower priority than the
combat gaps above.

**A — take:** me at origin, weapons `[gun,None]`,
`obs["pickups"]=[{"id":8001,"kind":"laser","pos":[3.0,0.0,0.0]}]`, zone radius 300.
`want_weapon` true, visible, distance ≤4, `abs(dz)≤4`, not charging.
**Expected:** `action["take"] == 8001`, label `"laser hunt"`, move toward the pickup.
**B — swap:** weapons `[gun, {"kind":"lightning",...}]`, same pickup, `slot_empty=false`,
`lightning_slot=1` → `action["take"]=8001`, `action["drop"]=1`. Do not drop a charging
laser (`laser_charging` guard at L835).

---

# Dangerous interactions between subsystems

### I1. `_apply_unstick` rotates an active dodge vector  `[flat]`
Dodge sets `act["move"]=[0,-1]` (gun bullet at 60 m), then `_apply_unstick` (L1620) sees a
static `pos_history` (six entries all at the current position over 0.6 s),
`unstick_until=-inf`, `unstick_started=-inf`, `unstick_sign=1`, `grounded=True`,
energy ≥60. It rotates by +90° to `[1,0]`, sets `jump`/`boost` true. **Observed:** the
dodge vector is abandoned and the bot jets sideways for 1.2 s, potentially along the
bullet path. **Safe:** skip unstick while a dodge/sidestep vector is active, or validate the
rotated vector against the projectile.

### I2. `_laser_guard` after `healing` releases a charged laser without aiming  `[flat]`
State `healing=False` at entry; hp 500/1400, in_zone, no mechs within 45 m; laser slot has
`charge=0.6`; `act["fire"]` starts `[False,False]`. `_heal` sets `healing=True` and
returns early; `_act` leaves `fire[1]=False`; `_laser_guard` L1367 sees `self.healing` and
returns before aiming, so the server sees trigger-release and fires the 60% beam along
`me.aim`. **Observed:** `bot.healing=True`, `fire[1]=False`, no aim correction.
**Safe:** while healing with a charged laser, either keep the trigger held (preserve charge)
or aim at the last beam/hit bearing before releasing; never dump the beam into a wall.

### I3. Zone-run overrides the anti-sandwich escape  `[flat]`
Me at `[45,0,0]`, target id1 at `[15,0]` (30 m, hp 1000), flankers id2/id3 at 80 m,
bearings `π±1.4` → `_anti_sandwich_move` returns an outward wedge vector (covered span
160°). Zone: `next_center=[100,0]`, `next_radius=60`, `shrink_end=t+0.7`,
`me.in_zone=True` → `d_next=55`, `excess=5`, `5/11.7=0.43 > 0.6*0.7=0.42`, so L1596
fires. **Observed:** L1591 overwrites the wedge move with a straight run to the next
center, `boost=True`; label contains both `wedge` and `zone-run`. **Safe:** emergency
disengage/dodge should outrank zone-run, or zone-run should preserve the escape bearing.

### I4. Roof tp-cover overridden by zone-run → walks off the roof  `[map]`
Me on `R` at center+6, target 30 m on the roof, third-party hit from id2; `_movement`
returns `"zone"` (next center far, target close), tp-cover sets move toward roof center at
L1518. Zone `next_center=[300,0]`, `next_radius=100`, `shrink_end=t+2`, me at `[0,0,R[6]]`
→ zone-run L1591 overwrites with `[1,0]`, `boost=True`. **Observed:** label contains both
`tp-cover` and `zone-run`; final move points off the roof toward the next circle.
**Safe:** while on a roof, zone-run should route to the roof edge/climb point or be
suppressed until the bot is off the roof.

### I5. Zone-edge validation turns a dodge into a move toward the blast  `[flat]`
Me `[9.5,0,0]`, zone `next_center=[0,0]`, `next_radius=10`; mortar impact `[10.5,0]`
(outside). `_validate_dodge_vec` rejects `[+1,0]` (5 m ahead outside the circle) and
accepts `[-1,0]` (toward the impact). **Observed:** `action.move=[-1,0]`, straight into
splash. **Safe:** when the away vector is outside the zone, choose a tangential boundary
vector (both perpendicular candidates are also outside at the exact boundary, so the code
must not simply reverse); at minimum never reverse into the impact.

### I6. Finals detection suppressed by any recent damage dealt  `[flat]`
`alive 8→6` at t=60, `prev_alive=8`, `non_our_deaths=1`, `recent_dealt={2:59.0}`.
`recently_hit_any` is true, so L1425 is skipped, `prev_alive` becomes 6, and the two deaths
are never counted; `is_finals` stays False. **Observed:** no FFA switch for the rest of the
match unless two more unexplained deaths occur. **Safe:** subtract `new_kills` (already
done) and require the damage to be on a mech that actually died; a hit on a third party
must not mask unrelated deaths. This is the damage-bookkeeping ↔ Finals-mode interaction.

---

## Suggested priority

1. §3 mortar dodge (biggest damage source never dodged), §6 blocked laser, §7 lightning.
2. §1/§2 Finals detection and silent walk (mode changes the whole endgame), §15 roof plan.
3. §5 NPC ignore, §14 attacking drone, §13 beam return fire.
4. §8/§9/§10 laser sidestep and roof cover/reload, §11 heal geometry, §12 target selection.
5. §16 pickup (acquisition, not immediate survival).
