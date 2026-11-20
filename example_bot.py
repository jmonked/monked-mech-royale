"""Walk to the zone and return fire on attackers or nearby mechs."""
import json
import math
import sys
import traceback
from array import array
from collections import defaultdict
from pathlib import Path

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


class _SightMap:
    """Index cover on the arena's terrain grid once, then sample eye-to-target rays."""

    def __init__(self, directory):
        with (directory / "world.json").open(encoding="utf-8") as f:
            world = json.load(f)
        grid = world["terrain"]
        self.x0, self.y0, self.step = grid["minX"], grid["minY"], grid["step"]
        self.nx, self.ny = grid["nx"], grid["ny"]
        self.scale = grid["scale"]
        self.ground = array("h")
        with (directory / grid["file"]).open("rb") as f:
            self.ground.fromfile(f, self.nx * self.ny)
        if sys.byteorder != "little":
            self.ground.byteswap()

        self.cover = defaultdict(list)
        for prism in world["prisms"]:
            # An even-odd scanline fills the footprint but leaves courtyard holes open.
            crossings = defaultdict(list)
            for ring in (prism["ring"], *prism["holes"]):
                vertices = list(zip(ring[::2], ring[1::2]))
                for (ax, ay), (bx, by) in zip(vertices, vertices[1:] + vertices[:1]):
                    for j in self._indices(min(ay, by), max(ay, by), self.y0, self.ny):
                        y = self.y0 + (j + 0.5) * self.step
                        crossings[j].append(ax + (bx - ax) * (y - ay) / (by - ay))
            span = (prism["base"], prism["top"], False)
            for j, xs in crossings.items():
                xs.sort()
                for lo, hi in zip(xs[::2], xs[1::2]):
                    for i in self._indices(lo, hi, self.x0, self.nx):
                        self.cover[j * self.nx + i].append(span)

        trees = world["trees"]
        fields = trees["fields"]
        for offset in range(0, len(trees["data"]), len(fields)):
            tree = dict(zip(fields, trees["data"][offset:offset + len(fields)]))
            base = tree["z"]
            crown = base + tree["crownBase"]
            self._add_tree_part(tree["x"], tree["y"], tree["trunkR"], base, crown, False)
            self._add_tree_part(tree.get("crownX", tree["x"]), tree.get("crownY", tree["y"]),
                                tree["crownR"], crown, base + tree["height"], True)
        rules = world["rules"]
        # exp(-density * distance) is the estimated light transmission through foliage.
        self.foliage_limit = -math.log(rules["canopyBlockT"]) / rules["canopyDensity"]

    def _indices(self, lo, hi, origin, count):
        start = math.ceil((lo - origin) / self.step - 0.5)
        stop = math.ceil((hi - origin) / self.step - 0.5)
        return range(max(0, start), min(count - 1, stop))

    def _add_tree_part(self, x, y, radius, bottom, top, foliage):
        if radius <= 0:
            return
        half_height = (top - bottom) / 2
        for j in self._indices(y - radius, y + radius, self.y0, self.ny):
            dy = self.y0 + (j + 0.5) * self.step - y
            for i in self._indices(x - radius, x + radius, self.x0, self.nx):
                dx = self.x0 + (i + 0.5) * self.step - x
                fraction = 1 - (dx * dx + dy * dy) / (radius * radius)
                if fraction >= 0:
                    inset = half_height * (1 - math.sqrt(fraction)) if foliage else 0
                    self.cover[j * self.nx + i].append((bottom + inset, top - inset, foliage))

    def clear(self, eye, end, check_foliage):
        x, y, z = eye
        dx, dy, dz = end[0] - x, end[1] - y, end[2] - z
        length = math.hypot(dx, dy, dz)
        samples = max(1, math.ceil(length / self.step))
        gx, gy = (x - self.x0) / self.step, (y - self.y0) / self.step
        sx, sy, sz = dx / (samples * self.step), dy / (samples * self.step), dz / samples
        gx, gy, z = gx + sx / 2, gy + sy / 2, z + sz / 2
        foliage_depth = 0.0
        for _ in range(samples):
            i, j = math.floor(gx), math.floor(gy)
            if 0 <= i < self.nx - 1 and 0 <= j < self.ny - 1:
                cell = j * self.nx + i
                fx, fy = gx - i, gy - j
                g = self.ground
                low = g[cell] * (1 - fx) + g[cell + 1] * fx
                high = g[cell + self.nx] * (1 - fx) + g[cell + self.nx + 1] * fx
                if z < (low * (1 - fy) + high * fy) * self.scale:
                    return False
                leafy = False
                for bottom, top, foliage in self.cover.get(cell, ()):
                    if bottom <= z <= top:
                        if not foliage:
                            return False
                        leafy = True
                if check_foliage and leafy:
                    foliage_depth += length / samples
                    if foliage_depth >= self.foliage_limit:
                        return False
            gx, gy, z = gx + sx, gy + sy, z + sz
        return True


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
        self.last_hits = {}
        self.last_damage_bearing = None
        self.last_mech_bearing = None
        self.previous_move = [0.0, 0.0]
        vision = config.get("vision") or {}
        self.view_range = _stat(vision, "range", 200)
        self.half_fov = math.radians(_stat(vision, "fov_deg", 120)) / 2
        self.canopy_blocks = _stat(vision, "canopy_blocks", True)
        mech = config.get("mech") or {}
        self.eye_height = _stat(mech, "eye_height", 8)
        self.mech_height = _stat(mech, "height", 9)
        self.size_per_cube = _stat(config.get("cubes") or {}, "size_per_cube", 0.05)
        self.last_seen = {}
        self.sight_map = None
        map_dir = (hello.get("map") or {}).get("dir")
        if map_dir:
            try:
                self.sight_map = _SightMap(Path(map_dir) / "v2")
            except Exception:  # never crash at hello: fall back to firing without a sight check
                traceback.print_exc()

    def _update_sight(self, me, actors, target, now):
        previous = self.last_seen
        # First appearance (including reappearance after memory expires) proves sight.
        self.last_seen = {
            actor["id"]: previous.get(actor["id"], now)
            for actor in actors
            if actor.get("kind") == "mech" and actor.get("id") is not None and actor.get("pos")
        }
        if target is None or target["id"] not in previous:
            return
        x, y, z = me["pos"]
        stats = me.get("stats") or {}
        eye = (x, y, z + _stat(stats, "eye_height", self.eye_height))
        near = self.near_range + _stat(stats, "near_range_bonus", 0)
        far = self.view_range + _stat(stats, "vision_bonus", 0)
        actual = me.get("aim")
        tx, ty, tz = target["pos"]
        height = self.mech_height * (1 + self.size_per_cube * (target.get("cubes") or 0))
        distance = math.hypot(tx - x, ty - y, tz + height / 2 - eye[2])
        close = distance <= near
        if not close:
            if distance > far or not actual or actual[0] is None:
                return
            bearing = math.atan2(ty - y, tx - x)
            if abs(math.remainder(bearing - actual[0], math.tau)) > self.half_fov:
                return
        if self.sight_map is None or any(
            self.sight_map.clear(eye, (tx, ty, end_z), self.canopy_blocks and not close)
            for end_z in (tz + height, tz + height / 2)
        ):
            self.last_seen[target["id"]] = now

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
        goal = obs["zone"]["next_center"]
        act: mf.Action = {"tick": obs["tick"]}
        if obs.get("offer"):
            act["pick"] = 0
        near = [p for p in (obs.get("pickups") or []) if math.dist(p["pos"][:2], (x, y)) < self.reach]
        weapons = me.get("weapons") or []
        if (len(weapons) < 2 or weapons[1] is None) and near and near[0]["kind"] != "gun":
            act["take"] = near[0]["id"]
        yaw = math.atan2(goal[1] - y, goal[0] - x)
        act.update(move=[math.cos(yaw), math.sin(yaw)], aim=[yaw, 0.0], boost=not me["in_zone"], jump=obs["tick"] % 40 == 0)

        state = "idle"
        actors = obs.get("mechs") or []
        target = self._choose_target(actors, me["pos"], now)
        self._update_sight(me, actors, target, now)
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
                if in_range and abs(yaw_error) <= math.radians(3) and now - self.last_seen[target["id"]] < 1.0:
                    act["fire"] = [True, True]
        elif self.last_mech_bearing is not None and now - self.last_mech_bearing[0] <= 3.0:
            state = "face"
            act["aim"] = [self.last_mech_bearing[1], 0.0]
        mf.draw.label(state)
        return act


if __name__ == "__main__":
    mf.run(Bot)
