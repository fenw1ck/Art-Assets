---
id: chest
title: Wooden chest (iron-bound)
kind: object
parent: containers
aliases: [wooden chest, treasure chest, iron-bound chest, coffer chest, sea chest, six-board chest]
depth: outline
updated: 2026-11-24
gaps: [photos of open chests (lid angle, inside), domed-lid proportions, Greek/Roman wooden chests (none survive; only stone and clay copies)]
used_by: [containers.js drawChest]
traits:
  construction: six-board
  lid: flat
  width: 1
  height: 0.5
  depth: 0.52
  lid_height: 0.09
  planks: 3
  feet: none
  wood: oak
  wood_colour: "#7a5230"
  grain: flat-sawn
  metal: wrought iron
  metal_colour: "#3b3a3a"
  bands: 2
  corner_brackets: true
  edge_binding: true
  strap_hinges: true
  lock_plate: rectangle
  hasp: true
  handles: ring
  rivets: 0.6
  contents: coins
  wear: 0.4
  states: [closed, open]
---

# Wooden chest

## Distinguishing features

- **Proportions.** An iron-bound merchant's chest measures about 50 × 32 × 28 in (W × H × D), and an English oak coffer about 40 × 25 × 20 in. Both are roughly **1 : 0.62 : 0.52** overall, lid included. In the traits that is a box height of 0.5 plus a lid of about 0.09, and a depth of 0.52.
- **Iron-bound.** Wrought-iron straps, edges and corners on oak or pine. Lids lift on long strap hinges that frame the lid. There are side handles, a lock plate on the front, and often a hasp.
- **"Metal edges"** (this brief) is the `edge_binding` and `corner_brackets` traits.
- **A game treasure chest** shows coins when open (Euclid chests give 1–20 coins).

## Rendering notes

- Wood: see `materials/wood/_wood.md`. Flat-sawn boards show arched cathedral grain; boards run horizontally on the front.
- Metal: see `materials/metal/_metal.md`. Wrought iron is near-black with softened edges and pitting, and rust where it is worn.
- Light from the upper left: top lightest, front mid, side darkest. Darken where the lid overhangs the box and where the box meets the floor (occlusion).

## Log

- 2026-11-24: created from the first brief. Proportions from dealer measurements of two antique chests.

## Sources

- 1stdibs, Antique iron-bound merchant's chest (H 32 × W 50 × D 28 in): https://www.1stdibs.com/buy/hasp-lock
- 1stdibs, English coffer, 18th century (H 24.8 × W 39.8 × D 20.5 in): https://www.1stdibs.com/buy/english-chest-coffer
- 1stdibs, Wrought iron strap hinges (Dutch oak trunk; Swedish dome-top trunk): https://www.1stdibs.com/buy/wrought-iron-strap-hinges-antique
- Met Museum, Chest, 15th–16th century (iron bands and hasps): https://www.metmuseum.org/art/collection/search/471591
- Euclid GAME_DESIGN.md, section 4 (chests and coins): https://github.com/fenw1ck/euclid/blob/main/GAME_DESIGN.md
