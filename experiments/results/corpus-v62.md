# Corpus check - v62

- Base: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `a023e35a15df4f425691bb2c8fdee257063e78a3`
- Scenario corpus: 4542
- Candidate diverged: 1698
- Clearly safer: 241
- Clearly worse: 125
- Neutral/uncertain: 1238
- Catastrophic regressions: 94
- Action fields changed: {'move': 1698}
- Activation tokens (in candidate label only): {'aggregate': 1841}
- Candidate tactical branch coverage: 451/528 (85.4%); changed lines reached: [82, 84]

| Category | identical | safer | worse | uncertain | catastrophic |
|---|---|---|---|---|---|
| combat-misc | 17 | 0 | 0 | 0 | 0 |
| cover-conflict | 234 | 47 | 25 | 219 | 17 |
| dodge-conflict | 233 | 37 | 21 | 205 | 14 |
| hypothesis | 804 | 32 | 7 | 154 | 3 |
| laser-crossfire | 254 | 21 | 18 | 219 | 9 |
| multi-threat | 352 | 46 | 25 | 272 | 17 |
| regression | 15 | 8 | 0 | 19 | 2 |
| sound-boundaries | 259 | 0 | 0 | 0 | 0 |
| unstick-conflict | 473 | 26 | 21 | 76 | 17 |
| zone-pressure | 203 | 24 | 8 | 74 | 15 |

## Reasons

- avoids walking at 2+ attackers: 234
- walks straight at an active attacker: 125
- C2 walks at 2+ attackers: 60
- C6 boosts into a wall: 28
- C5 leaves next circle: 7
- stays in next circle: 6
- steps out of live laser line: 3
- C4 steps into live laser line: 2

## catastrophic examples

- `multi-threat-s1009-t46.7` ['C6 boosts into a wall'] | base `laser hunt fight 1 hp 1085 hp26% c0` [-0.651, 0.759] -> cand `laser hunt fight 1 hp 1085 aggregate hp26% c0` [0.852, -0.524]
- `multi-threat-3att-unseen-multi-threat-s1004-t57.9` ['C6 boosts into a wall'] | base `zone fight 3 hp 424 tp-cover hp18% c6` [0.546, -0.838] -> cand `zone fight 3 hp 424 tp-cover aggregate hp18% c6` [-0.523, 0.852]
- `multi-threat-2att-multi-threat-s1006-t213.0` ['C2 walks at 2+ attackers'] | base `drop-walk fight 14 hp 1400 tp-cover hp52% c6 chg` [-0.66, 0.751] -> cand `drop-walk fight 14 hp 1400 tp-cover aggregate hp52% c6 chg` [0.341, 0.94]
- `multi-threat-3att-unseen-multi-threat-s1006-t213.0` ['C2 walks at 2+ attackers'] | base `drop-walk fight 14 hp 1400 tp-cover hp52% c6 chg` [-0.545, 0.839] -> cand `drop-walk fight 14 hp 1400 tp-cover aggregate hp52% c6 chg` [0.648, 0.762]
- `multi-threat-3att-unseen-multi-threat-s1011-t13.4` ['C2 walks at 2+ attackers'] | base `zone fight 9 hp 500 hp42% c0` [-0.708, -0.706] -> cand `zone fight 9 hp 500 aggregate hp42% c0` [0.587, -0.809]
- `multi-threat-2att-multi-threat-s1014-t120.4` ['C2 walks at 2+ attackers'] | base `zone fight 12 hp 860 tp-cover hp1% c0` [0.97, -0.245] -> cand `zone fight 12 hp 860 tp-cover aggregate hp1% c0` [-0.148, 0.989]
- `multi-threat-2att-multi-threat-s1018-t48.6` ['C2 walks at 2+ attackers'] | base `zone fight 13 hp 734 hp7% c2 chg` [-0.452, -0.892] -> cand `zone fight 13 hp 734 aggregate hp7% c2 chg` [0.681, 0.732]
- `multi-threat-3att-unseen-multi-threat-s1018-t48.6` ['C2 walks at 2+ attackers'] | base `zone fight 13 hp 734 hp7% c2 chg` [-0.452, -0.892] -> cand `zone fight 13 hp 734 aggregate hp7% c2 chg` [0.681, 0.732]
- `multi-threat-3att-unseen-multi-threat-s1021-t73.2` ['C2 walks at 2+ attackers'] | base `drop-walk fight 1 hp 627 tp-cover hp69% c2` [0.541, 0.841] -> cand `drop-walk fight 1 hp 627 tp-cover aggregate hp69% c2` [0.27, 0.963]
- `multi-threat-2att-multi-threat-s1023-t12.8` ['C2 walks at 2+ attackers'] | base `laser hunt fight 7 hp 1175 tp-cover hp81% c0` [-0.125, 0.992] -> cand `laser hunt fight 7 hp 1175 tp-cover aggregate hp81% c0` [0.999, 0.047]
- `multi-threat-3att-unseen-cover-conflict-s1004-t57.8` ['C6 boosts into a wall'] | base `zone fight 3 hp 424 tp-cover hp18% c6` [0.961, 0.278] -> cand `zone fight 3 hp 424 tp-cover aggregate hp18% c6` [-0.496, 0.868]
- `multi-threat-2att-cover-conflict-s1010-t73.4` ['C2 walks at 2+ attackers'] | base `zone fight 1 hp 574 tp-cover hp46% c2 chg` [-0.439, -0.898] -> cand `zone fight 1 hp 574 tp-cover aggregate hp46% c2 chg` [-0.258, 0.966]

## worse examples

- `multi-threat-s1010-t72.9` ['walks straight at an active attacker'] | base `zone fight 1 hp 574 tp-cover hp46% c2 chg` [-0.442, -0.897] -> cand `zone fight 1 hp 574 tp-cover aggregate hp46% c2 chg` [0.998, 0.064]
- `multi-threat-s1010-t73.2` ['walks straight at an active attacker'] | base `zone fight 1 hp 574 tp-cover hp46% c2 chg` [-0.446, -0.895] -> cand `zone fight 1 hp 574 tp-cover aggregate hp46% c2 chg` [0.995, 0.098]
- `multi-threat-s1018-t48.6` ['walks straight at an active attacker'] | base `zone fight 13 hp 734 hp7% c2 chg` [-0.452, -0.892] -> cand `zone fight 13 hp 734 aggregate hp7% c2 chg` [0.681, 0.732]
- `multi-threat-s1021-t76.5` ['walks straight at an active attacker'] | base `cube fight 10 hp 1400 tp-cover hp9% c2` [0.585, -0.811] -> cand `cube fight 10 hp 1400 tp-cover aggregate hp9% c2` [-0.14, 0.99]
- `multi-threat-s1021-t76.8` ['walks straight at an active attacker'] | base `cube fight 10 hp 1400 tp-cover hp6% c2` [0.454, -0.891] -> cand `cube fight 10 hp 1400 tp-cover aggregate hp6% c2` [-0.054, 0.999]
- `multi-threat-2att-multi-threat-s1010-t73.2` ['walks straight at an active attacker'] | base `zone fight 1 hp 574 tp-cover hp46% c2 chg` [-0.127, -0.992] -> cand `zone fight 1 hp 574 tp-cover aggregate hp46% c2 chg` [0.993, -0.121]
- `multi-threat-2att-multi-threat-s1014-t120.1` ['walks straight at an active attacker'] | base `zone fight 12 hp 860 tp-cover hp15% c0` [0.995, -0.1] -> cand `zone fight 12 hp 860 tp-cover aggregate hp15% c0` [0.577, -0.817]
- `multi-threat-3att-unseen-multi-threat-s1014-t120.1` ['walks straight at an active attacker'] | base `zone fight 12 hp 860 tp-cover hp15% c0` [0.995, -0.1] -> cand `zone fight 12 hp 860 tp-cover aggregate hp15% c0` [0.219, -0.976]
- `multi-threat-3att-unseen-multi-threat-s1019-t46.5` ['walks straight at an active attacker'] | base `zone fight 2 hp 1220 hp13% c0` [0.62, -0.784] -> cand `zone fight 2 hp 1220 aggregate hp13% c0` [0.681, -0.733]
- `multi-threat-3att-unseen-multi-threat-s1019-t47.1` ['walks straight at an active attacker'] | base `zone fight 2 hp 1220 hp13% c0` [0.607, -0.795] -> cand `zone fight 2 hp 1220 aggregate hp13% c0` [0.926, -0.379]
- `multi-threat-2att-multi-threat-s1021-t76.8` ['walks straight at an active attacker'] | base `cube fight 10 hp 1400 hp6% c2` [0.432, -0.902] -> cand `cube fight 10 hp 1400 aggregate hp6% c2` [-0.054, 0.999]
- `multi-threat-3att-unseen-multi-threat-s1023-t12.8` ['walks straight at an active attacker'] | base `laser hunt fight 7 hp 1175 hp81% c0` [-1.0, 0.021] -> cand `laser hunt fight 7 hp 1175 aggregate hp81% c0` [0.346, -0.938]

## safer examples

- `multi-threat-s1004-t57.3` ['avoids walking at 2+ attackers'] | base `zone fight 3 hp 571 tp-cover hp25% c6` [0.973, 0.233] -> cand `zone fight 3 hp 571 tp-cover aggregate hp25% c6` [-0.107, 0.994]
- `multi-threat-s1004-t57.6` ['avoids walking at 2+ attackers'] | base `zone fight 3 hp 498 tp-cover hp20% c6` [0.98, 0.2] -> cand `zone fight 3 hp 498 tp-cover aggregate hp20% c6` [-0.078, 0.997]
- `multi-threat-s1023-t13.7` ['avoids walking at 2+ attackers'] | base `laser hunt fight 7 hp 1175 hp78% c0` [0.999, -0.041] -> cand `laser hunt fight 7 hp 1175 aggregate hp78% c0` [-0.301, 0.954]
- `multi-threat-s1023-t14.0` ['avoids walking at 2+ attackers'] | base `laser hunt fight 7 hp 1175 hp78% c0` [1.0, -0.019] -> cand `laser hunt fight 7 hp 1175 aggregate hp78% c0` [-0.314, 0.949]
- `multi-threat-s1023-t14.3` ['avoids walking at 2+ attackers'] | base `laser hunt fight 7 hp 1175 hp78% c0` [1.0, 0.008] -> cand `laser hunt fight 7 hp 1175 aggregate hp78% c0` [-0.331, 0.944]
- `multi-threat-s1023-t14.6` ['avoids walking at 2+ attackers'] | base `laser hunt fight 7 hp 1175 hp78% c0` [0.999, 0.032] -> cand `laser hunt fight 7 hp 1175 aggregate hp78% c0` [-0.348, 0.938]
- `multi-threat-2att-multi-threat-s1001-t41.6` ['avoids walking at 2+ attackers'] | base `zone fight 15 hp 1265 ldodge hp61% c0` [0.635, -0.773] -> cand `zone fight 15 hp 1265 ldodge aggregate hp61% c0` [-0.708, 0.706]
- `multi-threat-3att-unseen-multi-threat-s1004-t56.3` ['avoids walking at 2+ attackers'] | base `zone fight 3 hp 1257 tp-cover hp31% c6 chg` [0.959, 0.283] -> cand `zone fight 3 hp 1257 tp-cover aggregate hp31% c6 chg` [0.558, -0.83]
- `multi-threat-2att-multi-threat-s1004-t57.3` ['avoids walking at 2+ attackers'] | base `zone fight 3 hp 571 tp-cover hp25% c6` [0.973, 0.233] -> cand `zone fight 3 hp 571 tp-cover aggregate hp25% c6` [-0.107, 0.994]
- `multi-threat-3att-unseen-multi-threat-s1004-t57.3` ['avoids walking at 2+ attackers'] | base `zone fight 3 hp 571 tp-cover hp25% c6` [0.973, 0.233] -> cand `zone fight 3 hp 571 tp-cover aggregate hp25% c6` [0.347, 0.938]
- `multi-threat-2att-multi-threat-s1004-t57.6` ['avoids walking at 2+ attackers'] | base `zone fight 3 hp 498 tp-cover hp20% c6` [0.98, 0.2] -> cand `zone fight 3 hp 498 tp-cover aggregate hp20% c6` [-0.078, 0.997]
- `multi-threat-2att-multi-threat-s1004-t57.9` ['avoids walking at 2+ attackers'] | base `zone fight 3 hp 424 tp-cover hp18% c6` [0.465, -0.886] -> cand `zone fight 3 hp 424 tp-cover aggregate hp18% c6` [-0.117, 0.993]
