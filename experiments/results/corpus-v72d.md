# Corpus check - v72d

- Base: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `d46383e15244dbb08b9535a75f5b88c2ebfe3010`
- Scenario corpus: 4542
- Candidate diverged: 121
- Clearly safer: 14
- Clearly worse: 0
- Neutral/uncertain: 107
- Catastrophic regressions: 0
- Action fields changed: {'move': 121}
- Activation tokens (in candidate label only): {'aggregate': 121}
- Candidate tactical branch coverage: 468/548 (85.4%); changed lines reached: [103, 109]

| Category | identical | safer | worse | uncertain | catastrophic |
|---|---|---|---|---|---|
| combat-misc | 16 | 0 | 0 | 1 | 0 |
| cover-conflict | 527 | 0 | 0 | 15 | 0 |
| dodge-conflict | 495 | 2 | 0 | 13 | 0 |
| hypothesis | 954 | 7 | 0 | 39 | 0 |
| laser-crossfire | 516 | 0 | 0 | 5 | 0 |
| multi-threat | 689 | 0 | 0 | 23 | 0 |
| regression | 35 | 4 | 0 | 5 | 0 |
| sound-boundaries | 259 | 0 | 0 | 0 | 0 |
| unstick-conflict | 613 | 0 | 0 | 0 | 0 |
| zone-pressure | 317 | 1 | 0 | 6 | 0 |

## Reasons

- avoids walking at 2+ attackers: 14

## safer examples

- `dodge-conflict-laser-sidestep+unseen-multi-threat-s1010-t71.4` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 671 hp55% c2` [0.656, -0.755] -> cand `zone fight 1 hp 671 aggregate hp55% c2` [-0.933, -0.36]
- `dodge-conflict-bullet+2att-multi-threat-s1014-t119.5` ['avoids walking at 2+ attackers'] | base `zone fight 12 hp 950 hp37% c0` [0.366, 0.931] -> cand `zone fight 12 hp 950 aggregate hp37% c0` [-0.704, 0.71]
- `zone-pressure-edge+2att-multi-threat-s1023-t18.1` ['avoids walking at 2+ attackers'] | base `zone fight 7 hp 635 hp55% c0` [0.783, 0.622] -> cand `zone fight 7 hp 635 aggregate hp55% c0` [0.254, 0.967]
- `codex-v72-boosted-wall-outside-check` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 875 push hp100% c0` [0.819, -0.574] -> cand `zone fight 1 hp 875 push aggregate hp100% c0` [-0.009, 1.0]
- `codex-v72-ordinary-boosted-push` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 875 push hp100% c0` [0.819, -0.574] -> cand `zone fight 1 hp 875 push aggregate hp100% c0` [0.035, -0.999]
- `codex-v72-same-bearing-near-collinear` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 1400 hp93% c0` [0.819, -0.574] -> cand `zone fight 1 hp 1400 aggregate hp93% c0` [0.009, 1.0]
- `codex-v72-wall-directly-on-best-escape` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 875 push hp100% c0` [0.819, -0.574] -> cand `zone fight 1 hp 875 push aggregate hp100% c0` [0.009, -1.0]
- `hyp-any` ['avoids walking at 2+ attackers'] | base `zone fight 2 hp 772 hp47% c6` [-0.933, 0.359] -> cand `zone fight 2 hp 772 aggregate hp47% c6` [-0.084, -0.997]
- `hyp-zone` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 657 hp88% c13` [-0.731, 0.682] -> cand `zone fight 1 hp 657 aggregate hp88% c13` [0.593, 0.805]
- `hyp-cover` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 434 push hp87% c15` [1.0, -0.006] -> cand `zone fight 1 hp 434 push aggregate hp87% c15` [-0.213, -0.977]
- `hyp-any` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 762 push hp100% c16` [0.357, 0.934] -> cand `zone fight 1 hp 762 push aggregate hp100% c16` [-0.616, 0.788]
- `hyp-cover` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 458 hp94% c2` [-0.124, -0.992] -> cand `zone fight 1 hp 458 aggregate hp94% c2` [0.991, 0.132]
