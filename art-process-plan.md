# Art Asset Builder: the process (draft 4, 24 Nov 2026)

What happens when you give me a prompt for art:

1. **Intake:** you answer a few questions.
2. **Research:** I look up what the library already holds, and you choose how much more to research.
3. **Build.**
4. **Check.**
5. **Add what was learned back to the library.**

Everything lives in `fenw1ck/art-assets`. Research is kept and added to over time, so nothing is researched twice.

## Decisions so far

- All art from every repo lives in art-assets. The projects copy what they need at release.
- PLANT_ART.md now lives only in art-assets, as the plant entries in `research/subjects/plants/`. The copies in Planting-Guide and euclid can be deleted.
- Decline is realistic: no cartoon rot symbol or flies.
- Abandoned greenhouses show some declining and dead plants among the healthy ones.
- The research library is cumulative. It is scanned first. New research runs only to fill a missing entry or a listed gap, or when you ask for a deeper search.
- You choose the next piece of art after order-of-work steps 1 and 2.

---

## 1. Intake (the user interface)

Two required questions, one optional description, and three advanced settings that the engine fills by default.

| # | Question | How it's answered | If left blank |
|---|---|---|---|
| 1 | **What is it?** | free text: "a brass oil lamp", "a robin", "the corridor floor" | required |
| 2 | **Where will it be seen?** | choose the project and place, e.g. Euclid hall / greenhouse / map / Planting Guide plot / card | required. The place sets the view and the size range |
| 3 | **Texture or look notes** | optional free text, no yes/no: "Salamanca golden stone, worn smooth in the middle", "glossy, chipped enamel" | the engine works out the textures from research |
| 4 | **States** (advanced) | the engine proposes them from research and you confirm or edit: lamp = on/off; plant = seedling, immature, mature, dead (+ declining, dormant where they apply) | the proposed list |
| 5 | **Repeating structure** (advanced) | e.g. "branches like a tomato" | the engine picks it from research (section 3) |
| 6 | **Variation between copies** (advanced) | e.g. "every hall different", "always identical" | seeded variation, the same on every visit |

For now the intake runs here in chat as a short question card. It can also become a page in art-assets (`builder.html`) that writes the brief to a file.

---

## 2. Research: the library comes first

**Where research lives:** `research/` in art-assets. Each entry is one file with a header (id, parent, aliases, depth, date, gaps). Entries form a tree, and each inherits from its parent:

```
subjects/   plants → solanaceae → tomato, pepper; lamiaceae; apiaceae; allium
            birds
materials/  stone → marble, villamayor-sandstone
patterns/   floors
rendering/  light-and-shadow, colour, textures, wear, readability   (how to draw anything)
```

A robin entry will hold only what makes it a robin. Wings, feather tracts and bill parts stay in `birds` and are never researched again.

**Depth levels:**
- **outline:** terms and main facts, 1–2 sources.
- **standard:** checked against several sources, with photos per state.
- **deep:** adds measurements, variation, and change over time.

**The flow for every prompt:**

1. `python3 tools/research.py lookup <subject>` walks the tree from the subject up to its root. For each level it reports whether the entry exists, its depth, its date and its listed gaps. For something new, `lookup robin --in birds` shows what the parent already covers.
2. I show you the result and you choose:
   - **Use as is:** go straight to building.
   - **Fill the gaps:** research only the missing levels and listed gaps.
   - **Deeper search:** take the entry up a depth level.
3. New findings are added to the right entry, never written over:
   - in my own words, with sources;
   - with a dated log line;
   - with the filled gaps removed;
   - with a raised depth if the entry now qualifies.
   - A fact true for all the siblings moves up to the parent.
4. `research.py check` validates the library. `research.py index` rewrites `research/index.json`, the map that other tools read.

**What every entry records:** parts (the shared anatomy), distinguishing features (these become the drawing's settings), construction order, states, rendering notes, log, and sources with licences.

---

## 3. Build

1. **Parts:** one function per part, shared across subjects: leaf, flower, fruit, stem; feather, bill; stone, seam, vein.
2. **Assembly rule:** one repeating pattern per subject:

   | Pattern | Examples |
   |---|---|
   | Recursive shoot | tomato |
   | Repeated fork | pepper, trees |
   | Opposite pairs turned 90° | mint family |
   | Compound frond | parsley |
   | Umbel of umbels | dill |
   | Golden-angle spiral | lettuce, sunflower |
   | Whorl stack | lavender |
   | Overlapping rows | feathers, roof tiles |
   | Tiling with jitter | floors, ivy |
   | Ring repeat | crowns, astrolabes |

3. **States** come from the same structure.
4. **Material layers,** in order: colour ramp (`ART_CORE.ramp`), pattern (`fbm`, `warp`, `voronoi`), seams, wear, light and shadow, then the scene tint.
5. **Variation,** seeded; palette swaps; swapped parts.
6. **Level of detail:** icon (≤48 px), card (96–200 px), detail (≥400 px).

## 4. Check

- **Silhouette test:** filled black, it still reads as itself, and states change the shape.
- **Greyscale value check:** it separates from its background.
- **`tools/contact-sheet.py`:** every asset × state × size, on light and dark backgrounds. `--compare` reports pixel changes against an earlier run, so a refactor can be proven to change nothing.
- **Side by side with the reference photos.** Each fix becomes a rule in code, and anything learned goes into the library.

## 5. Info card (one per asset)

Laid out like Euclid's blueprint title block: id and name; kind or family; states; sizes checked; palette ramps; assembly pattern; textures; variation controls; research entries used (with depth); sources; used by; version; last checked; known issues.

---

## 6. Order of work

1. ✅ Research library (`research/`, `tools/research.py`), seeded with the plant entries from PLANT_ART.md and outlines for birds, stone, marble, Villamayor sandstone, floor layouts and five rendering topics.
2. ✅ `core.js` (colour ramps, both existing RNGs kept exactly, noise, warped noise, Voronoi, ground shadow) and `tools/contact-sheet.py`. Not wired into plants.js or garden.js yet, so existing art is unchanged.
3. **Your choice of art next.** Candidates:
   - plant states with realistic decline, plus the abandoned greenhouses;
   - Euclid corridor floors;
   - moving the other game.html art into art-assets;
   - a new subject.
