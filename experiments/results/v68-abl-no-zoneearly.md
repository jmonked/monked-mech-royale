# v68-abl-no-zoneearly

- Baseline: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `6f9ffa8db11719955f094ad82484115bdb0e8619`
- Official baseline: 4.73
- Official candidate: not recorded
- Matches tested: 6 (seeds 1000..1005)
- Decisions compared: 6250
- Differing decisions: 4
- Matches diverged: 1/6
- Most common action difference: move (3)
- First-divergence pattern: boost+move | zone scan zone-run x1
- Local outcome direction (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): candidate placed better in 0, worse in 0, same in 6 of 6 matches
- Confidence / limitations: local sim only (no jumping/jets, no beams, guessed house bots); shared-world counts are counterfactual per decision; paired worlds stop being comparable after divergence.

## Action-difference categories

- move: 3
- boost+move: 1

## First divergence per match

- seed 1000: no divergence
- seed 1001: no divergence
- seed 1002 t=105.2s [boost+move] label `zone scan zone-run hp100% c0` hp 1400.0/1400.0 visible 0 attackers -
  - base {"boost": true, "move": [-0.5448828501034209, -0.8385121821793485]} vs candidate {"boost": false, "move": [-0.544882850103421, -0.8385121821793484]}
  - +3 s base: hp -52.0, moved 15.0 m, new attackers -; candidate: hp -53.0, moved 17.6 m, new attackers -; reconverged after 1.3 s
  - end (LOCAL ONLY - NOT AN OFFICIAL SCORE PREDICTOR): base place 16 t 147.5s cause zone; candidate place 16 t 147.5s cause zone
- seed 1003: no divergence
- seed 1004: no divergence
- seed 1005: no divergence
