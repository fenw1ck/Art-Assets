---
id: potato
title: Potato
kind: subject
parent: solanaceae
aliases: [Solanum tuberosum, potato plant, potatoes, spud, tuber]
depth: standard
updated: 2026-11-25
gaps: [tuber shapes by variety (fingerling, round, long), stolons drawn in a cut-away view, a flowering close-up from photos]
used_by: [plants.js drawPotato, plants.js tuber, plants.js harvest, items.js potato]
traits:
  leaf: pinnate
  leaf_shape: ovate
  margin: entire
  surface: matte
  branching: repeated-fork
  repeats: repeated-fork
  inflorescence: cluster
  flower_colour: "#cdb6e6"
  fruit: berry
  foliage_colour: "#4f8a40"
---

# Potato

## Distinguishing features

- **Habit:** a clump of erect, branching stems, 60–90 cm tall, smooth to sparsely hairy, from one seed piece (a tuber or a piece with an eye). Above ground the plant is an annual: stems and leaves die back each year.
- **Leaves:** odd-pinnate compound leaves, like a tomato's, spirally arranged, 20–30 cm long: a terminal leaflet and 2–4 pairs of leaflets (sources say 3–8 pairs, or 6–8 leaflets), with tiny leaflets between the pairs. Unlike tomato, the leaflets are smooth-edged, not toothed. Dark green.
- **Flowers** (seeded per plant: white #f4f1f6, lavender #cdb6e6, purple #9a6bc4 or pink #f2c6d6): in clusters at the stem tips or leaf angles, 2.5–3 cm, five-lobed stars in white, lavender, pink, purple or blue, with a yellow cone of stamens in the middle. One plant can carry several colours.
- **Berries:** sometimes small (about 1 cm), round, green or yellow-green berries after the flowers. Toxic.
- **Tubers:** form on stolons (underground stems) and are their swollen tips, so they are stems, not roots. The skin is red, purple, brown (or yellow); "eyes" are buds, each in a little crescent "brow", and the skin is dotted with lenticels.
- **Ready to harvest:** when the tubers are full grown and the tops die back; "new" potatoes can be dug from flowering onward.
- **Hilling ("earthing up"):** soil mounded around the stems as they grow. Buried stems grow more stolons, so more tubers form above the first ones, and the tubers stay covered (exposed to light they turn green and make solanine, which is toxic and not destroyed by cooking).

## The drawing (plants.js `drawPotato`)

- Stages: seedling (two short shoots with true compound leaves: a potato sprouts from a tuber, so no seed leaves), young (bushy, no flowers, no tubers), mature (flowering; ready to harvest: each tuber shows **a third** of itself above the soil), past (foliage yellowing, stems flopping, a few green berries), dead (brown, flopped).
- Repeating structure: the repeated fork. 3–5 stems from the base, each forking once into two flower-tipped branches.
- `o.hill` 0–3: the mound of soil gets taller and wider, and more tubers show. `o.skin`: red, purple or brown; otherwise seeded from the plant's seed (each copy differs, the same on every visit), as is the flower colour.
- `PLANTS.tuber(ctx,x,y,rx,ry,rot,skin,seed,o)` draws one tuber at any scale (`o.unit` for unit-box drawing, `o.dirt` for soil smudges).
- `PLANTS.harvest(p,{hill})`: part `root` (a tuber is botanically a stem, filed with roots for the game), item `potato`, cook first, count 3 + 2 per hilling (3, 5, 7, 9). Hilling's effect on yield is real but varies in trials; the game makes it simple and certain.

## Sources

- Britannica, potato (leaves, tuber as swollen underground stem): https://www.britannica.com/plant/potato
- NC State Extension Gardener Plant Toolbox, Solanum tuberosum (leaflets, flower colours, solanine, berries, harvest timing): https://plants.ces.ncsu.edu/plants/solanum-tuberosum/common-name/potato/
- NParks Flora & Fauna Web, Solanum tuberosum (odd-pinnate leaves, 3–8 pairs; flowers 2.5–3 cm in clusters): https://www.nparks.gov.sg/florafaunaweb/flora/6/4/6493
- Milne Open Textbooks, Potatoes: Solanum tuberosum (tubers on stolons; annual tops): https://milnepublishing.geneseo.edu/botany/chapter/potato/
- Wikipedia, Hilling (green potatoes, yield): https://en.wikipedia.org/wiki/Hilling
- Homes & Gardens, hilling up potatoes (more tubers from buried stems): https://www.homesandgardens.com/uk/gardens/hilling-up-potatoes
