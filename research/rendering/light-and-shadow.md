---
id: light-and-shadow
title: Light and shadow
kind: technique
parent: none
aliases: [shading, form shadow, cast shadow, core shadow, terminator, occlusion]
depth: standard
updated: 2026-11-24
gaps: [several light sources (torches, lamps), night scenes, translucency (leaves, marble)]
used_by: [plants.js ell, leaf, trunk, shadow]
---

# Light and shadow

## Parts

Every lit form has the same parts, from light to dark:

- **Highlight:** the reflection of the light source. Small and bright on shiny things; faint or absent on matte ones.
- **Light, then halftone:** the lit side, darkening as the surface turns away.
- **Terminator:** where light turns to shadow. Soft on round forms, hard on sharp edges.
- **Core shadow:** the darkest band of the shadow side, just past the terminator.
- **Reflected (bounced) light:** a lighter band on the shadow side from light bouncing off nearby surfaces. It is always darker than the lit side.
- **Occlusion shadow:** the darkest dark, in creases and where things touch.
- **Cast shadow:** the shadow the form throws onto other surfaces. It is sharp next to the object and softer farther away.

## Construction order

1. Pick the light direction. The house default is upper left.
2. Separate light and shadow shapes first, as two values.
3. Add halftones, then the core shadow, reflected light and occlusion.
4. Highlights last.

Five values are enough: three in the light, two in the shadow. Keep the lights and the shadows separate.

## Log

- 2026-11-24: created.

## Sources

- Proko, Elements of light and shadow: https://www.proko.com/course-lesson/elements-of-light-and-shadow/notes
- Sessions College, Looking at light: the anatomy of a shadow: https://www.sessions.edu/notes-on-design/looking-at-light-the-anatomy-of-a-shadow/
- Muddy Colors, light and shadow terms: https://www.muddycolors.com/?p=66610
- AWN, Vilppu, Getting a handle on direct lighting: https://www.awn.com/mag/issue4.11/4.11pages/4.11vilppu2.php3
