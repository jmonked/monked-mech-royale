# Submit gate

```text
Candidate: e02ddaaa9550b963788689869707f0748f00cb0e
Parent: aba6bef050c9a30fb74d3e06b8f8507e7b0105d9 (NOT the intended base c8e98e18b1471388bdeee6f2e090568393af446b)
Worktree: none checked out
Remote: NOT on origin
Gameplay files changed: experiments/results/HISTORY.md, experiments/results/sanity-v39-vs-v39.json, experiments/results/sanity-v39-vs-v39.md, experiments/results/v60-wedge-priority.json, experiments/results/v60-wedge-priority.md, experiments/results/v61-push-more-24.json, experiments/results/v61-push-more-24.md, experiments/results/v62-aggregate-threat.json, experiments/results/v62-aggregate-threat.md, experiments/results/v63-threat-gate.json, experiments/results/v63-threat-gate.md, experiments/results/v64-cube-cap.json, experiments/results/v64-cube-cap.md, experiments/results/v65-abl-no-tpcover.json, experiments/results/v65-abl-no-tpcover.md, experiments/results/v66-abl-no-nearsound.json, experiments/results/v66-abl-no-nearsound.md, experiments/results/v67-abl-no-reloadcover.json, experiments/results/v67-abl-no-reloadcover.md, experiments/results/v68-abl-no-zoneearly.json, experiments/results/v68-abl-no-zoneearly.md, experiments/results/v69-abl-no-ffa3p.json, experiments/results/v69-abl-no-ffa3p.md, experiments/results/v70-abl-no-shortguard.json, experiments/results/v70-abl-no-shortguard.md, experiments/results/v71-nearsound-0p9.json, experiments/results/v71-nearsound-0p9.md, tools/experiment_harness.py
Remote diff: 28 files changed, 7651 insertions(+)
Hypothesis: tooling commit (must be refused)
check.py: FAIL, late ?, p50 ? p99 ? max ? ms
Crash check (6 matches): errors 0, exit 0

NOT READY
  - parent is not the intended base
  - no remote ref points at the candidate
  - REFUSED: example_bot.py identical to base - not an official gameplay candidate
  - tooling/test/doc files in the gameplay commit: ['experiments/results/HISTORY.md', 'experiments/results/sanity-v39-vs-v39.json', 'experiments/results/sanity-v39-vs-v39.md', 'experiments/results/v60-wedge-priority.json', 'experiments/results/v60-wedge-priority.md', 'experiments/results/v61-push-more-24.json', 'experiments/results/v61-push-more-24.md', 'experiments/results/v62-aggregate-threat.json', 'experiments/results/v62-aggregate-threat.md', 'experiments/results/v63-threat-gate.json', 'experiments/results/v63-threat-gate.md', 'experiments/results/v64-cube-cap.json', 'experiments/results/v64-cube-cap.md', 'experiments/results/v65-abl-no-tpcover.json', 'experiments/results/v65-abl-no-tpcover.md', 'experiments/results/v66-abl-no-nearsound.json', 'experiments/results/v66-abl-no-nearsound.md', 'experiments/results/v67-abl-no-reloadcover.json', 'experiments/results/v67-abl-no-reloadcover.md', 'experiments/results/v68-abl-no-zoneearly.json', 'experiments/results/v68-abl-no-zoneearly.md', 'experiments/results/v69-abl-no-ffa3p.json', 'experiments/results/v69-abl-no-ffa3p.md', 'experiments/results/v70-abl-no-shortguard.json', 'experiments/results/v70-abl-no-shortguard.md', 'experiments/results/v71-nearsound-0p9.json', 'experiments/results/v71-nearsound-0p9.md', 'tools/experiment_harness.py']
  - check.py gate (PASS, 0 late, p99<10, max<50)
```
