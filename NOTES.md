# NOTES: mechfight/1 key rules (Team Monked)

Source: `buildathon/kit/mechfight-kit/protocol.md` (the same file as `kit/mech-protocol.md`) and the live `hello.config` from `check/stream.jsonl.gz`. **If this file and protocol.md disagree, protocol.md wins.** Read numbers from `hello["config"]` at runtime. They can change between matches.

## Loop and limits
- `hello` → reply `{"type":"ready","name":...}` within 20 s. Precompute map data here (world.json is 300 KB, terrain is 1070×724 int16).
- Then 10 `obs` per second (every 2 sim ticks at 20 Hz). Reply `{"tick": <echo>, ...}` within **50 ms** of wall time. Aim for p99 under 15 ms locally, because the scorer runs on 1 CPU.
- A missed reply keeps move/boost/aim but drops fire/jump/reload/pick/take/drop. After 1 s of missed replies the mech idles. If the process crashes, the mech idles for the rest of the match. The wrapper (`mechfight.py`) skips to the newest observation when several queue up.
- stdout carries protocol messages only. Logs go to stderr, and nobody sees them during matches. Write files only to /tmp. No network.
- Sandbox: 1 CPU, 512 MB, uid 65534, read-only disk, map at `/arena` (`hello.map.dir`).
- Local test: from the kit folder, run `python check/check.py -- python -u <bot>`. This checks the protocol only. It is **not a simulation**, so the only real score signal is a submission (48 matches, 4 submissions per hour per team).

## Scoring
- Score per match = `16 - place`. Place = the order of death (last alive = 1st). Mechs that die on the same tick share a place. `obs.alive` is the place you would get if you died now.
- If the clock runs out at 8:00, survivors are ranked by HP. In practice the zone reaches radius 0 at about 6:55 and deals 260 dps, so the **last mech alive is the one with the most HP at the final collapse** (no regen outside the zone).
- **Practice:** 15 house bots (4 easy, 4 medium, 4 hard, 3 expert) play as one squad. They share vision, never fight each other, and hunt us weakest first: 1 hunter at the start, more as they get thinned out, all of them late. So our points ≈ the number of house bots that die before we do, from our kills, the zone, or NPC drones. Hiding alone does not score points. Surviving while killing hunters one at a time does.
- **Final:** a real free-for-all between team bots. There, survival and placement matter most.
- Baseline (example bot) = 1.15. The recorded check stream shows a mech dying at t = 36.8 s in 13th place, so fights are short and lethal.

## Coordinates
- Meters, seconds, radians. x = east, y = north, z = up. Yaw is measured from +x counter-clockwise (0 = E, π/2 = N). Pitch is positive upward.
- Mech: `pos` = feet. It is a cylinder with r 2.5 and h 9. Center at z+4.5, eyes at z+8, gun muzzle at z+7, mortar tube at z+9.5. Shots leave 3 m out along the aim. Size scales by +5% per cube, with no cap.
- NPC drone: r 1.8, h 3.5.

## Observation (`obs`)
- `tick`, `t` (seconds), `alive` (mechs alive, NPCs not counted).
- `self`: `pos`, `vel`, `aim` [yaw, pitch] (**actual** torso aim, which turns at 4 rad/s yaw and 3 rad/s pitch), `hp`/`max_hp`, `energy`/`max_energy`, `grounded`, `cubes`, `upgrades`, `in_zone`, `weapons[2]`, `stats`.
  - `weapons[i]`: null or `{kind, cooldown, stats}`. The gun also has `ammo` and `reload`. The laser also has `charge`. Slot 1 is empty at spawn.
- `mechs`: visible mechs (`kind:"mech"`: hp, cubes, weapons list, `charging`) and NPCs (`kind:"npc"`). Includes 5 s of memory with the **real** position after a target leaves view.
- `projectiles`: visible enemy bullets and shells (pos, vel). Our own are omitted.
- `crates`, `cubes`, `pickups` (weapons on the ground, ids 8000+): listed only while visible.
- `sounds`: `{kind, bearing (world yaw, σ 7°), dist near<60/mid<160/far, age}`. They do not say who made them. The kind reveals the weapon.
- `beams`: laser and lightning shots seen since the last obs (`by`, `path`).
- `events`: `damaged{amount, weapon, bearing, by, rear}` (bearing and by are null for the zone), `hit`, `effect`, `kill`, `pickup`, `drop`, `upgrade`, `took`, `dropped`, `take_failed{reason}`.
- `drops`: supply drops (always known). `zone`: always known. `offer`: an upgrade choice or null.
- Id ranges: mechs 0–15, NPCs 100+, crates 1000+, cubes 5000+, pickups 8000+, drops 20000+.

## Action
`{"tick", "move":[x,y] (world frame, length ≤ 1), "boost", "jump", "aim":[yaw,pitch], "fire":[s0,s1], "reload", "pick":0-2, "take":id, "drop":0|1, "debug"}`
- Legs and torso are independent: you can move one way and aim another. Aim is clamped to pitch [-0.7, 1.3].
- `fire` holds the trigger for the 2 ticks until the next decision. `take` needs a horizontal distance ≤ 4 m and a vertical distance ≤ 4 m.
- Missing fields fall back to defaults (aim = the last commanded aim, everything else off).

## Movement
- Walk at 11.7 m/s. Boost at 19.5 m/s (drains 17 energy/s). Ground accel 58.5, air accel 12, gravity 22.
- Jump at 11 m/s. Boosting in the air jets up (accel 34, max rise 10 m/s, drains 15 energy/s). 100 energy climbs about 60 m (most roofs).
- Energy: 100 max. It regens 18/s after 0.6 s without spending.
- Step-up 1.2 m. Max slope 50°. Walls slide you along them. The map edge is a wall.

## Health and damage
- 1400 HP. After 5 s without dealing or taking damage, regen 45 HP/s (a full heal takes about 31 s). There is no regen outside the zone, and zone damage resets the 5 s timer.
- **Rear armor:** hits from outside the 180° front arc (centered on the torso yaw) deal **×1.5**. Face your attacker. `damaged.rear` tells you a hit came from behind.
- Cube scaling: damage × (1 + 0.04 × min(cubes, 10)). Max HP gets +4% per cube (cap 10).

## Weapons (slot 0 = gun at spawn, slot 1 = loot)
| Weapon | Key numbers | Notes |
|---|---|---|
| gun | 45 dmg, 0.24 s cooldown (≈187 DPS), 252 m/s, range 230, spread 0.6°, mag 12, reload 2.4 s | Straight line with no drop. **Lead moving targets.** |
| mortar | 200 direct hit + 160 splash (falls to 30% at 7 m), 72 m/s, gravity 22, cooldown 2.6 s, max range about 235 m at 45° | Lobs over buildings. Concussion: knockback 16 m/s up 9 and drains 45 energy. Our own splash hits us at 50%. |
| laser | up to 315 dmg (35% at no charge), full charge 0.75 s, range 280, hitscan, cooldown 1.65 s | Hold to charge, release to fire. Moves at half speed while charging. Visible (`charging`) and audible. Auto-fires after 2 s at full charge. +60% against a mech holding a mortar. |
| lightning | 60 dmg, range 45, cone 30°, needs LOS, chains 2× within 14 m (×0.7), 3 energy, 0.25 s cooldown | Hits the nearest target in the cone (mech/NPC/crate). Short: shuts down the target's laser for 2 s. |
- Triangle: laser > mortar, mortar > lightning, lightning > laser. The gun is neutral.
- Buildings, bridges and terrain block shots and sight. **Trees block sight (crowns partly, trunks fully) but not shots.**
- Loot: 40 floor weapons (1:1:1 mortar/laser/lightning). Crates (36, 300 HP) drop 1 cube and a weapon 50% of the time. Dead mechs drop their non-gun weapons and cubes+2. You cannot hold two of the same kind. A newly taken weapon cannot fire for max(1 s, its cooldown). Swap with `take` + `drop`.

## Vision and sound
- You see an object if your eye has LOS to its center or top, and either it is within **45 m** in any direction, or it is within **200 m** inside a **120° yaw wedge** around the torso aim. **Where you aim is where you look.** You are blind behind you beyond 45 m.
- Sound ranges (m): gun 320, mortar 420, explosion 420, laser 380, laser_charge 140, lightning 160, jet 90, boost 90, step 40, reload 60, death 600, crate 220, npc_gun 200, drop 600.
- Walking at ≤ 5 m/s (or standing still) on the ground is silent. Faster walking makes a step sound every 0.6 s. Boosting makes boost sounds.

## Zone (defaults, from `config.zone`)
- Starts at r 560 around (41.3, −72.8). `obs.zone` gives the `center`/`radius` now, `next_center`/`next_radius`, `shrink_start`/`shrink_end`, and `dps`. Shrink is linear. The next circle lies entirely inside the current one.
- Timeline:

| Phase | Hold (s) | Shrink (s) | → Radius (m) | dps |
|---|---|---|---|---|
| 1 | 0–60 | 60–110 | 380 | 20 |
| 2 | 110–155 | 155–195 | 240 | 35 |
| 3 | 195–230 | 230–265 | 140 | 60 |
| 4 | 265–295 | 295–325 | 70 | 100 |
| 5 | 325–350 | 350–375 | 25 | 160 |
| 6 | 375–390 | 390–415 | 0 | 260 |

- Outside the zone you lose `dps` HP/s (armor does not reduce it, and regen stops). The match ends when 1 mech is left or at 480 s.

## NPC drones, cubes, drops, upgrades
- 12 drones with 350 HP stay within 30 m of home. They shoot (25 dmg, 1 s cooldown) at attackers or at mechs within 45 m that they have LOS to. They chase up to 60 m from home or 90 m from the target. Each drops 2 cubes.
- Cubes: pick up within 3.5 m. Each gives +4% max HP and +4% damage (cap 10) and +5% size (no cap). Upgrade offers come at cube counts 1, 3, 6, 10, 15, 21, … Answer with `pick` within 5 s, or choice 0 is applied.
- Upgrade ids: plating (+15% HP), armor (−8% dmg), servos, capacitor, reactor, jets, nanites (+60% regen, starts 1.5 s sooner), gyros (+30% turn), sensors, gun_damage, gun_rate, gun_velocity, gun_mag, mortar_*, laser_*, lightning_*.
- Supply drops are called at 70, 140 and 210 s and land 25 s later inside the next circle. Stand **alone** in the 8 m ring for 4 s to get +3 cubes, full HP and full energy.

## Map (`/arena/v2`)
- `world.json`: `prisms[]` (kinds building/stadium/bridge; `base`, `top`, `ring` = flat [x0,y0,...], `holes`) are the solids. A bridge has a raised base, so you can walk and shoot under it. `trees` (flat `data` with `fields`) block sight only. Everything else in the file (blocks, cars, water, barriers) is scenery that the server ignores.
- `terrain.i16`: little-endian int16 centimeters, nx 1070 × ny 724, 1 m step from (`minX`, `minY`). The value at `x = minX + i, y = minY + j` is stored at index `j*nx + i`. Sample bilinearly.
