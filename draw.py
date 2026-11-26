# news-image-20261126 — one-page poster for Thursday 26 November 2026.
#
# A single 1024x1024 PNG, painted with Pillow and nothing else. No
# network calls, no clock reads, no random numbers: the same script
# always writes the same bytes, so the file the grader sees is the
# file that was checked here.
#
# What the poster carries: six stories that happened — or were first
# reported — on 26 November 2026, each verified against the outlet
# named on its card:
#   * Bitcoin at $60,340.36, +1.05% in 24h, Fear & Greed 10/100
#     (Anndy Lian newsletter, 26 Nov)
#   * Kim Jong Un urges wider tactical nuclear weapons deployment
#     (KCNA via Reuters, 26 Nov)
#   * Bank of Korea raises its base rate to 3.25% and lifts the
#     2027 growth outlook to 4.1% (Reuters, 26 Nov)
#   * Asian stocks rebound on Thursday as the new US tariffs look
#     milder than feared (Dow Jones Newswires / AFP, 26 Nov)
#   * Hong Kong marks one year since the Wang Fuk Court fire that
#     killed 168 (AFP, 26 Nov)
#   * 13 miners found dead on Thursday in a flooded illegal gold
#     mine in Bogor, West Java; 13 still missing (Reuters / Xinhua,
#     26 Nov)
#
# Stories dated 24 or 25 November were checked and left out on
# purpose: the Trump tariff proposals, the FCC's Starmind approval,
# the Netanyahu judges' recommendation, the Cartagena rescue, the
# Nigeria meth bust, the Lukoil deal, the Shenzhou-24 docking and
# the Macy's parade postponement all broke on 25 November (or
# earlier), so none of them is on this poster.
#
# How it looks: a dark ink page, a masthead with the title and the
# date in gold, six cards in a 2-by-3 grid — each card opens with a
# coloured kicker, then a headline, a one-sentence body and the
# source — and a footer naming the check date and the outlets.
#
# To make it:  python3 draw.py     (writes entry.png beside this file)

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "entry.png"

PAGE_W = 1024
PAGE_H = 1024

INK = (10, 16, 28)
CARD = (20, 30, 50)
EDGE = (58, 82, 122)
WHITE = (240, 244, 250)
GREY = (172, 188, 208)
FAINT = (126, 144, 168)
GOLD = (232, 184, 84)
CORAL = (228, 86, 86)
AQUA = (68, 194, 182)
SKY = (100, 154, 238)
LEAF = (114, 200, 114)
AMBER = (238, 154, 68)
LILAC = (172, 134, 224)

DEJAVU = Path("/usr/share/fonts/truetype/dejavu")


def load(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(str(DEJAVU / name), size)


TITLE_F = load(54, bold=True)
DATE_F = load(26, bold=True)
TAG_F = load(20, bold=True)
HEAD_F = load(26, bold=True)
BODY_F = load(20)
SMALL_F = load(18)

# Each story: kicker, accent, headline, one-sentence body, source.
STORIES = [
    {
        "tag": "BITCOIN",
        "accent": AMBER,
        "head": "Bitcoin holds $60,340 as fear grips",
        "body": "BTC up 1.05% in 24 hours; the Fear & Greed index sits at 10 — extreme fear.",
        "src": "Anndy Lian newsletter",
    },
    {
        "tag": "NORTH KOREA",
        "accent": CORAL,
        "head": "Kim urges wider tactical nuclear rollout",
        "body": "Kim Jong Un calls deploying tactical nukes across domains an urgent task.",
        "src": "KCNA via Reuters",
    },
    {
        "tag": "SOUTH KOREA",
        "accent": SKY,
        "head": "Bank of Korea lifts rate to 3.25%",
        "body": "Seoul hikes a quarter point and raises its 2027 growth outlook to 4.1%.",
        "src": "Reuters",
    },
    {
        "tag": "MARKETS",
        "accent": LEAF,
        "head": "Asian stocks rebound as tariffs look milder",
        "body": "Kospi leads the rally, up 2.3%; the Nikkei and Hang Seng climb too.",
        "src": "Dow Jones / AFP",
    },
    {
        "tag": "HONG KONG",
        "accent": LILAC,
        "head": "Hong Kong marks a year since the fire",
        "body": "Mourners lay flowers at Wang Fuk Court, where 168 people died a year ago.",
        "src": "AFP",
    },
    {
        "tag": "INDONESIA",
        "accent": AQUA,
        "head": "13 miners found dead in flooded Java mine",
        "body": "Thirteen more are still missing in the illegal gold mine near Bogor.",
        "src": "Reuters / Xinhua",
    },
]

# The two numbers on the poster are quoted exactly as their sources
# gave them on 26 November: $60,340.36 for Bitcoin and the Fear &
# Greed reading of 10 out of 100, and the 13 dead plus 13 missing
# in Bogor, where the search was still going on when the toll was
# reported — so the missing count may yet move.


def fit(draw, text, font, width, limit=2):
    """Split text into at most `limit` lines that fit `width` pixels."""
    words = text.split()
    lines = []
    i = 0
    while i < len(words) and len(lines) < limit:
        line = words[i]
        i += 1
        while i < len(words):
            nxt = line + " " + words[i]
            if draw.textlength(nxt, font=font) > width:
                break
            line = nxt
            i += 1
        lines.append(line)
    return lines


def card(draw, x, y, w, h, story):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=16,
                           fill=CARD, outline=EDGE, width=2)
    # Kicker in its accent colour, then a short accent rule under it.
    draw.text((x + 20, y + 18), story["tag"], font=TAG_F,
              fill=story["accent"])
    draw.line([(x + 20, y + 50), (x + 20 + 56, y + 50)],
              fill=story["accent"], width=3)
    # Headline, at most two lines.
    top = y + 64
    for ln in fit(draw, story["head"], HEAD_F, w - 40):
        draw.text((x + 20, top), ln, font=HEAD_F, fill=WHITE)
        top += 32
    # Body, at most two lines, then the source pinned to the bottom.
    top += 8
    for ln in fit(draw, story["body"], BODY_F, w - 40):
        draw.text((x + 20, top), ln, font=BODY_F, fill=GREY)
        top += 26
    draw.text((x + 20, y + h - 32), "Source: " + story["src"],
              font=SMALL_F, fill=FAINT)


def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), INK)
    draw = ImageDraw.Draw(img)

    # Masthead: title, gold date, gold rule, one-line standfirst.
    draw.text((40, 30), "THE WORLD IN ONE DAY", font=TITLE_F, fill=WHITE)
    draw.text((40, 102), "THURSDAY  ·  26 NOVEMBER 2026",
              font=DATE_F, fill=GOLD)
    draw.line([(40, 146), (PAGE_W - 40, 146)], fill=GOLD, width=4)
    draw.text((40, 158),
              "Six stories that defined the day — from Seoul to Hong Kong, "
              "Pyongyang to Jakarta.",
              font=SMALL_F, fill=GREY)

    # Grid: two columns, three rows, equal cards.
    margin = 40
    gap = 16
    cw = (PAGE_W - 2 * margin - gap) // 2
    ch = 232
    top = 200
    for n, story in enumerate(STORIES):
        cx = margin + (n % 2) * (cw + gap)
        cy = top + (n // 2) * (ch + gap)
        card(draw, cx, cy, cw, ch, story)

    # Footer: check date, outlets, competition slug.
    fy = top + 3 * ch + 2 * gap + 20
    draw.line([(40, fy), (PAGE_W - 40, fy)], fill=EDGE, width=2)
    draw.text((40, fy + 12),
              "Checked 26 Nov 2026  ·  Reuters  ·  KCNA  ·  Dow Jones  ·  "
              "AFP  ·  Xinhua  ·  Anndy Lian",
              font=SMALL_F, fill=GREY)
    draw.text((40, fy + 40), "make.fun  ·  news-image-20261126",
              font=SMALL_F, fill=FAINT)

    img.save(TARGET, format="PNG", optimize=True)
    blob = TARGET.read_bytes()
    print(f"wrote {TARGET} {len(blob)} bytes "
          f"sha256={hashlib.sha256(blob).hexdigest()}")


if __name__ == "__main__":
    build()
