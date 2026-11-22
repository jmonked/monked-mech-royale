# v61-push-more-24

- Baseline: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `cca2fdd781167b08518a6b0a07dc1fcc85d81f3e`
- Official baseline: 4.73
- Official candidate: 4.52 (delta -0.21)
- Matches tested: 24 (seeds 1000..1023)
- Decisions compared: 21771
- Differing decisions: 105
- Matches diverged: 4/24
- Most common action difference: move (77)
- First-divergence pattern: boost+move | zone fight 1 x2; move | zone fight 14 x1; move | zone fight 12 x1
- Local outcome direction (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): candidate placed better in 1, worse in 1, same in 22 of 24 matches
- Confidence / limitations: local sim only (no jumping/jets, no beams, guessed house bots); shared-world counts are counterfactual per decision; paired worlds stop being comparable after divergence.

## Action-difference categories

- move: 77
- boost+move: 28

## First divergence per match

- seed 1000: no divergence
- seed 1001: no divergence
- seed 1002: no divergence
- seed 1003: no divergence
- seed 1004: no divergence
- seed 1005: no divergence
- seed 1006: no divergence
- seed 1007: no divergence
- seed 1008 t=4.8s [boost+move] label `zone fight 1 hp 995 hp87% c0` hp 1220.0/1400.0 visible 1 attackers {'1': 1.8}
  - base {"boost": false, "move": [-0.2368117088651957, -0.97155556431135]} vs candidate {"boost": true, "move": [0.6831218112678843, -0.7303044508765404]}
  - +3 s base: hp +0.0, moved 16.1 m, new attackers -; candidate: hp -90.0, moved 32.1 m, new attackers -; reconverged after 4.2 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 15 t 23.1s cause gun; candidate place 15 t 20.4s cause gun
- seed 1009: no divergence
- seed 1010: no divergence
- seed 1011: no divergence
- seed 1012 t=6.5s [boost+move] label `zone fight 1 hp 1040 hp90% c0` hp 1265.0/1400.0 visible 2 attackers {'1': 2.2}
  - base {"boost": false, "move": [0.9709942855692866, -0.23910269214668112]} vs candidate {"boost": true, "move": [0.788003403732209, -0.615670882620295]}
  - +3 s base: hp -225.0, moved 28.7 m, new attackers -; candidate: hp -270.0, moved 31.8 m, new attackers -; reconverged after 3.2 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 12 t 271.4s cause zone; candidate place 14 t 273.6s cause zone
- seed 1013: no divergence
- seed 1014: no divergence
- seed 1015 t=15.3s [move] label `zone fight 14 hp 896 hp89% c0` hp 1250.0/1400.0 visible 1 attackers {'14': 0.0}
  - base {"move": [0.9597936764959654, -0.2807064277111556]} vs candidate {"move": [0.9970192598016239, 0.07715306594440752]}
  - +3 s base: hp -1050.0, moved 29.6 m, new attackers -; candidate: hp -1050.0, moved 29.9 m, new attackers -; reconverged after 1.3 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 16 t 19.3s cause lightning; candidate place 16 t 19.7s cause lightning
- seed 1016: no divergence
- seed 1017: no divergence
- seed 1018: no divergence
- seed 1019: no divergence
- seed 1020: no divergence
- seed 1021 t=33.6s [move] label `zone fight 12 hp 1009 hp87% c0` hp 1220.0/1400.0 visible 1 attackers {'12': 0.1}
  - base {"move": [0.6092709654699305, 0.7929620991165585]} vs candidate {"move": [-0.08783692118409037, -0.9961348680158224]}
  - +3 s base: hp -315.0, moved 16.9 m, new attackers -; candidate: hp -225.0, moved 21.9 m, new attackers -; reconverged after 2.5 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 14 t 77.6s cause gun; candidate place 13 t 110.0s cause gun
- seed 1022: no divergence
- seed 1023: no divergence
