"""Run against data/premodern_lands.json after any change. Fails loudly."""
import json, sys
d = json.load(open("data/premodern_lands.json"))
raw = {c["name"] for c in json.load(open("data/lands_raw.json"))}
h = json.load(open("data/premodern_lands_heuristics.json"))

def check(cond, msg):
    if not cond:
        print("FAIL:", msg); sys.exit(1)

check(len(d) == 199, "expected 199 lands, got %d" % len(d))
check(len({c["name"] for c in d}) == len(d), "duplicate names")
check({c["name"] for c in d} == raw, "names do not match the Scryfall pull")
check(len({tuple(c.keys()) for c in d}) == 1, "top-level key sets differ")
check(len({tuple(a.keys()) for c in d for a in c["abilities"]}) == 1, "ability key sets differ")
check(len({tuple(a.keys()) for c in d for a in c["other_abilities"]}) == 1, "other_ability key sets differ")
check(len({tuple(c["fetches"].keys()) for c in d if c["fetches"]}) == 1, "fetches key sets differ")

for c in d:
    for a in c["abilities"]:
        p = a["produces"]
        if p["mode"] == "fixed":
            check(len(p["mana"]) == a["amount"], "%s: fixed mana list does not match amount" % c["name"])
        if p["mode"] == "choice":
            check(a["amount"] == 1, "%s: choice mode must produce exactly 1" % c["name"])
        if a["self_sufficient"] and a["net_mana"] is not None:
            check(a["net_mana"] == a["amount"], "%s: self_sufficient but pays mana" % c["name"])
        if a["variable_amount"]:
            check(a["amount"] == 0 and a["net_mana"] is None, "%s: variable amount must floor at 0" % c["name"])

def in_scope(c):
    return (c["fetches"] is not None
            or any(a["variable_amount"] for a in c["abilities"])
            or any(a["produces"]["mode"] == "derived" for a in c["abilities"]))

check({c["name"] for c in d if in_scope(c)} == {e["name"] for e in h["entries"]},
      "heuristics file scope does not match the data file")

print("OK: 199 lands, all invariants hold, heuristics in sync")
