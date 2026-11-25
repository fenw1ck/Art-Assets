---
id: colour
title: Colour ramps and palettes
kind: technique
parent: none
aliases: [color, hue shifting, colour ramp, palette, dark mode]
depth: outline
updated: 2026-11-24
gaps: [ramps for each material in materials.js, a check for colour blindness]
used_by: []
---

# Colour ramps and palettes

## Parts

- **Ramp:** one material's colours from shadow to highlight.
- **Hue shift:** shift the hue as well as the brightness. Shadows lean toward blue or purple, highlights toward yellow. About 15–25° reads as natural; 30° or more looks stylised. A ramp that only changes brightness looks grey and muddy.
- **Saturation:** slightly higher in the shadows, lower in the brightest highlights.
- **By material:** matte has few or no highlights. Shiny has small, bright ones. Metal has high contrast, with its darkest dark right next to the highlight.

## House rules

- Euclid: `PAL` (colour-blind safe) means "equal" in figures, so don't use those hues in art where they could read as equality marks.
- Euclid dark mode lightens colours 30%.
- Don't over-render: lighting has to stay consistent across all the art.

## Log

- 2026-11-24: created.

## Sources

- GameDev.net, Color palettes: https://www.gamedev.net/articles/visual-arts/color-palettes-r4964/
- Ziva, Pixel art palette generator (hue-shifted ramps): https://ziva.sh/tools/pixel-art-palette-generator
- Highrise creator docs, material art guide: https://github.com/pocketzworld/creator-docs/blob/main/pages/learn/designer-resources/artguides/material.md
