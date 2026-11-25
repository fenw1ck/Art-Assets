---
id: containers
title: Containers (chests, boxes, trunks)
kind: object
class: container
parent: none
aliases: [container, box, trunk, coffer, casket, strongbox]
depth: outline
updated: 2026-11-24
gaps: [barrels, baskets, jars and amphorae (likely their own class), drawers]
used_by: [containers.js]
traits: {}
---

# Containers

The root for made boxes with lids. Its traits vocabulary is `container` in `research/traits.yaml`.

## Parts

- **Carcass (the box):** front, back, two ends and a bottom.
- **Lid:** flat or domed. It is hinged at the back.
- **Construction types:**
  - **dug-out:** hollowed from one log;
  - **boarded (six-board):** front, back, two ends, lid and bottom nailed together;
  - **clamped:** boards set into thick corner posts;
  - **framed and panelled:** thin panels held in a frame.
- **Fittings (hardware):**
  - **hinges:** strap hinges run across the lid from the back edge;
  - **straps and bands** wrap the box and lid for strength;
  - **corner brackets** and **edge binding** protect the corners and edges;
  - **lock plate (escutcheon)** with keyhole on the front;
  - **hasp:** a hinged flap on the lid front that drops over a staple or into the lock;
  - **handles** on the ends: rings or bails;
  - **nails and rivets** along every strap.

## Construction order

1. The box as a block in the chosen view, with the light from the upper left: top lightest, front mid, side darkest.
2. Boards on each face, then grain.
3. The lid: closed, or rotated about the back edge.
4. Fittings: bands, edges, corners, hinges, lock and hasp, handles, rivets.
5. Wear and contact shadow last.

## States

- **closed**
- **open:** the lid swings up and back past upright (about 100–110°) and shows the lid's inner face, the inside walls and the contents.
- Possibly **broken** (lid off, boards split) and **locked vs unlocked** (the hasp down or up).

## Log

- 2026-11-24: created for the first brief (wooden chest, Euclid game).

## Sources

- Fine Woodworking, A short history of chests: https://www.finewoodworking.com/2005/09/12/a-short-history-of-chests
- The Medieval Chest (greydragon.org): https://www.greydragon.org/library/chests.html
- Pickvance, Pin-hinged clamped chests (Kent Academic Repository): https://kar.kent.ac.uk/id/document/3249394
- Kent Archaeological Society, A study of medieval iron-bound "domed standard" chests: https://www.kentarchaeology.org.uk/journal/136/study-medieval-iron-bound-chests-domed-standard-chests-kent
- Fine Woodworking, Pine blanket chest completion (strap hinges, half-mortise lock, escutcheon): https://www.finewoodworking.com/2012/02/06/pine-blanket-chest-completion
