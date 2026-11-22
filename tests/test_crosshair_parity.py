"""Parity: the pure v72 kernel (tools/crosshair_mech.py) makes the same decision as the real
`_aggregate_threat_move` on every corpus state where v72 calls it. If this fails, CrossHair results on the kernel
say nothing about the bot."""
import os

import pytest

import crosshair_mech as km
import scenario_lab as lab

V72 = os.environ.get("MONKED_V72", "076094fbd128c8df846b695d5f24c3ec84d35767")


def _close(a, b):
    if a is None or b is None:
        return a is None and b is None
    return max(abs(a[0] - b[0]), abs(a[1] - b[1])) <= 1e-12


def _calls(scs):
    rn = lab.runner(V72)
    out = []
    for sc in scs:
        b = rn.new_bot(sc.get("state"), sc.get("flat", False))
        orig = b._aggregate_threat_move

        def spy(obs, intended, stock, _b=b, _orig=orig):
            res = _orig(obs, intended, stock)
            out.append((sc["name"], km.kernel_decision(*km.extract(_b, obs, intended, stock)), res))
            return res
        b._aggregate_threat_move = spy
        rn.run(sc, bot=b)
    return out


@pytest.mark.parametrize("cat", lab.CATEGORIES)
def test_kernel_matches_real_v72(cat):
    calls = _calls(lab.load_corpus([cat]))
    if not calls:
        pytest.skip("aggregate never called in this category")
    bad = [(n, k, r) for n, k, r in calls if not _close(k, r)]
    assert not bad, f"{len(bad)}/{len(calls)} mismatches, e.g. {bad[:3]}"


def test_gate_matches_real_v72():
    """v72_gate (+ prechecks inside the method) predicts exactly when the real bot calls the aggregate."""
    rn = lab.runner(V72)
    bad, n = [], 0
    for sc in lab.load_corpus():
        b = rn.new_bot(sc.get("state"), sc.get("flat", False))
        called = []
        orig = b._aggregate_threat_move
        b._aggregate_threat_move = lambda o, i, s, _o=orig: (called.append(1), _o(o, i, s))[1]
        r = rn.run(sc, bot=b)
        label = r["label"]
        if label.startswith("FFA@"):
            label = label.split(" ", 1)[1]
        toks = frozenset(label.split()) - {"aggregate"}
        me = sc["obs"]["self"]
        tgt = next((m for m in sc["obs"].get("mechs") or [] if m.get("id") == b.target_id), None)
        finishing = bool(tgt and tgt.get("hp") is not None and tgt.get("max_hp") and tgt["hp"] <= 0.3 * tgt["max_hp"]
                         and tgt["hp"] < me["hp"]) and "fight" in toks
        pred = km.v72_gate("fight" in toks, "zone" if label.startswith("zone ") else label.split(" ")[0],
                           "push" in toks, "chg" in toks, finishing, label.startswith("drop-hold"),
                           me.get("in_zone", True), toks)
        n += 1
        if pred != bool(called):
            bad.append((sc["name"], label, pred, bool(called)))
    assert not bad, f"{len(bad)}/{n} gate mismatches, e.g. {bad[:3]}"
