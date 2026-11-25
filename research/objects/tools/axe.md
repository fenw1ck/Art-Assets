---
id: axe
title: Ax (single-bit felling ax)
kind: object
parent: tools
aliases: [ax, axe, hatchet, felling axe, bronze ax, iron ax, starmetal ax]
depth: outline
updated: 2026-11-24
gaps: [double-bit and broad axes, photos of ancient bronze heads (shaft-hole axes), head weights by tier]
used_by: [tools.js drawAx, euclid game.html (vine cutting)]
traits:
  head_shape: single-bit
  head_metal: wrought iron
  head_colour: "#6d7177"
  haft_wood: hickory
  haft_colour: "#b07c45"
  lugs: true
  strikes: 6
---

# Ax

## Parts

- **Head:** the **bit** (blade) at one end and the **poll** (butt) at the other. The flat sides are the **cheeks**, often slightly hollow. The bit's upper corner is the **toe**, the lower one the **heel**; the edge is ground to a **bevel**. A **beard** is a heel that drops well below the rest of the head. **Lugs** are bulges above and below the eye that give the handle more grip.
- **Eye:** the slot the handle passes through. The handle's end shows at the top of the head, split by a wedge (the **wedge kerf**).
- **Haft** (handle, helve): the **shoulder** flares to fill the eye and stops the head sliding down; then the **throat**, the long **belly** (its upper edge is the **back**), the **grip** and a swelled **knob** at the end so it cannot slip from the hand.
- **Wood:** hickory most of all, or ash: strong and springy. Good handles have the grain running straight along their length, in line with the head.
- **Metal:** the edge is hardened and tempered harder than the body; a faint **temper line** shows where they meet. A poll hammered on hard things mushrooms.

## Distinguishing features (the game's three tiers)

| Tier | Name | Strikes to cut a door's vines | Head | Haft |
|---|---|---|---|---|
| basic | Bronze Ax | 10 | cast bronze, small, flared bit, no lugs, verdigris in the pits | pale ash |
| improved | Iron Ax | 6 | forged iron, bigger, lugs, bright bevel, temper line | hickory |
| best | Starmetal Ax | 3 | blue-black "starmetal" with star speckle and a gold inlay, bearded bit | dark hickory, gold-wire wrap over leather |

The strike counts follow Stardew Valley's ladder (10 hits for a tree with the starter axe, then fewer per upgrade).

## Construction order

1. Haft: an S along the belly, width swelling at the knob and flaring at the shoulder; light on the left edge; straight grain lines; hickory gets a darker heartwood streak.
2. Grip wrap (best tier only).
3. Head outline (rounded polygon per head shape), metal ramp top to bottom, a soft highlight in the cheek's hollow, the poll side in shade.
4. Bevel band and the bright cutting edge; temper line (iron); verdigris (bronze); star speckle and inlay (starmetal).
5. Lugs, the haft's end and wedge in the eye, the maker's mark (detail size only).

## States

- **Held** (still) and **swing**: wind-up behind the shoulder, an accelerating strike, a bounce off the vine. The bit glints at the moment of the strike.

## Rendering notes

- Never a black outline: a darker shade of the local colour (see `rendering/readability.md`).
- At icon size (≤48 px) the grain, temper line and mark are left out; the head's shape and colour carry the tier.
- Metal: see `materials/metal/_metal.md` (bronze browns and verdigris; iron dark grey, bright where ground).

## Log

- 2026-11-24: created for the Euclid game's ax. Parts from the US Forest Service's *An Ax to Grind* and Wikipedia; tiers modelled on Stardew Valley.

## Sources

- US Forest Service, *An Ax to Grind*, ch. 4 "Anatomy of an Ax": https://fs.usda.gov/t-d/pubs/pdfpubs/pdf18232812P/Part04_Anatomy.pdf
- US Forest Service, ax parts figure: https://www.fs.usda.gov/eng/pubs/htmlpubs/htm99232823/ld/fig003.htm
- Outdoor Life, visual glossary of axes: https://www.outdoorlife.com/articles/hunting/2014/04/visual-glossary-components-axes-and-hatchets
- Wikipedia, Axe: https://en.wikipedia.org/wiki/Axe
- Brant & Cochran, axe handle anatomy: https://www.bnctools.com/blogs/news/get-a-handle-on-it-part-2
- Stardew Valley Wiki, Axes: https://stardewvalleywiki.com/Axes
