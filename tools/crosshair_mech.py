"""Pure, typed decision kernels for CrossHair (tooling only; never imported by the bot).

Traceable line-for-line to v72 `_aggregate_threat_move` and its gate in `_act`
(commit 076094fbd128c8df846b695d5f24c3ec84d35767, example_bot.py) and, for comparison, to v62
(a023e35a15df4f425691bb2c8fdee257063e78a3). tests/test_crosshair_parity.py proves the v72 kernel returns the
same decision as the real method on every corpus state where the real method runs.

No I/O, no git, no draw calls. Geometry predicates (buildings) are passed in as callables for parity; the
symbolic wrappers (`*_sym`) replace them with one circular obstacle so CrossHair can search.
"""
import math
from typing import Callable, Dict, FrozenSet, List, Optional, Sequence, Tuple

THREAT_RECENT_S = 3.0
LOCK_TOKENS = frozenset({"wedge", "tp-cover", "cover", "dodge", "ldodge", "zone-run"})
Vec = Tuple[float, float]
Ray = Tuple[float, float, float]                 # (ux, uy, side) of a live charging beam near us
Blocked = Callable[[float, float, float, float], bool]   # segment (ax, ay) -> (bx, by) hits a building


# ---------------------------------------------------------------- gate (v72 _act)
def v72_gate(has_target: bool, movement: str, pushing: bool, charging: bool, finishing: bool, holding_drop: bool,
             in_zone: bool, tokens: FrozenSet[str]) -> bool:
    """example_bot.py _act: eligibility before calling _aggregate_threat_move."""
    return (has_target and movement == "zone" and not pushing and not charging and not finishing
            and not holding_drop and in_zone and not (LOCK_TOKENS & tokens))


def v72_prechecks(on_roof: bool, unstick_active: bool, x: float, y: float, zc: Vec, zr: float,
                  hist_age: float, hist_disp: float) -> bool:
    """First lines of _aggregate_threat_move. True = may continue. hist_*: oldest pos_history entry <= 0.65 s."""
    if on_roof or unstick_active:
        return False
    if math.hypot(x - zc[0], y - zc[1]) > zr:
        return False
    if hist_age >= 0.45 and hist_disp < 1.5:
        return False
    return True


# ---------------------------------------------------------------- threat classification
def v72_classify(my_id: int, now: float, x: float, y: float, z: float, killed: FrozenSet[int],
                 hits: Sequence[Tuple[int, float, Optional[float]]],
                 mechs: Sequence[Tuple[int, float, float, float, Optional[float], float, bool, bool, float]],
                 width: float, half_h: float, muzzle_h: float, laser_range: float
                 ) -> Tuple[Dict[int, float], List[Ray]]:
    """hits: (id, t_hit, bearing|None). mechs (visible kind=='mech'): (id, mx, my, mz, aim_yaw|None, aim_pitch,
    charging, los_blocked, scale). Returns (sources id->bearing to threat, rays). Duplicates collapse by id."""
    sources: Dict[int, float] = {}
    for mid, t_hit, bearing in hits:
        if 0 <= mid < 16 and mid != my_id and mid not in killed and now - t_hit <= THREAT_RECENT_S and bearing is not None:
            sources[mid] = bearing
    rays: List[Ray] = []
    for mid, mx, my, mz, ayaw, apitch, charging, blocked, mscale in mechs:
        if mid in killed or mid == my_id:
            continue
        dx, dy = x - mx, y - my
        dist = math.hypot(dx, dy)
        if dist < 1e-6:
            continue
        to_mech = math.atan2(-dy, -dx)
        if mid in sources:
            sources[mid] = to_mech
        if ayaw is None:
            continue
        yaw_err = abs(math.remainder(ayaw - math.atan2(dy, dx), math.tau))
        if charging and dist <= laser_range:
            ux, uy = math.cos(ayaw), math.sin(ayaw)
            along = ux * dx + uy * dy
            side = ux * dy - uy * dx
            beam_z = mz + muzzle_h * mscale + along * math.tan(apitch or 0.0)
            if along > 0 and abs(side) < width + 6.0 and abs(beam_z - (z + half_h)) < half_h + 3.0 and not blocked:
                rays.append((ux, uy, side))
                if abs(side) < width:
                    sources[mid] = to_mech
                    continue
        if dist <= 120.0 and yaw_err <= math.radians(5) and not blocked:
            sources[mid] = to_mech
    return sources, rays


# ---------------------------------------------------------------- selection (v72)
def v72_scores(units: Sequence[Vec], rays: Sequence[Ray], stock: Vec, intended: Vec, width: float):
    """(away, stock_score, cands[(score, vx, vy)]) exactly as v72 computes them."""
    sx, sy = sum(u[0] for u in units), sum(u[1] for u in units)
    if math.hypot(sx, sy) < 0.3 * len(units):
        away = math.atan2(stock[1], stock[0]) if math.hypot(*stock) > 1e-6 else 0.0
    else:
        away = math.atan2(-sy, -sx)
    il = math.hypot(*intended)
    iv = (intended[0] / il, intended[1] / il) if il > 1e-6 else (0.0, 0.0)

    def score(vx: float, vy: float) -> float:
        per = []
        for ux, uy in units:
            radial = vx * ux + vy * uy
            per.append(abs(vx * uy - vy * ux) - 0.6 * max(0.0, radial) + 0.15 * max(0.0, -radial))
        s = 0.5 * (min(per) + sum(per) / len(per)) + 0.2 * (vx * iv[0] + vy * iv[1])
        for ux, uy, side in rays:
            lateral = side + 5.0 * (ux * vy - uy * vx)
            s -= 2.0 * max(0.0, 1.0 - abs(lateral) / width)
        return s

    sl = math.hypot(*stock)
    stock_score = score(stock[0] / sl, stock[1] / sl) if sl > 1e-6 else score(0.0, 0.0)
    cands = []
    for i in range(8):
        ang = away + i * math.pi / 4
        vx, vy = math.cos(ang), math.sin(ang)
        cands.append((score(vx, vy), vx, vy))
    if il > 1e-6:
        cands.append((score(*iv), iv[0], iv[1]))
    return away, stock_score, cands


def beams_entered(rays: Sequence[Ray], vx: float, vy: float, hard: float) -> FrozenSet[int]:
    out = set()
    for i, (ux, uy, side) in enumerate(rays):
        end = side + 5.0 * (ux * vy - uy * vx)
        if abs(side) < hard or abs(end) < hard or (side > 0) != (end > 0):
            out.add(i)
    return frozenset(out)


def v72_select(x: float, y: float, stock: Vec, intended: Vec, units: Sequence[Vec], rays: Sequence[Ray],
               zc: Vec, zr: float, width: float, hard: float, body: float,
               point_blocked: Callable[[float, float], bool], blocked: Blocked) -> Optional[List[float]]:
    """Candidate loop of _aggregate_threat_move. None = keep v39's move."""
    if len(units) < 2:
        return None
    _away, stock_score, cands = v72_scores(units, rays, stock, intended, width)
    stock_beams = beams_entered(rays, stock[0], stock[1], hard)
    sl = math.hypot(*stock)
    speed = sl if sl > 1e-6 else 1.0
    for s, vx, vy in sorted(cands, reverse=True):
        if s < stock_score + 0.15:
            return None
        if max(vx * ux + vy * uy for ux, uy in units) > 0.7:
            continue
        tx, ty = x + 5.0 * vx, y + 5.0 * vy
        if math.hypot(tx - zc[0], ty - zc[1]) > zr or not beams_entered(rays, speed * vx, speed * vy, hard) <= stock_beams:
            continue
        fx, fy = x + (5.0 + body) * vx, y + (5.0 + body) * vy
        if point_blocked(tx, ty) or any(blocked(x + o * -vy, y + o * vx, fx + o * -vy, fy + o * vx)
                                        for o in (0.0, body, -body)):
            continue
        return [speed * vx, speed * vy]
    return None


def final_move(stock: Vec, chosen: Optional[List[float]]) -> List[float]:
    """_act: act['move'] = aggregate if aggregate is not None (else v39's move stays)."""
    return list(chosen) if chosen is not None else [stock[0], stock[1]]


# ---------------------------------------------------------------- v62 (reference only)
def v62_select(x: float, y: float, stock: Vec, intended: Vec, units: Sequence[Vec],
               rays5: Sequence[Tuple[float, float, float, float, float]], zc: Vec, zr: float, width: float,
               height: float, point_blocked: Callable[[float, float], bool], blocked: Blocked) -> Optional[List[float]]:
    """v62 candidate loop (a023e35): separation score, stock + intended + 8 probes (+ inward), [0,0] when all fail."""
    if len(units) < 2:
        return None
    sx, sy = sum(u[0] for u in units), sum(u[1] for u in units)
    if math.hypot(sx, sy) < 1e-6:
        sx, sy = units[0]
    away = math.atan2(-sy, -sx)
    speed = math.hypot(*stock) or 1.0
    candidates = [tuple(stock), tuple(intended)]
    for i in range(8):
        a = away + i * math.pi / 4
        candidates.append((speed * math.cos(a), speed * math.sin(a)))
    distance = math.hypot(x - zc[0], y - zc[1])
    zone_limit = max(zr, distance)
    if distance > zr:
        candidates.append((speed * (zc[0] - x) / distance, speed * (zc[1] - y) / distance))
    ranked = []
    for vx, vy in candidates:
        dx, dy = 5.0 * vx, 5.0 * vy
        tx, ty = x + dx, y + dy
        if math.hypot(tx - zc[0], ty - zc[1]) > zone_limit:
            continue
        separation = [-(vx * ux + vy * uy) for ux, uy in units]
        score = 0.5 * (min(separation) + sum(separation) / len(separation))
        score += 0.2 * (vx * intended[0] + vy * intended[1])
        if rays5:
            exposure = []
            for ux, uy, side, vertical, rise in rays5:
                lateral_step = ux * dy - uy * dx
                vertical_step = (ux * dx + uy * dy) * rise
                for fraction in (0.5, 1.0):
                    miss = max(abs(side + fraction * lateral_step) / width, abs(vertical + fraction * vertical_step) / height)
                    exposure.append(max(0.0, 1.0 - miss))
            score -= 2.0 * (max(exposure) + sum(exposure) / len(exposure))
        ranked.append((score, vx, vy, tx, ty))
    for _, vx, vy, tx, ty in sorted(ranked, key=lambda p: p[0], reverse=True):
        if not point_blocked(tx, ty) and not blocked(x, y, tx, ty):
            return [vx, vy]
    return [0.0, 0.0]


# ---------------------------------------------------------------- symbolic wrappers (bounded game ranges)
def _circle_blocker(ox: float, oy: float, orad: float):
    def seg_hits(ax: float, ay: float, bx: float, by: float) -> bool:
        if orad <= 0:
            return False
        dx, dy = bx - ax, by - ay
        L = dx * dx + dy * dy
        t = 0.0 if L <= 1e-12 else max(0.0, min(1.0, ((ox - ax) * dx + (oy - ay) * dy) / L))
        return math.hypot(ax + t * dx - ox, ay + t * dy - oy) < orad

    def point(px: float, py: float) -> bool:
        return orad > 0 and math.hypot(px - ox, py - oy) < orad
    return point, seg_hits


def _units(b1: float, b2: float, b3: float, n: int) -> List[Vec]:
    return [(math.cos(b), math.sin(b)) for b in (b1, b2, b3)[:n]]


def v72_kernel_sym(sx: float, sy: float, ix: float, iy: float, n: int, b1: float, b2: float, b3: float,
                   ray_on: bool, rux_ang: float, rside: float, zcx: float, zcy: float, zr: float,
                   ox: float, oy: float, orad: float) -> List[float]:
    """Symbolic v72 decision with us at the origin: stock move, intended move, n<=3 threat bearings, one optional
    live beam (direction angle, side offset), next circle, one circular obstacle. Returns the final move."""
    pb, bl = _circle_blocker(ox, oy, orad)
    rays = [(math.cos(rux_ang), math.sin(rux_ang), rside)] if ray_on else []
    chosen = v72_select(0.0, 0.0, (sx, sy), (ix, iy), _units(b1, b2, b3, n), rays, (zcx, zcy), zr,
                        width=5.5, hard=3.5, body=2.5, point_blocked=pb, blocked=bl)
    return final_move((sx, sy), chosen)


def v62_kernel_sym(sx: float, sy: float, ix: float, iy: float, n: int, b1: float, b2: float, b3: float,
                   ray_on: bool, rux_ang: float, rside: float, zcx: float, zcy: float, zr: float,
                   ox: float, oy: float, orad: float) -> List[float]:
    """Same inputs through v62's candidate loop (beam assumed at body height)."""
    pb, bl = _circle_blocker(ox, oy, orad)
    rays5 = [(math.cos(rux_ang), math.sin(rux_ang), rside, 0.0, 0.0)] if ray_on and abs(rside) < 5.5 else []
    chosen = v62_select(0.0, 0.0, (sx, sy), (ix, iy), _units(b1, b2, b3, n), rays5, (zcx, zcy), zr,
                        width=5.5, height=5.5, point_blocked=pb, blocked=bl)
    return final_move((sx, sy), chosen)


# ---------------------------------------------------------------- extraction from a live bot (parity only)
def extract(bot, obs, intended, stock):
    """Build the kernel inputs from the real bot at the moment _aggregate_threat_move is called."""
    me = obs["self"]
    now = obs["t"]
    x, y, z = me["pos"]
    scale = bot._scale(me)
    width = bot.mech_radius * scale + 3.0
    half_h = bot.half_height * scale
    laser_range = (bot.laser or {}).get("range", 280.0) if isinstance(bot.laser, dict) else 280.0
    hist = [p for p in bot.pos_history if now - p[0] <= 0.65] + [(now, x, y)]
    pre = dict(on_roof=bot._current_roof(me["pos"]) is not None, unstick_active=now < bot.unstick_until, x=x, y=y,
               zc=tuple(obs["zone"]["next_center"]), zr=obs["zone"]["next_radius"],
               hist_age=now - hist[0][0], hist_disp=math.hypot(x - hist[0][1], y - hist[0][2]))
    hits = [(mid, v[0], v[1]) for mid, v in bot.last_hits.items() if isinstance(mid, int)]
    mechs = []
    for m in obs.get("mechs") or []:
        if m.get("kind") != "mech" or not m.get("pos"):
            continue
        aim = m.get("aim")
        mechs.append((m.get("id"), *m["pos"], aim[0] if aim else None, (aim[1] if aim else 0.0) or 0.0,
                      bool(m.get("charging")), bot._target_blocked(me, m), bot._scale(m)))
    cls = dict(my_id=me.get("id"), now=now, x=x, y=y, z=z, killed=frozenset(bot.killed), hits=hits, mechs=mechs,
               width=width, half_h=half_h, muzzle_h=bot.muzzle_height, laser_range=laser_range)
    body = bot.mech_radius * scale
    sel = dict(x=x, y=y, stock=tuple(stock), intended=tuple(intended), zc=tuple(obs["zone"]["next_center"]),
               zr=obs["zone"]["next_radius"], width=width, hard=bot.mech_radius * scale + 1.0, body=body,
               point_blocked=lambda px, py: bot._point_blocked_2d(px, py, z),
               blocked=lambda ax, ay, bx, by: bot._building_blocked((ax, ay, z + 1.2), (bx, by, z + 1.2)))
    return pre, cls, sel


def kernel_decision(pre, cls, sel) -> Optional[List[float]]:
    if not v72_prechecks(**pre):
        return None
    sources, rays = v72_classify(**cls)
    units = [(math.cos(b), math.sin(b)) for b in sources.values()]
    return v72_select(units=units, rays=rays, **sel)
