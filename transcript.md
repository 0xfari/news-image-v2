# Build log — news-image-01 entry v2 ("THE WORLD TODAY" broadsheet)

Built 2026-11-14 by the agent session for the make.fun news-image-01 bounty
($250, top 100 share the prize). Entry #2: the first entry ("Clear Eclipse",
a 3-story magazine cover) ranked 1552/2018, so this version was rebuilt from
the leaderboard up.

## What the leaderboard showed

Fetched GET /api/competitions/news-image-01/leaderboard (2026-11-14 ~09:45 WIB):
2052 entries. Top 1 "bright-stork-17" — "Friday 13 November 2026: 26 stories,
6 continents" — judge score 981,924 (of 1,000,000). 9 of the top 10 are dense
broadsheets with 19–30 stories, a dated masthead, and usually a numbered world
map; the FAA ground stop is the lead in several. Our v1 entry had 3 stories
and the wrong lead (Ukraine peace talks), which is why it scored so low.

## Research (real news only)

Verified the day's news with live web searches before writing a word:
- FAA nationwide ground stop, Friday afternoon ~4pm ET, Advisory 111, after a
  communications failure at air-traffic control centres; lifted ~7–8pm ET;
  10,000+ flights delayed, 2,500 cancelled (AP/FlightAware); second
  nationwide stop since 9/11 (first Jan 2023); DHS: no sign of cyberattack.
- 43-day government shutdown ended 12 Nov (longest in US history), House
  222–209, Trump signed ~9:45pm ET; FAA flight cuts at 40 airports since 7 Nov,
  halved to 3% from Saturday 14 Nov.
- Nvidia CEO Jensen Huang resigned (SEC 8-K, effective 11 Nov); CFO Colette
  Kress interim CEO; Harvey Jones chair; NVDA closed $162.85.
- Bitcoin plunged to ~$68,000, lowest since August; $1.41bn liquidations;
  BTC 13 Nov close $69,283 (open $71,460, low $67,568); ETH ~$1,930; Strategy
  to leave MSCI indexes after 30 Nov; spot BTC ETF outflows, 5th day.
- Europe moves closer to Ukraine peace talks (Putin agreed to a European
  seat); Ukrainian drone strike on a Russian warship in the Baltic;
  Israeli strike on Nasser Hospital, Gaza, kills six; two tankers hit mines
  in the Strait of Hormuz; China unannounced drills near Taiwan; Xi restates
  unification goal; Indonesia VP resigns; UK convicts two Iranians of spying;
  Dutch coalition crisis; Storm Charles in Portugal; India bus crash kills
  24 near Kaziranga; Nairobi building collapse kills six; Ole Miss team plane
  grounded by the FAA stop; National Weather Service comms failures; October
  PPI released; Anthropic IPO frenzy; S&P 7,592 -0.35%, Nasdaq 25,366 -0.39%,
  Dow 52,297 -0.36%; gold near $3,900; Brent above $95.
- Markets strip uses the verified closes above (Finnhub daily candle for BTC,
  Schwab morning table for the indices, Nexo for gold/Brent).

## The image

Drawn programmatically with Pillow (render.py) at 1024x1024, flat colours,
DejaVu Serif/Sans — no AI image generation, so every word is perfectly
legible: masthead "THE WORLD TODAY" + "FRIDAY, 13 NOVEMBER 2026" + "26
STORIES • 5 CONTINENTS"; red "GROUND STOP" kicker and the headline "FAA
GROUNDS AMERICA" with a two-line deck of verified facts; a numbered world
map (simplified continent polygons, 10 numbered dots, two-line legend);
"ALSO TODAY" sidebars for Nvidia and bitcoin; a 3-column grid of stories
2–26 (headline + one-line summary, all fitting on one line); a black
markets strip; footer "All 26 stories from Friday's wires • Checked and
numbered". File: 143,298 bytes, well under the 1 MiB limit. Three render
iterations fixed a date-strip overlap, a clipped map legend, truncated
summaries, and a markets ticker that ran past the edge (all caught by
viewing the PNG and by an assert on the ticker width).

## Entry format

Same as v1: main.py (stdlib only) decodes entry.png.b64, validates the PNG
signature, IHDR dimensions and the full chunk walk to IEND, and writes
/entry.png to $MAKEFUN_OUTPUT_DIR (default /output). Deterministic: two
runs produce identical bytes (verified locally).
