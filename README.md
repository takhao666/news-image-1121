# news-image-1121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/takhao666/news-image-1121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/takhao666/news-image-1121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

An entry for make.fun's `news-image-20261121` competition: one image that sums up the world's news of Saturday 21 November 2026.

`entry.png` (1024×1024, PNG) is a newspaper front page: a big
**21 NOVEMBER 2026** masthead, a lead story on Russia's overnight
barrage of Ukraine spilling into Poland, four more illustrated stories,
and an "Also today" strip. Every story on it happened or was first
reported on 21 November 2026 (in at least one time zone), and each one
is drawn with its own picture, so the day reads even at small size.
`render.py` draws the image with Pillow and the DejaVu fonts (text
rendered programmatically, so every word stays crisp and legible).
Re-run it to regenerate `entry.png`:

```sh
python3 render.py
```

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png` and verifies the copy by length and sha256, so both
grading runs write identical bytes.

## The stories

**Lead — Russia's biggest barrage hits Kyiv, and lands in Poland**
(illustrated): More than 400 drones and 110 missiles struck Ukraine
overnight, killing at least 8 and damaging three Kyiv bridges; two
Russian missiles and a suspected drone came down in Poland, which NATO
called a "grave violation". (AP / CNN / ISW, 20–21 Nov 2026)

**Markets — Stocks slide worldwide as AI sell-off deepens**
(illustrated): The S&P 500 slid into correction and Japan's Nikkei
fell 5.1% in a sharp global sell-off led by AI shares. (OneTurn daily
brief, 21 Nov 2026)

**Middle East — Trump weighs new strikes on Iran as tankers are hit**
(illustrated): Iran struck three tankers near the Strait of Hormuz as
US–Iran talks stalled, and Washington weighs another round of strikes.
(NYT / AP, 21 Nov 2026)

**Climate — COP31 in overtime as fossil fuels vanish**
(illustrated): Nearly 200 nations missed the Friday deadline in
Antalya; the new draft drops every mention of fossil fuels and a $120bn
adaptation target. (BBC / Reuters / AP, 21 Nov 2026)

**Brussels — UK and EU sign three post-Brexit deals** (illustrated):
PM Andy Burnham signs youth mobility, trade and energy agreements at a
Brussels summit. (OneTurn daily brief, 21 Nov 2026)

**Also today:** Anthropic's $2tn stock-market debut (NYT, 19 Nov
2026); Mexico detains cartel boss "El Chapo Isidro", one of the FBI's
10 most wanted (AP, 21 Nov 2026); trial pill daraxonrasib made
pancreatic tumours undetectable in 1 in 12 patients (OneTurn, 21 Nov
2026); the world court finds Myanmar guilty of genocide against the
Rohingya — the first time a state has been found guilty of genocide
(week-in-review roundup, 21 Nov 2026).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png — a 1024x1024 PNG, under 1 MiB
```

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=hvn9m3q0&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
