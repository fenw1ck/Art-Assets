---
id: botanical-plate
title: Botanical plate construction and rendering method
kind: technique
parent: crafted-style
aliases: [naturalist's plate, plant art renderer, botanical illustration, plant infocards]
depth: standard
updated: 2026-11-25
gaps: [photo-verified leaf silhouettes for every cultivar, seedling and decline references by species, calibrated colour samples]
used_by: [tools/plant-art.py]
---

# Botanical plate construction and rendering method

## Purpose

Every plant is a botanical subject, not a generic green silhouette with a flower pasted on. The renderer must preserve the species' growth habit, branching order, leaf arrangement, leaf shape, reproductive structures and harvest organ. The same species profile drives both the drawing and its infocard, so a change in the botanical description changes the art instructions too.

## House style: Naturalist's Plate

- Warm ivory paper; one isolated specimen; restrained ground shadow.
- Proportional construction with crisp, closed shapes.
- Soft light from the upper left; gentle tonal variation within each leaf and stem.
- Fine midrib and lateral veins; margins and veins remain visible at the intended display size.
- A thin edge in the subject's own darker colour; no black cartoon outline.
- Botanical detail takes priority over decorative texture. Keep the silhouette readable at icon scale.
- A terracotta nursery pot is the consistent presentation device for this library. It is a display convention, not a claim that every species is naturally potted.

## Construction order

1. **Habit:** decide whether the plant is a rosette, tuft, upright herb, branched bush, cane, climbing/trailing vine, bulb, crown, subshrub or tree.
2. **Axis and branching:** place the main stem, trunk, crown or stolons first. Branches follow the species' real node pattern; do not use a recursive branch rule unless the plant actually branches that way.
3. **Leaves:** construct from the correct attachment pattern and morphology: alternate, opposite, whorled, basal, compound, strap-like, lobed, divided, peltate, fenestrated, etc. Draw petioles and midribs before leaf blades.
4. **Reproductive structures:** place flowers where the species bears them (terminal, axillary, in umbels, spikes, racemes, heads, spathes or trusses). Distinguish flowers from fruit.
5. **Harvest organ:** show the part the plant actually produces or the part harvested, where useful: fruit, pod, leaf, root, bulb, tuber, stem or flower.
6. **Stage:** preserve the same architecture while changing scale, internode length, leaf count, flowering, fruiting or decline. Do not simply shrink the mature plant to make a seedling.
7. **Variation:** vary seed, branch angles, leaf sizes and flower/fruit placement deterministically. A seed must reproduce the same image.
8. **Inspection:** render every species to an individual PNG and a contact sheet. Inspect at full size and at the library-card size; fix silhouettes that collapse or details that become noise.

## Renderer and infocard contract

`tools/plant-art.py` reads the canonical 57-item list from `plants.js`. `PROFILES` is deliberately explicit: every plant ID must have one growth habit, family, diagnostic anatomy, leaf construction, flower construction and fruit/harvest description. `--check` fails if any plant is missing or if a profile no longer matches the source list.

The renderer writes:
- `plant-art/<id>.png`: one isolated specimen per species.
- `plant-art/infocards.json`: the same botanical profile in structured form, with the renderer name and reusable style terms.
- `plant-art/contact-sheet.png`: all selected species in a consistent seven-column overview.

The infocard's `diagnostic_botany` field is the species-specific construction brief. `style_terms` is the reusable visual brief. Future renderers should consume the same fields rather than inventing new descriptions for the same species.

## Infocard morphology schema

Each plant infocard has a `morphology` object keyed by observable structural traits. Taxonomy remains a separate object and is never used as a substitute for species-level morphological evidence.

Each trait record uses this shape:

```json
{
  "status": "unknown",
  "values": [],
  "variants": [],
  "provenance": []
}
```

Allowed statuses:
- `documented`: one or more researched values are supported by the listed references.
- `variable`: the trait has documented alternatives; record the conditions in `variants`.
- `unknown`: research has not established the trait. This is not equivalent to absence.
- `not_applicable`: the trait genuinely does not apply to this plant structure; record the rationale and supporting basis in provenance.

Every value and variant must have trait-specific provenance. A provenance entry should identify the source title, exact URL or publication identifier, the claim it supports, and (where available) page, section, figure, specimen or access date. Do not cite a family or genus page as evidence for a species-specific value unless that source explicitly documents the species.

Variants must preserve their conditions, including cultivar, developmental stage, sex, environment or other relevant scope. Do not flatten conditional variation into a single default value. An unknown trait remains unknown until researched; do not infer it from taxonomy or a related species.

The initial 57 infocards receive empty, explicitly unknown morphology records as schema scaffolding. This is not a claim that those traits have been researched. The first 57 remain on rendering hold.

## Research discipline

- Use species-level references where available; use family-level references only for traits shared by the family.
- Separate established botanical facts from rendering decisions. A terracotta pot, paper colour, composition and seed variation are art direction; leaf arrangement, branching, flowers and fruit are botanical claims.
- Do not infer a species' exact leaf shape from its common name. Check a botanical description or extension publication and record the source.
- Existing research entries remain authoritative for the plants they cover. The Python profiles are a rendering index, not a replacement for cited research.

## References consulted

- University of Missouri Extension, *Flowering Annuals: Characteristics and Culture*: https://extension.missouri.edu/publications/g6629
- Clemson Cooperative Extension, *Growing Annuals*: https://hgic.clemson.edu/factsheet/growing-annuals/
- University of Maryland Extension, *Growing Apple and Pear Trees in a Home Garden*: https://www.extension.umd.edu/resource/growing-apple-and-pear-trees-home-garden
- University of Maine Cooperative Extension, *Pruning*: https://extension.umaine.edu/fruit/growing-fruit-trees-in-maine/pruning/
- UF/IFAS Extension, *The Fig*: https://ask.ifas.ufl.edu/publication/mg214
- UC Marin Master Gardeners, *Pruning Tips: Fruit Trees*: https://www.ucanr.edu/site/uc-marin-master-gardeners/collection/pruning-tips-fruit-trees
- Illinois Extension, *Uses | Flowers*: https://extension.illinois.edu/flowers/uses

## Log

- 2026-11-25: established a Python renderer and a one-profile-per-species contract for all 57 entries in `PLANTS.list`. The first pass is an architectural renderer; the listed gaps remain open until each species is checked against photos and species-level sources.
