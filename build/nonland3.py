import json

def ab(produces,amount,net,cost,ss,tap,cond=None,sac=False,addl=None,var=None,
       avail=None,restr=None,zone="battlefield"):
    return {"produces":produces,"amount":amount,"net_mana":net,"cost":cost,
            "additional_cost":addl,"self_sufficient":ss,"condition":cond,
            "sacrifices_self":sac,"variable_amount":var,"availability":avail,
            "restriction":restr,"requires_tap":tap,"zone":zone}
def oa(t,cost,effect,sac=False): return {"type":t,"cost":cost,"effect":effect,"sacrifices_self":sac}
def fixed(*m): return {"mode":"fixed","mana":list(m)}
def choice(*o): return {"mode":"choice","options":list(o)}
def uni(o,c): return {"mode":"choice_uniform","options":list(o),"count":c}
def comb(o,c): return {"mode":"choice_combination","options":list(o),"count":c}
def varv(u): return {"mode":"fixed_variable","unit":u}
def V(eq,note=None): return {"equals":eq,"note":note}
def G(applies,grants,kind,duration="permanent",zone="battlefield"):
    return {"applies_to":applies,"grants":grants,"kind":kind,"duration":duration,"active_zone":zone}
WUBRG=["W","U","B","R","G"]

def card(name,kind,mc,cmc,one_shot,abils,others=None,entry=None,total=None,glob=None,
         tapped=False,sick=False,notes=""):
    return {"name":name,"kind":kind,"mana_cost":mc,"cmc":cmc,"enters_tapped":tapped,
            "summoning_sick":sick,"one_shot":one_shot,"entry_cost":entry,
            "total_activations":total,"abilities":abils,"other_abilities":others or [],
            "global_effect":glob,"notes":notes}
def spell(name,kind,mc,cmc,produces,amount,cond=None,addl=None,var=None,restr=None,notes=""):
    net = None if var else amount-cmc
    return card(name,kind,mc,cmc,True,
      [ab(produces,amount,net,"Resolve this spell",False,False,cond=cond,addl=addl,
          var=var,restr=restr,zone="stack")],notes=notes)

N=[]

# --- rituals ----------------------------------------------------------------
N.append(spell("Dark Ritual","instant","{B}",1,fixed("B","B","B"),3,
  notes="Net plus two, and self_sufficient is false because casting it costs black. That is the whole point for a mana calculator: Dark Ritual can never be your first black mana, it multiplies black you already have. Same structural failure as the Odyssey filter lands, in a different card type."))
N.append(card("Cabal Ritual","instant","{1}{B}",2,True,
  [ab(fixed("B","B","B"),3,1,"Resolve this spell",False,False,zone="stack"),
   ab(fixed("B","B","B","B","B"),5,3,"Resolve this spell",False,False,zone="stack",
      cond={"type":"threshold","value":"seven or more cards in your graveyard"})],
  notes="Two mutually exclusive outputs from one printed spell, split so a consumer can pick the higher one when threshold is on. Net plus one before threshold and plus three after, so the same card is mediocre early and a genuine accelerant late."))
N.append(spell("Culling the Weak","instant","{B}",1,fixed("B","B","B","B"),4,
  addl={"action":"sacrifice","count":1,"target":"creature","timing":"additional cost to cast"},
  notes="Net plus three, the largest single burst in the pool, and the price is a creature on top of the black mana. The sacrifice is an additional cost to cast, so it happens whether or not the spell resolves."))
N.append(spell("Burnt Offering","instant","{B}",1,comb(["B","R"],0),0,
  addl={"action":"sacrifice","count":1,"target":"creature","timing":"additional cost to cast"},
  var=V("the sacrificed creature's mana value","Any mix of black and red. Zero if you sacrifice a zero-cost creature."),
  notes="Converts a creature's mana value into black and red in any combination. Amount is 0 because sacrificing a token or a free creature yields nothing."))
N.append(spell("Songs of the Damned","instant","{B}",1,varv("B"),0,
  var=V("the number of creature cards in your graveyard","Zero on an empty graveyard."),
  notes="Dead early and enormous in a deck that fills its own graveyard. Amount 0 with the real number in variable_amount, the same treatment as Gaea's Cradle."))
N.append(spell("Brightstone Ritual","instant","{R}",1,varv("R"),0,
  var=V("the number of Goblins on the battlefield","Counts every Goblin in play, including your opponent's."),
  notes="A ritual that only exists in one deck. Note it counts all Goblins on the battlefield rather than only yours."))
N.append(spell("Spoils of Evil","instant","{2}{B}",3,varv("C"),0,
  var=V("the number of artifact and creature cards in target opponent's graveyard","Zero against an empty graveyard."),
  notes="Colorless, contingent entirely on the opponent's graveyard, so it is unreliable by construction and gains life alongside."))
N.append(spell("Energy Tap","sorcery","{U}",1,varv("C"),0,
  addl={"action":"tap","count":1,"target":"untapped creature you control"},
  var=V("the tapped creature's mana value"),
  notes="Turns a creature's cost into colorless for one blue, sorcery speed, and the creature is only tapped rather than sacrificed."))
N.append(spell("Metamorphosis","sorcery","{G}",1,uni(WUBRG,0),0,
  addl={"action":"sacrifice","count":1,"target":"creature","timing":"additional cost to cast"},
  var=V("one plus the sacrificed creature's mana value","All the mana is one chosen color."),
  restr="Spend this mana only to cast creature spells.",
  notes="Restricted to creature spells, which makes it a specific engine piece rather than acceleration. All the mana is a single chosen color."))
N.append(spell("Drain Power","sorcery","{U}{U}",2,{"mode":"derived","source":"whatever the targeted player's lands produce"},0,
  var=V("the total mana the targeted player's lands produce","They choose which abilities to activate, so the colors are not yours to pick."),
  notes="Empties an opponent's lands into your pool. The target chooses which mana abilities to activate, so you cannot rely on colors, and against a tapped-out opponent it produces nothing."))

# --- enchantments that produce mana themselves ------------------------------
N.append(card("Eladamri's Vineyard","enchantment","{G}",1,False,
  [ab(fixed("G","G"),2,2,"At the beginning of each player's first main phase",True,False)],
  notes="Two green every turn for one mana, and it does the same for your opponent. Symmetric acceleration is a deckbuilding decision, not a mana one, so the file records the output and the note records who else gets it."))
N.append(card("Carnival of Souls","enchantment","{1}{B}",2,False,
  [ab(fixed("B"),1,1,"Whenever a creature enters",True,False)],
  notes="Black mana on every creature entering, yours or your opponent's, at one life each. The trigger is not optional, so in a creature-heavy game it drains you whether you want the mana or not."))
N.append(card("Iceberg","enchantment","{X}{U}{U}",2,False,
  [ab(varv("C"),0,None,"Remove an ice counter",True,False,
      var=V("one per ice counter removed","Enters with X counters, where X is what you paid on casting."))],
  [oa("activated","{3}","Put an ice counter on this enchantment.")],
  notes="Stores exactly the mana you paid into it and gives it back one at a time, so it is net zero at best and a way to bank mana across turns. Adding counters later at {3} apiece is a loss."))
N.append(card("Squandered Resources","enchantment","{B}{G}",2,False,
  [ab({"mode":"derived","source":"any mana type the sacrificed land could produce"},1,1,"Sacrifice a land",True,False,
      addl={"action":"sacrifice","count":1,"target":"land"},
      cond={"type":"controls_land"})],
  notes="Converts your board into mana one land at a time, unlimited within a turn and no tap required. Colors resolve against whatever you sacrifice, so it reads the land file rather than carrying colors of its own."))
N.append(card("Food Chain","enchantment","{2}{G}",3,False,
  [ab(uni(WUBRG,0),0,None,"Exile a creature you control",True,False,
      addl={"action":"exile","count":1,"target":"creature you control"},
      var=V("one plus the exiled creature's mana value","All the mana is one chosen color."),
      restr="Spend this mana only to cast creature spells.")],
  notes="Restricted to creature spells and net positive by one each time, which is what makes it an engine rather than a rock. Unlimited within a turn as long as creatures keep coming."))
N.append(card("Mana Cache","enchantment","{1}{R}{R}",3,False,
  [ab(varv("C"),0,None,"Remove a charge counter",True,False,
      var=V("one per charge counter removed",
            "Counters accrue at each player's end step, one per untapped land that player controls."))],
  [oa("triggered",None,"At the beginning of each player's end step, put a charge counter on this enchantment for each untapped land that player controls.")],
  notes="Rewards leaving lands untapped, which is a real cost, and any player may spend the counters on their own turn. Symmetric in a way that is easy to miss: your opponent can drain the cache you filled."))
N.append(card("Mana Echoes","enchantment","{2}{R}{R}",4,False,
  [ab(varv("C"),0,None,"Whenever a creature enters",True,False,
      var=V("the number of creatures you control sharing a type with the one that entered"))],
  notes="Colorless only, and it scales with tribal density rather than with anything the mana base does. Zero in a deck of unrelated creatures."))
N.append(card("Black Market","enchantment","{3}{B}{B}",5,False,
  [ab(varv("B"),0,None,"At the beginning of your first main phase",True,False,
      var=V("the number of charge counters","One counter per creature that has died since it entered."))],
  [oa("triggered",None,"Whenever a creature dies, put a charge counter on this enchantment.")],
  notes="Five mana that produces nothing until creatures start dying, then produces increasingly large amounts automatically. The mana arrives at your first main phase whether you can use it or not."))
N.append(card("Cadaverous Bloom","enchantment","{3}{B}{G}",5,False,
  [ab(fixed("B","B"),2,2,"Exile a card from your hand",True,False,
      addl={"action":"exile","count":1,"target":"a card from your hand"}),
   ab(fixed("G","G"),2,2,"Exile a card from your hand",True,False,
      addl={"action":"exile","count":1,"target":"a card from your hand"})],
  notes="Two cards' worth of mana per card exiled, unlimited within a turn. Recorded as two separate abilities because the printed choice is between {B}{B} and {G}{G} as pairs, never one of each."))
N.append(card("Carpet of Flowers","enchantment","{G}",1,False,
  [ab(uni(WUBRG,0),0,None,"At the beginning of each of your main phases",True,False,
      var=V("the number of Islands target opponent controls",
            "Zero against a deck with no Islands. All the mana is one chosen color."),
      avail={"pattern":"once_each_turn","reason":"Only if you have not already added mana with it this turn."})],
  notes="A sideboard card by design: enormous against blue and completely dead otherwise. Amount 0 is the honest default because in most matchups that is exactly what it makes."))

# --- global effects, permanent ----------------------------------------------
GL=[
 ("Wild Growth","{G}",1,"the enchanted land","adds an additional {G} whenever it is tapped for mana","extra_mana_on_tap",
  "Makes no mana itself; it upgrades one land. In source-counting terms the enchanted land becomes a green source in addition to whatever it already was, which is why this cannot be counted as a card-level green source without knowing what it is attached to."),
 ("Fertile Ground","{1}{G}",2,"the enchanted land","adds an additional one mana of any color whenever it is tapped for mana","extra_mana_on_tap",
  "See Wild Growth, with the extra mana being any color, which makes it fixing as well as ramp."),
 ("Overgrowth","{2}{G}",3,"the enchanted land","adds an additional {G}{G} whenever it is tapped for mana","extra_mana_on_tap",
  "Two extra green per tap. Three mana invested into a single land, so it is also two cards lost to one removal spell."),
 ("Elvish Guidance","{2}{G}",3,"the enchanted land","adds an additional {G} for each Elf on the battlefield whenever it is tapped for mana","extra_mana_on_tap",
  "Scales with Elves rather than with lands, and counts every Elf in play including your opponent's."),
 ("Vernal Bloom","{3}{G}",4,"every Forest","adds an additional {G} whenever it is tapped for mana","extra_mana_on_tap",
  "Symmetric and keyed to the Forest land type, so it helps your opponent's Forests too and does nothing for green lands that lack the type."),
 ("Mana Flare","{2}{R}",3,"every land, for every player","adds an additional one mana of any type that land produced whenever it is tapped for mana","extra_mana_on_tap",
  "Doubles every land in the game for both players. Whoever untaps into it first gets the most out of it, which is a deckbuilding argument rather than a mana one."),
 ("Overabundance","{1}{R}{G}",3,"every land, for every player","adds an additional one mana of any type that land produced whenever it is tapped for mana, and deals 1 damage to that player","extra_mana_on_tap",
  "Mana Flare with a life cost attached to every activation, for both players. The damage is not optional."),
 ("Mirari's Wake","{3}{G}{W}",5,"every land you control","adds an additional one mana of any type that land produced whenever you tap it for mana","extra_mana_on_tap",
  "One-sided Mana Flare at five mana. Doubles your entire mana base rather than a single land, so its effect on any source count is multiplicative and cannot be expressed as a number of sources."),
 ("Snowfall","{2}{U}",3,"every Island","may add an additional {U}, or {U}{U} instead if the Island is snow","extra_mana_on_tap",
  "The mana can only pay cumulative upkeep costs, including this card's own, so it is close to self-sustaining and useless for casting anything. Note the snow clause is live in this format because the snow basics are legal."),
 ("Winter's Night","{R}{G}{W}",3,"every snow land","adds an additional one mana of any type that land produced, and that land does not untap during its controller's next untap step","extra_mana_on_tap",
  "World enchantment, symmetric, and it charges every extra mana against the land's next untap, so it converts two turns of a land into one bigger turn. Only relevant to decks running the snow basics."),
 ("Chaos Moon","{3}{R}",4,"every Mountain, depending on the parity of permanents in play","adds an additional {R} on odd turns and produces only colorless on even ones","conditional_type_or_output_change",
  "Flips between helping and hurting based on a permanent count that changes constantly and that neither player fully controls. Recorded honestly rather than resolved: no calculator should model this as a stable effect."),
 ("Blanket of Night","{1}{B}{B}",3,"every land in play","is a Swamp in addition to its other land types","type_change",
  "Changes land types rather than mana, which makes it the single most disruptive card in this file for anything reading the land data. Every land becomes a Swamp, so the Torment Tainted cycle switches on for both players, Cabal Coffers counts every land in play, and the Onslaught fetchlands can find any land with the Swamp type. Symmetric."),
 ("Multani's Harmony","{G}",1,"the enchanted creature","gains \"{T}: Add one mana of any color\"","granted_ability",
  "Turns any creature into a Birds of Paradise. Subject to summoning sickness on the creature receiving it."),
]
for name,mc,cmc,applies,grants,kind,notes in GL:
    N.append(card(name,"enchantment",mc,cmc,False,[],glob=G(applies,grants,kind),notes=notes))

N.append(card("Overlaid Terrain","enchantment","{2}{G}{G}",4,False,[],
  entry={"action":"sacrifice","count":"all","target":"lands you control","timing":"replacement","if_unmet":None},
  glob=G("every land you control","gains \"{T}: Add two mana of any one color\"","granted_ability"),
  notes="Sacrifices your entire mana base as it enters and then doubles whatever you rebuild, so it is a four-mana reset with a huge payoff and no floor. entry_cost carries the sacrifice because it happens as a replacement on entering, not as a trigger you can respond to."))

# --- global effects, temporary ----------------------------------------------
N.append(card("Divergent Growth","instant","{G}",1,True,[],
  glob=G("lands you control","gain \"{T}: Add one mana of any color\"","granted_ability","until end of turn"),
  notes="One turn of perfect fixing for one green. It grants an ability rather than producing mana, so its value depends entirely on how many untapped lands you have when it resolves."))
N.append(card("Rain of Filth","instant","{B}",1,True,[],
  glob=G("lands you control","gain \"Sacrifice this land: Add {B}\"","granted_ability","until end of turn"),
  notes="Converts your whole mana base into black in a single turn at the cost of the lands themselves. A combo card, and one where counting sources is the wrong question entirely."))
N.append(card("Bubbling Muck","sorcery","{B}",1,True,[],
  glob=G("every Swamp, for every player","adds an additional {B} whenever it is tapped for mana","extra_mana_on_tap","until end of turn"),
  notes="A one-turn High Tide for Swamps, symmetric but sorcery speed so in practice only you benefit. Keyed to the Swamp land type, which Blanket of Night can hand to every land in play."))

d=json.load(open("data/premodern_nonlands.json"))
for c in d:
    if c["global_effect"] and "kind" not in c["global_effect"]:
        g=c["global_effect"]
        c["global_effect"]=G(g["applies_to"],g["grants"],"granted_ability","permanent",g.get("active_zone","battlefield"))
have={c["name"] for c in d}
assert not (have & {c["name"] for c in N}), sorted(have & {c["name"] for c in N})
d.extend(N)
ORDER=["name","kind","mana_cost","cmc","enters_tapped","summoning_sick","one_shot",
       "entry_cost","total_activations","abilities","other_abilities","global_effect","notes"]
d=[{k:c[k] for k in ORDER} for c in d]
json.dump(d,open("data/premodern_nonlands.json","w"),indent=2)
print("added",len(N),"| total",len(d))
