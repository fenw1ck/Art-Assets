---
id: creatures
title: Creatures of myth
kind: subject
parent: none
aliases: [monsters, mythical creatures, enemies, fantasy creatures, bestiary]
depth: outline
updated: 2026-11-25
gaps: [vase-painting references for each pose, more creatures (sphinx, griffin, chimera, cyclops)]
used_by: [creatures.js]
---

# Creatures of myth

## Parts

- The Euclid game's enemies, all from Greek (or Persian, via Greek writers) myth: harpy, basilisk, minotaur, manticore, hydra.
- **Four states, the same for each:** friendly (calm: head level or lowered, mouth shut, wings folded, tail down, soft round eyes), threatening (reared, mouth open, teeth, wings spread, tail raised, narrowed eyes with a red glint), wounded (hunched, one eye shut, cuts), dead (lying down or slumped, eyes crossed out, colour drained).
- Side view facing left, at 24–400 px. Silhouettes are kept distinct so each reads at icon size: tall biped (minotaur), winged hover (harpy), many necks (hydra), quadruped with a curled tail (manticore), coil and crest (basilisk).
- Rules (hit points, damage, which halls) live in engine.js `ENGINE.combat.CREATURES`.

## Sources

- Theoi Project, fantastic creatures (basilisk, manticore): https://theoi.com/greek-mythology/fantastic-creatures.html
- Wikipedia, List of Greek mythological creatures: https://en.wikipedia.org/wiki/List_of_Greek_mythological_creatures

## Rendering notes

- House style (25 Nov 2026, `research/rendering/house-style.md`): bodies from `ENGINE.skeleton` with anatomical proportions, painted as back-lit silhouettes with a cool rim and glowing eyes.
