---
id: traps
title: Traps
kind: object
parent: none
aliases: [trap, pressure plate, spikes, flame thrower, poison fog, path trap, euler path]
depth: outline
updated: 2026-11-25
gaps: [swinging blades, falling floor]
used_by: [traps.js; engine.js ENGINE.traps]
---

# Traps

## Parts

- **Pressure plate:** a slightly different floor slab with four rivets; pressed, it sinks and darkens. Bronze spikes thrust up around it.
- **Timed lock:** not drawn here; the lock's own timer (engine.js `locks`).
- **Path trap:** bronze studs (points) set in the floor joined by inlaid bronze lines (edges). Walked edges glow gold; going back over one turns it red and fires the room's trap: a lion-mouth nozzle in the wall shooting flame, spikes from the floor, or a cloud of green poison fog. The puzzle is an Euler trail: every edge once, none twice, a geometry problem the game's own subject (Euler's Königsberg bridges).
