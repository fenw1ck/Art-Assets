---
id: plants
title: Plants (flowering plants)
kind: subject
class: plant
parent: none
aliases: [plant, vegetable, herb, flower]
depth: standard
updated: 2026-11-25
gaps: [seedling (cotyledon) shapes by family, decline photos per family, root crops below ground]
used_by: [plants.js]
traits:
  stem: round-green
  states: [seedling, immature, mature, declining, dead]
---

# Plants

Moved here from PLANT_ART.md (Planting-Guide and euclid), which this entry and its children replace.

## Parts

- **Stem:** nodes, where leaves and buds attach, and the internodes between them. Round or square in section, green or woody, smooth or hairy.
- **Leaf:** the blade, its stalk (petiole; a leaf without one is sessile) and the midrib.
  - **Simple or compound.** A compound leaf is divided into leaflets: pinnate (in pairs along a central stalk, the rachis), palmate (spreading from one point) or bipinnate (twice divided).
  - **Shape:** ovate (egg-shaped, widest near the base), obovate, lance, linear, round, cordate, or thread-like.
  - **Tip:** pointed or rounded.
  - **Margin:** entire (smooth), serrate (teeth pointing forward), dentate (teeth pointing out), crenate (rounded teeth), wavy, or lobed.
  - **Venation:** pinnate (a midrib with side veins), palmate (veins from one point), or parallel.
  - **Surface:** glossy, puckered (bullate), wrinkled, or hairy.
- **Leaf arrangement (phyllotaxy):** alternate (one per node, sides taking turns), opposite (two per node), decussate (opposite pairs each turned a quarter turn), whorled (three or more per node), or basal/rosette (from the base). Alternate leaves usually follow a spiral of about 137.5° (the golden angle).
- **Branching:** a main stem with side shoots from the leaf angles (axils); a stem that forks again and again; or a crown of leaf stalks at ground level.
- **Flowers (inflorescence):** where they appear (leaf angles, forks, between nodes, tips), single or grouped. Groups are clusters, spikes of whorls, umbels (umbrella-shaped), heads, or balls.
- **Fruit:** where it hangs, how many per group, its shape, and how its colour changes as it ripens. Lower, older fruit ripen first.

## Construction order

1. Look at single leaves first, from close photos: simple or compound, shape, tip, margin, surface, veins.
2. Work out the structure from botanical ID guides, which are more reliable than any one photo: arrangement, branching, stem, where the flowers and fruit go.
3. Build from rules, not from one picture:
   - one small function per part (leaf, leaflet, flower, fruit, stem);
   - one shoot function that places the parts along a stem by the plant's rules;
   - when the plant repeats itself, call the shoot again at a smaller size (L-system style).
   - Seed the randomness, so each plant looks natural but is the same every time.
4. Draw every state from the same structure.
5. Shade: leaves get a lit half and a shaded half, a pale midrib and veins, and gloss or pucker where the real leaf has it. Fruit gets a gradient and a glint. Stems taper. Every plant sits on a soft shadow.
6. Check: every plant and state side by side, compared with photos. Tune the proportions: leaf size against plant size, fruit size, spread. Keep each fix as a rule in code.

## States

- **seedling:** seed leaves (cotyledons), then the first true leaves. These often have a different shape from the cotyledons.
- **immature (young):** leaves and stem only, or first flowers.
- **mature:** full size, flowering or fruiting.
- **declining:** droop and wilting; yellowing that starts on the oldest, lowest leaves; leaf edges brown and dry; leaves dropping; fruit shrivelling or splitting. Used in the abandoned greenhouses.
- **dead:** the skeleton remains (stems, stake, seed heads) with curled, brown, papery leaves. No cartoon symbols.
- **dormant:** perennials and trees only. Bare branches, or a crown at ground level.

## Rendering notes

- Light: upper-left key light; see `rendering/light-and-shadow.md`.
- Big foliage masses are dappled with small leaves, not left as smooth balloons.

## Log

- 2026-11-24: created from PLANT_ART.md plus botanical glossaries. Added the decline and dead states (realistic decline was decided 24 Nov 2026).

## Sources

- Purdue Plant ID glossary: https://hort.purdue.edu/plant-id-pal/glossary.html
- OpenTextBC, Plant Identification, ch. 14 Leaves: https://opentextbc.ca/plantidentification/chapter/plant-morphology-leaves/
- UT Austin Biodiversity Center, Botany basics: understanding leaves: https://biodiversity.utexas.edu/news/features/botany-basics-understanding-leaves
- Cornell Cooperative Extension, Botany language basics for plant ID: https://dlc.cce.cornell.edu/pluginfile.php/452580/mod_page/content/14/Botany%20Language%20Basics%20for%20Plant%20Id.pdf
- Prusinkiewicz & Lindenmayer, The Algorithmic Beauty of Plants (free online): https://algorithmicbotany.org/papers/abop/abop.pdf


## Flower workflow

New flowering-plant work follows `flower-rendering-workflow.md`: species-specific botanical research, growth architecture, separate parts, seeded variation, shared life stages, and rendered contact-sheet inspection before release. The tomato's recursive shoot pattern is used only where the species' actual growth habit supports it.


## Additional flower studies

- `cosmos.md`: airy, finely dissected opposite foliage and terminal composite heads.
- `zinnia.md`: bushy opposite-leaved growth and solitary terminal composite heads.
- `petunia.md`: trailing/spreading branches and solitary axillary trumpet flowers.
- `fuchsia.md`: shrub habit with pendent axillary flowers, tubular calyx and four sepals/four petals.


## Species-specific research records

The following records document botanical construction evidence for the Botanical Renderer. Each entry includes growth architecture, leaf form, branching, reproductive structures, rendering rules, sources and unresolved cultivar/stage questions. These are research briefs, not rendered assets.

- [Sweet corn](corn_sweet.md)
- [Bush bean](bean_bush.md)
- [Pole bean](bean_pole.md)
- [Garden pea](pea.md)
- [Summer squash / zucchini](squash_summer.md)
- [Winter squash](squash_winter.md)
- [Cucumber](cucumber.md)
- [Leaf lettuce](lettuce.md)
- [Spinach](spinach.md)
- [Kale](kale.md)
- [Cabbage](cabbage.md)
- [Broccoli](broccoli.md)
- [Swiss chard](chard.md)
- [Garden beet](beet.md)
- [Radish](radish.md)
- [Asparagus](asparagus.md)
- [Rhubarb](rhubarb.md)
- [Garden strawberry](strawberry.md)
- [Red raspberry](raspberry.md)
- [Highbush blueberry](blueberry.md)
- [French marigold](marigold_french.md)
- [Pothos](pothos.md)
- [Snake plant](snake_plant.md)
- [Monstera](monstera.md)
- [Peace lily](peace_lily.md)
- [Spider plant](spider_plant.md)
- [Apple](apple.md)
- [European pear](pear.md)
- [Peach](peach.md)
- [Fig](fig.md)
- [Meyer lemon](lemon_meyer.md)
- [Sunflower](sunflower.md)

## Additional plant profiles (research-only)

- [Oregano](oregano.md)
- [Rosemary](rosemary.md)
- [Garden sage](sage.md)
- [Greek oregano](oregano_greek.md)
- [Prostrate rosemary](rosemary_prostrate.md)
- [Purple sage](sage_purple.md)
- [Borage](borage.md)
- [Lemon thyme](thyme_lemon.md)
- [German chamomile](chamomile.md)
- [Bush basil](bush_basil.md)
- [Watermelon](watermelon.md)
- [Muskmelon](melon.md)
- [Pumpkin](pumpkin.md)
- [Sweet potato](sweet_potato.md)
- [Turnip](turnip.md)
- [Celery](celery.md)
- [Cauliflower](cauliflower.md)
- [Brussels sprouts](brussels_sprout.md)
- [Okra](okra.md)
- [White eggplant](eggplant_white.md)

## References and evidence policy

See [Botanical research references](_references.md) for taxonomy databases, morphology sources, specimen/image resources, cultivar references, evidence hierarchy and citation rules.
