import json

d = json.load(open("premodern_lands.json"))

# --- migrate availability to the ability level where the ability causes it ---
MOVE = {"Land Cap","River Delta","Lava Tubes","Timberline Ridge","Veldt","Undiscovered Paradise"}
for c in d:
    for a in c["abilities"]:
        a.setdefault("availability", None)
    for o in c["other_abilities"]:
        o.setdefault("availability", None)
    if c["name"] in MOVE:
        c["abilities"][0]["availability"] = c["availability"]
        c["availability"] = None
    if c["name"] == "Thawing Glaciers":
        c["other_abilities"][0]["availability"] = c["availability"]
        c["availability"] = None

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

SKIP = {"pattern": "skips_next_untap",
        "reason": "Using this ability leaves the land tapped through your next untap step, so the colored mode is available every other turn."}

new = []

pain = [("Caldera Lake",["U","R"]), ("Pine Barrens",["B","G"]), ("Salt Flats",["W","B"]),
        ("Scabland",["R","W"]), ("Skyshroud Forest",["G","U"])]
for i,(n,cols) in enumerate(pain):
    note = ("Enters tapped and still deals damage, which makes this cycle strictly worse than the Ice Age painlands "
            "rather than a variant of them. Same two-ability structure: the colorless mode is free of damage and the "
            "colored mode is not, and the damage is part of that ability's effect rather than a cost, so it cannot be "
            "declined once the mode is chosen. The enters_tapped flag is the whole difference and it is the thing that "
            "keeps these out of decks that the Ice Age cycle is fine for."
            if i == 0 else "See Caldera Lake. Same cycle.")
    new.append(card(n,"TMP",[],[],True,None,None,None,
        [ab(fixed("C"),1,1,"{T}",True), ab(choice(*cols),1,1,"{T}",True)],
        [], None, note))

slow = [("Cinder Marsh",["B","R"]), ("Rootwater Depths",["U","B"]), ("Thalakos Lowlands",["W","U"]),
        ("Vec Townships",["G","W"]), ("Mogg Hollows",["R","G"])]
for i,(n,cols) in enumerate(slow):
    note = ("Enters untapped, and the colorless mode is completely unrestricted: tap it for {C} every turn forever with "
            "no penalty. Only the colored mode locks it through your next untap step, which is why availability sits on "
            "that ability rather than on the card. Rate works out the same as the Ice Age depletion cycle, usable for "
            "color on alternating turns, but the mechanism and the free colorless mode are different and a calculator "
            "that treats the two cycles as interchangeable will undercount this one."
            if i == 0 else "See Cinder Marsh. Same cycle.")
    new.append(card(n,"TMP",[],[],False,None,None,None,
        [ab(fixed("C"),1,1,"{T}",True), ab(choice(*cols),1,1,"{T}",True,avail=SKIP)],
        [], None, note))

new.append(card("Ancient Tomb","TMP",[],[],False,None,None,None,
    [ab(fixed("C","C"),2,2,"{T}",True)],
    [], None,
    "Two colorless per activation, not one. Amount is the whole point of this card and a classifier that records only color identity loses it entirely. The 2 damage is part of the ability's effect, not a cost, so it is unavoidable and applies on every activation. Untapped, unconditional, unlimited, so it is real turn-one acceleration and the life total is the only limit."))

new.append(card("Wasteland","TMP",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{T}, Sacrifice","Destroy target nonbasic land.",True)],
    None,
    "A colorless source until the moment it is not. The sacrifice is on a non-mana ability, so sacrifices_self is false on the mana ability and true on the other_abilities entry. Behaviourally this is cracked early and proactively, which is what separates it from a card like Barbarian Ring that also sacrifices itself but gets held for a late-game finish. Nothing in the schema encodes that intent; the difference lives in the note and in what the ability actually does."))

new.append(card("Reflecting Pool","TMP",[],[],False,None,None,None,
    [ab({"mode":"derived","source":"any mana type that a land you control could produce"},1,1,"{T}",True,
        cond={"type":"controls_other_land_producing_mana"})],
    [], None,
    "Colors resolve against the board, not the card, so produces gets its own mode rather than a list. Two consequences that matter. Alone on the battlefield it produces nothing at all, because it can only mirror what your lands could produce and it has nothing to mirror; a hand of Reflecting Pools makes zero mana. And it mirrors what a land could actually produce right now, so a Tainted Field with no Swamp out contributes nothing to it. In a deck built on the Odyssey filters or the Homelands castles this is much weaker than it looks, because those lands can only produce color with mana already available."))

new.append(card("Maze of Shadows","TMP",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{T}","Untap target attacking creature with shadow. Prevent all combat damage that would be dealt to and dealt by that creature this turn.")],
    None,
    "Colorless source. The shadow ability costs {T} and competes with the mana ability."))

new.append(card("Ghost Town","TMP",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{0}","Return this land to its owner's hand. Activate only if it's not your turn.")],
    None,
    "Colorless source with a free escape hatch from Wasteland and other targeted land removal, usable only on an opponent's turn. Bouncing it is not a mana cost but it does cost your next land drop to replay, and it cannot be used to reset itself on your own turn. Not modeled as an availability restriction because using the mana ability imposes nothing; the bounce is optional and independent."))

new.append(card("Stalking Stones","TMP",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{6}","Becomes a 3/3 Elemental artifact creature that's still a land. This effect lasts indefinitely.")],
    None,
    "Colorless source. Animation costs six but does not tap it and is permanent, so unlike the Urza's Legacy manlands it is a one-time investment rather than a per-turn cost. Still a land after animating, so it keeps producing mana."))

new.append(card("Volrath's Stronghold","STH",["Legendary"],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{1}{B}, {T}","Put target creature card from your graveyard on top of your library.")],
    None,
    "Colorless source. Legendary, so a second copy is dead. The recursion ability costs {T} plus two mana, so a turn spent using it is a turn this land is a net drain rather than a source."))

new.append(card("City of Traitors","EXO",[],[],False,None,None,None,
    [ab(fixed("C","C"),2,2,"{T}",True)],
    [oa("triggered",None,"When you play another land, sacrifice this land.",True)],
    None,
    "Two colorless with no damage, and the price is that your next land drop kills it. total_activations is null rather than 1 because the count is not fixed: hold your land drops and it keeps producing indefinitely. In practice a deck plays it, uses it, and loses it on the following turn, so a calculator modeling turn-by-turn mana should treat the acceleration as borrowed rather than permanent. Only lands you play trigger it, so opponents cannot force it off and lands put onto the battlefield by effects rather than played do not trigger it either."))

have = {c["name"] for c in d}
assert not (have & {c["name"] for c in new})
d.extend(new)
json.dump(d, open("premodern_lands.json","w"), indent=2)
print("added", len(new), "total", len(d))
