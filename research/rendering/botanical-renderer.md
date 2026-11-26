---
id: botanical-renderer
title: Botanical Renderer
kind: method
parent: plants
aliases: [botanical intake, plant renderer, plant-art]
updated: 2026-11-25
used_by: [botanical-renderer.html, tools/plant-art.py]
gaps: [browser-to-Python job handoff, raster export of existing PLANTS.draw artwork, semantic image editing and mask workflow]
---

# Botanical Renderer

## Purpose

The Botanical Renderer is the research and artwork workflow for every plant in Fenwick. Its first responsibility is to preserve the best existing artwork, not replace it with a lower-quality procedural approximation. Its second is to make the plant's real botanical construction explicit enough that future renderings remain species-specific.

## User intake

The website tab `botanical-renderer.html` collects:
- identity: common and scientific name, cultivar, family;
- source art: existing Fenwick path, starting-art status and uploaded reference images;
- growth habit and architecture: main axis, branching, node spacing, internodes, dimensions and support;
- leaf anatomy: arrangement, simple/compound form, shape, petiole, venation, margin, surface and colour;
- flowers and fruit: inflorescence position, flower anatomy, fruit placement and morphology, harvest organs and season;
- requested life stages and visual requirements;
- user-supplied source URLs, research notes, open questions and region context.

Unknown fields are not defaults to guess. They become explicit research tasks in the exported JSON. The form supports users who know only the common name and can attach photographs; it does not require botanical vocabulary.

The form currently exports a portable JSON brief in the browser. It does not itself search the web, submit a server job, or invoke Python. Plant cards in the main Art Library now offer a source PNG export so the existing JavaScript canvas drawing can be supplied to the Python workflow. The next integration step is a trusted job handoff that passes the exported brief and exported source art to research and rendering tools.

## Non-negotiable asset preservation sequence

1. Find the best existing Fenwick artwork and its source code, research entry and related references.
2. Duplicate the original into a versioned working/source location. Never write over the original file or source function.
3. Inspect the source's visual identity: silhouette, proportions, palette, line quality, shading, leaf detail, stem structure and composition.
4. Research only the gaps not already answered by Fenwick's research or user-supplied evidence.
5. Extend or vary the existing construction. Prefer the existing species-specific drawing function and parts. Add anatomy-aware overlays, masks, compositing or transformations only where they preserve the original's quality.
6. Generate requested life stages from shared botanical rules, not unrelated redraws.
7. Compare every candidate to the source at full size and at library-card size. Reject a candidate that loses botanical detail or visual identity.
8. Save derived work separately with its source path, source hash, research sources, assumptions and renderer version.

A superior existing approved image may be reused unchanged. A new procedural image is never required merely because the renderer can draw one.

## Botanical construction requirements

- Identify the actual growth habit and main axis before choosing a branch algorithm.
- Record leaf arrangement (phyllotaxy), blade type and shape, margin, surface, venation, petiole and attachment.
- Record nodes and internodes, branch origin and branching sequence.
- Record where flowers form and whether they are solitary or in a particular inflorescence.
- Record fruit or seed placement, number per group, shape and ripening sequence.
- Build distinct species-specific structures. Do not make tomato, pepper and beans into one generic plant with different colours.
- Reuse recursion only when the researched species has a self-repeating shoot pattern. Tomato suckers, pepper forked branching and bean twining/leaflet/tendril structures are different mechanisms.

## Existing Fenwick research is the first lookup

Before external research, consult:
- `research/subjects/plants/_plants.md` for shared plant anatomy, leaf terminology and life stages;
- `research/subjects/plants/tomato.md` for tomato compound leaves, axillary suckers and trusses;
- `research/subjects/plants/pepper.md` for pepper simple leaves, forked branching and single flowers;
- `research/subjects/plants/flower-rendering-workflow.md` for the established flower construction and inspection process.

Treat user notes and references as evidence with provenance. Distinguish observed facts, sourced facts, inferred details and rendering choices. Do not silently promote an inference to a botanical fact.

## Technical note: source artwork and Pillow

The canonical live plant drawings currently live in `plants.js` and are drawn to a browser canvas. The Art Library's **Download source PNG** action exports that drawing losslessly from the browser canvas. Pillow can open, duplicate, resize, mask, composite and transform raster images; it does not execute the JavaScript drawing functions or understand plant anatomy in a PNG. Therefore, a raster duplicate is a protected starting point, not an intelligent botanical edit.

To use an existing `PLANTS.drawFit` / species drawing as a true source, first export it losslessly from the browser canvas (or port its drawing primitives to a shared renderer), then give that raster to Python as an immutable source. Pillow can then preserve it exactly and support controlled compositing. New growth, altered leaf placement or new life stages still require explicit botanical construction rules or a capable image-editing model; they cannot be safely inferred from pixels alone.

The Python renderer now writes only under `plant-art/derived/`; it does not overwrite artwork in `plant-art/`. Pass `--source-image PLANT_ID=PATH` to copy an approved source byte-for-byte into `plant-art/derived/source/` and create an unchanged working copy as the candidate image. Existing derived outputs are protected too; `--replace-derived` is required to replace them and never targets the source folder. The generic procedural path remains a draft, not a replacement for established plant drawing functions. Do not promote its output over approved Fenwick artwork.

## Quality gate

- Source image and source code remain unchanged.
- All research gaps are either answered with cited sources or left visibly unresolved.
- Branching, node spacing, petioles, leaf morphology, flowers and fruit placement are checked against the species evidence.
- Tomato, pepper, bush bean and pole bean remain visibly and structurally distinct.
- Seeded variations are reproducible.
- A contact sheet and full-size review are completed before release.
- A renderer that cannot improve on the approved source reuses the source unchanged.

## Log

- 2026-11-25: expanded the 32 profile-only plants into 32 species-specific research records. Each record includes taxonomic identity, growth habit, stem/node and branching architecture, leaf morphology and attachment, flower/inflorescence placement, fruit or harvest-organ anatomy, renderer construction rules, linked references, and explicit unresolved cultivar or growth-stage questions. All 57 infocards now link to a research record; the 32 newly researched plants have 117 linked source references in total. No artwork was generated.
- 2026-11-25: populated all 57 plant infocards from the canonical plant list and existing construction profiles. Each record now contains at least 8 populated user-data fields, with field-level provenance, linked research records and known gaps where available. The eight existing flower image references are retained; no new images were rendered. Added a data-only `--infocards-only` command and changed CI to validate card coverage without generating images.
- 2026-11-25: created the Botanical Renderer branch and website intake tab. The intake exports a structured brief with user evidence and explicit research tasks. Added browser-canvas source PNG export and changed Python output to a protected derived workspace. Server-side research/render job handoff and anatomy-aware editing remain future integration work.
