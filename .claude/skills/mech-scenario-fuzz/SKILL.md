---
name: mech-scenario-fuzz
description: Generate adversarial synthetic Mech Royale states for one bot subsystem with Hypothesis and the scenario lab, minimise failures, save them as permanent regression cases, and report the branch coverage gained. Never edits gameplay code.
---

# mech-scenario-fuzz

Input: a subsystem or hypothesis, e.g. "aggregate multi-attacker survival", "laser sidestep vs unseen attacker".

All work happens in the tooling worktree `C:\Users\julia\MONKED\wt-harness`. Gameplay files are read-only here.

## Steps

1. **Target branches**: find the functions involved (`grep -n "def _" example_bot.py`) and read the current blind spots in `experiments/results/COVERAGE.md` (regenerate with `python tools/tactical_coverage.py --ref <ref> --hypothesis 800`).
2. **State families**: extend `tests/combat_strategies.py` (`build(draw, family)`: one builder drives both Hypothesis and random sampling) or add a synth family in `tools/scenario_lab.py` (`synth()`: mutates harvested real states, keeping real map geometry). Use protocol field names exactly (`protocol.md`); never invent observation fields. Bot memory goes in `state` via `lab.enc(...)` (e.g. `last_hits {id: (t, bearing)}`, `last_near_sound (t, bearing)`, `pos_history [(t, x, y)]`).
3. **Properties**: add or parametrize a Hypothesis test in `tests/test_combat_properties.py` (valid action, timing, and with `MONKED_CANDIDATE`: no catastrophic verdict from `tools/tactical_rules.py`). Hypothesis shrinks failures to a minimal state; `conftest.save_found()` writes it to `experiments/corpus/regression/found-*.jsonl`.
4. **Harvest real states** when geometry matters: `python tools/scenario_lab.py harvest --ref <ref> --seeds 1000-1023` (replays bit-exactly; check with `python tools/scenario_lab.py verify`). `--regression seed:t0:t1 --reg-name <name>` saves a whole time window as a permanent regression set.
5. **Run**: `python -m pytest -n auto -q` (set `MONKED_CANDIDATE` for candidate-vs-base properties).
6. **Coverage gained**: rerun `tools/tactical_coverage.py` and report before/after branch arcs for the target functions.

## Output

- target functions/branches and which were uncovered
- state families added
- minimised failing cases (file paths under `experiments/corpus/regression/`)
- coverage before -> after for the targeted functions
