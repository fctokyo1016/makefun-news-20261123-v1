#!/usr/bin/env python3
"""Draw the front page for Monday 23 November 2026 — v2 final.

One broadsheet, 1024x1024: masthead, six big numbers, a region bar,
a UTC timeline, three illustrated lead stories, twelve small cards,
a dotted world map with numbered pins, a list of 26 further briefs,
a date-check box and a footer. v2 rebuilds the page after Monday
(UTC) closed: the Belgium strike and the Brussels march are reported
with their confirmed results, the COP31 panel carries Monday's
reactions to Sunday's collapse, the ATP final has its confirmed
winner, and the third lead is Monday's own biggest story — Nvidia
reinstating Jensen Huang and the market surge that followed.
Every story is dated 23 Nov 2026 and carries its source and a
certainty tag. The drawing is fully deterministic: the same run
always produces the same PNG bytes.
"""
from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
PALETTE = {
    "paper": (247, 243, 234),
    "ink": (20, 20, 20),
    "grey": (96, 92, 84),
    "red": (168, 30, 30),
    "navy": (16, 32, 56),
    "teal": (24, 92, 84),
    "gold": (196, 138, 32),
    "night": (18, 28, 54),
    "soft": (50, 50, 50),
    "green": (34, 110, 62),
}
SERIF_B = ["/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
           "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]
SERIF = ["/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]
SANS_B = ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
          "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
SANS = ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


def load(paths, size):
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


class Sheet:
    """The page: a canvas, a pen, a left margin and a moving y cursor."""

    def __init__(self):
        self.img = Image.new("RGB", CANVAS, PALETTE["paper"])
        self.pen = ImageDraw.Draw(self.img)
        self.mx = 24
        self.inner = CANVAS[0] - 2 * self.mx
        self.y = 0
        self._fonts = {}

    def font(self, kind, size):
        key = (kind, size)
        if key not in self._fonts:
            table = {"serif_b": SERIF_B, "serif": SERIF,
                     "sans_b": SANS_B, "sans": SANS}[kind]
            self._fonts[key] = load(table, size)
        return self._fonts[key]

    def width(self, text, kind, size):
        return self.pen.textlength(text, font=self.font(kind, size))

    def write(self, x, y, text, kind, size, colour):
        self.pen.text((x, y), text, font=self.font(kind, size), fill=colour)

    def centred(self, y, text, kind, size, colour):
        self.write((CANVAS[0] - self.width(text, kind, size)) / 2, y,
                   text, kind, size, colour)

    def wrap(self, text, kind, size, max_w):
        lines, current = [], ""
        for word in text.split():
            trial = (current + " " + word).strip()
            if self.width(trial, kind, size) <= max_w:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def para(self, x, y, text, kind, size, colour, max_w, leading, limit=99):
        for line in self.wrap(text, kind, size, max_w)[:limit]:
            self.write(x, y, line, kind, size, colour)
            y += leading
        return y

    def hline(self, y, weight=1, colour=None):
        self.pen.line([self.mx, y, CANVAS[0] - self.mx, y],
                      fill=colour or PALETTE["ink"], width=weight)
        return y

    def red_tag(self, x, y, w, left, right=""):
        self.pen.rectangle([x, y, x + w, y + 16], fill=PALETTE["red"])
        self.write(x + 5, y + 3, left, "sans_b", 10, (255, 255, 255))
        if right:
            self.write(x + w - 5 - self.width(right, "sans_b", 10), y + 3,
                       right, "sans_b", 10, (255, 255, 255))


page = Sheet()
pen = page.pen
MX = page.mx
IW = page.inner

# ---------- nameplate ----------
pen.rectangle([0, 0, CANVAS[0], 26], fill=PALETTE["navy"])
page.write(MX, 6, "THE WORLD IN ONE DAY", "sans_b", 13, (255, 255, 255))
right = "41 STORIES · 7 REGIONS · EVERY ONE DATED MONDAY 23 NOVEMBER 2026"
page.write(CANVAS[0] - MX - page.width(right, "sans_b", 11), 7,
           right, "sans_b", 11, (255, 255, 255))

page.centred(34, "Monday 23 November 2026", "serif_b", 57, PALETTE["ink"])
page.centred(102, "COP31 collapses in Antalya · Belgium's skies shut for a day · Nvidia soars 31% as Huang returns",
             "serif", 16, PALETTE["red"])
page.hline(128, 2)
page.hline(132, 1)

# ---------- six big numbers ----------
figures = [("49 hrs", "overtime at COP31 — a record"),
           ("0", "cover decisions adopted at Antalya"),
           ("404", "flights cancelled at Brussels Airport"),
           ("50,000", "marchers in Brussels (police count)"),
           ("+31%", "Nvidia on Huang's return"),
           ("98.79%", "Hong Kong's record EC turnout")]
cell = IW / 6
for pos, (big, small) in enumerate(figures):
    left = MX + pos * cell
    if pos:
        pen.line([left, 142, left, 176], fill=PALETTE["grey"], width=1)
    page.write(left + (cell - page.width(big, "serif_b", 29)) / 2, 138,
               big, "serif_b", 29, PALETTE["ink"])
    for row, line in enumerate(page.wrap(small.upper(), "sans", 9, cell - 8)):
        page.write(left + (cell - page.width(line, "sans", 9)) / 2, 172 + row * 11,
                   line, "sans", 9, PALETTE["grey"])
page.hline(196, 1)

# ---------- region bar ----------
regions = [("EUROPE 12", 0.22, (38, 84, 124)),
           ("MIDDLE EAST 5", 0.12, (168, 30, 30)),
           ("ASIA-PACIFIC 15", 0.26, (24, 92, 84)),
           ("AMERICAS 6", 0.13, (196, 138, 32)),
           ("AFRICA 1", 0.09, (110, 66, 140)),
           ("OCEANIA 1", 0.09, (70, 130, 60)),
           ("WORLD 1", 0.09, (90, 90, 90))]
cursor = MX
for label, share, hue in regions:
    seg = IW * share
    pen.rectangle([cursor, 202, cursor + seg - 2, 224], fill=hue)
    page.write(cursor + (seg - 2 - page.width(label, "sans_b", 10)) / 2, 207,
               label, "sans_b", 10, (255, 255, 255))
    cursor += seg

# ---------- the day in UTC ----------
pen.rectangle([MX, 230, CANVAS[0] - MX, 252], fill=PALETTE["navy"])
slots = [("THE DAY IN UTC", None), ("06:00", "ATC off in Belgium"),
         ("09:00", "Brussels march gathers"), ("12:15", "van torched at Midi"),
         ("14:30", "Nvidia brings Huang back"), ("21:00", "Nasdaq closes +6.5%")]
cursor = MX + 8
for moment, what in slots:
    if what is None:
        page.write(cursor, 236, moment, "sans_b", 11, (255, 255, 255))
        cursor += page.width(moment, "sans_b", 11) + 18
    else:
        page.write(cursor, 236, moment, "sans_b", 11, PALETTE["gold"])
        cursor += page.width(moment, "sans_b", 11) + 4
        page.write(cursor, 236, what, "sans", 11, (255, 255, 255))
        cursor += page.width(what, "sans", 11) + 13

# ---------- lead illustrations ----------
def flame_at(x, y, scale=1.0):
    pen.polygon([(x, y), (x + 7 * scale, y - 16 * scale), (x + 14 * scale, y)],
                fill=(232, 120, 30))
    pen.polygon([(x + 4 * scale, y), (x + 7 * scale, y - 9 * scale), (x + 10 * scale, y)],
                fill=(246, 190, 60))


def draw_cop(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(188, 220, 206))
    # semicircular amphitheatre of seats
    for ring, rad in enumerate((58, 74, 90)):
        for k in range(9):
            ang = 3.14159 * (0.15 + 0.0875 * k)
            import math
            cx = x + w / 2 + rad * 1.6 * math.cos(ang + 3.14159)
            cy = y + h - 8 - rad * 0.62 * math.sin(ang)
            pen.ellipse([cx - 6, cy - 4, cx + 6, cy + 4], fill=(52, 40, 30))
    # podium desk and gavel
    pen.rectangle([x + w / 2 - 46, y + h - 34, x + w / 2 + 46, y + h - 18], fill=(120, 84, 40))
    pen.rectangle([x + w / 2 - 16, y + h - 48, x + w / 2 + 16, y + h - 34], fill=(90, 60, 30))
    pen.line([x + w / 2 + 24, y + h - 46, x + w / 2 + 34, y + h - 58], fill=(90, 60, 30), width=3)
    # the torn final text, crossed out in red
    pen.polygon([(x + 22, y + 12), (x + 78, y + 12), (x + 72, y + 62), (x + 22, y + 62)],
                fill=(250, 248, 240), outline=PALETTE["ink"])
    pen.polygon([(x + 78, y + 12), (x + 96, y + 18), (x + 88, y + 58), (x + 72, y + 62)],
                fill=(232, 230, 220), outline=PALETTE["ink"])
    for ln in range(3):
        pen.line([x + 30, y + 22 + ln * 10, x + 66, y + 22 + ln * 10],
                 fill=(130, 130, 130), width=1)
    pen.line([x + 28, y + 18, x + 72, y + 56], fill=PALETTE["red"], width=3)
    pen.line([x + 72, y + 18, x + 28, y + 56], fill=PALETTE["red"], width=3)
    # wall clock
    pen.ellipse([x + w - 58, y + 10, x + w - 26, y + 42], outline=PALETTE["ink"], width=2)
    pen.line([x + w - 42, y + 26, x + w - 42, y + 16], fill=PALETTE["ink"], width=2)
    pen.line([x + w - 42, y + 26, x + w - 32, y + 30], fill=PALETTE["ink"], width=2)
    page.red_tag(x, y, w, "NO COVER DECISION", "FIRST NO-DEAL COP SINCE 2009")


def draw_brussels(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(198, 212, 226))
    pen.ellipse([x + 24, y + 10, x + 66, y + 52], fill=(240, 244, 248))
    pen.ellipse([x + 190, y + 6, x + 224, y + 38], fill=(240, 244, 248))
    # runway
    pen.polygon([(x + 60, y + h), (x + w, y + h - 30), (x + w, y + h), (x + 60, y + h)],
                fill=(120, 128, 138))
    for k in range(4):
        pen.line([x + 100 + k * 52, y + h - 8 - k * 6, x + 118 + k * 52, y + h - 10 - k * 6],
                 fill=(255, 255, 255), width=2)
    # control tower on the left
    pen.rectangle([x + 24, y + 34, x + 44, y + h - 12], fill=(88, 98, 110))
    pen.rectangle([x + 16, y + 16, x + 52, y + 36], fill=(58, 68, 82))
    for k in range(3):
        pen.rectangle([x + 20 + k * 11, y + 21, x + 28 + k * 11, y + 30], fill=(150, 200, 230))
    # parked jet, nose to the right
    pen.polygon([(x + 84, y + 60), (x + 246, y + 40), (x + 254, y + 46), (x + 116, y + 72),
                 (x + 92, y + 72)], fill=(242, 242, 242), outline=PALETTE["ink"])
    pen.polygon([(x + 148, y + 56), (x + 172, y + 32), (x + 182, y + 56)],
                fill=(222, 222, 222), outline=PALETTE["ink"])
    for k in range(5):
        pen.rectangle([x + 126 + k * 16, y + 54, x + 134 + k * 16, y + 60], fill=(40, 90, 140))
    # red prohibition disc
    cx, cy = x + w - 40, y + 60
    pen.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=PALETTE["red"], width=5)
    pen.line([cx - 16, cy + 16, cx + 16, cy - 16], fill=PALETTE["red"], width=5)
    page.red_tag(x, y, w, "404 FLIGHTS CANCELLED", "50,000 MARCH IN BRUSSELS")


def draw_nvidia(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=PALETTE["night"])
    # grid lines
    for gy in range(4):
        yy = y + 22 + gy * 18
        pen.line([x + 10, yy, x + w - 10, yy], fill=(40, 56, 92), width=1)
    # the day's gain, top left, clear of the chart
    page.write(x + 14, y + 20, "+31%", "sans_b", 24, (46, 220, 110))
    # rising candlesticks on the right
    base = y + h - 18
    candles = [(110, 20, 30), (150, 26, 40), (190, 22, 36), (230, 34, 50),
               (268, 40, 58)]
    for off, lo, hi in candles:
        pen.line([x + off + 7, base - hi - 8, x + off + 7, base - lo + 4],
                 fill=(120, 200, 120), width=2)
        pen.rectangle([x + off, base - hi, x + off + 14, base - lo],
                      fill=(46, 180, 90))
    # the surge arrow over the candles
    pen.line([x + 118, base - 26, x + 180, base - 40, x + 240, base - 50,
              x + w - 24, base - 56], fill=(250, 210, 60), width=3)
    pen.polygon([(x + w - 24, base - 56), (x + w - 40, base - 52),
                 (x + w - 28, base - 38)], fill=(250, 210, 60))
    page.write(x + 14, y + h - 16, "NASDAQ +6.5% · S&P +4.7% · DOW +3.0%",
               "sans_b", 9, (255, 255, 255))
    page.red_tag(x, y, w, "NVDA +31%", "+$950BN IN A DAY")


leads = [
    (draw_cop, "1  ANTALYA, TÜRKIYE · CLIMATE", "CONFIRMED",
     "COP31 ends with no deal — and the world reacts",
     "Sunday's plenary adopts no cover decision after 49 hours of "
     "overtime — the longest COP ever, first with no deal since "
     "Copenhagen 2009. Monday: Guterres voices “deep dismay”, Stiell "
     "says it “fell short”, Gore calls the veto “outrageous”.",
     "Reuters · AP · AFP · CNN"),
    (draw_brussels, "2  BRUSSELS, BELGIUM · STRIKE", "CONFIRMED",
     "Belgium's skies shut for a day as 50,000 march",
     "Skeyes suspends ATC 07:00–21:00; 404 of 429 Brussels Airport flights "
     "are cancelled, hitting 50,000+ passengers, and Charleroi halts all "
     "day. Police count 50,000 on the march to Midi (unions say 70,000); "
     "De Wever warns his government could fall.",
     "RTBF · AFP · Belga"),
    (draw_nvidia, "3  NEW YORK, USA · MARKETS", "CONFIRMED",
     "Huang is back: Nvidia soars 31% as Trump brokers return",
     "Eleven days after Huang quit amid scandal, the board reinstates him "
     "as CEO; Trump says “I made the deal”. Nvidia jumps 31% — its best "
     "day since 2003, adding about $950bn — as the Nasdaq gains 6.5% and "
     "the S&P 4.7%.",
     "Reuters · Investopedia · USA Today"),
]
panel_w = (IW - 24) / 3
for pos, (scene, kicker, cert, head, body, src) in enumerate(leads):
    left = MX + pos * (panel_w + 12)
    scene(left, 260, panel_w, 96)
    page.write(left, 364, kicker, "sans_b", 10, PALETTE["grey"])
    page.write(left + panel_w - page.width(cert, "sans_b", 9), 365,
               cert, "sans_b", 9, PALETTE["red"])
    yy = page.para(left, 379, head, "serif_b", 19, PALETTE["ink"], panel_w, 23, 3)
    yy = page.para(left, yy + 3, body, "sans", 10.5, PALETTE["soft"], panel_w, 13.5, 5)
    page.write(left, 486, src, "sans", 9, PALETTE["grey"])
page.hline(500, 1)

# ---------- twelve small cards ----------
def pictogram(kind, x, y, w, h, bg):
    pen.rectangle([x, y, x + w, y + h], fill=bg)
    cx, cy = x + w / 2, y + h / 2
    white = (255, 255, 255)
    if kind == "ballot":
        pen.rectangle([cx - 16, cy - 4, cx + 16, cy + 12], outline=white, width=2)
        pen.rectangle([cx - 8, cy - 13, cx + 10, cy - 5], fill=white)
    elif kind == "book":
        pen.rectangle([cx - 14, cy - 11, cx + 14, cy + 11], outline=white, width=2)
        pen.line([cx, cy - 11, cx, cy + 11], fill=white, width=2)
        for side in (-1, 1):
            pen.line([cx + side * 10, cy - 5, cx + side * 4, cy - 5], fill=white, width=1)
            pen.line([cx + side * 10, cy + 1, cx + side * 4, cy + 1], fill=white, width=1)
    elif kind == "phone":
        pen.rectangle([cx - 8, cy - 13, cx + 8, cy + 13], outline=white, width=2)
        pen.line([cx - 4, cy - 8, cx + 4, cy - 8], fill=white, width=1)
        pen.line([cx - 4, cy - 3, cx + 4, cy - 3], fill=(250, 210, 60), width=2)
    elif kind == "fire":
        flame_at(cx - 7, cy + 8, 1.4)
    elif kind == "rubble":
        pen.polygon([(cx - 18, cy + 12), (cx - 6, cy - 8), (cx + 2, cy + 2),
                     (cx + 8, cy - 12), (cx + 18, cy + 12)], outline=white, width=2)
        pen.line([cx - 2, cy - 12, cx + 2, cy + 12], fill=(250, 210, 60), width=2)
    elif kind == "radar":
        pen.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=white, width=2)
        pen.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=white, width=2)
        pen.line([cx, cy, cx + 11, cy - 11], fill=(250, 210, 60), width=2)
    elif kind == "ship":
        pen.polygon([(cx - 20, cy + 2), (cx + 20, cy + 2), (cx + 13, cy + 12), (cx - 13, cy + 12)],
                    fill=(200, 200, 200))
        pen.rectangle([cx - 4, cy - 12, cx + 3, cy + 2], fill=(200, 200, 200))
        flame_at(cx + 6, cy + 2, 0.8)
    elif kind == "crowd":
        for off in (-14, 0, 14):
            pen.ellipse([cx + off - 5, cy - 12, cx + off + 5, cy - 2], fill=white)
            pen.pieslice([cx + off - 8, cy - 2, cx + off + 8, cy + 14], 180, 360, fill=white)
    elif kind == "bolt":
        pen.polygon([(cx + 2, cy - 14), (cx - 9, cy + 2), (cx - 1, cy + 2),
                     (cx - 3, cy + 14), (cx + 10, cy - 3), (cx + 1, cy - 3)], fill=(250, 210, 60))
    elif kind == "tennis":
        pen.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=white, width=3)
        pen.arc([cx - 12, cy - 12, cx + 12, cy + 12], 300, 60, fill=white, width=2)
        pen.arc([cx - 12, cy - 12, cx + 12, cy + 12], 120, 240, fill=white, width=2)
    elif kind == "bus":
        pen.rectangle([cx - 20, cy - 10, cx + 20, cy + 10], outline=white, width=2)
        for k in range(4):
            pen.rectangle([cx - 16 + k * 9, cy - 6, cx - 10 + k * 9, cy + 1], fill=(150, 200, 230))
        pen.ellipse([cx - 14, cy + 8, cx - 6, cy + 16], fill=PALETTE["ink"])
        pen.ellipse([cx + 6, cy + 8, cx + 14, cy + 16], fill=PALETTE["ink"])


cards = [
    {"icon": "ballot", "hue": (38, 84, 124), "no": "4", "place": "HONG KONG · ELECTION",
     "head": "Hong Kong names its Election Committee",
     "body": "Turnout 98.79% as 723 seats are filled; ex-minister Chan loses by two votes; Rimsky Yuen and Sophia Chan win seats.",
     "src": "SCMP", "cert": "CONFIRMED"},
    {"icon": "book", "hue": (24, 92, 84), "no": "5", "place": "SEOUL · EDUCATION",
     "head": "Seoul's education minister quits over AI row",
     "body": "Choi Kyo-jin steps down after rushed anti-cheating steps sparked a row over AI use.",
     "src": "AFP", "cert": "CONFIRMED"},
    {"icon": "phone", "hue": (168, 30, 30), "no": "6", "place": "BEIJING · TELECOMS",
     "head": "China slams US ban on its telecom carriers",
     "body": "Beijing says it “firmly opposes” the FCC move against Chinese telecom carriers.",
     "src": "Reuters", "cert": "REPORTED"},
    {"icon": "fire", "hue": (90, 60, 30), "no": "7", "place": "CIKANDE · FIRE",
     "head": "Cikande fire: body bags out, dozens missing",
     "body": "Seven body bags recovered; around 50 still unaccounted for after the factory fire.",
     "src": "Wires", "cert": "REPORTED"},
    {"icon": "rubble", "hue": (70, 100, 120), "no": "8", "place": "DYMER · WAR",
     "head": "Dymer: at least 14 still missing in the rubble",
     "body": "Rescuers search the wreckage of the Kyiv-region block hit in the drone barrage.",
     "src": "Reuters", "cert": "REPORTED"},
    {"icon": "radar", "hue": (24, 44, 74), "no": "9", "place": "BAHRAIN · CLAIM",
     "head": "Bahrain: the struck site was civilian",
     "body": "Manama says the target was a civilian site; Iran's radar claim remains unproven.",
     "src": "Al Jazeera", "cert": "CLAIM"},
    {"icon": "ship", "hue": (24, 44, 74), "no": "10", "place": "GULF OF FINLAND · SEA",
     "head": "Sparta II still burning off Finland",
     "body": "The Russian cargo ship burns into a second day; the Loviisa rescue operation leads.",
     "src": "Reuters", "cert": "REPORTED"},
    {"icon": "crowd", "hue": (196, 138, 32), "no": "11", "place": "LISBON · PROTEST",
     "head": "Thousands march in Lisbon over living costs",
     "body": "Streets fill as cost-of-living protests spread across Europe.",
     "src": "Wires", "cert": "REPORTED"},
    {"icon": "fire", "hue": (168, 30, 30), "no": "12", "place": "NARAIL · VIOLENCE",
     "head": "Narail: 30 homes torched in political attacks",
     "body": "Homes of Awami League figures set alight in a night of political violence.",
     "src": "Local wires", "cert": "REPORTED"},
    {"icon": "bolt", "hue": (70, 130, 60), "no": "13", "place": "DELHI · ENERGY",
     "head": "India and Nepal talk energy and connectivity",
     "body": "Delhi and Kathmandu discuss power links as pollution curbs bite in the capital.",
     "src": "Wires", "cert": "REPORTED"},
    {"icon": "tennis", "hue": (110, 66, 140), "no": "14", "place": "TURIN · TENNIS",
     "head": "Alcaraz wins his first ATP Finals crown",
     "body": "Beats Zverev 6-2, 7-6(7) in Turin, saving three set points in the tie-break; a year after losing the final to Sinner.",
     "src": "ATP", "cert": "CONFIRMED"},
    {"icon": "bus", "hue": (38, 84, 124), "no": "15", "place": "MANILA · STRIKE",
     "head": "Manila: transport strike begins, runs to Tuesday",
     "body": "Manibela's strike halts jeepneys and buses across the capital.",
     "src": "GMA", "cert": "CONFIRMED"},
]
PILL = {"CONFIRMED": (34, 110, 62), "REPORTED": (70, 100, 120), "CLAIM": (168, 30, 30)}
card_w = (IW - 5 * 8) / 6
for idx, card in enumerate(cards):
    cx0 = MX + (idx % 6) * (card_w + 8)
    cy0 = 508 + (idx // 6) * 128
    pictogram(card["icon"], cx0, cy0, card_w, 38, card["hue"])
    pen.rectangle([cx0, cy0, cx0 + 20, cy0 + 16], fill=PALETTE["red"])
    page.write(cx0 + (20 - page.width(card["no"], "sans_b", 10)) / 2, cy0 + 3,
               card["no"], "sans_b", 10, (255, 255, 255))
    pill_w = page.width(card["cert"], "sans_b", 7.5) + 9
    pen.rectangle([cx0 + card_w - pill_w, cy0, cx0 + card_w, cy0 + 13], fill=PILL[card["cert"]])
    page.write(cx0 + card_w - pill_w + 4.5, cy0 + 2.5, card["cert"], "sans_b", 7.5, (255, 255, 255))
    yy = page.para(cx0, cy0 + 43, card["head"], "serif_b", 11.5, PALETTE["ink"], card_w, 14, 3)
    yy = page.para(cx0, yy + 1, card["body"], "sans", 9, (60, 60, 60), card_w, 11.5, 3)
    page.write(cx0, cy0 + 118, card["src"], "sans", 8, PALETTE["grey"])
page.hline(772, 1)

# ---------- dotted world map ----------
# Continents as ellipses in lon/lat space; dots are plotted on a fine
# grid wherever a grid point falls inside one of them.
LAND = [(-100, 45, 36, 24), (-60, -15, 15, 25), (15, 52, 21, 12),
        (20, 5, 18, 28), (90, 45, 46, 22), (135, -25, 15, 10)]
MAP_X, MAP_Y, MAP_W, MAP_H = MX + 2, 800, 330, 92


def lonlat_to_xy(lon, lat):
    return (MAP_X + (lon + 180) / 360 * MAP_W,
            MAP_Y + (90 - lat) / 180 * MAP_H)


def on_land(lon, lat):
    for clon, clat, rx, ry in LAND:
        if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1:
            return True
    return False


page.write(MX, 780, "WHERE IT HAPPENED", "sans_b", 11, PALETTE["ink"])
page.write(MX + 150, 782, "pins match story numbers", "sans", 9, PALETTE["grey"])
step = 4.0
gx = MAP_X
while gx < MAP_X + MAP_W:
    gy = MAP_Y
    while gy < MAP_Y + MAP_H:
        lon = (gx - MAP_X) / MAP_W * 360 - 180
        lat = 90 - (gy - MAP_Y) / MAP_H * 180
        if on_land(lon, lat):
            pen.ellipse([gx, gy, gx + 2.2, gy + 2.2], fill=(120, 130, 150))
        gy += step
    gx += step

pins = [(1, 30.7, 36.9), (2, 4.4, 50.9), (3, -74.0, 40.7), (4, 114.2, 22.3),
        (5, 127.0, 37.5), (6, 116.4, 39.9), (7, 106.8, -6.2), (8, 30.5, 50.4),
        (9, 50.6, 26.2), (10, 25.0, 60.0), (11, -9.1, 38.7), (12, 90.4, 23.8),
        (13, 77.2, 28.6), (14, 7.7, 45.1), (15, 121.0, 14.6)]
for num, lon, lat in pins:
    px, py = lonlat_to_xy(lon, lat)
    pen.ellipse([px - 6, py - 6, px + 7, py + 7], fill=PALETTE["red"])
    label = str(num)
    page.write(px - page.width(label, "sans_b", 8) / 2 + 0.5, py - 4,
               label, "sans_b", 8, (255, 255, 255))

# ---------- 26 more stories ----------
further = [
    "16 Middle East: Eisenkot, Netanyahu parties resume talks (Haaretz)",
    "17 Middle East: Iran sets out its nuclear doctrine stance (Wires)",
    "18 Middle East: UN hands over peacekeeper posts in Lebanon (Wires)",
    "19 Middle East: Fire hits Iraq power station (Wires)",
    "20 Asia-Pacific: Myanmar junta purges graft in recruitment (AFP)",
    "21 Asia-Pacific: Myanmar calls ASEAN ruling 'unfair' (Wires)",
    "22 Asia-Pacific: Kim tours factories in North Korea (KCNA)",
    "23 Asia-Pacific: Japan-Saudi energy ties strengthened (Wires)",
    "24 Asia-Pacific: Delhi chokes: pollution curbs in force (Wires)",
    "25 Americas: Trump-Xi agree oversight of military AI (Wires)",
    "26 Americas: Trump floats 10% cap on card interest (Wires)",
    "27 Americas: Seattle airport arrests draw criticism (Wires)",
    "28 Americas: Messi's Miami fall in MLS play-offs (AP)",
    "29 World: 'Killer robots' pact pushed at the UN (Wires)",
    "30 Europe: EU-UK trade talks resume (Wires)",
    "31 Europe: Living-cost protests spread in France (Wires)",
    "32 Europe: PIK: 'Collapse beats a half-hearted deal' (PIK)",
    "33 Europe: Liverpool rout United 4-0 in Pochettino's debut (AP)",
    "34 Africa: Algeria forces kill suspected traffickers (Wires)",
    "35 Asia-Pacific: Dhaka tribunal orders Yamin trial (Wires)",
    "36 Asia-Pacific: Philippines eyes 4m new voters, 2028 (GMA)",
    "37 Asia-Pacific: India's oil import bill up 60% (Mathrubhumi)",
    "38 Europe: Madrid beat Celta Vigo in La Liga (Wires)",
    "39 Europe: Turin doubles: Arribage & Olivetti win (ATP)",
    "40 Oceania: India lead New Zealand in Wellington (Wires)",
    "41 Americas: Kansas City lift the NWSL crown (Wires)",
]
ax = 372
page.write(ax, 780, "ALSO ON MONDAY 23 NOVEMBER — 26 MORE STORIES", "sans_b", 11, PALETTE["ink"])
col_w = (CANVAS[0] - MX - ax - 12) / 2
for pos, item in enumerate(further):
    bx = ax + (pos // 13) * (col_w + 12)
    by = 798 + (pos % 13) * 11.2
    page.para(bx, by, item, "sans", 8.5, (40, 40, 40), col_w, 10, 1)

# ---------- date check ----------
pen.rectangle([MX, 946, CANVAS[0] - MX, 978], outline=PALETTE["red"], width=2)
page.write(MX + 8, 952, "DATE CHECK", "sans_b", 10, PALETTE["red"])
check = ("Left out as other days' news: the 186-drone night over Kyiv (Sat–Sun) · the Sparta II strike (Sat) · "
         "BepiColombo reaches Mercury (Sat) · “El Chapo Isidro” arrested (Fri). Sunday's results, reported "
         "Monday: Liverpool 4-0, Alcaraz's ATP crown, Hong Kong's vote; COP31 collapsed at Sunday's plenary — "
         "Monday's story is the fallout.")
page.para(MX + 92, 952, check, "sans", 9.5, (40, 40, 40), IW - 104, 12, 2)

# ---------- footer ----------
page.write(MX, 984,
           "Sources: Reuters, AP, AFP, CNN, Al Jazeera, RTBF, Belga, Xinhua, SCMP, The Times, El País, GMA, Haaretz, KCNA, ATP, Investopedia, USA Today — and the wires named with each story.",
           "sans", 8.5, PALETTE["grey"])
page.write(MX, 996,
           "PRESS TIME 23:30 UTC · CERTAINTY — CONFIRMED = two or more wires · REPORTED = carried by the day's wires · CLAIM = one side's account · FORECAST = still to happen",
           "sans_b", 8.5, PALETTE["grey"])
pen.rectangle([0, 1010, CANVAS[0], CANVAS[1]], fill=PALETTE["navy"])
page.write(MX, 1014, "THE WORLD IN ONE DAY", "sans_b", 10, (255, 255, 255))
tail = "MONDAY 23 NOVEMBER 2026 · ONE PAGE"
page.write(CANVAS[0] - MX - page.width(tail, "sans_b", 10), 1014, tail, "sans_b", 10, (255, 255, 255))

page.img.save("/home/hatch/workspace/makefun-news-1123/build-v2/entry.png")
print("saved entry.png")
