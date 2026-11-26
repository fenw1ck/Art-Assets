---
id: corn_sweet
title: Sweet corn
kind: subject
parent: species-research
scientific_name: "Zea mays (sweet-corn cultivar group)"
family: Poaceae
depth: standard
updated: 2026-11-25
used_by: [plant-art/infocards.json, tools/plant-art.py]
traits:
  habit: "Tall, usually single, jointed grass culm; roots include brace roots from lower nodes."
  leaf: "Alternate two-ranked linear blades with parallel veins, prominent midrib, sheathing bases and ligule; blades arch outward from successive nodes."
  branching: "One dominant upright culm with distinct nodes and internodes; usually little lateral branching. Female ear shoots arise from upper leaf axils."
  inflorescence: "Monoecious: terminal branched tassel is the male inflorescence; one or more lateral axillary ears are female inflorescences, wrapped in husks and bearing long silks."
  fruit: "Ear is a compact cob with kernels in longitudinal rows; silk emerges from husk tip. Kernels are caryopses, not berries."
---

# Sweet corn (Zea mays (sweet-corn cultivar group))

## Distinguishing features

- **Growth architecture:** Tall, usually single, jointed grass culm; roots include brace roots from lower nodes.
- **Leaves:** Alternate two-ranked linear blades with parallel veins, prominent midrib, sheathing bases and ligule; blades arch outward from successive nodes.
- **Stem and branching:** One dominant upright culm with distinct nodes and internodes; usually little lateral branching. Female ear shoots arise from upper leaf axils.
- **Flowers:** Monoecious: terminal branched tassel is the male inflorescence; one or more lateral axillary ears are female inflorescences, wrapped in husks and bearing long silks.
- **Fruit:** Ear is a compact cob with kernels in longitudinal rows; silk emerges from husk tip. Kernels are caryopses, not berries.

## Renderer construction rules

Construct a single segmented vertical culm first, then alternate sheathing leaves. Put the tassel only at the apex. Put one or two husked ears on upper axillary nodes, with silks at their tips. Never scatter ears along every node or make the tassel a flower cluster.

## Research gaps

- Cultivar-specific ear and kernel colour
- Sweet-corn plant height and leaf count for the intended cultivar

## Sources

- https://www.ogtr.gov.au/sites/default/files/files/2021-07/the_biology_of_zea_mays_l._ssp_mays_maize_or_corn.pdf
- https://plantuse.plantnet.org/en/Zea_mays_%28PROSEA%29

## Log

- 2026-11-25: species-specific morphology and construction rules added for the Botanical Renderer. This is research/data work only; no artwork was rendered.
