---
name: mech-submit-gate
description: Mandatory gate before any official Mech Royale submission - verifies base/hash/clean worktree/remote, REFUSES commits whose example_bot.py equals the base (tooling/docs/results-only commits like e02ddaaa), runs focused tests, pytest scenario suite, corpus catastrophic check, check.py timing and the crash check, and prints a READY / NOT READY card. Never submits.
---

# mech-submit-gate

Run from the tooling worktree `C:\Users\julia\MONKED\wt-harness`:

```powershell
python tools/submit_gate.py --candidate <hash> --base c8e98e1 --hypothesis "<one line>" --focused "python <scratch focused test>"
```

`--quick` skips pytest and the corpus (git, gameplay and runtime checks only) for fast pre-checks; never use it for the final card.

## What it enforces

- **Git**: candidate resolves; its parent is exactly the intended base; its worktree (if checked out) is clean; a remote ref on `origin` points at the exact hash.
- **Gameplay**: `example_bot.py` differs from the base. If only tools, docs, tests or experiment results changed -> `REFUSED: ... not an official gameplay candidate`. Tooling/test/result files inside a gameplay commit -> NOT READY.
- **Tests**: focused test command exits 0; `pytest -n auto` with `MONKED_CANDIDATE` passes (properties, corpus fidelity, candidate safety, metamorphic); corpus check (`experiment_harness.py corpus`, corpus + 1,000 generated states) has 0 catastrophic regressions.
- **Runtime**: check.py PASS, 0 late, p99 < 10 ms, max < 50 ms; 6-match `sim.py` crash check with errors 0 and no hang.

## Output card

```text
Candidate / Parent / Worktree / Remote
Gameplay files changed / Remote diff / Hypothesis
Focused test / Scenario tests / Scenario corpus size
Candidate divergences / Clearly safer / worse / uncertain / Catastrophic regressions
check.py / Crash check
READY | NOT READY (+ reasons)
```

The card is also written to `experiments/results/gate-<hash7>.md`. Hand the card to the user; the user submits manually. Afterwards record the official score: `python tools/experiment_harness.py record-score <hash> <score> --submission <BB-id>`.
