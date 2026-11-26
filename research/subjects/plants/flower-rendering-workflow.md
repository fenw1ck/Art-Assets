---
id: flower-rendering-workflow
title: Flower rendering workflow
kind: method
parent: plants
updated: 2026-11-25
used_by: [plants.js]
---
# Flower rendering workflow

This is the standard process for adding flowering plants to `fenw1ck/Art-Assets`.

## Required sequence
1. **Research the species first.** Use botanical references and close photographs to establish leaf structure, arrangement, stem habit, branching, inflorescence position and flower morphology. Record sources in a species research file.
2. **Describe the growth architecture.** Decide whether the plant is trailing, climbing, upright, mounded, rosette-forming, branched or otherwise. Identify the actual repeating unit (if any). Do not borrow recursive construction from another species unless its growth habit supports it.
3. **Build individual botanical parts.** Implement leaves, stems, buds and flowers as separate drawing functions. Preserve the real petal arrangement and flower symmetry (radial vs bilateral), leaf venation and attachment.
4. **Build the whole plant from its rules.** Place parts at biologically plausible nodes and inflorescences. Use seeded variation so every specimen is reproducible.
5. **Render every life stage from one shared structure.** Immature, mature and past-flowering states should differ by age, not by unrelated redraws. Past flowering should remove or fade flowers while retaining plausible stems and foliage.
6. **Make a variation set.** Provide at least 15 deterministic mature specimens where appropriate. Vary branch geometry, leaf dimensions/orientation, flower number and placement while preserving the species' identity.
7. **Render and inspect.** Use `tools/contact-sheet.py --sheet plants` and the plant preview to inspect all stages and seeds. Check silhouette, leaf morphology, flower shape, stem connections, clipping and small-size readability against botanical references.
8. **Revise before release.** Do not push a renderer as finished until its contact sheet has been rendered and visually inspected. Keep the reference plate in `research/plates/`.

## Architectural rule
A shared rendering framework is encouraged; a shared growth habit is not. Recursive shoots, axillary branching, tendrils, terminal heads, racemes and trailing stems are distinct botanical mechanisms. Choose the construction that the researched species supports.

## First comparative plate
See `research/plates/flower-growth-studies.svg` for Nasturtium, Calendula, Pansy and Sweet pea. It is a visual study, not a substitute for species-specific code validation.
