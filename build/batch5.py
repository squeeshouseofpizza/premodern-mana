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
def var(eq): return {"equals": eq, "accrual": None, "requires_untap_before_use": False}
def card(name, fp, sup, lt, et, entry, avail, total, abils, others, fetches, notes):
    return {"name": name, "first_printing": fp, "supertypes": sup, "land_types": lt,
            "enters_tapped": et, "entry_cost": entry, "availability": avail,
            "total_activations": total, "abilities": abils, "other_abilities": others,
            "fetches": fetches, "notes": notes}
CYCLE = oa("activated_from_hand","{2}","Discard this card: Draw a card.")
WUBRG = ["W","U","B","R","G"]
new = []

cyc = [("Drifting Meadow","W"),("Remote Isle","U"),("Polluted Mire","B"),
       ("Smoldering Crater","R"),("Slippery Karst","G")]
for i,(n,col) in enumerate(cyc):
    note = ("Enters tapped, produces one mana of its colour, and carries an ability that is only usable from hand. "
            "Cycling is recorded with type activated_from_hand because it has no bearing on mana once the card is on "
            "the battlefield; what it changes is the decision to play the land at all. A calculator counting coloured "
            "sources in a decklist should count this at full weight, but a calculator modelling opening hands should "
            "know the card has a second use as a cantrip and will sometimes never be a land."
            if i == 0 else "See Drifting Meadow. Same cycle.")
    new.append(card(n,"USG",[],[],True,None,None,None,[ab(fixed(col),1,1,"{T}",True)],[CYCLE],None,note))

new.append(card("Blasted Landscape","USG",[],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],[CYCLE],None,
    "The colourless member of the cycling cycle and the only one that does not enter tapped. Easy to lose that difference if the six are treated as one group."))

new.append(card("Gaea's Cradle","JGP",["Legendary"],[],False,None,None,None,
    [ab({"mode":"fixed_variable","unit":"G"},0,None,"{T}",True,var=var("creatures you control"))],
    [], None,
    "first_printing reads JGP because prefer:oldest found the judge promo; the card is legal through Urza's Saga. Amount is 0 by default because with no creatures on the battlefield this taps for nothing at all, and it is not a green source in any meaningful sense until a board exists. That is the entire classification problem here: read as a green land it is a green land, read correctly it is a multiplier on a board state the mana base cannot itself provide. Legendary, so a second copy is dead."))

new.append(card("Serra's Sanctum","USG",["Legendary"],[],False,None,None,None,
    [ab({"mode":"fixed_variable","unit":"W"},0,None,"{T}",True,var=var("enchantments you control"))],
    [], None,
    "See Gaea's Cradle. Same shape, counting enchantments. Produces nothing on an empty board, so it can never be the white source that lets you cast your first enchantment."))

new.append(card("Phyrexian Tower","USG",["Legendary"],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True),
     ab(fixed("B","B"),2,2,"{T}, Sacrifice a creature",True,
        addl={"action":"sacrifice","count":1,"target":"creature"})],
    [], None,
    "The second ability sacrifices a creature, not the land, so sacrifices_self is false and additional_cost carries the price. Repeatable as long as you have creatures. Like Gaea's Cradle it converts a board into mana, but unlike the Cradle it always has a floor: the colourless mode works on an empty board."))

new.append(card("Thran Quarry","USG",[],[],False,None,None,None,
    [ab(choice(*WUBRG),1,1,"{T}",True)],
    [oa("triggered",None,"At the beginning of the end step, if you control no creatures, sacrifice this land.",True)],
    None,
    "Untapped, free, any colour, unlimited. On raw mana production this is the best fixing in the pool so far, and the entire cost is the survival clause. The condition on the mana ability is null on purpose: you can tap it for any colour even with no creatures, it simply dies at the end step. Note the trigger checks at the beginning of the end step of every turn, not only yours, so losing your last creature on an opponent's turn kills it before you untap."))

new.append(card("Shivan Gorge","USG",["Legendary"],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{2}{R}, {T}","Deals 1 damage to each opponent.")],
    None,
    "Colourless source. The damage ability costs {T} plus three mana, so any turn it is used this land is a net drain of three."))

man = [("Faerie Conclave","U","{1}{U}","2/1 blue Faerie with flying"),
       ("Forbidding Watchtower","W","{1}{W}","1/5 white Soldier"),
       ("Ghitu Encampment","R","{1}{R}","2/1 red Warrior with first strike"),
       ("Spawning Pool","B","{1}{B}","1/1 black Skeleton with a regenerate ability"),
       ("Treetop Village","G","{1}{G}","3/3 green Ape with trample")]
for i,(n,col,cost,body) in enumerate(man):
    note = ("Enters tapped, so it is never a turn-one source of its colour, and that is the real cost of the cycle. "
            "Animation does not tap it, so it can be tapped for mana and animated in the same turn, but the animation "
            "cost is mana out of the same pool, and a land that attacks is tapped and produces nothing on your next "
            "turn until it untaps. Still a land while animated, so it keeps its mana ability."
            if i == 0 else "See Faerie Conclave. Same cycle.")
    new.append(card(n,"ULG",[],[],True,None,None,None,
        [ab(fixed(col),1,1,"{T}",True)],
        [oa("activated",cost,"This land becomes a %s until end of turn. It's still a land." % body)],
        None, note))

new.append(card("Yavimaya Hollow","UDS",["Legendary"],[],False,None,None,None,
    [ab(fixed("C"),1,1,"{T}",True)],
    [oa("activated","{G}, {T}","Regenerate target creature.")],
    None,
    "Colourless source. The regeneration ability costs {T} plus a green mana, so it competes with the mana ability and requires green from elsewhere. Legendary."))

have={c["name"] for c in d}
assert not (have & {c["name"] for c in new})
d.extend(new)
json.dump(d, open("premodern_lands.json","w"), indent=2)
print("added",len(new),"total",len(d))
