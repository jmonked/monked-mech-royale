# v62-aggregate-threat

- Baseline: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `a023e35a15df4f425691bb2c8fdee257063e78a3`
- Official baseline: 4.73
- Official candidate: not recorded
- Matches tested: 6 (seeds 1000..1005)
- Decisions compared: 6285
- Differing decisions: 60
- Matches diverged: 3/6
- Most common action difference: move (60)
- First-divergence pattern: move | zone fight 1 x1; move | zone fight 15 x1; move | zone fight 7 x1
- Local outcome direction (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): candidate placed better in 0, worse in 1, same in 5 of 6 matches
- Confidence / limitations: local sim only (no jumping/jets, no beams, guessed house bots); shared-world counts are counterfactual per decision; paired worlds stop being comparable after divergence.

## Action-difference categories

- move: 60

## First divergence per match

- seed 1000 t=14.7s [move] label `zone fight 1 hp 860 hp76% c0` hp 1062.5/1400.0 visible 3 attackers {'1': 0.1, '8': 0.0}
  - base {"move": [-0.7018982101137876, -0.7122772652830225]} vs candidate {"move": [-0.9515743313999633, -0.30741875645560884]}
  - +3 s base: hp -765.0, moved 36.8 m, new attackers [8]; candidate: hp -652.5, moved 40.2 m, new attackers [8]; reconverged after 4.1 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 16 t 25.4s cause gun; candidate place 16 t 31.2s cause gun
- seed 1001 t=40.9s [move] label `zone fight 15 hp 1310 ldodge hp78% c0` hp 1085.0/1400.0 visible 4 attackers {'15': 0.2}
  - base {"move": [0.6030309709015447, -0.7977177747383722]} vs candidate {"move": [-0.286586326371755, 0.9580544230557791]}
  - +3 s base: hp -810.0, moved 35.1 m, new attackers [5]; candidate: hp -720.0, moved 41.7 m, new attackers [5]; reconverged after 1.7 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 16 t 46.8s cause gun; candidate place 16 t 46.8s cause gun
- seed 1002: no divergence
- seed 1003: no divergence
- seed 1004 t=53.8s [move] label `zone fight 7 hp 570 wedge tp-cover hp49% c4 chg` hp 802.8/1624.0 visible 5 attackers {'7': 0.0, '3': 0.0}
  - base {"move": [0.932850392970702, 0.36026399255879976]} vs candidate {"move": [-0.5901812146235512, -0.8072707934178406]}
  - +3 s base: hp -315.5, moved 5.4 m, new attackers [3]; candidate: hp -619.0, moved 4.1 m, new attackers [3]; reconverged after 1.5 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 12 t 61.5s cause gun; candidate place 13 t 59.5s cause gun
- seed 1005: no divergence
