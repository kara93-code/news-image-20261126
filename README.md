[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/kara93-code/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/kara93-code/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# news-image-20261126 — SPARSE experiment

One image summing up Thursday 26 November 2026's world news: 9 verified
stories only — 2 large illustrated leads, 3 medium cards, 4 one-line
briefs. An experiment against the NI25 DENSE layout (25 stories, #188,
12-0 pairwise): fewer stories, bigger and clearer, with the date line
prominent in red.

## Stories (all verified against wire reports, 26 Nov 2026 morning)

1. **Africa — Giza fuel tanker fire:** 31 killed, 21 hurt on the Cairo
   ring road above the Warraq tunnel (Reuters / CNN).
2. **Americas — Nasdaq dives 4%:** AI stocks rout Wall Street; Nvidia
   -8.6%; US plans new tariffs on 14 partners (Reuters).
3. **Middle East — Netanyahu:** judges urge prosecutors to drop the
   Case 4000 bribery charge and reconsider Case 2000 (Reuters / CNN).
4. **Europe — Poland:** plans a no-fly zone on its Ukraine border after
   Russian missiles crossed its airspace (Reuters).
5. **Asia — North Korea:** expels the Swiss envoy and orders its
   Pyongyang office shut within 48 hours (Reuters / KCNA).
6. **Global — Hera/DART:** first photos show DART left a stadium-size
   crater on asteroid Dimorphos (ESA).
7. **Asia — Bangladesh:** garment workers win a 36% pay rise, to 17,000
   taka a month (AP).
8. **Europe — Melania Trump:** helps reunite 9 more children; 43
   returned in all (White House / Reuters).
9. **Europe — Russia:** its own figures show nearly 500,000 war dead
   (BBC analysis of leaked Rosstat data).

Left out on purpose: 25 Nov stories (Shenzhou-24, BepiColombo,
Nvidia/Huang, Huawei verdict, Houthi drone on Riyadh, Cartagena
standoff) and 24 Nov stories (turkey pardon, Lukashenko offer).

## Build

`draw.py` renders `assets/entry.png` (1024x1024, Pillow, dev machine
only). `main.py` is stdlib-only and copies the asset to
`/output/entry.png`; the grader runs it with `python3 -P -s` in a bare
python:3.13 image with no Pillow and no network.

```sh
python3 draw.py
env -i TZ=UTC PYTHONHASHSEED=0 LANG=C.UTF-8 MAKEFUN_OUTPUT_DIR=out \
  python3 -P -s main.py
```
