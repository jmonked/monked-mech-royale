"""v34: v33 (4.44) + switch-gated reload cover, early/no-laser push caution,
more crate cubes, early zone-run, FFA third-party targeting, and rich replay labels."""
import json
import math
import traceback
from pathlib import Path

import mechfight as mf


# --- v34 switches: set False to turn a change off ---
USE_RELOAD_COVER = True      # point 14: step behind cover while gun reloads and laser is busy
USE_EARLY_CAUTION = True     # point 13: in first 60 s, don't push a laser holder without a laser
USE_NO_LASER_CAUTION = True  # point 15: without a laser, don't push a laser holder unless <= 50% HP
USE_MORE_CUBES = True        # point 16: break crates when no mech is within 120 m (don't skip for 180 m mechs)
USE_ZONE_EARLY = True        # point 17: head straight into next circle before shrink runs out
USE_FFA_THIRD_PARTY = True   # point 11: in Finals FFA, prioritize mechs actively losing HP to other bots

USE_WALL_STEER = True        # v35: steer around nearby walls before stalling
USE_COVER_PEEK = True        # v35: step toward cover below 85% laser charge

THREAT_RECENT_S = 3.0  # an attacker counts as "shooting us now" for this long after a hit
THREAT_RANGE = 60.0    # ...and only while it is this close
CUBE_IDLE_RANGE = 60.0  # walk this far for a cube when nothing is targeted (40 m while fighting/hunting)
CRATE_RANGE = 40.0      # break crates this close (inside cube reach, so the cube gets collected)
DRONE_RANGE = 55.0      # farm NPC drones this close (2 cubes per 350 HP, no squad escalation)
DRONE_CUBE_CAP = 15     # farm drones up to the 15-cube upgrade threshold (plating snowball)
KILL_LOOT_RANGE = 200.0  # walk this far for the cubes our kill dropped (80 m after LATE_T)
KILL_LOOT_S = 25.0       # ...within this long after the kill
PUSH_RANGE = 230.0     # push a weaker, isolated target from this far...
PUSH_STOP = 35.0       # ...until this close
PUSH_MIN_HP = 0.6      # only while we have this much HP
PUSH_CLEAR = 80.0      # and no other mech is this close to us
LATE_T = 230.0         # from the 3rd zone shrink on: no more chasing, let the zone and the squad thin out
LASER_LEAD_S = 0.1     # the beam goes out about one decision after we command the aim
HEAL_FIGHTBACK_S = 2.0  # while healing, keep shooting an attacker that hit us this recently
DUEL_STRAFE_RAD = math.radians(35)  # diagonal angle during pushes/duels to dodge 252 m/s gun fire
ROOF_LASER_MAX_DZ = 30.0  # max vertical climb for a rooftop laser when unpressured
ROOF_CLAIM_MAX_H = 45.0   # max building height to claim as a rooftop fortress
ROOF_MIN_RADIUS = 8.0     # minimum roof radius so we can pull back from the edge safely
ROOF_WALK_TIMEOUT_S = 8.0  # give up walking to a roof if no 1 m progress in 8 s
SANDWICH_SPAN_RAD = math.radians(150)  # disengage outward if 2+ nearby threats wrap > 150 deg around us
SANDWICH_RANGE = 110.0
FINALS_DETECT_T = 110.0  # nobody dies to zone before 110 s; >= 2 non-our deaths before this proves FFA finals
MORTAR_GRAVITY = 22.0
DROP_HEALTHY_DIST = 150.0  # only chase drops within 150 m when >= 75% HP (250 m when hurt)
DROP_CONTEST_ABORT_S = 3.0  # abandon a drop if a rival hangs around it for >= 3 s
STEER_OFFSETS = (
    math.radians(30), -math.radians(30),
    math.radians(60), -math.radians(60),
    math.radians(90), -math.radians(90),
    math.radians(120), -math.radians(120),
)

UPGRADE_RANK = {name: rank for rank, name in enumerate((
    "plating", "laser_damage", "laser_charge", "armor", "gun_damage",
    "gun_rate", "gun_mag", "nanites", "lightning_efficiency", "lightning_range",
    "lightning_chain", "gyros", "servos", "gun_velocity", "sensors",
    "laser_pierce", "capacitor", "reactor", "jets", "mortar_reload",
    "mortar_splash", "mortar_velocity",
))}


def _stat(stats, key, default):
    value = stats.get(key)
    return default if value is None else value


def _point_in_ring(px, py, ring):
    inside = False
    ax, ay = ring[-1]
    for bx, by in ring:
        if (ay > py) != (by > py):
            x_int = ax + (py - ay) * (bx - ax) / (by - ay)
            if px < x_int:
                inside = not inside
        ax, ay = bx, by
    return inside


def _point_in_prism_2d(px, py, ring, holes):
    if not _point_in_ring(px, py, ring):
        return False
    for hole in holes:
        if _point_in_ring(px, py, hole):
            return False
    return True


def _ring_intervals(ax, ay, dx, dy, ring):
    """Return sorted [(t0, t1), ...] clamped to [0, 1] where segment a->b lies inside ring."""
    crossings = []
    px, py = ring[-1]
    side_a = dx * (py - ay) - dy * (px - ax)
    for qx, qy in ring:
        side_b = dx * (qy - ay) - dy * (qx - ax)
        if (side_a > 0) != (side_b > 0):
            t = ((px - ax) * (qy - py) - (py - ay) * (qx - px)) / (side_b - side_a)
            crossings.append(t)
        px, py, side_a = qx, qy, side_b
    crossings.sort()
    intervals = []
    for enter, leave in zip(crossings[::2], crossings[1::2]):
        t0 = max(enter, 0.0)
        t1 = min(leave, 1.0)
        if t1 - t0 > 1e-9:
            intervals.append((t0, t1))
    return intervals


def _subtract_intervals(base_ivs, cut_ivs):
    if not cut_ivs:
        return base_ivs
    out = base_ivs
    for c0, c1 in cut_ivs:
        nxt = []
        for a, b in out:
            if c1 <= a or c0 >= b:
                nxt.append((a, b))
            else:
                if a < c0 - 1e-9:
                    nxt.append((a, c0))
                if b > c1 + 1e-9:
                    nxt.append((c1, b))
        out = nxt
        if not out:
            break
    return out


def _crosses_prism_3d(a, b, ring, holes, base, top):
    """Exact 3D segment vs vertical prism with courtyard holes subtracted."""
    ax, ay, az = a
    bx, by, bz = b
    dx, dy, dz = bx - ax, by - ay, bz - az
    ivs = _ring_intervals(ax, ay, dx, dy, ring)
    if not ivs:
        return False
    if holes:
        for hole in holes:
            h_ivs = _ring_intervals(ax, ay, dx, dy, hole)
            if h_ivs:
                ivs = _subtract_intervals(ivs, h_ivs)
                if not ivs:
                    return False
    for t0, t1 in ivs:
        z0 = az + dz * t0
        z1 = az + dz * t1
        if max(z0, z1) > base and min(z0, z1) < top:
            return True
    return False


def _crosses_ring(start, end, ring):
    x, y = start
    return bool(_ring_intervals(x, y, end[0] - x, end[1] - y, ring))


def _load_prisms(hello):
    """Return (cover_buildings, los_buildings, roofs) with courtyard holes respected
    and climb points filtered to open ground outside every building."""
    with (Path(hello["map"]["dir"]) / "v2" / "world.json").open(encoding="utf-8") as source:
        prisms = json.load(source)["prisms"]
    cover_buildings = []
    los_buildings = []
    raw_roofs = []
    for idx, prism in enumerate(prisms):
        if prism["kind"] not in ("building", "stadium"):
            continue
        flat = prism["ring"]
        ring = list(zip(flat[::2], flat[1::2]))
        holes = [list(zip(h[::2], h[1::2])) for h in (prism.get("holes") or []) if len(h) >= 6]
        area2 = cx = cy = 0.0
        for (ax, ay), (bx, by) in zip(ring[-1:] + ring[:-1], ring):
            cross = ax * by - bx * ay
            area2 += cross
            cx += (ax + bx) * cross
            cy += (ay + by) * cross
        if abs(area2) > 1e-8:
            center = (cx / (3 * area2), cy / (3 * area2))
            radius = max(math.dist(p, center) for p in ring)
            base, top = prism["base"], prism["top"]
            height = top - base
            entry = (center, radius, ring, holes, base, top)
            los_buildings.append(entry)
            if height >= 9:
                cover_buildings.append(entry)
            if (9.0 <= height <= ROOF_CLAIM_MAX_H and radius >= ROOF_MIN_RADIUS
                    and _point_in_prism_2d(center[0], center[1], ring, holes)):
                raw_roofs.append((idx, center, radius, ring, holes, base, top))

    roofs = []
    for idx, center, radius, ring, holes, base, top in raw_roofs:
        valid_climbs = []
        for ux, uy in ((1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0),
                       (0.707, 0.707), (-0.707, 0.707), (0.707, -0.707), (-0.707, -0.707)):
            vx, vy = max(ring, key=lambda p: p[0] * ux + p[1] * uy)
            cx_pt, cy_pt = vx + 3.5 * ux, vy + 3.5 * uy
            blocked = False
            for b_center, b_rad, b_ring, b_holes, b_base, b_top in los_buildings:
                if b_top - b_base <= 1.2:
                    continue
                if math.dist((cx_pt, cy_pt), b_center) <= b_rad + 0.5:
                    if _point_in_prism_2d(cx_pt, cy_pt, b_ring, b_holes):
                        blocked = True
                        break
            if not blocked:
                valid_climbs.append((cx_pt, cy_pt))
        if valid_climbs:
            roofs.append((idx, center, radius, ring, holes, base, top, valid_climbs))
    return cover_buildings, los_buildings, roofs


def _point_to_segment_dist_sq(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    seg_sq = dx * dx + dy * dy
    if seg_sq <= 1e-12:
        return (px - ax) ** 2 + (py - ay) ** 2
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / seg_sq))
    qx, qy = ax + t * dx, ay + t * dy
    return (px - qx) ** 2 + (py - qy) ** 2


def _strafe_sign(now):
    return 1.0 if math.sin(now * 3.1) + 0.55 * math.sin(now * 5.3) >= 0.0 else -1.0


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
        self.spread = _stat(gun, "spread_deg", 0.6)
        self.gun_range = _stat(gun, "range", 230)
        self.laser = (config.get("weapons") or {}).get("laser") or {}
        self.lightning = (config.get("weapons") or {}).get("lightning") or {}
        mortar = (config.get("weapons") or {}).get("mortar") or {}
        self.mortar_gravity = _stat(mortar, "gravity", MORTAR_GRAVITY)
        self.mortar_splash = _stat(mortar, "splash_radius", 7.0) + 1.2
        self.muzzle_height = _stat(config.get("mech") or {}, "muzzle_height", 7)
        self.mech_radius = _stat(config.get("mech") or {}, "radius", 2.5)
        crates = config.get("crates") or {}
        self.crate_radius = _stat(crates, "radius", 1.4)
        self.crate_height = _stat(crates, "height", 2.4)
        npc = config.get("npc") or {}
        self.npc_radius = _stat(npc, "radius", 1.8)
        self.npc_half_height = 0.5 * _stat(npc, "height", 3.5)
        self.half_height = 0.5 * _stat(config.get("mech") or {}, "height", 9)
        self.tracks = {}
        self.hp_seen = {}             # point 11: mech id -> (time, hp)
        self.hp_drop_t = {}           # point 11: mech id -> last time hp dropped without us hitting it
        self.size_per_cube = _stat(cubes, "size_per_cube", 0.05)
        self.laser_released = False
        self.laser_target = None
        self.laser_full_since = None
        self.walk_speed = _stat(config.get("mech") or {}, "walk_speed", 11.7)
        self.step_speed = _stat(config.get("sound") or {}, "step_speed", 5.0)
        self.drop_id = None
        self.drop_retry_at = {}
        self.drop_contested_since = {}
        self.last_hits = {}
        self.recent_dealt = {}
        self.target_id = None
        self.killed = set()
        self.prev_alive = 16
        self.non_our_deaths = 0
        self.last_damage_bearing = None
        self.last_mech_bearing = None
        self.last_sound = None
        self.last_beam_threat = None
        self.pickups = {}
        self.cubes = {}
        self.cube_progress = (None, math.inf, 0.0)
        self.unreachable = set()
        self.unreachable_roofs = set()
        self.roof_goal = None
        self.hunt_progress = {}
        self.previous_move = [0.0, 0.0]
        self.healing = False
        self.kill_spots = []
        self.mech_seen = {}
        self.cover_spot = None
        self.cover_threat = None
        self.cover_time = -math.inf
        self.pos_history = []
        self.unstick_until = -math.inf
        self.unstick_started = -math.inf
        self.unstick_sign = 1.0
        self.unstick_streak = 0
        self.is_finals = False
        self.finals_t = None          # point 8: timestamp when Finals FFA switch tripped
        self._now = 0.0
        self._los_cache = {}
        try:
            self.buildings, self.los_buildings, self.roofs = _load_prisms(hello)
        except Exception:
            self.buildings, self.los_buildings, self.roofs = [], [], []

    def _muzzle_z(self, me):
        own_scale = self._scale(me)
        return me["pos"][2] + _stat(me.get("stats") or {}, "muzzle_height", self.muzzle_height * own_scale)

    def _building_blocked(self, a, b):
        ax, ay, az = a
        bx, by, bz = b
        lo_z = min(az, bz)
        hi_z = max(az, bz)
        for center, radius, ring, holes, base, top in self.los_buildings:
            if top <= lo_z or base >= hi_z:
                continue
            if _point_to_segment_dist_sq(center[0], center[1], ax, ay, bx, by) > radius * radius:
                continue
            if _crosses_prism_3d(a, b, ring, holes, base, top):
                return True
        return False

    def _target_blocked(self, me, target):
        tid = target.get("id")
        if tid is not None and tid in self._los_cache:
            return self._los_cache[tid]
        muzzle_pos = (me["pos"][0], me["pos"][1], self._muzzle_z(me))
        target_half = self.npc_half_height if target.get("kind") == "npc" else self.half_height * self._scale(target)
        target_pos = (target["pos"][0], target["pos"][1], target["pos"][2] + target_half)
        res = self._building_blocked(muzzle_pos, target_pos)
        if tid is not None:
            self._los_cache[tid] = res
        return res

    def _point_blocked_2d(self, px, py, z):
        for center, radius, ring, holes, base, top in self.los_buildings:
            if top <= z + 1.2 or base > z + 8.0:
                continue
            if math.dist((px, py), center) <= radius + 1.0:
                if _point_in_prism_2d(px, py, ring, holes):
                    return True
        return False

    def _steer_around_walls(self, move, me, zone):
        """v35: proactive local wall avoidance. If desired move hits a solid prism within 5.5 m,
        pick the smallest clear angular deflection (+/-30..120 deg) before we ever stall."""
        if not self.los_buildings:
            return move
        mx, my = move
        mag = math.hypot(mx, my)
        if mag <= 0.25:
            return move
        ux, uy = mx / mag, my / mag
        px, py, pz = me["pos"]
        probe = 5.5
        if not self._point_blocked_2d(px + probe * ux, py + probe * uy, pz):
            return move
        # Prefer deflections that stay inside next_center/next_radius if we're already inside.
        in_next = math.dist((px, py), zone["next_center"]) <= zone["next_radius"]
        for off in STEER_OFFSETS:
            c, s = math.cos(off), math.sin(off)
            rx, ry = ux * c - uy * s, ux * s + uy * c
            nx, ny = px + probe * rx, py + probe * ry
            if self._point_blocked_2d(nx, ny, pz):
                continue
            if in_next and math.dist((nx, ny), zone["next_center"]) > zone["next_radius"]:
                continue
            return [rx * mag, ry * mag]
        return move

    def _peek_cover(self, me, weapons, target, zone, act):
        laser = next((w for w in weapons[:2] if w and w["kind"] == "laser"), None)
        if laser is None:
            return False
        charge = laser.get("charge") or 0
        full = _stat(laser.get("stats") or {}, "charge", self.laser.get("charge", 0.75))
        if not (0.0 < charge < 0.85 * full) or self._target_blocked(me, target):
            return False
        xy = me["pos"][:2]
        roof = self._current_roof(me["pos"])
        if roof is not None:
            spot = roof[1]
            if not _point_in_prism_2d(spot[0], spot[1], roof[3], roof[4]):
                return False
        else:
            spot = self._find_cover(xy, target["pos"][:2], zone)
            if spot is None:
                return False
        distance = math.dist(xy, spot)
        if distance <= 2.0 or (roof is None and distance > 25.0):
            return False
        act["move"] = [(spot[0] - xy[0]) / distance, (spot[1] - xy[1]) / distance]
        act["boost"] = False
        return True

    def _current_roof(self, pos):
        x, y, z = pos
        for roof in self.roofs:
            _idx, center, radius, ring, holes, _base, top, _climbs = roof
            if abs(z - top) <= 1.5 and math.dist((x, y), center) <= radius + 1.0 and _point_in_prism_2d(x, y, ring, holes):
                return roof
        return None

    def _pick_roof_goal(self, me, zone, now):
        xy = me["pos"][:2]
        mz = me["pos"][2]
        energy = me.get("energy", 0.0)
        best = None
        best_score = math.inf
        for roof in self.roofs:
            idx, center, radius, _ring, _holes, _base, top, climbs = roof
            if idx in self.unreachable_roofs:
                continue
            if math.dist(center, zone["next_center"]) > max(0.0, zone["next_radius"] - radius - 4.0):
                continue
            climb_h = top - mz
            if climb_h > ROOF_CLAIM_MAX_H:
                continue
            if energy < max(45.0, climb_h / 0.6 + 10.0):
                continue
            climb_xy = min(climbs, key=lambda c: math.dist(xy, c))
            dist = math.dist(xy, climb_xy)
            if dist > 140.0:
                continue
            score = dist + 0.5 * math.dist(center, zone["next_center"])
            if score < best_score:
                best_score = score
                best = [idx, climb_xy, center, top, None, dist, now]
        return best

    def _validate_dodge_vec(self, vec, me, zone, on_roof):
        mx, my, mz = me["pos"]
        for cand in (vec, [-vec[0], -vec[1]]):
            ax, ay = mx + 5.0 * cand[0], my + 5.0 * cand[1]
            if math.dist((ax, ay), zone["next_center"]) > zone["next_radius"]:
                continue
            if on_roof is not None:
                _idx, _c, _r, ring, holes, _b, _t, _cl = on_roof
                if not _point_in_prism_2d(ax, ay, ring, holes):
                    continue
            elif self._point_blocked_2d(ax, ay, mz):
                continue
            return cand
        return None

    def _projectile_dodge(self, obs, *, ignore_npc=False, ignore_mortar=False):
        me = obs["self"]
        if not me.get("in_zone", True):
            return None, False
        mx, my, mz = me["pos"]
        mvx, mvy, mvz = me.get("vel") or (0.0, 0.0, 0.0)
        m_speed = math.hypot(mvx, mvy)
        scale = self._scale(me)
        my_r = self.mech_radius * scale + 1.1
        my_h = 2.0 * self.half_height * scale
        zone = obs["zone"]
        on_roof = self._current_roof(me["pos"])
        best_urgency = 0.0
        best_vec = None
        need_boost = False

        for proj in obs.get("projectiles") or []:
            kind = proj.get("kind")
            pos = proj.get("pos")
            vel = proj.get("vel")
            if not pos or not vel:
                continue
            px, py, pz = pos
            vx, vy, vz = vel
            if kind == "mortar":
                if ignore_mortar:
                    continue
                g = self.mortar_gravity
                disc = vz * vz + 2.0 * g * (pz - mz)
                if disc < 0.0:
                    continue
                t_land = (vz + math.sqrt(disc)) / g
                if not (0.05 <= t_land <= 2.4):
                    continue
                ix, iy = px + vx * t_land, py + vy * t_land
                fx, fy = mx + mvx * t_land, my + mvy * t_land
                dx, dy = fx - ix, fy - iy
                d = math.hypot(dx, dy)
                if d < self.mortar_splash:
                    urgency = 3.0 / max(t_land, 0.15)
                    if urgency > best_urgency:
                        cdx, cdy = mx - ix, my - iy
                        cd = math.hypot(cdx, cdy)
                        ux, uy = (cdx / cd, cdy / cd) if cd > 1e-4 else ((dx / d, dy / d) if d > 1e-4 else (1.0, 0.0))
                        best_urgency = urgency
                        best_vec = [ux, uy]
                        need_boost = t_land <= 0.9 and me.get("energy", 0) >= 20
            elif kind in ("gun", "npc"):
                if kind == "npc" and ignore_npc:
                    continue
                rvx, rvy, rvz = vx - mvx, vy - mvy, vz - mvz
                rv2 = rvx * rvx + rvy * rvy + rvz * rvz
                if rv2 <= 1.0:
                    continue
                rx, ry, rz = mx - px, my - py, (mz + 0.5 * my_h) - pz
                t_hit = (rx * rvx + ry * rvy + rz * rvz) / rv2
                if not (0.20 <= t_hit <= 0.65):
                    continue
                dx = (mx + mvx * t_hit) - (px + vx * t_hit)
                dy = (my + mvy * t_hit) - (py + vy * t_hit)
                dz = (mz + 0.5 * my_h + mvz * t_hit) - (pz + vz * t_hit)
                if abs(dz) > 0.5 * my_h + 1.0:
                    continue
                d2 = math.hypot(dx, dy)
                if d2 < my_r:
                    urgency = (1.6 if kind == "gun" else 0.8) / max(t_hit, 0.15)
                    if urgency > best_urgency:
                        vh = math.hypot(vx, vy)
                        if vh > 1e-4:
                            nx, ny = -vy / vh, vx / vh
                            if d2 < 0.65 * my_r and m_speed > 1.0:
                                if nx * mvx + ny * mvy > 0:
                                    nx, ny = -nx, -ny
                            else:
                                if dx * nx + dy * ny < 0:
                                    nx, ny = -nx, -ny
                            best_urgency = urgency
                            best_vec = [nx, ny]
                            need_boost = False

        if best_vec is None:
            return None, False
        valid = self._validate_dodge_vec(best_vec, me, zone, on_roof)
        if valid is None:
            return None, False
        return valid, need_boost

    def _laser_sidestep(self, obs, charging_self):
        me = obs["self"]
        if not me.get("in_zone", True):
            return None, False
        mx, my, _mz = me["pos"]
        my_r = self.mech_radius * self._scale(me)
        zone = obs["zone"]
        on_roof = self._current_roof(me["pos"])
        best_dist = math.inf
        best_vec = None
        for m in obs.get("mechs") or []:
            if m.get("kind") != "mech" or not m.get("charging") or not m.get("pos") or m.get("id") in self.killed:
                continue
            aim = m.get("aim")
            if not aim or aim[0] is None:
                continue
            ex, ey = m["pos"][0], m["pos"][1]
            dist = math.hypot(mx - ex, my - ey)
            if dist > 280.0 or dist < 5.0 or dist >= best_dist:
                continue
            to_me = math.atan2(my - ey, mx - ex)
            cone = max(math.radians(2.0), min(math.radians(18.0), math.atan2(my_r + 3.0, dist)))
            if abs(math.remainder(aim[0] - to_me, math.tau)) > cone:
                continue
            if self._target_blocked(me, m):
                continue
            nx, ny = -math.sin(aim[0]), math.cos(aim[0])
            cand_a = [nx, ny]
            cand_b = [-nx, -ny]
            if on_roof is not None:
                rc = on_roof[1]
                if math.dist((mx + 4 * cand_b[0], my + 4 * cand_b[1]), rc) < math.dist((mx + 4 * cand_a[0], my + 4 * cand_a[1]), rc):
                    cand_a, cand_b = cand_b, cand_a
            else:
                cross = math.cos(aim[0]) * (my - ey) - math.sin(aim[0]) * (mx - ex)
                if cross < 0:
                    cand_a, cand_b = cand_b, cand_a
            valid = self._validate_dodge_vec(cand_a, me, zone, on_roof)
            if valid is not None:
                best_dist = dist
                best_vec = valid
        if best_vec is None:
            return None, False
        return best_vec, (not charging_self and me.get("energy", 0) >= 35 and best_dist <= 160.0)

    def _find_cover(self, xy, threat, zone):
        closest = None
        best_distance = math.inf
        for center, radius, ring, _holes, _base, _top in self.buildings:
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
        threshold = 0.85 if self.healing else (0.65 if self.is_finals else 0.5)
        if not me["in_zone"] or me["hp"] >= threshold * me["max_hp"]:
            self.healing = False
            return False

        on_roof = self._current_roof(pos)
        nearest_mech = min((m for m in obs.get("mechs") or [] if m.get("kind") == "mech" and m.get("pos")),
                           key=lambda m: math.dist(pos, m["pos"]), default=None)
        if nearest_mech is not None:
            dist_3d = math.dist(pos, nearest_mech["pos"])
            safe_above = on_roof is not None and (pos[2] - nearest_mech["pos"][2] >= 7.0) and self._target_blocked(me, nearest_mech)
            if dist_3d <= self.near_range and not safe_above:
                self.healing = False
                return False

        now, zone, xy = obs["t"], obs["zone"], pos[:2]
        threat = None
        yaw = me["aim"][0]
        if nearest_mech is not None:
            threat = nearest_mech["pos"][:2]
            yaw = math.atan2(threat[1] - xy[1], threat[0] - xy[0])
        elif self.last_mech_bearing is not None and now - self.last_mech_bearing[0] <= 10:
            yaw = self.last_mech_bearing[1]
            threat = (xy[0] + 100 * math.cos(yaw), xy[1] + 100 * math.sin(yaw))

        if on_roof is not None:
            self.healing = True
            center = on_roof[1]
            dist_c = math.dist(xy, center)
            move = [(center[0] - xy[0]) / dist_c, (center[1] - xy[1]) / dist_c] if dist_c > 2.5 else [0.0, 0.0]
            act.update(move=move, boost=False, aim=[yaw, 0.0])
            mf.draw.label(f"roof-heal {me['hp'] / me['max_hp']:.0%} c{me.get('cubes', 0)}"[:80])
            return True

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
            ux, uy = -math.cos(yaw), -math.sin(yaw)
            ahead = (xy[0] + 4 * ux, xy[1] + 4 * uy)
            if math.dist(ahead, zone["next_center"]) <= zone["next_radius"]:
                move = [ux, uy]
        act.update(move=move, boost=boost, aim=[yaw, 0.0])
        mf.draw.label(f"heal {me['hp'] / me['max_hp']:.0%} c{me.get('cubes', 0)}"[:80])
        return True

    def _remember_damage(self, events, now):
        for event in events:
            etype = event.get("type")
            if etype == "hit":
                tid = event.get("target")
                if tid is not None and 0 <= tid < 16:
                    self.recent_dealt[tid] = now
                continue
            attacker = event.get("by")
            if etype != "damaged" or attacker is None:
                continue
            bearing = event.get("bearing")
            self.last_hits[attacker] = (now, bearing)
            if bearing is not None:
                self.last_damage_bearing = bearing
                if 0 <= attacker < 16:
                    self.last_mech_bearing = (now, bearing)

    def _remember_beams(self, beams, pos, now):
        for beam in beams:
            by = beam.get("by")
            path = beam.get("path") or []
            if by is None or not (0 <= by < 16) or by in self.killed or not path:
                continue
            origin = path[0]
            if len(origin) < 2:
                continue
            bearing = math.atan2(origin[1] - pos[1], origin[0] - pos[0])
            fired_at = now - beam.get("age", 0.0)
            if self.last_beam_threat is None or fired_at >= self.last_beam_threat[0]:
                self.last_beam_threat = (fired_at, bearing, origin)

    def _eff_hp(self, mech, has_laser):
        hp = mech.get("hp")
        if hp is None:
            return None
        eff = hp
        if has_laser and "mortar" in (mech.get("weapons") or []):
            eff *= 0.70
        elif mech.get("charging"):
            eff *= 0.85
        # Point 11: in Finals FFA, prioritize mechs actively taking third-party damage.
        if USE_FFA_THIRD_PARTY and self.is_finals and self._now - self.hp_drop_t.get(mech.get("id"), -math.inf) <= 2.0:
            eff *= 0.8
        return eff

    def _choose_target(self, mechs, pos, now, weapons, cubes=0):
        laser = next((w for w in weapons if w and w["kind"] == "laser"), None)
        has_laser = laser is not None
        if laser:
            reach = _stat(laser.get("stats") or {}, "range", _stat(self.laser, "range", 280))
        else:
            gun = next((w for w in weapons if w and w["kind"] == "gun"), None) or {}
            reach = _stat(gun.get("stats") or {}, "range", self.gun_range)

        laser_damage = 0.0
        if laser:
            laser_damage = _stat(laser.get("stats") or {}, "damage", _stat(self.laser, "damage", 315))
            laser_damage *= 0.955 * 0.76 * (1 + self.damage_per_cube * min(cubes or 0, self.cube_cap))

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
            wounded_cut = 0.60 if self.is_finals else 0.50
            wounded = hp is not None and max_hp is not None and hp <= wounded_cut * max_hp
            if not (recent or distance <= self.near_range or (wounded and distance <= reach)):
                continue
            if under_fire and not recent and distance > self.near_range and not (hp is not None and hp <= laser_damage):
                continue
            if now >= LATE_T and not recent and distance > self.near_range:
                continue
            if mech_id == self.target_id:
                current = mech
            eff_hp = self._eff_hp(mech, has_laser)
            if eff_hp is None:
                rank = (math.inf, 0, distance - (1.0 if recent else 0.0))
            else:
                rank = (eff_hp, not recent, distance)
            if best_rank is None or rank < best_rank:
                best, best_rank = mech, rank

        if current is not None and best is not None:
            cur_eff = self._eff_hp(current, has_laser)
            best_eff = self._eff_hp(best, has_laser)
            if cur_eff is None or best_eff is None or best_eff >= 0.6 * cur_eff:
                best = current
        self.target_id = best["id"] if best is not None else None
        return best

    def _drop_goal(self, obs, healing):
        me, zone, now = obs["self"], obs["zone"], obs["t"]
        healthy = me["hp"] >= 0.75 * me["max_hp"]
        max_drop_dist = DROP_HEALTHY_DIST if healthy else 250.0
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
                return drop
            contested = any(m.get("kind") == "mech" and m["id"] != me["id"]
                            and math.dist(m["pos"][:2], xy) <= drop["radius"] + 12
                            for m in obs.get("mechs") or [])
            if contested:
                first_c = self.drop_contested_since.setdefault(drop_id, now)
                if now - first_c >= DROP_CONTEST_ABORT_S:
                    self.drop_retry_at[drop_id] = now + 60.0
                elif active:
                    self.drop_retry_at[drop_id] = now + 15.0
                continue
            else:
                self.drop_contested_since.pop(drop_id, None)
            if not in_ring and me["hp"] < 0.35 * me["max_hp"]:
                if active:
                    self.drop_retry_at[drop_id] = now + 15.0
                continue
            if ((healing and not active) or not me["in_zone"] or distance > max_drop_dist
                    or math.dist(xy, zone["next_center"]) > zone["next_radius"] - 4):
                continue
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
        now = obs["t"]
        self.kill_spots = [(t, xy) for t, xy in self.kill_spots if now - t <= KILL_LOOT_S]
        shot_at = any(0 <= mid < 16 and now - hit[0] <= THREAT_RECENT_S for mid, hit in self.last_hits.items())
        loot_reach = KILL_LOOT_RANGE if now < LATE_T else 80.0
        for cube_id, location in list(self.cubes.items()):
            distance = math.dist(pos[:2], location[:2])
            height = location[2] - pos[2]
            if abs(height) <= 4 and ((picked_up and distance <= self.cube_radius)
                                     or (cube_id not in visible and distance <= 4)):
                del self.cubes[cube_id]
                continue
            reach = max_distance
            if not pursuing_drop and not shot_at and any(math.dist(location[:2], xy) <= 12 for _, xy in self.kill_spots):
                reach = max(reach, loot_reach)
            if (height <= 3.5
                    and distance <= reach and cube_id not in self.unreachable
                    and math.dist(location[:2], zone["next_center"]) <= zone["next_radius"]):
                options.append((distance, cube_id))

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

    def _movement(self, obs, weapons, act, drop=None):
        me = obs["self"]
        xy = me["pos"][:2]
        mz = me["pos"][2]
        zone = obs["zone"]
        now = obs["t"]
        goal = zone["next_center"]
        visible = {p["id"]: p for p in obs.get("pickups") or []}
        self.pickups.update(visible)
        for pickup_id, pickup in list(self.pickups.items()):
            if pickup_id not in visible and math.dist(xy, pickup["pos"][:2]) <= 6:
                del self.pickups[pickup_id]
        for event in obs.get("events") or []:
            if event.get("type") in ("took", "take_failed"):
                self.pickups.pop(event.get("id"), None)

        has_laser = any(w and w["kind"] == "laser" for w in weapons[:2])
        slot_empty = len(weapons) < 2 or weapons[1] is None
        lightning_slot = next((i for i, w in enumerate(weapons[:2]) if w and w["kind"] == "lightning"), None)
        laser_charging = any(w and w["kind"] == "laser" and (w.get("charge") or 0) > 0 for w in weapons[:2])
        enemy_close = any(
            m.get("kind") == "mech" and m.get("pos") and m.get("id") not in self.killed
            and math.dist(m["pos"][:2], xy) <= self.near_range
            for m in obs.get("mechs") or []
        )

        state = "zone"
        outside = not me["in_zone"]
        boost = outside
        jump = obs["tick"] % 40 == 0
        hunt_id = None
        hunt_pickup = None

        want_weapon = (not has_laser) and (slot_empty or lightning_slot is not None)
        if want_weapon:
            best_take = best_hunt = (2, math.inf)
            for pickup_id, pickup in self.pickups.items():
                kind = pickup["kind"]
                if kind == "laser":
                    pass
                elif kind == "lightning" and slot_empty:
                    pass
                else:
                    continue
                location = pickup["pos"][:2]
                distance = math.dist(xy, location)
                dz = pickup["pos"][2] - mz
                rank = (0 if kind == "laser" else 1, distance)
                if (pickup_id in visible and distance <= self.reach and abs(dz) <= 4.0
                        and rank < best_take and not laser_charging):
                    act["take"] = pickup_id
                    if not slot_empty and lightning_slot is not None and kind == "laser":
                        act["drop"] = lightning_slot
                    else:
                        act.pop("drop", None)
                    best_take = rank
                if pickup_id in self.unreachable:
                    continue
                if dz > 5.0:
                    if not (kind == "laser" and dz <= ROOF_LASER_MAX_DZ
                            and me.get("energy", 0) >= max(60.0, dz / 0.6 + 10.0) and not enemy_close):
                        continue
                if kind == "laser":
                    max_hunt_dist = 250.0 if now < 90.0 else 130.0
                    time_ok = now < LATE_T
                else:
                    max_hunt_dist = 250.0
                    time_ok = now < 90.0
                if (time_ok and distance <= max_hunt_dist and rank < best_hunt
                        and math.dist(location, zone["next_center"]) <= zone["next_radius"]):
                    best_hunt = rank
                    hunt_id = pickup_id
                    hunt_pickup = pickup
                    state = "laser hunt"
                    goal = location
                    boost = outside or (me["energy"] >= 30 and distance > 25)

        yaw = math.atan2(goal[1] - xy[1], goal[0] - xy[0])
        move_yaw = yaw

        holding_drop = drop is not None and math.dist(xy, drop["pos"][:2]) <= drop["radius"] - 2
        if holding_drop:
            cube = None
        elif drop is not None:
            cube = self._cube_goal(obs, 15.0, pursuing_drop=True)
        else:
            cube_reach = 40 if hunt_id is not None else (CUBE_IDLE_RANGE if self.target_id is None else 40)
            cube = self._cube_goal(obs, cube_reach, pursuing_drop=False)

        if cube is not None:
            location, distance = cube
            state = "cube"
            move_yaw = math.atan2(location[1] - xy[1], location[0] - xy[0])
            boost = me["energy"] >= 40 and distance > 15
            self.hunt_progress.pop(hunt_id, None)
        elif drop is not None:
            self.hunt_progress.pop(hunt_id, None)
            dx, dy = drop["pos"][0] - xy[0], drop["pos"][1] - xy[1]
            distance = math.hypot(dx, dy)
            act.update(move=[0.0, 0.0] if holding_drop else [dx / distance, dy / distance],
                       aim=[yaw, 0.0], boost=not holding_drop and me["energy"] >= 30 and distance > 30,
                       jump=not holding_drop and obs["tick"] % 40 == 0)
            return f"drop-hold {drop['progress']:.1f}/{drop['capture_s']:g}s" if holding_drop else "drop-walk"
        elif hunt_id is not None:
            best, since = self.hunt_progress.get(hunt_id, (math.inf, now))
            if best_hunt[1] < best - 1:
                self.hunt_progress[hunt_id] = (best_hunt[1], now)
            elif now - since > 6:
                self.unreachable.add(hunt_id)
            if hunt_pickup is not None and hunt_pickup["pos"][2] - mz > 3.5 and best_hunt[1] <= 12.0:
                if me.get("energy", 0) >= 15:
                    jump = bool(me.get("grounded", False))
                    boost = True
        elif (now >= LATE_T or self.is_finals) and has_laser and not outside and self.roofs:
            on_roof = self._current_roof(me["pos"])
            if on_roof is not None and math.dist(on_roof[1], zone["next_center"]) <= zone["next_radius"] - 4.0:
                self.roof_goal = None
                state = "roof"
                center = on_roof[1]
                dc = math.dist(xy, center)
                if dc <= 4.0:
                    act.update(move=[0.0, 0.0], aim=[yaw, 0.0], boost=False, jump=False)
                    return state
                move_yaw = math.atan2(center[1] - xy[1], center[0] - xy[0])
                boost = False
                jump = False
            elif not enemy_close:
                if self.roof_goal is not None:
                    r_id, climb_xy, center_xy, top, climb_started, w_best, w_since = self.roof_goal
                    out_of_zone = math.dist(center_xy, zone["next_center"]) > zone["next_radius"] - 4.0
                    d_now = math.dist(xy, climb_xy)
                    if d_now < w_best - 1.0:
                        self.roof_goal[5] = d_now
                        self.roof_goal[6] = now
                        w_since = now
                    walk_timed_out = climb_started is None and (now - w_since > ROOF_WALK_TIMEOUT_S)
                    climb_timed_out = climb_started is not None and (now - climb_started > 6.0) and mz < top - 1.0
                    if out_of_zone or walk_timed_out or climb_timed_out:
                        if walk_timed_out or climb_timed_out:
                            self.unreachable_roofs.add(r_id)
                        self.roof_goal = None
                if self.roof_goal is None:
                    self.roof_goal = self._pick_roof_goal(me, zone, now)
                if self.roof_goal is not None:
                    r_id, climb_xy, center_xy, top, climb_started, _wb, _ws = self.roof_goal
                    d_climb = math.dist(xy, climb_xy)
                    if mz >= top - 0.5:
                        state = "roof-climb"
                        move_yaw = math.atan2(center_xy[1] - xy[1], center_xy[0] - xy[0])
                        boost = False
                        jump = False
                    elif d_climb <= 6.0:
                        state = "roof-climb"
                        if climb_started is None:
                            self.roof_goal[4] = now
                        move_yaw = math.atan2(center_xy[1] - xy[1], center_xy[0] - xy[0])
                        jump = bool(me.get("grounded", False))
                        boost = me.get("energy", 0) >= 15
                    else:
                        state = "roof-walk"
                        move_yaw = math.atan2(climb_xy[1] - xy[1], climb_xy[0] - xy[0])
                        boost = False

        act.update(move=[math.cos(move_yaw), math.sin(move_yaw)], aim=[yaw, 0.0],
                   boost=boost, jump=jump)
        return state

    def _track(self, mechs, now):
        for m in mechs:
            if m.get("kind") not in ("mech", "npc") or m.get("id") is None or not m.get("pos"):
                continue
            pos, vel = m["pos"], m.get("vel")
            prev = self.tracks.get(m["id"])
            if prev and 0 < now - prev[0] <= 0.21:
                delta = [(p - q) / (now - prev[0]) for p, q in zip(pos, prev[1])]
                vel = [0.85 * v + 0.15 * d for v, d in zip(vel, delta)] if vel else delta
            self.tracks[m["id"]] = (now, pos, vel or (0, 0, 0))
            # Point 11: detect third-party HP drops on enemy mechs for Finals targeting.
            if m.get("kind") == "mech":
                hp = m.get("hp")
                if hp is not None:
                    prev_hp = self.hp_seen.get(m["id"])
                    if prev_hp and hp < prev_hp[1] - 1 and now - self.recent_dealt.get(m["id"], -math.inf) > 0.5:
                        self.hp_drop_t[m["id"]] = now
                    self.hp_seen[m["id"]] = (now, hp)

    def _scale(self, mech):
        return 1 + self.size_per_cube * (mech.get("cubes") or 0)

    def _lead_aim(self, me, target, delay, speed=None):
        vel = self.tracks.get(target["id"], (0, target["pos"], target.get("vel") or (0, 0, 0)))[2]
        own = me.get("vel") or (0, 0, 0)
        stats = me.get("stats") or {}
        dx, dy, dz = (p - q + (v - u) * delay for p, q, v, u in zip(target["pos"], me["pos"], vel, own))
        own_scale = self._scale(me)
        if target.get("kind") == "npc":
            target_half = self.npc_half_height
        else:
            target_half = self.half_height * self._scale(target)
        dz += target_half - _stat(stats, "muzzle_height", self.muzzle_height * own_scale)
        offset = _stat(stats, "radius", self.mech_radius * own_scale) + 0.5
        if speed is not None:
            vx, vy, vz = vel
            a = speed * speed - (vx * vx + vy * vy + vz * vz)
            b = offset * speed - (dx * vx + dy * vy + dz * vz)
            c = dx * dx + dy * dy + dz * dz - offset * offset
            if c > 0 and a > 0:
                flight = c / (math.sqrt(b * b + a * c) + b)
                dx, dy, dz = dx + vx * flight, dy + vy * flight, dz + vz * flight
        return [math.atan2(dy, dx), math.atan2(dz, math.hypot(dx, dy))], math.hypot(dx, dy, dz)

    def _on_body(self, actual, aim, distance, target, spread=None):
        if not actual or None in actual or distance <= 1e-6:
            return False
        if target.get("kind") == "npc":
            radius = self.npc_radius
            half_h = self.npc_half_height
        else:
            scale = self._scale(target)
            radius = self.mech_radius * scale
            half_h = self.half_height * scale
        width = math.atan2(radius, distance)
        projected_height = half_h * math.cos(aim[1]) + radius * abs(math.sin(aim[1]))
        height = math.atan2(projected_height, distance)
        yaw = abs(math.remainder(actual[0] - aim[0], math.tau)) * math.cos(aim[1])
        pitch = abs(actual[1] - aim[1])
        if spread is None:
            gate = min(math.radians(4), 0.8 * width)
            if self.laser_full_since is not None and self._now - self.laser_full_since >= 0.8:
                return yaw <= min(2 * gate, width) and pitch <= height
            return yaw <= gate and pitch <= 0.8 * height
        gate = min(width, math.radians(12), max(math.radians(0.1), width - 0.25 * math.radians(spread)))
        return math.hypot(yaw, pitch * width / max(height, 1e-6)) <= gate

    def _laser_ready(self, me, weapon, target):
        stats = weapon.get("stats") or {}
        charge = weapon.get("charge") or 0
        full = 0.93 * _stat(stats, "charge", self.laser.get("charge", 0.75))
        if charge < full:
            self.laser_full_since = None
            return False
        if self.laser_full_since is None:
            self.laser_full_since = self._now
        if self._target_blocked(me, target):
            return False
        aim, distance = self._lead_aim(me, target, 0.05)
        return self._on_body(me.get("aim"), aim, distance, target)

    def _alt_laser_target(self, me, mechs, exclude_id, reach):
        actual = me.get("aim")
        if not actual or actual[0] is None:
            return None
        actual_yaw = actual[0]
        mx, my = me["pos"][0], me["pos"][1]
        best = None
        best_hp = math.inf
        for m in mechs:
            mid = m.get("id")
            if m.get("kind") != "mech" or mid is None or mid == exclude_id or mid in self.killed or not m.get("pos"):
                continue
            if math.dist(me["pos"], m["pos"]) > reach:
                continue
            to_alt = math.atan2(m["pos"][1] - my, m["pos"][0] - mx)
            if abs(math.remainder(to_alt - actual_yaw, math.tau)) > math.radians(30.0):
                continue
            if self._target_blocked(me, m):
                continue
            hp = m.get("hp") if m.get("hp") is not None else 1400.0
            if hp < best_hp:
                best, best_hp = m, hp
        return best

    def _fight(self, me, weapons, target, act, mechs=None):
        x, y, _z = me["pos"]
        muzzle_z = self._muzzle_z(me)
        tx, ty, tz = target["pos"]
        target_half = self.npc_half_height if target.get("kind") == "npc" else self.half_height * self._scale(target)
        direct = [math.atan2(ty - y, tx - x),
                  math.atan2(tz + target_half - muzzle_z, max(math.hypot(tx - x, ty - y), 1e-6))]
        distance = math.dist(me["pos"], target["pos"])
        actual = me.get("aim")

        def aligned(yaw, degrees):
            return (bool(actual) and actual[0] is not None
                    and abs(math.remainder(yaw - actual[0], math.tau)) <= math.radians(degrees))

        aim = direct
        use_direct = False
        charging = False
        blocked = self._target_blocked(me, target)
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
                delay = 0.1 if (weapon.get("cooldown") or 0) > 0.05 else 0.05
                aim, intercept_range = self._lead_aim(me, target, delay, _stat(stats, "speed", self.gun_speed))
                barrel = _stat(me.get("stats") or {}, "radius", self.mech_radius * self._scale(me)) + 0.5
                act["fire"][i] = (not blocked
                                  and intercept_range - barrel <= _stat(stats, "range", self.gun_range)
                                  and self._on_body(actual, aim, intercept_range, target,
                                                    _stat(stats, "spread_deg", self.spread)))
                if blocked and (weapon.get("reload") or 0) <= 0 and (weapon.get("ammo") is not None) and 0 < weapon["ammo"] <= 6:
                    act["reload"] = True
            elif kind == "laser":
                reach = _stat(stats, "range", self.laser.get("range", 280))
                cur_charge = weapon.get("charge") or 0
                if distance <= reach and ((cur_charge == 0 and weapon.get("cooldown", 0) <= 0 and not blocked)
                                          or cur_charge > 0):
                    laser_tgt = target
                    if blocked and cur_charge > 0 and mechs:
                        alt = self._alt_laser_target(me, mechs, target.get("id"), reach)
                        if alt is not None:
                            laser_tgt = alt
                            blocked = False
                    self.laser_target = laser_tgt["id"]
                    full_charge = _stat(stats, "charge", self.laser.get("charge", 0.75))
                    near_full = cur_charge >= 0.93 * full_charge - 0.1
                    if near_full or not gun_useful or laser_tgt is not target:
                        use_direct = True
                        direct, _ = self._lead_aim(me, laser_tgt, LASER_LEAD_S)
                    if blocked and self.laser_full_since is not None and self._now - self.laser_full_since >= 1.6:
                        charging = False
                    else:
                        charging = not self._laser_ready(me, weapon, laser_tgt)
                    act["fire"][i] = charging
                    self.laser_released = not charging
            elif kind == "lightning":
                reach = _stat(stats, "range", self.lightning.get("range", 45))
                if not blocked and distance <= 0.9 * reach and me["energy"] >= 10:
                    use_direct = True
                    cone = _stat(stats, "cone_deg", self.lightning.get("cone_deg", 30))
                    act["fire"][i] = aligned(direct[0], 0.4 * cone)
        act["aim"] = direct if use_direct else aim
        return charging

    def _shoot_beam_origin(self, obs, weapons, act):
        if self.last_beam_threat is None:
            return False
        fired_at, _bearing, origin = self.last_beam_threat
        if obs["t"] - fired_at > 0.8 or len(origin) < 3:
            return False
        me = obs["self"]
        muzzle_pos = (me["pos"][0], me["pos"][1], self._muzzle_z(me))
        aim_pt = (origin[0], origin[1], origin[2] - 2.5)
        dist = math.dist(muzzle_pos, aim_pt)
        if dist > self.gun_range or dist < 5.0 or self._building_blocked(muzzle_pos, aim_pt):
            return False
        dx, dy, dz = aim_pt[0] - muzzle_pos[0], aim_pt[1] - muzzle_pos[1], aim_pt[2] - muzzle_pos[2]
        yaw = math.atan2(dy, dx)
        pitch = math.atan2(dz, max(math.hypot(dx, dy), 1e-6))
        act["aim"] = [yaw, pitch]
        actual = me.get("aim") or [None, None]
        gate = min(math.radians(4.0), math.atan2(self.mech_radius, max(dist, 1.0)))
        on = (actual[0] is not None and actual[1] is not None
              and abs(math.remainder(yaw - actual[0], math.tau)) <= gate
              and abs(pitch - actual[1]) <= math.atan2(self.half_height, max(dist, 1.0)))
        for i, w in enumerate(weapons[:2]):
            if w and w["kind"] == "gun" and (w.get("reload") or 0) <= 0 and (w.get("ammo") is None or w["ammo"] > 0):
                act["fire"][i] = on
                break
        return True

    def _maybe_early_reload(self, weapons, act):
        for w in weapons[:2]:
            if w and w["kind"] == "gun":
                if (w.get("reload") or 0) <= 0 and (w.get("ammo") is not None) and 0 < w["ammo"] <= 6:
                    act["reload"] = True
                return

    def _shoot_drone(self, obs, weapons, act):
        me = obs["self"]
        now = obs["t"]
        x, y, z = me["pos"]
        zone = obs["zone"]
        cubes = me.get("cubes") or 0
        best = None
        for m in obs.get("mechs") or []:
            if m.get("kind") != "npc" or not m.get("pos"):
                continue
            npc_id = m.get("id")
            dx, dy, dz = m["pos"][0] - x, m["pos"][1] - y, m["pos"][2] - z
            distance = math.hypot(dx, dy)
            hit = self.last_hits.get(npc_id)
            attacking_us = hit is not None and now - hit[0] <= THREAT_RECENT_S
            farm_ok = now < LATE_T and cubes < DRONE_CUBE_CAP and distance <= DRONE_RANGE
            if not (attacking_us or farm_ok):
                continue
            if abs(dz) > 4.0 or math.dist(m["pos"][:2], zone["next_center"]) > zone["next_radius"]:
                continue
            if self._target_blocked(me, m):
                continue
            rank = (0 if attacking_us else 1, distance)
            if best is None or rank < best[1]:
                best = (m, rank)
        if best is None:
            return False
        drone, _rank = best
        self._fight(me, weapons, drone, act)
        return True

    def _shoot_crate(self, obs, weapons, act):
        me = obs["self"]
        x, y, z = me["pos"]
        zone = obs["zone"]
        best = None
        for crate in obs.get("crates") or []:
            cx, cy, cz = crate["pos"]
            distance = math.hypot(cx - x, cy - y)
            if (distance <= CRATE_RANGE and abs(cz - z) <= 3 and (best is None or distance < best[1])
                    and math.dist((cx, cy), zone["next_center"]) <= zone["next_radius"]):
                best = (crate, distance)
        if best is None:
            return False
        crate, distance = best
        cx, cy, cz = crate["pos"]
        muzzle_z = self._muzzle_z(me)
        yaw = math.atan2(cy - y, cx - x)
        act["aim"] = [yaw, math.atan2(cz + self.crate_height / 2 - muzzle_z, max(distance, 1.0))]
        actual = me.get("aim") or [None]
        on = actual[0] is not None and abs(math.remainder(yaw - actual[0], math.tau)) <= math.radians(
            max(0.5, min(5.0, math.degrees(math.atan2(0.8 * self.crate_radius, max(distance, 1.0))))))
        laser_slot = next((i for i, w in enumerate(weapons[:2]) if w and w["kind"] == "laser"
                           and (w.get("cooldown", 0) <= 0 or (w.get("charge") or 0) > 0)), None)
        if laser_slot is not None:
            w = weapons[laser_slot]
            full = 0.93 * _stat(w.get("stats") or {}, "charge", self.laser.get("charge", 0.75))
            act["fire"][laser_slot] = not ((w.get("charge") or 0) >= full + 0.04 and on)
            self.laser_released = not act["fire"][laser_slot]
            return True
        gun_slot = next((i for i, w in enumerate(weapons[:2]) if w and w["kind"] == "gun"), None)
        if gun_slot is not None:
            act["fire"][gun_slot] = on
        return True

    def _should_push(self, obs, target):
        me, zone, now = obs["self"], obs["zone"], obs["t"]
        # Point 13: in the first 60 s, don't push a laser holder when we don't have a laser.
        if USE_EARLY_CAUTION and now < 60.0:
            my_laser = any(w and w["kind"] == "laser" for w in (me.get("weapons") or [])[:2])
            if "laser" in (target.get("weapons") or []) and not my_laser:
                return False
        if now >= LATE_T or me["hp"] < PUSH_MIN_HP * me["max_hp"] or not target.get("pos"):
            return False
        if self.is_finals:
            hp, max_hp = target.get("hp"), target.get("max_hp")
            if hp is None or max_hp is None or hp > 0.5 * max_hp:
                return False
        distance = math.dist(me["pos"][:2], target["pos"][:2])
        if not PUSH_STOP <= distance <= PUSH_RANGE:
            return False
        hp, cubes = target.get("hp"), target.get("cubes") or 0
        has_laser = any(w and w["kind"] == "laser" for w in (me.get("weapons") or [])[:2])
        t_weapons = target.get("weapons") or []
        # Point 15: without a laser, don't push a laser holder unless they are <= 50% of our HP.
        if USE_NO_LASER_CAUTION and not has_laser and "laser" in t_weapons and (hp is None or hp > 0.5 * me["hp"]):
            return False
        outgunned = (has_laser and "laser" not in t_weapons and "lightning" not in t_weapons
                     and hp is not None and hp <= 0.95 * me["hp"])
        weaker = (hp is not None and hp <= 0.7 * me["hp"]) or cubes + 2 <= (me.get("cubes") or 0) or outgunned
        if not weaker or math.dist(target["pos"][:2], zone["next_center"]) > zone["next_radius"]:
            return False
        return not any(m.get("kind") == "mech" and m.get("id") != target.get("id") and m.get("pos")
                       and m.get("id") not in self.killed and math.dist(m["pos"][:2], me["pos"][:2]) <= PUSH_CLEAR
                       for m in obs.get("mechs") or [])

    def _anti_sandwich_move(self, me, mechs, zone):
        xy = me["pos"][:2]
        bearings = []
        for m in mechs:
            if m.get("kind") != "mech" or m.get("id") in self.killed or not m.get("pos"):
                continue
            d = math.dist(xy, m["pos"][:2])
            if d <= SANDWICH_RANGE:
                bearings.append(math.atan2(m["pos"][1] - xy[1], m["pos"][0] - xy[0]))
        if len(bearings) < 2:
            return None
        bearings.sort()
        max_gap = 0.0
        best_mid = 0.0
        for i in range(len(bearings)):
            a = bearings[i]
            b = bearings[i + 1] if i + 1 < len(bearings) else bearings[0] + math.tau
            gap = b - a
            if gap > max_gap:
                max_gap = gap
                best_mid = a + 0.5 * gap
        if math.tau - max_gap <= SANDWICH_SPAN_RAD:
            return None
        ux, uy = math.cos(best_mid), math.sin(best_mid)
        ahead = (xy[0] + 6.0 * ux, xy[1] + 6.0 * uy)
        if math.dist(ahead, zone["next_center"]) <= zone["next_radius"]:
            return [ux, uy]
        return None

    def _rotate_move_safe(self, move, angle, xy, zone):
        mx, my = move
        if math.hypot(mx, my) <= 1e-6:
            return move
        for sign in (1.0, -1.0):
            ang = angle * sign
            c, s = math.cos(ang), math.sin(ang)
            rx, ry = mx * c - my * s, mx * s + my * c
            ahead = (xy[0] + 6.0 * rx, xy[1] + 6.0 * ry)
            if math.dist(ahead, zone["next_center"]) <= zone["next_radius"]:
                return [rx, ry]
        return move

    def _apply_unstick(self, obs, act, charging):
        now = obs["t"]
        me = obs["self"]
        x, y = me["pos"][0], me["pos"][1]
        self.pos_history.append((now, x, y))
        self.pos_history = [p for p in self.pos_history if now - p[0] <= 0.65]

        move = act.get("move") or [0.0, 0.0]
        if math.hypot(move[0], move[1]) <= 0.3:
            return

        if now >= self.unstick_until and not charging:
            oldest = self.pos_history[0]
            if now - oldest[0] >= 0.45 and math.hypot(x - oldest[1], y - oldest[2]) < 1.5:
                if now - self.unstick_started <= 4.0:
                    self.unstick_streak += 1
                    if self.unstick_streak >= 3:
                        self.unstick_sign = -self.unstick_sign
                        self.unstick_streak = 0
                else:
                    self.unstick_streak = 1
                self.unstick_started = now
                self.unstick_until = now + 1.2

        if now < self.unstick_until:
            ang = self.unstick_sign * (math.pi / 2.0)
            c, s = math.cos(ang), math.sin(ang)
            mx, my = move
            act["move"] = [mx * c - my * s, mx * s + my * c]
            if now - self.unstick_started <= 0.5 and me.get("energy", 0) >= 60:
                act["jump"] = bool(me.get("grounded", False))
                act["boost"] = True

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
        if self.last_beam_threat is not None and now - self.last_beam_threat[0] <= 3.0:
            return self.last_beam_threat[1]
        nearest = min((m for m in mechs if m.get("kind") == "mech" and m.get("pos")),
                      key=lambda m: math.dist(pos, m["pos"]), default=None)
        if nearest is not None:
            return math.atan2(nearest["pos"][1] - pos[1], nearest["pos"][0] - pos[0])
        if self.last_sound is not None and now - self.last_sound[0] <= 2:
            return self.last_sound[1]
        return None

    def _laser_guard(self, obs, act):
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
            aim, _ = self._lead_aim(me, pick, LASER_LEAD_S)
            actual = me.get("aim") or [None]
            if actual[0] is not None and abs(math.remainder(aim[0] - actual[0], math.tau)) > math.radians(30):
                return
            act["aim"] = aim
            fire[i] = not self._laser_ready(me, weapon, pick)
            return

    def act(self, obs: mf.Observation) -> mf.Action:
        self.laser_released = False
        self._now = obs.get("t", 0.0)
        self._los_cache.clear()
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
        new_kills = 0
        for e in events:
            if e.get("type") == "kill" and "target" in e:
                tid = e["target"]
                if tid not in self.killed:
                    new_kills += 1
                self.killed.add(tid)
                spot = self.mech_seen.get(tid)
                if spot is not None:
                    self.kill_spots.append((now, spot))

        alive = obs.get("alive")
        if alive is not None:
            alive_i = int(alive)
            if not self.is_finals and now < FINALS_DETECT_T and alive_i < self.prev_alive:
                delta_deaths = (self.prev_alive - alive_i) - new_kills
                if delta_deaths > 0:
                    recently_hit_any = any(now - t <= 3.0 for t in self.recent_dealt.values())
                    if not recently_hit_any:
                        self.non_our_deaths += delta_deaths
                        if self.non_our_deaths >= 2:
                            self.is_finals = True
                            self.finals_t = now
            self.prev_alive = alive_i

        for m in obs.get("mechs") or []:
            if m.get("kind") == "mech" and m.get("pos") and m.get("id") is not None:
                self.mech_seen[m["id"]] = (m["pos"][0], m["pos"][1])
        self._remember_sounds(obs.get("sounds") or [], now)
        me = obs["self"]
        self._remember_beams(obs.get("beams") or [], me["pos"], now)
        weapons = me.get("weapons") or []
        mechs = obs.get("mechs") or []
        self._track(mechs, now)
        act: mf.Action = {"tick": obs["tick"], "fire": [False, False]}
        choices = (obs.get("offer") or {}).get("choices") or []
        if choices:
            act["pick"] = min(range(len(choices)),
                              key=lambda i: UPGRADE_RANK.get(choices[i].get("id"), len(UPGRADE_RANK)))
        target = self._choose_target(mechs, me["pos"], now, weapons, me.get("cubes", 0))
        finishing = (target is not None and target.get("hp") is not None and target.get("max_hp")
                     and target["hp"] <= 0.3 * target["max_hp"] and target["hp"] < me["hp"])
        healing = not finishing and self._heal(obs, act)
        drop = self._drop_goal(obs, healing)
        if healing:
            if target is not None:
                hit = self.last_hits.get(target["id"])
                if hit is not None and now - hit[0] <= HEAL_FIGHTBACK_S:
                    move, boost = act["move"], act.get("boost")
                    self._fight(me, weapons, target, act, mechs)
                    act.update(move=move, boost=boost)
                    for i, weapon in enumerate(weapons[:2]):
                        if weapon and weapon["kind"] == "laser" and not (weapon.get("charge") or 0) > 0:
                            act["fire"][i] = False
            else:
                self._maybe_early_reload(weapons, act)
            dodge_vec, dodge_boost = self._projectile_dodge(obs)
            if dodge_vec is not None:
                act["move"] = dodge_vec
                if dodge_boost:
                    act["boost"] = True
            if USE_WALL_STEER and self._current_roof(me["pos"]) is None:
                act["move"] = self._steer_around_walls(act["move"], me, obs["zone"])
            self._apply_unstick(obs, act, charging=False)
            return act

        movement = self._movement(obs, weapons, act, drop)
        holding_drop = movement.startswith("drop-hold")
        state = "idle"
        charging = False
        pushing = False
        if target is not None:
            hp = target.get("hp")
            state = f"fight {target['id']} hp {round(hp) if hp is not None else '?'}"
            charging = self._fight(me, weapons, target, act, mechs)
            escape = None if finishing else self._anti_sandwich_move(me, mechs, obs["zone"])
            if escape is not None:
                act["move"] = escape
                act["boost"] = me.get("energy", 0) >= 30 and not charging
                state += " wedge"
            elif movement in ("zone", "laser hunt", "drop-walk"):
                s_sign = _strafe_sign(now)
                if self._should_push(obs, target):
                    dx, dy = target["pos"][0] - me["pos"][0], target["pos"][1] - me["pos"][1]
                    dist = math.hypot(dx, dy)
                    if dist > 1e-6:
                        push_dir = [dx / dist, dy / dist]
                        act["move"] = self._rotate_move_safe(push_dir, s_sign * DUEL_STRAFE_RAD,
                                                             me["pos"][:2], obs["zone"])
                        act["boost"] = me.get("energy", 0) >= 40 and dist > 80 and not charging
                        pushing = True
                        state += " push"
                elif movement in ("zone", "drop-walk"):
                    act["move"] = self._rotate_move_safe(act["move"], s_sign * DUEL_STRAFE_RAD,
                                                         me["pos"][:2], obs["zone"])
            if (USE_COVER_PEEK and charging and not finishing and not pushing and not holding_drop
                    and escape is None and not movement.startswith("roof") and me.get("in_zone", True)
                    and self._peek_cover(me, weapons, target, obs["zone"], act)):
                state += " peek-c"
            # Point 14: step behind cover while gun is reloading, laser is busy, and target is shooting us.
            elif USE_RELOAD_COVER and not finishing and not pushing and not holding_drop and movement != "roof-climb":
                reloading = any(w and w["kind"] == "gun" and (w.get("reload") or 0) > 0.6 for w in weapons[:2])
                laser_busy = all(not (w and w["kind"] == "laser") or (w.get("cooldown") or 0) > 0.5 for w in weapons[:2])
                hit = self.last_hits.get(target["id"])
                being_shot = hit is not None and now - hit[0] <= 2.0
                if reloading and laser_busy and being_shot and not self._target_blocked(me, target):
                    on_roof = self._current_roof(me["pos"])
                    if on_roof is not None:
                        # On a rooftop, pull back toward roof center instead of walking off the edge.
                        rc = on_roof[1]
                        d = math.dist(me["pos"][:2], rc)
                        if d > 2.0:
                            act["move"] = [(rc[0] - me["pos"][0]) / d, (rc[1] - me["pos"][1]) / d]
                            act["boost"] = False
                            state += " cover"
                    else:
                        spot = self._find_cover(me["pos"][:2], target["pos"][:2], obs["zone"])
                        if spot is not None:
                            d = math.dist(me["pos"][:2], spot)
                            if 2.0 < d <= 40.0:
                                act["move"] = [(spot[0] - me["pos"][0]) / d, (spot[1] - me["pos"][1]) / d]
                                act["boost"] = me.get("energy", 0) >= 30 and d > 10 and not charging
                                state += " cover"
        else:
            if self._shoot_drone(obs, weapons, act):
                state = "drone"
            elif self._shoot_beam_origin(obs, weapons, act):
                state = "beam-ret"
            else:
                self._maybe_early_reload(weapons, act)
                # Point 16: break crates when no mech is within 120 m and nobody hit us in 5 s.
                near_threat = (any(m.get("kind") == "mech" and m.get("pos") and m.get("id") not in self.killed
                                   and math.dist(m["pos"], me["pos"]) <= 120.0 for m in mechs)
                               or (self.last_mech_bearing is not None and now - self.last_mech_bearing[0] <= 5))
                if USE_MORE_CUBES and not near_threat and self._shoot_crate(obs, weapons, act):
                    state = "crate"
                else:
                    bearing = self._face_bearing(mechs, me["pos"], now)
                    if bearing is not None:
                        state = "face"
                        act["aim"] = [bearing, 0.0]
                    elif self._shoot_crate(obs, weapons, act):
                        state = "crate"
                    else:
                        has_laser = any(w and w["kind"] == "laser" for w in weapons[:2])
                        if not has_laser and now < LATE_T:
                            state = "scan"
                            act["aim"] = [(now * 1.2) % math.tau, 0.0]
            if (self.is_finals and me.get("in_zone", True) and not act.get("boost")
                    and drop is None and movement not in ("cube", "roof-climb", "roof-walk")):
                walk = _stat(me.get("stats") or {}, "walk_speed", self.walk_speed)
                if walk > self.step_speed:
                    scale = (self.step_speed - 0.2) / walk
                    mx, my = act["move"]
                    act["move"] = [mx * scale, my * scale]
                    state += " silent"

        # Point 17: head straight into next circle before shrink time runs out.
        z = obs["zone"]
        if USE_ZONE_EARLY and me.get("in_zone", True) and not holding_drop:
            d_next = math.dist(me["pos"][:2], z["next_center"])
            excess = d_next - max(z["next_radius"] - 10.0, 2.0)
            secs_left = (z.get("shrink_end") or now) - now
            speed = _stat(me.get("stats") or {}, "walk_speed", self.walk_speed)
            if excess > 0 and secs_left > 0 and excess / speed > 0.6 * secs_left and d_next > 1e-6:
                act["move"] = [(z["next_center"][0] - me["pos"][0]) / d_next,
                               (z["next_center"][1] - me["pos"][1]) / d_next]
                act["boost"] = me.get("energy", 0) >= 30 and not charging
                state += " zone-run"

        if movement != "roof-climb":
            protect_drop = holding_drop and drop is not None and (drop.get("progress") or 0) >= 2.5
            if not protect_drop:
                dodge_vec, dodge_boost = self._projectile_dodge(
                    obs, ignore_npc=(pushing or holding_drop), ignore_mortar=False)
                if dodge_vec is not None:
                    act["move"] = dodge_vec
                    if dodge_boost and not charging:
                        act["boost"] = True
                    state += " dodge"
                elif not holding_drop and not finishing:
                    l_vec, l_boost = self._laser_sidestep(obs, charging)
                    if l_vec is not None:
                        act["move"] = l_vec
                        if l_boost:
                            act["boost"] = True
                        state += " ldodge"

        if not holding_drop and movement != "roof-climb":
            if USE_WALL_STEER and self._current_roof(me["pos"]) is None:
                act["move"] = self._steer_around_walls(act["move"], me, obs["zone"])
            self._apply_unstick(obs, act, charging)
        # Points 8 & 9: show Finals trip timestamp, HP %, and cube count (<= 80 chars).
        mode_tag = f"FFA@{self.finals_t:.0f}s " if self.is_finals and self.finals_t is not None else ""
        label = (f"{mode_tag}{movement} {state} hp{me['hp'] / me['max_hp']:.0%} c{me.get('cubes', 0)}"
                 + (" chg" if charging else ""))
        mf.draw.label(label[:80])
        return act


if __name__ == "__main__":
    mf.run(Bot)