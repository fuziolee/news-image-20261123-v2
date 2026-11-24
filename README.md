# The World in One Day — Monday, 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/fuziolee/news-image-20261123-v2/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/fuziolee/news-image-20261123-v2/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One day of world news, one picture: 37 verified stories from Monday, 23 November 2026 — 4 illustrated hero stories, 12 short reports and 21 more headlines — across 7 regions, with a UTC timeline, a world map of where it happened, and a date-check banner.

## How it renders

`main.py` is a stdlib-only Python renderer (zlib + struct PNG writer, 5x7 bitmap font). It is fully deterministic — no timestamps, no randomness — and writes a 1024x1024 `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`).

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

## What's on the page

- 4 hero stories with drawn illustration motifs (sea drones, diplomacy map, oil tanker, aid train)
- 12 short stories, 21 further headlines, 7 regions
- UTC timeline of the day, world map with 16 numbered story dots
- CLAIM badges mark one side's account, not independently confirmed facts
- Sources: AP · Reuters · BBC · UN News · The Hindu BusinessLine · ICC · AAP · PINA · The Business Standard · Sowetan · Bloomberg Government · Korea JoongAng Daily · Phys.org · Scientific Reports · Just Security · Press TV · Al Jazeera
