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

This is the v2 final version, rebuilt after Monday (UTC) closed.
The three leads: COP31 in Antalya ending with no cover decision
after a record 49 hours of overtime, with Monday's reactions —
Guterres's "deep dismay", Stiell's "fell short", Gore calling
the fossil-fuel veto "outrageous"; Belgium's national strike,
with 404 of 429 Brussels Airport flights cancelled and 50,000
people marching in Brussels; and Nvidia reinstating Jensen
Huang as CEO after President Trump's intervention, the shares
jumping 31% and adding about $950bn in a day as the Nasdaq
gained 6.5%. Reporting was checked against the wires and major
outlets of the day (among them Reuters, AP, AFP, CNN, Al
Jazeera, RTBF, Belga, Xinhua, SCMP, The Times, El País, GMA,
Haaretz, KCNA, ATP, Investopedia and USA Today).
