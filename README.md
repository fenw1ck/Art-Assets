# art-assets

Shared art for the Euclid game and the Planting Guide. Each project copies the files it needs at release.

## Files

- `plants.js` — `drawPlant` and the 50 plant symbols (name, silhouette, colours, mature size).
- `garden.js` — `window.GARDEN`, the garden generator and its shared pieces:
  - `plan(seed)` lays out a walled garden 8–50 cells wide and 16–50 tall, themed herb, vegetable, fruit, flower or mixed: paths, beds planted at each plant's spread, trellises, lanterns, benches, tools, a fountain, lock spots, a treasure spot and the gate.
  - `render(plan, s)` draws the still parts onto a canvas at `s` px per cell.
  - `fountain`, `lantern` (animated), `chest`, `pedestal`, `gate` draw single pieces at any scale.

`garden.js` needs `plants.js` loaded first.
