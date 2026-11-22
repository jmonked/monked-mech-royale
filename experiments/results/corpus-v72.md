# Corpus check - v72

- Base: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `a027c8c9ef4ced5884d51446c4fc440682ee4bd4`
- Scenario corpus: 4472
- Candidate diverged: 296
- Clearly safer: 45
- Clearly worse: 23
- Neutral/uncertain: 192
- Catastrophic regressions: 36
- Action fields changed: {'move': 296}
- Activation tokens (in candidate label only): {'aggregate': 296}
- Candidate tactical branch coverage: 395/536 (73.7%); changed lines reached: [84, 91]

| Category | identical | safer | worse | uncertain | catastrophic |
|---|---|---|---|---|---|
| cover-conflict | 503 | 10 | 2 | 21 | 4 |
| dodge-conflict | 469 | 5 | 4 | 16 | 6 |
| hypothesis | 920 | 11 | 4 | 60 | 5 |
| laser-crossfire | 487 | 4 | 2 | 11 | 10 |
| multi-threat | 651 | 2 | 3 | 53 | 2 |
| regression | 14 | 0 | 0 | 0 | 0 |
| sound-boundaries | 259 | 0 | 0 | 0 | 0 |
| unstick-conflict | 591 | 2 | 4 | 11 | 4 |
| zone-pressure | 282 | 11 | 4 | 20 | 5 |

## Reasons

- walks straight at an active attacker: 26
- avoids walking at 2+ attackers: 24
- steps out of live laser line: 20
- C2 walks at 2+ attackers: 19
- C4 steps into live laser line: 18
- stays in next circle: 4

## catastrophic examples

- `multi-threat-3att-unseen-multi-threat-s1019-t47.1` ['C2 walks at 2+ attackers'] | base `zone fight 2 hp 1220 hp13% c0` [0.607, -0.795] -> cand `zone fight 2 hp 1220 aggregate hp13% c0` [0.922, 0.387]
- `multi-threat-3att-unseen-multi-threat-s1021-t76.5` ['C2 walks at 2+ attackers'] | base `cube fight 10 hp 1400 hp9% c2` [0.586, -0.81] -> cand `cube fight 10 hp 1400 aggregate hp9% c2` [0.146, -0.989]
- `laser-crossfire-laser+gun-multi-threat-s1000-t15.2` ['C4 steps into live laser line'] | base `zone fight 1 hp 860 hp60% c0` [-0.905, 0.426] -> cand `zone fight 1 hp 860 aggregate hp60% c0` [-0.94, -0.341]
- `laser-crossfire-laser+gun-multi-threat-s1000-t15.5` ['C4 steps into live laser line'] | base `zone fight 1 hp 860 hp52% c0` [-0.908, 0.42] -> cand `zone fight 1 hp 860 aggregate hp52% c0` [-0.946, -0.325]
- `laser-crossfire-2lasers-multi-threat-s1000-t15.8` ['C4 steps into live laser line'] | base `zone fight 1 hp 860 hp47% c0` [-0.911, 0.413] -> cand `zone fight 1 hp 860 aggregate hp47% c0` [-0.953, -0.302]
- `laser-crossfire-2lasers-multi-threat-s1009-t46.7` ['C4 steps into live laser line'] | base `laser hunt fight 1 hp 1085 hp26% c0` [-0.651, 0.759] -> cand `laser hunt fight 1 hp 1085 aggregate hp26% c0` [-0.688, -0.726]
- `laser-crossfire-2lasers-multi-threat-s1011-t10.1` ['C4 steps into live laser line'] | base `zone fight 9 hp 860 hp76% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp76% c0` [0.121, 0.993]
- `laser-crossfire-2lasers-multi-threat-s1011-t10.7` ['C4 steps into live laser line'] | base `zone fight 9 hp 860 hp65% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp65% c0` [-0.731, -0.683]
- `laser-crossfire-2lasers-multi-threat-s1011-t11.0` ['C4 steps into live laser line'] | base `zone fight 9 hp 860 hp58% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp58% c0` [0.447, 0.894]
- `laser-crossfire-2lasers-multi-threat-s1011-t11.6` ['C4 steps into live laser line'] | base `zone fight 9 hp 815 hp52% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 815 aggregate hp52% c0` [0.667, 0.745]
- `laser-crossfire-laser+gun-multi-threat-s1011-t13.4` ['C4 steps into live laser line'] | base `zone fight 9 hp 500 hp42% c0` [-0.708, -0.706] -> cand `zone fight 9 hp 500 aggregate hp42% c0` [-0.913, 0.409]
- `laser-crossfire-2lasers-multi-threat-s1011-t13.4` ['C4 steps into live laser line', 'C4 steps into live laser line'] | base `zone fight 9 hp 500 hp42% c0` [-0.708, -0.706] -> cand `zone fight 9 hp 500 aggregate hp42% c0` [-0.776, 0.63]

## worse examples

- `multi-threat-3att-unseen-multi-threat-s1011-t13.4` ['walks straight at an active attacker'] | base `zone fight 9 hp 500 hp42% c0` [-0.708, -0.706] -> cand `zone fight 9 hp 500 aggregate hp42% c0` [-0.988, 0.157]
- `multi-threat-2att-multi-threat-s1021-t76.8` ['walks straight at an active attacker'] | base `cube fight 10 hp 1400 hp6% c2` [0.432, -0.902] -> cand `cube fight 10 hp 1400 aggregate hp6% c2` [-0.054, 0.999]
- `multi-threat-3att-unseen-cover-conflict-s1003-t70.3` ['walks straight at an active attacker'] | base `zone fight 14 hp 150 hp3% c2` [-0.165, 0.986] -> cand `zone fight 14 hp 150 aggregate hp3% c2` [-0.797, 0.604]
- `laser-crossfire-laser+gun-multi-threat-s1021-t76.8` ['walks straight at an active attacker'] | base `cube fight 10 hp 1400 hp6% c2` [0.432, -0.902] -> cand `cube fight 10 hp 1400 aggregate hp6% c2` [-0.054, 0.999]
- `laser-crossfire-2lasers-multi-threat-s1021-t76.8` ['walks straight at an active attacker'] | base `cube fight 10 hp 1400 hp6% c2` [0.432, -0.902] -> cand `cube fight 10 hp 1400 aggregate hp6% c2` [-0.054, 0.999]
- `dodge-conflict-laser-sidestep+unseen-multi-threat-s1011-t10.4` ['walks straight at an active attacker'] | base `zone fight 9 hp 860 hp69% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp69% c0` [-0.881, 0.473]
- `dodge-conflict-bullet+2att-multi-threat-s1011-t13.4` ['walks straight at an active attacker'] | base `zone fight 9 hp 500 hp42% c0` [-0.708, -0.706] -> cand `zone fight 9 hp 500 aggregate hp42% c0` [0.687, -0.727]
- `dodge-conflict-bullet+2att-multi-threat-s1019-t46.8` ['walks straight at an active attacker'] | base `zone fight 2 hp 1220 hp13% c0` [0.616, -0.788] -> cand `zone fight 2 hp 1220 aggregate hp13% c0` [-0.777, -0.629]
- `dodge-conflict-bullet+2att-multi-threat-s1021-t76.5` ['walks straight at an active attacker'] | base `cube fight 10 hp 1400 hp9% c2` [0.586, -0.81] -> cand `cube fight 10 hp 1400 aggregate hp9% c2` [-0.14, 0.99]
- `cover-conflict-reload+2nd-multi-threat-s1021-t76.8` ['walks straight at an active attacker'] | base `cube fight 10 hp 1400 hp6% c2` [0.432, -0.902] -> cand `cube fight 10 hp 1400 aggregate hp6% c2` [-0.054, 0.999]
- `cover-conflict-tp+charging-multi-threat-s1021-t76.8` ['walks straight at an active attacker'] | base `cube fight 10 hp 1400 hp6% c2` [0.432, -0.902] -> cand `cube fight 10 hp 1400 aggregate hp6% c2` [-0.054, 0.999]
- `unstick-conflict-stalled+2att-multi-threat-s1010-t71.4` ['walks straight at an active attacker'] | base `zone fight 1 hp 671 hp55% c2` [-0.755, -0.656] -> cand `zone fight 1 hp 671 aggregate hp55% c2` [-0.995, -0.104]

## safer examples

- `multi-threat-2att-multi-threat-s1023-t14.6` ['avoids walking at 2+ attackers'] | base `laser hunt fight 7 hp 1175 hp78% c0` [0.999, 0.032] -> cand `laser hunt fight 7 hp 1175 aggregate hp78% c0` [-0.02, 1.0]
- `multi-threat-3att-unseen-multi-threat-s1023-t14.6` ['avoids walking at 2+ attackers'] | base `laser hunt fight 7 hp 1175 hp78% c0` [0.999, 0.032] -> cand `laser hunt fight 7 hp 1175 aggregate hp78% c0` [-0.686, -0.727]
- `laser-crossfire-laser+gun-multi-threat-s1011-t11.0` ['steps out of live laser line'] | base `zone fight 9 hp 860 hp58% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp58% c0` [0.447, 0.894]
- `laser-crossfire-laser+gun-multi-threat-s1011-t11.3` ['steps out of live laser line'] | base `zone fight 9 hp 860 hp55% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp55% c0` [0.261, 0.965]
- `laser-crossfire-laser+gun-cover-conflict-s1021-t76.5` ['steps out of live laser line'] | base `cube fight 10 hp 1400 hp9% c2` [0.586, -0.81] -> cand `cube fight 10 hp 1400 aggregate hp9% c2` [-0.14, 0.99]
- `laser-crossfire-2lasers-cover-conflict-s1021-t76.5` ['steps out of live laser line'] | base `cube fight 10 hp 1400 hp9% c2` [0.586, -0.81] -> cand `cube fight 10 hp 1400 aggregate hp9% c2` [-0.14, 0.99]
- `dodge-conflict-laser-sidestep+unseen-multi-threat-s1000-t15.8` ['steps out of live laser line'] | base `zone fight 1 hp 860 hp47% c0` [-0.911, 0.413] -> cand `zone fight 1 hp 860 aggregate hp47% c0` [-0.983, -0.184]
- `dodge-conflict-laser-sidestep+unseen-multi-threat-s1010-t71.4` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 671 hp55% c2` [0.656, -0.755] -> cand `zone fight 1 hp 671 aggregate hp55% c2` [-0.933, -0.36]
- `dodge-conflict-laser-sidestep+unseen-multi-threat-s1011-t11.0` ['steps out of live laser line'] | base `zone fight 9 hp 860 hp58% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp58% c0` [0.562, 0.827]
- `dodge-conflict-bullet+2att-multi-threat-s1014-t119.5` ['avoids walking at 2+ attackers'] | base `zone fight 12 hp 950 hp37% c0` [0.366, 0.931] -> cand `zone fight 12 hp 950 aggregate hp37% c0` [-0.704, 0.71]
- `dodge-conflict-laser-sidestep+unseen-cover-conflict-s1021-t76.5` ['steps out of live laser line'] | base `cube fight 10 hp 1400 hp9% c2` [0.586, -0.81] -> cand `cube fight 10 hp 1400 aggregate hp9% c2` [0.158, -0.987]
- `cover-conflict-tp+charging-multi-threat-s1000-t15.8` ['steps out of live laser line'] | base `zone fight 1 hp 860 hp47% c0` [-0.911, 0.413] -> cand `zone fight 1 hp 860 aggregate hp47% c0` [-0.983, -0.184]
