# art-assets

All the art for fenw1ck's projects (the Euclid game, the Planting Guide and any future project) lives here, together with the research behind it. Each project copies the files it needs at release.

## Files

- `core.js`: shared helpers: colour, hue-shifted colour ramps, seeded random numbers, noise, warped noise, Voronoi cells and the ground shadow, plus the factor modules for perspective (`view`, `face`), shading (`light`, `shade`), line (`ink`, `weight`) and resolution (`lod`). Load it first. `plants.js` and `garden.js` still have their own copies of these and will move onto `core.js` one at a time, each move checked pixel for pixel.
- `containers.js`: chests drawn from research traits (`CONTAINERS.drawChest`), closed or open, flat or domed lid, with wood grain, iron or brass fittings, wear and coins. Needs `core.js`.
- `tools.js`: `TOOLS.drawAx`, the ax in three tiers (Bronze, Iron, Starmetal: 10, 6 and 3 strikes), metal head on a wooden haft, with `TOOLS.swing(u)` for the swing and `TOOLS.bitPoint` to aim it. Needs `core.js`.
- `vines.js`: `VINES.render`, woody vines grown over a doorway: English ivy, muscadine grape, wisteria and Virginia creeper, with their leaves, bark, rootlets or tendrils, and sometimes flowers, fruit or autumn colour. States: full, damaged (0..1, clearing from the lock outward, an even share per strike) and cut back. `VINES.pick(seed)` chooses a species per door; `VINES.removed` lists the leaves that fall between two damage values. Needs `core.js`.
- `furniture.js`: `FURNITURE.bookshelf`, `.armchair` (front or side) and `.sideTable` (with a lit lamp): the library room's furniture at standard sizes. Needs `core.js`.
- `floors.js`: `FLOORS.stone`, `.wood` and `.carpet`: indoor floor textures (top-down, 1 unit = 1 m) for every room that is not a greenhouse; a carpet can be laid on either. Needs `core.js`.
- `bedroom.js`: `BEDROOM.bed` (canopy, tree of life, art deco, four-post, bunk, Japanese futon; front or side view), `.nightstand`, `.nightlight` (cylinder, sphere, jar of fireflies) and `.mobile` (propeller planes, woodland creatures, space). Needs `core.js`.
- `items.js`: `ITEMART.draw` for every item the Euclid game knows (treasure, clothing, tools, the chest), `ITEMART.coin` (beaded rim, legend, crest; gold, silver, bronze; fresh, worn, rusty, muddy) and `ITEMART.coins` (a heap). Scrolls (ribbon per colour), clothing (boots in three speed upgrades, greaves, chiton, trousers) and potions (weed killer: fluid colour by strength, `o.level` for how full). Weapons: `weapon-<knife|sword|staff>-<bronze|iron|starmetal>` with `o.state` perfect, damaged or broken (`--sheet weapons`). Fuel and cooking: `firewood`, `kindling`, `cauldron`, and cooked food `dish-<recipe>`, `cooked-<plant>`, `burnt`. Food: `potato-red|purple|brown` (raw, uses `PLANTS.tuber` when plants.js is loaded), `potato-baked`, and `produce-<plant id>` (drawn by the part harvested). Needs `core.js`; uses `containers.js` and `tools.js` when present.
- `engine.js`: **the game engine** (now also `skeleton`: posable creature bodies, geometry only): how the games behave, kept apart from how they look (`window.ENGINE`). Parts: `clock` (game time), `health`, `keys` (the PC layout), `locks` (lock timers and cooldown), `moves` (jump, climb, ledges, falls), `traps` (plates, the Euler-path trap), `combat` (weapons, creatures, wear), `fuel` (kindling, firewood, trees) and `cook` (recipes, ingredients, the timing minigame). No drawing; numbers are named fields. `ENGINE.parts` describes each part. The Euclid game is its first user (copy the file there after a change).
- `items.js`: `ITEMART.draw` for every item the Euclid game knows (treasure, clothing, tools, the chest), `ITEMART.coin` (beaded rim, legend, crest; gold, silver, bronze; fresh, worn, rusty, muddy) and `ITEMART.coins` (a heap). Scrolls (ribbon per colour), clothing (boots in three speed upgrades, greaves, chiton, trousers) and potions (weed killer: fluid colour by strength, `o.level` for how full; health potions `health-minor|greater|supreme`: red fluid, a caduceus stopper in bronze, silver or gold with 2, 3 or 4 feathers a wing). Backpacks: `backpack-satchel|rucksack|expedition` (16, 24, 32 slots in the game; research `objects/items/backpack.md`). Weapons: `weapon-<knife|sword|staff>-<bronze|iron|starmetal>` with `o.state` perfect, damaged or broken (`--sheet weapons`). Fuel and cooking: `firewood`, `kindling`, `cauldron`, and cooked food `dish-<recipe>`, `cooked-<plant>`, `burnt`. Food: `potato-red|purple|brown` (raw, uses `PLANTS.tuber` when plants.js is loaded), `potato-baked`, and `produce-<plant id>` (drawn by the part harvested). Needs `core.js`; uses `containers.js` and `tools.js` when present.
- `engine.js`: **the game engine**: how the games behave, kept apart from how they look (`window.ENGINE`). Parts: `clock` (game time), `health`, `keys` (the PC layout), `locks` (lock timers and cooldown), `moves` (jump, climb, ledges, falls), `traps` (plates, the Euler-path trap), `combat` (weapons, creatures, wear), `fuel` (kindling, firewood, trees) and `cook` (recipes, ingredients, the timing minigame). No drawing; numbers are named fields. `ENGINE.parts` describes each part. The Euclid game is its first user (copy the file there after a change).
- `engine.html`: the **Game engine** tab of the site: one card per part with its rules read live from engine.js, a small live demo (a running clock, a health bar to poke, the keys, a lock timer, the jump arc, a playable path trap, the creatures and weapons, a playable cooking check, fuel) and **Edit this part**, which opens the Request Builder with a ticket about that part (`?engine=<part>`).
- `creatures.js`: `CREATURES.draw` for the harpy, basilisk, minotaur, manticore and hydra in four states (friendly, threatening, wounded, dead), in the house style: bodies from `ENGINE.skeleton`, painted by `ART_CORE.house`, cached per pose. Needs core.js and engine.js. Contact sheet: `--sheet creatures`.
- `kitchen.js`: `KITCHEN.stove` (cast-iron range with an oven), `.table`, `.island`, `.shelf`, `.campfire` and `.cauldron`. Contact sheet: `--sheet kitchen`.
- `traps.js`: `TRAPS.plate`, `.spikes`, `.nozzle`, `.flame`, `.fog`, `.stud` and `.edge` (the parts a room draws in its own perspective). Contact sheet: `--sheet traps`.
- `plants.js`: mint has its own drawing (`drawMint`: stolons, quilted serrate leaves, whorled flower spikes; seedling, young, mature, past/declining and dead; `immature` and `declining` are accepted as stage names). `drawPlant` and the 51 plant symbols (name, silhouette, colours, mature size). The potato has its own botanical drawing (`drawPotato`: pinnate smooth-edged leaves, forked stems, star flowers, tubers showing a third above the soil when mature; `o.hill` 0–3 for earthing up, `o.skin` red/purple/brown, otherwise seeded), plus `PLANTS.tuber` (one potato at any scale) and `PLANTS.harvest(p,{hill})` (what any plant gives when harvested: fruit, root, flower or leaf, the item id, whether it must be cooked, how many). `draw`, `drawFit` and `drawRaw` take an optional last argument `o` passed to the plant's drawing. Contact sheet: `--sheet potato`.
- `garden.js`: `window.GARDEN`, the garden generator and its shared pieces:
  - `plan(seed)` lays out a walled garden 8–50 cells wide and 16–50 tall, themed herb, vegetable, fruit, flower or mixed: paths, beds planted at each plant's spread, trellises, lanterns, benches, tools, a fountain, lock spots, a treasure spot and the gate.
  - `render(plan, s, o)` draws the still parts onto a canvas at `s` px per cell; `o.wild` gives an abandoned greenhouse floor (irregular flagstone or packed-dirt paths, moss and grass creeping in).
  - `fountain`, `lantern` (animated), `chest`, `pedestal` and `gate` each draw a single piece at any scale.

  `garden.js` needs `plants.js` loaded first.
- `research/`: the research library: living things (plants, birds), made things (containers), materials (stone, wood, metal), floor layouts, and how to render them (light and shadow, colour, textures, wear, readability). Entries carry `traits` in the vocabulary of `research/traits.yaml`, which the drawing programs read. See `research/README.md`. It replaces PLANT_ART.md.
- `index.html`: **the art library** (25 Nov 2026; https://fenw1ck.github.io/Art-Assets/). Every piece of art the modules can draw, drawn live, searchable by name, category, file and research aliases, with category filters. Tap a piece for its info card (file, function, research entry, aliases, gaps, used by) and **Edit this art**, which opens the Request Builder with an "Improve" ticket, a link back to the piece (`#<id>`) and the picture attached (passed as a PNG data URL in the hash, `#img=`). **Make new art** goes to the Request Builder. To add a new module's art to the library, add `add(...)` lines in index.html; `items.js` shows up by itself once it is on main.
- `builder-archive.html`: the retired Art Asset Builder (intake, library lookup, live preview, research library and gallery tabs), kept working in case it is needed again; the last version of the builder before the change is commit cd99c14.

## How the art is organised

Decided 25 Nov 2026, after looking at how asset libraries are organised (digital asset management guides, game asset stores, faceted classification). The library uses **one branch plus tags**, as most of them do:

- **One branch: where a piece lives** (like animal taxonomy or the Dewey system). The branches are the research tree in `research/`: kind of thing (Living things, Made things, Materials, Patterns and surfaces), then each entry's parents, down to the piece. Examples: Living things › Plants › Nightshade family › Potato; Made things › Items › Food › Potato red. A piece with no research entry of its own hangs under its nearest one, so giving it an entry later moves it to the right place.
- **Tags (facets): find it by any trait.** Five groups, each piece carrying one or more tags in each:
  - Where: indoor, outdoor, both.
  - Use: consumable, **ingredient** (food that must be cooked in an oven or cauldron before it can be eaten; set from `PLANTS.harvest(p).ingredient`), permanent, wardrobe, environment, harvest, tool, container, currency, weapon, enemy, trap, cooking, fuel.
  - Rooms: greenhouse, garden, corridor, library, bedroom, kitchen, front doors.
  - Made of: plant, wood, stone, metal, fabric, glass, paper, leather, food, soil, creature.
  - Projects: Euclid game, Planting Guide.
- **Where this lives in the code:** `index.html`. `TAGS_CAT` gives each library category its default tags, `TAGS_BY` changes them per piece, `CATPATH` gives the branch for pieces with no research entry, and each card's `res` list names its research entry (first) and fallbacks.
- **On the page:** **How it's organised** shows the branch tree and every tag with its count. A card shows its branch and its tags, and tapping either lists everything filed there. You can also filter by typing, for example `room:greenhouse`, `use:consumable` or `in:Nightshade family`.
- **Edit this art** sends the branch, the tags, the research entry (or the nearest one, as "file it under") and the drawing function to the Request Builder, which writes them into the ticket's Art brief.
- **Adding art:**
  - Give the piece a research entry where it belongs; that sets its branch.
  - Add its card with `add(...)` in `index.html`.
  - If its category's tags don't fit, add a `TAGS_BY` line. Keep to the tags above; add a new tag only when no existing one fits, and list it here.

## Tools

- `python3 tools/research.py lookup <name>`: what the library already knows, level by level. Also `traits`, `map`, `check` and `index`.
- `python3 tools/contact-sheet.py`: every plant in every state, the size ladder, the chests, the axes, the vines and core.js's test swatches, on light and dark backgrounds, written to `contact/`. With `--compare <folder>` it reports which pixels changed; `--sheet vines` renders one sheet.
- `plant-art/diverse-infocards.json`: 38 researched, taxonomy-aware infocards extending the canonical catalogue beyond the original flowering-plant set: 9 aquatic plants, 6 mosses/liverworts, 6 sedges/rushes, 7 ferns/fern allies and 10 tree species. These are research profiles, not rendered illustrations; each records order, family, genus, species, architecture, diagnostic reproductive structures, sources and remaining species-level gaps. The records are also merged into `plant-art/infocards.json`.
- `python3 tools/plant-art.py`: the Python botanical-plate renderer and infocard factory. It reads all 57 species from `plants.js`, with one construction profile per species. `--infocards-only` refreshes the canonical `plant-art/infocards.json` for all 57 plants, preserving user research, provenance and existing image references, without drawing or rendering any images. Normal rendering writes derived files only under `plant-art/derived/`; existing artwork under `plant-art/` is not overwritten. Supply approved raster sources with `--source-image <id>=<path>` to make a byte-preserving source copy and use it unchanged as the starting image; use `--replace-derived` only to replace files in the derived workspace. `--check` validates profiles, `--only <id> ...` selects plants, and `--seed N` makes procedural drafts reproducible. Requires Pillow.
- `botanical-renderer.html`: the Botanical Renderer research intake tab. Users can enter the plant's identity, growth architecture, branching and node spacing, leaf anatomy, flowers, fruit, life stages, source links, notes and reference photographs. Export produces a portable JSON research brief; this static page does not itself browse the web or run Python.

## The Euclid style guide (25 Nov 2026)

Every new piece of art follows the style for its category. Read the rules before drawing: `research/rendering/crafted-style.md` (the first three) and `research/rendering/house-style.md` (creatures).

| What | Style | Reference |
|---|---|---|
| Architecture (rooms, halls, doors, the temple) | **9 · The sublime: monumental halls**: vast colonnades in golden mist, soaring arches, great steps, light shafts, grandeur | `drafts/manticore-crafted.html` #9 |
| Objects (furniture, items, chests, tools) | **2 · Tree of Life, carved and inlaid**: warm wood relief, grain, carved bevel light, organic branching ornament | the tree-of-life bed; drafts #2 |
| Plants | **1 · Naturalist's plate**: exact botany, crisp shapes, soft light, a thin same-colour edge, fine true detail | the mint (`drawMint`); drafts #1 |
| Mythical creatures | **The shadow style** (black and white): back-lit silhouettes on `ENGINE.skeleton` (below). Leave them alone. | `creatures.js` |

Existing art moves over when it is next worked on: the plants mostly match already; the rooms and objects don't yet.

## The shadow style for mythical creatures (decided 25 Nov 2026; called the "house style" in the code)

**Mythical creatures: accurate proportions, back-lit silhouette lighting.** The subject is one dark shape lit from behind; only its outer edge catches a cool rim, hair breaks the edge, faint inner contours keep the parts readable, and the eyes glow. Bodies come from `ENGINE.skeleton` (anatomical proportions); painting is `ART_CORE.house` in `core.js`. Rules: `research/rendering/house-style.md`; read it before drawing anything. Done so far: the creatures. Older pieces (plants, rooms, items, vines) move over when they are next worked on.

## Making new art

0. Read `research/rendering/house-style.md` (the house style). Build bodies on `ENGINE.skeleton`, paint with `ART_CORE.house`.

1. Answer the intake questions in the Request Builder's art card.
2. Look up the research and choose: use it as it is, fill its gaps, or search deeper.
3. Build.
4. Check with the contact sheets.
5. Add what was learned to `research/`.

The full process is in the project doc *Art process plan*.
