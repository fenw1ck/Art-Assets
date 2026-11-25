# art-assets

All the art for fenw1ck's projects (the Euclid game, the Planting Guide and any future project) lives here, together with the research behind it. Each project copies the files it needs at release.

## Files

- `core.js`: shared helpers: colour, hue-shifted colour ramps, seeded random numbers, noise, warped noise, Voronoi cells and the ground shadow, plus the factor modules for perspective (`view`, `face`), shading (`light`, `shade`), line (`ink`, `weight`) and resolution (`lod`). Load it first. `plants.js` and `garden.js` still have their own copies of these and will move onto `core.js` one at a time, each move checked pixel for pixel.
- `containers.js`: chests drawn from research traits (`CONTAINERS.drawChest`), closed or open, flat or domed lid, with wood grain, iron or brass fittings, wear and coins. Needs `core.js`.
- `plants.js`: `drawPlant` and the 51 plant symbols (name, silhouette, colours, mature size).
- `garden.js`: `window.GARDEN`, the garden generator and its shared pieces:
  - `plan(seed)` lays out a walled garden 8–50 cells wide and 16–50 tall, themed herb, vegetable, fruit, flower or mixed: paths, beds planted at each plant's spread, trellises, lanterns, benches, tools, a fountain, lock spots, a treasure spot and the gate.
  - `render(plan, s)` draws the still parts onto a canvas at `s` px per cell.
  - `fountain`, `lantern` (animated), `chest`, `pedestal` and `gate` each draw a single piece at any scale.

  `garden.js` needs `plants.js` loaded first.
- `research/`: the research library: living things (plants, birds), made things (containers), materials (stone, wood, metal), floor layouts, and how to render them (light and shadow, colour, textures, wear, readability). Entries carry `traits` in the vocabulary of `research/traits.yaml`, which the drawing programs read. See `research/README.md`. It replaces PLANT_ART.md.
- `index.html`: the Art Asset Builder (fenw1ck.github.io/Art-Assets): intake, library lookup, a live preview when the engine can already draw it, and the brief.

## Tools

- `python3 tools/research.py lookup <name>`: what the library already knows, level by level. Also `traits`, `map`, `check` and `index`.
- `python3 tools/contact-sheet.py`: every plant in every state, the size ladder, the chests and core.js's test swatches, on light and dark backgrounds, written to `contact/`. With `--compare <folder>` it reports which pixels changed.

## Making new art

1. Answer the intake questions.
2. Look up the research and choose: use it as it is, fill its gaps, or search deeper.
3. Build.
4. Check with the contact sheets.
5. Add what was learned to `research/`.

The full process is in the project doc *Art process plan*.
