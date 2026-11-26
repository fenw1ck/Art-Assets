---
id: crafted-style
title: The crafted style (everything but the mythical creatures)
kind: technique
parent: none
aliases: [crafted style, clean style, romantic style, storybook realism, botanical illustration, art deco, art nouveau, tree of life, eyvind earle, sleeping beauty, sublime, grandeur, monumental]
depth: outline
updated: 2026-11-25
gaps: [which of the ten manticore drafts (or which mix) the user picks, rooms redrawn in it (lofty, monumental), a palette per room type]
used_by: [plants.js (the mint is the reference), bedroom.js (tree-of-life and art deco beds), drafts/manticore-crafted.html]
---

# The crafted style

The user's own description (25 Nov 2026), with the mint, the tree-of-life bed and the art deco bed as the examples: romantic, romanticised, hand-drawn Disney, "a place you would want to spend a lot of time in", lofty, breathtaking, enticing, mysterious, monumental architecture, a sense of grandeur, awe-inspiring, sublime space. **Proportional art**, not the shadow look.

**Which style where:**
- **The mythical creatures keep the shadow style.** That is the back-lit silhouette (`house-style.md`), which the user likes for them.
- **Everything else is drawn in this crafted style:** plants, rooms, furniture, items, architecture.

## Parts (what the examples share)

1. **Accurate structure first.** The mint's opposite leaf pairs turn a quarter turn at each node, as a real mint's do; the beds have real joinery. Bodies come from research and `ENGINE.skeleton`, never from a cartoon.
2. **Crisp, clean shapes.** Every form is a closed, precise shape. There is no sketchy line and no painterly blur.
3. **Soft directional light.** Light comes from the upper left as a gentle gradient across each shape, with a soft core shadow. Highlights are restrained. Nothing is hard-cel.
4. **A thin edge in the shape's own darker colour,** never a black outline (the Art Nouveau variant may use a firm dark contour).
5. **Fine true detail,** like serrations, sunken veins and wood grain, drawn sparingly at a size where it reads.
6. **Ornament from craft traditions.** The tree of life (organic, branching, carved), Art Deco (symmetry, geometry, sunbursts, black and gold), and Art Nouveau (whiplash curves, a halo disc, flat colour in a firm outline).
7. **Grandeur in the settings:** tall vertical forms, layered depth and light from far away. This follows Eyvind Earle's *Sleeping Beauty*, built from medieval manuscripts, tapestries and pre-Renaissance painting, where columns and tapestries stretch the full height of the ballroom. Rooms should feel lofty and inviting: high arches, warm light shafts, mist in the distance.

## The ten manticore drafts (`drafts/manticore-crafted.html`)

All ten share draft 1's accurate lion anatomy; only the treatment changes:

1. naturalist's plate (like the mint)
2. tree of life, carved and inlaid (like the tree-of-life bed)
3. Art Deco black and gold (like the art deco bed)
4. Art Nouveau (Mucha)
5. Sleeping Beauty (Eyvind Earle)
6. millefleurs tapestry
7. cathedral stained glass
8. gilded bestiary page
9. the sublime: monumental halls
10. classic hand-drawn film

The user's pick is still to come. These are style studies for the look of the world; the creatures themselves stay in the shadow style.

## Log

- 2026-11-25: created from the "Improve the Mint art" request. The mint was redrawn to the same standard (its own `drawMint`).

## Sources

- Eyvind Earle and Sleeping Beauty: https://cuckoocomics.com/eyvind_earle.html ; https://www.sparknotes.com/film/sleepingbeauty/section2/ ; https://www.dailyartmagazine.com/sleeping-beauty-medieval-tapestry/
- Art Nouveau and Mucha (whiplash line, halo disc, flat colour in a firm contour): https://blog.fineartamerica.com/art-nouveau-explained/
- Art Deco (symmetry, geometric shapes, sunbursts, black and gold): https://www.adobe.com/uk/express/learn/blog/all-about-art-deco ; https://americantinceilings.com/blogs/home/art-deco-interior-design
