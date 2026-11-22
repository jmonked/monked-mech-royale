# Corpus check - v72b

- Base: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `50801ce96314bb18268cce6228b80d741e252c6a`
- Scenario corpus: 4472
- Candidate diverged: 244
- Clearly safer: 29
- Clearly worse: 12
- Neutral/uncertain: 190
- Catastrophic regressions: 13
- Action fields changed: {'move': 244}
- Activation tokens (in candidate label only): {'aggregate': 244}

| Category | identical | safer | worse | uncertain | catastrophic |
|---|---|---|---|---|---|
| cover-conflict | 512 | 3 | 0 | 24 | 1 |
| dodge-conflict | 474 | 3 | 2 | 20 | 1 |
| hypothesis | 920 | 11 | 4 | 60 | 5 |
| laser-crossfire | 494 | 2 | 0 | 16 | 2 |
| multi-threat | 661 | 0 | 1 | 49 | 0 |
| regression | 14 | 0 | 0 | 0 | 0 |
| sound-boundaries | 259 | 0 | 0 | 0 | 0 |
| unstick-conflict | 593 | 2 | 4 | 9 | 4 |
| zone-pressure | 301 | 8 | 1 | 12 | 0 |

## Reasons

- avoids walking at 2+ attackers: 21
- walks straight at an active attacker: 16
- steps out of live laser line: 11
- C2 walks at 2+ attackers: 9
- C4 steps into live laser line: 4
- stays in next circle: 1

## catastrophic examples

- `laser-crossfire-2lasers-multi-threat-s1011-t10.7` ['C4 steps into live laser line'] | base `zone fight 9 hp 860 hp65% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp65% c0` [-0.731, -0.683]
- `laser-crossfire-2lasers-multi-threat-s1011-t13.4` ['C4 steps into live laser line'] | base `zone fight 9 hp 500 hp42% c0` [-0.708, -0.706] -> cand `zone fight 9 hp 500 aggregate hp42% c0` [-0.776, 0.63]
- `dodge-conflict-laser-sidestep+unseen-multi-threat-s1011-t13.4` ['C4 steps into live laser line'] | base `zone fight 9 hp 500 hp42% c0` [-0.708, -0.706] -> cand `zone fight 9 hp 500 aggregate hp42% c0` [-1.0, -0.027]
- `cover-conflict-tp+charging-multi-threat-s1011-t13.4` ['C4 steps into live laser line'] | base `zone fight 9 hp 500 hp42% c0` [-0.708, -0.706] -> cand `zone fight 9 hp 500 aggregate hp42% c0` [-0.947, 0.321]
- `unstick-conflict-stalled+2att-multi-threat-s1000-t15.8` ['C2 walks at 2+ attackers'] | base `zone fight 1 hp 860 hp47% c0` [-0.413, -0.911] -> cand `zone fight 1 hp 860 aggregate hp47% c0` [0.184, -0.983]
- `unstick-conflict-stalled+2att-multi-threat-s1023-t17.2` ['C2 walks at 2+ attackers'] | base `laser hunt fight 7 hp 770 hp61% c0` [-0.987, -0.162] -> cand `laser hunt fight 7 hp 770 aggregate hp61% c0` [0.802, 0.597]
- `unstick-conflict-stalled+2att-multi-threat-s1023-t18.1` ['C2 walks at 2+ attackers'] | base `zone fight 7 hp 635 hp55% c0` [-0.786, 0.619] -> cand `zone fight 7 hp 635 aggregate hp55% c0` [0.863, 0.505]
- `unstick-conflict-stalled+2att-multi-threat-s1023-t18.4` ['C2 walks at 2+ attackers'] | base `zone fight 7 hp 635 hp49% c0` [-0.782, 0.623] -> cand `zone fight 7 hp 635 aggregate hp49% c0` [0.882, 0.471]
- `hyp-unstick` ['C2 walks at 2+ attackers'] | base `zone fight 2 hp 471 hp56% c8` [-0.938, -0.346] -> cand `zone fight 2 hp 471 aggregate hp56% c8` [0.734, -0.68]
- `hyp-any` ['C2 walks at 2+ attackers'] | base `zone fight 1 hp 528 hp60% c16` [0.721, 0.693] -> cand `zone fight 1 hp 528 aggregate hp60% c16` [0.897, -0.443]
- `hyp-unstick` ['C2 walks at 2+ attackers'] | base `zone fight 1 hp 675 hp57% c11` [0.996, -0.087] -> cand `zone fight 1 hp 675 aggregate hp57% c11` [0.402, 0.916]
- `hyp-unstick` ['C2 walks at 2+ attackers'] | base `zone fight 3 hp 433 hp98% c3` [-0.797, -0.604] -> cand `zone fight 3 hp 433 aggregate hp98% c3` [-0.253, 0.967]

## worse examples

- `multi-threat-3att-unseen-multi-threat-s1011-t13.4` ['walks straight at an active attacker'] | base `zone fight 9 hp 500 hp42% c0` [-0.708, -0.706] -> cand `zone fight 9 hp 500 aggregate hp42% c0` [-0.988, 0.157]
- `dodge-conflict-laser-sidestep+unseen-multi-threat-s1011-t10.4` ['walks straight at an active attacker'] | base `zone fight 9 hp 860 hp69% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp69% c0` [-0.881, 0.473]
- `dodge-conflict-bullet+2att-multi-threat-s1011-t13.4` ['walks straight at an active attacker'] | base `zone fight 9 hp 500 hp42% c0` [-0.708, -0.706] -> cand `zone fight 9 hp 500 aggregate hp42% c0` [0.687, -0.727]
- `unstick-conflict-stalled+2att-multi-threat-s1010-t71.4` ['walks straight at an active attacker'] | base `zone fight 1 hp 671 hp55% c2` [-0.755, -0.656] -> cand `zone fight 1 hp 671 aggregate hp55% c2` [-0.995, -0.104]
- `unstick-conflict-stalled+2att-multi-threat-s1011-t11.0` ['walks straight at an active attacker'] | base `zone fight 9 hp 860 hp58% c0` [-0.708, -0.706] -> cand `zone fight 9 hp 860 aggregate hp58% c0` [-0.894, 0.447]
- `unstick-conflict-stalled+2att-multi-threat-s1011-t11.6` ['walks straight at an active attacker'] | base `zone fight 9 hp 815 hp52% c0` [-0.708, -0.706] -> cand `zone fight 9 hp 815 aggregate hp52% c0` [-0.998, -0.055]
- `unstick-conflict-stalled+2att-multi-threat-s1021-t76.8` ['walks straight at an active attacker'] | base `cube fight 10 hp 1400 hp6% c2` [0.432, -0.902] -> cand `cube fight 10 hp 1400 aggregate hp6% c2` [-0.054, 0.999]
- `zone-pressure-edge+2att-cover-conflict-s1014-t119.8` ['walks straight at an active attacker'] | base `zone fight 12 hp 905 hp26% c0` [0.58, -0.815] -> cand `zone fight 12 hp 905 aggregate hp26% c0` [-0.684, -0.73]
- `hyp-unstick` ['walks straight at an active attacker'] | base `zone fight 2 hp 444 hp13% c11` [0.753, 0.658] -> cand `zone fight 2 hp 444 aggregate hp13% c11` [-0.563, 0.826]
- `hyp-cover` ['walks straight at an active attacker'] | base `zone fight 2 hp 1033 hp68% c13` [0.999, 0.036] -> cand `zone fight 2 hp 1033 aggregate hp68% c13` [0.56, 0.829]
- `hyp-unstick` ['walks straight at an active attacker'] | base `zone fight 1 hp 1232 hp84% c16` [0.961, -0.276] -> cand `zone fight 1 hp 1232 aggregate hp84% c16` [-0.51, -0.86]
- `hyp-multi` ['walks straight at an active attacker'] | base `zone fight 2 hp 815 hp29% c0` [-0.917, 0.398] -> cand `zone fight 2 hp 815 aggregate hp29% c0` [-0.111, -0.994]

## safer examples

- `laser-crossfire-laser+gun-multi-threat-s1011-t11.0` ['steps out of live laser line'] | base `zone fight 9 hp 860 hp58% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp58% c0` [0.447, 0.894]
- `laser-crossfire-2lasers-multi-threat-s1011-t11.0` ['steps out of live laser line'] | base `zone fight 9 hp 860 hp58% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp58% c0` [0.447, 0.894]
- `dodge-conflict-laser-sidestep+unseen-multi-threat-s1010-t71.4` ['avoids walking at 2+ attackers'] | base `zone fight 1 hp 671 hp55% c2` [0.656, -0.755] -> cand `zone fight 1 hp 671 aggregate hp55% c2` [-0.933, -0.36]
- `dodge-conflict-laser-sidestep+unseen-multi-threat-s1011-t11.0` ['steps out of live laser line'] | base `zone fight 9 hp 860 hp58% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp58% c0` [0.562, 0.827]
- `dodge-conflict-bullet+2att-multi-threat-s1014-t119.5` ['avoids walking at 2+ attackers'] | base `zone fight 12 hp 950 hp37% c0` [0.366, 0.931] -> cand `zone fight 12 hp 950 aggregate hp37% c0` [-0.704, 0.71]
- `cover-conflict-tp+charging-multi-threat-s1011-t11.0` ['steps out of live laser line'] | base `zone fight 9 hp 860 hp58% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 860 aggregate hp58% c0` [0.447, 0.894]
- `cover-conflict-tp+charging-multi-threat-s1011-t11.6` ['steps out of live laser line'] | base `zone fight 9 hp 815 hp52% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 815 aggregate hp52% c0` [0.667, 0.745]
- `cover-conflict-tp+charging-multi-threat-s1011-t11.9` ['steps out of live laser line'] | base `zone fight 9 hp 770 hp49% c0` [-0.706, 0.708] -> cand `zone fight 9 hp 770 aggregate hp49% c0` [0.454, 0.891]
- `unstick-conflict-stalled+2att-multi-threat-s1023-t13.1` ['avoids walking at 2+ attackers'] | base `laser hunt fight 7 hp 1175 hp78% c0` [0.999, -0.038] -> cand `laser hunt fight 7 hp 1175 aggregate hp78% c0` [0.208, 0.978]
- `unstick-conflict-stalled+2att-multi-threat-s1023-t14.6` ['avoids walking at 2+ attackers'] | base `laser hunt fight 7 hp 1175 hp78% c0` [0.999, 0.032] -> cand `laser hunt fight 7 hp 1175 aggregate hp78% c0` [-0.02, 1.0]
- `zone-pressure-edge+2att-multi-threat-s1011-t11.0` ['avoids walking at 2+ attackers'] | base `laser hunt fight 9 hp 860 hp58% c0` [0.917, -0.398] -> cand `laser hunt fight 9 hp 860 aggregate hp58% c0` [0.447, 0.894]
- `zone-pressure-edge+2att-multi-threat-s1011-t11.3` ['avoids walking at 2+ attackers'] | base `laser hunt fight 9 hp 860 hp55% c0` [0.913, -0.409] -> cand `laser hunt fight 9 hp 860 aggregate hp55% c0` [0.506, 0.863]
