import json

def ab(produces, amount, net, cost, ss, cond=None, sac=False, addl=None, var=None,
       avail=None, restr=None):
    return {"produces": produces, "amount": amount, "net_mana": net, "cost": cost,
            "additional_cost": addl, "self_sufficient": ss, "condition": cond,
            "sacrifices_self": sac, "variable_amount": var, "availability": avail,
            "restriction": restr}
def oa(t, cost, effect, sac=False):
    return {"type": t, "cost": cost, "effect": effect, "sacrifices_self": sac}
def fixed(*m): return {"mode":"fixed","mana":list(m)}
def choice(*o): return {"mode":"choice","options":list(o)}
def uni(opts,count): return {"mode":"choice_uniform","options":list(opts),"count":count}
def varv(unit): return {"mode":"fixed_variable","unit":unit}
def V(eq,note=None): return {"equals":eq,"note":note}
WUBRG=["W","U","B","R","G"]

def card(name,kind,mc,cmc,tapped,sick,one_shot,abils,others=None,entry=None,total=None,notes=""):
    return {"name":name,"kind":kind,"mana_cost":mc,"cmc":cmc,"enters_tapped":tapped,
            "summoning_sick":sick,"one_shot":one_shot,"entry_cost":entry,
            "total_activations":total,"abilities":abils,"other_abilities":others or [],
            "notes":notes}

C=[]

# --- plain colourless rocks -------------------------------------------------
C.append(card("Sisay's Ring","artifact","{4}",4,False,False,False,
  [ab(fixed("C","C"),2,2,"{T}",True)],
  notes="Four mana for a rock that taps for two. Net positive from the turn after it lands, and never fixes colour. cmc is the number that matters most on these: it cannot contribute anything before turn four on an untouched curve."))
C.append(card("Thran Dynamo","artifact","{4}",4,False,False,False,
  [ab(fixed("C","C","C"),3,3,"{T}",True)],
  notes="Same slot as Sisay's Ring for one more mana of output. Colourless only."))
C.append(card("Worn Powerstone","artifact","{3}",3,True,False,False,
  [ab(fixed("C","C"),2,2,"{T}",True)],
  notes="Enters tapped, so the turn it is cast it does nothing at all. Three mana in, two per turn from the following turn onward."))
C.append(card("Mind Stone","artifact","{2}",2,False,False,False,
  [ab(fixed("C"),1,1,"{T}",True)],
  [oa("activated","{1}, {T}, Sacrifice","Draw a card.",True)],
  notes="Ramps for one and cashes itself in for a card later, so it is the rare accelerant that is not dead in the late game. The draw mode competes with the mana ability for the tap."))
C.append(card("Manakin","creature","{2}",2,False,True,False,
  [ab(fixed("C"),1,1,"{T}",True)],
  notes="A rock that can be killed. summoning_sick is true and it is the field that separates this from Mind Stone: cast on turn two, it produces nothing until turn three."))
C.append(card("Millikin","creature","{2}",2,False,True,False,
  [ab(fixed("C"),1,1,"{T}",True,addl={"action":"mill","count":1})],
  notes="Colourless mana that costs a card off the top each time. In a deck that wants a full graveyard the mill is upside; anywhere else it is a real cost and additional_cost records it rather than burying it in text."))

# --- mana batteries ---------------------------------------------------------
for n,col in [("White Mana Battery","W"),("Blue Mana Battery","U"),("Black Mana Battery","B"),
              ("Red Mana Battery","R"),("Green Mana Battery","G")]:
    first = n=="White Mana Battery"
    C.append(card(n,"artifact","{4}",4,False,False,False,
      [ab(varv(col),1,None,"{T}, Remove any number of charge counters",True,
          var=V("one plus the number of charge counters removed",
                "Removing zero counters still adds one, so the floor is 1 rather than 0."))],
      [oa("activated","{2}, {T}","Put a charge counter on this artifact.")],
      notes=("Reads like a storage artifact and works like a bad mana rock. Removing no counters "
             "still adds one, so amount is 1, not 0. Charging costs {2} and the tap, which buys "
             "one future mana for two present ones, so the storage mode is a net loss and the "
             "card is really a four-mana rock that taps for one of its colour."
             if first else "See White Mana Battery. Same cycle.")))

# --- Invasion cameos --------------------------------------------------------
for n,cols in [("Seashell Cameo",["W","U"]),("Drake-Skull Cameo",["U","B"]),
               ("Bloodstone Cameo",["B","R"]),("Troll-Horn Cameo",["R","G"]),
               ("Tigereye Cameo",["G","W"])]:
    C.append(card(n,"artifact","{3}",3,False,False,False,
      [ab(choice(*cols),1,1,"{T}",True)],
      notes=("Three mana for a rock that taps for one of two colours. Fixes without accelerating, "
             "since it costs three to add one. Its value is entirely colour, which makes it the "
             "artifact answer to the same problem the Invasion taplands solve for free."
             if n=="Seashell Cameo" else "See Seashell Cameo. Same cycle.")))

# --- Mirage-era diamonds ----------------------------------------------------
for n,col in [("Marble Diamond","W"),("Sky Diamond","U"),("Charcoal Diamond","B"),
              ("Fire Diamond","R"),("Moss Diamond","G")]:
    C.append(card(n,"artifact","{2}",2,True,False,False,
      [ab(fixed(col),1,1,"{T}",True)],
      notes=("Two mana, enters tapped, then taps for one of its colour every turn. Genuine "
             "acceleration from the turn after it lands, and the enters_tapped flag is why it is "
             "not acceleration on the turn you cast it."
             if n=="Marble Diamond" else "See Marble Diamond. Same cycle.")))

# --- Odyssey eggs -----------------------------------------------------------
for n,cols in [("Skycloud Egg",["W","U"]),("Darkwater Egg",["U","B"]),
               ("Shadowblood Egg",["B","R"]),("Mossfire Egg",["R","G"]),
               ("Sungrass Egg",["G","W"])]:
    C.append(card(n,"artifact","{1}",1,False,False,True,
      [ab(fixed(*cols),2,0,"{2}, {T}, Sacrifice",False,sac=True)],
      [oa("activated","{2}, {T}, Sacrifice","Draw a card.",True)],
      notes=("Net zero mana. You pay {2} and get two back, so this never accelerates anything; it "
             "converts generic mana into two specific colours and replaces itself with a card. "
             "self_sufficient is false, so it can never produce your first coloured mana, which "
             "is the same trap as the Odyssey filter lands from the same block."
             if n=="Skycloud Egg" else "See Skycloud Egg. Same cycle.")))

# --- Masques Ramos artifacts ------------------------------------------------
for n,col in [("Tooth of Ramos","W"),("Eye of Ramos","U"),("Skull of Ramos","B"),
              ("Heart of Ramos","R"),("Horn of Ramos","G")]:
    C.append(card(n,"artifact","{3}",3,False,False,False,
      [ab(fixed(col),1,1,"{T}",True),
       ab(fixed(col),1,1,"Sacrifice",True,sac=True)],
      notes=("The sacrifice ability has no tap symbol in its cost, which is the detail worth "
             "having. You can tap it for one and then sacrifice it for another in the same turn, "
             "so it is two mana in a pinch, and the sacrifice still works while it is tapped or "
             "summoning-sick-irrelevant. Three mana for one per turn is otherwise poor."
             if n=="Tooth of Ramos" else "See Tooth of Ramos. Same cycle.")))

# --- Invasion attendants ----------------------------------------------------
for n,cols in [("Dromar's Attendant",["W","U","B"]),("Crosis's Attendant",["U","B","R"]),
               ("Darigaaz's Attendant",["B","R","G"]),("Rith's Attendant",["R","G","W"]),
               ("Treva's Attendant",["G","W","U"])]:
    C.append(card(n,"creature","{5}",5,False,False,True,
      [ab(fixed(*cols),3,2,"{1}, Sacrifice",False,sac=True)],
      notes=("Five mana for a 2/2 that can later be turned into three specific colours for one. "
             "The mana ability has no tap in its cost, so summoning sickness does not stop you "
             "cracking it the turn it arrives. Net plus two when used, but you have already paid "
             "five, so this is fixing for a deck that got there, not acceleration."
             if n=="Dromar's Attendant" else "See Dromar's Attendant. Same cycle.")))

# --- zero-cost fast mana ----------------------------------------------------
C.append(card("Lotus Petal","artifact","{0}",0,False,False,True,
  [ab(choice(*WUBRG),1,1,"{T}, Sacrifice",True,sac=True)],
  notes="Free to cast and produces any colour once, so it is one of the few nonland cards in the pool that genuinely can be your first coloured mana on turn one. One shot: using it is the end of it. Net plus one on the turn it is used and minus a card overall."))
C.append(card("Mox Diamond","artifact","{0}",0,False,False,False,
  [ab(choice(*WUBRG),1,1,"{T}",True)],
  entry={"action":"discard","count":1,"target":"land card","timing":"replacement","if_unmet":"graveyard"},
  notes="Free, untapped, any colour, every turn, and the price is a land card discarded as it enters. Same replacement-effect shape as the Alliances lands, so entry_cost carries it: if you cannot or will not discard a land it goes straight to the graveyard. In land-count terms it is a wash, which is why it is played as fixing and tempo rather than as ramp."))
C.append(card("Lion's Eye Diamond","artifact","{0}",0,False,False,True,
  [ab(uni(WUBRG,3),3,3,"Discard your hand, Sacrifice",True,sac=True)],
  notes="Three mana of one colour for free, and the cost is your entire hand, which is why it only functions in decks built to empty their hand first or to use the mana before the discard matters. Instant speed only. produces uses choice_uniform because all three mana are the same chosen colour, not three colours."))

# --- filters and converters -------------------------------------------------
C.append(card("Mana Cylix","artifact","{1}",1,False,False,False,
  [ab(choice(*WUBRG),1,0,"{1}, {T}",False)],
  notes="Pure colour conversion at net zero. Never accelerates and can never make your first coloured mana. The cheapest fixer in the pool and correspondingly the weakest."))
C.append(card("Celestial Prism","artifact","{3}",3,False,False,False,
  [ab(choice(*WUBRG),1,-1,"{2}, {T}",False)],
  notes="Net minus one per activation. Three to cast and then it loses you mana every time you use it, so it is only fixing of last resort."))
C.append(card("Mana Prism","artifact","{3}",3,False,False,False,
  [ab(fixed("C"),1,1,"{T}",True),
   ab(choice(*WUBRG),1,0,"{1}, {T}",False)],
  notes="Two modes, and only the colourless one is self-sufficient. Structurally identical to the Homelands castles: a colourless source with a conversion button attached."))
C.append(card("Phyrexian Lens","artifact","{3}",3,False,False,False,
  [ab(choice(*WUBRG),1,1,"{T}, Pay 1 life",True)],
  notes="Any colour, no mana cost to activate, so self_sufficient is true and the price is a life per use. The artifact equivalent of City of Brass, except the life loss is part of the ability rather than a trigger on tapping."))
C.append(card("Chromatic Sphere","artifact","{1}",1,False,False,True,
  [ab(choice(*WUBRG),1,0,"{1}, {T}, Sacrifice",False,sac=True)],
  [oa("activated","{1}, {T}, Sacrifice","Draw a card.",True)],
  notes="Net zero mana that replaces itself with a card immediately. Fixing and deck-thinning rather than acceleration."))
C.append(card("Barbed Sextant","artifact","{1}",1,False,False,True,
  [ab(choice(*WUBRG),1,0,"{1}, {T}, Sacrifice",False,sac=True)],
  [oa("activated","{1}, {T}, Sacrifice","Draw a card at the beginning of the next turn's upkeep.",True)],
  notes="See Chromatic Sphere, except the card arrives next upkeep rather than immediately, which makes it materially worse in any deck that wanted the card now."))
C.append(card("Astrolabe","artifact","{3}",3,False,False,True,
  [ab(uni(WUBRG,2),2,1,"{1}, {T}, Sacrifice",False,sac=True)],
  [oa("activated","{1}, {T}, Sacrifice","Draw a card at the beginning of the next turn's upkeep.",True)],
  notes="Two mana of one chosen colour for one, so net plus one, plus a delayed card. Not to be confused with the Modern Horizons card of a similar name, which is not in this pool."))

# --- board-dependent --------------------------------------------------------
C.append(card("Fellwar Stone","artifact","{2}",2,False,False,False,
  [ab({"mode":"derived","source":"any colour a land an opponent controls could produce"},1,1,"{T}",True,
      cond={"type":"opponent_controls_land_producing_mana"})],
  notes="Colours resolve against the opponent's board, not yours and not the card, so it is the one accelerant in the pool whose usefulness is a matchup question. Against a mono-coloured deck it is a one-colour rock; against nothing it produces nothing. Note it reads colours, so an opponent playing only colourless-producing lands leaves it dead."))
C.append(card("Star Compass","artifact","{2}",2,True,False,False,
  [ab({"mode":"derived","source":"any colour a basic land you control could produce"},1,1,"{T}",True,
      cond={"type":"controls_basic_land"})],
  notes="Mirrors your own basics, so in a deck with no basic lands it produces nothing at all. Enters tapped. Worth pairing with the land file: fetchlands find basics, and this reads basics, so the two interact in a way neither card mentions."))
C.append(card("Sol Grail","artifact","{3}",3,False,False,False,
  [ab(choice(*WUBRG),1,1,"{T}",True)],
  notes="The colour is chosen as it enters and then fixed for the rest of the game, so the choice mode here is a one-time decision rather than a per-activation one. Treat it as a rock of whichever colour you named."))
C.append(card("Charmed Pendant","artifact","{4}",4,False,False,False,
  [ab({"mode":"derived","source":"the coloured mana symbols in the milled card's mana cost"},0,None,"{T}, Mill a card",True,
      addl={"action":"mill","count":1},
      var=V("the number of coloured pips on the card milled",
            "Zero if the milled card is a land or has no coloured pips."))],
  notes="Output is whatever the top of your library happens to be, so it can produce nothing, and the floor of zero is real rather than theoretical. Instant speed only. Any calculator should treat this as unreliable rather than as four fixed sources."))

# --- sacrifice outlets ------------------------------------------------------
C.append(card("Ashnod's Altar","artifact","{3}",3,False,False,False,
  [ab(fixed("C","C"),2,2,"Sacrifice a creature",True,
      addl={"action":"sacrifice","count":1,"target":"creature"})],
  notes="No tap in the cost, so it is repeatable as many times as you have creatures within a single turn. That makes it a combo piece rather than a mana rock, and a source count is the wrong lens for it entirely."))
C.append(card("Phyrexian Altar","artifact","{3}",3,False,False,False,
  [ab(choice(*WUBRG),1,1,"Sacrifice a creature",True,
      addl={"action":"sacrifice","count":1,"target":"creature"})],
  notes="See Ashnod's Altar. One mana instead of two, but any colour, and likewise unlimited within a turn."))
C.append(card("Cathodion","creature","{3}",3,False,False,True,
  [ab(fixed("C","C","C"),3,3,"When this creature dies",True,sac=True)],
  notes="The mana comes from a death trigger rather than an activated ability, so you do not control the timing unless you also control a sacrifice outlet. Three mana back from a three-mana body makes it free to loop with an altar."))
C.append(card("Workhorse","creature","{6}",6,False,False,False,
  [ab(fixed("C"),1,1,"Remove a +1/+1 counter",True,
      addl={"action":"remove_counter","count":1,"target":"+1/+1 counter"})],
  total=4,
  notes="Four activations, one per counter, and each one shrinks the creature. total_activations is 4 for the same reason Gemstone Mine's is 3: the limit is printed, not situational. No tap in the cost, so all four can be used in one turn."))

# --- storage and charge -----------------------------------------------------
C.append(card("Kyren Toy","artifact","{3}",3,False,False,False,
  [ab(varv("C"),1,None,"{T}, Remove X charge counters",True,
      var=V("X plus one, where X is the number of charge counters removed",
            "Removing zero counters still adds one, so the floor is 1."))],
  [oa("activated","{1}, {T}","Put a charge counter on this artifact.")],
  notes="Charging costs {1} and the tap to buy one future colourless, so like the mana batteries the storage mode loses tempo. The floor is one, not zero."))
C.append(card("Jeweled Amulet","artifact","{0}",0,False,False,False,
  [ab({"mode":"derived","source":"the type of mana spent to charge it"},1,1,"{T}, Remove a charge counter",True,
      cond={"type":"has_charge_counter"})],
  [oa("activated","{1}, {T}","Put a charge counter and note the type of mana spent. Activate only if there are no charge counters on this artifact.")],
  notes="The release ability costs no mana and yields one, so per ability it is net plus one; across the full cycle of charging and releasing it is net zero, one mana in and the same one back out later. It moves mana across turns rather than making any, which is occasionally what a deck wants and is never acceleration."))
C.append(card("Lotus Blossom","artifact","{2}",2,False,False,True,
  [ab(varv("any one colour"),0,None,"{T}, Sacrifice",True,sac=True,
      var=V("the number of petal counters","One counter per upkeep, starting the turn after it lands, so the payoff grows only if it survives."))],
  [oa("triggered",None,"At the beginning of your upkeep, you may put a petal counter on this artifact.")],
  notes="Produces nothing the turn it is cast and nothing at all if cracked immediately, so amount is 0. Every point of output is a turn of it sitting on the battlefield being a target."))
C.append(card("Ventifact Bottle","artifact","{3}",3,False,False,False,
  [ab(varv("C"),0,None,"Automatic at the beginning of your first main phase",True,
      var=V("the number of charge counters removed","All counters are removed at once and the artifact taps itself."))],
  [oa("activated","{X}{1}, {T}","Put X charge counters on this artifact. Activate only as a sorcery.")],
  notes="Charging costs X plus one to store X, so every cycle loses a mana, and the release is not optional: it fires at your first main phase whether or not you want it. A calculator should treat this as a mana sink, not a source."))
C.append(card("Thran Turbine","artifact","{1}",1,False,False,False,
  [ab(fixed("C","C"),2,2,"At the beginning of your upkeep",True,
      restr="This mana can't be spent to cast spells.")],
  notes="Two free colourless every upkeep that cannot pay for a single spell. The restriction field exists for this card: counted as a source without it, it would look like the best accelerant in the format. It pays for activated abilities only."))
C.append(card("Diamond Kaleidoscope","artifact","{4}",4,False,False,False,
  [ab(choice(*WUBRG),1,1,"Sacrifice a Prism token",True,
      addl={"action":"sacrifice","count":1,"target":"Prism token"},
      cond={"type":"controls_token","value":"Prism"})],
  [oa("activated","{3}, {T}","Create a 0/1 colourless Prism artifact creature token.")],
  notes="Two steps and both are expensive: four to cast, then three and a tap per token, and each token converts into exactly one mana of any colour. Net deeply negative as mana; it exists for decks that want the tokens themselves."))

# --- big creatures ----------------------------------------------------------
C.append(card("Metalworker","creature","{3}",3,False,True,False,
  [ab(varv("C"),0,None,"{T}",True,
      var=V("two per artifact card revealed from your hand",
            "Reveal only, the cards are not spent, so the same hand can be revealed every turn."))],
  notes="Zero in a deck with no other artifacts and enormous in a deck built around them, which makes it the clearest case in this file for keeping assumed values out of the data. Summoning sick, so nothing on the turn it lands. The cards are revealed rather than discarded, so the same hand works every turn."))
C.append(card("Lotus Guardian","creature","{7}",7,False,True,False,
  [ab(choice(*WUBRG),1,1,"{T}",True)],
  notes="Seven mana for a flying body that taps for one of any colour. By the time this is castable the fixing is decoration."))

json.dump(C,open("data/premodern_nonlands.json","w"),indent=2)
print("artifacts classified:",len(C))
