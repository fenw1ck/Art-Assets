---
id: food
title: Food
kind: object
parent: items
aliases: [food item, produce, harvest, crops, vegetables, potato item, baked potato]
depth: outline
updated: 2026-11-25
gaps: [cooked versions of other produce, a cooking pot or fire as a station, what eating does]
used_by: [items.js potato, items.js produce; plants.js harvest]
---

# Food

## Parts

- **Consumable:** eaten once, then gone (as in farming sims such as Stardew Valley, where crops go to the inventory when harvested and some must be cooked).
- **Harvest:** pulling a mature plant removes it and puts what it gives in the inventory: its **fruit, root, flower or leaf** (`PLANTS.harvest`). Houseplants give nothing.
- **Must be cooked:** the potato (and eggplant, corn, beans, winter squash, asparagus, rhubarb) is raw when harvested and has to be cooked before it can be eaten.

## Kinds

- **Potato:** raw (`potato-red`, `potato-purple`, `potato-brown`, drawn by `PLANTS.tuber`) and baked (`potato-baked`: split jacket, fluffy inside, butter, steam). Research: subjects/plants/potato.md.
- **Produce:** `produce-<plant id>`, drawn from the plant's colours by the part: fruit (round, or long for corn, beans, peas, cucumber, squash, eggplant), root (taproot, or bulb for onion, garlic, beet, radish), flower, or a bundle of leaves.

## Log

- 2026-11-25: created with the potato.
