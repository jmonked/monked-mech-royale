"""Hunt for a laser early and return fire on attackers or nearby mechs."""
import math
import traceback

import mechfight as mf


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


class Bot:
    name = "monked"

    def __init__(self, hello: mf.Hello):
        config = hello.get("config") or {}
        self.reach = _stat(config.get("loot") or {}, "pickup_radius", 4)
        self.near_range = _stat(config.get("vision") or {}, "near_range", 45)
        gun = (config.get("weapons") or {}).get("gun") or {}
        self.gun_speed = _stat(gun, "speed", 252)
        self.gun_range = _stat(gun, "range", 230)
        self.laser = (config.get("weapons") or {}).get("laser") or {}
        self.lightning = (config.get("weapons") or {}).get("lightning") or {}
        self.muzzle_height = _stat(config.get("mech") or {}, "muzzle_height", 7)
        self.last_hits = {}
        self.last_damage_bearing = None
        self.last_mech_bearing = None
        self.last_sound = None
        self.pickups = {}
        self.unreachable = set()
        self.hunt_progress = {}
        self.previous_move = [0.0, 0.0]

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

    def _choose_target(self, mechs, pos, now):
        target = None
        closest = math.inf
        for mech in mechs:
            if mech.get("kind") != "mech" or mech.get("id") is None or not mech.get("pos"):
                continue
            distance = math.dist(mech["pos"], pos)
            hit = self.last_hits.get(mech["id"])
            recent = hit is not None and now - hit[0] <= 8.0
            if not recent and distance > self.near_range:
                continue
            # Prefer a recent attacker when the distances differ by about a metre.
            ranked_distance = distance - (1.0 if recent else 0.0)
            if ranked_distance < closest:
                target, closest = mech, ranked_distance
        return target

    def _movement(self, obs, slot_empty, act):
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
        if slot_empty:
            best_take = best_hunt = (2, math.inf)
            hunt_id = None
            for pickup_id, pickup in self.pickups.items():
                kind = pickup["kind"]
                if kind not in ("laser", "lightning"):
                    continue
                location = pickup["pos"][:2]
                distance = math.dist(xy, location)
                rank = (0 if kind == "laser" else 1, distance)
                if pickup_id in visible and distance <= self.reach and rank < best_take:
                    act["take"] = pickup_id
                    best_take = rank
                # Skip rooftop pickups (take needs <= 4 m vertical) and ones we failed to reach.
                if pickup["pos"][2] - me["pos"][2] > 5 or pickup_id in self.unreachable:
                    continue
                if (obs["t"] < 90 and distance <= 250 and rank < best_hunt
                        and math.dist(location, zone["next_center"]) <= zone["next_radius"]):
                    best_hunt = rank
                    hunt_id = pickup_id
                    state = "laser hunt"
                    goal = location
                    boost = outside or (me["energy"] >= 30 and distance > 25)
            if hunt_id is not None:
                # Give up on a pickup if we have not closed 1 m on it in 6 s (blocked by a building).
                now = obs["t"]
                best, since = self.hunt_progress.get(hunt_id, (math.inf, now))
                if best_hunt[1] < best - 1:
                    self.hunt_progress[hunt_id] = (best_hunt[1], now)
                elif now - since > 6:
                    self.unreachable.add(hunt_id)

        yaw = math.atan2(goal[1] - xy[1], goal[0] - xy[0])
        act.update(move=[math.cos(yaw), math.sin(yaw)], aim=[yaw, 0.0],
                   boost=boost, jump=obs["tick"] % 40 == 0)
        return state

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
        for i, weapon in enumerate(weapons[:2]):
            if not weapon:
                continue
            kind = weapon["kind"]
            stats = weapon.get("stats") or {}
            if kind == "gun":
                aim = _lead_aim(muzzle, target, _stat(stats, "speed", self.gun_speed))
                act["fire"][i] = distance <= _stat(stats, "range", self.gun_range) and aligned(aim[0], 3)
            elif kind == "laser":
                reach = _stat(stats, "range", self.laser.get("range", 280))
                if distance <= reach and weapon.get("cooldown", 0) <= 0:
                    use_direct = True
                    full_charge = _stat(stats, "charge", self.laser.get("charge", 0.75))
                    charged = weapon.get("charge", 0) >= 0.93 * full_charge
                    charging = not (charged and aligned(direct[0], 1.5))
                    act["fire"][i] = charging
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

    def act(self, obs: mf.Observation) -> mf.Action:
        try:
            action = self._act(obs)
            self.previous_move = action["move"]
            return action
        except Exception:
            traceback.print_exc()
            return {"tick": obs.get("tick", 0), "move": self.previous_move}

    def _act(self, obs: mf.Observation) -> mf.Action:
        now = obs["t"]
        self._remember_damage(obs.get("events") or [], now)
        self._remember_sounds(obs.get("sounds") or [], now)
        me = obs["self"]
        weapons = me.get("weapons") or []
        mechs = obs.get("mechs") or []
        act: mf.Action = {"tick": obs["tick"], "fire": [False, False]}
        if obs.get("offer"):
            act["pick"] = 0
        movement = self._movement(obs, len(weapons) < 2 or weapons[1] is None, act)
        state = "idle"
        charging = False
        target = self._choose_target(mechs, me["pos"], now)
        if target is not None:
            state = f"fight {target['id']}"
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
