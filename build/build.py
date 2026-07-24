import json, collections
cards=[]
for f in ["/mnt/user-data/uploads/search.json","/mnt/user-data/uploads/search__1_.json"]:
    for c in json.load(open(f))["data"]:
        cards.append({
            "name": c["name"],
            "set": c["set"].upper(),
            "set_name": c["set_name"],
            "released": c["released_at"],
            "type_line": c.get("type_line",""),
            "oracle_text": c.get("oracle_text",""),
        })
assert len({c["name"] for c in cards})==len(cards), "dupes"
json.dump(cards, open("lands_raw.json","w"), indent=1)
print("total", len(cards))
by=collections.defaultdict(list)
for c in cards: by[(c["released"],c["set"],c["set_name"])].append(c["name"])
for k in sorted(by):
    print(f'\n{k[0][:4]} {k[1]} {k[2]} ({len(by[k])})')
    print("  " + "; ".join(sorted(by[k])))
