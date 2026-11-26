---
id: house-style
title: The house style (all new art)
kind: technique
parent: none
aliases: [house style, art style, euclid art style, silhouette, back-lit, backlit, rim light, rim lighting, moonlight, accurate proportions]
depth: outline
updated: 2026-11-25
gaps: [rooms, plants and items drawn in it (only the creatures are so far), how rooms light a silhouette indoors (torches as the back-light), animation of the skeleton between poses]
used_by: [core.js ART_CORE.house, creatures.js, engine.js ENGINE.skeleton]
---

# The house style

Chosen 25 Nov 2026 (ticket "Euclid Game Art", after ten style drafts of the manticore): **accurate proportions** (draft 1) with **back-lit silhouette lighting** (draft 9). Not photorealistic rendering, not rounded or cartoon shapes. Every new piece of art follows it unless a ticket asks otherwise.

## Parts (the rules)

1. **Proportions are anatomical.** Bodies come from `ENGINE.skeleton` (engine.js), built from each animal's real proportions: a lion's body for the manticore, a man about 7.5 heads tall for the minotaur, a vulture-sized bird for the harpy, true snake proportions (the head wider than the neck) for the basilisk and hydra. The style paints the body; it never changes its proportions.
2. **The light is behind the subject.** A pale moon (or another light) sits behind it, so the subject is one dark shape (`#070c0f`, never pure black) against a lit, misty background.
3. **Only the outer edge is lit.** A thin cool rim (`#d6f2ff`) plus a softer glow (`#9fd8f0`) along the outline of the whole silhouette: the merged shape, never each part separately (lit edges inside the body read as plastic).
4. **Texture lives on the edge.** Fur and manes break the outline with hair (manes radiate outward from the head); feathers show short tips; scales, horn, hoof and chitin keep a clean edge.
5. **Faint inner contours** (about 20% blue-grey) where a near part overlaps the body, and faint struts for wing bones, so legs and wings still read.
6. **Eyes glow:** amber when calm, burning red-orange when threatening, dim when hurt, dark when dead. They are the only warm colour.
7. **States change the pose, not the paint:** threatening rears and raises wings or a fist; wounded hunches and lowers the head; dead lies down and the rim fades.

## Construction order

Skeleton parts (back to front) → fill all into one silhouette → hair and feather edges → faint inner contours and bones → rim (silhouette minus itself moved away from the light) → outer glow → eyes.

## Rendering notes

- `ART_CORE.house.paint(ctx, W, H, parts, o)` does all of the above; `ART_CORE.house.moon()` paints the back-light for cards and sheets.
- Cache it: paint each pose once into an offscreen canvas per size bucket (creatures.js does).
- Below about 30 px the hair edges are skipped; the rim and eyes still read.

## Log

- 2026-11-25: created. Replaces the "storybook" draft of the same day, which was rejected as too rounded; ten drafts followed (photorealistic, anime, 3D film, pixel art, low-poly, comic, painterly, dark fantasy, silhouette, flat vector), each with its own body. The choice was draft 1's proportions with draft 9's lighting.

## Sources

- Rim lighting and silhouettes as a readability tool are common in back-lit game art (for example Limbo and Hollow Knight). No images were copied; the approach is drawn in code.
- Anatomy: the creature entries in `research/subjects/creatures/` and their sources.
