# The research library

Everything learned while making art is kept here, so it is learned once. Before any new art is built, the library is checked first. Research only runs again to fill a gap, or when you ask for a deeper search. New findings are added to the entries, never written over them.

## How it is organised

Each entry is one Markdown file with a short header (front matter), in a tree:

```
research/
  rendering/      how to draw anything: light and shadow, colour, textures, wear, readability
  subjects/       what things are made of: plants, birds, … (class → family → species)
  materials/      stone, wood, metal, glass … (class → kind → named stone)
  patterns/       layouts: floors, walls, bonds, inlay
```

An entry only holds what is new at its level and inherits the rest from its parent. "Robin" lists what makes a robin a robin (bill, colours, proportions). It inherits wings, feather tracts and the bill's parts from `birds`, through `passerines` once that entry exists.

## The header

```yaml
---
id: tomato                  # unique, lower case
title: Tomato
kind: subject               # subject | material | pattern | technique
parent: solanaceae          # the entry it inherits from (none for a root)
aliases: [Solanum lycopersicum, cherry tomato]
depth: standard             # outline | standard | deep (see below)
updated: 2026-11-24
gaps: [seedling true-leaf shape, decline photos]
used_by: [plants.js drawTomato]
---
```

**Depth.**
- **outline:** the terms and the main facts from 1–2 sources. Enough to start a drawing.
- **standard:** checked against several sources, with photos per state. Enough to build a finished asset.
- **deep:** standard, plus measurements, variation within the kind, and how it changes over time or use.

## The body

Every entry uses the same sections; leave out any that don't apply:

1. **Parts:** the components every member shares (the shared anatomy at this level).
2. **Distinguishing features:** what sets it apart from its siblings. These become the drawing's parameters.
3. **Construction order:** how to build the drawing, part by part.
4. **States:** how it changes (growth, decline, on/off, wear).
5. **Rendering notes:** materials, textures and the techniques from `rendering/` that apply.
6. **Log:** dated notes on what was added and why.
7. **Sources:** title, URL, and the licence of any image.

## Looking something up

```
python3 tools/research.py lookup robin      # walks robin → birds and reports what exists
python3 tools/research.py map               # the whole tree, with depth and gaps
python3 tools/research.py check             # validates headers and parents
```

`lookup` prints, for each level from the subject up to the root, whether an entry exists, its depth, its date and its gaps. That tells you what to ask:

- **Everything needed exists:** use it as it is, or run a deeper search.
- **Some levels are missing or have gaps:** research only those levels and gaps, then add the results.
- **Nothing exists:** research from the nearest existing parent down.

## Adding research

- Add to the right section, write it in your own words, and cite the source.
- Raise `depth` only when the entry meets the next level.
- Update `updated`, add a line to the log, and remove the gaps that are now filled.
- When a fact applies to all the siblings, move it up to the parent entry.
