# v72-aggregate-threat-v2-seeds1006-1023

- Baseline: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `a027c8c9ef4ced5884d51446c4fc440682ee4bd4`
- Official baseline: 4.73
- Official candidate: not recorded
- Matches tested: 18 (seeds 1006..1023)
- Decisions compared: 14934
- Differing decisions: 105
- Matches diverged: 10/18
- Most common action difference: move (105)
- First-divergence pattern: move | zone fight 2 x2; move | laser hunt fight 1 x1; move | zone fight 1 x1; move | zone fight 9 x1; move | zone fight 12 x1; move | zone fight 3 x1; move | zone fight 13 x1; move | zone fight 4 x1; move | laser hunt fight 7 x1
- Local outcome direction (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): candidate placed better in 1, worse in 1, same in 16 of 18 matches
- Confidence / limitations: local sim only (no jumping/jets, no beams, guessed house bots); shared-world counts are counterfactual per decision; paired worlds stop being comparable after divergence.

## Action-difference categories

- move: 105

## First divergence per match

- seed 1006: no divergence
- seed 1007 t=19.0s [move] label `zone fight 2 hp 817 push hp77% c2` hp 1170.0/1512.0 visible 3 attackers {'2': 1.3}
  - base {"move": [0.7011226768351284, -0.7130406664612783]} vs candidate {"move": [-0.9851198775399372, -0.1718686326113603]}
  - +3 s base: hp -360.0, moved 28.6 m, new attackers [9]; candidate: hp -450.0, moved 27.3 m, new attackers [9]; reconverged after 1.7 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 14 t 32.8s cause gun; candidate place 14 t 34.9s cause gun
- seed 1008: no divergence
- seed 1009 t=46.5s [move] label `laser hunt fight 1 hp 1130 hp29% c0` hp 402.5/1400.0 visible 3 attackers {'7': 2.6, '1': 0.1}
  - base {"move": [-0.6583238699128442, 0.7527348021069417]} vs candidate {"move": [-0.6557844922281663, -0.7549481437509772]}
  - +3 s base: hp -360.0; candidate: hp -382.5; no reconvergence
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 16 t 48.1s cause gun; candidate place 16 t 47.9s cause gun
- seed 1010 t=68.9s [move] label `zone fight 1 hp 1351 hp93% c2` hp 1399.5/1512.0 visible 3 attackers {'7': 0.1}
  - base {"move": [-0.9833686558861754, -0.18162072189212525]} vs candidate {"move": [0.42459436044820775, 0.9053836916333192]}
  - +3 s base: hp -652.5, moved 9.4 m, new attackers [1]; candidate: hp -697.5, moved 26.2 m, new attackers [1]; reconverged after 3.4 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 14 t 88.0s cause gun; candidate place 14 t 82.8s cause gun
- seed 1011 t=7.0s [move] label `zone fight 9 hp 1130 hp100% c0` hp 1400.0/1400.0 visible 2 attackers -
  - base {"move": [-0.7023654513556896, 0.71181653025335]} vs candidate {"move": [-0.864041245165731, 0.5034210232523598]}
  - +3 s base: hp -337.5, moved 33.3 m, new attackers [1, 9]; candidate: hp -337.5, moved 30.5 m, new attackers [1, 9]; reconverged after 6.9 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 15 t 19.4s cause gun; candidate place 16 t 19.5s cause gun
- seed 1012: no divergence
- seed 1013 t=23.0s [move] label `zone fight 2 hp 1400 hp97% c0` hp 1355.0/1400.0 visible 3 attackers {'2': 0.0}
  - base {"move": [-0.5645592282886638, -0.8253925597884368]} vs candidate {"move": [-0.44281654786181673, 0.8966122377816081]}
  - +3 s base: hp -900.0, moved 27.9 m, new attackers [2, 5, 14]; candidate: hp -315.0, moved 22.8 m, new attackers [2]; reconverged after 1.0 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 16 t 26.8s cause laser; candidate place 15 t 34.0s cause gun
- seed 1014 t=117.2s [move] label `zone fight 12 hp 1355 hp100% c0` hp 1400.0/1400.0 visible 3 attackers -
  - base {"move": [0.9591658708932416, -0.28284418345373386]} vs candidate {"move": [0.17577280484708185, 0.9844307599197567]}
  - +3 s base: hp -1275.0, moved 23.0 m, new attackers [12, 14]; candidate: hp -990.0, moved 18.2 m, new attackers [12, 14]; reconverged after 2.6 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 16 t 120.6s cause lightning; candidate place 16 t 121.1s cause gun
- seed 1015: no divergence
- seed 1016 t=36.9s [move] label `zone fight 3 hp 874 hp76% c0` hp 1058.0/1400.0 visible 3 attackers {'3': 1.9}
  - base {"move": [0.9992460360348913, 0.038824727540020754]} vs candidate {"move": [0.023136842782690247, -0.9997323074233667]}
  - +3 s base: hp -180.0, moved 10.8 m, new attackers [2]; candidate: hp -315.0, moved 5.5 m, new attackers [2]; reconverged after 1.2 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 13 t 53.4s cause gun; candidate place 13 t 52.8s cause gun
- seed 1017: no divergence
- seed 1018 t=48.3s [move] label `zone fight 13 hp 734 hp16% c2` hp 280.8/1738.8 visible 3 attackers {'13': 1.6}
  - base {"move": [-0.44039917034449133, -0.8978020777208547]} vs candidate {"move": [0.667747565829569, 0.7443877943173742]}
  - +3 s base: hp -157.5; candidate: hp -157.5; no reconvergence
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 13 t 48.8s cause gun; candidate place 13 t 48.8s cause gun
- seed 1019: no divergence
- seed 1020: no divergence
- seed 1021: no divergence
- seed 1022 t=37.4s [move] label `zone fight 4 hp 559 hp61% c0` hp 860.0/1400.0 visible 2 attackers {'4': 0.1}
  - base {"move": [0.9210415812390886, 0.3894642546224225]} vs candidate {"move": [-0.4696295444922582, 0.8828635743646885]}
  - +3 s base: hp -585.0, moved 23.9 m, new attackers [1]; candidate: hp -585.0, moved 19.0 m, new attackers [1]; reconverged after 1.0 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 15 t 74.2s cause gun; candidate place 15 t 45.9s cause gun
- seed 1023 t=16.3s [move] label `laser hunt fight 7 hp 950 hp65% c0` hp 905.0/1400.0 visible 2 attackers {'7': 0.7}
  - base {"move": [0.9961445870607847, 0.08772663033252076]} vs candidate {"move": [0.9322418419845675, 0.3618358026138663]}
  - +3 s base: hp -315.0, moved 3.8 m, new attackers -; candidate: hp -450.0, moved 31.6 m, new attackers -; reconverged after 1.7 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 16 t 24.8s cause gun; candidate place 16 t 23.1s cause gun
