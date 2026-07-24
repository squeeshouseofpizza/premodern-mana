import json
d = json.load(open("premodern_lands.json"))

for c in d:
    if c["name"] == "Rhystic Cave":
        c["notes"] = ("Five-colour fixing that any opponent can switch off for one mana, so it should not be counted as "
            "a reliable coloured source in any matchup where the opponent holds mana up. The Gatherer ruling of "
            "2004-10-04 says the card carries errata specifically so that it cannot be activated during the casting of "
            "a spell or the activation of an ability, which exists to stop an opponent paying {1} and leaving you short "
            "mid-cast. The practical consequence is that the mana has to be floated before you begin casting, never "
            "tapped in response to your own spell. An earlier revision of this note guessed at a stack-based "
            "explanation for that restriction; the ruling is the reason it changed.")

def ab(produces, amount, net, cost, ss, cond=None, sac=False, addl=None, var=None, avail=None):
    return {"produces": produces, "amount": amount, "net_mana": net, "cost": cost,
            "additional_cost": addl, "self_sufficient": ss, "condition": cond,
            "sacrifices_self": sac, "variable_amount": var, "availability": avail}
def oa(t, cost, effect, sac=False, avail=None):
    return {"type": t, "cost": cost, "effect": effect, "sacrifices_self": sac, "availability": avail}
def fixed(*m): return {"mode": "fixed", "mana": list(m)}
def choice(*o): return {"mode": "choice", "options": list(o)}
def card(name, fp, sup, lt, et, entry, avail, total, abils, others, fetches, notes):
    return {"name": name, "first_printing": fp, "supertypes": sup, "land_types": lt,
            "enters_tapped": et, "entry_cost": entry, "availability": avail,
            "total_activations": total, "abilities": abils, "other_abilities": others,
            "fetches": fetches, "notes": notes}
WUBRG = ["W","U","B","R","G"]
new = []

tap = [("Coastal Tower",["W","U"]),("Elfhame Palace",["G","W"]),("Salt Marsh",["U","B"]),
       ("Shivan Oasis",["R","G"]),("Urborg Volcano",["B","R"])]
for i,(n,cols) in enumerate(tap):
    note = ("The simplest shape in the format: enters tapped, taps for one of two colours, no cost, no limit, no "
            "condition. Worth recording precisely because it is the baseline every more complicated dual should be "
            "compared against. Never a turn-one source of either colour."
            if i == 0 else "See Coastal Tower. Same cycle.")
    new.append(card(n,"INV",[],[],True,None,None,None,[ab(choice(*cols),1,1,"{T}",True)],[],None,note))

sac = [("Ancient Spring","U",["W","B"]),("Geothermal Crevice","R",["B","G"]),
       ("Irrigation Ditch","W",["G","U"]),("Sulfur Vent","B",["U","R"]),("Tinder Farm","G",["R","W"])]
for i,(n,main,pair) in enumerate(sac):
    note = ("The colours of the two abilities do not overlap, which makes this cycle a genuine trap for anything "
            "reading mana symbols. Ancient Spring looks like a white-blue-black land. In play it is a blue land that "
            "can, exactly once, be cashed in for white and black instead. Note the sacrifice mode produces both "
            "symbols together, mode fixed, not a choice between them. Enters tapped, so nothing on turn one, and after "
            "the sacrifice you are down a land."
            if i == 0 else "See Ancient Spring. Same cycle, and the same non-overlap between the two abilities.")
    new.append(card(n,"INV",[],[],True,None,None,None,
        [ab(fixed(main),1,1,"{T}",True), ab(fixed(*pair),2,2,"{T}, Sacrifice",True,sac=True)],
        [],None,note))

new.append(card("Archaeological Dig","INV",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True), ab(choice(*WUBRG),1,1,"{T}, Sacrifice",True,sac=True)],
    [],None,
    "Untapped colourless land that can convert itself once into any single coloured mana. Unlike the Homelands and Masques filters the coloured mode is self-sufficient and nets a full mana, because the price is the land rather than mana. A calculator should count it as one coloured source of every colour, available once."))

new.append(card("Keldon Necropolis","INV",["Legendary"],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{4}{R}, {T}, Sacrifice a creature","Deals 2 damage to any target.")],
    None,
    "Colourless source. Legendary. The damage ability costs five mana plus a creature plus the tap, so it is a late-game mana sink and never competes with using this as a land."))

lair = [("Crosis's Catacombs",["U","B","R"]),("Darigaaz's Caldera",["B","R","G"]),
        ("Dromar's Cavern",["W","U","B"]),("Rith's Grove",["R","G","W"]),("Treva's Ruins",["G","W","U"])]
for i,(n,cols) in enumerate(lair):
    note = ("Two differences from the Visions Karoo cycle that a summary would flatten. These do not enter tapped, and "
            "the land you return does not have to be untapped, only a non-Lair land. Against that, they produce one "
            "mana of a choice of three rather than two mana, so they fix better and accelerate not at all. The cost is "
            "an entering trigger rather than a replacement effect, and failing to pay sacrifices the Lair. Returning a "
            "land costs you a future land drop rather than a card, so the deck is down tempo, not resources."
            if i == 0 else "See Crosis's Catacombs. Same cycle.")
    new.append(card(n,"PLS",[],["Lair"],False,
        {"action":"return_to_hand","count":1,"target":"non-Lair land","must_be_untapped":False,
         "timing":"etb_trigger","if_unmet":"sacrifice_self"},
        None,None,[ab(choice(*cols),1,1,"{T}",True)],[],None,note))

new.append(card("Forsaken City","PLS",[],[],False,None,None,None,
    [ab(choice(*WUBRG),1,1,"{T}",True,
        avail={"pattern":"requires_upkeep_payment",
               "reason":"Does not untap during your untap step. Untapping requires exiling a card from your hand at the beginning of your upkeep."})],
    [oa("static",None,"This land doesn't untap during your untap step."),
     oa("triggered",None,"At the beginning of your upkeep, you may exile a card from your hand. If you do, untap this land.")],
    None,
    "Free untapped any-colour mana on the turn it lands, and after that every single use costs a card exiled from hand. The first activation is genuinely free, which is why availability sits on the ability rather than the card and why enters_tapped is false. In a deck that empties its hand this stops untapping entirely and becomes a dead land, so the restriction is not a fixed rate like the depletion lands, it is contingent on a resource the mana base cannot supply."))

new.append(card("Meteor Crater","PLS",[],[],False,None,None,None,
    [ab({"mode":"derived","source":"a colour of a permanent you control"},1,1,"{T}",True,
        cond={"type":"controls_coloured_permanent"})],
    [],None,
    "Derived like Reflecting Pool but from a different pool of objects, and much weaker for it. It reads colours off permanents you control, and lands are almost always colourless, so with only lands on the battlefield this produces nothing at all. It cannot help you cast your first spell, only your second onwards, and only in a colour you already have on board. Note it looks at permanents, not lands, so an artifact or a coloured creature enables it."))

new.append(card("Terminal Moraine","PLS",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{2}, {T}, Sacrifice","Search your library for a basic land card, put that card onto the battlefield tapped, then shuffle.",True)],
    {"source":"library","land_types":None,"basic_only":True,"enters_tapped":True,"life_cost":0,
     "shuffles":True,"returns_self_to_hand":False},
    "A colourless land that can convert itself into any basic for two mana. Unlike the Mirage fetches it costs mana and the fetched land arrives tapped, so the turn you use it costs you three mana of tempo for a land that does nothing until next turn. Colours resolve against the decklist."))

pain = [("Battlefield Forge",["R","W"]),("Caves of Koilos",["W","B"]),("Llanowar Wastes",["B","G"]),
        ("Shivan Reef",["U","R"]),("Yavimaya Coast",["G","U"])]
for i,(n,cols) in enumerate(pain):
    note = ("Mechanically identical to the Ice Age painlands, and unlike the Tempest cycle these enter untapped. Free "
            "colourless mode with no damage, free coloured mode with 1 damage as part of that ability's effect rather "
            "than as a cost. Real turn-one sources of both colours. Together with the Ice Age five these are the "
            "backbone of two-colour mana in the format."
            if i == 0 else "See Battlefield Forge. Same cycle.")
    new.append(card(n,"APC",[],[],False,None,None,None,
        [ab(fixed("C"),1,1,"{T}",True), ab(choice(*cols),1,1,"{T}",True)],[],None,note))

have={c["name"] for c in d}
assert not (have & {c["name"] for c in new})
d.extend(new)
json.dump(d, open("premodern_lands.json","w"), indent=2)
print("added",len(new),"total",len(d))
