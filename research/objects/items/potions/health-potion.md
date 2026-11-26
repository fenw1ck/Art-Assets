---
id: health-potion
title: Health potion
kind: object
parent: potions
aliases: [healing potion, health-minor, health-greater, health-supreme, red potion, caduceus potion]
depth: outline
updated: 2026-11-25
gaps: [a drinking animation, an empty-flask item]
used_by: [items.js health; euclid game.html (useItem: Drink; shop; rooms)]
---

# Health potion

## Distinguishing features

- **Red means healing.** Across games, potions that restore health are shown in red (Zelda's Red Potion, Diablo's healing potions), and players read the colour without being told. Strength is shown here by how deep the red is: rose, red, deep crimson that glows.
- **The caduceus stopper** (asked for in the ticket). A caduceus is Hermes' staff: **two** snakes twined round a rod in opposite directions, heads facing at the top, with a **pair of wings** above them. It is often used for medicine, though the strict medical symbol is the Rod of Asclepius (one snake, no wings). We draw the true caduceus because it was asked for and reads better small.
- **Three tiers**, named as Dungeons & Dragons names its healing potions (Healing, Greater, … Supreme). Each tier gets a different metal on the caduceus and more feathers in its wings, so the tiers differ in more than colour (helps colour-blind players):

| id | Name | Fluid | Caduceus | Wings (feathers each side) | Heals | Price |
|---|---|---|---|---|---|---|
| health-minor | Health Potion | rose #e58a8a | bronze | 2 | +25 | 10 |
| health-greater | Greater Health Potion | red #c8282e | silver | 3 | +50 | 22 |
| health-supreme | Supreme Health Potion | deep crimson #7e0b22, glowing | gold | 4 | full (+100) | 45 |

## Construction order

1. Glow (supreme only), then the sphere's fluid clipped to the circle, with a meniscus and a few bubbles.
2. The neck and the glass outline, then the cork.
3. The caduceus on the cork: rod, the two snakes (each a sine path crossing three times, dark edge then metal), heads, wings (an arm plus 2–4 primaries each side), the knob.
4. The highlight on the upper left of the sphere (light from the upper left, as for every item).

## States

- `o.level` 0–1: how full. Single use: drinking it uses it up.

## Log

- 2026-11-25: created for the Euclid game's health potions (ticket "Health Potions and harvestable food").

## Sources

- Caduceus as a symbol of medicine, Wikipedia: https://en.wikipedia.org/wiki/Caduceus_as_a_symbol_of_medicine
- Caduceus, Encyclopaedia Britannica: https://www.britannica.com/topic/caduceus
- The symbols of medicine, Science Museum Group blog: https://blog.sciencemuseumgroup.org.uk/the-symbols-of-medicine/
- Why are healing potions red and mana potions blue?, Mein-MMO: https://mein-mmo.de/en/why-are-healing-potions-red-and-mana-potions-blue,1242516
- Potions of Healing, D&D Beyond: https://www.dndbeyond.com/magic-items/4708-potions-of-healing
