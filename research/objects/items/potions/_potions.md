---
id: potions
title: Potions
kind: object
parent: items
aliases: [potion, flask, phial, vial, consumables]
depth: outline
updated: 2026-11-25
gaps: [a pouring animation, empty flasks as items]
used_by: [items.js potion, health; euclid game.html (weed killer, health potions)]
---

# Potions

## Distinguishing features

- **Single use:** a potion is used up when poured and leaves the inventory (farming sims treat sprays and fertilizers the same way: one use, then gone).
- **The flask:** a glass sphere (a round-bottomed flask) with a short stem, stopped with a cork. Light comes from the upper left, so the highlight curves along the upper-left of the sphere.
- **Strength shows in the fluid's colour**, from pale to deep, plus a paper tag tied at the neck with one, two or three leaves on it.

## Kinds

- weed-killer: the first potion. Poured.
- health-potion: drunk for health; red, with a caduceus stopper (three tiers).

## Log

- 2026-11-25: created for the Euclid game (weed killer).
- 2026-11-25: added health potions; strength now also shows in a second channel (tag leaves, caduceus metal and wings), not only colour.
