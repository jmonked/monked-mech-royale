"""Hunt for a laser, finish weakened mechs and collect nearby power cubes."""
import json
import math
import traceback
from pathlib import Path

import mechfight as mf


THREAT_RECENT_S = 3.0  # an attacker counts as "shooting us now" for this long after a hit
THREAT_RANGE = 60.0    # ...and only while it is this close
LATE_HUNT_RANGE = 80.0  # after the opening, still fetch a laser/lightning this close when not fighting
LATE_T = 230.0         # from the 3rd zone shrink on: no more chasing, let the zone and the squad thin out
LASER_LEAD_S = 0.1     # the beam goes out about one decision after we command the aim
HEAL_FIGHTBACK_S = 2.0  # while healing, keep shooting an attacker that hit us this recently

UPGRADE_RANK = {name: rank for rank, name in enumerate((
    "armor", "plating", "nanites", "laser_damage", "laser_charge", "gun_damage",
    "gun_rate", "gun_mag", "lightning_efficiency", "lightning_range", "lightning_chain",
    "gyros", "servos", "capacitor", "reactor", "jets", "gun_velocity", "sensors",
    "laser_pierce", "mortar_reload", "mortar_splash", "mortar_velocity",
))}


def _stat(stats, key, default):
    value = stats.get(key)
    return default if value is None else value


def _lead_aim(muzzle, target, speed):
    tx, ty, tz = target["pos"]
    dx, dy, dz = tx - muzzle[0], ty - muzzle[1], tz + 4.5 - muzzle[2]
    vx, vy, vz = target.get("vel") or (0.0, 0.0, 0.0)
    lx, ly, lz = dx, dy, dz
    for _ in range(3):
        flight_time = math.hypot(lx, ly, lz) / speed
        lx, ly, lz = dx + vx * flight_time, dy + vy * flight_time, dz + vz * flight_time
    return [math.atan2(ly, lx), math.atan2(lz, math.hypot(lx, ly))]


def _load_cover(hello):
    with (Path(hello["map"]["dir"]) / "v2" / "world.json").open(encoding="utf-8") as source:
        prisms = json.load(source)["prisms"]
    buildings = []
    for prism in prisms:
        if prism["kind"] not in ("building", "stadium") or prism["top"] - prism["base"] < 9:
            continue
        flat = prism["ring"]
        ring = list(zip(flat[::2], flat[1::2]))
        # Area-weighted centroid, independent of how densely each wall is sampled.
        area2 = cx = cy = 0.0
        for (ax, ay), (bx, by) in zip(ring[-1:] + ring[:-1], ring):
            cross = ax * by - bx * ay
            area2 += cross
            cx += (ax + bx) * cross
            cy += (ay + by) * cross
        if abs(area2) > 1e-8:
            center = (cx / (3 * area2), cy / (3 * area2))
            buildings.append((center, max(math.dist(p, center) for p in ring), ring))
    return buildings


def _crosses_ring(start, end, ring):
    # Intersections along the infinite sight line come in entry/exit pairs.
    # Only count a pair if some length of the actual segment lies inside it.
    x, y = start
    dx, dy = end[0] - x, end[1] - y
    crossings = []
    ax, ay = ring[-1]
    side_a = dx * (ay - y) - dy * (ax - x)
    for bx, by in ring:
        side_b = dx * (by - y) - dy * (bx - x)
        if (side_a > 0) != (side_b > 0):
            t = ((ax - x) * (by - ay) - (ay - y) * (bx - ax)) / (side_b - side_a)
            crossings.append(t)
        ax, ay, side_a = bx, by, side_b
    crossings.sort()
    return any(min(leave, 1.0) - max(enter, 0.0) > 1e-9
               for enter, leave in zip(crossings[::2], crossings[1::2]))


class Bot:
    name = "monked"

    def __init__(self, hello: mf.Hello):
        config = hello.get("config") or {}
        self.reach = _stat(config.get("loot") or {}, "pickup_radius", 4)
        self.near_range = _stat(config.get("vision") or {}, "near_range", 45)
        cubes = config.get("cubes") or {}
        self.cube_radius = _stat(cubes, "pickup_radius", 3.5)
        self.cube_cap = _stat(cubes, "stat_cap", 10)
        self.damage_per_cube = _stat(cubes, "damage_per_cube", 0.04)
        gun = (config.get("weapons") or {}).get("gun") or {}
        self.gun_speed = _stat(gun, "speed", 252)
        self.gun_range = _stat(gun, "range", 230)
        self.laser = (config.get("weapons") or {}).get("laser") or {}
        self.lightning = (config.get("weapons") or {}).get("lightning") or {}
        self.muzzle_height = _stat(config.get("mech") or {}, "muzzle_height", 7)
        self.mech_radius = _stat(config.get("mech") or {}, "radius", 2.5)
        self.size_per_cube = _stat(cubes, "size_per_cube", 0.05)
        self.laser_released = False
        self.laser_target = None      # id of the mech the laser was last charged at
        self.laser_full_since = None  # when the current charge became full
        self.walk_speed = _stat(config.get("mech") or {}, "walk_speed", 11.7)
        self.drop_id = None
        self.drop_retry_at = {}
        self.last_hits = {}
        self.target_id = None
        self.killed = set()
        self.last_damage_bearing = None
        self.last_mech_bearing = None
        self.last_sound = None
        self.pickups = {}
        self.cubes = {}
        self.cube_progress = (None, math.inf, 0.0)
        self.unreachable = set()
        self.hunt_progress = {}
        self.previous_move = [0.0, 0.0]
        self.healing = False
        self.cover_spot = None
        self.cover_threat = None
        self.cover_time = -math.inf
        try:
            self.buildings = _load_cover(hello)
        except Exception:
            self.buildings = []

    def _find_cover(self, xy, threat, zone):
        closest = None
        best_distance = math.inf
        for center, radius, ring in self.buildings:
            distance = math.dist(xy, center)
            if distance > 120 or distance - radius - 4 >= best_distance:
                continue
            dx, dy = center[0] - threat[0], center[1] - threat[1]
            length = math.hypot(dx, dy)
            if length == 0:
                continue
            vx, vy = max(ring, key=lambda p: p[0] * dx + p[1] * dy)
            spot = (vx + 4 * dx / length, vy + 4 * dy / length)
            distance = math.dist(xy, spot)
            if (distance < best_distance and math.dist(spot, zone["next_center"]) <= zone["next_radius"] - 5
                    and _crosses_ring(threat, spot, ring)):
                closest, best_distance = spot, distance
        return closest

    def _heal(self, obs, act):
        me = obs["self"]
        pos = me["pos"]
        threshold = 0.85 if self.healing else 0.5
        if not me["in_zone"] or me["hp"] >= threshold * me["max_hp"]:
            self.healing = False
            return False

        nearest = min((m["pos"] for m in obs.get("mechs") or [] if m.get("kind") == "mech" and m.get("pos")),
                      key=lambda p: math.dist(pos, p), default=None)
        if nearest is not None and math.dist(pos, nearest) <= self.near_range:
            self.healing = False
            return False

        now, zone, xy = obs["t"], obs["zone"], pos[:2]
        threat = None
        yaw = me["aim"][0]
        if nearest is not None:
            threat = nearest[:2]
            yaw = math.atan2(threat[1] - xy[1], threat[0] - xy[0])
        elif self.last_mech_bearing is not None and now - self.last_mech_bearing[0] <= 10:
            yaw = self.last_mech_bearing[1]
            threat = (xy[0] + 100 * math.cos(yaw), xy[1] + 100 * math.sin(yaw))

        if threat is None:
            self.cover_spot = self.cover_threat = None
        elif (not self.healing or self.cover_threat is None or now - self.cover_time >= 1
              or math.dist(threat, self.cover_threat) > 15):
            self.cover_spot = self._find_cover(xy, threat, zone)
            self.cover_time, self.cover_threat = now, threat
        self.healing = True
        move, boost = [0.0, 0.0], False
        spot = self.cover_spot
        if spot is not None and math.dist(spot, zone["next_center"]) <= zone["next_radius"] - 5:
            distance = math.dist(xy, spot)
            if distance > 3:
                move = [(spot[0] - xy[0]) / distance, (spot[1] - xy[1]) / distance]
                boost = me["energy"] >= 30 and distance > 20
        elif threat is not None:
            # Allow four metres of walking room before the next circle's edge.
            ux, uy = -math.cos(yaw), -math.sin(yaw)
            ahead = (xy[0] + 4 * ux, xy[1] + 4 * uy)
            if math.dist(ahead, zone["next_center"]) <= zone["next_radius"]:
                move = [ux, uy]
        act.update(move=move, boost=boost, aim=[yaw, 0.0])
        mf.draw.label(f"heal {me['hp'] / me['max_hp']:.0%}")
        return True

    def _remember_damage(self, events, now):
        for event in events:
            attacker = event.get("by")
            if event.get("type") != "damaged" or attacker is None:
                continue
            bearing = event.get("bearing")
            self.last_hits[attacker] = (now, bearing)
            if bearing is not None:
                self.last_damage_bearing = bearing
                if 0 <= attacker < 16:
                    self.last_mech_bearing = (now, bearing)

    def _choose_target(self, mechs, pos, now, weapons, cubes=0):
        laser = next((w for w in weapons if w and w["kind"] == "laser"), None)
        if laser:
            reach = _stat(laser.get("stats") or {}, "range", _stat(self.laser, "range", 280))
        else:
            gun = next((w for w in weapons if w and w["kind"] == "gun"), None) or {}
            reach = _stat(gun.get("stats") or {}, "range", self.gun_range)

        laser_damage = 0.0
        if laser:
            laser_damage = _stat(laser.get("stats") or {}, "damage", _stat(self.laser, "damage", 315))
            # Cubes scale damage; assume the target may have up to 3 armor upgrades (-24%).
            # We release at 93% charge: 35% + 65% * 0.93 = 95.5% of full damage.
            laser_damage *= 0.955 * 0.76 * (1 + self.damage_per_cube * min(cubes or 0, self.cube_cap))
        # Under fire: a mech that hit us in the last 3 s from close range. While one is around,
        # don't turn away to chase a distant wounded mech unless one full laser shot kills it.
        under_fire = any(
            mech.get("kind") == "mech" and mech.get("id") is not None and 0 <= mech["id"] < 16
            and mech["id"] not in self.killed and mech.get("pos")
            and now - self.last_hits.get(mech["id"], (-math.inf,))[0] <= THREAT_RECENT_S
            and math.dist(mech["pos"], pos) <= THREAT_RANGE
            for mech in mechs)

        best = current = None
        best_rank = None
        for mech in mechs:
            mech_id = mech.get("id")
            if mech.get("kind") != "mech" or mech_id is None or mech_id in self.killed or not mech.get("pos"):
                continue
            distance = math.dist(mech["pos"], pos)
            hit = self.last_hits.get(mech_id)
            recent = hit is not None and now - hit[0] <= 8.0
            hp, max_hp = mech.get("hp"), mech.get("max_hp")
            wounded = hp is not None and max_hp is not None and hp <= 0.5 * max_hp
            if not (recent or distance <= self.near_range or (wounded and distance <= reach)):
                continue
            if under_fire and not recent and distance > self.near_range and not hp <= laser_damage:
                continue
            # Late game: only fight what shoots us or comes close; don't walk out after wounded mechs.
            if now >= LATE_T and not recent and distance > self.near_range:
                continue
            if mech_id == self.target_id:
                current = mech
            if hp is None:
                rank = (math.inf, 0, distance - (1.0 if recent else 0.0))
            else:
                rank = (hp, not recent, distance)
            if best_rank is None or rank < best_rank:
                best, best_rank = mech, rank

        if current is not None:
            hp, best_hp = current.get("hp"), best.get("hp")
            if hp is None or best_hp is None or best_hp >= 0.6 * hp:
                best = current
        self.target_id = best["id"] if best is not None else None
        return best

    def _drop_goal(self, obs, healing):
        me, zone, now = obs["self"], obs["zone"], obs["t"]
        best = None
        best_distance = math.inf
        for drop in obs.get("drops") or []:
            drop_id = drop["id"]
            if now < self.drop_retry_at.get(drop_id, -math.inf):
                continue
            xy = drop["pos"][:2]
            distance = math.dist(me["pos"][:2], xy)
            active = drop_id == self.drop_id
            in_ring = distance <= drop["radius"] - 2
            if active and in_ring:
                # Once in place, keep holding even if a rival contests the capture.
                return drop
            contested = any(m.get("kind") == "mech" and m["id"] != me["id"]
                            and math.dist(m["pos"][:2], xy) <= drop["radius"] + 12
                            for m in obs.get("mechs") or [])
            if contested or (not in_ring and me["hp"] < 0.35 * me["max_hp"]):
                if active:
                    self.drop_retry_at[drop_id] = now + 15
                continue
            if ((healing and not active) or not me["in_zone"] or distance > 250
                    or math.dist(xy, zone["next_center"]) > zone["next_radius"] - 4
                    or (not active and me["hp"] >= 0.75 * me["max_hp"])):  # only go when hurt
                continue
            # Time departure once. Boosting toward the drop can put us ahead of schedule.
            speed = _stat(me.get("stats") or {}, "walk_speed", self.walk_speed)
            if not active and drop["lands_in"] > distance / speed + 3:
                continue
            if distance < best_distance:
                best, best_distance = drop, distance
        self.drop_id = best["id"] if best is not None else None
        return best

    def _cube_goal(self, obs, max_distance, *, pursuing_drop=False):
        me = obs["self"]
        pos = me["pos"]
        zone = obs["zone"]
        visible = {c["id"]: c["pos"] for c in obs.get("cubes") or []}
        self.cubes.update(visible)
        picked_up = any(e.get("type") == "pickup" for e in obs.get("events") or [])
        options = []
        for cube_id, location in list(self.cubes.items()):
            distance = math.dist(pos[:2], location[:2])
            height = location[2] - pos[2]
            if abs(height) <= 4 and ((picked_up and distance <= self.cube_radius)
                                     or (cube_id not in visible and distance <= 4)):
                del self.cubes[cube_id]
                continue
            if (not pursuing_drop and me.get("cubes", 0) < self.cube_cap and height <= 3.5
                    and distance <= max_distance and cube_id not in self.unreachable
                    and math.dist(location[:2], zone["next_center"]) <= zone["next_radius"]):
                options.append((distance, cube_id))

        now = obs["t"]
        previous_id, best, since = self.cube_progress
        for distance, cube_id in sorted(options):
            if cube_id != previous_id or distance <= best - 1:
                self.cube_progress = (cube_id, distance, now)
            elif now - since >= 4:
                self.unreachable.add(cube_id)
                continue
            return self.cubes[cube_id], distance
        self.cube_progress = (None, math.inf, now)
        return None

    def _movement(self, obs, slot_empty, act, drop=None):
        me = obs["self"]
        xy = me["pos"][:2]
        zone = obs["zone"]
        goal = zone["next_center"]
        visible = {p["id"]: p for p in obs.get("pickups") or []}
        self.pickups.update(visible)
        for pickup_id, pickup in list(self.pickups.items()):
            if pickup_id not in visible and math.dist(xy, pickup["pos"][:2]) <= 6:
                del self.pickups[pickup_id]
        for event in obs.get("events") or []:
            if event.get("type") in ("took", "take_failed"):
                self.pickups.pop(event.get("id"), None)

        state = "zone"
        outside = not me["in_zone"]
        boost = outside
        hunt_id = None
        weapons = me.get("weapons") or []
        # Holding lightning: a laser is worth swapping in (sim: laser matches ~2.2 vs lightning ~1.5).
        swap_slot = next((i for i, w in enumerate(weapons[:2]) if w and w.get("kind") == "lightning"), None)
        if slot_empty or swap_slot is not None:
            best_take = best_hunt = (2, math.inf)
            for pickup_id, pickup in self.pickups.items():
                kind = pickup["kind"]
                if kind not in ("laser", "lightning") or (not slot_empty and kind != "laser"):
                    continue
                location = pickup["pos"][:2]
                distance = math.dist(xy, location)
                rank = (0 if kind == "laser" else 1, distance)
                # Swapping costs the laser's 1.65 s equip time, so never swap mid-fight.
                if (pickup_id in visible and distance <= self.reach and abs(pickup["pos"][2] - me["pos"][2]) <= 4
                        and rank < best_take and (slot_empty or self.target_id is None)):
                    act["take"] = pickup_id
                    if not slot_empty:
                        act["drop"] = swap_slot
                    best_take = rank
                # Skip rooftop pickups (take needs <= 4 m vertical) and ones we failed to reach.
                if pickup["pos"][2] - me["pos"][2] > 5 or pickup_id in self.unreachable:
                    continue
                # Early: anything within 250 m. Later: within 80 m while not fighting (e.g. a kill's drop).
                if (((obs["t"] < 90 and distance <= 250)
                     or (distance <= LATE_HUNT_RANGE and self.target_id is None
                         and pickup_id in visible and me["in_zone"])) and rank < best_hunt
                        and math.dist(location, zone["next_center"]) <= zone["next_radius"]):
                    best_hunt = rank
                    hunt_id = pickup_id
                    state = "laser hunt"
                    goal = location
                    boost = outside or (me["energy"] >= 30 and distance > 25)
        # Preserve the default facing even when collecting a drop or cube.
        yaw = math.atan2(goal[1] - xy[1], goal[0] - xy[0])
        move_yaw = yaw
        cube = self._cube_goal(obs, 15 if hunt_id is not None and obs["t"] < 90 else 40, pursuing_drop=drop is not None)
        if drop is not None:
            self.hunt_progress.pop(hunt_id, None)
            dx, dy = drop["pos"][0] - xy[0], drop["pos"][1] - xy[1]
            distance = math.hypot(dx, dy)
            holding = distance <= drop["radius"] - 2
            act.update(move=[0.0, 0.0] if holding else [dx / distance, dy / distance],
                       aim=[yaw, 0.0], boost=not holding and me["energy"] >= 30 and distance > 30,
                       jump=not holding and obs["tick"] % 40 == 0)
            return f"drop {drop['progress']:.1f}/{drop['capture_s']:g}s"
        if cube is not None:
            location, distance = cube
            state = "cube"
            move_yaw = math.atan2(location[1] - xy[1], location[0] - xy[0])
            boost = me["energy"] >= 40 and distance > 15
            self.hunt_progress.pop(hunt_id, None)
        elif hunt_id is not None:
            # Give up on a pickup if we have not closed 1 m on it in 6 s (blocked by a building).
            now = obs["t"]
            best, since = self.hunt_progress.get(hunt_id, (math.inf, now))
            if best_hunt[1] < best - 1:
                self.hunt_progress[hunt_id] = (best_hunt[1], now)
            elif now - since > 6:
                self.unreachable.add(hunt_id)

        act.update(move=[math.cos(move_yaw), math.sin(move_yaw)], aim=[yaw, 0.0],
                   boost=boost, jump=obs["tick"] % 40 == 0)
        return state

    def _hit_gate(self, target, distance, low, high):
        """Degrees of yaw error that still put the shot on the target's body (with a margin)."""
        radius = self.mech_radius * (1 + self.size_per_cube * (target.get("cubes") or 0))
        return min(high, max(low, math.degrees(math.atan2(0.8 * radius, max(distance, 1.0)))))

    def _laser_aim(self, me, target):
        """Aim where the target will be when the beam goes out (about one decision from now)."""
        x, y, z = me["pos"]
        muzzle_z = z + _stat(me.get("stats") or {}, "muzzle_height", self.muzzle_height)
        vx, vy, _ = target.get("vel") or (0.0, 0.0, 0.0)
        tx, ty = target["pos"][0] + vx * LASER_LEAD_S, target["pos"][1] + vy * LASER_LEAD_S
        return [math.atan2(ty - y, tx - x),
                math.atan2(target["pos"][2] + 4.5 - muzzle_z, math.hypot(tx - x, ty - y))]

    def _laser_ready(self, me, weapon, target):
        """Full charge and the torso (as measured now) is on the target's body."""
        stats = weapon.get("stats") or {}
        charge = weapon.get("charge") or 0
        full = 0.93 * _stat(stats, "charge", self.laser.get("charge", 0.75))
        if charge < full:
            self.laser_full_since = None
            return False
        if self.laser_full_since is None:
            self.laser_full_since = self._now
        actual = me.get("aim") or [None]
        if actual[0] is None:
            return False
        x, y, _ = me["pos"]
        distance = math.dist(me["pos"], target["pos"])
        gate = self._hit_gate(target, distance, 0.35, 4.0)
        if self._now - self.laser_full_since >= 0.8:
            # Been waiting a while: loosen up to the full body width (never wider), before the game auto-fires.
            radius = self.mech_radius * (1 + self.size_per_cube * (target.get("cubes") or 0))
            gate = max(gate, min(2 * gate, math.degrees(math.atan2(radius, max(distance, 1.0)))))
        yaw = math.atan2(target["pos"][1] - y, target["pos"][0] - x)
        return abs(math.remainder(yaw - actual[0], math.tau)) <= math.radians(gate)

    def _fight(self, me, weapons, target, act):
        x, y, z = me["pos"]
        muzzle_height = _stat(me.get("stats") or {}, "muzzle_height", self.muzzle_height)
        muzzle = (x, y, z + muzzle_height)
        tx, ty, tz = target["pos"]
        direct = [math.atan2(ty - y, tx - x),
                  math.atan2(tz + 4.5 - muzzle[2], math.hypot(tx - x, ty - y))]
        distance = math.dist(me["pos"], target["pos"])
        actual = me.get("aim")

        def aligned(yaw, degrees):
            return (bool(actual) and actual[0] is not None
                    and abs(math.remainder(yaw - actual[0], math.tau)) <= math.radians(degrees))

        aim = direct
        use_direct = False
        charging = False
        # While the laser charges, the torso follows the gun's lead so the gun keeps hitting;
        # it swings onto the laser line only once the charge is (almost) full.
        gun_useful = any(
            w and w["kind"] == "gun" and distance <= _stat(w.get("stats") or {}, "range", self.gun_range)
            and not (w.get("reload") or 0) > 0 and (w.get("ammo") is None or w["ammo"] > 0)
            for w in weapons[:2])
        for i, weapon in enumerate(weapons[:2]):
            if not weapon:
                continue
            kind = weapon["kind"]
            stats = weapon.get("stats") or {}
            if kind == "gun":
                aim = _lead_aim(muzzle, target, _stat(stats, "speed", self.gun_speed))
                act["fire"][i] = (distance <= _stat(stats, "range", self.gun_range)
                                  and aligned(aim[0], self._hit_gate(target, distance, 0.6, 3.0)))
            elif kind == "laser":
                reach = _stat(stats, "range", self.laser.get("range", 280))
                if distance <= reach and (weapon.get("cooldown", 0) <= 0 or (weapon.get("charge") or 0) > 0):
                    self.laser_target = target["id"]
                    full_charge = _stat(stats, "charge", self.laser.get("charge", 0.75))
                    # Turn onto the laser line one decision early (turning takes ~0.1 s).
                    near_full = (weapon.get("charge") or 0) >= 0.93 * full_charge - 0.1
                    if near_full or not gun_useful:
                        use_direct = True
                        direct = self._laser_aim(me, target)
                    charging = not self._laser_ready(me, weapon, target)
                    act["fire"][i] = charging
                    self.laser_released = not charging
            elif kind == "lightning":
                reach = _stat(stats, "range", self.lightning.get("range", 45))
                if distance <= 0.9 * reach and me["energy"] >= 10:
                    use_direct = True
                    cone = _stat(stats, "cone_deg", self.lightning.get("cone_deg", 30))
                    act["fire"][i] = aligned(direct[0], 0.4 * cone)
        act["aim"] = direct if use_direct else aim
        return charging

    def _remember_sounds(self, sounds, now):
        for sound in sounds:
            if (sound.get("kind") not in ("gun", "laser", "laser_charge", "lightning", "mortar")
                    or sound.get("dist") not in ("near", "mid") or sound.get("bearing") is None):
                continue
            heard = now - sound.get("age", 0)
            if self.last_sound is None or heard >= self.last_sound[0]:
                self.last_sound = (heard, sound["bearing"])

    def _face_bearing(self, mechs, pos, now):
        if self.last_mech_bearing is not None and now - self.last_mech_bearing[0] <= 5:
            return self.last_mech_bearing[1]
        nearest = min((m for m in mechs if m.get("kind") == "mech" and m.get("pos")),
                      key=lambda m: math.dist(pos, m["pos"]), default=None)
        if nearest is not None:
            return math.atan2(nearest["pos"][1] - pos[1], nearest["pos"][0] - pos[0])
        if self.last_sound is not None and now - self.last_sound[0] <= 2:
            return self.last_sound[1]
        return None

    def _laser_guard(self, obs, act):
        """Don't throw away a charge just because this tick's logic stopped holding the trigger:
        keep it for the mech we were charging at (or one shooting us) if it is still tracked,
        in reach and within a small turn. Otherwise let it go, as v8 did (full speed again)."""
        me = obs["self"]
        for i, weapon in enumerate((me.get("weapons") or [])[:2]):
            if not weapon or weapon.get("kind") != "laser" or not (weapon.get("charge") or 0) > 0:
                continue
            fire = act.setdefault("fire", [False, False])
            if fire[i] or self.laser_released or self.healing or not me.get("in_zone", True):
                return
            reach = _stat(weapon.get("stats") or {}, "range", self.laser.get("range", 280))
            now = obs["t"]
            in_reach = [m for m in obs.get("mechs") or [] if m.get("kind") == "mech" and m.get("pos")
                        and m.get("id") not in self.killed and math.dist(m["pos"], me["pos"]) <= reach]
            pick = next((m for m in in_reach if m["id"] == self.laser_target), None) or min(
                (m for m in in_reach if now - self.last_hits.get(m["id"], (-math.inf,))[0] <= THREAT_RECENT_S),
                key=lambda m: math.dist(m["pos"], me["pos"]), default=None)
            if pick is None:
                return
            aim = self._laser_aim(me, pick)
            actual = me.get("aim") or [None]
            if actual[0] is not None and abs(math.remainder(aim[0] - actual[0], math.tau)) > math.radians(30):
                return  # a big turn at half speed isn't worth it
            act["aim"] = aim
            fire[i] = not self._laser_ready(me, weapon, pick)
            return

    def act(self, obs: mf.Observation) -> mf.Action:
        self.laser_released = False
        self._now = obs.get("t", 0.0)
        try:
            action = self._act(obs)
            try:
                self._laser_guard(obs, action)
            except Exception:
                traceback.print_exc()
            self.previous_move = action["move"]
            return action
        except Exception:
            traceback.print_exc()
            return {"tick": obs.get("tick", 0), "move": self.previous_move}

    def _act(self, obs: mf.Observation) -> mf.Action:
        now = obs["t"]
        events = obs.get("events") or []
        self._remember_damage(events, now)
        self.killed.update(e["target"] for e in events if e.get("type") == "kill" and "target" in e)
        self._remember_sounds(obs.get("sounds") or [], now)
        me = obs["self"]
        weapons = me.get("weapons") or []
        mechs = obs.get("mechs") or []
        act: mf.Action = {"tick": obs["tick"], "fire": [False, False]}
        choices = (obs.get("offer") or {}).get("choices") or []
        if choices:
            act["pick"] = min(range(len(choices)),
                              key=lambda i: UPGRADE_RANK.get(choices[i].get("id"), len(UPGRADE_RANK)))
        target = self._choose_target(mechs, me["pos"], now, weapons, me.get("cubes", 0))
        # Don't break off to heal when the target is nearly dead and weaker than us: take the kill.
        finishing = (target is not None and target.get("hp") is not None and target.get("max_hp")
                     and target["hp"] <= 0.3 * target["max_hp"] and target["hp"] < me["hp"])
        healing = not finishing and self._heal(obs, act)
        drop = self._drop_goal(obs, healing)
        if healing:
            # Still being shot (regen is paused anyway): shoot back at that attacker while retreating.
            if target is not None:
                hit = self.last_hits.get(target["id"])
                if hit is not None and now - hit[0] <= HEAL_FIGHTBACK_S:
                    move, boost = act["move"], act.get("boost")
                    self._fight(me, weapons, target, act)
                    act.update(move=move, boost=boost)
                    # Don't start a laser charge here: it would halve our speed on the way to cover.
                    for i, weapon in enumerate(weapons[:2]):
                        if weapon and weapon["kind"] == "laser" and not (weapon.get("charge") or 0) > 0:
                            act["fire"][i] = False
            return act
        movement = self._movement(obs, len(weapons) < 2 or weapons[1] is None, act, drop)
        state = "idle"
        charging = False
        if target is not None:
            hp = target.get("hp")
            state = f"fight {target['id']} hp {round(hp) if hp is not None else '?'}"
            charging = self._fight(me, weapons, target, act)
        else:
            bearing = self._face_bearing(mechs, me["pos"], now)
            if bearing is not None:
                state = "face"
                act["aim"] = [bearing, 0.0]
        mf.draw.label(f"{movement} {state}" + (" chg" if charging else ""))
        return act


if __name__ == "__main__":
    mf.run(Bot)
