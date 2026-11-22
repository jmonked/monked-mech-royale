"""CrossHair invariants A-I for the v72 decision kernel (tools/crosshair_mech.py, parity-tested vs the real bot).

Run (asserts mode: the leading asserts are preconditions, any later failing assert is a counterexample):
  crosshair check tools/crosshair_props.py --analysis_kind=asserts --per_condition_timeout=60

All inputs are bounded to game ranges: |move| <= 1, bearings in [-pi, pi], beam offsets within 15 m, next circle
30-400 m with us inside it (the method returns early outside it), one circular obstacle within 60 m.
"""
import math
from typing import List

import crosshair_mech as km

EPS = 1e-9


def _in_range(sx: float, sy: float, ix: float, iy: float, b1: float, b2: float, b3: float, rux: float, rside: float,
              zcx: float, zcy: float, zr: float, ox: float, oy: float, orad: float) -> bool:
    return (all(math.isfinite(v) for v in (sx, sy, ix, iy, b1, b2, b3, rux, rside, zcx, zcy, zr, ox, oy, orad))
            and math.hypot(sx, sy) <= 1.0 and math.hypot(ix, iy) <= 1.0
            and all(-math.pi <= b <= math.pi for b in (b1, b2, b3, rux)) and -15.0 <= rside <= 15.0
            and 30.0 <= zr <= 400.0 and math.hypot(zcx, zcy) <= zr
            and -60.0 <= ox <= 60.0 and -60.0 <= oy <= 60.0 and 0.0 <= orad <= 30.0)


def _same(a: List[float], b: List[float]) -> bool:
    return abs(a[0] - b[0]) <= EPS and abs(a[1] - b[1]) <= EPS


def inv_a_fewer_than_two_threats(sx: float, sy: float, ix: float, iy: float, n: int, b1: float, b2: float, b3: float,
                                 ray_on: bool, rux: float, rside: float, zcx: float, zcy: float, zr: float,
                                 ox: float, oy: float, orad: float) -> None:
    """A: fewer than two credible threats -> exactly v39's move."""
    assert 0 <= n <= 1
    assert _in_range(sx, sy, ix, iy, b1, b2, b3, rux, rside, zcx, zcy, zr, ox, oy, orad)
    out = km.v72_kernel_sym(sx, sy, ix, iy, n, b1, b2, b3, ray_on, rux, rside, zcx, zcy, zr, ox, oy, orad)
    assert out == [sx, sy]


def inv_b_locked(has_target: bool, mv: int, pushing: bool, charging: bool, finishing: bool, holding_drop: bool,
                 in_zone: bool, lock: int, sx: float, sy: float) -> None:
    """B: any emergency token, push, charge, finishing, drop hold, non-zone movement or out of zone -> no aggregate."""
    assert 0 <= mv <= 5 and 0 <= lock <= 6
    assert math.isfinite(sx) and math.isfinite(sy)
    movement = ("zone", "laser hunt", "cube", "drop-walk", "roof-walk", "roof-climb")[mv]
    tokens = frozenset() if lock == 6 else frozenset({sorted(km.LOCK_TOKENS)[lock]})
    locked = (lock != 6 or pushing or charging or finishing or holding_drop or not in_zone or movement != "zone"
              or not has_target)
    eligible = km.v72_gate(has_target, movement, pushing, charging, finishing, holding_drop, in_zone, tokens)
    if locked:
        assert not eligible
        assert km.final_move((sx, sy), None) == [sx, sy]


def inv_c_no_valid_candidate(sx: float, sy: float, ix: float, iy: float, n: int, b1: float, b2: float, b3: float,
                             zcx: float, zcy: float, zr: float, ox: float, oy: float, orad: float) -> None:
    """C: an obstacle that blocks every step from our position -> exactly v39's move (never [0, 0])."""
    assert 2 <= n <= 3
    assert 12.0 <= orad <= 30.0 and math.hypot(ox, oy) <= orad - 9.0
    assert _in_range(sx, sy, ix, iy, b1, b2, b3, 0.0, 0.0, zcx, zcy, zr, ox, oy, orad)
    out = km.v72_kernel_sym(sx, sy, ix, iy, n, b1, b2, b3, False, 0.0, 0.0, zcx, zcy, zr, ox, oy, orad)
    assert out == [sx, sy]


def inv_d_finite_bounded(sx: float, sy: float, ix: float, iy: float, n: int, b1: float, b2: float, b3: float,
                         ray_on: bool, rux: float, rside: float, zcx: float, zcy: float, zr: float,
                         ox: float, oy: float, orad: float) -> None:
    """D: the move is finite and never longer than 1 (nor longer than v39's own move)."""
    assert 0 <= n <= 3
    assert _in_range(sx, sy, ix, iy, b1, b2, b3, rux, rside, zcx, zcy, zr, ox, oy, orad)
    out = km.v72_kernel_sym(sx, sy, ix, iy, n, b1, b2, b3, ray_on, rux, rside, zcx, zcy, zr, ox, oy, orad)
    assert all(math.isfinite(v) for v in out)
    assert math.hypot(*out) <= max(math.hypot(sx, sy), 1e-6 if math.hypot(sx, sy) > 1e-6 else 1.0) + EPS


def inv_e_no_threat_approach(sx: float, sy: float, ix: float, iy: float, n: int, b1: float, b2: float, b3: float,
                             ray_on: bool, rux: float, rside: float, zcx: float, zcy: float, zr: float,
                             ox: float, oy: float, orad: float) -> None:
    """E: when the aggregate overrides v39, it never closes on any active threat (cos <= 0.7, v72's own rule)."""
    assert 2 <= n <= 3
    assert _in_range(sx, sy, ix, iy, b1, b2, b3, rux, rside, zcx, zcy, zr, ox, oy, orad)
    out = km.v72_kernel_sym(sx, sy, ix, iy, n, b1, b2, b3, ray_on, rux, rside, zcx, zcy, zr, ox, oy, orad)
    if not _same(out, [sx, sy]):
        L = math.hypot(*out)
        for b in (b1, b2, b3)[:n]:
            assert (out[0] * math.cos(b) + out[1] * math.sin(b)) / L <= 0.7 + 1e-9


def inv_f_beam_safety(sx: float, sy: float, ix: float, iy: float, n: int, b1: float, b2: float, b3: float,
                      rux: float, rside: float, zcx: float, zcy: float, zr: float,
                      ox: float, oy: float, orad: float) -> None:
    """F: if v39's step avoids a live beam strip, the aggregate's step does not touch it either."""
    assert 2 <= n <= 3
    assert _in_range(sx, sy, ix, iy, b1, b2, b3, rux, rside, zcx, zcy, zr, ox, oy, orad)
    assert not km.beams_entered([(math.cos(rux), math.sin(rux), rside)], sx, sy, 3.5)   # precondition (leading)
    out = km.v72_kernel_sym(sx, sy, ix, iy, n, b1, b2, b3, True, rux, rside, zcx, zcy, zr, ox, oy, orad)
    assert not km.beams_entered([(math.cos(rux), math.sin(rux), rside)], out[0], out[1], 3.5)


def inv_g_zone(sx: float, sy: float, ix: float, iy: float, n: int, b1: float, b2: float, b3: float,
               ray_on: bool, rux: float, rside: float, zcx: float, zcy: float, zr: float,
               ox: float, oy: float, orad: float) -> None:
    """G: an aggregate override always ends its 5 m probe inside the next circle."""
    assert 2 <= n <= 3
    assert _in_range(sx, sy, ix, iy, b1, b2, b3, rux, rside, zcx, zcy, zr, ox, oy, orad)
    out = km.v72_kernel_sym(sx, sy, ix, iy, n, b1, b2, b3, ray_on, rux, rside, zcx, zcy, zr, ox, oy, orad)
    if not _same(out, [sx, sy]):
        L = math.hypot(*out)
        assert math.hypot(5.0 * out[0] / L - zcx, 5.0 * out[1] / L - zcy) <= zr + 1e-9


def inv_h_threat_order(sx: float, sy: float, ix: float, iy: float, n: int, b1: float, b2: float, b3: float,
                       ray_on: bool, rux: float, rside: float, zcx: float, zcy: float, zr: float,
                       ox: float, oy: float, orad: float) -> None:
    """H: reordering the same threats does not change the decision (beyond float noise)."""
    assert 2 <= n <= 3
    assert _in_range(sx, sy, ix, iy, b1, b2, b3, rux, rside, zcx, zcy, zr, ox, oy, orad)
    a = km.v72_kernel_sym(sx, sy, ix, iy, n, b1, b2, b3, ray_on, rux, rside, zcx, zcy, zr, ox, oy, orad)
    b = km.v72_kernel_sym(sx, sy, ix, iy, n, b2, b1, b3, ray_on, rux, rside, zcx, zcy, zr, ox, oy, orad)
    assert abs(a[0] - b[0]) <= 1e-6 and abs(a[1] - b[1]) <= 1e-6


def inv_i_duplicate_ids(mid: int, other: int, age1: float, age2: float, bear1: float, bear2: float, dup: bool) -> None:
    """I: the same mech id reported twice never counts as two threats."""
    assert 0 <= mid < 16 and 0 <= other < 16 and mid != other and mid != 0 and other != 0
    assert 0.0 <= age1 <= 2.9 and 0.0 <= age2 <= 2.9
    assert -math.pi <= bear1 <= math.pi and -math.pi <= bear2 <= math.pi
    hits = [(mid, 100.0 - age1, bear1), (mid if dup else other, 100.0 - age2, bear2)]
    sources, _ = km.v72_classify(0, 100.0, 0.0, 0.0, 0.0, frozenset(), hits, [], 5.5, 4.5, 7.0, 280.0)
    assert len(sources) == (1 if dup else 2)


# ---------------------------------------------------------------- diffbehavior wrappers (same signatures)
def stock_identity(sx: float, sy: float, ix: float, iy: float, n: int, b1: float, b2: float, b3: float) -> List[float]:
    a = _bounded(sx, sy, ix, iy, n, b1, b2, b3, 0.0, 0.0, 0.0, 0.0, 300.0, 0.0, 0.0, 0.0)
    return [a[0], a[1]]


def v72_outside_activation(sx: float, sy: float, ix: float, iy: float, n: int, b1: float, b2: float,
                           b3: float) -> List[float]:
    """Domain where v72 must be inert: at most one credible threat (n clipped), no beam, open map."""
    a = _bounded(sx, sy, ix, iy, n, b1, b2, b3, 0.0, 0.0, 0.0, 0.0, 300.0, 0.0, 0.0, 0.0)
    return km.v72_kernel_sym(a[0], a[1], a[2], a[3], min(a[4], 1), a[5], a[6], a[7], False, 0.0, 0.0, 0.0, 0.0, 300.0,
                             0.0, 0.0, 0.0)


def v72_locked(sx: float, sy: float, ix: float, iy: float, n: int, b1: float, b2: float, b3: float) -> List[float]:
    """Domain where an emergency owns movement (lock token present): the gate refuses, v39's move stays."""
    tok = frozenset({sorted(km.LOCK_TOKENS)[abs(n) % len(km.LOCK_TOKENS)]})
    chosen = (km.v72_kernel_sym(sx, sy, ix, iy, 3, b1, b2, b3, False, 0.0, 0.0, 0.0, 0.0, 300.0, 0.0, 0.0, 0.0)
              if km.v72_gate(True, "zone", False, False, False, False, True, tok) else None)
    return [sx, sy] if chosen is None else chosen


def _clamp(v: float, lo: float, hi: float) -> float:
    return lo if not math.isfinite(v) else max(lo, min(hi, v))


def _bounded(sx, sy, ix, iy, n, b1, b2, b3, rux, rside, zcx, zcy, zr, ox, oy, orad):
    sx, sy, ix, iy = (_clamp(v, -1.0, 1.0) for v in (sx, sy, ix, iy))
    s = math.hypot(sx, sy)
    if s > 1.0:
        sx, sy = sx / s, sy / s
    s = math.hypot(ix, iy)
    if s > 1.0:
        ix, iy = ix / s, iy / s
    b1, b2, b3, rux = (_clamp(v, -math.pi, math.pi) for v in (b1, b2, b3, rux))
    zr = _clamp(zr, 30.0, 400.0)
    zcx, zcy = _clamp(zcx, -zr, zr), _clamp(zcy, -zr, zr)
    if math.hypot(zcx, zcy) > zr:
        zcx, zcy = 0.0, 0.0
    return (sx, sy, ix, iy, min(max(n, 0), 3), b1, b2, b3, rux, _clamp(rside, -15.0, 15.0), zcx, zcy, zr,
            _clamp(ox, -60.0, 60.0), _clamp(oy, -60.0, 60.0), _clamp(orad, 0.0, 30.0))


def v62_bounded(sx: float, sy: float, ix: float, iy: float, n: int, b1: float, b2: float, b3: float, ray_on: bool,
                rux: float, rside: float, zcx: float, zcy: float, zr: float, ox: float, oy: float,
                orad: float) -> List[float]:
    a = _bounded(sx, sy, ix, iy, n, b1, b2, b3, rux, rside, zcx, zcy, zr, ox, oy, orad)
    return [round(v, 9) for v in km.v62_kernel_sym(*a[:8], ray_on, *a[8:])]


def v72_bounded(sx: float, sy: float, ix: float, iy: float, n: int, b1: float, b2: float, b3: float, ray_on: bool,
                rux: float, rside: float, zcx: float, zcy: float, zr: float, ox: float, oy: float,
                orad: float) -> List[float]:
    a = _bounded(sx, sy, ix, iy, n, b1, b2, b3, rux, rside, zcx, zcy, zr, ox, oy, orad)
    return [round(v, 9) for v in km.v72_kernel_sym(*a[:8], ray_on, *a[8:])]
