import json
d = json.load(open("premodern_lands.json"))

# --- correction: Reflecting Pool note was wrong about costs/conditions -------
for c in d:
    if c["name"] == "Reflecting Pool":
        c["notes"] = ("Colours resolve against the board, not the card, so produces gets its own mode rather than a "
            "list. Per the Gatherer rulings the ability checks the effects of your other lands' mana abilities but "
            "not their costs, their activation conditions, or whether they are untapped: a Homelands castle you "
            "cannot afford to activate still feeds it, as does a tapped land. Mana types include colourless, so a "
            "land that could add {C} lets this add {C}. What it cannot do is bootstrap. If every other land you "
            "control either lacks a mana ability or is another Reflecting Pool, you may activate it and it produces "
            "nothing, so a hand of Reflecting Pools makes zero mana. An earlier revision of this note claimed the "
            "opposite about conditional lands; it was wrong and the rulings are the reason it changed.")
# --- fetches gains a source key ---------------------------------------------
for c in d:
    if c["fetches"] is not None:
        c["fetches"] = {"source": "library", **c["fetches"]}

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

dep = [("Peat Bog","B"),("Hickory Woodlot","G"),("Remote Farm","W"),
       ("Sandstone Needle","R"),("Saprazzan Skerry","U")]
for i,(n,col) in enumerate(dep):
    note = ("Two activations total, then it sacrifices itself, so total_activations is 2 and the lifetime output is "
            "four mana. Enters tapped, so nothing on the turn it lands. This is the cycle most likely to be misread as "
            "a normal dual-producing land: it taps for two of its colour, which looks like acceleration, but it is a "
            "four-mana card that occupies a land slot and then disappears. Contrast the Fallen Empires storage lands, "
            "which are also slow but never run out."
            if i == 0 else "See Peat Bog. Same cycle.")
    new.append(card(n,"MMQ",[],[],True,None,None,2,
        [ab(fixed(col,col),2,2,"{T}, Remove a depletion counter",True,sac=True)],
        [], None, note))

sto = [("Fountain of Cho","W"),("Mercadian Bazaar","R"),("Rushwood Grove","G"),
       ("Saprazzan Cove","U"),("Subterranean Hangar","B")]
for i,(n,col) in enumerate(sto):
    note = ("Storage, but mechanically different from the Fallen Empires cycle and better. Charging is an activated "
            "ability that taps the land, so it untaps normally every turn and you simply choose each turn whether to "
            "charge or to cash out. The Fallen Empires version instead required you to decline your untap step and "
            "only charged at upkeep. Same broad shape, one counter per turn invested, but this one is easier to use "
            "and never locks you out of the land. Enters tapped, and amount is 0 by default because with no counters "
            "it produces nothing."
            if i == 0 else "See Fountain of Cho. Same cycle.")
    new.append(card(n,"MMQ",[],[],True,None,None,None,
        [ab({"mode":"fixed_variable","unit":col},0,None,"{T}, Remove any number of storage counters",True,
            var={"equals":"storage counters removed",
                 "accrual":"one counter per activation of the charge ability, which taps this land",
                 "requires_untap_before_use":False})],
        [oa("activated","{T}","Put a storage counter on this land.")],
        None, note))

new.append(card("Dust Bowl","MMQ",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{3}, {T}, Sacrifice a land","Destroy target nonbasic land.",False,
        {"pattern":"consumes_a_land_per_use","reason":"Each activation eats a land from your board, which may be this one."})],
    None,
    "Colourless source with repeatable land destruction. The sacrifice is a land, not necessarily this one, so sacrifices_self is false; you can feed it another land and keep Dust Bowl. Each use costs three mana plus a land plus this land's tap, so a turn spent activating it is deeply negative on mana."))

new.append(card("High Market","MMQ",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{T}, Sacrifice a creature","You gain 1 life.")],
    None,
    "Colourless source. The sacrifice outlet costs {T} and competes with the mana ability, and it eats a creature rather than the land."))

new.append(card("Rishadan Port","MMQ",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{1}, {T}","Tap target land.")],
    None,
    "Colourless source. Any turn it is used to tap a land it is a net drain of one and produces nothing itself, which is the whole tension in playing it: it is either your mana or their mana, never both."))

new.append(card("Tower of the Magistrate","MMQ",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{1}, {T}","Target creature gains protection from artifacts until end of turn.")],
    None,
    "Colourless source with a non-mana ability that competes for the tap."))

new.append(card("Henge of Ramos","MMQ",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True),
     ab(choice(*WUBRG),1,-1,"{2}, {T}",False)],
    [], None,
    "Same trap as School of the Unseen and the Homelands castles. Reads as five-colour fixing; the coloured mode nets minus one and is not self-sufficient, so it can never produce your first coloured mana."))

new.append(card("Kor Haven","NEM",["Legendary"],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{1}{W}, {T}","Prevent all combat damage that would be dealt by target attacking creature this turn.")],
    None,
    "Colourless source. Legendary. The prevention ability needs white from elsewhere and taps the land, so it is never both mana and defence on the same turn."))

new.append(card("Rath's Edge","NEM",["Legendary"],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{4}, {T}, Sacrifice a land","Deals 1 damage to any target.",False,
        {"pattern":"consumes_a_land_per_use","reason":"Each activation eats a land, which may be this one."})],
    None,
    "See Dust Bowl for the sacrifice-a-land shape. Legendary."))

new.append(card("Terrain Generator","NEM",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{2}, {T}","You may put a basic land card from your hand onto the battlefield tapped.")],
    {"source":"hand","land_types":None,"basic_only":True,"enters_tapped":True,"life_cost":0,
     "shuffles":False,"returns_self_to_hand":False},
    "The fetches object gained a source key for this card. It is not a library search: it puts a basic from your hand onto the battlefield, so it does not thin the deck, does not shuffle, and does nothing if your hand has no basics. It also does not use your land drop, which is the actual reason to play it. Costs two mana plus the tap, and the land arrives tapped, so the turn you use it is a net minus three."))

new.append(card("Rhystic Cave","PCY",[],[],False,None,None,None,
    [ab(choice(*WUBRG),1,1,"{T}",True,
        cond={"type":"opponent_may_prevent","cost_to_prevent":"{1}","who":"any player"})],
    [], None,
    "Five-colour fixing that an opponent can switch off for one mana, so a calculator should not count it as a reliable coloured source in any matchup where the opponent holds mana up. Flagged: the printed line 'Activate only as an instant' and the unless-any-player-pays clause together suggest the ability uses the stack rather than being an ordinary mana ability, which would mean it cannot be activated while paying for a spell and must be floated in advance. I have not verified that against the rulings and the note should not be trusted on it until someone does."))

new.append(card("Wintermoon Mesa","PCY",[],[],True,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{2}, {T}, Sacrifice","Tap two target lands.",True)],
    None,
    "Enters tapped, taps for colourless, and the ability sacrifices it, so it is a land that converts itself into a one-shot double Rishadan Port activation for two mana."))

have={c["name"] for c in d}
assert not (have & {c["name"] for c in new})
d.extend(new)
json.dump(d, open("premodern_lands.json","w"), indent=2)
print("added",len(new),"total",len(d))
