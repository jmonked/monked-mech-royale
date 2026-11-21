"""v50-opus: clean-sheet bot. One pipeline per decision:
memory -> threat picture -> target (seen or unseen) -> weapons + aim -> goals -> one movement
evaluator (12 directions + stand still) -> boost / hop. No behaviour overwrites another's output."""
import heapq
import json
import math
import random
import time
import traceback
from pathlib import Path

import mechfight as mf

LATE_T = 230.0        # 3rd shrink on: no chasing, let the zone thin them out
HIT_RECENT = 3.0      # an attacker counts as "shooting us now" for this long
HEAL_EXIT = 0.85
CELL = 32.0           # building lookup grid (m)
NCELL = 6.0           # navigation grid (m)
NB8 = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0), (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)]
DIRS = [(math.cos(k * math.pi / 6), math.sin(k * math.pi / 6)) for k in range(12)] + [(0.0, 0.0)]
DRONE_RANGE, DRONE_CUBE_CAP = 55.0, 15
COMBAT_SOUNDS = ("gun", "laser", "laser_charge", "lightning", "mortar")
UPGRADE_RANK = {n: r for r, n in enumerate((
    "plating", "laser_damage", "laser_charge", "armor", "gun_damage", "gun_rate", "gun_mag", "nanites",
    "lightning_efficiency", "lightning_range", "lightning_chain", "gyros", "servos", "gun_velocity", "sensors",
    "laser_pierce", "capacitor", "reactor", "jets", "mortar_reload", "mortar_splash", "mortar_velocity"))}


def _in_ring(px, py, ring):
    inside = False
    ax, ay = ring[-1]
    for bx, by in ring:
        if (ay > py) != (by > py) and px < ax + (py - ay) * (bx - ax) / (by - ay):
            inside = not inside
        ax, ay = bx, by
    return inside


def _in_prism(px, py, ring, holes):
    return _in_ring(px, py, ring) and not any(_in_ring(px, py, h) for h in holes)


def _ring_intervals(ax, ay, dx, dy, ring):
    """Sorted [(t0, t1)] in [0, 1] where segment a + t*d lies inside ring."""
    cross = []
    px, py = ring[-1]
    sa = dx * (py - ay) - dy * (px - ax)
    for qx, qy in ring:
        sb = dx * (qy - ay) - dy * (qx - ax)
        if (sa > 0) != (sb > 0):
            cross.append(((px - ax) * (qy - py) - (py - ay) * (qx - px)) / (sb - sa))
        px, py, sa = qx, qy, sb
    cross.sort()
    return [(max(a, 0.0), min(b, 1.0)) for a, b in zip(cross[::2], cross[1::2]) if min(b, 1.0) - max(a, 0.0) > 1e-9]


def _subtract(ivs, cuts):
    for c0, c1 in cuts:
        nxt = []
        for a, b in ivs:
            if c1 <= a or c0 >= b:
                nxt.append((a, b))
                continue
            if a < c0:
                nxt.append((a, c0))
            if b > c1:
                nxt.append((c1, b))
        ivs = nxt
    return ivs


def _seg_dist_sq(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = 0.0 if L <= 1e-12 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L))
    return (px - ax - t * dx) ** 2 + (py - ay - t * dy) ** 2


def _strafe_sign(now):
    return 1.0 if math.sin(now * 3.1) + 0.55 * math.sin(now * 5.3) >= 0.0 else -1.0


def _unit(dx, dy):
    d = math.hypot(dx, dy)
    return (dx / d, dy / d, d) if d > 1e-6 else (0.0, 0.0, 0.0)


def _angdiff(a, b):
    return abs(math.remainder(a - b, math.tau))


class World:
    """Static map: building prisms on a grid, roofs with climb points, cover spots, openness."""

    def __init__(self, path):
        self.blds, self.grid, self.roofs, self.spots = [], {}, [], []
        self.nav = None
        if path is None:
            return
        with open(path, encoding="utf-8") as f:
            world = json.load(f)
        for p in world.get("prisms") or []:
            if p.get("kind") not in ("building", "stadium"):
                continue
            ring = list(zip(p["ring"][::2], p["ring"][1::2]))
            holes = [list(zip(h[::2], h[1::2])) for h in (p.get("holes") or []) if len(h) >= 6]
            a2 = cx = cy = 0.0
            for (ax, ay), (bx, by) in zip(ring[-1:] + ring[:-1], ring):
                c = ax * by - bx * ay
                a2, cx, cy = a2 + c, cx + (ax + bx) * c, cy + (ay + by) * c
            if abs(a2) < 1e-8:
                continue
            cx, cy = cx / (3 * a2), cy / (3 * a2)
            rad = max(math.hypot(x - cx, y - cy) for x, y in ring)
            idx = len(self.blds)
            self.blds.append((cx, cy, rad, ring, holes, p["base"], p["top"], a2 > 0))
            xs, ys = [x for x, _ in ring], [y for _, y in ring]
            for i in range(int(math.floor(min(xs) / CELL)), int(math.floor(max(xs) / CELL)) + 1):
                for j in range(int(math.floor(min(ys) / CELL)), int(math.floor(max(ys) / CELL)) + 1):
                    self.grid.setdefault((i, j), []).append(idx)
        b = world.get("bounds") or {}
        bounds = (b.get("minX", -520), b.get("minY", -340), b.get("maxX", 560), b.get("maxY", 390))
        self._roofs_and_spots()
        self._raster(*bounds)

    def _roofs_and_spots(self):
        seen = set()
        for cx, cy, rad, ring, holes, base, top, ccw in self.blds:
            h = top - base
            if h < 9:
                continue
            if h <= 45 and rad >= 8 and _in_prism(cx, cy, ring, holes):
                climbs = []
                for ux, uy in ((1, 0), (-1, 0), (0, 1), (0, -1), (.707, .707), (-.707, .707), (.707, -.707), (-.707, -.707)):
                    vx, vy = max(ring, key=lambda q: q[0] * ux + q[1] * uy)
                    if not self.solid(vx + 3.5 * ux, vy + 3.5 * uy, base):
                        climbs.append((vx + 3.5 * ux, vy + 3.5 * uy))
                if climbs:
                    self.roofs.append((len(self.roofs), (cx, cy), rad, ring, holes, top, climbs))
            sgn = 1.0 if ccw else -1.0
            n = len(ring)
            for k in range(n):
                ax, ay = ring[k - 1]
                vx, vy = ring[k]
                bx, by = ring[(k + 1) % n]
                e1x, e1y, l1 = _unit(vx - ax, vy - ay)
                e2x, e2y, l2 = _unit(bx - vx, by - vy)
                pts = []
                if l2 >= 24:   # long wall: hold its middle too
                    pts.append(((vx + bx) / 2 + 4.5 * sgn * e2y, (vy + by) / 2 - 4.5 * sgn * e2x))
                if max(l1, l2) >= 3 and (e1x * e2y - e1y * e2x) * sgn > 0.2:   # convex corner
                    nx, ny, _ = _unit(sgn * (e1y + e2y), -sgn * (e1x + e2x))
                    pts.append((vx + 4.5 * nx, vy + 4.5 * ny))
                for sx, sy in pts:
                    key = (round(sx / 6), round(sy / 6))
                    if key not in seen and not self.solid(sx, sy, base):
                        seen.add(key)
                        self.spots.append((sx, sy))

    def _raster(self, x0, y0, x1, y1):
        """Walkable 6 m grid: a cell is blocked when its centre is inside a building (scanline fill)."""
        nx, ny = int((x1 - x0) / NCELL) + 1, int((y1 - y0) / NCELL) + 1
        blk = bytearray(nx * ny)
        for _cx, _cy, _r, ring, holes, base, top, _ccw in self.blds:
            if top - base <= 1.2:
                continue
            rings = [ring] + holes
            ys = [q[1] for q in ring]
            for j in range(max(0, int((min(ys) - y0) / NCELL)), min(ny - 1, int((max(ys) - y0) / NCELL)) + 1):
                yc = y0 + (j + 0.5) * NCELL
                xs = []
                for r in rings:
                    ax, ay = r[-1]
                    for bx, by in r:
                        if (ay > yc) != (by > yc):
                            xs.append(ax + (yc - ay) * (bx - ax) / (by - ay))
                        ax, ay = bx, by
                xs.sort()
                for a, b in zip(xs[::2], xs[1::2]):
                    i0, i1 = max(0, math.ceil((a - x0) / NCELL - 0.5)), min(nx - 1, math.floor((b - x0) / NCELL - 0.5))
                    blk[j * nx + i0:j * nx + i1 + 1] = b"" * max(0, i1 - i0 + 1)
        self.nav = (blk, x0, y0, nx, ny)

    def path(self, sx, sy, gx, gy, limit=700):
        """Weighted A* on the 6 m grid (bounded work); ends at the goal or the reached cell closest to it."""
        if self.nav is None:
            return [(gx, gy)]
        blk, x0, y0, nx, ny = self.nav

        def cell(x, y):
            return min(ny - 1, max(0, int((y - y0) / NCELL))) * nx + min(nx - 1, max(0, int((x - x0) / NCELL)))
        s, g = cell(sx, sy), cell(gx, gy)
        gi, gj = g % nx, g // nx
        heap, prev, cost = [(0.0, 0.0, s)], {s: -1}, {s: 0.0}
        best, best_h, n = s, math.inf, 0
        while heap and n < limit:
            _f, c, u = heapq.heappop(heap)
            if c > cost[u]:
                continue
            n += 1
            ui, uj = u % nx, u // nx
            hx, hy = abs(ui - gi), abs(uj - gj)
            if max(hx, hy) + 0.414 * min(hx, hy) < best_h:
                best, best_h = u, max(hx, hy) + 0.414 * min(hx, hy)
            if u == g:
                break
            for di, dj, w in NB8:
                vi, vj = ui + di, uj + dj
                if not (0 <= vi < nx and 0 <= vj < ny):
                    continue
                v = vj * nx + vi
                if blk[v] or (di and dj and (blk[uj * nx + vi] or blk[vj * nx + ui])):
                    continue
                if c + w < cost.get(v, math.inf):
                    cost[v], prev[v] = c + w, u
                    hx, hy = abs(vi - gi), abs(vj - gj)
                    heapq.heappush(heap, (c + w + 1.8 * (max(hx, hy) + 0.414 * min(hx, hy)), c + w, v))
        out, u = [], best
        while u != -1:
            out.append((x0 + (u % nx + 0.5) * NCELL, y0 + (u // nx + 0.5) * NCELL))
            u = prev[u]
        out.reverse()
        if best == g:
            out[-1] = (gx, gy)
        return out

    def walk_blocked(self, ax, ay, bx, by, z):
        """Is there a wall (taller than a step at feet height z) on the straight walk from a to b?"""
        return self.blocked((ax, ay, z + 1.3), (bx, by, z + 1.3))

    def openness(self, x, y):
        """0 next to a building, 0.5 within 24 m of one, 1 in the open (from the nav grid)."""
        if self.nav is None:
            return 0.0
        blk, x0, y0, nx, ny = self.nav
        i, j = int((x - x0) / NCELL), int((y - y0) / NCELL)
        for r, val in ((2, 0.0), (4, 0.5)):
            for jj in range(max(0, j - r), min(ny, j + r + 1)):
                if any(blk[jj * nx + ii] for ii in range(max(0, i - r), min(nx, i + r + 1))):
                    return val
        return 1.0

    def cell_blds(self, x, y):
        return self.grid.get((int(math.floor(x / CELL)), int(math.floor(y / CELL)))) or ()

    def seg_blds(self, ax, ay, bx, by):
        """Buildings registered in every grid cell the segment passes (DDA walk)."""
        i, j = int(math.floor(ax / CELL)), int(math.floor(ay / CELL))
        ei, ej = int(math.floor(bx / CELL)), int(math.floor(by / CELL))
        dx, dy = bx - ax, by - ay
        si, sj = (1 if dx > 0 else -1), (1 if dy > 0 else -1)
        tdx = abs(CELL / dx) if dx else math.inf
        tdy = abs(CELL / dy) if dy else math.inf
        tmx = ((i + (si > 0)) * CELL - ax) / dx if dx else math.inf
        tmy = ((j + (sj > 0)) * CELL - ay) / dy if dy else math.inf
        out = set()
        for _ in range(abs(ei - i) + abs(ej - j) + 1):
            out.update(self.grid.get((i, j)) or ())
            if tmx < tmy:
                tmx, i = tmx + tdx, i + si
            else:
                tmy, j = tmy + tdy, j + sj
        return out

    def blocked(self, a, b):
        lo, hi = min(a[2], b[2]), max(a[2], b[2])
        dx, dy, dz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
        for k in self.seg_blds(a[0], a[1], b[0], b[1]):
            cx, cy, rad, ring, holes, base, top, _ = self.blds[k]
            if top <= lo or base >= hi or _seg_dist_sq(cx, cy, a[0], a[1], b[0], b[1]) > rad * rad:
                continue
            ivs = _ring_intervals(a[0], a[1], dx, dy, ring)
            for h in holes:
                if ivs:
                    ivs = _subtract(ivs, _ring_intervals(a[0], a[1], dx, dy, h))
            for t0, t1 in ivs:
                z0, z1 = a[2] + dz * t0, a[2] + dz * t1
                if max(z0, z1) > base and min(z0, z1) < top:
                    return True
        return False

    def solid(self, x, y, z):
        """A wall we would walk into at feet height z."""
        for k in self.cell_blds(x, y):
            cx, cy, rad, ring, holes, base, top, _ = self.blds[k]
            if top > z + 1.2 and base < z + 8.0 and (x - cx) ** 2 + (y - cy) ** 2 <= (rad + 1) ** 2 \
                    and _in_prism(x, y, ring, holes):
                return True
        return False

    def roof_at(self, pos):
        for roof in self.roofs:
            _i, c, rad, ring, holes, top, _cl = roof
            if abs(pos[2] - top) <= 1.5 and math.dist(pos[:2], c) <= rad + 1 and _in_prism(pos[0], pos[1], ring, holes):
                return roof
        return None


class Bot:
    name = "monked"

    def __init__(self, hello: mf.Hello):
        cfg = hello.get("config") or {}
        mech, W = cfg.get("mech") or {}, cfg.get("weapons") or {}
        self.radius, self.height = mech.get("radius", 2.5), mech.get("height", 9.0)
        self.muzzle = mech.get("muzzle_height", 7.0)
        self.walk = mech.get("walk_speed", 11.7)
        self.accel, self.air_accel = mech.get("ground_accel", 58.5), mech.get("air_accel", 12.0)
        self.gun_cfg, self.laser_cfg, self.light_cfg = W.get("gun") or {}, W.get("laser") or {}, W.get("lightning") or {}
        self.mortar_g = (W.get("mortar") or {}).get("gravity", 22.0)
        self.splash = (W.get("mortar") or {}).get("splash_radius", 7.0) + 1.5
        self.laser_cd = self.laser_cfg.get("cooldown", 1.65)
        self.near = (cfg.get("vision") or {}).get("near_range", 45)
        cubes = cfg.get("cubes") or {}
        self.size_per_cube = cubes.get("size_per_cube", 0.05)
        self.reach = (cfg.get("loot") or {}).get("pickup_radius", 4)
        npc = cfg.get("npc") or {}
        self.npc_r, self.npc_hh = npc.get("radius", 1.8), 0.5 * npc.get("height", 3.5)
        self.rng = random.Random(hello.get("seed") or 0)
        try:
            self.world = World(Path(hello["map"]["dir"]) / "v2" / "world.json")
        except Exception:
            traceback.print_exc()
            self.world = World(None)
        self.tracks, self.hits, self.dealt, self.laser_fired, self.seen = {}, {}, {}, {}, {}
        self.killed, self.kill_spots, self.heard = set(), [], []
        self.pickups, self.cubes, self.unreachable, self.progress = {}, {}, set(), {}
        self.dmg_bearing = self.beam_threat = None
        self.short_until = self.stuck_until = -math.inf
        self.stuck_dir, self.pos_hist = (0.0, 0.0), []
        self.target_id = self.drop_id = None
        self.laser_full_since = None
        self.drop_retry, self.drop_contest = {}, {}
        self.healing, self.heal_spot, self.place, self.place_t, self.roof_goal = False, None, None, -99.0, None
        self.unreachable_roofs = set()
        self.prev_move, self.prev_aim, self.prev_fire = [0.0, 0.0], None, [False, False]
        self.prev_alive, self.other_deaths, self.is_finals = 16, 0, False
        self.paths = {}
        self.now = 0.0

    # ------------------------------------------------------------------ safety wrapper
    def act(self, obs: mf.Observation) -> mf.Action:
        self.now = obs.get("t", 0.0) or 0.0
        try:
            act = self._act(obs)
            self.prev_move, self.prev_aim, self.prev_fire = act["move"], act.get("aim"), list(act["fire"])
            return act
        except Exception:
            traceback.print_exc()
            act = {"tick": obs.get("tick", 0), "move": self.prev_move, "fire": list(self.prev_fire)}
            if self.prev_aim:
                act["aim"] = self.prev_aim
            return act

    # ------------------------------------------------------------------ memory
    def _memory(self, obs, me, now):
        pos = me["pos"]
        new_kills = 0
        for e in obs.get("events") or []:
            et = e.get("type")
            if et == "damaged" and e.get("bearing") is not None:
                self.dmg_bearing = (now, e["bearing"])
                if e.get("by") is not None:
                    self.hits[e["by"]] = (now, e["bearing"], e.get("weapon"))
            elif et == "hit" and e.get("target") is not None:
                self.dealt[e["target"]] = now
            elif et == "kill" and e.get("target") is not None:
                new_kills += e["target"] not in self.killed
                self.killed.add(e["target"])
                self.hits.pop(e["target"], None)
                if e["target"] in self.seen:
                    self.kill_spots.append((now, self.seen[e["target"]][1][:2]))
            elif et == "effect" and e.get("effect") == "short":
                self.short_until = now + self.light_cfg.get("short_s", 2.0)
            elif et in ("took", "take_failed"):
                self.pickups.pop(e.get("id"), None)
        alive = obs.get("alive")
        if alive is not None:   # >= 2 deaths we didn't cause before 110 s means a free-for-all
            if not self.is_finals and now < 110 and alive < self.prev_alive:
                if not any(now - t <= 3 for t in self.dealt.values()):
                    self.other_deaths += self.prev_alive - alive - new_kills
                    self.is_finals = self.other_deaths >= 2
            self.prev_alive = alive
        self.heard = [h for h in self.heard if now - h[0] <= 4.0]
        for s in obs.get("sounds") or []:
            if s.get("bearing") is not None and s.get("dist") in ("near", "mid"):
                self.heard.append((now - (s.get("age") or 0), s["bearing"], s.get("dist"), s.get("kind")))
        for bm in obs.get("beams") or []:
            by, path = bm.get("by"), bm.get("path") or []
            if by is None or by in self.killed or not path or len(path[0]) < 3:
                continue
            fired = now - (bm.get("age") or 0)
            if bm.get("kind") == "laser":
                self.laser_fired[by] = max(self.laser_fired.get(by, -99.0), fired)
            if self.beam_threat is None or fired >= self.beam_threat[0]:
                self.beam_threat = (fired, path[0])
        for m in obs.get("mechs") or []:
            mid, mpos = m.get("id"), m.get("pos")
            if mid is None or not mpos:
                continue
            vel = m.get("vel") or (0.0, 0.0, 0.0)
            prev = self.tracks.get(mid)
            if prev and 0 < now - prev[0] <= 0.21:
                vel = [0.85 * v + 0.15 * (p - q) / (now - prev[0]) for v, p, q in zip(vel, mpos, prev[1])]
            self.tracks[mid] = (now, mpos, vel)
            if m.get("kind") == "mech":
                self.seen[mid] = (now, mpos, m)
        aim_yaw = (me.get("aim") or [0.0])[0] or 0.0
        for store, listed in ((self.pickups, obs.get("pickups") or []), (self.cubes, obs.get("cubes") or [])):
            ids = {p.get("id") for p in listed}
            for p in listed:
                if p.get("id") is not None and p.get("pos"):
                    store[p["id"]] = p
            for pid, p in list(store.items()):   # forget loot whose spot we can see but isn't listed
                if pid in ids:
                    continue
                dx, dy = p["pos"][0] - pos[0], p["pos"][1] - pos[1]
                d, eye = math.hypot(dx, dy), (pos[0], pos[1], pos[2] + 8)
                if d <= 35 or (d <= 120 and _angdiff(math.atan2(dy, dx), aim_yaw) < math.radians(50)
                               and not self.world.blocked(eye, (p["pos"][0], p["pos"][1], p["pos"][2] + 1))):
                    del store[pid]

    # ------------------------------------------------------------------ helpers
    def _scale(self, m):
        return 1 + self.size_per_cube * (m.get("cubes") or 0)

    def _muzzle_pos(self, me):
        st = me.get("stats") or {}
        return (me["pos"][0], me["pos"][1], me["pos"][2] + st.get("muzzle_height", self.muzzle * self._scale(me)))

    def _center(self, m):
        hh = self.npc_hh if m.get("kind") == "npc" else 0.5 * self.height * self._scale(m)
        return (m["pos"][0], m["pos"][1], m["pos"][2] + hh)

    def _los_blocked(self, me, m):
        key = m.get("id")
        if key not in self._los:
            self._los[key] = self.world.blocked(self._muzzle_pos(me), self._center(m))
        return self._los[key]

    def _lead(self, me, m, delay, speed=None):
        vel = self.tracks.get(m.get("id"), (0, 0, m.get("vel") or (0, 0, 0)))[2]
        own = me.get("vel") or (0, 0, 0)
        mz = self._muzzle_pos(me)
        c = self._center(m)
        dx, dy, dz = (c[k] - mz[k] + (vel[k] - own[k]) * delay for k in range(3))
        if speed:
            off = self.radius * self._scale(me) + 0.5
            a = speed * speed - (vel[0] ** 2 + vel[1] ** 2 + vel[2] ** 2)
            b = off * speed - (dx * vel[0] + dy * vel[1] + dz * vel[2])
            cc = dx * dx + dy * dy + dz * dz - off * off
            if cc > 0 and a > 0:
                fl = cc / (math.sqrt(b * b + a * cc) + b)
                dx, dy, dz = dx + vel[0] * fl, dy + vel[1] * fl, dz + vel[2] * fl
        return [math.atan2(dy, dx), math.atan2(dz, math.hypot(dx, dy))], math.hypot(dx, dy, dz)

    def _on_body(self, actual, aim, dist, m, spread=None):
        if not actual or None in actual or dist <= 1e-6:
            return False
        s = self._scale(m)
        r, hh = (self.npc_r, self.npc_hh) if m.get("kind") == "npc" else (self.radius * s, 0.5 * self.height * s)
        width = math.atan2(r, dist)
        height = math.atan2(hh * math.cos(aim[1]) + r * abs(math.sin(aim[1])), dist)
        yaw, pitch = _angdiff(actual[0], aim[0]) * math.cos(aim[1]), abs(actual[1] - aim[1])
        if spread is None:   # laser: tight gate, widened (never past the body) after 0.8 s at full charge
            gate = min(math.radians(4), 0.8 * width)
            if self.laser_full_since is not None and self.now - self.laser_full_since >= 0.8:
                return yaw <= min(2 * gate, width) and pitch <= height
            return yaw <= gate and pitch <= 0.8 * height
        gate = min(width, math.radians(12), max(math.radians(0.1), width - 0.25 * math.radians(spread)))
        return math.hypot(yaw, pitch * width / max(height, 1e-6)) <= gate

    def _zone_at(self, z, dt):
        """Live circle dt seconds from now (center/radius move linearly to next during the shrink)."""
        c, r, nc, nr = z["center"], z["radius"], z["next_center"], z["next_radius"]
        start, end = z.get("shrink_start", 0), z.get("shrink_end", 0)
        t = self.now + dt
        if t <= start or end <= start:
            return c, r
        f = (t - start) / (end - start) if self.now < start else min(1.0, dt / max(end - self.now, 1e-3))
        f = min(1.0, f)
        return (c[0] + (nc[0] - c[0]) * f, c[1] + (nc[1] - c[1]) * f), r + (nr - r) * f

    # ------------------------------------------------------------------ situation
    def _situation(self, obs, me, weapons, now):
        pos, xy = me["pos"], me["pos"][:2]
        hp_frac = me["hp"] / max(me.get("max_hp") or 1, 1)
        kinds = [w.get("kind") if w else None for w in weapons]
        ctx = dict(has_laser="laser" in kinds, has_light="lightning" in kinds, hp=hp_frac, charging=False)
        gun = next((w for w in weapons if w and w.get("kind") == "gun"), None)
        laser = next((w for w in weapons if w and w.get("kind") == "laser"), None)
        gun_range = ((gun or {}).get("stats") or {}).get("range", self.gun_cfg.get("range", 230))
        reach = ((laser or {}).get("stats") or {}).get("range", 280) if laser else gun_range
        ctx["gun_range"] = gun_range
        attackers = {a: h for a, h in self.hits.items() if 0 <= a < 16 and now - h[0] <= HIT_RECENT}
        mechs, best, best_s, visible = [], None, -math.inf, set()
        healing_prev = self.healing
        for m in obs.get("mechs") or []:
            mid = m.get("id")
            if m.get("kind") != "mech" or not m.get("pos") or mid in self.killed or mid == me.get("id"):
                continue
            visible.add(mid)
            ux, uy, d = _unit(m["pos"][0] - xy[0], m["pos"][1] - xy[1])
            aim = m.get("aim") or [None]
            cone = math.atan2(self.radius + 1.5, max(d, 1.0)) + 0.03
            aiming = aim[0] is not None and _angdiff(aim[0], math.atan2(-uy, -ux)) < cone
            info = dict(m=m, id=mid, d=d, u=(ux, uy), aiming=aiming, charging=bool(m.get("charging")) and aiming,
                        laser="laser" in (m.get("weapons") or []), light="lightning" in (m.get("weapons") or []),
                        cd=max(0.0, self.laser_fired.get(mid, -99.0) + self.laser_cd - now),
                        hit_age=now - self.hits.get(mid, (-99.0,))[0], blocked=self._los_blocked(me, m))
            mechs.append(info)
            hp, mhp = m.get("hp"), m.get("max_hp") or 1400
            wounded = hp is not None and hp <= (0.6 if self.is_finals else 0.5) * mhp
            engaged = info["hit_age"] <= 8 or now - self.dealt.get(mid, -99.0) <= 5
            if not (engaged or d <= 60 or info["charging"] or (aiming and d <= 150)
                    or (wounded and d <= reach and now < LATE_T)):
                continue
            if healing_prev and not (info["hit_age"] <= HIT_RECENT or d <= 60 or info["charging"]):
                continue   # while healing only shoot back (dealing damage resets our regen timer)
            s = (60 + 20 * (1 - info["hit_age"] / HIT_RECENT)) if info["hit_age"] <= HIT_RECENT else (20 if engaged else 0)
            s += 35 * info["charging"] + 10 * aiming - 0.12 * d + 15 * (mid == self.target_id)
            if hp is not None:
                s += 30 * (1 - hp / mhp) + (25 if hp <= 250 else 0)
            if ctx["has_laser"] and "mortar" in (m.get("weapons") or []):
                s += 10
            if info["blocked"]:
                s -= 40
            if d > max(reach, gun_range) + 20 and info["hit_age"] > HIT_RECENT:
                continue
            if s > best_s:
                best, best_s = info, s
        blind = None   # most recent attacker we can't see: last track, else the damage bearing
        for aid, (t, br, wpn) in sorted(attackers.items(), key=lambda kv: -kv[1][0]):
            if aid in visible or br is None:
                continue
            tr = self.tracks.get(aid)
            if tr and now - tr[0] <= 6.0:
                age = min(now - tr[0], 2.0)
                est = (tr[1][0] + tr[2][0] * age, tr[1][1] + tr[2][1] * age, tr[1][2] + 0.5 * self.height)
            else:
                rng = 30.0 if wpn == "lightning" else 120.0
                est = (xy[0] + rng * math.cos(br), xy[1] + rng * math.sin(br), pos[2] + 4.5)
            blind = dict(id=aid, est=est, age=now - t, score=50 + 20 * (1 - (now - t) / HIT_RECENT))
            break
        if blind and best is not None and best_s >= blind["score"]:
            blind = None
        target = None if blind else best
        self.target_id = target["id"] if target else None
        n_active = len(attackers) + sum(1 for i in mechs if i["aiming"] and i["d"] <= gun_range and i["id"] not in attackers)
        # Healing: below 50% (65% in finals) unless we are finishing a weaker target in a 1v1.
        thp = (target["m"].get("hp") if target else None)
        finishing = target is not None and thp is not None and thp < me["hp"] and (
            thp <= 0.3 * (target["m"].get("max_hp") or 1400) or n_active <= 1)
        enter = 0.65 if self.is_finals else 0.5
        self.healing = me.get("in_zone", True) and not finishing and hp_frac < (HEAL_EXIT if self.healing else enter)
        ctx.update(mechs=mechs, target=target, blind=blind, attackers=attackers, n_active=n_active,
                   finishing=finishing, healing=self.healing, roof=self.world.roof_at(pos),
                   hit_recent=any(now - h[0] <= 1.5 for h in self.hits.values()))
        return ctx

    # ------------------------------------------------------------------ weapons and aim
    def _engage(self, me, weapons, info, act, ctx):
        m = info["m"]
        actual = me.get("aim")
        dist = math.dist(me["pos"], m["pos"])
        blocked = self._los_blocked(me, m)
        mz, c = self._muzzle_pos(me), self._center(m)
        flat = max(math.hypot(c[0] - mz[0], c[1] - mz[1]), 1e-6)
        direct = [math.atan2(c[1] - mz[1], c[0] - mz[0]), math.atan2(c[2] - mz[2], flat)]
        aim, use_direct = direct, False
        gun_ok = False
        for i, w in enumerate(weapons):
            if not w:
                continue
            st, kind = w.get("stats") or {}, w.get("kind")
            if kind == "gun":
                delay = 0.1 if (w.get("cooldown") or 0) > 0.05 else 0.05
                aim, rng = self._lead(me, m, delay, st.get("speed", self.gun_cfg.get("speed", 252)))
                gun_ok = self._gun_ready(w) and rng <= st.get("range", 230)
                act["fire"][i] = (not blocked and rng - 3 <= st.get("range", 230)
                                  and self._on_body(actual, aim, rng, m, st.get("spread_deg", 0.6)))
                if blocked and (w.get("reload") or 0) <= 0 and w.get("ammo") is not None and 0 < w["ammo"] <= 6:
                    act["reload"] = True
            elif kind == "laser":
                charge, full = w.get("charge") or 0, 0.93 * st.get("charge", self.laser_cfg.get("charge", 0.75))
                travel = ctx["healing"] and self.heal_spot is not None and math.dist(me["pos"][:2], self.heal_spot) > 8
                if self.now < self.short_until or dist > st.get("range", 280):
                    continue
                if charge <= 0 and ((w.get("cooldown") or 0) > 0 or blocked or travel or m.get("kind") != "mech"):
                    continue
                if charge < full:
                    self.laser_full_since = None
                elif self.laser_full_since is None:
                    self.laser_full_since = self.now
                if charge >= full - 0.1 or not gun_ok:
                    use_direct = True
                    direct, _ = self._lead(me, m, 0.1)
                lead, ldist = self._lead(me, m, 0.05)
                ready = charge >= full and not blocked and self._on_body(actual, lead, ldist, m)
                stale = blocked and self.laser_full_since is not None and self.now - self.laser_full_since >= 1.6
                act["fire"][i] = not (ready or stale)
                ctx["charging"] = act["fire"][i]
            elif kind == "lightning":
                st_r = st.get("range", self.light_cfg.get("range", 45))
                if not blocked and dist <= 0.9 * st_r and (me.get("energy") or 0) >= 10:
                    use_direct = True
                    act["fire"][i] = bool(actual) and actual[0] is not None and _angdiff(direct[0], actual[0]) <= \
                        math.radians(0.4 * st.get("cone_deg", 30))
        act["aim"] = direct if use_direct else aim

    @staticmethod
    def _gun_ready(w):
        return bool(w) and (w.get("reload") or 0) <= 0 and (w.get("ammo") is None or w["ammo"] > 0)

    def _hold_laser(self, weapons, act, ctx, keep):
        """No target in view: a charging laser keeps its charge while an unseen shooter may step out
        (the server fires it on its own after hold_s); otherwise let it go rather than crawl at half speed."""
        for i, w in enumerate(weapons):
            if w and w.get("kind") == "laser" and (w.get("charge") or 0) > 0:
                act["fire"][i] = keep
                ctx["charging"] = keep

    def _fire(self, obs, me, weapons, ctx, act):
        now, pos = self.now, me["pos"]
        if ctx["target"]:
            self._engage(me, weapons, ctx["target"], act, ctx)
            return f"fight {ctx['target']['id']}"
        gun_i = next((i for i, w in enumerate(weapons) if w and w.get("kind") == "gun"), None)
        gun = weapons[gun_i] if gun_i is not None else None
        gun_ready = self._gun_ready(gun)
        b = ctx["blind"]
        if b:   # unseen shooter: turn to it (that usually reveals it) and fire blind if no building is in the way
            mz = self._muzzle_pos(me)
            ex, ey, ez = b["est"]
            yaw = math.atan2(ey - mz[1], ex - mz[0])
            d = math.hypot(ex - mz[0], ey - mz[1])
            act["aim"] = [yaw, math.atan2(ez - mz[2], max(d, 1.0))]
            actual = me.get("aim") or [None]
            if gun_ready and actual[0] is not None and d <= ctx["gun_range"] and \
                    _angdiff(yaw, actual[0]) <= max(math.radians(1.5), math.atan2(3.0, d)) and \
                    not self.world.blocked(mz, (ex, ey, ez)):
                act["fire"][gun_i] = True
            self._hold_laser(weapons, act, ctx, True)
            return f"blind {b['id']}"
        self._hold_laser(weapons, act, ctx, False)
        quiet = not any(now - h[0] <= HIT_RECENT for a, h in self.hits.items() if 0 <= a < 16)
        if quiet and self._shoot_drone(obs, me, weapons, act, ctx):
            return "drone"
        near_mech = any(i["d"] <= 120 for i in ctx["mechs"])
        if self._gun_ready(gun) and gun.get("ammo") is not None and gun["ammo"] <= 6 and not ctx["hit_recent"]:
            act["reload"] = True   # reload in quiet moments
        if quiet and not near_mech and self._shoot_crate(obs, me, weapons, act):
            return "crate"
        act["aim"] = [self._face_yaw(ctx, pos, now), 0.0]
        return "face"

    def _face_yaw(self, ctx, pos, now):
        if self.dmg_bearing and now - self.dmg_bearing[0] <= 3.0:
            return self.dmg_bearing[1]
        if self.beam_threat and now - self.beam_threat[0] <= 3.0:
            o = self.beam_threat[1]
            return math.atan2(o[1] - pos[1], o[0] - pos[0])
        combat = [h for h in self.heard if h[3] in COMBAT_SOUNDS and now - h[0] <= 2.5]
        if combat:
            return max(combat, key=lambda h: (h[2] == "near", h[0]))[1]
        if ctx["mechs"]:
            m = min(ctx["mechs"], key=lambda i: i["d"])["m"]
            return math.atan2(m["pos"][1] - pos[1], m["pos"][0] - pos[0])
        steps = [h for h in self.heard if h[3] in ("step", "boost", "jet") and now - h[0] <= 2.0]
        if steps:
            return steps[-1][1]
        # Idle: sweep the open side when our back is to a wall, else a full circle.
        free = [a for a in (k * math.pi / 4 for k in range(8))
                if not self.world.solid(pos[0] + 12 * math.cos(a), pos[1] + 12 * math.sin(a), pos[2])]
        if 0 < len(free) < 8:
            return math.atan2(sum(map(math.sin, free)), sum(map(math.cos, free))) + 1.1 * math.sin(now * 0.9)
        return (now * 1.2) % math.tau

    def _shoot_drone(self, obs, me, weapons, act, ctx):
        x, y, z = me["pos"]
        zone, best = obs["zone"], None
        for m in obs.get("mechs") or []:
            if m.get("kind") != "npc" or not m.get("pos"):
                continue
            d = math.hypot(m["pos"][0] - x, m["pos"][1] - y)
            attacking = self.now - self.hits.get(m.get("id"), (-99.0,))[0] <= HIT_RECENT
            farm = self.now < LATE_T and (me.get("cubes") or 0) < DRONE_CUBE_CAP and d <= DRONE_RANGE
            if not (attacking or farm) or abs(m["pos"][2] - z) > 4 or self._los_blocked(me, m) \
                    or math.dist(m["pos"][:2], zone["next_center"]) > zone["next_radius"]:
                continue
            rank = (not attacking, d)
            if best is None or rank < best[0]:
                best = (rank, m)
        if best is None:
            return False
        self._engage(me, weapons, dict(m=best[1], id=best[1].get("id")), act, ctx)
        return True

    def _shoot_crate(self, obs, me, weapons, act):
        x, y, z = me["pos"]
        zone = obs["zone"]
        crates = [(math.hypot(c["pos"][0] - x, c["pos"][1] - y), c) for c in obs.get("crates") or [] if c.get("pos")]
        crates = [(d, c) for d, c in crates if d <= 40 and abs(c["pos"][2] - z) <= 3
                  and math.dist(c["pos"][:2], zone["next_center"]) <= zone["next_radius"]]
        if not crates:
            return False
        d, c = min(crates, key=lambda dc: dc[0])
        mz = self._muzzle_pos(me)
        yaw = math.atan2(c["pos"][1] - y, c["pos"][0] - x)
        act["aim"] = [yaw, math.atan2(c["pos"][2] + 1.2 - mz[2], max(d, 1.0))]
        actual = me.get("aim") or [None]
        gate = max(math.radians(0.5), min(math.radians(5), math.atan2(1.1, max(d, 1))))
        on = actual[0] is not None and _angdiff(yaw, actual[0]) <= gate
        for i, w in enumerate(weapons):
            if w and w.get("kind") == "gun":
                act["fire"][i] = on
        return True

    # ------------------------------------------------------------------ goals
    def _goals(self, obs, me, weapons, ctx, act):
        """Returns [(x, y, weight)], may set take/drop and a deliberate climb override."""
        now, zone, pos = self.now, obs["zone"], me["pos"]
        xy, speed = pos[:2], (me.get("stats") or {}).get("walk_speed", self.walk)
        nc, nr = zone["next_center"], zone["next_radius"]
        goals, label = [], "hold"
        margin = min(10.0, 0.25 * nr)
        need = math.dist(xy, nc) - (nr - margin)
        secs = max((zone.get("shrink_end") or now) - now, 1.0)
        urgency = max(0.0, min(1.5, (need / speed + 4.0) / secs)) if need > 0 else 0.0
        if not me.get("in_zone", True):
            urgency = 1.5
        ctx["urgency"] = urgency
        place = self._placement(me, zone, ctx)
        if not me.get("in_zone", True):   # outside: straight back in
            c = zone["center"]
            goals.append((c[0], c[1], 34.0))
            label = "zone"
        elif urgency > 0:   # into the next circle, to a building edge there rather than the open centre
            goals.append(((place or nc)[0], (place or nc)[1], 4 + 20 * urgency))
            label = "zone"
        n_zone = len(goals)
        damp = 0.3 if urgency > 0.6 else 1.0
        shot_at = any(now - h[0] <= HIT_RECENT for a, h in self.hits.items() if 0 <= a < 16)
        drop = self._drop_goal(obs, me, ctx)
        if drop is not None:
            holding = math.dist(xy, drop["pos"][:2]) <= drop.get("radius", 8) - 2
            goals.append((drop["pos"][0], drop["pos"][1], (20 if holding else 12) * damp))
            ctx["holding_drop"] = holding
            label = "drop"
        # Weapons: laser first, lightning into an empty slot, never a mortar.
        has_laser, slot_empty = ctx["has_laser"], len(weapons) < 2 or weapons[1] is None
        light_i = next((i for i, w in enumerate(weapons) if w and w.get("kind") == "lightning"), None)
        charging_self = any(w and w.get("kind") == "laser" and (w.get("charge") or 0) > 0 for w in weapons)
        if not has_laser and (slot_empty or light_i is not None):
            hunt = None
            for pid, p in self.pickups.items():
                kind = p.get("kind")
                if kind not in ("laser", "lightning") or (kind == "lightning" and not slot_empty):
                    continue
                d, dz = math.dist(xy, p["pos"][:2]), p["pos"][2] - pos[2]
                if d <= self.reach and abs(dz) <= 4 and not charging_self and \
                        (act.get("take") is None or kind == "laser"):
                    act["take"] = pid
                    if not slot_empty and kind == "laser":
                        act["drop"] = light_i
                if pid in self.unreachable or math.dist(p["pos"][:2], nc) > nr - 4:
                    continue
                if dz > 5 and not (kind == "laser" and dz <= 30 and (me.get("energy") or 0) >= max(60, dz / 0.6 + 10)
                                   and not any(i["d"] <= self.near for i in ctx["mechs"])):
                    continue
                cap = (250 if now < 90 else 130) if kind == "laser" else (250 if now < 90 else 0)
                if shot_at:
                    cap = min(cap, 40)
                if now < LATE_T and d <= cap and (hunt is None or (kind != "laser", d) < hunt[0]):
                    hunt = ((kind != "laser", d), pid, p, dz)
            if hunt is not None and not self._stalled(hunt[1], hunt[0][1]):
                _r, pid, p, dz = hunt
                goals.append((p["pos"][0], p["pos"][1], 12 * damp))
                label = "weapon"
                if dz > 3.5 and hunt[0][1] <= 12 and (me.get("energy") or 0) >= 15:
                    ctx["climb"] = (p["pos"][0], p["pos"][1])
        cube = None if ctx.get("holding_drop") else self._cube_goal(obs, me, ctx, drop is not None, shot_at)
        if cube is not None:
            goals.append((cube[0], cube[1], 10 * damp))
            label = "cube"
        # Fight: a range band per matchup. Aggressive 1v1s; no backpedal except out of lightning reach.
        tgt = ctx["target"]
        if tgt is not None and not ctx["healing"]:
            m, d = tgt["m"], tgt["d"]
            thp, mhp = m.get("hp") or 1400, me["hp"]
            lo, hi = 0.0, 110.0
            advantage = (thp <= 0.7 * mhp or (m.get("cubes") or 0) + 2 <= (me.get("cubes") or 0)
                         or (has_laser and not tgt["laser"] and not tgt["light"] and thp <= 0.95 * mhp)
                         or (tgt["laser"] and tgt["cd"] > 0.5 and d < 150))
            if tgt["laser"] and not has_laser and thp > 0.5 * mhp and now < 60:
                advantage = False
            alone = not any(i["id"] != tgt["id"] and i["d"] <= 80 for i in ctx["mechs"])
            if tgt["light"] and not ctx["has_light"]:
                lo, hi = 50.0, 90.0
            elif ctx["has_light"] and tgt["laser"] and ctx["n_active"] <= 1 and ctx["hp"] > 0.4:
                lo, hi = 0.0, 32.0
            elif advantage and alone and ctx["n_active"] <= 1 and now < LATE_T and math.dist(m["pos"][:2], nc) <= nr:
                hi = 50.0
            elif ctx["n_active"] >= 2 or now >= LATE_T:
                hi = max(d, 60.0)
            if self.is_finals and thp > 0.5 * (m.get("max_hp") or 1400):
                hi = max(hi, min(d, 150.0))
            if d > hi:
                goals.append((m["pos"][0], m["pos"][1], (9 if hi <= 50 else 6) * damp))
                label = "push" if hi <= 50 else "close"
            elif d < lo:
                ux, uy = tgt["u"]
                goals.append((xy[0] - 60 * ux, xy[1] - 60 * uy, 6 * damp))
                label = "space"
            else:
                label = "duel"
            # Third party: a near cover spot that blocks the other shooters while we keep shooting.
            if ctx["n_active"] >= 2:
                spot = self._near_cover(me, ctx, exclude=tgt["id"], max_d=35.0, zone=zone)
                if spot:
                    goals.append((spot[0], spot[1], 7 * damp))
                    label += "+cover"
        if ctx["healing"]:
            if ctx["roof"] is not None:
                self.heal_spot = ctx["roof"][1]
            else:
                self.heal_spot = self._near_cover(me, ctx, exclude=None, max_d=45.0, zone=zone)
            if self.heal_spot:
                goals.append((self.heal_spot[0], self.heal_spot[1], 12 * damp))
            label = "heal"
        else:
            self.heal_spot = None
        if (has_laser and (now >= LATE_T or self.is_finals) and urgency < 0.5 and not ctx["mechs"]
                and not shot_at and label in ("hold", "zone")):
            label = self._roof_goal(me, zone, goals, ctx) or label
        if place and not any(w >= 6 for _x, _y, w in goals[n_zone:]) and label in ("hold", "zone", "cube", "drop", "weapon"):
            goals.append((place[0], place[1], 6.0))
            if label == "hold":
                label = "place"
        return goals, label

    def _stalled(self, key, d):
        """True (and remembered) when walking to key made no 1 m progress for 6 s of pursuit."""
        best, since, last = self.progress.get(key, (math.inf, self.now, self.now))
        if self.now - last > 1.0 or d < best - 1:   # new or resumed pursuit, or progress
            best, since = d, self.now
        self.progress[key] = (best, since, self.now)
        if self.now - since > 6:
            self.unreachable.add(key)
            return True
        return False

    def _cube_goal(self, obs, me, ctx, pursuing_drop, shot_at):
        pos, zone, now = me["pos"], obs["zone"], self.now
        self.kill_spots = [(t, xy) for t, xy in self.kill_spots if now - t <= 25]
        reach = 15.0 if pursuing_drop else (40.0 if ctx["target"] else 60.0)
        best = None
        for cid, c in self.cubes.items():
            loc = c["pos"]
            d = math.dist(pos[:2], loc[:2])
            r = reach
            if not pursuing_drop and not shot_at and any(math.dist(loc[:2], k) <= 12 for _t, k in self.kill_spots):
                r = max(r, 200.0 if now < LATE_T else 80.0)
            if loc[2] - pos[2] <= 3.5 and d <= r and cid not in self.unreachable \
                    and math.dist(loc[:2], zone["next_center"]) <= zone["next_radius"] and (best is None or d < best[0]):
                best = (d, cid, loc)
        if best is None or self._stalled(best[1], best[0]):
            return None
        return best[2]

    def _drop_goal(self, obs, me, ctx):
        zone, now, xy = obs["zone"], self.now, me["pos"][:2]
        max_d = 150.0 if ctx["hp"] >= 0.75 else 250.0
        best = None
        for drop in obs.get("drops") or []:
            did, dxy = drop.get("id"), (drop.get("pos") or [0, 0])[:2]
            if now < self.drop_retry.get(did, -99.0):
                continue
            d = math.dist(xy, dxy)
            active, in_ring = did == self.drop_id, d <= drop.get("radius", 8) - 2
            if active and in_ring:
                return drop
            if any(i["d"] < 400 and math.dist(i["m"]["pos"][:2], dxy) <= drop.get("radius", 8) + 12 for i in ctx["mechs"]):
                first = self.drop_contest.setdefault(did, now)
                if now - first >= 3.0 or active:
                    self.drop_retry[did] = now + (60.0 if now - first >= 3.0 else 15.0)
                continue
            self.drop_contest.pop(did, None)
            if ctx["hp"] < 0.35 or (ctx["healing"] and not active) or not me.get("in_zone", True) or d > max_d \
                    or math.dist(dxy, zone["next_center"]) > zone["next_radius"] - 4:
                continue
            if not active and (drop.get("lands_in") or 0) > d / self.walk + 3:
                continue
            if best is None or d < best[0]:
                best = (d, drop)
        self.drop_id = best[1].get("id") if best else None
        return best[1] if best else None

    def _near_cover(self, me, ctx, exclude, max_d, zone):
        """Closest building-edge spot within max_d whose building hides us from the main other threat."""
        threat = None
        others = [i for i in ctx["mechs"]
                  if i["id"] != exclude and (i["hit_age"] <= HIT_RECENT or i["aiming"] or i["d"] < 120)]
        if others:
            threat = min(others, key=lambda i: (i["hit_age"] > HIT_RECENT, i["d"]))["m"]["pos"]
        elif ctx["blind"] and ctx["blind"]["id"] != exclude:
            threat = ctx["blind"]["est"]
        elif exclude is None and ctx["target"]:
            threat = ctx["target"]["m"]["pos"]
        elif exclude is None and self.dmg_bearing and self.now - self.dmg_bearing[0] <= 10:
            b = self.dmg_bearing[1]
            threat = (me["pos"][0] + 100 * math.cos(b), me["pos"][1] + 100 * math.sin(b), me["pos"][2])
        if threat is None:
            return None
        xy, z = me["pos"][:2], me["pos"][2]
        near = sorted((math.hypot(sx - xy[0], sy - xy[1]), sx, sy) for sx, sy in self.world.spots
                      if abs(sx - xy[0]) <= max_d and abs(sy - xy[1]) <= max_d)
        for d, sx, sy in near[:24]:
            if d <= max_d and math.dist((sx, sy), zone["next_center"]) <= zone["next_radius"] - 3 \
                    and self.world.blocked((threat[0], threat[1], threat[2] + 8), (sx, sy, z + 4.5)):
                return (sx, sy)
        return None

    def _placement(self, me, zone, ctx):
        """A building corner/edge inside the next circle: near us, away from known mechs, not the open centre."""
        fresh = self.now - self.place_t < 3.0
        if fresh and (self.place is None or math.dist(self.place, zone["next_center"]) <= zone["next_radius"] - 6):
            return self.place
        nc, nr, xy = zone["next_center"], zone["next_radius"], me["pos"][:2]
        lim = nr - min(12.0, 0.3 * nr)
        best, best_s = None, math.inf
        for sx, sy in self.world.spots:
            dc = math.hypot(sx - nc[0], sy - nc[1])
            if dc > lim:
                continue
            d = math.hypot(sx - xy[0], sy - xy[1])
            if d > 300:
                continue
            s = d + 0.25 * dc + sum(max(0.0, 120 - math.dist((sx, sy), i["m"]["pos"][:2])) * 1.5 for i in ctx["mechs"])
            if self.place and math.dist((sx, sy), self.place) < 3:
                s -= 15   # hysteresis
            if s < best_s:
                best, best_s = (sx, sy), s
        self.place, self.place_t = best, self.now
        return best

    def _roof_goal(self, me, zone, goals, ctx):
        """With a laser late on: claim a rooftop inside the next circle when nobody is around."""
        pos, xy = me["pos"], me["pos"][:2]
        nc, nr = zone["next_center"], zone["next_radius"]
        if ctx["roof"] is not None and math.dist(ctx["roof"][1], nc) <= nr - 4:
            goals.append((ctx["roof"][1][0], ctx["roof"][1][1], 6.0))
            self.roof_goal = None
            return "roof"
        g = self.roof_goal
        if g is not None and (math.dist(g[2], nc) > nr - g[4] - 4 or self.now - g[5] > 25):
            self.unreachable_roofs.add(g[0])
            g = self.roof_goal = None
        if g is None:
            best = None
            for idx, c, rad, _ring, _holes, top, climbs in self.world.roofs:
                if idx in self.unreachable_roofs or math.dist(c, nc) > nr - rad - 4 or top - pos[2] > 45:
                    continue
                if (me.get("energy") or 0) < max(45.0, (top - pos[2]) / 0.6 + 10):
                    continue
                cl = min(climbs, key=lambda q: math.dist(xy, q))
                d = math.dist(xy, cl)
                if d <= 140 and (best is None or d + 0.5 * math.dist(c, nc) < best[0]):
                    best = (d + 0.5 * math.dist(c, nc), [idx, cl, c, top, rad, self.now])
            g = self.roof_goal = best[1] if best else None
        if g is None:
            return None
        if math.dist(xy, g[1]) <= 6 or pos[2] >= g[3] - 0.5:
            ctx["climb"] = g[2]
        else:
            goals.append((g[1][0], g[1][1], 8.0))
        return "roof-walk"

    def _nav(self, me, kind, gx, gy):
        """Next waypoint toward a goal: the goal itself when the walk there is clear, else along an A* path."""
        x, y, z = me["pos"]
        if math.hypot(gx - x, gy - y) < 6 or not self.world.walk_blocked(x, y, gx, gy, z):
            return gx, gy
        p = self.paths.get(kind)
        if self.now < self.stuck_until and p is not None and p[0] < self.stuck_until - 1.5:
            p = None   # we got stuck following it: plan again
        if p is None or self.now - p[0] > 1.5 or math.hypot(p[1][0] - gx, p[1][1] - gy) > 10:
            if self._plans <= 0:   # one A* per decision keeps us well inside the time budget
                return (gx, gy) if p is None else p[2][-1]
            self._plans -= 1
            p = self.paths[kind] = (self.now, (gx, gy), self.world.path(x, y, gx, gy))
        pts = p[2]
        k0 = min(range(len(pts)), key=lambda k: (pts[k][0] - x) ** 2 + (pts[k][1] - y) ** 2)
        for k in range(min(len(pts) - 1, k0 + 8), k0, -1):
            if not self.world.walk_blocked(x, y, pts[k][0], pts[k][1], z):
                return pts[k]
        return pts[min(k0 + 1, len(pts) - 1)]

    # ------------------------------------------------------------------ movement evaluator
    def _evaluate(self, obs, me, ctx, goals):
        now, pos, zone, W = self.now, me["pos"], obs["zone"], self.world
        x, y, z = pos
        v0 = me.get("vel") or [0.0, 0.0, 0.0]
        acc = self.accel if me.get("grounded", True) else self.air_accel
        speed = (me.get("stats") or {}).get("walk_speed", self.walk) * (0.5 if ctx["charging"] else 1.0)
        my_r = self.radius * self._scale(me) + 0.9
        if ctx["roof"] is None:   # walk around buildings instead of into them
            self.paths = {k: v for k, v in self.paths.items() if now - v[0] <= 3.0}
            goals = [self._nav(me, (round(gx / 25), round(gy / 25)), gx, gy) + (w,) for gx, gy, w in goals]
        body_z = z + 0.5 * self.height * self._scale(me)
        # Incoming fire: bullets (closest approach), shells (landing point), laser lines (charging mechs).
        bullets, shells, lines = [], [], []
        for p in obs.get("projectiles") or []:
            bp, bv = p.get("pos"), p.get("vel")
            if not bp or not bv:
                continue
            if p.get("kind") == "mortar":
                disc = bv[2] ** 2 + 2 * self.mortar_g * (bp[2] - z)
                if disc >= 0:
                    t = (bv[2] + math.sqrt(disc)) / self.mortar_g
                    if 0.05 <= t <= 2.5:
                        shells.append((t, bp[0] + bv[0] * t, bp[1] + bv[1] * t))
                continue
            rv = (bv[0] - v0[0], bv[1] - v0[1], bv[2] - v0[2])
            rv2 = rv[0] ** 2 + rv[1] ** 2 + rv[2] ** 2
            if rv2 < 1:
                continue
            t = ((x - bp[0]) * rv[0] + (y - bp[1]) * rv[1] + (body_z - bp[2]) * rv[2]) / rv2
            if 0.12 <= t <= 1.2 and abs(bp[2] + bv[2] * t - body_z) <= 0.5 * self.height + 1:
                bullets.append((t, bp[0] + bv[0] * t, bp[1] + bv[1] * t, 10.0 if p.get("kind") == "gun" else 5.0))
        lateral, avoid, covers = [], [], []
        tgt = ctx["target"]
        for i in ctx["mechs"]:
            m = i["m"]
            if i["charging"] and not i["blocked"]:
                a = m["aim"][0]
                lines.append((m["pos"][0], m["pos"][1], math.cos(a), math.sin(a)))
            w = 0.0
            if i["laser"] and i["d"] <= 280 and not i["blocked"] and i["cd"] < 0.3:
                w = 5.0 if i["charging"] else 3.0
            elif i["hit_age"] <= HIT_RECENT and i["d"] <= ctx["gun_range"]:
                w = 1.5
            if w:
                lateral.append((i["u"][0], i["u"][1], w))
            if tgt is None or i["id"] != tgt["id"]:
                if i["d"] <= 170:
                    avoid.append((i["u"][0], i["u"][1], 3.0 * (1 - i["d"] / 170)))
                danger = 2.0 if i["hit_age"] <= HIT_RECENT else (1.5 if i["aiming"] else (1.0 if i["d"] <= 150 else 0.0))
                if danger:
                    covers.append((danger, (m["pos"][0], m["pos"][1], m["pos"][2] + 8), 4.0))
        covers = sorted(covers, key=lambda c: -c[0])[:2]
        if ctx["blind"]:
            bx, by, bz = ctx["blind"]["est"]
            covers.append((2.0, (bx, by, bz + 3.5), 3.0))
            ux, uy, _ = _unit(bx - x, by - y)
            lateral.append((ux, uy, 1.5))
        if tgt is not None:
            m = tgt["m"]
            gun = next((w for w in me.get("weapons") or [] if w and w.get("kind") == "gun"), {}) or {}
            hide = ctx["healing"] or ((gun.get("reload") or 0) > 0.6 and not any(
                w and w.get("kind") == "laser" and (w.get("cooldown") or 0) <= 0.5 for w in me.get("weapons") or []))
            covers.append((1.0, (m["pos"][0], m["pos"][1], m["pos"][2] + 8), 5.0 if hide else -3.0))
        tb = math.atan2(tgt["u"][1], tgt["u"][0]) if tgt else None
        for t, br, dist, kind in self.heard:
            if now - t <= 3.0 and (tb is None or _angdiff(br, tb) > 0.3):
                avoid.append((math.cos(br), math.sin(br), 1.5 if dist == "near" else 0.8))
        c15, r15 = self._zone_at(zone, 1.5)
        jink = _strafe_sign(now)
        open_w = 2.0 if (now < LATE_T and tgt is None and not ctx["healing"] and ctx.get("urgency", 0) < 0.6) else 0.0
        roof = ctx["roof"]
        keep_roof = roof is not None and math.dist(roof[1], zone["next_center"]) <= zone["next_radius"] - 4
        drop_c = ctx.get("holding_drop") and next((d for d in obs.get("drops") or [] if d.get("id") == self.drop_id), None)
        under_fire = ctx["hit_recent"] or bool(bullets)
        scores, p8s = [], []
        for dx, dy in DIRS:
            vx, vy = dx * speed, dy * speed
            ex, ey = vx - v0[0], vy - v0[1]
            tau = math.hypot(ex, ey) / acc
            ax, ay = (ex / tau, ey / tau) if tau > 1e-6 else (0.0, 0.0)

            def P(t):
                if t <= tau:
                    return x + v0[0] * t + 0.5 * ax * t * t, y + v0[1] * t + 0.5 * ay * t * t
                return (x + v0[0] * tau + 0.5 * ax * tau * tau + vx * (t - tau),
                        y + v0[1] * tau + 0.5 * ay * tau * tau + vy * (t - tau))
            p1 = P(1.0)
            s = 0.0
            for gx, gy, w in goals:
                d0 = math.hypot(gx - x, gy - y)
                if d0 > 0.5:
                    s += w * (d0 - math.hypot(gx - p1[0], gy - p1[1])) / max(speed, 1.0)
            moving = dx or dy
            if moving:
                if W.solid(x + 3.5 * dx, y + 3.5 * dy, z) or W.solid(x + 7 * dx, y + 7 * dy, z):
                    s -= 40
                if keep_roof and not _in_prism(x + 4 * dx, y + 4 * dy, roof[3], roof[4]):
                    s -= 40
                if now < self.stuck_until and dx * self.stuck_dir[0] + dy * self.stuck_dir[1] > 0.5:
                    s -= 25
                if drop_c and math.dist((x + 6 * dx, y + 6 * dy), drop_c["pos"][:2]) > drop_c.get("radius", 8) - 1.5:
                    s -= 30   # don't step out of a drop ring we are capturing
                s += 1.0 * (dx * self.prev_move[0] + dy * self.prev_move[1])
            else:
                s += -6.0 if under_fire else 1.0
            p15 = P(1.5)
            e = math.hypot(p15[0] - c15[0], p15[1] - c15[1]) - (r15 - 3)
            if e > 0:
                s -= 6 + 3 * e
            for t, bx, by, w in bullets:
                px, py = P(t)
                if math.hypot(px - bx, py - by) < my_r:
                    s -= w
            for t, ix, iy in shells:
                px, py = P(t)
                if math.hypot(px - ix, py - iy) < self.splash:
                    s -= 25
            for lx, ly, ux, uy in lines:
                for t in (0.3, 0.7):
                    px, py = P(t)
                    rx, ry = px - lx, py - ly
                    if rx * ux + ry * uy > 0 and abs(rx * uy - ry * ux) < my_r + 0.6:
                        s -= 15
            for ux, uy, w in lateral:
                cr = dx * uy - dy * ux
                s += w * abs(cr) + 0.5 * w * jink * cr
            for ux, uy, w in avoid:
                s -= w * (dx * ux + dy * uy)
            if open_w:
                s -= open_w * W.openness(p15[0], p15[1])
            scores.append(s)
            p8s.append(P(0.8))
        # Cover from known shooters (exposure to our target), one shooter at a time for every
        # direction alike, stopping early if this decision is running long.
        for _dg, eye, w in covers:
            if time.perf_counter() - self._t0 > 0.012:
                break
            for k, (px, py) in enumerate(p8s):
                if W.blocked(eye, (px, py, body_z)):
                    scores[k] += w
        best = DIRS[max(range(len(DIRS)), key=scores.__getitem__)]
        ctx["dodging"] = bool(bullets or shells or lines)
        return list(best)

    # ------------------------------------------------------------------ main
    def _act(self, obs):
        now, me = self.now, obs["self"]
        pos = me["pos"]
        self._los, self._plans, self._t0 = {}, 1, time.perf_counter()
        self._memory(obs, me, now)
        weapons = (list(me.get("weapons") or []) + [None, None])[:2]
        act = {"tick": obs["tick"], "fire": [False, False], "boost": False, "jump": False}
        choices = (obs.get("offer") or {}).get("choices") or []
        if choices:
            act["pick"] = min(range(len(choices)), key=lambda i: UPGRADE_RANK.get(choices[i].get("id"), 99))
        ctx = self._situation(obs, me, weapons, now)
        fire_state = self._fire(obs, me, weapons, ctx, act)
        goals, label = self._goals(obs, me, weapons, ctx, act)
        energy, grounded = me.get("energy") or 0, me.get("grounded", True)
        if ctx.get("climb") is not None:   # deliberate climb: straight at it, jump + jet
            ux, uy, d = _unit(ctx["climb"][0] - pos[0], ctx["climb"][1] - pos[1])
            act["move"] = [ux, uy] if d > 2.5 else [0.0, 0.0]
            act["jump"] = grounded and d > 2.5 and energy >= 15
            act["boost"] = energy >= 15 and d > 2.5 and (not grounded or act["jump"])
            label += " climb"
        else:
            act["move"] = self._evaluate(obs, me, ctx, goals)
            far_goal = any(w >= 6 and math.dist(pos[:2], (gx, gy)) > 50 for gx, gy, w in goals)
            act["boost"] = grounded and not ctx["charging"] and act["move"] != [0.0, 0.0] and (
                (ctx.get("urgency", 0) > 0.6 and energy >= 20)
                or (far_goal and energy >= 60 and not ctx["mechs"] and not ctx["target"])
                or (ctx.get("dodging") and energy >= 25 and ctx["hit_recent"]))
            # Hops: v39's 2 s cadence, plus irregular extra hops under gunfire. Never jet in the air.
            hop = obs["tick"] % 40 == 0
            gunfire = any(now - h[0] <= 1.0 and h[2] == "gun" for h in self.hits.values())
            if gunfire and not ctx.get("dodging") and self.world.openness(pos[0], pos[1]) > 0.2 and self.rng.random() < 0.25:
                hop = True   # irregular vertical dodge in the open
            act["jump"] = bool(grounded and hop and not ctx.get("holding_drop"))
            self._unstick(me, act)
        mf.draw.label(f"{label} {fire_state} hp{ctx['hp']:.0%} c{me.get('cubes', 0)}"
                      + (" heal" if ctx["healing"] else "") + (" chg" if ctx["charging"] else ""))
        return act

    def _unstick(self, me, act):
        now, (x, y) = self.now, me["pos"][:2]
        mv = act["move"]
        self.pos_hist = [p for p in self.pos_hist if now - p[0] <= 0.6] + [(now, x, y, mv[0], mv[1])]
        old = self.pos_hist[0]
        mx, my, mean = _unit(sum(p[3] for p in self.pos_hist), sum(p[4] for p in self.pos_hist))
        # Pushing one general way for 0.5 s (a dodge reversal cancels out) but not moving: avoid that way.
        if now - old[0] >= 0.45 and mean > 0.5 * len(self.pos_hist) and math.hypot(x - old[1], y - old[2]) < 1.2:
            self.stuck_dir, self.stuck_until = (mx, my), now + 1.5
            self.pos_hist = []
            act["jump"] = bool(me.get("grounded", True))


if __name__ == "__main__":
    mf.run(Bot)
