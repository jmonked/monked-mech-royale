"""Hypothesis property tests on semantically generated combat states (real Bot.act, flat world).

Base properties (always): the bot answers every family of tactical state with a well-formed action in time.
Candidate properties (MONKED_CANDIDATE set): no catastrophic regression vs base (tools/tactical_rules.py), and every
emergency move the base chose (dodge, laser sidestep, wedge, tp-cover, reload cover, zone-run) is preserved.
"""
import math

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

import combat_strategies as cs
import scenario_lab as lab
import tactical_rules as rules
from conftest import BASE, CANDIDATE, EXAMPLES, save_found

SET = settings(max_examples=EXAMPLES, deadline=None, derandomize=True, database=None,
               suppress_health_check=[HealthCheck.too_slow, HealthCheck.data_too_large, HealthCheck.filter_too_much])


def assert_valid(act, obs, ms):
    assert act.get("tick") == obs["tick"], "tick echo"
    mv = act.get("move")
    assert isinstance(mv, list) and len(mv) == 2 and all(math.isfinite(v) for v in mv), f"move {mv}"
    assert math.hypot(*mv) <= 1.0 + 1e-6, f"move norm {mv}"
    aim = act.get("aim")
    assert isinstance(aim, list) and len(aim) == 2 and all(math.isfinite(v) for v in aim), f"aim {aim}"
    fire = act.get("fire", [False, False])
    assert isinstance(fire, list) and len(fire) == 2 and all(isinstance(f, bool) for f in fire), f"fire {fire}"
    for k in ("boost", "jump", "reload"):
        if k in act:
            assert isinstance(act[k], bool), f"{k} {act[k]}"
    # Real latency is gated by check.py (p99 < 10 ms, max < 50 ms). Under pytest -n auto every core is busy and the OS
    # can deschedule a worker mid-decision, so here we only catch pathological loops.
    assert ms < 250.0, f"decision took {ms:.1f} ms"


@pytest.mark.parametrize("family", cs.FAMILIES)
@SET
@given(data=st.data())
def test_base_valid_action(family, data):
    sc = data.draw(cs.combat(family))
    r = lab.runner(BASE).run(sc)
    assert_valid(r["action"], sc["obs"], r["ms"])


needs_candidate = pytest.mark.skipif(not CANDIDATE, reason="MONKED_CANDIDATE not set")


@needs_candidate
@pytest.mark.parametrize("family", cs.FAMILIES)
@SET
@given(data=st.data())
def test_candidate_valid_and_safe(family, data):
    sc = data.draw(cs.combat(family))
    rb = lab.runner(BASE).run(sc)
    rc = lab.runner(CANDIDATE).run(sc)
    assert_valid(rc["action"], sc["obs"], rc["ms"])
    verdict, reasons = rules.classify(sc, rb["bot"], rb, rc)
    if verdict == "catastrophic":
        save_found(f"hyp-{family}", sc, reasons)
    assert verdict != "catastrophic", f"{reasons} base={rb['label']} cand={rc['label']}"
