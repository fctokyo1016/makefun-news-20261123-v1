#!/usr/bin/env python3
"""Front page for Monday 23 November 2026 — v2, second draft.

The same broadsheet as the first v2 build, drawn again from a blank
slate: masthead, six headline numbers, a region bar, a UTC timeline,
three illustrated lead stories, twelve short cards, a dotted world
map with numbered pins, twenty-six one-line briefs, a date-check box
and a footer. The news is the confirmed Monday picture: the Belgium
strike and march with their real results, Monday's reactions to the
COP31 collapse, Alcaraz's confirmed ATP crown, and Nvidia bringing
Jensen Huang back with a 31% surge. Deterministic: rerunning this
file reproduces the same PNG bytes.
"""
import math

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
GREY = (96, 92, 84)
RED = (168, 30, 30)
NAVY = (16, 32, 56)
TEAL = (24, 92, 84)
GOLD = (196, 138, 32)
NIGHT = (18, 28, 54)
SOFT = (50, 50, 50)
GREEN = (34, 110, 62)

FONTS = {
    "serif_b": ("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"),
    "serif": ("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),
    "sans_b": ("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
               "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    "sans": ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
}


def pick(kind, size):
    for path in FONTS[kind]:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


class Broadsheet:
    """A 1024x1024 newspaper page with a pen and a left margin."""

    def __init__(self):
        self.canvas = Image.new("RGB", (SIZE, SIZE), PAPER)
        self.pen = ImageDraw.Draw(self.canvas)
        self.margin = 24
        self.span = SIZE - 2 * self.margin
        self.cache = {}

    def f(self, kind, size):
        key = (kind, size)
        if key not in self.cache:
            self.cache[key] = pick(kind, size)
        return self.cache[key]

    def tw(self, text, kind, size):
        return self.pen.textlength(text, font=self.f(kind, size))

    def put(self, x, y, text, kind, size, colour):
        self.pen.text((x, y), text, font=self.f(kind, size), fill=colour)

    def mid(self, y, text, kind, size, colour):
        self.put((SIZE - self.tw(text, kind, size)) / 2, y, text, kind, size, colour)

    def split(self, text, kind, size, width):
        lines, current = [], ""
        for word in text.split():
            trial = (current + " " + word).strip()
            if self.tw(trial, kind, size) <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def block(self, x, y, text, kind, size, colour, width, gap, limit=99):
        for line in self.split(text, kind, size, width)[:limit]:
            self.put(x, y, line, kind, size, colour)
            y += gap
        return y

    def bar(self, y, weight=1, colour=None):
        self.pen.line((self.margin, y, SIZE - self.margin, y),
                      fill=colour or INK, width=weight)

    def box(self, x, y, w, h, fill):
        self.pen.rectangle((x, y, x + w, y + h), fill=fill)

    def flag(self, x, y, w, left, right=""):
        self.box(x, y, w, 16, RED)
        self.put(x + 5, y + 3, left, "sans_b", 10, (255, 255, 255))
        if right:
            self.put(x + w - 5 - self.tw(right, "sans_b", 10), y + 3,
                     right, "sans_b", 10, (255, 255, 255))


sheet = Broadsheet()
draw = sheet.pen
M = sheet.margin
SPAN = sheet.span

# ---------- nameplate ----------
draw.rectangle((0, 0, SIZE, 26), fill=NAVY)
sheet.put(M, 6, "THE WORLD IN ONE DAY", "sans_b", 13, (255, 255, 255))
strap = "41 STORIES · 7 REGIONS · EVERY ONE DATED MONDAY 23 NOVEMBER 2026"
sheet.put(SIZE - M - sheet.tw(strap, "sans_b", 11), 7, strap, "sans_b", 11, (255, 255, 255))

sheet.mid(34, "Monday 23 November 2026", "serif_b", 57, INK)
sheet.mid(102, "COP31 collapses in Antalya · Belgium's skies shut for a day · Nvidia soars 31% as Huang returns",
          "serif", 16, RED)
sheet.bar(128, 2)
sheet.bar(132, 1)

# ---------- six big numbers ----------
STATS = [("49 hrs", "overtime at COP31 — a record"),
         ("0", "cover decisions adopted at Antalya"),
         ("404", "flights cancelled at Brussels Airport"),
         ("50,000", "marchers in Brussels (police count)"),
         ("+31%", "Nvidia on Huang's return"),
         ("98.79%", "Hong Kong's record EC turnout")]
cell = SPAN / 6
for i, (big, small) in enumerate(STATS):
    left = M + i * cell
    if i:
        draw.line((left, 142, left, 176), fill=GREY, width=1)
    sheet.put(left + (cell - sheet.tw(big, "serif_b", 29)) / 2, 138,
              big, "serif_b", 29, INK)
    for row, line in enumerate(sheet.split(small.upper(), "sans", 9, cell - 8)):
        sheet.put(left + (cell - sheet.tw(line, "sans", 9)) / 2, 172 + row * 11,
                  line, "sans", 9, GREY)
sheet.bar(196, 1)

# ---------- region bar ----------
REGIONS = [("EUROPE 12", 0.22, (38, 84, 124)),
           ("MIDDLE EAST 5", 0.12, (168, 30, 30)),
           ("ASIA-PACIFIC 15", 0.26, (24, 92, 84)),
           ("AMERICAS 6", 0.13, (196, 138, 32)),
           ("AFRICA 1", 0.09, (110, 66, 140)),
           ("OCEANIA 1", 0.09, (70, 130, 60)),
           ("WORLD 1", 0.09, (90, 90, 90))]
x = M
for label, frac, hue in REGIONS:
    seg = SPAN * frac
    draw.rectangle((x, 202, x + seg - 2, 224), fill=hue)
    sheet.put(x + (seg - 2 - sheet.tw(label, "sans_b", 10)) / 2, 207,
              label, "sans_b", 10, (255, 255, 255))
    x += seg

# ---------- the day in UTC ----------
draw.rectangle((M, 230, SIZE - M, 252), fill=NAVY)
SLOTS = [("THE DAY IN UTC", None), ("06:00", "ATC off in Belgium"),
         ("09:00", "Brussels march gathers"), ("12:15", "van torched at Midi"),
         ("14:30", "Nvidia brings Huang back"), ("21:00", "Nasdaq closes +6.5%")]
x = M + 8
for moment, what in SLOTS:
    if what is None:
        sheet.put(x, 236, moment, "sans_b", 11, (255, 255, 255))
        x += sheet.tw(moment, "sans_b", 11) + 18
    else:
        sheet.put(x, 236, moment, "sans_b", 11, GOLD)
        x += sheet.tw(moment, "sans_b", 11) + 4
        sheet.put(x, 236, what, "sans", 11, (255, 255, 255))
        x += sheet.tw(what, "sans", 11) + 13

# ---------- lead illustrations ----------
def flame(x, y, s=1.0):
    draw.polygon(((x, y), (x + 7 * s, y - 16 * s), (x + 14 * s, y)), fill=(232, 120, 30))
    draw.polygon(((x + 4 * s, y), (x + 7 * s, y - 9 * s), (x + 10 * s, y)), fill=(246, 190, 60))


def scene_cop(x, y, w, h):
    draw.rectangle((x, y, x + w, y + h), fill=(188, 220, 206))
    mid_x = x + w / 2
    # semicircular amphitheatre of seats
    for rad in (58, 74, 90):
        for k in range(9):
            ang = math.pi * (0.15 + 0.0875 * k)
            cx = mid_x - rad * 1.6 * math.cos(ang)
            cy = y + h - 8 - rad * 0.62 * math.sin(ang)
            draw.ellipse((cx - 6, cy - 4, cx + 6, cy + 4), fill=(52, 40, 30))
    # podium desk, lectern block and gavel
    draw.rectangle((mid_x - 46, y + h - 34, mid_x + 46, y + h - 18), fill=(120, 84, 40))
    draw.rectangle((mid_x - 16, y + h - 48, mid_x + 16, y + h - 34), fill=(90, 60, 30))
    draw.line((mid_x + 24, y + h - 46, mid_x + 34, y + h - 58), fill=(90, 60, 30), width=3)
    # the torn final text, crossed out in red
    draw.polygon(((x + 22, y + 12), (x + 78, y + 12), (x + 72, y + 62), (x + 22, y + 62)),
                 fill=(250, 248, 240), outline=INK)
    draw.polygon(((x + 78, y + 12), (x + 96, y + 18), (x + 88, y + 58), (x + 72, y + 62)),
                 fill=(232, 230, 220), outline=INK)
    for ln in range(3):
        draw.line((x + 30, y + 22 + ln * 10, x + 66, y + 22 + ln * 10),
                  fill=(130, 130, 130), width=1)
    draw.line((x + 28, y + 18, x + 72, y + 56), fill=RED, width=3)
    draw.line((x + 72, y + 18, x + 28, y + 56), fill=RED, width=3)
    # wall clock
    draw.ellipse((x + w - 58, y + 10, x + w - 26, y + 42), outline=INK, width=2)
    draw.line((x + w - 42, y + 26, x + w - 42, y + 16), fill=INK, width=2)
    draw.line((x + w - 42, y + 26, x + w - 32, y + 30), fill=INK, width=2)
    sheet.flag(x, y, w, "NO COVER DECISION", "FIRST NO-DEAL COP SINCE 2009")


def scene_brussels(x, y, w, h):
    draw.rectangle((x, y, x + w, y + h), fill=(198, 212, 226))
    draw.ellipse((x + 24, y + 10, x + 66, y + 52), fill=(240, 244, 248))
    draw.ellipse((x + 190, y + 6, x + 224, y + 38), fill=(240, 244, 248))
    # runway
    draw.polygon(((x + 60, y + h), (x + w, y + h - 30), (x + w, y + h), (x + 60, y + h)),
                 fill=(120, 128, 138))
    for k in range(4):
        draw.line((x + 100 + k * 52, y + h - 8 - k * 6, x + 118 + k * 52, y + h - 10 - k * 6),
                  fill=(255, 255, 255), width=2)
    # control tower on the left
    draw.rectangle((x + 24, y + 34, x + 44, y + h - 12), fill=(88, 98, 110))
    draw.rectangle((x + 16, y + 16, x + 52, y + 36), fill=(58, 68, 82))
    for k in range(3):
        draw.rectangle((x + 20 + k * 11, y + 21, x + 28 + k * 11, y + 30), fill=(150, 200, 230))
    # parked jet, nose to the right
    draw.polygon(((x + 84, y + 60), (x + 246, y + 40), (x + 254, y + 46), (x + 116, y + 72),
                  (x + 92, y + 72)), fill=(242, 242, 242), outline=INK)
    draw.polygon(((x + 148, y + 56), (x + 172, y + 32), (x + 182, y + 56)),
                 fill=(222, 222, 222), outline=INK)
    for k in range(5):
        draw.rectangle((x + 126 + k * 16, y + 54, x + 134 + k * 16, y + 60), fill=(40, 90, 140))
    # red prohibition disc
    cx, cy = x + w - 40, y + 60
    draw.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), outline=RED, width=5)
    draw.line((cx - 16, cy + 16, cx + 16, cy - 16), fill=RED, width=5)
    sheet.flag(x, y, w, "404 FLIGHTS CANCELLED", "50,000 MARCH IN BRUSSELS")


def scene_nvidia(x, y, w, h):
    draw.rectangle((x, y, x + w, y + h), fill=NIGHT)
    for gy in range(4):
        yy = y + 22 + gy * 18
        draw.line((x + 10, yy, x + w - 10, yy), fill=(40, 56, 92), width=1)
    # the day's gain, top left, clear of the chart
    sheet.put(x + 14, y + 20, "+31%", "sans_b", 24, (46, 220, 110))
    # rising candlesticks on the right
    base = y + h - 18
    for off, lo, hi in ((110, 20, 30), (150, 26, 40), (190, 22, 36),
                        (230, 34, 50), (268, 40, 58)):
        draw.line((x + off + 7, base - hi - 8, x + off + 7, base - lo + 4),
                  fill=(120, 200, 120), width=2)
        draw.rectangle((x + off, base - hi, x + off + 14, base - lo), fill=(46, 180, 90))
    # the surge arrow over the candles
    draw.line([(x + 118, base - 26), (x + 180, base - 40), (x + 240, base - 50),
               (x + w - 24, base - 56)], fill=(250, 210, 60), width=3)
    draw.polygon(((x + w - 24, base - 56), (x + w - 40, base - 52),
                  (x + w - 28, base - 38)), fill=(250, 210, 60))
    sheet.put(x + 14, y + h - 16, "NASDAQ +6.5% · S&P +4.7% · DOW +3.0%",
              "sans_b", 9, (255, 255, 255))
    sheet.flag(x, y, w, "NVDA +31%", "+$950BN IN A DAY")


LEADS = [
    {"scene": scene_cop, "kick": "1  ANTALYA, TÜRKIYE · CLIMATE", "mark": "CONFIRMED",
     "title": "COP31 ends with no deal — and the world reacts",
     "text": "Sunday's plenary adopts no cover decision after 49 hours of "
             "overtime — the longest COP ever, first with no deal since "
             "Copenhagen 2009. Monday: Guterres voices “deep dismay”, Stiell "
             "says it “fell short”, Gore calls the veto “outrageous”.",
     "src": "Reuters · AP · AFP · CNN"},
    {"scene": scene_brussels, "kick": "2  BRUSSELS, BELGIUM · STRIKE", "mark": "CONFIRMED",
     "title": "Belgium's skies shut for a day as 50,000 march",
     "text": "Skeyes suspends ATC 07:00–21:00; 404 of 429 Brussels Airport flights "
             "are cancelled, hitting 50,000+ passengers, and Charleroi halts all "
             "day. Police count 50,000 on the march to Midi (unions say 70,000); "
             "De Wever warns his government could fall.",
     "src": "RTBF · AFP · Belga"},
    {"scene": scene_nvidia, "kick": "3  NEW YORK, USA · MARKETS", "mark": "CONFIRMED",
     "title": "Huang is back: Nvidia soars 31% as Trump brokers return",
     "text": "Eleven days after Huang quit amid scandal, the board reinstates him "
             "as CEO; Trump says “I made the deal”. Nvidia jumps 31% — its best "
             "day since 2003, adding about $950bn — as the Nasdaq gains 6.5% and "
             "the S&P 4.7%.",
     "src": "Reuters · Investopedia · USA Today"},
]
panel_w = (SPAN - 24) / 3
for pos, lead in enumerate(LEADS):
    left = M + pos * (panel_w + 12)
    lead["scene"](left, 260, panel_w, 96)
    sheet.put(left, 364, lead["kick"], "sans_b", 10, GREY)
    sheet.put(left + panel_w - sheet.tw(lead["mark"], "sans_b", 9), 365,
              lead["mark"], "sans_b", 9, RED)
    yy = sheet.block(left, 379, lead["title"], "serif_b", 19, INK, panel_w, 23, 3)
    yy = sheet.block(left, yy + 3, lead["text"], "sans", 10.5, SOFT, panel_w, 13.5, 5)
    sheet.put(left, 486, lead["src"], "sans", 9, GREY)
sheet.bar(500, 1)

# ---------- twelve small cards ----------
def glyph(kind, x, y, w, h, bg):
    draw.rectangle((x, y, x + w, y + h), fill=bg)
    cx, cy = x + w / 2, y + h / 2
    white = (255, 255, 255)
    if kind == "ballot":
        draw.rectangle((cx - 16, cy - 4, cx + 16, cy + 12), outline=white, width=2)
        draw.rectangle((cx - 8, cy - 13, cx + 10, cy - 5), fill=white)
    elif kind == "book":
        draw.rectangle((cx - 14, cy - 11, cx + 14, cy + 11), outline=white, width=2)
        draw.line((cx, cy - 11, cx, cy + 11), fill=white, width=2)
        for side in (-1, 1):
            draw.line((cx + side * 10, cy - 5, cx + side * 4, cy - 5), fill=white, width=1)
            draw.line((cx + side * 10, cy + 1, cx + side * 4, cy + 1), fill=white, width=1)
    elif kind == "phone":
        draw.rectangle((cx - 8, cy - 13, cx + 8, cy + 13), outline=white, width=2)
        draw.line((cx - 4, cy - 8, cx + 4, cy - 8), fill=white, width=1)
        draw.line((cx - 4, cy - 3, cx + 4, cy - 3), fill=(250, 210, 60), width=2)
    elif kind == "fire":
        flame(cx - 7, cy + 8, 1.4)
    elif kind == "rubble":
        draw.polygon(((cx - 18, cy + 12), (cx - 6, cy - 8), (cx + 2, cy + 2),
                      (cx + 8, cy - 12), (cx + 18, cy + 12)), outline=white, width=2)
        draw.line((cx - 2, cy - 12, cx + 2, cy + 12), fill=(250, 210, 60), width=2)
    elif kind == "radar":
        draw.ellipse((cx - 13, cy - 13, cx + 13, cy + 13), outline=white, width=2)
        draw.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), outline=white, width=2)
        draw.line((cx, cy, cx + 11, cy - 11), fill=(250, 210, 60), width=2)
    elif kind == "ship":
        draw.polygon(((cx - 20, cy + 2), (cx + 20, cy + 2), (cx + 13, cy + 12), (cx - 13, cy + 12)),
                     fill=(200, 200, 200))
        draw.rectangle((cx - 4, cy - 12, cx + 3, cy + 2), fill=(200, 200, 200))
        flame(cx + 6, cy + 2, 0.8)
    elif kind == "crowd":
        for off in (-14, 0, 14):
            draw.ellipse((cx + off - 5, cy - 12, cx + off + 5, cy - 2), fill=white)
            draw.pieslice((cx + off - 8, cy - 2, cx + off + 8, cy + 14), 180, 360, fill=white)
    elif kind == "bolt":
        draw.polygon(((cx + 2, cy - 14), (cx - 9, cy + 2), (cx - 1, cy + 2),
                      (cx - 3, cy + 14), (cx + 10, cy - 3), (cx + 1, cy - 3)), fill=(250, 210, 60))
    elif kind == "tennis":
        draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), outline=white, width=3)
        draw.arc((cx - 12, cy - 12, cx + 12, cy + 12), 300, 60, fill=white, width=2)
        draw.arc((cx - 12, cy - 12, cx + 12, cy + 12), 120, 240, fill=white, width=2)
    elif kind == "bus":
        draw.rectangle((cx - 20, cy - 10, cx + 20, cy + 10), outline=white, width=2)
        for k in range(4):
            draw.rectangle((cx - 16 + k * 9, cy - 6, cx - 10 + k * 9, cy + 1), fill=(150, 200, 230))
        draw.ellipse((cx - 14, cy + 8, cx - 6, cy + 16), fill=INK)
        draw.ellipse((cx + 6, cy + 8, cx + 14, cy + 16), fill=INK)


CARDS = [
    {"glyph": "ballot", "colour": (38, 84, 124), "num": "4",
     "tag": "HONG KONG · ELECTION", "mark": "CONFIRMED",
     "title": "Hong Kong names its Election Committee",
     "blurb": "Turnout 98.79% as 723 seats are filled; ex-minister Chan loses by two votes; Rimsky Yuen and Sophia Chan win seats.",
     "src": "SCMP"},
    {"glyph": "book", "colour": (24, 92, 84), "num": "5",
     "tag": "SEOUL · EDUCATION", "mark": "CONFIRMED",
     "title": "Seoul's education minister quits over AI row",
     "blurb": "Choi Kyo-jin steps down after rushed anti-cheating steps sparked a row over AI use.",
     "src": "AFP"},
    {"glyph": "phone", "colour": (168, 30, 30), "num": "6",
     "tag": "BEIJING · TELECOMS", "mark": "REPORTED",
     "title": "China slams US ban on its telecom carriers",
     "blurb": "Beijing says it “firmly opposes” the FCC move against Chinese telecom carriers.",
     "src": "Reuters"},
    {"glyph": "fire", "colour": (90, 60, 30), "num": "7",
     "tag": "CIKANDE · FIRE", "mark": "REPORTED",
     "title": "Cikande fire: body bags out, dozens missing",
     "blurb": "Seven body bags recovered; around 50 still unaccounted for after the factory fire.",
     "src": "Wires"},
    {"glyph": "rubble", "colour": (70, 100, 120), "num": "8",
     "tag": "DYMER · WAR", "mark": "REPORTED",
     "title": "Dymer: at least 14 still missing in the rubble",
     "blurb": "Rescuers search the wreckage of the Kyiv-region block hit in the drone barrage.",
     "src": "Reuters"},
    {"glyph": "radar", "colour": (24, 44, 74), "num": "9",
     "tag": "BAHRAIN · CLAIM", "mark": "CLAIM",
     "title": "Bahrain: the struck site was civilian",
     "blurb": "Manama says the target was a civilian site; Iran's radar claim remains unproven.",
     "src": "Al Jazeera"},
    {"glyph": "ship", "colour": (24, 44, 74), "num": "10",
     "tag": "GULF OF FINLAND · SEA", "mark": "REPORTED",
     "title": "Sparta II still burning off Finland",
     "blurb": "The Russian cargo ship burns into a second day; the Loviisa rescue operation leads.",
     "src": "Reuters"},
    {"glyph": "crowd", "colour": (196, 138, 32), "num": "11",
     "tag": "LISBON · PROTEST", "mark": "REPORTED",
     "title": "Thousands march in Lisbon over living costs",
     "blurb": "Streets fill as cost-of-living protests spread across Europe.",
     "src": "Wires"},
    {"glyph": "fire", "colour": (168, 30, 30), "num": "12",
     "tag": "NARAIL · VIOLENCE", "mark": "REPORTED",
     "title": "Narail: 30 homes torched in political attacks",
     "blurb": "Homes of Awami League figures set alight in a night of political violence.",
     "src": "Local wires"},
    {"glyph": "bolt", "colour": (70, 130, 60), "num": "13",
     "tag": "DELHI · ENERGY", "mark": "REPORTED",
     "title": "India and Nepal talk energy and connectivity",
     "blurb": "Delhi and Kathmandu discuss power links as pollution curbs bite in the capital.",
     "src": "Wires"},
    {"glyph": "tennis", "colour": (110, 66, 140), "num": "14",
     "tag": "TURIN · TENNIS", "mark": "CONFIRMED",
     "title": "Alcaraz wins his first ATP Finals crown",
     "blurb": "Beats Zverev 6-2, 7-6(7) in Turin, saving three set points in the tie-break; a year after losing the final to Sinner.",
     "src": "ATP"},
    {"glyph": "bus", "colour": (38, 84, 124), "num": "15",
     "tag": "MANILA · STRIKE", "mark": "CONFIRMED",
     "title": "Manila: transport strike begins, runs to Tuesday",
     "blurb": "Manibela's strike halts jeepneys and buses across the capital.",
     "src": "GMA"},
]
PILL = {"CONFIRMED": (34, 110, 62), "REPORTED": (70, 100, 120), "CLAIM": (168, 30, 30)}
card_w = (SPAN - 5 * 8) / 6
for idx, card in enumerate(CARDS):
    cx0 = M + (idx % 6) * (card_w + 8)
    cy0 = 508 + (idx // 6) * 128
    glyph(card["glyph"], cx0, cy0, card_w, 38, card["colour"])
    draw.rectangle((cx0, cy0, cx0 + 20, cy0 + 16), fill=RED)
    sheet.put(cx0 + (20 - sheet.tw(card["num"], "sans_b", 10)) / 2, cy0 + 3,
              card["num"], "sans_b", 10, (255, 255, 255))
    pill_w = sheet.tw(card["mark"], "sans_b", 7.5) + 9
    draw.rectangle((cx0 + card_w - pill_w, cy0, cx0 + card_w, cy0 + 13), fill=PILL[card["mark"]])
    sheet.put(cx0 + card_w - pill_w + 4.5, cy0 + 2.5, card["mark"], "sans_b", 7.5, (255, 255, 255))
    yy = sheet.block(cx0, cy0 + 43, card["title"], "serif_b", 11.5, INK, card_w, 14, 3)
    yy = sheet.block(cx0, yy + 1, card["blurb"], "sans", 9, (60, 60, 60), card_w, 11.5, 3)
    sheet.put(cx0, cy0 + 118, card["src"], "sans", 8, GREY)
sheet.bar(772, 1)

# ---------- dotted world map ----------
# Continents as ellipses in lon/lat space; dots are plotted on a fine
# grid wherever a grid point falls inside one of them.
BLOBS = [(-100, 45, 36, 24), (-60, -15, 15, 25), (15, 52, 21, 12),
         (20, 5, 18, 28), (90, 45, 46, 22), (135, -25, 15, 10)]
MAP_X, MAP_Y, MAP_W, MAP_H = M + 2, 800, 330, 92


def to_xy(lon, lat):
    return (MAP_X + (lon + 180) / 360 * MAP_W,
            MAP_Y + (90 - lat) / 180 * MAP_H)


def landed(lon, lat):
    for clon, clat, rx, ry in BLOBS:
        if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1:
            return True
    return False


sheet.put(M, 780, "WHERE IT HAPPENED", "sans_b", 11, INK)
sheet.put(M + 150, 782, "pins match story numbers", "sans", 9, GREY)
gx = MAP_X
while gx < MAP_X + MAP_W:
    gy = MAP_Y
    while gy < MAP_Y + MAP_H:
        lon = (gx - MAP_X) / MAP_W * 360 - 180
        lat = 90 - (gy - MAP_Y) / MAP_H * 180
        if landed(lon, lat):
            draw.ellipse((gx, gy, gx + 2.2, gy + 2.2), fill=(120, 130, 150))
        gy += 4.0
    gx += 4.0

PINS = [(1, 30.7, 36.9), (2, 4.4, 50.9), (3, -74.0, 40.7), (4, 114.2, 22.3),
        (5, 127.0, 37.5), (6, 116.4, 39.9), (7, 106.8, -6.2), (8, 30.5, 50.4),
        (9, 50.6, 26.2), (10, 25.0, 60.0), (11, -9.1, 38.7), (12, 90.4, 23.8),
        (13, 77.2, 28.6), (14, 7.7, 45.1), (15, 121.0, 14.6)]
for num, lon, lat in PINS:
    px, py = to_xy(lon, lat)
    draw.ellipse((px - 6, py - 6, px + 7, py + 7), fill=RED)
    label = str(num)
    sheet.put(px - sheet.tw(label, "sans_b", 8) / 2 + 0.5, py - 4,
              label, "sans_b", 8, (255, 255, 255))

# ---------- 26 more stories ----------
EXTRA = [
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
sheet.put(ax, 780, "ALSO ON MONDAY 23 NOVEMBER — 26 MORE STORIES", "sans_b", 11, INK)
col_w = (SIZE - M - ax - 12) / 2
for pos, item in enumerate(EXTRA):
    bx = ax + (pos // 13) * (col_w + 12)
    by = 798 + (pos % 13) * 11.2
    sheet.block(bx, by, item, "sans", 8.5, (40, 40, 40), col_w, 10, 1)

# ---------- date check ----------
draw.rectangle((M, 946, SIZE - M, 978), outline=RED, width=2)
sheet.put(M + 8, 952, "DATE CHECK", "sans_b", 10, RED)
NOTE = ("Left out as other days' news: the 186-drone night over Kyiv (Sat–Sun) · the Sparta II strike (Sat) · "
        "BepiColombo reaches Mercury (Sat) · “El Chapo Isidro” arrested (Fri). Sunday's results, reported "
        "Monday: Liverpool 4-0, Alcaraz's ATP crown, Hong Kong's vote; COP31 collapsed at Sunday's plenary — "
        "Monday's story is the fallout.")
sheet.block(M + 92, 952, NOTE, "sans", 9.5, (40, 40, 40), SPAN - 104, 12, 2)

# ---------- footer ----------
sheet.put(M, 984,
          "Sources: Reuters, AP, AFP, CNN, Al Jazeera, RTBF, Belga, Xinhua, SCMP, The Times, El País, GMA, Haaretz, KCNA, ATP, Investopedia, USA Today — and the wires named with each story.",
          "sans", 8.5, GREY)
sheet.put(M, 996,
          "PRESS TIME 23:30 UTC · CERTAINTY — CONFIRMED = two or more wires · REPORTED = carried by the day's wires · CLAIM = one side's account · FORECAST = still to happen",
          "sans_b", 8.5, GREY)
draw.rectangle((0, 1010, SIZE, SIZE), fill=NAVY)
sheet.put(M, 1014, "THE WORLD IN ONE DAY", "sans_b", 10, (255, 255, 255))
tail = "MONDAY 23 NOVEMBER 2026 · ONE PAGE"
sheet.put(SIZE - M - sheet.tw(tail, "sans_b", 10), 1014, tail, "sans_b", 10, (255, 255, 255))

sheet.canvas.save("/home/hatch/workspace/makefun-news-1123/build-v2/entry.png")
print("saved entry.png")
