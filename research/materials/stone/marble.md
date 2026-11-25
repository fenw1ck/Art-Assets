---
id: marble
title: Marble (and decorative stones sold as marble)
kind: material
parent: stone
aliases: [Carrara, giallo antico, portasanta, breccia, Portoro, verde antico, Sienna marble]
depth: outline
updated: 2026-11-24
gaps: [colour swatches from photos for each named stone, vein measurements, polish/reflection]
used_by: []
---

# Marble

## Distinguishing features

- Real marble reads as marble through its large-scale structure: a dominant vein direction, a few big "event" veins, empty areas between them, and a clear value hierarchy. It also has translucency.
- **Veins** are fracture paths that were later filled. They have a width that varies along them, a main direction, and branches. They thin where they turn.
- **Book-matching:** slabs cut side by side are laid mirrored, so a vein continues across the seam as a reflection.

Named kinds to research further:
- **Portoro:** fine gold veins on black.
- **Verde antico / serpentine:** angular pieces in a chaotic mosaic, rather than flowing veins.
- **Sienna:** warm yellow with reddish veining.
- **Breccia:** angular fragments cemented together.
- **Giallo antico, portasanta:** both used in Roman opus sectile floors.
- **Carrara:** white to grey with grey veins.

## Rendering notes

- Banding, warped by layered noise (domain warping), gives the flow. Ken Perlin's first procedural marble (1984) worked this way.
- Thresholding noise alone gives blobs with no direction, so draw the main veins as curves on top.
- Breccia uses Voronoi fragments.

## Log

- 2026-11-24: outline from procedural-marble research.

## Sources

- Inigo Quilez, Domain warping: https://iquilezles.org/articles/warp
- LAPIDEO technical briefing on procedural marble (auriea.org): https://auriea.org/LAPIDEO
- GameDev.net Shaderlab, Procedural marble: https://gamedev.net/shaderlab/24-procedural-marble/
