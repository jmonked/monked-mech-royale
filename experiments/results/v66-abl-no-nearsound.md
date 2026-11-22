# v66-abl-no-nearsound

- Baseline: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `b465f3861c8577276c298472409d388c6ee61483`
- Official baseline: 4.73
- Official candidate: 4.54 (delta -0.19)
- Matches tested: 6 (seeds 1000..1005)
- Decisions compared: 6296
- Differing decisions: 13
- Matches diverged: 2/6
- Most common action difference: aim (13)
- First-divergence pattern: aim | cube face x1; aim | zone face x1
- Local outcome direction (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): candidate placed better in 0, worse in 0, same in 6 of 6 matches
- Confidence / limitations: local sim only (no jumping/jets, no beams, guessed house bots); shared-world counts are counterfactual per decision; paired worlds stop being comparable after divergence.

## Action-difference categories

- aim: 13

## Activation windows

- nearsound 0.6<age<=0.9: 39 decisions, aim differs 0, any field differs 0
- nearsound age<=0.6: 298 decisions, aim differs 13, any field differs 13

## First divergence per match

- seed 1000: no divergence
- seed 1001: no divergence
- seed 1002: no divergence
- seed 1003 t=41.6s [aim] label `cube face hp68% c0` hp 950.0/1400.0 visible 0 attackers {'1': 0.0}
  - base {"aim": [1.8252973387330371, 0.0]} vs candidate {"aim": [1.867882943121604, 0.0]}
  - +3 s base: hp +112.0, moved 42.1 m, new attackers -; candidate: hp +112.0, moved 42.1 m, new attackers -; reconverged after 1.4 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 15 t 71.0s cause gun; candidate place 15 t 71.0s cause gun
- seed 1004 t=36.0s [aim] label `zone face hp79% c0` hp 1107.5/1400.0 visible 2 attackers {'1': 0.9}
  - base {"aim": [1.2569722116019548, 0.0]} vs candidate {"aim": [1.3624732252273926, 0.0]}
  - +3 s base: hp -90.0, moved 17.2 m, new attackers [8]; candidate: hp -90.0, moved 17.2 m, new attackers [8]; reconverged after 1.5 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 12 t 61.5s cause gun; candidate place 12 t 66.2s cause gun
- seed 1005: no divergence
