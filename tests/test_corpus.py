"""Persistent scenario corpus checks (experiments/corpus).

* fidelity: every harvested scenario recorded from the base still reproduces its recorded action exactly
  (guards the lab itself and accidental base drift).
* candidate: zero catastrophic regressions on any corpus category, including the permanent regression set.
"""
import pytest

import scenario_lab as lab
import tactical_rules as rules
from conftest import BASE, CANDIDATE


@pytest.mark.parametrize("cat", lab.CATEGORIES)
def test_replay_fidelity(cat):
    scs = [s for s in lab.load_corpus([cat]) if s.get("expect")]
    if not scs:
        pytest.skip("no recorded scenarios")
    bad = []
    for s in scs:
        r = lab.runner(s["expect"]["ref"]).run(s)
        if r["action"] != s["expect"]["action"]:
            bad.append(s["name"])
    assert not bad, f"{len(bad)}/{len(scs)} drifted, e.g. {bad[:3]}"


@pytest.mark.skipif(not CANDIDATE, reason="MONKED_CANDIDATE not set")
@pytest.mark.parametrize("cat", lab.CATEGORIES)
def test_candidate_no_catastrophe(cat):
    scs = lab.load_corpus([cat])
    if not scs:
        pytest.skip("empty category")
    bad = []
    for s in scs:
        rb = lab.runner(BASE).run(s)
        rc = lab.runner(CANDIDATE).run(s)
        verdict, reasons = rules.classify(s, rb["bot"], rb, rc)
        if verdict == "catastrophic":
            bad.append((s["name"], reasons))
    assert not bad, f"{len(bad)} catastrophic, e.g. {bad[:3]}"
