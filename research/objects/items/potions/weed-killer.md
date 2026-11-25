---
id: weed-killer
title: Weed killer
kind: object
parent: potions
aliases: [herbicide, vine killer, potion-weak, potion-strong, potion-strongest]
depth: outline
updated: 2026-11-25
gaps: [withered-vine drawing (vines currently just fall away as they do under the ax)]
used_by: [items.js potion; euclid game.html pour()]
---

# Weed killer

## Distinguishing features

| Strength | Fluid | Tag | Vines removed by one flask | Matches |
|---|---|---|---|---|
| weak | pale green #c3d86a | one leaf | 40% | the Iron Ax's cut in work (10 → 6 strikes) |
| strong | green #45a84e | two leaves | 70% | the Starmetal Ax's cut (10 → 3 strikes) |
| strongest | deep green #1d6b3c, glowing | three leaves | all of them | — |

- Poured on a door's vines it removes that share of them at once; the ax does the rest.
- It also kills any garden plant it is poured on (the plant is drawn in its `dead` stage from plants.js).
- Single use: the flask is gone after one pour.
