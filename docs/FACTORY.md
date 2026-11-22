# MONKED Experiment Factory

Development tooling for the Mech Royale bot. Lives on branch `tools-experiment-harness` (worktree
`C:\Users\julia\MONKED\wt-harness`). **Never merge into a gameplay branch; never submit a tooling commit** (the
submit gate refuses commits whose `example_bot.py` equals the base, e.g. `e02ddaaa`, which scored 4.73 because it
was v39 unchanged).

Control: v39 `c8e98e18b1471388bdeee6f2e090568393af446b` = 4.73 official. The live scorer is deterministic.
The local simulator is NOT an official-score predictor (v63 changed 0 local decisions yet scored 4.69).

## Pieces

| File | What |
|---|---|
| `tools/scenario_lab.py` | Runs the real `Bot.act` on a stored observation + full bot memory. `harvest` real states from local matches (bit-exact replay, `verify`), `synth` rare combinations from harvested states, `stats`. |
| `tools/gap_scenarios.py` | Hand-built states for the branches the corpus missed (designed by DeepSeek, `experiments/results/DEEPSEEK_GAPS.md`). |
| `experiments/corpus/<category>/*.jsonl` | Persistent scenario corpus (multi-threat, laser-crossfire, dodge-conflict, cover-conflict, unstick-conflict, sound-boundaries, zone-pressure, combat-misc, regression). |
| `tests/combat_strategies.py` | One semantic combat-state builder for Hypothesis (shrinking) and random sampling (coverage). |
| `tests/test_combat_properties.py` | Hypothesis properties: valid action + timing for every family; with a candidate, no catastrophic verdict. |
| `tests/test_corpus.py` | Corpus replay fidelity; candidate has 0 catastrophic on every category. |
| `tests/test_metamorphic.py` | Rotation, translation, enemy-order invariance; timing-boundary probe report (`BOUNDARIES-*.md`). |
| `tools/tactical_rules.py` | Conservative verdicts per scenario: identical / safer / worse / uncertain / catastrophic (C1-C6). |
| `tools/tactical_coverage.py` | Branch coverage per tactical function (`COVERAGE.md`). |
| `tools/experiment_harness.py` | `compare` (local match lockstep + paired worlds), `corpus` (scenario verdicts + coverage), `record-score`, `table`. |
| `tools/submit_gate.py` | Mandatory READY / NOT READY card before any official submission. |
| `.claude/skills/mech-*` | Project skills: mech-experiment, mech-scenario-fuzz, mech-red-team, mech-submit-gate. |

## Commands

```powershell
python -m pip install -r requirements-dev.txt          # hypothesis, coverage, pytest-xdist (dev only)
python -m pytest -n auto -q                            # v39 suite (base properties, corpus fidelity, metamorphic)
$env:MONKED_CANDIDATE="C:\Users\julia\MONKED\wt-v72\example_bot.py"; python -m pytest -n auto -q
python tools/experiment_harness.py corpus --candidate <hash> --name <vNN> --hypothesis 1000 --coverage
python tools/experiment_harness.py compare --candidate <hash> --name <vNN> --matches 24
python tools/tactical_coverage.py --ref c8e98e1 --hypothesis 800
python tools/submit_gate.py --candidate <hash> --hypothesis "<one line>" --focused "python <focused test>"
python tools/experiment_harness.py record-score <hash> <official score> --submission <BB-id>
```

## Catastrophic rules (tools/tactical_rules.py)

C1 overriding an emergency move the base chose (dodge, laser sidestep, wedge, tp-cover, reload cover, zone-run);
C2 walking straight at 2+ active attackers; C3 stalling under crossfire; C4 stepping into a live (line-of-sight)
charging-laser line; C5 leaving the next circle; C6 boosting into a wall. "Safer"/"worse" need a geometric proof
from the single observation; everything else is "uncertain". No synthetic score is computed.

## T3 multi-model workflow (verified in this environment)

`orchestrator_capabilities` lists: Claude (this lead), `codex / gpt-6.2-sol` (reasoningEffort low..ultra; team cap
"high"), `opencode / deepseek/deepseek-flash` (variant none/low/high/max; "max" allowed).

```
Claude Opus (lead, traces code, integrates, owns commits)
  +-- delegate_task  codex / gpt-6.2-sol  {reasoningEffort: high}  isolation: worktree   -> independent implementation / reproduction
  +-- delegate_task  opencode / deepseek-flash  {variant: max}     read-only + scratch   -> red team, coverage gaps, scenarios
```

Rules: one agent per worktree; children get self-contained briefs (no parent history); async + completion
notification (no polling); every reported failure is reproduced with the lab before code changes; DeepSeek never
integrates. Briefs must demand bounded reads (Sol previously looped on context compaction with whole-file reads).

## Outside agents (ChatGPT / other tools) - audit of the installed T3 Code 0.1.11

Found in the bundled CLI (`C:\Users\julia\.t3\bin\t3.cmd --help`):
- `t3 thread list | start | send | show` - list a project's threads, start a thread and print its id, send a
  message (a busy thread receives it as its next turn), show a thread's state and latest messages. These talk to the
  running server, so an outside agent that can run shell commands on this machine can drive T3 threads today.
- `t3 project` (manage projects), `t3 environment link | list | unlink` (link other T3 environments so agents here
  work there; revocable under Settings -> Sharing & access), `t3 pair` (pairing token for a running server),
  `t3 auth` (local auth control plane), `t3 up` / `t3 connect` (remote access via T3 Connect: login, link, status),
  `--lan` / `--tailscale-serve` server flags.
- No `mcp` subcommand and no documented MCP server endpoint for outside agents were found in this version. The
  `mcp__t3-code__*` tools are exposed to agents running inside T3, not as a public MCP URL.

So: an external agent can be connected today through the CLI (`t3 thread ...`) on this machine or a linked
environment after `t3 connect` / `t3 up`. Exact URLs, ports and tokens are produced by those commands at setup time
and must not be committed. Nothing was configured or exposed during this task.

## Not done on purpose

- Atheris (coverage-guided fuzzing) is deferred: this is Windows; Hypothesis + branch coverage came first. If still
  needed, run it under WSL2 against `scenario_lab.Runner.run` with the JSON scenario as the fuzz input.
- No dashboard, no ML, no simulator rewrite, no parameter fitting to local seeds.

## Known limitations

- Static single-decision verdicts cannot prove multi-second outcomes; most divergences are honestly "uncertain".
- The local simulator has no jumping/jets, beams, projectiles or crates; harvested states inherit that. Synthetic
  and gap families add projectiles, beams, lasers and roofs on top of harvested or flat-world states.
- Flat-world Hypothesis states remove buildings so metamorphic transforms are exact; geometry is covered by
  harvested/synth/gap states instead.
- Rotation invariance excludes the idle scan (an absolute, time-based yaw sweep by design).
- Exact ties are excluded from generated states: two enemies at exactly equal distance make v39 pick the first
  listed, so a translation that changes float rounding can switch the target (harmless with real floats).
- Generated states never put our mech exactly on the zone centre (atan2(+-0, +-0) depends on the sign of zero).
- Generated enemies never aim with exactly zero error: v39 picks the laser-sidestep side from the sign of our offset
  from the beam line, so a dead-centre beam makes the side depend on float rounding (either side is equally good).

## CrossHair layer (symbolic, final pre-submission check)

- `tools/crosshair_mech.py`: pure typed kernels traceable to v72 `_aggregate_threat_move` + its `_act` gate (and v62
  for comparison); `extract()` feeds them from a live bot. `tests/test_crosshair_parity.py` proves kernel == real
  method on every corpus call (414 calls, 69 activations, 0 mismatches) and gate == real on every corpus state.
- `tools/crosshair_props.py`: invariants A-I in asserts mode
  (`crosshair check tools/crosshair_props.py --analysis_kind=asserts --per_condition_timeout=90`) and diffbehavior
  wrappers (`stock_identity` vs `v72_outside_activation` / `v72_locked`; `v62_bounded` vs `v72_bounded`).
- `tests/test_crosshair_cover.py`: 568 `crosshair cover --coverage_type=path` cases pinned as regression tests.
- Trig is concretised by CrossHair, so this is concolic search within a budget, not a proof over all reals.
