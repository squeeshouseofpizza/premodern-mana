import json
d = json.load(open("premodern_lands.json"))

def in_scope(c):
    return (c["fetches"] is not None
            or any(a["variable_amount"] for a in c["abilities"])
            or any(a["produces"]["mode"] == "derived" for a in c["abilities"]))

scope = [c["name"] for c in d if in_scope(c)]

H = {
 "Gaea's Cradle": (2, "green", "Typical creature count on the turns a deck that plays it wants to untap with it. Zero in the opening turns and in any draw where the board has been swept."),
 "Serra's Sanctum": (2, "white", "Typical enchantment count once an Enchantress-style deck is running. Zero before the first enchantment resolves."),
 "Reflecting Pool": (1, "union of the colors of the other lands in the decklist", "One mana, and color identity borrowed from the rest of the mana base. Produces nothing if it is the only mana-producing land you control."),
 "Icatian Store": (1, "white", "Charging costs a turn each, so treat as one mana per turn invested rather than a source you can tap on demand."),
 "Sand Silos": (1, "blue", "See Icatian Store."),
 "Bottomless Vault": (1, "black", "See Icatian Store."),
 "Dwarven Hold": (1, "red", "See Icatian Store."),
 "Hollow Trees": (1, "green", "See Icatian Store."),
 "Fountain of Cho": (1, "white", "One mana per turn invested. Easier to use than the Fallen Empires cycle because it untaps normally."),
 "Mercadian Bazaar": (1, "red", "See Fountain of Cho."),
 "Rushwood Grove": (1, "green", "See Fountain of Cho."),
 "Saprazzan Cove": (1, "blue", "See Fountain of Cho."),
 "Subterranean Hangar": (1, "black", "See Fountain of Cho."),
 "Bad River": (1, "colors of the Island and Swamp cards in the decklist", "Counts as a source of whatever it can actually find in this deck. Zero for a color with no fetchable land."),
 "Flood Plain": (1, "colors of the Plains and Island cards in the decklist", "See Bad River."),
 "Grasslands": (1, "colors of the Forest and Plains cards in the decklist", "See Bad River."),
 "Mountain Valley": (1, "colors of the Mountain and Forest cards in the decklist", "See Bad River."),
 "Rocky Tar Pit": (1, "colors of the Swamp and Mountain cards in the decklist", "See Bad River."),
 "Thawing Glaciers": (0, "none directly", "Produces no mana itself and costs one per activation. Its value is land count over a long game, not mana on any given turn, and it consumes your land drop every turn it is replayed."),
 "Terrain Generator": (1, "colorless", "Count only its own colorless mana. The basic it deploys should be counted as that basic, not as extra output from this card."),
 "Meteor Crater": (1, "colors of your own non-land permanents once a board exists", "Zero with only lands on the battlefield, since lands are colorless. Cannot cast your first spell, only later ones in a color you already have out."),
 "Terminal Moraine": (1, "colorless", "Count only its own colorless mana. The basic it fetches should be counted as that basic, not as extra output from this card."),
 "Cabal Coffers": (3, "black", "Typical Swamp count when a deck that plays it wants to activate. Costs {2} to use, so it is net positive only past two Swamps and produces nothing on its own."),
 "Krosan Verge": (2, "green and white", "Counts as a source of both, delayed. Both lands arrive tapped and the activation costs {2} plus the land itself."),
 "Bloodstained Mire": (1, "colors of the Swamp and Mountain cards in the decklist", "Counts as a source of whatever it can actually find in this deck. Zero for a color with no fetchable land. Costs 1 life and can be cracked the turn it is played."),
 "Flooded Strand": (1, "colors of the Plains and Island cards in the decklist", "See Bloodstained Mire."),
 "Polluted Delta": (1, "colors of the Island and Swamp cards in the decklist", "See Bloodstained Mire."),
 "Windswept Heath": (1, "colors of the Forest and Plains cards in the decklist", "See Bloodstained Mire."),
 "Wooded Foothills": (1, "colors of the Mountain and Forest cards in the decklist", "See Bloodstained Mire."),
}

missing = [n for n in scope if n not in H]
extra = [n for n in H if n not in scope]
assert not missing and not extra, (missing, extra)

out = {
  "meta": {
    "status": "opinion, not verified fact",
    "purpose": "Deck-profile defaults for lands whose real output cannot be read off the card. Layered on top of premodern_lands.json by the calculator; never merged into it.",
    "scope_rule": "Any card in premodern_lands.json with a non-null fetches object, any ability with a non-null variable_amount, or any ability whose produces.mode is 'derived'.",
    "warning": "Every number here is a judgement call about typical decks and should be argued with. premodern_lands.json contains only what the card and the rulings say; this file contains what we think it is worth. If the two ever disagree, the data file is right and this one is wrong.",
    "generated_against_card_count": len(d)
  },
  "entries": [
    {"name": n, "assumed_amount": H[n][0], "assumed_colors": H[n][1], "floor": 0,
     "confidence": "opinion", "basis": H[n][2]}
    for n in scope
  ]
}
json.dump(out, open("premodern_lands_heuristics.json","w"), indent=2)
print("heuristics entries:", len(out["entries"]))
