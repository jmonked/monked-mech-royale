# Corpus check - v62

- Base: `c8e98e18b1471388bdeee6f2e090568393af446b`
- Candidate: `a023e35a15df4f425691bb2c8fdee257063e78a3`
- Scenario corpus: 4472
- Candidate diverged: 1677
- Clearly safer: 260
- Clearly worse: 110
- Neutral/uncertain: 1108
- Catastrophic regressions: 199
- Action fields changed: {'move': 1677}
- Activation tokens (in candidate label only): {'aggregate': 1819}

| Category | identical | safer | worse | uncertain | catastrophic |
|---|---|---|---|---|---|
| cover-conflict | 232 | 50 | 21 | 202 | 35 |
| dodge-conflict | 223 | 46 | 20 | 183 | 28 |
| hypothesis | 804 | 32 | 5 | 142 | 17 |
| laser-crossfire | 247 | 32 | 14 | 178 | 43 |
| multi-threat | 352 | 49 | 22 | 259 | 29 |
| regression | 5 | 2 | 0 | 7 | 0 |
| sound-boundaries | 259 | 0 | 0 | 0 | 0 |
| unstick-conflict | 472 | 25 | 20 | 66 | 29 |
| zone-pressure | 201 | 24 | 8 | 71 | 18 |

## Reasons

- avoids walking at 2+ attackers: 228
- walks straight at an active attacker: 113
- C6 boosts into a wall: 84
- C2 walks at 2+ attackers: 60
- C4 steps into live laser line: 52
- steps out of live laser line: 40
- C5 leaves next circle: 7
- stays in next circle: 6

## catastrophic examples

- `multi-threat-s1009-t46.7` ['C6 boosts into a wall'] | base `laser hunt fight 1 hp 1085 hp26% c0` [-0.651, 0.759] -> cand `laser hunt fight 1 hp 1085 aggregate hp26% c0` [0.852, -0.524]
- `multi-threat-s1014-t119.8` ['C6 boosts into a wall'] | base `zone fight 12 hp 905 tp-cover hp26% c0` [1.0, 0.031] -> cand `zone fight 12 hp 905 tp-cover aggregate hp26% c0` [0.364, -0.931]
- `multi-threat-s1014-t120.1` ['C6 boosts into a wall'] | base `zone fight 12 hp 860 tp-cover hp15% c0` [0.995, -0.1] -> cand `zone fight 12 hp 860 tp-cover aggregate hp15% c0` [0.345, -0.939]
- `multi-threat-s1014-t120.4` ['C6 boosts into a wall'] | base `zone fight 12 hp 860 tp-cover hp1% c0` [0.97, -0.245] -> cand `zone fight 12 hp 860 tp-cover aggregate hp1% c0` [0.401, -0.916]
- `multi-threat-s1021-t73.2` ['C6 boosts into a wall'] | base `drop-walk fight 1 hp 627 tp-cover hp69% c2` [0.541, 0.841] -> cand `drop-walk fight 1 hp 627 tp-cover aggregate hp69% c2` [-0.195, 0.981]
- `multi-threat-2att-multi-threat-s1006-t213.0` ['C2 walks at 2+ attackers'] | base `drop-walk fight 14 hp 1400 tp-cover hp52% c6 chg` [-0.66, 0.751] -> cand `drop-walk fight 14 hp 1400 tp-cover aggregate hp52% c6 chg` [0.341, 0.94]
- `multi-threat-3att-unseen-multi-threat-s1006-t213.0` ['C2 walks at 2+ attackers'] | base `drop-walk fight 14 hp 1400 tp-cover hp52% c6 chg` [-0.545, 0.839] -> cand `drop-walk fight 14 hp 1400 tp-cover aggregate hp52% c6 chg` [0.648, 0.762]
- `multi-threat-3att-unseen-multi-threat-s1011-t13.4` ['C2 walks at 2+ attackers'] | base `zone fight 9 hp 500 hp42% c0` [-0.708, -0.706] -> cand `zone fight 9 hp 500 aggregate hp42% c0` [0.587, -0.809]
- `multi-threat-2att-multi-threat-s1014-t119.8` ['C6 boosts into a wall'] | base `zone fight 12 hp 905 tp-cover hp26% c0` [1.0, 0.031] -> cand `zone fight 12 hp 905 tp-cover aggregate hp26% c0` [0.124, -0.992]
- `multi-threat-2att-multi-threat-s1014-t120.1` ['C6 boosts into a wall'] | base `zone fight 12 hp 860 tp-cover hp15% c0` [0.995, -0.1] -> cand `zone fight 12 hp 860 tp-cover aggregate hp15% c0` [0.577, -0.817]
- `multi-threat-3att-unseen-multi-threat-s1014-t120.1` ['C6 boosts into a wall'] | base `zone fight 12 hp 860 tp-cover hp15% c0` [0.995, -0.1] -> cand `zone fight 12 hp 860 tp-cover aggregate hp15% c0` [0.219, -0.976]
- `multi-threat-2att-multi-threat-s1014-t120.4` ['C2 walks at 2+ attackers'] | base `zone fight 12 hp 860 tp-cover hp1% c0` [0.97, -0.245] -> cand `zone fight 12 hp 860 tp-cover aggregate hp1% c0` [-0.148, 0.989]

## worse examples

- `multi-threat-s1010-t72.9` ['walks straight at an active attacker'] | base `zone fight 1 hp 574 tp-cover hp46% c2 chg` [-0.442, -0.897] -> cand `zone fight 1 hp 574 tp-cover aggregate hp46% c2 chg` [0.998, 0.064]
- `multi-threat-s1010-t73.2` ['walks straight at an active attacker'] | base `zone fight 1 hp 574 tp-cover hp46% c2 chg` [-0.446, -0.895] -> cand `zone fight 1 hp 574 tp-cover aggregate hp46% c2 chg` [0.995, 0.098]
- `multi-threat-s1018-t48.6` ['walks straight at an active attacker'] | base `zone fight 13 hp 734 hp7% c2 chg` [-0.452, -0.892] -> cand `zone fight 13 hp 734 aggregate hp7% c2 chg` [0.681, 0.732]
- `multi-threat-s1021-t76.5` ['walks straight at an active attacker'] | base `cube fight 10 hp 1400 tp-cover hp9% c2` [0.585, -0.811] -> cand `cube fight 10 hp 1400 tp-cover aggregate hp9% c2` [-0.14, 0.99]
- `multi-threat-s1021-t76.8` ['walks straight at an active attacker'] | base `cube fight 10 hp 1400 tp-cover hp6% c2` [0.454, -0.891] -> cand `cube fight 10 hp 1400 tp-cover aggregate hp6% c2` [-0.054, 0.999]
- `multi-threat-2att-multi-threat-s1010-t73.2` ['walks straight at an active attacker'] | base `zone fight 1 hp 574 tp-cover hp46% c2 chg` [-0.127, -0.992] -> cand `zone fight 1 hp 574 tp-cover aggregate hp46% c2 chg` [0.993, -0.121]
- `multi-threat-3att-unseen-multi-threat-s1019-t46.5` ['walks straight at an active attacker'] | base `zone fight 2 hp 1220 hp13% c0` [0.62, -0.784] -> cand `zone fight 2 hp 1220 aggregate hp13% c0` [0.681, -0.733]
- `multi-threat-3att-unseen-multi-threat-s1019-t47.1` ['walks straight at an active attacker'] | base `zone fight 2 hp 1220 hp13% c0` [0.607, -0.795] -> cand `zone fight 2 hp 1220 aggregate hp13% c0` [0.926, -0.379]
- `multi-threat-2att-multi-threat-s1021-t76.8` ['walks straight at an active attacker'] | base `cube fight 10 hp 1400 hp6% c2` [0.432, -0.902] -> cand `cube fight 10 hp 1400 aggregate hp6% c2` [-0.054, 0.999]
- `multi-threat-3att-unseen-multi-threat-s1023-t12.8` ['walks straight at an active attacker'] | base `laser hunt fight 7 hp 1175 hp81% c0` [-1.0, 0.021] -> cand `laser hunt fight 7 hp 1175 aggregate hp81% c0` [0.346, -0.938]
- `multi-threat-3att-unseen-multi-threat-s1023-t13.4` ['walks straight at an active attacker'] | base `laser hunt fight 7 hp 1175 hp78% c0` [0.042, 0.999] -> cand `laser hunt fight 7 hp 1175 aggregate hp78% c0` [-0.969, -0.247]
- `multi-threat-2att-multi-threat-s1023-t14.3` ['walks straight at an active attacker'] | base `laser hunt fight 7 hp 1175 tp-cover hp78% c0` [0.254, -0.967] -> cand `laser hunt fight 7 hp 1175 tp-cover aggregate hp78% c0` [-0.997, -0.073]

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
