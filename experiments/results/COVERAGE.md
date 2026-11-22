# Tactical branch coverage - c8e98e1

Scenarios: 3512 corpus + 800 Hypothesis states
Tactical branch arcs taken: 413/490 (84.3%)

| Function | Branch arcs taken | % |
|---|---|---|
| _shoot_crate (L1193-1225) | 2/10 | 20.0 |
| _movement (L786-951) | 49/74 | 66.2 |
| _laser_guard (L1361-1384) | 7/10 | 70.0 |
| _on_body (L997-1018) | 6/8 | 75.0 |
| _projectile_dodge (L388-473) | 35/44 | 79.5 |
| _shoot_beam_origin (L1128-1153) | 8/10 | 80.0 |
| _rotate_move_safe (L1287-1298) | 5/6 | 83.3 |
| _laser_ready (L1020-1032) | 5/6 | 83.3 |
| _shoot_drone (L1162-1191) | 12/14 | 85.7 |
| _laser_sidestep (L475-518) | 21/24 | 87.5 |
| _find_cover (L520-537) | 7/8 | 87.5 |
| _act (L1402-1627) | 100/114 | 87.7 |
| _drop_goal (L705-746) | 20/22 | 90.9 |
| _fight (L1058-1126) | 22/24 | 91.7 |
| _cube_goal (L748-784) | 13/14 | 92.9 |
| _heal (L539-597) | 23/24 | 95.8 |
| _anti_sandwich_move (L1258-1285) | 16/16 | 100.0 |
| _should_push (L1227-1256) | 16/16 | 100.0 |
| _choose_target (L648-703) | 24/24 | 100.0 |
| _apply_unstick (L1300-1331) | 14/14 | 100.0 |
| _face_bearing (L1348-1359) | 8/8 | 100.0 |

## Branches never taken (first 8 per function)

### _act
- L1517 -> [1530]: `if d > 2.0:`
- L1549 -> [1550]: `if 2.0 < d <= 40.0:`
- L1583 -> [1590]: `if walk > self.step_speed:`
- L1541 -> [1542, 1590]: `if d > 2.0:`
- L1537 -> [1539]: `if on_roof is not None:`
- L1465 -> [1466]: `if dodge_boost:`
- L1564 -> [1565]: `if USE_MORE_CUBES and not near_threat and self._shoot_crate(obs, weapons, act):`
- L1604 -> [1620]: `if not protect_drop:`
- ... 5 more

### _fight
- L1119 -> [1080]: `elif kind == "lightning":`
- L1104 -> [1105]: `if alt is not None:`

### _projectile_dodge
- L456 -> [404]: `if vh > 1e-4:`
- L436 -> [437]: `if kind == "npc" and ignore_npc:`
- L417 -> [418]: `if disc < 0.0:`
- L428 -> [404]: `if urgency > best_urgency:`
- L413 -> [414]: `if ignore_mortar:`
- L426 -> [404]: `if d < self.mortar_splash:`
- L454 -> [404]: `if urgency > best_urgency:`
- L420 -> [421]: `if not (0.05 <= t_land <= 2.4):`
- ... 1 more

### _laser_sidestep
- L506 -> [507, 512]: `if math.dist((mx + 4 * cand_b[0], my + 4 * cand_b[1]), rc) < math.dist((mx + 4 * cand_a[0], my + 4 * cand_a[1]`
- L504 -> [505]: `if on_roof is not None:`

### _find_cover
- L529 -> [530]: `if length == 0:`

### _heal
- L587 -> [595]: `if distance > 3:`

### _movement
- L937 -> [945]: `elif d_climb <= 6.0:`
- L834 -> [836]: `if (pickup_id in visible and distance <= self.reach and abs(dz) <= 4.0`
- L867 -> [868]: `if holding_drop:`
- L927 -> [929]: `if self.roof_goal is None:`
- L901 -> [902]: `if on_roof is not None and math.dist(on_roof[1], zone["next_center"]) <= zone["next_radius"] - 4.0:`
- L837 -> [838, 840]: `if not slot_empty and lightning_slot is not None and kind == "laser":`
- L939 -> [941]: `if climb_started is None:`
- L912 -> [949]: `elif not enemy_close:`
- ... 11 more

### _laser_guard
- L1380 -> [1381, 1382]: `if actual[0] is not None and abs(math.remainder(aim[0] - actual[0], math.tau)) > math.radians(30):`
- L1376 -> [1378]: `if pick is None:`

### _shoot_drone
- L1178 -> [1179]: `if not (attacking_us or farm_ok):`
- L1182 -> [1183]: `if self._target_blocked(me, m):`

### _shoot_crate
- L1223 -> [1224, 1225]: `if gun_slot is not None:`
- L1201 -> [1198, 1203]: `if (distance <= CRATE_RANGE and abs(cz - z) <= 3 and (best is None or distance < best[1])`
- L1216 -> [1217, 1222]: `if laser_slot is not None:`
- L1204 -> [1206]: `if best is None:`
- L1198 -> [1199]: `for crate in obs.get("crates") or []:`

### _shoot_beam_origin
- L1149 -> [1153]: `for i, w in enumerate(weapons[:2]):`
- L1150 -> [1149]: `if w and w["kind"] == "gun" and (w.get("reload") or 0) <= 0 and (w.get("ammo") is None or w["ammo"] > 0):`

### _drop_goal
- L726 -> [727]: `if now - first_c >= DROP_CONTEST_ABORT_S:`
- L728 -> [730]: `elif active:`

### _cube_goal
- L779 -> [780]: `elif now - since >= 4:`

### _rotate_move_safe
- L1289 -> [1290]: `if math.hypot(mx, my) <= 1e-6:`

### _on_body
- L998 -> [999]: `if not actual or None in actual or distance <= 1e-6:`
- L1014 -> [1015]: `if self.laser_full_since is not None and self._now - self.laser_full_since >= 0.8:`

### _laser_ready
- L1029 -> [1030]: `if self._target_blocked(me, target):`

