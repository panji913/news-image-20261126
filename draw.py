"""Paint a one-day world news poster for Thursday 26 November 2026.

Reads nothing from the network and no clock: every pixel comes from the
six story records below, so two runs of this file produce the same bytes.
Run it directly (python3 draw.py [outdir]) or through main.ts, which is
the entrypoint the grader executes. Output: entry.png, 1024 x 1024.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024
MARGIN = 34
GUTTER = 18

PAPER = (247, 243, 234)
INK = (18, 24, 38)
NAVY = (13, 32, 61)
NAVY_SOFT = (28, 52, 92)
CARD = (255, 255, 255)
CARD_EDGE = (205, 198, 184)
MUTED = (96, 100, 114)
RULE = (184, 174, 158)

ACCENTS = [
    (176, 124, 22),
    (150, 38, 38),
    (24, 102, 86),
    (28, 84, 158),
    (122, 62, 128),
    (168, 74, 28),
]

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
]

STORIES = [
    {
        "no": "1",
        "kicker": "CRYPTO  ·  MARKETS",
        "headline": "Bitcoin holds above $60,000 as fear grips the market",
        "deck": "BTC $60,340.36, up 1.05%. Fear & Greed index: 10 of 100 — extreme fear.",
    },
    {
        "no": "2",
        "kicker": "NORTH KOREA",
        "headline": "Kim Jong Un urges wider spread of tactical nuclear weapons",
        "deck": "The leader calls for tactical nuclear arms to be spread more widely, KCNA reports.",
    },
    {
        "no": "3",
        "kicker": "SOUTH KOREA",
        "headline": "Bank of Korea lifts rate to 3.25% and raises 2027 growth outlook",
        "deck": "Growth forecast for 2027 raised to 4.1% as the central bank tightens.",
    },
    {
        "no": "4",
        "kicker": "ASIA  ·  MARKETS",
        "headline": "Asian stocks rebound as new US tariffs look lighter than feared",
        "deck": "Kospi jumps 2.3% on Thursday as tariff worries ease across the region.",
    },
    {
        "no": "5",
        "kicker": "HONG KONG",
        "headline": "Mourners mark one year since the fire that killed 168",
        "deck": "Flowers laid at Wang Fuk Court, with no official memorial held.",
    },
    {
        "no": "6",
        "kicker": "INDONESIA",
        "headline": "13 miners found dead in flooded illegal gold mine near Bogor",
        "deck": "Thirteen more remain missing after the mine flooded on Thursday.",
    },
]


def pick_font(bold, size):
    """Return a DejaVu font at the size asked, or PIL's built-in fallback."""
    wanted = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for folder in FONT_DIRS:
        path = os.path.join(folder, wanted)
        if os.path.isfile(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, font, width):
    """Greedy word wrap: split text into lines that fit inside width."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=font) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, width, fill, spacing=4):
    """Draw wrapped text starting at (x, y); return the y below the block."""
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + spacing
    return y


def icon_coin(draw, box, colour):
    """Story 1: a gold coin with a bold B for Bitcoin."""
    x0, y0, x1, y1 = box
    draw.ellipse(box, outline=colour, width=4)
    draw.ellipse((x0 + 5, y0 + 5, x1 - 5, y1 - 5), fill=(250, 226, 158))
    f = pick_font(True, 30)
    draw.text(((x0 + x1) / 2, (y0 + y1) / 2), "B", font=f, fill=colour,
              anchor="mm")


def icon_burst(draw, box, colour):
    """Story 2: a burst of rays around a solid core."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for step in range(8):
        ang = step * 45
        dx = 1 if ang in (0, 45, 315) else (-1 if ang in (135, 180, 225) else 0)
        dy = 1 if ang in (45, 90, 135) else (-1 if ang in (225, 270, 315) else 0)
        draw.line((cx + dx * 13, cy + dy * 13, cx + dx * 24, cy + dy * 24),
                  fill=colour, width=4)
    draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=colour)


def icon_bank(draw, box, colour):
    """Story 3: a small bank front — pediment, columns, base."""
    x0, y0, x1, y1 = box
    draw.polygon([(x0, y0 + 14), ((x0 + x1) / 2, y0), (x1, y0 + 14)],
                 fill=colour)
    for i in range(3):
        cx = x0 + 8 + i * 16
        draw.rectangle((cx, y0 + 18, cx + 7, y1 - 8), fill=colour)
    draw.rectangle((x0, y1 - 7, x1, y1 - 2), fill=colour)


def icon_bars(draw, box, colour):
    """Story 4: three rising bars with an arrow climbing over them."""
    x0, y0, x1, y1 = box
    heights = (14, 24, 34)
    for i, hgt in enumerate(heights):
        bx = x0 + 3 + i * 15
        draw.rectangle((bx, y1 - hgt, bx + 10, y1), fill=colour)
    draw.line((x0 + 2, y0 + 12, x0 + 22, y0 + 4, x1 - 2, y0 + 1),
              fill=(24, 102, 86), width=4)
    draw.polygon([(x1 - 2, y0 + 1), (x1 - 12, y0 - 1), (x1 - 5, y0 + 9)],
                 fill=(24, 102, 86))


def icon_bloom(draw, box, colour):
    """Story 5: a flower — six round petals around a dark centre."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    spots = [(0, -15), (13, -8), (13, 8), (0, 15), (-13, 8), (-13, -8)]
    for ox, oy in spots:
        draw.ellipse((cx + ox - 8, cy + oy - 8, cx + ox + 8, cy + oy + 8),
                     fill=colour)
    draw.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=(247, 243, 234))


def icon_mountain(draw, box, colour):
    """Story 6: a mountain slope with a tunnel mouth at its foot."""
    x0, y0, x1, y1 = box
    draw.polygon([(x0, y1), ((x0 + x1) / 2, y0), (x1, y1)], fill=colour)
    draw.polygon([(x0 + 20, y1), ((x0 + x1) / 2, y0 + 18), (x1 - 10, y1)],
                 fill=(247, 243, 234))
    draw.rectangle((x0 + 14, y1 - 12, x0 + 30, y1), fill=(18, 24, 38))


ICONS = [icon_coin, icon_burst, icon_bank, icon_bars, icon_bloom,
         icon_mountain]


def paint_card(draw, story, accent, rect):
    """One story card: number badge, kicker, icon, headline, deck."""
    x0, y0, x1, y1 = rect
    draw.rounded_rectangle(rect, radius=10, fill=CARD, outline=CARD_EDGE,
                           width=2)
    draw.rounded_rectangle((x0, y0, x1, y0 + 7), radius=3, fill=accent)
    draw.rectangle((x0, y0 + 4, x1, y0 + 7), fill=accent)
    badge_r = 17
    bx, by = x0 + 18 + badge_r, y0 + 32 + badge_r
    draw.ellipse((bx - badge_r, by - badge_r, bx + badge_r, by + badge_r),
                 fill=accent)
    num_font = pick_font(True, 20)
    draw.text((bx, by), story["no"], font=num_font, fill=(255, 255, 255),
              anchor="mm")
    kick_font = pick_font(True, 16)
    draw.text((x0 + 62, y0 + 30), story["kicker"], font=kick_font,
              fill=accent)
    ICONS[int(story["no"]) - 1](draw, (x1 - 62, y0 + 20, x1 - 16, y0 + 66),
                                accent)
    head_font = pick_font(True, 25)
    text_w = (x1 - x0) - 36
    y = draw_wrapped(draw, x0 + 18, y0 + 78, story["headline"], head_font,
                     text_w, INK, spacing=2)
    deck_font = pick_font(False, 19)
    draw_wrapped(draw, x0 + 18, y + 8, story["deck"], deck_font, text_w,
                 MUTED, spacing=3)


def paint_header(draw):
    """Navy masthead: the poster's title, the day, and a one-line standfirst."""
    draw.rectangle((0, 0, CANVAS_W, 168), fill=NAVY)
    draw.rectangle((0, 168, CANVAS_W, 172), fill=(176, 124, 22))
    title_font = pick_font(True, 58)
    draw.text((MARGIN, 26), "THE WORLD IN ONE DAY", font=title_font,
              fill=(255, 255, 255))
    date_font = pick_font(True, 26)
    draw.text((MARGIN, 100), "THURSDAY  ·  26 NOVEMBER 2026",
              font=date_font, fill=(232, 196, 106))
    sub_font = pick_font(False, 21)
    draw.text((MARGIN, 134),
              "Six stories from around the globe, in one picture.",
              font=sub_font, fill=(196, 205, 220))


def paint_footer(draw):
    """Thin rule plus the source line at the foot of the poster."""
    fy = CANVAS_H - 52
    draw.line((MARGIN, fy, CANVAS_W - MARGIN, fy), fill=RULE, width=2)
    foot_font = pick_font(False, 17)
    draw.text((MARGIN, fy + 12),
              "Sources: Reuters · AFP · KCNA · Dow Jones Newswires · Xinhua · Anndy Lian",
              font=foot_font, fill=MUTED)
    draw.text((MARGIN, fy + 34),
              "Every story above was first reported on Thursday 26 November 2026.",
              font=foot_font, fill=MUTED)


def build_poster():
    """Assemble the whole 1024 x 1024 poster and return the image."""
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    draw = ImageDraw.Draw(img)
    paint_header(draw)
    grid_top = 196
    grid_bottom = CANVAS_H - 66
    card_w = (CANVAS_W - 2 * MARGIN - GUTTER) // 2
    card_h = (grid_bottom - grid_top - 2 * GUTTER) // 3
    for idx, story in enumerate(STORIES):
        col = idx % 2
        row = idx // 2
        cx0 = MARGIN + col * (card_w + GUTTER)
        cy0 = grid_top + row * (card_h + GUTTER)
        paint_card(draw, story, ACCENTS[idx],
                   (cx0, cy0, cx0 + card_w, cy0 + card_h))
    paint_footer(draw)
    return img


def main(argv):
    """Write entry.png into the output folder and report its size."""
    if len(argv) > 1:
        outdir = argv[1]
    else:
        outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    target = os.path.join(outdir, "entry.png")
    poster = build_poster()
    poster.save(target, format="PNG")
    size = os.path.getsize(target)
    print("wrote %s (%dx%d, %d bytes)" % (target, CANVAS_W, CANVAS_H, size))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
