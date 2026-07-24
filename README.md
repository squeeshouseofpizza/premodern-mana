# Premodern mana sources

A hand-verified classification of every land legal in Premodern, and a calculator that
uses it.

Premodern's card pool is frozen at Fourth Edition through Scourge, so this data does not
rotate and is not maintained on a schedule. It is either right or it has a bug.

## Why it exists

Deriving land behaviour from oracle text by pattern matching produces a new bug on every
deck you test. Some examples this data set handles correctly:

- **Skycloud Expanse** is `{1}, {T}: Add {W}{U}`. Anything reading mana symbols records a
  white-blue source. It produces nothing on its own and can never be your first coloured
  mana.
- **Fetchlands** find basics, because Premodern has no dual lands. Their colours are a
  property of your decklist, not of the card.
- **Wasteland and Barbarian Ring** both sacrifice themselves. One is cracked early and one
  is held all game.
- **Ancient Tomb** produces two colourless, not one.
- **Gemstone Mine** has three uses, not unlimited.
- **The Tainted cycle** only produces colour if you control a Swamp.
- **Riftstone Portal** changes what every other land in your deck does, from the graveyard.

Every card was read individually and the reasoning is in its `notes` field.

## Layout

```
index.html                        the calculator, served by GitHub Pages
fourthwall-embed.html             snippet to paste into a Fourthwall custom HTML section
data/premodern_lands.json         199 lands, the verified data
data/premodern_lands_heuristics.json   deck-profile opinions, kept separate on purpose
data/lands_raw.json               the Scryfall pull everything was built from
build/batch1.py ... batch9.py     the scripts that assemble the data file
build/heur.py                     generates the heuristics file
SCHEMA.md                         every field, all five produces modes, the invariants
```

`data/premodern_lands.json` is the source of truth. The scripts in `build/` are the record
of how it was assembled and how each field came to exist: `batch3.py` onwards each append
one set's worth of cards and, where a batch forced a schema change, perform the migration
on everything already in the file. The first 45 cards predate that approach and were
written directly, so rerunning the scripts from scratch will not reproduce the file.

Keep them anyway. They are the practical way to make a bulk change: write the
transformation, run it against the current file, and rerun the validator, which enforces
every invariant in SCHEMA.md and fails loudly rather than shipping a broken build.

## Publishing

1. Push the repo.
2. Settings, Pages, deploy from branch, root of `main`.
3. Confirm `https://USERNAME.github.io/REPO/` loads and the colour tiles populate. If the
   page reports that card data did not load, `data/premodern_lands.json` is not where the
   page expects it.
4. Put the contents of `fourthwall-embed.html` into a Fourthwall custom HTML section and
   replace the placeholder URL.

The Fourthwall section is an iframe on purpose. It stays far under Fourthwall's 25,000
character limit on custom HTML, it cannot collide with the site's own CSS, and every later
change ships by pushing here instead of re-pasting markup.

## What the calculator does

Paste a decklist. Every spell is checked against the number of coloured sources it needs to be
cast on curve, using Frank Karsten's 2022 tables interpolated to your actual land count, with his
gold-card rule applied to multicolour spells and turn-one requirements measured against untapped
sources only. Results are sorted worst first, so the card your mana base actually fails is at the
top.

Sources are counted from the data files rather than from mana symbols. Fetchlands resolve against
the rest of your decklist, since the format has no duals. Lands whose symbols overstate them are
excluded from the turn-one count and listed with the reason. Nonland mana is included at Karsten's
own weightings: dorks at half a source, artifact accelerants at three quarters, Mox Diamond at one,
and one-shot effects at zero because a ritual multiplies mana you already have rather than making a
colour available.

Two conveniences worth knowing. A line reading `Sideboard` separates the sideboard, which is then
marked but still checked. And a card you never hard-cast can carry the cost you actually pay,
written after the name.

That cost may be paid in lands rather than mana, which matters in this format. Gush free-cast
wants two Islands on the battlefield, not two blue sources, and a Skycloud Expanse is blue and is
not an Island. Write a land type as its own pip and it is counted against the lands that carry
that type, plus any fetchland that can find one: `4 Gush {Island}{Island}`,
`4 Snuff Out {Swamp}`, `4 Daze {Island}`.

It does not simulate. Source counts checked against published targets, Monte Carlo later.

## Building the card cost table

The per-spell check needs the mana cost of every legal card. Open `build/fetch-card-costs.html`
in a browser and press the button: it pages through Scryfall, respects the rate limit, and saves
`premodern_card_costs.json`. Put that file in `data/`. Run it once, since the card pool is frozen.

Without it the page still counts sources correctly and says plainly that costs are unavailable.

## Two files, on purpose

`premodern_lands.json` contains only what the card and the rulings say. Anything that
depends on what a deck is trying to do lives in `premodern_lands_heuristics.json`, which
is generated by a script that asserts its scope against the data file so the two cannot
drift apart. Gaea's Cradle taps for green equal to your creature count; that is a fact and
it is in the data file. Assuming that number is two in practice is an opinion and it is in
the other one. If they ever disagree, the data file is right.
