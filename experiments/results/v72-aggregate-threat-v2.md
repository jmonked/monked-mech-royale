# v72-aggregate-threat-v2

- Baseline: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `a027c8c9ef4ced5884d51446c4fc440682ee4bd4`
- Official baseline: 4.73
- Official candidate: not recorded
- Matches tested: 6 (seeds 1000..1005)
- Decisions compared: 6244
- Differing decisions: 29
- Matches diverged: 3/6
- Most common action difference: move (29)
- First-divergence pattern: move | zone fight 1 x1; move | zone fight 15 x1; move | zone fight 7 x1
- Local outcome direction (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): candidate placed better in 0, worse in 1, same in 5 of 6 matches
- Confidence / limitations: local sim only (no jumping/jets, no beams, guessed house bots); shared-world counts are counterfactual per decision; paired worlds stop being comparable after divergence.

## Action-difference categories

- move: 29

## First divergence per match

- seed 1000 t=14.3s [move] label `zone fight 1 hp 950 hp84% c0` hp 1175.0/1400.0 visible 3 attackers {'1': 0.2}
  - base {"move": [-0.6959134047000131, -0.7181257084653325]} vs candidate {"move": [-0.9586219674779165, -0.28468214462584135]}
  - +3 s base: hp -832.5, moved 38.1 m, new attackers [8]; candidate: hp -765.0, moved 40.0 m, new attackers [8]; reconverged after 2.4 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 16 t 25.4s cause gun; candidate place 16 t 24.5s cause gun
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
