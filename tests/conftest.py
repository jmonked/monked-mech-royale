"""Shared config for the MONKED experiment-factory tests.

Environment:
  MONKED_BASE       gameplay control ref (default c8e98e1 = v39)
  MONKED_CANDIDATE  candidate ref or bot file path; candidate-vs-base tests are skipped when unset
  MONKED_EXAMPLES   Hypothesis examples per property (default 120)
Run:  pytest -n auto            (pytest-xdist; every worker loads its own bot copies, no shared state)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

BASE = os.environ.get("MONKED_BASE", "c8e98e1")
CANDIDATE = os.environ.get("MONKED_CANDIDATE") or None
EXAMPLES = int(os.environ.get("MONKED_EXAMPLES", "120"))
FOUND = os.path.join(ROOT, "experiments", "corpus", "regression")


def save_found(name, sc, reasons):
    """Persist a failing generated state so it becomes a permanent regression case."""
    os.makedirs(FOUND, exist_ok=True)
    sc = dict(sc, category="regression", name=f"found-{name}", found_reasons=reasons,
              source=dict(sc.get("source", {}), found_by=name, candidate=CANDIDATE))
    with open(os.path.join(FOUND, f"found-{name}.jsonl"), "w", encoding="utf-8") as f:
        f.write(json.dumps(sc, separators=(",", ":")) + "\n")
