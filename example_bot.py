"""Walk to the zone and return fire on attackers or nearby mechs."""
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
        self.muzzle_height = _stat(config.get("mech") or {}, "muzzle_height", 7)
        self.walk_speed = _stat(config.get("mech") or {}, "walk_speed", 11.7)
        self.last_hits = {}
        self.last_damage_bearing = None
        self.last_mech_bearing = None
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
        me = obs["self"]
        x, y, z = me["pos"]
        act: mf.Action = {"tick": obs["tick"]}
        if obs.get("offer"):
            act["pick"] = 0
        near = [p for p in (obs.get("pickups") or []) if math.dist(p["pos"][:2], (x, y)) < self.reach]
        weapons = me.get("weapons") or []
        if (len(weapons) < 2 or weapons[1] is None) and near and near[0]["kind"] != "gun":
            act["take"] = near[0]["id"]
        zone = obs.get("zone") or {}
        goal = zone.get("next_center") or zone.get("center") or (x, y)
        dx, dy = goal[0] - x, goal[1] - y
        distance = math.hypot(dx, dy)
        next_radius = _stat(zone, "next_radius", 0.0)
        margin = min(25.0, 0.25 * next_radius)
        safe_r = max(0.0, next_radius - margin)
        moving = distance > (safe_r if safe_r > 0.0 else 2.0)
        move = [dx / distance, dy / distance] if moving else [0.0, 0.0]
        boost = not me["in_zone"]
        shrink_end = zone.get("shrink_end")
        if moving and not boost and _stat(me, "energy", 0.0) >= 15 and shrink_end is not None:
            walk_speed = _stat(me.get("stats") or {}, "walk_speed", self.walk_speed)
            boost = walk_speed > 0 and (distance - safe_r) / walk_speed > (shrink_end - now) * 0.8 - 2
        yaw = math.atan2(dy, dx)
        act.update(move=move, aim=[yaw, 0.0], boost=boost, jump=obs["tick"] % 40 == 0)

        state = "idle"
        target = self._choose_target(obs.get("mechs") or [], me["pos"], now)
        if target is not None:
            state = f"fight {target['id']}"
            gun = (weapons[0] if weapons else None) or {}
            stats = gun.get("stats") or {}
            speed = _stat(stats, "speed", self.gun_speed)
            muzzle_height = _stat(me.get("stats") or {}, "muzzle_height", self.muzzle_height)
            aim = _lead_aim((x, y, z + muzzle_height), target, speed)
            act["aim"] = aim
            actual = me.get("aim")
            if gun.get("kind") == "gun" and actual and actual[0] is not None:
                yaw_error = math.remainder(aim[0] - actual[0], math.tau)
                in_range = math.dist(me["pos"], target["pos"]) <= _stat(stats, "range", self.gun_range)
                if in_range and abs(yaw_error) <= math.radians(3):
                    act["fire"] = [True, True]
        elif self.last_mech_bearing is not None and now - self.last_mech_bearing[0] <= 3.0:
            state = "face"
            act["aim"] = [self.last_mech_bearing[1], 0.0]
        movement = "boost" if boost else "to zone" if moving else "safe"
        mf.draw.label(f"{movement} {state}")
        return act


if __name__ == "__main__":
    mf.run(Bot)
