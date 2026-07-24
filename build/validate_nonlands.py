"""Run against data/premodern_nonlands.json after any change."""
import json, sys
d=json.load(open("data/premodern_nonlands.json"))
raw={r["name"] for r in json.load(open("data/nonlands_raw_slim.json"))}
banned=set(json.load(open("data/banned.json")))
def check(c,m):
    if not c: print("FAIL:",m); sys.exit(1)

check(len(d)==155,"expected 155, got %d"%len(d))
check(len({c["name"] for c in d})==len(d),"duplicate names")
check({c["name"] for c in d}==raw,"names do not match the Scryfall pull")
check(not ({c["name"] for c in d} & banned),"a banned card is in the file")
check(len({tuple(c.keys()) for c in d})==1,"top-level key sets differ")
check(len({tuple(a.keys()) for c in d for a in c["abilities"]})==1,"ability key sets differ")

for c in d:
    for a in c["abilities"]:
        p=a["produces"]; n=c["name"]
        if p["mode"]=="fixed": check(len(p["mana"])==a["amount"],"%s: fixed list vs amount"%n)
        if p["mode"]=="choice": check(a["amount"]==1,"%s: choice must be 1"%n)
        if a["self_sufficient"] and a["net_mana"] is not None:
            check(a["net_mana"]==a["amount"],"%s: self_sufficient but pays mana"%n)
        if a["variable_amount"]: check(a["net_mana"] is None,"%s: variable must have null net"%n)
        if a["zone"]=="stack": check(c["one_shot"],"%s: stack ability must be one_shot"%n)
    # a creature whose mana ability taps must be marked summoning sick
    if c["kind"]=="creature":
        taps=any(a["requires_tap"] and a["zone"]=="battlefield" for a in c["abilities"])
        check(taps==c["summoning_sick"],"%s: summoning_sick disagrees with requires_tap"%c["name"])
    # a card with no mana ability must be doing something else
    if not c["abilities"]:
        check(c["global_effect"] or c["other_abilities"],"%s: no abilities and no effect"%c["name"])
print("OK: 155 nonlands, all invariants hold, none banned")
