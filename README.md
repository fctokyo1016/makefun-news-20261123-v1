[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/fctokyo1016/makefun-news-20261123-v1/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/fctokyo1016/makefun-news-20261123-v1/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# Monday 23 November 2026: the world in one day (41 stories)

This repository holds an entry for the [make.fun bounty
`news-image-20261123`](https://make.fun/bounty/news-image-20261123),
which closes Tue, Nov 25, 2026, 09:00 JST.

To run the entry: `python3 main.py`. It writes the front page to
`/output/entry.png`.

## What is in here

- `entry.png` — the finished front page: a 1024x1024 PNG, under
  1 MiB, drawn for Monday, 23 November 2026.
- `render.py` — the program that draws `entry.png` from scratch
  with Python and PIL. It is deterministic, so running it again
  reproduces the same file byte-for-byte.
- `main.py` — the entrypoint. It checks that `entry.png` is a real
  PNG under the 1 MiB cap, then copies it to `/output/entry.png`.
  It needs no network and always writes identical bytes.
- `LICENSE` — MIT.

## What the page shows

"THE WORLD IN ONE DAY" packs **41 stories** from Monday,
23 November 2026 into a single newspaper page: a masthead with
the day's three biggest stories, six headline numbers, a bar of
the seven regions, a UTC timeline, three illustrated lead
stories, twelve short cards, a dotted world map with numbered
pins, 26 one-line briefs, and a date-check box that names what
was left out because it belongs to another day.

Every item is dated to 23 November 2026 and tagged with its
source and a certainty level: CONFIRMED means two or more wires
carried it, REPORTED means the day's wires carried it, CLAIM
means it is one side's account.

The three leads: COP31 in Antalya ending with no cover decision
after a record 49 hours of overtime; Belgium's national strike
shutting air traffic control from 07:00 to 21:00, with 429
flights and about 59,500 passengers due at Brussels Airport;
and Liverpool beating Manchester United 4-0 at Anfield in
Mauricio Pochettino's first match in charge. Reporting was
checked against the wires and major outlets of the day
(among them Reuters, AP, AFP, Al Jazeera, RTBF, Xinhua, SCMP,
The Times, El País, GMA, Haaretz, KCNA and ATP).
