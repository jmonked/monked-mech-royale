---
name: mech-red-team
description: Adversarially attack a Mech Royale gameplay candidate (preferably with DeepSeek Flash 1017 via T3 delegate_task) to find priority inversions, stale state, dangerous interactions, timing-boundary failures, false threat classification, missing fallbacks and server/client mismatches - returned as concrete reproducible scenarios. The red team breaks things; it does not judge the candidate overall.
---

# mech-red-team

## Delegate (T3)

1. `orchestrator_capabilities` (search "deepseek") to confirm `opencode / deepseek/deepseek-flash` is available.
2. `delegate_task` with `target = {providerInstanceId: "opencode", model: "deepseek/deepseek-flash", options: {variant: "max"}}`, `role: "review"`, `mode: "async"`. DeepSeek may run at "max"; GPT/Sol children are capped at "high".
3. The brief must be self-contained (children get no parent history) and include:
   - candidate worktree path + full hash; control `c8e98e1`; the diff command
   - `experiments/results/corpus-<name>.md` (corpus verdicts), `COVERAGE.md` gaps, harness summary
   - the scenario format and runner (`tools/scenario_lab.py`, `tests/combat_strategies.py`, `tools/tactical_rules.py`)
   - the hunt list: priority inversion, stale flags / state corruption, dangerous subsystem interactions (unstick, zone-run, laser guard, boost kept from push, jump+boost jets), timing boundaries, movement override conflicts, false threat classification (own id, NPC ids, killed ids, aim None, bearing None), missing fallback, server-vs-client mismatch
   - hard rules: read-only on repo and worktrees, bounded reads (<=150 lines), no `git branch`, no long sim runs; write reproductions to `%TEMP%\redteam_<name>\<n>.json`
   - required output: up to 8 cases, each with scenario JSON, observed v39 vs candidate actions + labels, why it is dangerous, severity; only cases actually reproduced
4. Do not wait or poll; continue other work until the completion notification.

## Integrate

- Reproduce every case yourself with the lab (`lab.runner(ref).run(sc)`) before acting. Optionally hand the strongest cases to Codex/Sol (`codex / gpt-6.2-sol`, `reasoningEffort: "high"`, `isolation: "worktree"`) for independent reproduction.
- Confirmed and dangerous -> fix the logic in the candidate worktree, save the scenario under `experiments/corpus/regression/`, rerun the corpus check.
- Not reproducible or not dangerous -> record why in the final report; do not change code.
