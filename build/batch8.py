import json
d = json.load(open("premodern_lands.json"))

# fetches gains selection/count; every card gains a global_effect key
for c in d:
    c.setdefault("global_effect", None)
    if c["fetches"] is not None:
        f = c["fetches"]
        c["fetches"] = {"source": f["source"], "selection": "one_of", "count": 1,
                        "land_types": f["land_types"], "basic_only": f["basic_only"],
                        "enters_tapped": f["enters_tapped"], "life_cost": f["life_cost"],
                        "shuffles": f["shuffles"], "returns_self_to_hand": f["returns_self_to_hand"]}
    for k in ["name","first_printing","supertypes","land_types","enters_tapped","entry_cost",
              "availability","total_activations","abilities","other_abilities","fetches",
              "global_effect","notes"]:
        c[k] = c.pop(k)

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
THRESH = {"type":"threshold","value":"seven or more cards in your graveyard"}
new = []

filt = [("Skycloud Expanse",["W","U"]),("Darkwater Catacombs",["U","B"]),("Shadowblood Ridge",["B","R"]),
        ("Mossfire Valley",["R","G"]),("Sungrass Prairie",["G","W"])]
for i,(n,cols) in enumerate(filt):
    note = ("The card that started this project. One ability, no colorless mode, and it costs a mana to use, so "
            "self_sufficient is false and this can never be your first colored source. Alone on the battlefield it "
            "produces nothing at all. What it does do is convert one generic mana into two colored, which is net plus "
            "one and genuinely good in a deck that already has a mana base, so it should not be written off either. "
            "produces is mode fixed with both symbols: you get {W} and {U} together, never a choice between them."
            if i == 0 else "See Skycloud Expanse. Same cycle.")
    new.append(card(n,"ODY",[],[],False,None,None,None,
        [ab(fixed(*cols),2,1,"{1}, {T}",False)],[],None,note))

sacany = [("Abandoned Outpost","W"),("Seafloor Debris","U"),("Bog Wreckage","B"),
          ("Ravaged Highlands","R"),("Timberland Ruins","G")]
for i,(n,col) in enumerate(sacany):
    note = ("Enters tapped, taps for its color, or cashes itself in for any single color. Both modes are free and "
            "self-sufficient, so the fixing here is real in a way the Odyssey filter cycle's is not, at the price of "
            "the land itself and a turn of tempo."
            if i == 0 else "See Abandoned Outpost. Same cycle.")
    new.append(card(n,"ODY",[],[],True,None,None,None,
        [ab(fixed(col),1,1,"{T}",True), ab(choice(*WUBRG),1,1,"{T}, Sacrifice",True,sac=True)],
        [],None,note))

thr = [("Nomad Stadium","W","{W}","You gain 4 life."),
       ("Cephalid Coliseum","U","{U}","Target player draws three cards, then discards three cards."),
       ("Cabal Pit","B","{B}","Target creature gets -2/-2 until end of turn."),
       ("Barbarian Ring","R","{R}","It deals 2 damage to any target."),
       ("Centaur Garden","G","{G}","Target creature gets +3/+3 until end of turn.")]
for i,(n,col,cost,eff) in enumerate(thr):
    note = ("No colorless mode, so unlike every painland cycle every single tap for mana costs you a life. Enters "
            "untapped and is otherwise unrestricted. The threshold ability sacrifices it and is gated on seven cards "
            "in your graveyard, which is a condition the mana base cannot supply on its own. Behaviourally this is the "
            "opposite of Wasteland despite both sacrificing themselves: Wasteland is cracked early and proactively, "
            "these are held all game and cashed in late, so a deck expects to use them as lands for many turns first."
            if i == 3 else "See Barbarian Ring. Same cycle.")
    new.append(card(n,"ODY",[],[],False,None,None,None,
        [ab(fixed(col),1,1,"{T}",True)],
        [oa("activated","%s, {T}, Sacrifice" % cost, eff + " Activate only if there are seven or more cards in your graveyard.", True)],
        None,note))

new.append(card("Crystal Quarry","ODY",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True),
     ab(fixed("W","U","B","R","G"),5,0,"{5}, {T}",False)],
    [],None,
    "The five-color mode is net zero: five mana in, five mana out, one of each color. It is a color converter, not acceleration, and it is not self-sufficient. Useful only in a deck that already produces five generic and needs all five colors in one turn, which is a narrow ask."))

new.append(card("Deserted Temple","ODY",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{1}, {T}","Untap target land.")],
    None,
    "Colorless source whose second ability can target itself, since the tap is paid as a cost before the ability resolves, so for one mana it can reset itself. More usefully it untaps a land that produces more than one mana, which is why it is played alongside Cabal Coffers and the storage lands rather than as a mana source in its own right."))

new.append(card("Petrified Field","ODY",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{T}, Sacrifice","Return target land card from your graveyard to your hand.",True)],
    None,
    "Colorless source that trades itself for a land in the graveyard, so it is roughly land-count neutral and card-count neutral, buying back whatever was killed or sacrificed earlier."))

new.append(card("Tarnished Citadel","ODY",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True),
     ab(choice(*WUBRG),1,1,"{T}",True)],
    [],None,
    "Painland structure with a five-color colored mode and a much steeper price: 3 damage per activation, part of the ability's effect rather than a cost, so it cannot be declined. The colorless mode is free. Untapped and unlimited, so as raw fixing it is excellent and the life total is the constraint."))

new.append(card("Cabal Coffers","TOR",[],[],False,None,None,None,
    [ab({"mode":"fixed_variable","unit":"B"},0,None,"{2}, {T}",False,
        var={"equals":"Swamps you control","accrual":None,"requires_untap_before_use":False})],
    [],None,
    "Not self-sufficient, which is the fact most likely to be missed: it costs {2} to activate, so it can never produce your first black mana and it is net negative until you control three Swamps. It counts Swamps by land type, so Snow-Covered Swamps count and Cabal Coffers itself does not. Amount is 0 by default because the floor is genuinely zero mana returned for two spent."))

tainted = [("Tainted Field",["W","B"]),("Tainted Isle",["U","B"]),
           ("Tainted Peak",["B","R"]),("Tainted Wood",["B","G"])]
for i,(n,cols) in enumerate(tainted):
    note = ("The colorless mode is free and unconditional; only the colored mode requires a Swamp, so the condition "
            "sits on that ability alone. It checks the Swamp land type, so Snow-Covered Swamp turns it on and this "
            "land does not count itself. In a deck with no Swamps at all it is simply a colorless land. Worth noting "
            "against Reflecting Pool: the Pool ignores activation conditions, so a Tainted Field with no Swamp in play "
            "still lets a Reflecting Pool produce white or black."
            if i == 0 else "See Tainted Field. Same cycle.")
    new.append(card(n,"TOR",[],[],False,None,None,None,
        [ab(fixed("C"),1,1,"{T}",True),
         ab(choice(*cols),1,1,"{T}",True,cond={"type":"controls_land_type","value":["Swamp"]})],
        [],None,note))

new.append(card("Krosan Verge","JUD",[],[],True,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{2}, {T}, Sacrifice","Search your library for a Forest card and a Plains card, put them onto the battlefield tapped, then shuffle.",True)],
    {"source":"library","selection":"one_each","count":2,"land_types":["Forest","Plains"],
     "basic_only":False,"enters_tapped":True,"life_cost":0,"shuffles":True,"returns_self_to_hand":False},
    "The first fetch in the file that gets two lands, and it gets one of each type rather than a choice, which is why the fetches object gained a selection key. Both arrive tapped and it costs {2} plus the land, so the turn you use it is heavily negative and the payoff is a land ahead plus fixed colors from the following turn. Searches by land type, not for basics, so it can find any Forest or Plains card."))

new.append(card("Nantuko Monastery","JUD",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{G}{W}","This land becomes a 4/4 green and white Insect Monk creature with first strike until end of turn. It's still a land. Activate only if there are seven or more cards in your graveyard.")],
    None,
    "Colorless source. Animation does not tap it, so mana and animation are compatible on the same turn, but it needs green and white from elsewhere and seven cards in the graveyard."))

new.append(card("Riftstone Portal","JUD",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("static_from_graveyard",None,"As long as this card is in your graveyard, lands you control have \"{T}: Add {G} or {W}.\"")],
    None,
    "Unique in this file and the one card here that cannot be evaluated in isolation. On the battlefield it is a colorless land. In the graveyard it grants every land you control the ability to tap for green or white, which means a deck's entire mana base changes color identity based on whether this card has been discarded or milled. Any calculator that sums per-card colors will be wrong about every other land in the deck while this sits in the graveyard, so global_effect is set to make it findable rather than leaving the fact buried in a note.",
    {"applies_to":"all lands you control","grants":"{T}: Add {G} or {W}","active_zone":"graveyard"}))

have={c["name"] for c in d}
assert not (have & {c["name"] for c in new})
d.extend(new)
json.dump(d, open("premodern_lands.json","w"), indent=2)
print("added",len(new),"total",len(d))
