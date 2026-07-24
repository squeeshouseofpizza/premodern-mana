import json

def ab(produces, amount, net, cost, ss, tap, cond=None, sac=False, addl=None, var=None,
       avail=None, restr=None, zone="battlefield"):
    return {"produces":produces,"amount":amount,"net_mana":net,"cost":cost,
            "additional_cost":addl,"self_sufficient":ss,"condition":cond,
            "sacrifices_self":sac,"variable_amount":var,"availability":avail,
            "restriction":restr,"requires_tap":tap,"zone":zone}
def oa(t,cost,effect,sac=False):
    return {"type":t,"cost":cost,"effect":effect,"sacrifices_self":sac}
def fixed(*m): return {"mode":"fixed","mana":list(m)}
def choice(*o): return {"mode":"choice","options":list(o)}
def uni(o,c): return {"mode":"choice_uniform","options":list(o),"count":c}
def comb(o,c): return {"mode":"choice_combination","options":list(o),"count":c}
def varv(u): return {"mode":"fixed_variable","unit":u}
def V(eq,note=None): return {"equals":eq,"note":note}
WUBRG=["W","U","B","R","G"]

def card(name,kind,mc,cmc,tapped,sick,one_shot,abils,others=None,entry=None,total=None,
         glob=None,notes=""):
    return {"name":name,"kind":kind,"mana_cost":mc,"cmc":cmc,"enters_tapped":tapped,
            "summoning_sick":sick,"one_shot":one_shot,"entry_cost":entry,
            "total_activations":total,"abilities":abils,"other_abilities":others or [],
            "global_effect":glob,"notes":notes}

N=[]
SICK_NOTE=("summoning_sick is true and requires_tap is true on the mana ability, so it produces "
           "nothing the turn it lands.")

# --- one-mana tappers -------------------------------------------------------
N.append(card("Llanowar Elves","creature","{G}",1,False,True,False,
  [ab(fixed("G"),1,1,"{T}",True,True)],
  notes="The baseline mana creature. One green on turn two if it survives, and that conditional is the whole reason Karsten counts dorks as half a source rather than a full one. "+SICK_NOTE))
N.append(card("Fyndhorn Elves","creature","{G}",1,False,True,False,
  [ab(fixed("G"),1,1,"{T}",True,True)],
  notes="Functionally identical to Llanowar Elves."))
N.append(card("Birds of Paradise","creature","{G}",1,False,True,False,
  [ab(choice(*WUBRG),1,1,"{T}",True,True)],
  notes="Any color for one green, which makes it the best fixer in the pool that is not a land, and a flying blocker besides. Still a creature: it dies to everything, and it cannot tap the turn it arrives."))
N.append(card("Wirewood Elf","creature","{1}{G}",2,False,True,False,
  [ab(fixed("G"),1,1,"{T}",True,True)],notes="Two-mana Llanowar Elves."))
N.append(card("Vine Trellis","creature","{1}{G}",2,False,True,False,
  [ab(fixed("G"),1,1,"{T}",True,True)],
  notes="Defender, so it accelerates and blocks and does nothing else. Same mana profile as Wirewood Elf with a far better body for surviving."))
N.append(card("Heart Warden","creature","{1}{G}",2,False,True,False,
  [ab(fixed("G"),1,1,"{T}",True,True)],
  [oa("activated","{2}, Sacrifice","Draw a card.",True)],
  notes="Accelerates early and converts into a card once it stops mattering, the creature version of Mind Stone."))
N.append(card("Skyshroud Troopers","creature","{3}{G}",4,False,True,False,
  [ab(fixed("G"),1,1,"{T}",True,True)],
  notes="Four mana for one green a turn, which is nearly never worth a card. Recorded for completeness."))
N.append(card("Sisters of the Flame","creature","{1}{R}{R}",3,False,True,False,
  [ab(fixed("R"),1,1,"{T}",True,True)],notes="Three mana for one red a turn."))
N.append(card("Llanowar Dead","creature","{B}{G}",2,False,True,False,
  [ab(fixed("B"),1,1,"{T}",True,True)],
  notes="Costs green and black and produces black only, so it does not fix, it converts a two-color investment into one color."))
N.append(card("Utopia Tree","creature","{1}{G}",2,False,True,False,
  [ab(choice(*WUBRG),1,1,"{T}",True,True)],
  notes="Birds of Paradise for one more mana and no flying."))
N.append(card("Werebear","creature","{1}{G}",2,False,True,False,
  [ab(fixed("G"),1,1,"{T}",True,True)],
  [oa("static",None,"Threshold: gets +3/+3 as long as there are seven or more cards in your graveyard.")],
  notes="A mana creature that turns into a 4/4 late. The threshold clause has no bearing on mana."))
N.append(card("Fyndhorn Elder","creature","{2}{G}",3,False,True,False,
  [ab(fixed("G","G"),2,2,"{T}",True,True)],
  notes="Two green from one card, so it is genuine ramp rather than fixing. Three mana in, two per turn after."))
N.append(card("Elvish Aberration","creature","{5}{G}",6,False,True,False,
  [ab(fixed("G","G","G"),3,3,"{T}",True,True)],
  [oa("activated_from_hand","{2}","Forestcycling: search your library for a Forest card, reveal it, put it into your hand, then shuffle.")],
  notes="Six mana for three green a turn, which is a late-game mana sink. The forestcycling mode is the reason it sees play: from hand it is a two-mana Forest tutor, and that mode has nothing to do with its mana ability."))
N.append(card("Nantuko Elder","creature","{2}{G}",3,False,True,False,
  [ab(fixed("C","G"),2,2,"{T}",True,True)],
  notes="Two mana but only one of them green, so produces is mode fixed with both symbols rather than a choice. Reading it as two green would overstate its fixing."))

# --- no tap in the cost, so usable the turn they arrive ----------------------
N.append(card("Wall of Roots","creature","{1}{G}",2,False,False,False,
  [ab(fixed("G"),1,1,"Put a -0/-1 counter on this creature",True,False,
      addl={"action":"put_counter","count":1,"target":"-0/-1 counter on itself"},
      avail={"pattern":"once_each_turn","reason":"Printed restriction: activate only once each turn."})],
  total=5,
  notes="The mana ability has no tap in its cost, so summoning_sick is false and it produces green the turn it lands, which is what separates it from every other two-mana dork in the pool. Five activations total: the body is 0/5 and the fifth counter kills it. Once per turn, so the five are spread across five turns."))
N.append(card("Blood Pet","creature","{B}",1,False,False,True,
  [ab(fixed("B"),1,1,"Sacrifice this creature",True,False,sac=True)],
  notes="One black back for the one black you spent, so it is net zero mana across its life. What it actually does is move a mana from one turn to a later one, and it is not summoning sick because the cost has no tap."))
N.append(card("Blood Vassal","creature","{2}{B}",3,False,False,True,
  [ab(fixed("B","B"),2,2,"Sacrifice this creature",True,False,sac=True)],
  notes="Three mana in, two black back whenever you want them. Net negative overall; it exists to convert a body into black at instant speed."))
N.append(card("Morgue Toad","creature","{2}{B}",3,False,False,True,
  [ab(fixed("U","R"),2,2,"Sacrifice this creature",True,False,sac=True)],
  notes="Cast for black, cashes in for blue and red, so like the Invasion sacrifice lands its two abilities share no colors with its cost. Fixing across color pairs, once."))
N.append(card("Tinder Wall","creature","{G}",1,False,False,True,
  [ab(fixed("R","R"),2,2,"Sacrifice this creature",True,False,sac=True)],
  [oa("activated","{R}, Sacrifice","Deals 2 damage to target creature it's blocking.",True)],
  notes="One green becomes two red, which is a color conversion and a net plus one, available the turn it lands. A defender in the meantime."))
N.append(card("Skirk Prospector","creature","{R}",1,False,False,False,
  [ab(fixed("R"),1,1,"Sacrifice a Goblin",True,False,
      addl={"action":"sacrifice","count":1,"target":"Goblin"})],
  notes="Repeatable within a turn as long as Goblins keep dying, and it can sacrifice itself since it is a Goblin. No tap, so it works immediately. This is a combo engine in the shape of a mana creature."))
N.append(card("Blood Celebrant","creature","{B}",1,False,False,False,
  [ab(choice(*WUBRG),1,0,"{B}, Pay 1 life",False,False)],
  notes="Net zero: one black in, one of any color out, plus a life. Pure conversion, so it can never produce your first colored mana, but it converts an unlimited number of times per turn."))
N.append(card("Agent of Stromgald","creature","{R}",1,False,False,False,
  [ab(fixed("B"),1,0,"{R}",False,False)],
  notes="Net zero red into black, repeatable, no tap. A color converter rather than a mana source."))
N.append(card("Bog Initiate","creature","{1}{B}",2,False,False,False,
  [ab(fixed("B"),1,0,"{1}",False,False)],
  notes="Net zero generic into black, unlimited per turn. Useful only in a deck that needs to convert a lot of colorless into black in one turn."))
N.append(card("Initiates of the Ebon Hand","creature","{B}",1,False,False,False,
  [ab(fixed("B"),1,0,"{1}",False,False,
      avail={"pattern":"self_destructs_past_a_threshold",
             "reason":"Using it four or more times in a turn sacrifices it at the beginning of the next end step."})],
  notes="See Bog Initiate, with a printed cap on enthusiasm: the fourth activation in a turn kills it. Recorded as availability rather than total_activations because the limit is per turn and only bites if you cross it."))
N.append(card("Nomadic Elf","creature","{1}{G}",2,False,False,False,
  [ab(choice(*WUBRG),1,-1,"{1}{G}",False,False)],
  notes="Net minus one, and it requires green to make anything else, so it fixes only for a deck already based in green. Among the worst rates in the pool."))
N.append(card("Skyshroud Elf","creature","{1}{G}",2,False,True,False,
  [ab(fixed("G"),1,1,"{T}",True,True),
   ab(choice("R","W"),1,0,"{1}",False,False)],
  notes="Two abilities with different profiles. The green one taps and is real mana; the red-or-white one is net zero conversion and needs no tap, so it works the turn it lands while the green one does not."))
N.append(card("Skirge Familiar","creature","{4}{B}",5,False,False,False,
  [ab(fixed("B"),1,1,"Discard a card",True,False,
      addl={"action":"discard","count":1,"target":"a card"})],
  notes="Converts cards into black mana at one for one, unlimited within a turn and no tap required. Five mana to deploy, so it is a combo piece and not acceleration."))
N.append(card("Overeager Apprentice","creature","{2}{B}",3,False,False,True,
  [ab(fixed("B","B","B"),3,3,"Discard a card, Sacrifice this creature",True,False,sac=True)],
  notes="Three black at instant speed for a card and the body. Net zero against its own casting cost, so it is a ritual with a delay rather than acceleration."))

# --- tap plus a mana cost ---------------------------------------------------
N.append(card("Apprentice Wizard","creature","{1}{U}{U}",3,False,True,False,
  [ab(fixed("C","C","C"),3,2,"{U}, {T}",False,True)],
  notes="Net plus two per turn, which is the best repeatable rate on any creature here, and it needs blue mana to work so it cannot bootstrap itself. "+SICK_NOTE))
N.append(card("Bog Witch","creature","{2}{B}",3,False,True,False,
  [ab(fixed("B","B","B"),3,2,"{B}, {T}, Discard a card",False,True,
      addl={"action":"discard","count":1,"target":"a card"})],
  notes="A repeatable Dark Ritual that costs a card each time. Net plus two in mana, minus one in cards."))
N.append(card("Sea Scryer","creature","{1}{U}",2,False,True,False,
  [ab(fixed("C"),1,1,"{T}",True,True),
   ab(fixed("U"),1,0,"{1}, {T}",False,True)],
  notes="Both abilities tap it, so they are mutually exclusive: colorless for free, or blue at net zero. Structurally the Homelands castle pattern on a creature."))
N.append(card("Helionaut","creature","{2}{W}",3,False,True,False,
  [ab(choice(*WUBRG),1,0,"{1}, {T}",False,True)],
  notes="Net zero fixing on a flying body. Cannot make your first colored mana."))
N.append(card("Ceta Disciple","creature","{U}",1,False,True,False,
  [ab(choice(*WUBRG),1,0,"{G}, {T}",False,True)],
  [oa("activated","{R}, {T}","Target creature gets +2/+0 until end of turn.")],
  notes="Costs blue to cast, green to activate, and produces any color at net zero. A three-color card that fixes for none of them until you already have two."))
N.append(card("Necra Disciple","creature","{B}",1,False,True,False,
  [ab(choice(*WUBRG),1,0,"{G}, {T}",False,True)],
  [oa("activated","{W}, {T}","Prevent the next 1 damage that would be dealt to any target this turn.")],
  notes="See Ceta Disciple. Same cycle, black body, green activation."))

# --- board-dependent and variable ------------------------------------------
N.append(card("Priest of Titania","creature","{1}{G}",2,False,True,False,
  [ab(varv("G"),0,None,"{T}",True,True,
      var=V("the number of Elves on the battlefield",
            "Counts every Elf in play including opponents' and including itself."))],
  notes="Zero on an empty board and enormous in an Elf deck, so amount is 0 and the real number lives in variable_amount, exactly as with Gaea's Cradle. Note it counts all Elves on the battlefield, not just yours, and it counts itself."))
N.append(card("Rofellos, Llanowar Emissary","creature","{G}{G}",2,False,True,False,
  [ab(varv("G"),0,None,"{T}",True,True,
      var=V("the number of Forests you control","Counts by land type, so Snow-Covered Forest counts."))],
  notes="Legendary. Counts Forests by land type, so snow basics count and nonbasic green lands without the Forest type do not. Zero in a deck with no Forests, which is not hypothetical in a format where much of the fixing is nonbasic."))
N.append(card("Wirewood Channeler","creature","{3}{G}",4,False,True,False,
  [ab({"mode":"choice_uniform_variable","options":WUBRG},0,None,"{T}",True,True,
      var=V("the number of Elves on the battlefield","All the mana must be the same chosen color."))],
  notes="Like Priest of Titania but any single color, which turns an Elf board into fixing as well as ramp. All the mana is one color, not spread across several."))
N.append(card("Soldevi Adnate","creature","{1}{B}",2,False,True,False,
  [ab(varv("B"),0,None,"{T}, Sacrifice a black or artifact creature",True,True,
      addl={"action":"sacrifice","count":1,"target":"black or artifact creature"},
      var=V("the mana value of the sacrificed creature","Zero if the creature sacrificed costs zero."))],
  notes="Converts a large creature into black mana equal to its cost. Needs a specific kind of creature to eat, so in most decks it is dead weight and in a reanimator shell it is a ritual."))
N.append(card("Harvester Druid","creature","{1}{G}",2,False,True,False,
  [ab({"mode":"derived","source":"any color a land you control could produce"},1,1,"{T}",True,True,
      cond={"type":"controls_land_producing_mana"})],
  notes="Mirrors your own lands, so it fixes nothing your mana base cannot already do; what it does is add a second copy of a color you are short of. Reflecting Pool on a body, with the same bootstrapping limit."))
N.append(card("Quirion Explorer","creature","{1}{G}",2,False,True,False,
  [ab({"mode":"derived","source":"any color a land an opponent controls could produce"},1,1,"{T}",True,True,
      cond={"type":"opponent_controls_land_producing_mana"})],
  notes="Reads the opponent's lands, so its value is a matchup question and it can be blank in game one. Fellwar Stone on a body."))
N.append(card("Benthic Explorers","creature","{3}{U}",4,False,True,False,
  [ab({"mode":"derived","source":"any mana type the untapped land could produce"},1,1,"{T}, Untap a tapped land an opponent controls",True,True,
      addl={"action":"untap","count":1,"target":"tapped land an opponent controls"},
      cond={"type":"opponent_controls_tapped_land"})],
  notes="Requires the opponent to have a tapped land, so it does nothing on your turn against an untapped board and nothing at all against an opponent who holds mana up. Four mana for a conditional one."))
N.append(card("Quirion Elves","creature","{1}{G}",2,False,True,False,
  [ab(fixed("G"),1,1,"{T}",True,True),
   ab(choice(*WUBRG),1,1,"{T}",True,True,
      cond={"type":"color_chosen_as_it_enters"})],
  notes="The second color is locked in as it enters and cannot be changed afterwards, so the choice mode here is a one-time decision. Both abilities tap it, so it makes one mana a turn, of green or of the named color."))
N.append(card("Urborg Elf","creature","{1}{G}",2,False,True,False,
  [ab(choice("B","G","U"),1,1,"{T}",True,True)],
  notes="Three fixed colors, no choice made on entry, one mana a turn."))
N.append(card("Pygmy Hippo","creature","{G}{U}",2,False,False,False,
  [ab(varv("C"),0,None,"Combat damage trigger when unblocked",True,False,
      cond={"type":"attacks_and_is_unblocked"},
      var=V("the amount of mana the defending player lost this way",
            "Depends entirely on the opponent's untapped lands and their choices."))],
  notes="Mana as a combat trigger, contingent on attacking, being unblocked, and the opponent having lands to drain. It also gives up its combat damage to do it. Not a mana source in any sense a calculator should count; recorded so it is not mistaken for one."))
N.append(card("Witch Engine","creature","{5}{B}",6,False,True,True,
  [ab(fixed("B","B","B","B"),4,4,"{T}",True,True)],
  [oa("triggered",None,"Target opponent gains control of this creature when the mana ability is used.")],
  notes="Four black once, and then your opponent owns the creature, which is why one_shot is true even though the ability is not printed as a sacrifice. Six mana to deploy makes this a late-game burst, not ramp."))

# --- from other zones and global effects ------------------------------------
N.append(card("Elvish Spirit Guide","creature","{2}{G}",3,False,False,True,
  [ab(fixed("G"),1,1,"Exile this creature from your hand",True,False,zone="hand")],
  notes="Free green from your hand without ever casting it, which makes it one of the very few cards in the pool that can produce colored mana on turn one before any land is played. The zone field exists for this: counted as a battlefield source it would be wrong twice over, since it never enters play when used this way."))
N.append(card("Citanul Hierophants","creature","{3}{G}",4,False,True,False,
  [ab(fixed("G"),1,1,"{T}",True,True)],
  glob={"applies_to":"creatures you control","grants":"{T}: Add {G}","active_zone":"battlefield"},
  notes="Grants every creature you control a green mana ability, so like Riftstone Portal it changes what other cards do and cannot be evaluated on its own. Its own tap ability comes from the same granted ability. Any count that sums per-card colors is wrong about your whole board while this is out, and the granted abilities are subject to summoning sickness on the creatures receiving them."))
N.append(card("Birchlore Rangers","creature","{G}",1,False,False,False,
  [ab(choice(*WUBRG),1,1,"Tap two untapped Elves you control",True,False,
      addl={"action":"tap","count":2,"target":"untapped Elves you control"},
      cond={"type":"controls_n_creature_type","value":2,"creature_type":"Elf"})],
  notes="The cost taps other Elves rather than using this creature's own tap symbol, so summoning-sick Elves can be tapped to pay it and this card works the turn it lands. Any color, which makes an Elf board into full fixing."))
N.append(card("Seton, Krosan Protector","creature","{G}{G}{G}",3,False,False,False,
  [ab(fixed("G"),1,1,"Tap an untapped Druid you control",True,False,
      addl={"action":"tap","count":1,"target":"untapped Druid you control"},
      cond={"type":"controls_creature_type","value":"Druid"})],
  notes="See Birchlore Rangers on the tapping cost. Legendary in effect through its name only; it is a Druid itself, so it can tap itself if it is not summoning sick, and other Druids regardless."))
N.append(card("Quirion Sentinel","creature","{1}{G}",2,False,False,True,
  [ab(choice(*WUBRG),1,1,"When this creature enters",True,False)],
  notes="One mana of any color, once, on arrival. Net minus one against its casting cost, so it is a two-mana body that refunds one and fixes a color."))
N.append(card("Priest of Gix","creature","{2}{B}",3,False,False,True,
  [ab(fixed("B","B","B"),3,3,"When this creature enters",True,False)],
  notes="Three black on arrival for a three-mana creature, so it is free to cast in black-mana terms and leaves a body behind. The mana comes on the trigger, not from an activated ability, so it cannot be held for later."))

# --- restricted mana --------------------------------------------------------
N.append(card("Soldevi Machinist","creature","{1}{U}",2,False,True,False,
  [ab(fixed("C","C"),2,2,"{T}",True,True,
      restr="Spend this mana only to activate abilities of artifacts.")],
  notes="Two colorless a turn that cannot cast a single spell. The restriction field is doing all the work here, exactly as with Thran Turbine."))
N.append(card("Adarkar Unicorn","creature","{1}{W}{W}",3,False,True,False,
  [ab(fixed("U"),1,1,"{T}",True,True,restr="Spend this mana only to pay cumulative upkeep costs."),
   ab(fixed("C","U"),2,2,"{T}",True,True,restr="Spend this mana only to pay cumulative upkeep costs.")],
  notes="The printed ability offers a choice between one mana and two, which is a choice of amount rather than of color, so it is split into two mutually exclusive entries. Both are restricted to paying cumulative upkeep, which makes this unusable as mana in almost every deck."))

# --- forest sacrifice -------------------------------------------------------
N.append(card("Orcish Lumberjack","creature","{R}",1,False,True,False,
  [ab(comb(["R","G"],3),3,3,"{T}, Sacrifice a Forest",True,True,
      addl={"action":"sacrifice","count":1,"target":"Forest"},
      cond={"type":"controls_land_type","value":["Forest"]})],
  notes="Three mana in any mix of red and green for one land, which is why produces needed a combination mode: unlike Lion's Eye Diamond the three do not have to match. Eats a Forest each time, so it trades long-term mana for a burst, and it checks the Forest land type rather than the card name."))
N.append(card("Goblin Clearcutter","creature","{3}{R}",4,False,True,False,
  [ab(comb(["R","G"],3),3,3,"{T}, Sacrifice a Forest",True,True,
      addl={"action":"sacrifice","count":1,"target":"Forest"},
      cond={"type":"controls_land_type","value":["Forest"]})],
  notes="See Orcish Lumberjack. Four mana instead of one for the same ability."))
N.append(card("Jungle Patrol","creature","{3}{G}",4,False,True,False,
  [ab(fixed("R"),1,1,"Sacrifice a token named Wood",True,False,
      addl={"action":"sacrifice","count":1,"target":"token named Wood"},
      cond={"type":"controls_token","value":"Wood"})],
  [oa("activated","{1}{G}, {T}","Create a 0/1 green Wall creature token with defender named Wood.")],
  notes="Two steps and net negative: two mana and a tap makes a token, and the token converts into one red. Green into red conversion at a punishing rate."))

d=json.load(open("data/premodern_nonlands.json"))
for c in d:
    c.setdefault("global_effect",None)
    for a in c["abilities"]:
        a.setdefault("requires_tap","{T}" in a["cost"])
        a.setdefault("zone","battlefield")
have={c["name"] for c in d}
assert not (have & {c["name"] for c in N}), "duplicate"
d.extend(N)
json.dump(d,open("data/premodern_nonlands.json","w"),indent=2)
print("creatures added:",len(N),"| nonlands total:",len(d))
