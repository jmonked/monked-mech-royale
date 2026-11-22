# v71-nearsound-0p9

- Baseline: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `1c4827e7b8680d0750748c87c54521088ef027dd`
- Official baseline: 4.73
- Official candidate: 4.73 (delta +0.00)
- Matches tested: 6 (seeds 1000..1005)
- Decisions compared: 6250
- Differing decisions: 8
- Matches diverged: 2/6
- Most common action difference: aim (8)
- First-divergence pattern: aim | cube face x1; aim | zone face x1
- Local outcome direction (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): candidate placed better in 0, worse in 0, same in 6 of 6 matches
- Confidence / limitations: local sim only (no jumping/jets, no beams, guessed house bots); shared-world counts are counterfactual per decision; paired worlds stop being comparable after divergence.

## Action-difference categories

- aim: 8

## Activation windows

- nearsound 0.6<age<=0.9: 44 decisions, aim differs 8, any field differs 8
- nearsound age<=0.6: 289 decisions, aim differs 0, any field differs 0

## First divergence per match

- seed 1000: no divergence
- seed 1001: no divergence
- seed 1002: no divergence
- seed 1003 t=42.1s [aim] label `cube face hp68% c0` hp 950.0/1400.0 visible 0 attackers {'1': 0.5}
  - base {"aim": [1.867882943121604, 0.0]} vs candidate {"aim": [1.8252973387330371, 0.0]}
  - +3 s base: hp +112.0, moved 28.9 m, new attackers -; candidate: hp +112.0, moved 28.9 m, new attackers -; reconverged after 1.3 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 15 t 71.0s cause gun; candidate place 15 t 71.0s cause gun
- seed 1004 t=36.6s [aim] label `zone face hp79% c0` hp 1107.5/1400.0 visible 2 attackers {'1': 1.5}
  - base {"aim": [1.3624732252273926, 0.0]} vs candidate {"aim": [1.2569722116019548, 0.0]}
  - +3 s base: hp -90.0, moved 25.8 m, new attackers [8]; candidate: hp -90.0, moved 25.8 m, new attackers [8]; reconverged after 1.3 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 12 t 61.5s cause gun; candidate place 12 t 61.5s cause gun
- seed 1005: no divergence
