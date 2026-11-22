# Corpus check - v61

- Base: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `cca2fdd781167b08518a6b0a07dc1fcc85d81f3e`
- Scenario corpus: 4472
- Candidate diverged: 1
- Clearly safer: 0
- Clearly worse: 0
- Neutral/uncertain: 1
- Catastrophic regressions: 0
- Action fields changed: {'boost': 1, 'move': 1}
- Activation tokens (in candidate label only): {'push': 1}
- Candidate tactical branch coverage: 355/490 (72.4%); changed lines reached: [1, 2]

| Category | identical | safer | worse | uncertain | catastrophic |
|---|---|---|---|---|---|
| cover-conflict | 540 | 0 | 0 | 0 | 0 |
| dodge-conflict | 500 | 0 | 0 | 0 | 0 |
| hypothesis | 999 | 0 | 0 | 1 | 0 |
| laser-crossfire | 514 | 0 | 0 | 0 | 0 |
| multi-threat | 711 | 0 | 0 | 0 | 0 |
| regression | 14 | 0 | 0 | 0 | 0 |
| sound-boundaries | 259 | 0 | 0 | 0 | 0 |
| unstick-conflict | 612 | 0 | 0 | 0 | 0 |
| zone-pressure | 322 | 0 | 0 | 0 | 0 |

## Reasons

