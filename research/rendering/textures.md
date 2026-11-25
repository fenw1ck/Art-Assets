---
id: textures
title: Textures
kind: technique
parent: none
aliases: [texture, veins, cracks, grout, seams, grain, noise, voronoi, domain warping]
depth: outline
updated: 2026-11-24
gaps: [wood grain, bark, feather barbs at large sizes, water, glass, a canvas noise implementation in core.js]
used_by: [plants.js dapple]
---

# Textures

## Methods

| Texture | Method | Rule |
|---|---|---|
| Marble veins | banding warped by layered noise (domain warping), plus main veins drawn as curves | one main direction, a few big veins, empty areas between, veins thin where they turn; see `materials/stone/marble.md` |
| Breccia, terrazzo | Voronoi fragments set in a matrix | angular pieces |
| Sandstone | fine grain speckle, faint bedding, patina gradient | see `materials/stone/villamayor-sandstone.md` |
| Cracks | Voronoi cell edges, or shortest paths across a weighted grid | they branch and join; they start at edges and stress points |
| Seams, grout | layout grid, then a recessed line: occlusion on one side, a lit edge on the other | darker and lower than the stone |
| No visible repeats | per-tile seeds; Wang tiles | |
| Foliage masses | small leaves scattered over the mass, lit on the upper left | already in plants.js (`dapple`) |
| Leaf surface | veins, gloss band, pucker dots, wrinkle strokes | already in plants.js (`leaf`, `sLeaf`, `tomLeaflet`) |

## Log

- 2026-11-24: created.

## Sources

- Inigo Quilez, Domain warping: https://iquilezles.org/articles/warp
- Wikipedia, Procedural texture: https://en.wikipedia.org/wiki/Procedural_texture
- Crack patterns from Voronoi diagrams of weighted graphs (Carleton GIGL): https://gigl.scs.carleton.ca/papers/crack.pdf
- Procedural Wang Tile Algorithm for Stochastic Wall Patterns: https://arxiv.org/abs/1706.03950
- Sperl, Procedural generation of brick and stone textures (TU Wien, 2013): https://www.cg.tuwien.ac.at/research/publications/2013/sperl-2013-BA/sperl-2013-BA-thesis.pdf
