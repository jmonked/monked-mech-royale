# v60-wedge-priority

- Baseline: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `5bab1a0c44874a79a93445b47601ab5381e71bda`
- Official baseline: 4.73
- Official candidate: 4.71 (delta -0.02)
- Matches tested: 6 (seeds 1000..1005)
- Decisions compared: 6244
- Differing decisions: 7
- Matches diverged: 1/6
- Most common action difference: move (7)
- First-divergence pattern: move | zone fight 7 x1
- Local outcome direction (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): candidate placed better in 0, worse in 1, same in 5 of 6 matches
- Confidence / limitations: local sim only (no jumping/jets, no beams, guessed house bots); shared-world counts are counterfactual per decision; paired worlds stop being comparable after divergence.

## Action-difference categories

- move: 7

## First divergence per match

- seed 1000: no divergence
- seed 1001: no divergence
- seed 1002: no divergence
- seed 1003: no divergence
- seed 1004 t=53.8s [move] label `zone fight 7 hp 570 wedge tp-cover hp49% c4 chg` hp 802.8/1624.0 visible 5 attackers {'7': 0.0, '3': 0.0}
  - base {"move": [0.932850392970702, 0.36026399255879976]} vs candidate {"move": [-0.959210055509249, 0.28269430381587707]}
  - +3 s base: hp -315.5, moved 5.4 m, new attackers [3]; candidate: hp -518.0, moved 3.4 m, new attackers [3]; reconverged after 1.0 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 12 t 61.5s cause gun; candidate place 13 t 60.9s cause gun
- seed 1005: no divergence
