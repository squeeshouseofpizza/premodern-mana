import json

def ab(produces, amount, net, cost, ss, cond=None, sac=False, addl=None, var=None):
    return {"produces": produces, "amount": amount, "net_mana": net, "cost": cost,
            "additional_cost": addl, "self_sufficient": ss, "condition": cond,
            "sacrifices_self": sac, "variable_amount": var}

def fixed(*m): return {"mode": "fixed", "mana": list(m)}
def choice(*o): return {"mode": "choice", "options": list(o)}
WUBRG = ["W","U","B","R","G"]

def card(name, fp, sup, lt, et, entry, avail, total, abils, others, fetches, notes):
    return {"name": name, "first_printing": fp, "supertypes": sup, "land_types": lt,
            "enters_tapped": et, "entry_cost": entry, "availability": avail,
            "total_activations": total, "abilities": abils, "other_abilities": others,
            "fetches": fetches, "notes": notes}

def oa(t, cost, effect, sac=False):
    return {"type": t, "cost": cost, "effect": effect, "sacrifices_self": sac}

def entry(action, count, target, untapped, timing, if_unmet):
    return {"action": action, "count": count, "target": target,
            "must_be_untapped": untapped, "timing": timing, "if_unmet": if_unmet}

new = []

# --- Alliances "sacrifice a land to play it" cycle -------------------------
new.append(card("Balduvian Trading Post","ALL",[],[],False,
    entry("sacrifice",1,"Mountain",True,"replacement","graveyard"),None,None,
    [ab(fixed("C","R"),2,2,"{T}",True)],
    [oa("activated","{1}, {T}","Deals 1 damage to target attacking creature.")],
    None,
    "Produces both mana every time, not a choice between them. This is the distinction the produces object exists for: {C}{R} is mode fixed with two symbols, while a painland's {W} or {U} is mode choice with one. Entry cost is a replacement effect, so it is paid before the land is ever on the battlefield and there is no window where you control it without having paid. If you cannot pay it never enters and goes to the graveyard, which costs you the land drop and the card. Net land count is unchanged, but you convert a Mountain into two mana a turn. The Mountain must be untapped, which is not true of every member of this cycle."))

new.append(card("Soldevi Excavations","ALL",[],[],False,
    entry("sacrifice",1,"Island",True,"replacement","graveyard"),None,None,
    [ab(fixed("C","U"),2,2,"{T}",True)],
    [oa("activated","{1}, {T}","Scry 1.")],
    None,
    "See Balduvian Trading Post. Same shape, blue, and the Island must also be untapped."))

new.append(card("Heart of Yavimaya","ALL",[],[],False,
    entry("sacrifice",1,"Forest",False,"replacement","graveyard"),None,None,
    [ab(fixed("G"),1,1,"{T}",True)],
    [oa("activated","{T}","Target creature gets +1/+1 until end of turn.")],
    None,
    "Only one mana, unlike the Balduvian and Soldevi members of this cycle, so the Forest you eat is a straight downgrade in mana terms and you are paying for the pump ability. The Forest does not have to be untapped here, which is a real difference from Balduvian Trading Post and Soldevi Excavations and is easy to flatten if you read the cycle as uniform. The pump ability costs {T} and competes with the mana ability."))

new.append(card("Kjeldoran Outpost","ALL",[],[],False,
    entry("sacrifice",1,"Plains",False,"replacement","graveyard"),None,None,
    [ab(fixed("W"),1,1,"{T}",True)],
    [oa("activated","{1}{W}, {T}","Create a 1/1 white Soldier creature token.")],
    None,
    "See Heart of Yavimaya. One mana, Plains need not be untapped. The token ability costs {T} plus two mana, so on any turn you make a Soldier this land is a net drain of two, not a source."))

new.append(card("Lake of the Dead","ALL",[],[],False,
    entry("sacrifice",1,"Swamp",False,"replacement","graveyard"),None,None,
    [ab(fixed("B"),1,1,"{T}",True),
     ab(fixed("B","B","B","B"),4,4,"{T}, Sacrifice a Swamp",True,
        addl={"action":"sacrifice","count":1,"target":"Swamp"})],
    [], None,
    "The big ability sacrifices a Swamp, not itself, so sacrifices_self is false and additional_cost carries the real price. Lake of the Dead survives; your Swamp does not. It is repeatable as long as you keep feeding it Swamps, which is why it is not modeled as a one-shot. Entry cost eats a Swamp too, so getting to the four-mana turn costs two Swamps in total. Net mana on the turn you fire it is plus four, but land count drops by one each time and the file does not model that decay anywhere except here."))

new.append(card("School of the Unseen","ALL",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True),
     ab(choice(*WUBRG),1,-1,"{2}, {T}",False)],
    [], None,
    "Same family as the Homelands castles. Reads as a five-color source and is not one: the colored mode nets minus one and is not self-sufficient, so it can never be your first colored mana and never accelerates you. It is a colorless land with an expensive late-game fixing button."))

new.append(card("Sheltered Valley","ALL",[],[],False,
    entry("sacrifice","all others","Sheltered Valley",False,"replacement",None),None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("triggered",None,"At the beginning of your upkeep, if you control three or fewer lands, you gain 1 life.")],
    None,
    "The entry replacement is not a cost you can fail to pay, it is self-culling: playing a second copy sacrifices the first. Four copies in a deck are still at most one on the battlefield at any time. Any calculator that counts copies in a decklist as independent mana sources will overcount this card specifically, which is why entry_cost is populated even though nothing can go wrong when it enters."))

new.append(card("Thawing Glaciers","ALL",[],[],True,None,
    {"pattern":"consumes_land_drop_each_turn",
     "reason":"Returns itself to hand at the next cleanup, so replaying it uses your land drop every turn."},
    None,[],
    [oa("activated","{1}, {T}","Search your library for a basic land card, put it onto the battlefield tapped, then shuffle. Return this land to its owner's hand at the beginning of the next cleanup step.",False)],
    {"land_types": None, "basic_only": True, "enters_tapped": True, "life_cost": 0,
     "shuffles": True, "returns_self_to_hand": True},
    "Produces no mana itself, so abilities is empty. Three costs a naive reading misses. It enters tapped, so it cannot fetch the turn it lands. The fetched land arrives tapped, so it gives no mana that turn either. And it bounces itself every turn, which means replaying it consumes your land drop, so the engine only nets you a land per turn if you would otherwise have had nothing to play. Fetches any basic, so its colors resolve against the decklist, not the card."))

# --- Mirage fetchlands -----------------------------------------------------
mir = [("Bad River",["Island","Swamp"]), ("Flood Plain",["Plains","Island"]),
       ("Grasslands",["Forest","Plains"]), ("Mountain Valley",["Mountain","Forest"]),
       ("Rocky Tar Pit",["Swamp","Mountain"])]
for i,(n,types) in enumerate(mir):
    note = ("Produces no mana of its own, so abilities is empty and produces is null. Its colors are a property of "
            "the decklist, not the card: it finds any card with the listed land types, which in this pool means the "
            "basics and the snow basics. Note basic_only is false because the printed text says card, not basic card, "
            "so anything that ever gains one of these types is a legal target. Two timing costs that separate this "
            "cycle from the Onslaught fetches: it enters tapped, and cracking it costs {T}, so it cannot be played and "
            "cracked on the same turn. The land it finds arrives untapped, which the Onslaught cycle does not, and it "
            "costs no life."
            if i == 0 else "See Bad River. Same cycle.")
    new.append(card(n,"MIR",[],[],True,None,None,None,[],
        [oa("activated","{T}, Sacrifice",
            "Search your library for a %s or %s card, put it onto the battlefield, then shuffle." % tuple(types), True)],
        {"land_types": types, "basic_only": False, "enters_tapped": False, "life_cost": 0,
         "shuffles": True, "returns_self_to_hand": False},
        note))

new.append(card("Crystal Vein","MIR",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True),
     ab(fixed("C","C"),2,2,"{T}, Sacrifice",True,sac=True)],
    [], None,
    "The card that motivated the abilities array. One object, two genuinely different modes: a normal colorless land, or two colorless once. A single amount_per_activation and a single sacrifices_self cannot hold both without lying about one of them."))

new.append(card("Teferi's Isle","MIR",["Legendary"],[],True,None,
    {"pattern":"every_other_turn",
     "reason":"Phasing. It phases out before your untap step on alternating turns, so it is absent for a whole turn cycle at a time."},
    None,
    [ab(fixed("U","U"),2,2,"{T}",True)],
    [oa("static",None,"Phasing.")],
    None,
    "Two blue for one tap is real acceleration, and the drawbacks are all in timing. It enters tapped, so nothing on turn one. Phasing then takes it away on alternating turns: it phases out before your next untap step, so it does not untap that turn either, and it is usable again the turn after. Reasoning it through, the first turn you can actually tap it is two turns after you play it, and every other turn from there. Legendary, so a second copy is dead. Flagged as the timing I would most like a second pair of eyes on."))

# --- Visions Karoo cycle ---------------------------------------------------
karoo = [("Coral Atoll","Island","U"), ("Dormant Volcano","Mountain","R"),
         ("Everglades","Swamp","B"), ("Jungle Basin","Forest","G"), ("Karoo","Plains","W")]
for i,(n,basic,col) in enumerate(karoo):
    note = ("Looks like the Alliances cycle and behaves differently in two ways that matter. The cost is a triggered "
            "ability on entering rather than a replacement effect, so the land is briefly on the battlefield and can be "
            "responded to. And you return the basic to hand rather than sacrificing it, so the land is not lost, only "
            "delayed, and it costs you a land drop later instead of a card. If you cannot or will not pay, this land "
            "sacrifices itself. It enters tapped and taps for two, so across its first two turns it is even with a "
            "basic, and ahead only from the third turn on."
            if i == 0 else "See Coral Atoll. Same cycle.")
    new.append(card(n,"VIS",[],[],True,
        entry("return_to_hand",1,basic,True,"etb_trigger","sacrifice_self"),None,None,
        [ab(fixed("C",col),2,2,"{T}",True)],
        [], None, note))

new.append(card("Griffin Canyon","VIS",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{T}","Untap target Griffin. If it's a creature, it gets +1/+1 until end of turn.")],
    None,
    "Plain colorless land for mana purposes. The Griffin ability costs {T} and competes with the mana ability."))

new.append(card("Quicksand","VIS",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{T}, Sacrifice","Target attacking creature without flying gets -1/-2 until end of turn.",True)],
    None,
    "Colorless source that doubles as removal. The sacrifice is on a non-mana ability, which is why other_abilities carries its own sacrifices_self: a deck expecting to use Quicksand as removal should not count it as a land for the rest of the game."))

new.append(card("Undiscovered Paradise","VIS",[],[],False,None,
    {"pattern":"one_activation_per_land_drop",
     "reason":"Instead of untapping it returns to your hand during your next untap step, so each use costs a land drop to replay."},
    None,
    [ab(choice(*WUBRG),1,1,"{T}",True)],
    [oa("triggered",None,"During your next untap step, as you untap your permanents, return this land to its owner's hand.")],
    None,
    "Enters untapped and taps for any color immediately, so unlike most fixing in this era it is a genuine turn-one colored source. The price is that it never untaps; it bounces instead. It is one mana per land drop, so in a deck that wants to develop its mana base every turn it is not free fixing, it is a tax on growth. It can still be tapped during an opponent's turn before it returns."))

# --- Weatherlight ----------------------------------------------------------
new.append(card("Gemstone Mine","WTH",[],[],False,None,None,3,
    [ab(choice(*WUBRG),1,1,"{T}, Remove a mining counter",True,sac=True)],
    [], None,
    "Three activations total, then it sacrifices itself. total_activations is 3 and it is the field that matters more than anything else on this card: treated as an unlimited five-color source it is one of the best lands in the format, and treated correctly it is three mana spread across a game. The sacrifice happens after the third use, when the last counter is gone, so you do get all three. sacrifices_self is true on the ability because using it is what eventually kills it."))

new.append(card("Lotus Vale","WTH",[],[],False,
    entry("sacrifice",2,"land",True,"replacement","graveyard"),None,None,
    [ab({"mode":"choice_uniform","options":WUBRG,"count":3},3,3,"{T}",True)],
    [], None,
    "Three mana of any one color, all the same color, which is why produces needs the choice_uniform mode rather than choice: you do not get to spread it across three colors. Entry cost is two untapped lands, and it is a replacement effect, so if you cannot pay it goes straight to the graveyard and you have lost the card and your land drop for nothing. Board arithmetic: two lands and a land drop become one land. Mana per turn is roughly break even, card economy is not, and the whole thing dies to one Wasteland."))

new.append(card("Scorched Ruins","WTH",[],[],False,
    entry("sacrifice",2,"land",True,"replacement","graveyard"),None,None,
    [ab(fixed("C","C","C","C"),4,4,"{T}",True)],
    [], None,
    "See Lotus Vale for the entry cost. Four colorless from one land is the largest single activation in the pool so far, and it is colorless, so it accelerates but never fixes."))

new.append(card("Winding Canyons","WTH",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{2}, {T}","You may cast creature spells this turn as though they had flash.")],
    None,
    "Colorless source. The flash ability costs {T} plus two, so any turn it is used this land is a net drain of two rather than a source."))

d = json.load(open("premodern_lands.json"))
have = {c["name"] for c in d}
assert not (have & {c["name"] for c in new}), "duplicate"
d.extend(new)
json.dump(d, open("premodern_lands.json","w"), indent=2)
print("added", len(new), "total", len(d))
