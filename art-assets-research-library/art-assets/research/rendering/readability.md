---
id: readability
title: Readability checks
kind: technique
parent: none
aliases: [silhouette test, value check, grayscale, level of detail, LOD]
depth: outline
updated: 2026-11-24
gaps: [minimum sizes measured in each project]
used_by: [tools/contact-sheet.py]
---

# Readability

## Checks

- **Silhouette:** fill the drawing solid black. It should still read as itself and be told apart from its neighbours. States should change the shape, not only the colour.
- **Value:** in greyscale, the subject separates from its background. Gameplay objects need stronger contrast than the scenery.
- **Level of detail:**
  - icon (≤ 48 px): silhouette plus the one colour that names it;
  - card (96–200 px): the main parts;
  - detail (≥ 400 px): fine texture.

## Log

- 2026-11-24: created.

## Sources

- Bugnet, Readable game art: why clarity beats detail: https://bugnet.io/blog/readable-game-art-why-clarity-beats-detail
- Ice Wyrm Games, Reducing visual confusion in your game: https://icewyrmgames.github.io/research/reducing-visual-confusion-in-your-game
