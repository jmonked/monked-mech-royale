# Corpus check - gate-076094f

- Base: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `C:\Users\julia\AppData\Local\Temp\tmplevhzop4\example_bot.py`
- Scenario corpus: 4556
- Candidate diverged: 101
- Clearly safer: 9
- Clearly worse: 0
- Neutral/uncertain: 92
- Catastrophic regressions: 0
- Action fields changed: {'move': 101}
- Activation tokens (in candidate label only): {'aggregate': 101}

| Category | identical | safer | worse | uncertain | catastrophic |
|---|---|---|---|---|---|
| combat-misc | 16 | 0 | 0 | 1 | 0 |
| cover-conflict | 531 | 0 | 0 | 11 | 0 |
| dodge-conflict | 497 | 2 | 0 | 11 | 0 |
| hypothesis | 960 | 5 | 0 | 35 | 0 |
| laser-crossfire | 516 | 0 | 0 | 5 | 0 |
| multi-threat | 694 | 0 | 0 | 18 | 0 |
| regression | 50 | 1 | 0 | 7 | 0 |
| sound-boundaries | 259 | 0 | 0 | 0 | 0 |
| unstick-conflict | 613 | 0 | 0 | 0 | 0 |
| zone-pressure | 319 | 1 | 0 | 4 | 0 |

## Reasons

- avoids walking at 2+ attackers: 9

## safer examples

- `dodge-conflict-laser-sidestep+unseen-multi-threat-s1010-t71.4` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 671 hp55% c2` [0.656, -0.755] -> cand `zone fight 1 hp 671 aggregate hp55% c2` [-0.933, -0.36]
- `dodge-conflict-bullet+2att-multi-threat-s1014-t119.5` ['avoids walking at 2+ attackers'] | base `zone fight 12 hp 950 hp37% c0` [0.366, 0.931] -> cand `zone fight 12 hp 950 aggregate hp37% c0` [-0.704, 0.71]
- `zone-pressure-edge+2att-multi-threat-s1023-t18.1` ['avoids walking at 2+ attackers'] | base `zone fight 7 hp 635 hp55% c0` [0.783, 0.622] -> cand `zone fight 7 hp 635 aggregate hp55% c0` [0.254, 0.967]
- `codex-v72-same-bearing-near-collinear` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 1400 hp93% c0` [0.819, -0.574] -> cand `zone fight 1 hp 1400 aggregate hp93% c0` [0.009, 1.0]
- `hyp-any` ['avoids walking at 2+ attackers'] | base `zone fight 2 hp 772 hp47% c6` [-0.933, 0.359] -> cand `zone fight 2 hp 772 aggregate hp47% c6` [-0.084, -0.997]
- `hyp-zone` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 657 hp88% c13` [-0.731, 0.682] -> cand `zone fight 1 hp 657 aggregate hp88% c13` [0.593, 0.805]
- `hyp-cover` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 458 hp94% c2` [-0.124, -0.992] -> cand `zone fight 1 hp 458 aggregate hp94% c2` [0.991, 0.132]
- `hyp-cover` ['avoids walking at 2+ attackers'] | base `zone fight 2 hp 557 hp23% c2` [0.987, 0.16] -> cand `zone fight 2 hp 557 aggregate hp23% c2` [0.073, 0.997]
- `hyp-multi` ['avoids walking at 2+ attackers'] | base `zone fight 3 hp 691 hp22% c9` [-0.945, 0.326] -> cand `zone fight 3 hp 691 aggregate hp22% c9` [-0.25, -0.968]
