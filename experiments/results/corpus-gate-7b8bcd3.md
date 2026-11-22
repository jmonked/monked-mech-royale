# Corpus check - gate-7b8bcd3

- Base: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `C:\Users\julia\AppData\Local\Temp\tmpw7zzfnsr\example_bot.py`
- Scenario corpus: 4512
- Candidate diverged: 194
- Clearly safer: 26
- Clearly worse: 1
- Neutral/uncertain: 167
- Catastrophic regressions: 0
- Action fields changed: {'move': 194}
- Activation tokens (in candidate label only): {'aggregate': 194}

| Category | identical | safer | worse | uncertain | catastrophic |
|---|---|---|---|---|---|
| combat-misc | 16 | 0 | 0 | 1 | 0 |
| cover-conflict | 516 | 3 | 0 | 23 | 0 |
| dodge-conflict | 486 | 3 | 1 | 20 | 0 |
| hypothesis | 941 | 10 | 0 | 49 | 0 |
| laser-crossfire | 503 | 2 | 0 | 16 | 0 |
| multi-threat | 665 | 0 | 0 | 47 | 0 |
| regression | 14 | 0 | 0 | 0 | 0 |
| sound-boundaries | 259 | 0 | 0 | 0 | 0 |
| unstick-conflict | 613 | 0 | 0 | 0 | 0 |
| zone-pressure | 305 | 8 | 0 | 11 | 0 |

## Reasons

- avoids walking at 2+ attackers: 19
- steps out of live laser line: 11
- walks straight at an active attacker: 5

## worse examples

- `dodge-conflict-laser-sidestep+unseen-multi-threat-s1011-t10.4` ['walks straight at an active attacker'] | base `zone fight 9 hp 860 hp69% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp69% c0` [-0.881, 0.473]

## safer examples

- `laser-crossfire-laser+gun-multi-threat-s1011-t11.0` ['steps out of live laser line'] | base `zone fight 9 hp 860 hp58% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp58% c0` [0.447, 0.894]
- `laser-crossfire-2lasers-multi-threat-s1011-t11.0` ['steps out of live laser line'] | base `zone fight 9 hp 860 hp58% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp58% c0` [0.447, 0.894]
- `dodge-conflict-laser-sidestep+unseen-multi-threat-s1010-t71.4` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 671 hp55% c2` [0.656, -0.755] -> cand `zone fight 1 hp 671 aggregate hp55% c2` [-0.933, -0.36]
- `dodge-conflict-laser-sidestep+unseen-multi-threat-s1011-t11.0` ['steps out of live laser line'] | base `zone fight 9 hp 860 hp58% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp58% c0` [0.562, 0.827]
- `dodge-conflict-bullet+2att-multi-threat-s1014-t119.5` ['avoids walking at 2+ attackers'] | base `zone fight 12 hp 950 hp37% c0` [0.366, 0.931] -> cand `zone fight 12 hp 950 aggregate hp37% c0` [-0.704, 0.71]
- `cover-conflict-tp+charging-multi-threat-s1011-t11.0` ['steps out of live laser line'] | base `zone fight 9 hp 860 hp58% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp58% c0` [0.447, 0.894]
- `cover-conflict-tp+charging-multi-threat-s1011-t11.6` ['steps out of live laser line'] | base `zone fight 9 hp 815 hp52% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 815 aggregate hp52% c0` [0.667, 0.745]
- `cover-conflict-tp+charging-multi-threat-s1011-t11.9` ['steps out of live laser line'] | base `zone fight 9 hp 770 hp49% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 770 aggregate hp49% c0` [0.454, 0.891]
- `zone-pressure-edge+2att-multi-threat-s1011-t11.0` ['avoids walking at 2+ attackers'] | base `laser hunt fight 9 hp 860 hp58% c0` [0.917, -0.398] -> cand `laser hunt fight 9 hp 860 aggregate hp58% c0` [0.447, 0.894]
- `zone-pressure-edge+2att-multi-threat-s1011-t11.3` ['avoids walking at 2+ attackers'] | base `laser hunt fight 9 hp 860 hp55% c0` [0.913, -0.409] -> cand `laser hunt fight 9 hp 860 aggregate hp55% c0` [0.506, 0.863]
- `zone-pressure-edge+2att-multi-threat-s1011-t11.6` ['avoids walking at 2+ attackers'] | base `laser hunt fight 9 hp 815 hp52% c0` [0.908, -0.419] -> cand `laser hunt fight 9 hp 815 aggregate hp52% c0` [0.667, 0.745]
- `zone-pressure-edge+2att-multi-threat-s1014-t118.6` ['avoids walking at 2+ attackers'] | base `zone fight 12 hp 1130 hp56% c0` [0.258, 0.966] -> cand `zone fight 12 hp 1130 aggregate hp56% c0` [0.984, 0.181]
