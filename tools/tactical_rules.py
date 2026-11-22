"""Conservative tactical classification of a base-vs-candidate action pair on one scenario.

Only strong safety violations are CATASTROPHIC. "Safer"/"worse" need a concrete geometric reason that a single
static observation can prove; everything else that differs is UNCERTAIN. No scores, no weights.

Rules (candidate compared with base on the same scenario):
  C1 emergency-override    base chose an emergency move (dodge, ldodge, wedge, tp-cover, cover, zone-run) and the
                           candidate replaced it without choosing that same emergency itself
  C2 toward-crossfire      2+ active attackers and the candidate walks straight at 2+ of them (cos > 0.7) when the
                           base did not
  C3 stall-under-crossfire 2+ active attackers, candidate |move| < 0.2 while base |move| >= 0.5 (not holding a drop)
  C4 into-laser-line       a visible charging mech with clear line of sight aimed at us; the candidate's 5 m step ends inside its beam
                           width while the base's ends outside
  C5 leaves-zone           we are inside the next circle and the candidate's 5 m step leaves it while the base's
                           does not
  C6 boost-into-wall       candidate boosts along a 5 m step blocked by a building while the base's step is clear
Safer (inverse proofs): candidate exits a beam line the base stays in; avoids walking at 2+ attackers the base walks
at; stays in the next circle when the base leaves it. Worse (non-catastrophic): candidate walks straight at one
active attacker (cos > 0.7) when the base does not.
"""
import math

EMERGENCY = ("dodge", "ldodge", "wedge", "tp-cover", "cover", "zone-run")
STEP = 5.0


def _unit(v):
    n = math.hypot(v[0], v[1]) if v else 0.0
    return (v[0] / n, v[1] / n, n) if n > 1e-9 else (0.0, 0.0, 0.0)


def attackers(sc, bot):
    """Active attacker unit vectors (from us), by mech id: recent hit within 3 s; visible position preferred."""
    obs = sc["obs"]
    me = obs["self"]
    t = obs["t"]
    x, y = me["pos"][0], me["pos"][1]
    vis = {m["id"]: m for m in obs.get("mechs") or [] if m.get("kind") == "mech" and m.get("pos")}
    out = {}
    for k, v in (getattr(bot, "last_hits", {}) or {}).items():
        if not (isinstance(k, int) and 0 <= k < 16) or k == me.get("id") or t - v[0] > 3.0:
            continue
        if k in vis:
            ang = math.atan2(vis[k]["pos"][1] - y, vis[k]["pos"][0] - x)
        elif v[1] is not None:
            ang = v[1]
        else:
            continue
        out[k] = (math.cos(ang), math.sin(ang))
    return out


def beams(sc, bot):
    """Charging visible mechs whose aim line covers us: (ux, uy, side_offset_now, width)."""
    obs = sc["obs"]
    me = obs["self"]
    x, y = me["pos"][0], me["pos"][1]
    scale = bot._scale(me) if hasattr(bot, "_scale") else 1.0
    width = getattr(bot, "mech_radius", 2.5) * scale + 1.0
    out = []
    for m in obs.get("mechs") or []:
        aim = m.get("aim")
        if m.get("kind") != "mech" or not m.get("charging") or not m.get("pos") or not aim or aim[0] is None:
            continue
        ux, uy = math.cos(aim[0]), math.sin(aim[0])
        dx, dy = x - m["pos"][0], y - m["pos"][1]
        if ux * dx + uy * dy <= 0:
            continue
        if hasattr(bot, "_target_blocked") and bot._target_blocked(me, m):
            continue   # a building stops the beam: not a live line
        side = ux * dy - uy * dx
        if abs(side) < width + STEP:
            out.append((ux, uy, side, width))
    return out


def _in_beam(b, vx, vy):
    ux, uy, side, width = b
    return abs(side + STEP * (ux * vy - uy * vx)) < width


def classify(sc, bot, base, cand):
    """bot: a base Bot instance restored to the scenario state (for geometry + memory). Returns (verdict, reasons)."""
    ab, ac = base["action"], cand["action"]
    if ab == ac:
        return "identical", []
    obs = sc["obs"]
    me = obs["self"]
    x, y, z = me["pos"]
    bm, cm = ab.get("move") or [0.0, 0.0], ac.get("move") or [0.0, 0.0]
    bx, by, bn = _unit(bm)
    cx, cy, cn = _unit(cm)
    btoks, ctoks = set(base["label"].split()), set(cand["label"].split())
    cat, safer, worse = [], [], []
    move_changed = bm != cm

    for tok in EMERGENCY:
        if tok in btoks and move_changed and tok not in ctoks:
            cat.append(f"C1 overrode {tok}")

    att = attackers(sc, bot)
    if len(att) >= 2:
        b_at = sum(1 for u in att.values() if bn and bx * u[0] + by * u[1] > 0.7)
        c_at = sum(1 for u in att.values() if cn and cx * u[0] + cy * u[1] > 0.7)
        if c_at >= 2 and b_at < 2:
            cat.append("C2 walks at 2+ attackers")
        elif b_at >= 2 and c_at < 2:
            safer.append("avoids walking at 2+ attackers")
        holding = "drop-hold" in ctoks
        if cn < 0.2 and bn >= 0.5 and not holding:
            cat.append("C3 stalls under crossfire")
    if att:
        b_one = any(bn and bx * u[0] + by * u[1] > 0.7 for u in att.values())
        c_one = any(cn and cx * u[0] + cy * u[1] > 0.7 for u in att.values())
        if c_one and not b_one and "C2 walks at 2+ attackers" not in cat:
            worse.append("walks straight at an active attacker")

    for b in beams(sc, bot):
        b_in = _in_beam(b, bx * min(bn, 1.0), by * min(bn, 1.0))
        c_in = _in_beam(b, cx * min(cn, 1.0), cy * min(cn, 1.0))
        if c_in and not b_in:
            cat.append("C4 steps into live laser line")
        elif b_in and not c_in:
            safer.append("steps out of live laser line")

    zone = obs.get("zone") or {}
    if zone.get("next_center") is not None and zone.get("next_radius") is not None:
        ncx, ncy = zone["next_center"]
        r = zone["next_radius"]
        if math.hypot(x - ncx, y - ncy) <= r:
            b_out = math.hypot(x + STEP * bx * min(bn, 1) - ncx, y + STEP * by * min(bn, 1) - ncy) > r
            c_out = math.hypot(x + STEP * cx * min(cn, 1) - ncx, y + STEP * cy * min(cn, 1) - ncy) > r
            if c_out and not b_out:
                cat.append("C5 leaves next circle")
            elif b_out and not c_out:
                safer.append("stays in next circle")

    if ac.get("boost") and cn and hasattr(bot, "_building_blocked"):
        c_blk = bot._building_blocked((x, y, z + 1.3), (x + STEP * cx, y + STEP * cy, z + 1.3))
        b_blk = bn and bot._building_blocked((x, y, z + 1.3), (x + STEP * bx, y + STEP * by, z + 1.3))
        if c_blk and not b_blk:
            cat.append("C6 boosts into a wall")

    if cat:
        return "catastrophic", cat
    if safer and not worse:
        return "safer", safer
    if worse and not safer:
        return "worse", worse
    return "uncertain", safer + worse
