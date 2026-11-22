# v65-abl-no-tpcover

- Baseline: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `13907274e57b58fc47c734df8b12d3a062f07271`
- Official baseline: 4.73
- Official candidate: 4.72 (delta -0.01)
- Matches tested: 6 (seeds 1000..1005)
- Decisions compared: 6175
- Differing decisions: 33
- Matches diverged: 3/6
- Most common action difference: boost+move (19)
- First-divergence pattern: boost+move | zone fight 1 x1; boost+move | zone fight 14 x1; boost+move | cube fight 8 x1
- Local outcome direction (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): candidate placed better in 0, worse in 1, same in 5 of 6 matches
- Confidence / limitations: local sim only (no jumping/jets, no beams, guessed house bots); shared-world counts are counterfactual per decision; paired worlds stop being comparable after divergence.

## Action-difference categories

- boost+move: 19
- move: 14

## First divergence per match

- seed 1000 t=17.4s [boost+move] label `zone fight 1 hp 860 tp-cover hp21% c0` hp 297.5/1400.0 visible 3 attackers {'1': 2.1, '8': 0.0}
  - base {"boost": true, "move": [-0.37529000971127563, -0.9269074433895278]} vs candidate {"boost": false, "move": [-0.881307902758908, 0.4725424642661177]}
  - +3 s base: hp +0.0, moved 18.9 m, new attackers -; candidate: hp +0.0, moved 14.1 m, new attackers -; reconverged after 1.5 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 16 t 25.4s cause gun; candidate place 16 t 24.9s cause gun
- seed 1001: no divergence
- seed 1002: no divergence
- seed 1003 t=68.9s [boost+move] label `zone fight 14 hp 146 tp-cover hp3% c2` hp 42.0/1512.0 visible 3 attackers {'6': 0.2}
  - base {"boost": true, "move": [-0.9624696765720985, 0.27138924385317836]} vs candidate {"boost": false, "move": [0.9498457313145718, 0.31271886208459837]}
  - +3 s base: hp +0.0; candidate: hp +0.0; no reconvergence
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 15 t 71.0s cause gun; candidate place 15 t 71.3s cause gun
- seed 1004 t=37.4s [boost+move] label `cube fight 8 hp 1400 tp-cover hp79% c0 chg` hp 1107.5/1400.0 visible 2 attackers {'1': 2.3}
  - base {"boost": false, "move": [-0.8255877342507144, -0.5642737749131815]} vs candidate {"boost": true, "move": [-0.9874746237551663, 0.15777790542275794]}
  - +3 s base: hp -90.0, moved 26.8 m, new attackers [8]; candidate: hp -45.0, moved 26.9 m, new attackers [8]; reconverged after 1.2 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 12 t 61.5s cause gun; candidate place 14 t 54.2s cause gun
- seed 1005: no divergence
