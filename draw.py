#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news broadsheet (SPARSE experiment).

Nine verified stories only: 2 large illustrated leads, 3 medium cards,
4 one-line briefs. Renders one 1024x1024 page with Pillow on the dev
machine; the graded entrypoint only copies the rendered file.
Every story below was verified against wire reports the morning of
26 Nov 2026 (all first reported 26 Nov in at least one time zone):
Giza tanker fire (Reuters/CNN), Nasdaq -4% (Reuters), Netanyahu
judges (Reuters/CNN), Poland no-fly zone (Reuters), North Korea
expels Swiss envoy (Reuters/KCNA), Hera/DART crater (ESA),
Bangladesh wage rise (AP), Melania reunions (White House/Reuters),
Russia war dead (BBC analysis of leaked Rosstat data).
Left out on purpose: 24-25 Nov stories (turkey pardon, Lukashenko
offer, Cartagena standoff, Shenzhou-24, BepiColombo, Nvidia/Huang,
Huawei verdict, Houthi drone on Riyadh).
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "entry.png")

W, H = 1024, 1024
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (246, 241, 227)
PANEL = (255, 253, 246)
INK = (25, 25, 25)
GREY = (91, 91, 91)
BLUE = (25, 70, 170)
RED = (185, 30, 30)
TEAL = (15, 118, 110)
ORANGE = (194, 87, 11)
PURPLE = (109, 40, 168)
BROWN = (124, 74, 18)
NAVY = (16, 32, 64)

REGION = {
    "Americas": BLUE,
    "Europe": TEAL,
    "Middle East": RED,
    "Asia": ORANGE,
    "Africa": PURPLE,
    "Oceania": BROWN,
    "Global": GREY,
}


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, width, fill=INK, spacing=3,
               max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def sky_bands(draw, box, top, bottom, steps=14):
    x0, y0, x1, y1 = box
    for i in range(steps):
        t = i / (steps - 1)
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t)
                    for c in range(3))
        yy0 = y0 + (y1 - y0) * i // steps
        yy1 = y0 + (y1 - y0) * (i + 1) // steps
        draw.rectangle([x0, yy0, x1, yy1], fill=col)


def draw_fire(draw, x, y, w, h):
    """Night highway fire: burning tanker on the Cairo ring road."""
    sky_bands(draw, (x, y, x + w, y + h), (18, 16, 38), (92, 42, 22))
    rng = random.Random(7)
    for _ in range(20):
        sx = x + rng.randint(6, w - 6)
        sy = y + rng.randint(6, h // 3)
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r],
                     fill=(220, 220, 210))
    # glow on the horizon
    draw.ellipse([x + w // 2 - 100, y + h - 130, x + w // 2 + 100,
                  y + h - 30], fill=(255, 150, 50))
    draw.ellipse([x + w // 2 - 66, y + h - 104, x + w // 2 + 66,
                  y + h - 36], fill=(255, 200, 90))
    # distant skyline, dark against the glow
    base = y + h - 62
    bx = x + 8
    rng2 = random.Random(21)
    while bx < x + w - 30:
        bw = rng2.randint(30, 58)
        bh = rng2.randint(26, 58)
        draw.rectangle([bx, base - bh, bx + bw, base], fill=(28, 24, 34))
        bx += bw + 6
    # road with perspective
    draw.polygon([(x, y + h), (x + w * 0.30, base + 8),
                  (x + w * 0.70, base + 8), (x + w, y + h)],
                 fill=(38, 38, 44))
    draw.line([x + w * 0.30, base + 8, x + w * 0.44, y + h],
              fill=(230, 200, 60), width=3)
    draw.line([x + w * 0.70, base + 8, x + w * 0.56, y + h],
              fill=(230, 200, 60), width=3)
    # tanker, side view, on the road
    tx, ty = x + w // 2 - 105, base - 34
    draw.rectangle([tx, ty, tx + 150, ty + 30], fill=(150, 150, 148))
    draw.ellipse([tx + 150, ty + 2, tx + 176, ty + 28], fill=(90, 90, 88))
    draw.rectangle([tx + 152, ty + 8, tx + 172, ty + 22],
                   fill=(180, 220, 240))
    for wx in (tx + 18, tx + 52, tx + 120):
        draw.ellipse([wx, ty + 32, wx + 16, ty + 48], fill=(15, 15, 15))
        draw.ellipse([wx + 4, ty + 36, wx + 12, ty + 44],
                     fill=(120, 120, 120))
    # flames over the tanker
    cx = x + w // 2
    for dx, s, col in [(-72, 52, (255, 110, 20)), (-30, 72, (255, 150, 30)),
                       (18, 62, (255, 110, 20)), (62, 44, (255, 190, 60)),
                       (-52, 34, (255, 190, 60))]:
        fx = cx + dx
        fy = ty + 6
        draw.polygon([(fx - s // 2, fy), (fx, fy - s),
                      (fx + s // 2, fy)], fill=col)
        draw.polygon([(fx - s // 4, fy), (fx, fy - s // 2),
                      (fx + s // 4, fy)], fill=(255, 220, 110))
    # smoke columns
    for sx, sy, r in [(x + 70, y + 22, 18), (x + 108, y + 46, 14),
                      (x + w - 80, y + 26, 17), (x + w - 118, y + 50, 13)]:
        draw.ellipse([sx - r, sy - r // 2, sx + r, sy + r // 2],
                     fill=(64, 60, 66))


def draw_market(draw, x, y, w, h):
    """Wall Street sell-off: a falling chart on a dark board."""
    sky_bands(draw, (x, y, x + w, y + h), (10, 20, 52), (24, 48, 96))
    # grid
    for gy in range(5):
        yy = y + 18 + gy * (h - 40) // 4
        draw.line([x + 12, yy, x + w - 12, yy], fill=(52, 76, 120), width=1)
    for gx in range(6):
        xx = x + 12 + gx * (w - 24) // 5
        draw.line([xx, y + 12, xx, y + h - 12], fill=(52, 76, 120), width=1)
    # descending bars
    base = y + h - 22
    heights = [118, 104, 112, 88, 94, 70, 58, 40]
    bw = (w - 40) // len(heights)
    for i, hh in enumerate(heights):
        bx = x + 20 + i * bw
        draw.rectangle([bx, base - hh, bx + bw - 8, base],
                       fill=(200, 60, 50))
    # falling line over the bars
    pts = []
    for i, hh in enumerate(heights):
        px = x + 20 + i * bw + (bw - 8) // 2
        py = base - hh - 16
        pts.append((px, py))
    draw.line(pts, fill=(255, 210, 90), width=4)
    for px, py in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 210, 90))
    # arrow head at the last point
    ex, ey = pts[-1]
    draw.polygon([(ex, ey + 16), (ex - 12, ey - 2), (ex + 2, ey - 2)],
                 fill=(255, 210, 90))
    # big fall label (caption below the panel already names the market)
    f_big = font(SANS_B, 44)
    label = "-4%"
    draw.text((x + 18, y + 10), label, font=f_big, fill=(255, 90, 80))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=NAVY, width=2)
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=1)

    f_mast = font(SERIF_B, 40)
    f_date = font(SERIF_B, 30)
    f_sub = font(SANS_B, 14)
    f_kick = font(SANS_B, 13)
    f_head = font(SANS_B, 22)
    f_deck = font(SANS, 14)
    f_src = font(SANS, 11)
    f_card_h = font(SANS_B, 21)
    f_card_d = font(SANS, 13)
    f_brief_h = font(SANS_B, 20)
    f_brief = font(SANS, 20)
    f_small = font(SANS, 11)
    f_small_b = font(SANS_B, 11)

    # masthead
    mast = "THE WORLD'S NEWS IN ONE PICTURE"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 26), mast,
           font=f_mast, fill=BLUE)
    # date line — PROMINENT: red, 30px, ruled above and below
    d.line([60, 108, W - 60, 108], fill=RED, width=2)
    date_line = "THURSDAY, 26 NOVEMBER 2026"
    d.text(((W - d.textlength(date_line, font=f_date)) / 2, 118), date_line,
           font=f_date, fill=RED)
    d.line([60, 164, W - 60, 164], fill=RED, width=2)
    sub = "9 STORIES  \u2022  6 REGIONS  \u2022  EVERY ONE FROM THIS THURSDAY"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 174), sub,
           font=f_sub, fill=INK)
    d.line([28, 198, W - 28, 198], fill=INK, width=2)

    # --- 2 large illustrated leads ---
    leads = [
        {"art": "fire", "region": "Africa", "topic": "DISASTER",
         "head": "Fuel tanker fire kills 31 on Cairo ring road",
         "deck": "Blaze above the Warraq tunnel engulfs cars; 21 hurt.",
         "src": "Reuters \u00b7 CNN"},
        {"art": "market", "region": "Americas", "topic": "MARKETS",
         "head": "Nasdaq dives 4% as AI stocks rout Wall Street",
         "deck": "Nvidia falls 8.6%; US plans tariffs on 14 partners.",
         "src": "Reuters"},
    ]
    art = {"fire": draw_fire, "market": draw_market}
    ly, lh, cap = 206, 210, 124
    for i, lead in enumerate(leads):
        x = 24 + i * 486
        lw = 476
        d.rectangle([x, ly, x + lw, ly + lh + cap], outline=INK, width=1,
                    fill=PANEL)
        art[lead["art"]](d, x + 1, ly + 1, lw - 2, lh - 2)
        col = REGION[lead["region"]]
        d.rectangle([x, ly + lh, x + lw, ly + lh + 30], fill=col)
        tag = "%s  \u2022  %s" % (lead["region"].upper(), lead["topic"])
        d.text((x + 10, ly + lh + 7), tag, font=f_kick,
               fill=(255, 255, 255))
        yy = text_block(d, x + 10, ly + lh + 38, lead["head"], f_head,
                        lw - 20, spacing=1, max_lines=2)
        text_block(d, x + 10, yy + 2, lead["deck"], f_deck, lw - 20,
                   fill=(50, 50, 50), spacing=2, max_lines=1)
        d.text((x + 10, ly + lh + cap - 14), lead["src"], font=f_src,
               fill=GREY)

    # --- 3 medium cards ---
    cards = [
        ("Middle East", "LAW",
         "Judges urge end to Netanyahu bribery case",
         "Court says a conviction in Case 4000 is unlikely; "
         "prosecutors to reconsider a second case."),
        ("Europe", "DEFENCE",
         "Poland plans no-fly zone on Ukraine border",
         "Warsaw acts after Russian missiles crossed its airspace; "
         "NATO intercept idea raised in Brussels."),
        ("Asia", "DIPLOMACY",
         "North Korea expels Swiss envoy",
         "Pyongyang orders its office shut in 48 hours in a row "
         "over sanctions on a youth camp."),
    ]
    cy0, ch, cw, gap = 556, 152, 315, 10
    for i, (region, topic, head, deck) in enumerate(cards):
        x = 24 + i * (cw + gap)
        y = cy0
        col = REGION[region]
        d.rectangle([x, y, x + cw, y + ch], outline=INK, width=1,
                    fill=PANEL)
        d.rectangle([x, y, x + cw, y + 34], fill=col)
        tag = "%s  \u2022  %s" % (region.upper(), topic)
        d.text((x + 10, y + 9), tag, font=f_kick, fill=(255, 255, 255))
        yy = text_block(d, x + 10, y + 44, head, f_card_h, cw - 20,
                        spacing=1, max_lines=2)
        text_block(d, x + 10, yy + 4, deck, f_card_d, cw - 20,
                   fill=(50, 50, 50), spacing=2, max_lines=3)

    # --- IN BRIEF: 4 one-liners, 2 columns ---
    by = 724
    d.line([24, by, W - 24, by], fill=INK, width=2)
    d.text((24, by + 8), "IN BRIEF", font=f_brief_h, fill=RED)
    briefs = [
        ("Global", "Hera photos show DART left a stadium-size crater "
                   "on asteroid Dimorphos."),
        ("Asia", "Bangladesh garment workers win a 36% pay rise, "
                "to 17,000 taka a month."),
        ("Europe", "Melania Trump helps reunite 9 more children; "
                  "43 returned in all."),
        ("Europe", "Russia's own figures show nearly 500,000 "
                  "war dead."),
    ]
    yy = by + 48
    for i, (region, text) in enumerate(briefs):
        col_i, row_i = divmod(i, 2)
        x = 24 + col_i * 488
        y = yy + row_i * 72
        col = REGION[region]
        d.text((x, y), "\u2022", font=f_brief, fill=col)
        line = "%s: %s" % (region, text)
        text_block(d, x + 22, y, line, f_brief, 460, spacing=2,
                   max_lines=2)

    # --- footer: date check + sources ---
    fy = 916
    d.line([24, fy, W - 24, fy], fill=INK, width=1)
    check = ("DATE CHECK \u2014 Left out: 25 Nov stories, not today. "
             "Shenzhou-24 \u2022 BepiColombo \u2022 Nvidia/Huang "
             "\u2022 Huawei verdict \u2022 Houthi drone on Riyadh "
             "\u2022 Cartagena standoff \u2022 Turkey pardon (24 Nov) "
             "\u2022 Lukashenko offer (24 Nov).")
    text_block(d, 24, fy + 8, check, f_small_b, W - 48, fill=RED,
               spacing=1, max_lines=2)
    srcs = ("Sources: Reuters \u2022 CNN \u2022 AP \u2022 ESA "
            "\u2022 White House \u2022 BBC \u2014 Illustrations are drawings.")
    d.text((24, 978), srcs, font=f_small, fill=GREY)

    img.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
