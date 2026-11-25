# art-assets

All the art for fenw1ck's projects (the Euclid game, the Planting Guide and any future project) lives here, together with the research behind it. Each project copies the files it needs at release.

## Files

- `core.js`: shared helpers: colour, hue-shifted colour ramps, seeded random numbers, noise, warped noise, Voronoi cells and the ground shadow. Load it first. `plants.js` and `garden.js` still have their own copies of these and will move onto `core.js` one at a time, each move checked pixel for pixel.
- `plants.js`: `drawPlant` and the 51 plant symbols (name, silhouette, colours, mature size).
- `garden.js`: `window.GARDEN`, the garden generator and its shared pieces:
  - `plan(seed)` lays out a walled garden 8–50 cells wide and 16–50 tall, themed herb, vegetable, fruit, flower or mixed: paths, beds planted at each plant's spread, trellises, lanterns, benches, tools, a fountain, lock spots, a treasure spot and the gate.
  - `render(plan, s)` draws the still parts onto a canvas at `s` px per cell.
  - `fountain`, `lantern` (animated), `chest`, `pedestal` and `gate` each draw a single piece at any scale.

  `garden.js` needs `plants.js` loaded first.
- `research/`: the research library: what things are made of (plants, birds, stone, floor layouts) and how to render them (light and shadow, colour, textures, wear, readability). See `research/README.md`. It replaces PLANT_ART.md.

## Tools

- `python3 tools/research.py lookup <name>`: what the library already knows, level by level. Also `map`, `check` and `index`.
- `python3 tools/contact-sheet.py`: every plant in every state, the size ladder and core.js's test swatches, on light and dark backgrounds, written to `contact/`. With `--compare <folder>` it reports which pixels changed.

## Making new art

1. Answer the intake questions.
2. Look up the research and choose: use it as it is, fill its gaps, or search deeper.
3. Build.
4. Check with the contact sheets.
5. Add what was learned to `research/`.

The full process is in the project doc *Art process plan*.
