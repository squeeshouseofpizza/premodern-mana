import json
d = json.load(open("premodern_lands.json"))

def ab(produces, amount, net, cost, ss, cond=None, sac=False, addl=None, var=None, avail=None):
    return {"produces": produces, "amount": amount, "net_mana": net, "cost": cost,
            "additional_cost": addl, "self_sufficient": ss, "condition": cond,
            "sacrifices_self": sac, "variable_amount": var, "availability": avail}
def oa(t, cost, effect, sac=False, avail=None):
    return {"type": t, "cost": cost, "effect": effect, "sacrifices_self": sac, "availability": avail}
def fixed(*m): return {"mode": "fixed", "mana": list(m)}
def choice(*o): return {"mode": "choice", "options": list(o)}
def card(name, fp, sup, lt, et, entry, avail, total, abils, others, fetches, notes, glob=None):
    return {"name": name, "first_printing": fp, "supertypes": sup, "land_types": lt,
            "enters_tapped": et, "entry_cost": entry, "availability": avail,
            "total_activations": total, "abilities": abils, "other_abilities": others,
            "fetches": fetches, "global_effect": glob, "notes": notes}
WUBRG = ["W","U","B","R","G"]
new = []

fetch = [("Bloodstained Mire",["Swamp","Mountain"]), ("Flooded Strand",["Plains","Island"]),
         ("Polluted Delta",["Island","Swamp"]), ("Windswept Heath",["Forest","Plains"]),
         ("Wooded Foothills",["Mountain","Forest"])]
for i,(n,types) in enumerate(fetch):
    note = ("Produces no mana itself, so abilities is empty and produces is null; its colors are a property of the "
            "decklist, since Premodern has no dual lands and these can only find what the deck actually plays. Three "
            "differences from the Mirage cycle, all of them in this one's favour. It enters untapped, so it can be "
            "played and cracked on the same turn. The land it finds arrives untapped. The price is 1 life. Searches by "
            "land type rather than for basics, so anything carrying the type is legal, which in this pool means the "
            "basics and the snow basics."
            if i == 0 else "See Bloodstained Mire. Same cycle.")
    new.append(card(n,"ONS",[],[],False,None,None,None,[],
        [oa("activated","{T}, Pay 1 life, Sacrifice",
            "Search your library for a %s or %s card, put it onto the battlefield, then shuffle." % tuple(types), True)],
        {"source":"library","selection":"one_of","count":1,"land_types":types,"basic_only":False,
         "enters_tapped":False,"life_cost":1,"shuffles":True,"returns_self_to_hand":False},
        note))

cyc = [("Barren Moor","B"),("Forgotten Cave","R"),("Lonely Sandbar","U"),
       ("Secluded Steppe","W"),("Tranquil Thicket","G")]
for i,(n,col) in enumerate(cyc):
    note = ("Same shape as the Urza's Saga cycling lands, with one difference: cycling costs a single mana of this "
            "land's own color rather than {2}. That makes it cheaper in the deck that wants it and unusable in a deck "
            "that cannot produce that color, which is a real constraint on a card whose whole point is flexibility. "
            "Enters tapped. Cycling is recorded as activated_from_hand and has no bearing on battlefield mana."
            if i == 0 else "See Barren Moor. Same cycle.")
    new.append(card(n,"ONS",[],[],True,None,None,None,
        [ab(fixed(col),1,1,"{T}",True)],
        [oa("activated_from_hand","{%s}" % col,"Discard this card: Draw a card.")],
        None,note))

util = [("Contested Cliffs","{R}{G}, {T}","Target Beast creature you control fights target creature an opponent controls."),
        ("Daru Encampment","{W}, {T}","Target Soldier creature gets +1/+1 until end of turn."),
        ("Goblin Burrows","{1}{R}, {T}","Target Goblin creature gets +2/+0 until end of turn."),
        ("Riptide Laboratory","{1}{U}, {T}","Return target Wizard you control to its owner's hand."),
        ("Unholy Grotto","{B}, {T}","Put target Zombie card from your graveyard on top of your library."),
        ("Wirewood Lodge","{G}, {T}","Untap target Elf.")]
for i,(n,cost,eff) in enumerate(util):
    note = ("Colorless source with a tribal ability that costs colored mana this land cannot produce, so it never "
            "pays for its own ability and any turn it is used it is a net drain. Records as a colorless source only; "
            "the color in the activation cost is a requirement, not production, and is exactly the sort of symbol a "
            "text scanner would wrongly count."
            if i == 0 else "See Contested Cliffs. Same pattern, different tribe.")
    new.append(card(n,"ONS",[],[],False,None,None,None,
        [ab(fixed("C"),1,1,"{T}",True)],[oa("activated",cost,eff)],None,note))

new.append(card("Seaside Haven","ONS",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{W}{U}, {T}, Sacrifice a Bird","Draw a card.")],
    None,
    "See Contested Cliffs. Colorless source; the ability needs white and blue from elsewhere and eats a Bird, not the land."))

new.append(card("Starlit Sanctum","ONS",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{W}, {T}, Sacrifice a Cleric creature","You gain life equal to the sacrificed creature's toughness."),
     oa("activated","{B}, {T}, Sacrifice a Cleric creature","Target player loses life equal to the sacrificed creature's power.")],
    None,
    "See Contested Cliffs. Two separate non-mana abilities in different colors; neither produces mana and both compete with the tap."))

new.append(card("Grand Coliseum","ONS",[],[],True,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True),
     ab(choice(*WUBRG),1,1,"{T}",True)],
    [],None,
    "City of Brass that enters tapped and has a free colorless mode. Two structural differences from City of Brass beyond the tapped entry: the damage here is part of the colored ability's effect rather than a trigger on becoming tapped, so tapping for colorless costs nothing and taps by opponents' effects cost nothing either. Never a turn-one source of anything."))

new.append(card("Temple of the False God","SCG",[],[],False,None,None,None,
    [ab(fixed("C","C"),2,2,"{T}",True,cond={"type":"controls_n_lands","value":5})],
    [],None,
    "Two colorless, and completely dead until you control five lands, itself included. Until then it is not a mana source at all, it is a blank that costs you a land drop, which is why the condition sits on the only ability rather than anywhere softer. Once live it is genuine acceleration with no cost and no limit. self_sufficient is true because activating it needs no mana; the constraint is the board, not the pool."))

have={c["name"] for c in d}
assert not (have & {c["name"] for c in new})
d.extend(new)
json.dump(d, open("premodern_lands.json","w"), indent=2)
print("added",len(new),"total",len(d))
