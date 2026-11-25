---
id: indoor-floors
title: Indoor floors
kind: pattern
parent: floors
aliases: [interior floors, room floors]
depth: outline
updated: 2026-11-25
gaps: [tile and terrazzo, parquet and herringbone, wear paths by room use]
used_by: [floors.js, euclid game.html (corridor, library, bedroom)]
---

# Indoor floors

## Parts

- The floor of every room that is not a greenhouse (greenhouse floors are garden floors: grass, flagstone and dirt paths, see `floors`). Two kinds so far, **stone** and **wood**; **carpet** can be laid over either.
- Drawn top-down as a texture covering the room (1 unit = about 1 m), then laid into the room's perspective one screen row at a time, so the pattern stays true as it recedes.

## Log

- 2026-11-25: created as the parent of stone-floor, wood-floor and carpet, for the Euclid game's indoor rooms.
