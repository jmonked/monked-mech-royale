# Tactical branch coverage - c8e98e1

Scenarios: 3472 corpus
Tactical branch arcs taken: 316/490 (64.5%)

| Function | Branch arcs taken | % |
|---|---|---|
| _shoot_beam_origin (L1128-1153) | 1/10 | 10.0 |
| _shoot_crate (L1193-1225) | 2/10 | 20.0 |
| _projectile_dodge (L388-473) | 11/44 | 25.0 |
| _shoot_drone (L1162-1191) | 4/14 | 28.6 |
| _laser_guard (L1361-1384) | 5/10 | 50.0 |
| _movement (L786-951) | 40/74 | 54.1 |
| _fight (L1058-1126) | 14/24 | 58.3 |
| _on_body (L997-1018) | 5/8 | 62.5 |
| _should_push (L1227-1256) | 11/16 | 68.8 |
| _act (L1402-1627) | 80/114 | 70.2 |
| _heal (L539-597) | 18/24 | 75.0 |
| _face_bearing (L1348-1359) | 6/8 | 75.0 |
| _laser_sidestep (L475-518) | 20/24 | 83.3 |
| _choose_target (L648-703) | 20/24 | 83.3 |
| _rotate_move_safe (L1287-1298) | 5/6 | 83.3 |
| _laser_ready (L1020-1032) | 5/6 | 83.3 |
| _drop_goal (L705-746) | 19/22 | 86.4 |
| _find_cover (L520-537) | 7/8 | 87.5 |
| _cube_goal (L748-784) | 13/14 | 92.9 |
| _anti_sandwich_move (L1258-1285) | 16/16 | 100.0 |
| _apply_unstick (L1300-1331) | 14/14 | 100.0 |

## Branches never taken (first 8 per function)

### _act
- L1517 -> [1518, 1530]: `if d > 2.0:`
- L1424 -> [1425, 1429]: `if not recently_hit_any:`
- L1549 -> [1550]: `if 2.0 < d <= 40.0:`
- L1426 -> [1427, 1429]: `if self.non_our_deaths >= 2:`
- L1583 -> [1584, 1590]: `if walk > self.step_speed:`
- L1541 -> [1542, 1590]: `if d > 2.0:`
- L1537 -> [1539]: `if on_roof is not None:`
- L1514 -> [1515]: `if on_roof is not None:`
- ... 19 more

### _fight
- L1119 -> [1080, 1120]: `elif kind == "lightning":`
- L1095 -> [1119]: `elif kind == "laser":`
- L1102 -> [1103]: `if blocked and cur_charge > 0 and mechs:`
- L1104 -> [1105, 1107]: `if alt is not None:`
- L1113 -> [1114]: `if blocked and self.laser_full_since is not None and self._now - self.laser_full_since >= 1.6:`
- L1093 -> [1094]: `if blocked and (weapon.get("reload") or 0) <= 0 and (weapon.get("ammo") is not None) and 0 < weapon["ammo"] <=`
- L1121 -> [1080, 1122]: `if not blocked and distance <= 0.9 * reach and me["energy"] >= 10:`

### _projectile_dodge
- L471 -> [472, 473]: `if valid is None:`
- L412 -> [413]: `if kind == "mortar":`
- L440 -> [441]: `if rv2 <= 1.0:`
- L456 -> [404, 457]: `if vh > 1e-4:`
- L449 -> [450, 451]: `if abs(dz) > 0.5 * my_h + 1.0:`
- L408 -> [409]: `if not pos or not vel:`
- L436 -> [437]: `if kind == "npc" and ignore_npc:`
- L444 -> [446]: `if not (0.20 <= t_hit <= 0.65):`
- ... 12 more

### _laser_sidestep
- L506 -> [507, 512]: `if math.dist((mx + 4 * cand_b[0], my + 4 * cand_b[1]), rc) < math.dist((mx + 4 * cand_a[0], my + 4 * cand_a[1]`
- L504 -> [505]: `if on_roof is not None:`
- L489 -> [490]: `if not aim or aim[0] is None:`

### _find_cover
- L529 -> [530]: `if length == 0:`

### _heal
- L587 -> [595]: `if distance > 3:`
- L590 -> [595]: `elif threat is not None:`
- L576 -> [577]: `if threat is None:`
- L563 -> [567]: `elif self.last_mech_bearing is not None and now - self.last_mech_bearing[0] <= 10:`
- L593 -> [594]: `if math.dist(ahead, zone["next_center"]) <= zone["next_radius"]:`
- L567 -> [568]: `if on_roof is not None:`

### _should_push
- L1238 -> [1239, 1240]: `if hp is None or max_hp is None or hp > 0.5 * max_hp:`
- L1236 -> [1237]: `if self.is_finals:`
- L1232 -> [1233]: `if "laser" in (target.get("weapons") or []) and not my_laser:`
- L1247 -> [1248]: `if USE_NO_LASER_CAUTION and not has_laser and "laser" in t_weapons and (hp is None or hp > 0.5 * me["hp"]):`

### _choose_target
- L690 -> [691]: `if eff_hp is None:`
- L700 -> [702]: `if cur_eff is None or best_eff is None or best_eff >= 0.6 * cur_eff:`
- L685 -> [686]: `if now >= LATE_T and not recent and distance > self.near_range:`
- L683 -> [684]: `if under_fire and not recent and distance > self.near_range and not (hp is not None and hp <= laser_damage):`

### _face_bearing
- L1351 -> [1352]: `if self.last_beam_threat is not None and now - self.last_beam_threat[0] <= 3.0:`
- L1357 -> [1358]: `if self.last_sound is not None and now - self.last_sound[0] <= 2:`

### _movement
- L937 -> [938, 945]: `elif d_climb <= 6.0:`
- L834 -> [836]: `if (pickup_id in visible and distance <= self.reach and abs(dz) <= 4.0`
- L867 -> [868]: `if holding_drop:`
- L927 -> [928, 929]: `if self.roof_goal is None:`
- L901 -> [902, 912]: `if on_roof is not None and math.dist(on_roof[1], zone["next_center"]) <= zone["next_radius"] - 4.0:`
- L899 -> [900]: `elif (now >= LATE_T or self.is_finals) and has_laser and not outside and self.roofs:`
- L837 -> [838, 840]: `if not slot_empty and lightning_slot is not None and kind == "laser":`
- L939 -> [940, 941]: `if climb_started is None:`
- ... 12 more

### _laser_guard
- L1367 -> [1369]: `if fire[i] or self.laser_released or self.healing or not me.get("in_zone", True):`
- L1380 -> [1381, 1382]: `if actual[0] is not None and abs(math.remainder(aim[0] - actual[0], math.tau)) > math.radians(30):`
- L1376 -> [1377, 1378]: `if pick is None:`

### _shoot_drone
- L1170 -> [1172]: `if m.get("kind") != "npc" or not m.get("pos"):`
- L1185 -> [1169, 1186]: `if best is None or rank < best[1]:`
- L1178 -> [1179, 1180]: `if not (attacking_us or farm_ok):`
- L1180 -> [1181, 1182]: `if abs(dz) > 4.0 or math.dist(m["pos"][:2], zone["next_center"]) > zone["next_radius"]:`
- L1182 -> [1183, 1184]: `if self._target_blocked(me, m):`
- L1187 -> [1189]: `if best is None:`

### _shoot_crate
- L1223 -> [1224, 1225]: `if gun_slot is not None:`
- L1201 -> [1198, 1203]: `if (distance <= CRATE_RANGE and abs(cz - z) <= 3 and (best is None or distance < best[1])`
- L1216 -> [1217, 1222]: `if laser_slot is not None:`
- L1204 -> [1206]: `if best is None:`
- L1198 -> [1199]: `for crate in obs.get("crates") or []:`

### _shoot_beam_origin
- L1129 -> [1131]: `if self.last_beam_threat is None:`
- L1138 -> [1139, 1140]: `if dist > self.gun_range or dist < 5.0 or self._building_blocked(muzzle_pos, aim_pt):`
- L1149 -> [1150, 1153]: `for i, w in enumerate(weapons[:2]):`
- L1150 -> [1149, 1151]: `if w and w["kind"] == "gun" and (w.get("reload") or 0) <= 0 and (w.get("ammo") is None or w["ammo"] > 0):`
- L1132 -> [1133, 1134]: `if obs["t"] - fired_at > 0.8 or len(origin) < 3:`

### _drop_goal
- L726 -> [727]: `if now - first_c >= DROP_CONTEST_ABORT_S:`
- L728 -> [730]: `elif active:`
- L719 -> [720]: `if active and in_ring:`

### _cube_goal
- L779 -> [780]: `elif now - since >= 4:`

### _rotate_move_safe
- L1289 -> [1290]: `if math.hypot(mx, my) <= 1e-6:`

### _on_body
- L998 -> [999]: `if not actual or None in actual or distance <= 1e-6:`
- L1000 -> [1001]: `if target.get("kind") == "npc":`
- L1014 -> [1015]: `if self.laser_full_since is not None and self._now - self.laser_full_since >= 0.8:`

### _laser_ready
- L1029 -> [1030]: `if self._target_blocked(me, target):`

