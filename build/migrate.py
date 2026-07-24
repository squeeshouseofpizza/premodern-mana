import json
d = json.load(open("premodern_lands.json"))
STORAGE = {"Icatian Store","Sand Silos","Bottomless Vault","Dwarven Hold","Hollow Trees"}
for c in d:
    c.setdefault("entry_cost", None)
    c.setdefault("fetches", None)
    for a in c["abilities"]:
        p, amt = a["produces"], a["amount"]
        if c["name"] in STORAGE:
            a["produces"] = {"mode": "fixed_variable", "unit": p[0]}
        elif len(p) == 1:
            a["produces"] = {"mode": "fixed", "mana": p * amt}
        else:
            assert amt == 1, (c["name"], p, amt)
            a["produces"] = {"mode": "choice", "options": p}
        a.setdefault("additional_cost", None)
        a.setdefault("variable_amount", None)
        # stable key order
        for k in ["produces","amount","net_mana","cost","additional_cost","self_sufficient",
                  "condition","sacrifices_self","variable_amount"]:
            a[k] = a.pop(k)
    for k in ["name","first_printing","supertypes","land_types","enters_tapped","entry_cost",
              "availability","total_activations","abilities","other_abilities","fetches","notes"]:
        c[k] = c.pop(k)
json.dump(d, open("premodern_lands.json","w"), indent=2)
print("migrated", len(d))
akeys={tuple(a.keys()) for c in d for a in c["abilities"]}
print("ability key sets:", len(akeys))
print(json.dumps(d[0]["abilities"][0]))
print(json.dumps([a["produces"] for a in d[5]["abilities"]]))
print(json.dumps([a["produces"] for a in d[10]["abilities"]]))
