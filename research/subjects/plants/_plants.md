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

## Broader plant-lineage infocards

The catalogue now extends beyond flowering plants into bryophytes, lycophytes, ferns and horsetails, gymnosperms, grasses and broadleaf trees. Research-only infocards are stored in [infocards-expanded.json](../../../plant-art/infocards-expanded.json) and are deliberately not rendered.

- [Nonvascular and spore-bearing plants](nonvascular-and-spore-plants.md): common haircap moss, peat moss (*Sphagnum*, genus-level), running clubmoss, bracken fern, northern maidenhair fern, field horsetail, and Kentucky bluegrass.
- [Woody plants](woody-plants.md): eastern white pine, red maple, white oak, water oak, and black willow.

The taxonomy index identifies the exact lineage and profile scope. Some entries are species-level; the *Sphagnum* card is explicitly genus-level, and the bracken/maidenhair fern records retain species-specific research gaps rather than treating general fern traits as complete species evidence.

## References and evidence policy

See [Botanical research references](_references.md) for taxonomy databases, morphology sources, specimen/image resources, cultivar references, evidence hierarchy and citation rules.


## Botanical taxonomy — canonical plant index

The list is organized by botanical classification, not by garden use or visual similarity. Follow the ranks: **Kingdom → Angiosperms → major clade → Order → Family → Genus → Species → horticultural/cultivar group**. Cultivar groups and growth habits are horticultural subdivisions, not formal taxonomic ranks.

Machine-readable model: [taxonomy.json](taxonomy.json). All infocards also carry a `taxonomy` object and corresponding `user_data.taxonomy_*` fields. The 20 newer research profiles are listed but do not yet have infocards.

### Order: Alismatales

#### Family: Araceae

- **Genus Epipremnum**
  - [Pothos](research/subjects/plants/pothos.md) (*Epipremnum aureum*; golden pothos; cultivar variegation unspecified) — infocard `pothos`
- **Genus Monstera**
  - [Monstera](research/subjects/plants/monstera.md) (*Monstera deliciosa*; Swiss cheese plant) — infocard `monstera`
- **Genus Spathiphyllum**
  - [Peace lily](research/subjects/plants/peace_lily.md) (*Spathiphyllum wallisii*; species reference; cultivated hybrids vary) — infocard `peace_lily`

### Order: Apiales

#### Family: Apiaceae

- **Genus Anethum**
  - [Dill](research/subjects/plants/apiaceae.md) (*Anethum graveolens*; dill) — infocard `dill`
- **Genus Apium**
  - [Celery](research/subjects/plants/celery.md) (*Apium graveolens*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
- **Genus Coriandrum**
  - [Cilantro](research/subjects/plants/apiaceae.md) (*Coriandrum sativum*; cilantro/coriander) — infocard `cilantro`
- **Genus Daucus**
  - [Carrot](research/subjects/plants/apiaceae.md) (*Daucus carota*; cultivated carrot) — infocard `carrot`
- **Genus Petroselinum**
  - [Parsley](research/subjects/plants/apiaceae.md) (*Petroselinum crispum*; culinary parsley) — infocard `parsley`

### Order: Asparagales

#### Family: Amaryllidaceae

- **Genus Allium**
  - [Chives](research/subjects/plants/allium.md) (*Allium schoenoprasum*; chives) — infocard `chives`
  - [Garlic](research/subjects/plants/allium.md) (*Allium sativum*; cultivated garlic) — infocard `garlic`
  - [Onion (bulb)](research/subjects/plants/allium.md) (*Allium cepa*; bulb onion) — infocard `onion`

#### Family: Asparagaceae

- **Genus Asparagus**
  - [Asparagus](research/subjects/plants/asparagus.md) (*Asparagus officinalis*; cultivated asparagus) — infocard `asparagus`
- **Genus Chlorophytum**
  - [Spider plant](research/subjects/plants/spider_plant.md) (*Chlorophytum comosum*; spider plant) — infocard `spider_plant`
- **Genus Dracaena**
  - [Snake plant](research/subjects/plants/snake_plant.md) (*Dracaena trifasciata*; snake plant) — infocard `snake_plant`

### Order: Asterales

#### Family: Asteraceae

- **Genus Calendula**
  - [Calendula](research/subjects/plants/calendula.md) (*Calendula officinalis*; pot marigold) — infocard `calendula`
- **Genus Cosmos**
  - [Cosmos](research/subjects/plants/cosmos.md) (*Cosmos bipinnatus*; garden cosmos) — infocard `cosmos`
- **Genus Helianthus**
  - [Sunflower](research/subjects/plants/sunflower.md) (*Helianthus annuus*; common sunflower) — infocard `sunflower`
- **Genus Lactuca**
  - [Lettuce (leaf)](research/subjects/plants/lettuce.md) (*Lactuca sativa*; leaf-lettuce cultivar group) — infocard `lettuce`
- **Genus Matricaria**
  - [German chamomile](research/subjects/plants/chamomile.md) (*Matricaria chamomilla*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
- **Genus Tagetes**
  - [Marigold (French)](research/subjects/plants/marigold_french.md) (*Tagetes patula*; French marigold) — infocard `marigold_french`
- **Genus Zinnia**
  - [Zinnia](research/subjects/plants/zinnia.md) (*Zinnia elegans*; garden zinnia) — infocard `zinnia`

### Order: Boraginales

#### Family: Boraginaceae

- **Genus Borago**
  - [Borage](research/subjects/plants/borage.md) (*Borago officinalis*; cultivar or horticultural selection not yet specified) — research-only; infocard pending

### Order: Brassicales

#### Family: Brassicaceae

- **Genus Brassica**
  - [Broccoli](research/subjects/plants/broccoli.md) (*Brassica oleracea*; Italica Group) — infocard `broccoli`
  - [Brussels sprouts](research/subjects/plants/brussels_sprout.md) (*Brassica oleracea*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
  - [Cabbage](research/subjects/plants/cabbage.md) (*Brassica oleracea*; Capitata Group) — infocard `cabbage`
  - [Cauliflower](research/subjects/plants/cauliflower.md) (*Brassica oleracea*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
  - [Kale](research/subjects/plants/kale.md) (*Brassica oleracea*; Acephala Group) — infocard `kale`
  - [Turnip](research/subjects/plants/turnip.md) (*Brassica rapa subsp. rapa*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
- **Genus Raphanus**
  - [Radish](research/subjects/plants/radish.md) (*Raphanus sativus*; cultivated radish) — infocard `radish`

#### Family: Tropaeolaceae

- **Genus Tropaeolum**
  - [Nasturtium](research/subjects/plants/nasturtium.md) (*Tropaeolum majus*; garden nasturtium) — infocard `nasturtium`

### Order: Caryophyllales

#### Family: Amaranthaceae

- **Genus Beta**
  - [Beet](research/subjects/plants/beet.md) (*Beta vulgaris*; Conditiva Group) — infocard `beet`
  - [Swiss chard](research/subjects/plants/chard.md) (*Beta vulgaris*; Cicla Group) — infocard `chard`
- **Genus Spinacia**
  - [Spinach](research/subjects/plants/spinach.md) (*Spinacia oleracea*; spinach) — infocard `spinach`

#### Family: Polygonaceae

- **Genus Rheum**
  - [Rhubarb](research/subjects/plants/rhubarb.md) (*Rheum rhabarbarum*; garden rhubarb) — infocard `rhubarb`

### Order: Cucurbitales

#### Family: Cucurbitaceae

- **Genus Citrullus**
  - [Watermelon](research/subjects/plants/watermelon.md) (*Citrullus lanatus*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
- **Genus Cucumis**
  - [Cucumber](research/subjects/plants/cucumber.md) (*Cucumis sativus*; cucumber) — infocard `cucumber`
  - [Muskmelon](research/subjects/plants/melon.md) (*Cucumis melo*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
- **Genus Cucurbita**
  - [Pumpkin](research/subjects/plants/pumpkin.md) (*Cucurbita pepo*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
  - [Summer squash / zucchini](research/subjects/plants/squash_summer.md) (*Cucurbita pepo*; summer-squash cultivar group) — infocard `squash_summer`
  - [Winter squash](research/subjects/plants/squash_winter.md) (*Cucurbita maxima*; winter-squash representative; species selection pending) — infocard `squash_winter`

### Order: Ericales

#### Family: Ericaceae

- **Genus Vaccinium**
  - [Blueberry (highbush)](research/subjects/plants/blueberry.md) (*Vaccinium corymbosum*; highbush blueberry) — infocard `blueberry`

### Order: Fabales

#### Family: Fabaceae

- **Genus Lathyrus**
  - [Sweet pea](research/subjects/plants/sweet-pea.md) (*Lathyrus odoratus*; sweet pea) — infocard `sweet_pea`
- **Genus Phaseolus**
  - [Bean (bush)](research/subjects/plants/bean_bush.md) (*Phaseolus vulgaris*; bush growth-habit cultivars) — infocard `bean_bush`
  - [Bean (pole)](research/subjects/plants/bean_pole.md) (*Phaseolus vulgaris*; pole/climbing growth-habit cultivars) — infocard `bean_pole`
- **Genus Pisum**
  - [Pea](research/subjects/plants/pea.md) (*Pisum sativum*; garden pea) — infocard `pea`

### Order: Lamiales

#### Family: Lamiaceae

- **Genus Lavandula**
  - [Lavender (English)](research/subjects/plants/lamiaceae.md) (*Lavandula angustifolia*; English lavender) — infocard `lavender`
- **Genus Mentha**
  - [Mint](research/subjects/plants/lamiaceae.md) (*Mentha spp.*; culinary mint; species unspecified) — infocard `mint`
- **Genus Ocimum**
  - [Basil](research/subjects/plants/lamiaceae.md) (*Ocimum basilicum*; culinary basil) — infocard `basil`
  - [Bush basil](research/subjects/plants/bush_basil.md) (*Ocimum basilicum*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
- **Genus Origanum**
  - [Greek oregano](research/subjects/plants/oregano_greek.md) (*Origanum vulgare*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
  - [Oregano](research/subjects/plants/oregano.md) (*Origanum vulgare*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
- **Genus Salvia**
  - [Garden sage](research/subjects/plants/sage.md) (*Salvia officinalis*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
  - [Prostrate rosemary](research/subjects/plants/rosemary_prostrate.md) (*Salvia rosmarinus*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
  - [Purple sage](research/subjects/plants/sage_purple.md) (*Salvia officinalis*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
  - [Rosemary](research/subjects/plants/rosemary.md) (*Salvia rosmarinus*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
- **Genus Thymus**
  - [Lemon thyme](research/subjects/plants/thyme_lemon.md) (*Thymus × citriodorus*; cultivar or horticultural selection not yet specified) — research-only; infocard pending
  - [Thyme](research/subjects/plants/lamiaceae.md) (*Thymus vulgaris*; common thyme) — infocard `thyme`

### Order: Malpighiales

#### Family: Violaceae

- **Genus Viola**
  - [Pansy](research/subjects/plants/pansy.md) (*Viola × wittrockiana*; garden pansy hybrid group) — infocard `pansy`

### Order: Malvales

#### Family: Malvaceae

- **Genus Abelmoschus**
  - [Okra](research/subjects/plants/okra.md) (*Abelmoschus esculentus*; cultivar or horticultural selection not yet specified) — research-only; infocard pending

### Order: Myrtales

#### Family: Onagraceae

- **Genus Fuchsia**
  - [Fuchsia](research/subjects/plants/fuchsia.md) (*Fuchsia spp.*; cultivated fuchsia; species/hybrid unspecified) — infocard `fuchsia`

### Order: Poales

#### Family: Poaceae

- **Genus Zea**
  - [Sweet corn](research/subjects/plants/corn_sweet.md) (*Zea mays*; sweet-corn cultivar group) — infocard `corn_sweet`

### Order: Rosales

#### Family: Moraceae

- **Genus Ficus**
  - [Fig](research/subjects/plants/fig.md) (*Ficus carica*; common fig) — infocard `fig`

#### Family: Rosaceae

- **Genus Fragaria**
  - [Strawberry](research/subjects/plants/strawberry.md) (*Fragaria × ananassa*; garden strawberry) — infocard `strawberry`
- **Genus Malus**
  - [Apple (semi-dwarf)](research/subjects/plants/apple.md) (*Malus domestica*; semi-dwarf form; rootstock unspecified) — infocard `apple`
- **Genus Prunus**
  - [Peach](research/subjects/plants/peach.md) (*Prunus persica*; peach) — infocard `peach`
- **Genus Pyrus**
  - [Pear (European, dwarf)](research/subjects/plants/pear.md) (*Pyrus communis*; dwarf form; rootstock unspecified) — infocard `pear`
- **Genus Rubus**
  - [Raspberry](research/subjects/plants/raspberry.md) (*Rubus idaeus*; red raspberry) — infocard `raspberry`

### Order: Sapindales

#### Family: Rutaceae

- **Genus Citrus**
  - [Meyer lemon](research/subjects/plants/lemon_meyer.md) (*Citrus × meyeri*; Meyer lemon) — infocard `lemon_meyer`

### Order: Solanales

#### Family: Convolvulaceae

- **Genus Ipomoea**
  - [Sweet potato](research/subjects/plants/sweet_potato.md) (*Ipomoea batatas*; cultivar or horticultural selection not yet specified) — research-only; infocard pending

#### Family: Solanaceae

- **Genus Capsicum**
  - [Pepper (bell)](research/subjects/plants/pepper.md) (*Capsicum annuum*; bell pepper cultivar group) — infocard `pepper_bell`
- **Genus Petunia**
  - [Petunia](research/subjects/plants/petunia.md) (*Petunia × atkinsiana*; garden petunia hybrid group) — infocard `petunia`
- **Genus Solanum**
  - [Eggplant](research/subjects/plants/pepper.md) (*Solanum melongena*; eggplant cultivar group) — infocard `eggplant`
  - [Potato](research/subjects/plants/potato.md) (*Solanum tuberosum*; cultivated potato) — infocard `potato`
  - [Tomato (cherry)](research/subjects/plants/tomato.md) (*Solanum lycopersicum*; cherry tomato cultivar group) — infocard `tomato_cherry`
  - [Tomato (determinate)](research/subjects/plants/tomato.md) (*Solanum lycopersicum*; determinate growth-habit group) — infocard `tomato_determinate`
  - [Tomato (indeterminate)](research/subjects/plants/tomato.md) (*Solanum lycopersicum*; indeterminate growth-habit group) — infocard `tomato_indeterminate`
  - [White eggplant](research/subjects/plants/eggplant_white.md) (*Solanum melongena*; cultivar or horticultural selection not yet specified) — research-only; infocard pending

## Taxonomy governance

- Accepted names and synonymy must be checked against POWO and World Flora Online; IPNI is used for nomenclatural publication data, not morphology.
- Keep hybrid markers and infraspecific ranks explicit. Where a card represents multiple species or an unspecified cultivar, mark that ambiguity rather than assigning a false exact taxon.
- A taxon may have several horticultural infocards (for example, determinate and indeterminate tomato); each infocard points to the same species and uses its own subordinate horticultural label.
- Research-only profiles remain visible in this index. This organizational change does not authorize rendering.
