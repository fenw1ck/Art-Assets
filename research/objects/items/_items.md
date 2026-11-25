---
id: items
title: Items
kind: object
parent: none
aliases: [item, inventory item, pickup, loot]
depth: outline
updated: 2026-11-25
gaps: [food and crafting ingredients, rarity tiers, item weights]
used_by: [items.js, euclid game.html (rooms, chests, the bag)]
---

# Items

Things the player can pick up, keep in the inventory (the bag), use, drop, sell and buy back. Everything here is drawn by `items.js`; each kind has its own entry below this one when it needs research.

## Parts (every item has)

- **Kind**, which says what it does: **tool** (reusable, never used up: the ax), **consumable** (used once, then gone: scrolls, potions, food), **clothing** (worn in a named slot: boots, cape, rings, hat, gloves, shirt, trousers; worn items don't take bag space), **treasure** (only for selling), **currency** (coins: a count, not a bag slot), **container** (a chest: holds coins and one item, and is itself an item you can carry and place).
- **Price** (its sales value). The shop buys at half price and sells at full price, and it sells back what you sold to it.
- **Room tags**: how likely it is in each room type (corridor, greenhouse, library, bedroom); 0 keeps it out of a room type.
- **Art**: a resting pose, drawn standing on the floor of a room, also used small as a bag icon.

## Distinguishing features

- Games sort items into types such as equipment for slots, consumables, currency and treasure; equipment goes in named slots (head, chest, hands…), and consumables are spent when used.

## Log

- 2026-11-25: created as the Items category for the Euclid game's inventory (with coin; chest is filed under containers and counts as an item).

## Sources

- Wikipedia, Item (game terminology): https://en.wikipedia.org/wiki/Item_(game_terminology)
- Heroic Labs, Inventory (stackable, consumable, equipment slot): https://heroiclabs.com/docs/hiro/concepts/inventory/
- gml-raptor wiki, Inventory types (slot inventories for equipment): https://github.com/Grisgram/gml-raptor/wiki/Inventory-Types
