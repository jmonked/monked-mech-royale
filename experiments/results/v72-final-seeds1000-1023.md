# v72-final-seeds1000-1023

- Baseline: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `076094fbd128c8df846b695d5f24c3ec84d35767`
- Official baseline: 4.73
- Official candidate: not recorded
- Matches tested: 24 (seeds 1000..1023)
- Decisions compared: 21349
- Differing decisions: 68
- Matches diverged: 8/24
- Most common action difference: move (68)
- First-divergence pattern: move | zone fight 1 x2; move | zone fight 7 x2; move | zone fight 15 x1; move | zone fight 2 x1; move | zone fight 3 x1; move | zone fight 4 x1
- Local outcome direction (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): candidate placed better in 1, worse in 1, same in 22 of 24 matches
- Confidence / limitations: local sim only (no jumping/jets, no beams, guessed house bots); shared-world counts are counterfactual per decision; paired worlds stop being comparable after divergence.

## Action-difference categories

- move: 68

## First divergence per match

- seed 1000 t=14.3s [move] label `zone fight 1 hp 950 hp84% c0` hp 1175.0/1400.0 visible 3 attackers {'1': 0.2}
  - base {"move": [-0.6959134047000131, -0.7181257084653325]} vs candidate {"move": [-0.9819588728217439, -0.18909461146910078]}
  - +3 s base: hp -832.5, moved 38.1 m, new attackers [8]; candidate: hp -810.0, moved 40.2 m, new attackers [8]; reconverged after 2.4 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 16 t 25.4s cause gun; candidate place 16 t 25.2s cause gun
- seed 1001 t=40.5s [move] label `zone fight 15 hp 1400 hp81% c0` hp 1130.0/1400.0 visible 4 attackers {'15': 0.0}
  - base {"move": [0.7799737897084877, -0.6258121821823059]} vs candidate {"move": [-0.47385271182786964, -0.8806041150786056]}
  - +3 s base: hp -855.0, moved 24.9 m, new attackers [5]; candidate: hp -720.0, moved 39.8 m, new attackers [5]; reconverged after 1.3 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 16 t 46.8s cause gun; candidate place 16 t 50.9s cause gun
- seed 1002: no divergence
- seed 1003: no divergence
- seed 1004 t=52.6s [move] label `zone fight 7 hp 639 hp58% c4` hp 937.8/1624.0 visible 3 attackers {'7': 0.8}
  - base {"move": [0.958824030360635, -0.2840008429617559]} vs candidate {"move": [-0.11579901240972904, -0.9932726658500833]}
  - +3 s base: hp -472.5, moved 13.3 m, new attackers [3]; candidate: hp -540.0, moved 16.1 m, new attackers [3]; reconverged after 1.8 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 12 t 61.5s cause gun; candidate place 13 t 57.9s cause gun
- seed 1005: no divergence
- seed 1006: no divergence
- seed 1007: no divergence
- seed 1008: no divergence
- seed 1009: no divergence
- seed 1010 t=71.3s [move] label `zone fight 1 hp 671 hp55% c2` hp 837.0/1512.0 visible 4 attackers {'7': 0.2, '1': 0.1}
  - base {"move": [0.6406090112804704, -0.7678672376565223]} vs candidate {"move": [-0.9389005467344782, -0.3441885578308753]}
  - +3 s base: hp -180.0, moved 4.8 m, new attackers -; candidate: hp -90.0, moved 7.0 m, new attackers -; reconverged after 1.4 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 14 t 88.0s cause gun; candidate place 14 t 89.4s cause gun
- seed 1011: no divergence
- seed 1012: no divergence
- seed 1013 t=23.0s [move] label `zone fight 2 hp 1400 hp97% c0` hp 1355.0/1400.0 visible 3 attackers {'2': 0.0}
  - base {"move": [-0.5645592282886638, -0.8253925597884368]} vs candidate {"move": [-0.44281654786181673, 0.8966122377816081]}
  - +3 s base: hp -900.0, moved 27.9 m, new attackers [2, 5, 14]; candidate: hp -315.0, moved 22.8 m, new attackers [2]; reconverged after 1.0 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 16 t 26.8s cause laser; candidate place 15 t 40.5s cause gun
- seed 1014: no divergence
- seed 1015: no divergence
- seed 1016 t=36.9s [move] label `zone fight 3 hp 874 hp76% c0` hp 1058.0/1400.0 visible 3 attackers {'3': 1.9}
  - base {"move": [0.9992460360348913, 0.038824727540020754]} vs candidate {"move": [0.023136842782690247, -0.9997323074233667]}
  - +3 s base: hp -180.0, moved 10.8 m, new attackers [2]; candidate: hp -315.0, moved 5.5 m, new attackers [2]; reconverged after 1.2 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 13 t 53.4s cause gun; candidate place 13 t 52.8s cause gun
- seed 1017: no divergence
- seed 1018: no divergence
- seed 1019: no divergence
- seed 1020: no divergence
- seed 1021: no divergence
- seed 1022 t=37.4s [move] label `zone fight 4 hp 559 hp61% c0` hp 860.0/1400.0 visible 2 attackers {'4': 0.1}
  - base {"move": [0.9210415812390886, 0.3894642546224225]} vs candidate {"move": [-0.4696295444922582, 0.8828635743646885]}
  - +3 s base: hp -585.0, moved 23.9 m, new attackers [1]; candidate: hp -585.0, moved 19.0 m, new attackers [1]; reconverged after 1.0 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 15 t 74.2s cause gun; candidate place 15 t 45.9s cause gun
- seed 1023 t=18.0s [move] label `zone fight 7 hp 635 hp55% c0` hp 770.0/1400.0 visible 2 attackers {'7': 0.0, '1': 0.6}
  - base {"move": [-0.9489164291700545, 0.3155275114013876]} vs candidate {"move": [0.26307817318198734, -0.9647745201834613]}
  - +3 s base: hp -450.0, moved 7.7 m, new attackers -; candidate: hp -495.0, moved 19.8 m, new attackers -; reconverged after 2.3 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 16 t 24.8s cause gun; candidate place 16 t 28.9s cause gun
