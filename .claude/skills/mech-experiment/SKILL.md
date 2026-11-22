---
name: mech-experiment
description: Run ONE isolated Mech Royale gameplay hypothesis end to end (exact base, isolated worktree, smallest change, focused tests, scenario corpus, branch coverage, harness, catastrophic check, check.py, crash test, push, remote verification, submission card). Never submits to the competition.
---

# mech-experiment

One gameplay hypothesis, start to finish. The official control is v39 `c8e98e18b1471388bdeee6f2e090568393af446b` (4.73) unless the user names another base. Tooling lives on branch `tools-experiment-harness` (worktree `C:\Users\julia\MONKED\wt-harness`); never merge tooling into a gameplay branch. Never touch the main checkout `C:\Users\julia\MONKED\monked-mech-royale` except to run read-only commands from it (it is mid-merge).

## Workflow

1. **Verify the base**: `git -C C:\Users\julia\MONKED\monked-mech-royale rev-parse c8e98e1` must print the full v39 hash.
2. **Isolated worktree**: `git -C <main repo> worktree add -b <vNN-name> C:\Users\julia\MONKED\wt-<vNN-name> c8e98e1`.
3. **Trace before editing**: grep the real callers and state flow of every function you touch (bounded reads; `example_bot.py` is ~1,640 lines). Note which subsystems write `act["move"]`, `act["aim"]`, `act["boost"]`, `act["fire"]` after your change point (override order in `_act`).
4. **Smallest change**: one hypothesis, behind a `USE_<NAME>` switch when it adds logic. Unix LF endings. Standard library only. Never edit `mechfight.py` or the Dockerfile.
5. **Focused unit test** (scratch file, not committed): drive `Bot._act` with stubs, or a scenario via `tools/scenario_lab.py`, proving (a) the intended change happens and (b) everything else is identical to v39.
6. **Scenario corpus + Hypothesis + metamorphic** (from the harness worktree):
   `$env:MONKED_CANDIDATE="C:\Users\julia\MONKED\wt-<vNN>\example_bot.py"; python -m pytest -n auto -q`
7. **Corpus verdicts + coverage**:
   `python tools/experiment_harness.py corpus --candidate <hash> --name <vNN> --hypothesis 1000 --coverage`
   Catastrophic must be 0. Read every "worse" example. `changed lines reached` shows whether the corpus exercises your new code. If it does not, add scenarios (skill `mech-scenario-fuzz`) before trusting anything.
8. **Match forensics**: `python tools/experiment_harness.py compare --candidate <hash> --name <vNN> --matches 24` (first divergence per match, +1/+3 s windows, local outcomes; LOCAL ONLY).
9. **Red team** (skill `mech-red-team`): DeepSeek Flash attacks the diff; reproduce every reported case with the lab before acting on it.
10. **Runtime**: check.py (0 errors, 0 late, p99 < 10 ms, max < 50 ms) and the 6-match crash check, both included in the gate.
11. **Commit + push** the gameplay branch only (`example_bot.py` only). Message ends with the project's Co-Authored-By line.
12. **Gate** (skill `mech-submit-gate`): `python tools/submit_gate.py --candidate <hash> --hypothesis "<one line>" --focused "python <scratch test>"`. Only READY candidates are offered to the user.
13. **Submission card**: return the gate card plus the corpus and harness summaries. The user submits manually and reports the official score; record it with `python tools/experiment_harness.py record-score <hash> <score> --submission <BB-id>`.

## Rules

- Do not fit parameters to local seeds or the corpus. Fix logic flaws the factory exposes; do not tune numbers until local placement improves.
- The local simulator is not an official-score predictor (v63 changed 0 local decisions yet moved the official score).
- The live scorer is deterministic: same commit, same score. Never resubmit an identical commit.
- Never submit a commit whose `example_bot.py` equals its base (the gate refuses it).
