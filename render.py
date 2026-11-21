#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page (1024x1024 PNG).

A newspaper front page drawn entirely with Pillow primitives: every word
is rendered with DejaVu fonts, every picture is drawn from shapes, so the
text stays crisp and the file stays small. Run: python3 render.py
writes entry.png next to this file.

Stories (all happened or first reported on 21 Nov 2026, any time zone):
  lead    Russia's overnight barrage on Ukraine; missiles land in Poland
  markets S&P 500 into correction, Nikkei -5.1%
  Iran    Trump weighs new strikes; three tankers hit near Hormuz
  COP31   Antalya talks past deadline, fossil fuels cut from draft
  UK-EU   three post-Brexit deals signed in Brussels
  also    Anthropic $2tn debut; El Chapo Isidro arrested; cancer pill
          trial; ICJ finds Myanmar guilty of Rohingya genocide
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (176, 32, 32)
TEAL = (18, 92, 108)
NAVY = (22, 42, 82)
MUTED = (96, 90, 76)
CREAM_BOX = (238, 231, 212)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(d, text, fnt, max_w):
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def draw_para(d, x, y, max_w, text, fnt, fill=INK, leading=None, max_lines=None):
    leading = leading or int(fnt.size * 1.35)
    lines = wrap_text(d, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_head(d, x, y, max_w, text, fnt, fill=INK):
    leading = int(fnt.size * 1.1)
    for line in wrap_text(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(d, x0, x1, y, width=2):
    d.line([(x0, y), (x1, y)], fill=INK, width=width)


def tag(d, x, y, text):
    d.text((x, y), text, font=F(SANS_B, 15), fill=RED)


# ---------------------------------------------------------------- pictures

def pic_barrage(d, x0, y0, x1, y1):
    """Night over Kyiv: dark sky, missile arcs, explosions, three bridges."""
    hh = y1 - y0
    for i in range(hh):
        t = i / max(1, hh)
        d.line([(x0, y0 + i), (x1, y0 + i)],
               fill=(int(16 + 30 * t), int(26 + 30 * t), int(58 + 40 * t)))
    for sx, sy in [(x0 + 40, y0 + 16), (x0 + 180, y0 + 10), (x0 + 330, y0 + 20),
                   (x0 + 470, y0 + 12), (x0 + 560, y0 + 26)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    # red missile streaks, fully inside the frame, with bright heads
    for (ax, ay, bx, by) in [(x0 + 60, y0 + 14, x0 + 150, y0 + 66),
                             (x0 + 290, y0 + 10, x0 + 380, y0 + 62),
                             (x0 + 480, y0 + 16, x0 + 560, y0 + 68)]:
        d.line([(ax, ay), (bx, by)], fill=(255, 90, 60), width=4)
        d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 220, 120))
    # explosion bursts
    for ex, ey, r in [(x0 + 150, y0 + 78, 16), (x0 + 400, y0 + 72, 13),
                      (x0 + 560, y0 + 84, 11)]:
        for k in range(8):
            import math
            a = k * math.pi / 4
            d.line([(ex, ey), (ex + int(r * math.cos(a)), ey + int(r * math.sin(a)))],
                   fill=(255, 170, 40), width=3)
        d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 220, 120))
    # river + three bridges at the bottom
    d.rectangle([x0, y1 - 26, x1, y1], fill=(30, 70, 110))
    for bx in (x0 + 30, x0 + 250, x0 + 460):
        d.arc([bx, y1 - 52, bx + 110, y1 - 6], start=180, end=360,
              fill=(220, 220, 220), width=4)
        d.line([(bx, y1 - 26), (bx + 110, y1 - 26)], fill=(220, 220, 220), width=3)
    d.text((x0 + 10, y1 - 24), "KYIV", font=F(SANS_B, 13), fill=(255, 255, 255))
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def pic_market(d, x0, y0, x1, y1):
    """Falling chart: grid, red downtrend, candlesticks, -5.1% callout."""
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255))
    for gy in range(y0 + 20, y1, 22):
        d.line([(x0, gy), (x1, gy)], fill=(225, 225, 225), width=1)
    for gx in range(x0 + 40, x1, 44):
        d.line([(gx, y0), (gx, y1)], fill=(225, 225, 225), width=1)
    # candlesticks, falling, kept clear of the label at the top
    tops = [y0 + 40, y0 + 50, y0 + 46, y0 + 64, y0 + 72, y0 + 86]
    for i, top in enumerate(tops):
        cx = x0 + 26 + i * 46
        d.line([(cx + 8, top - 6), (cx + 8, top + 26)], fill=RED, width=2)
        d.rectangle([cx, top, cx + 16, top + 20], fill=RED)
    # trend line with arrowhead
    pts = [(x0 + 14, y0 + 44), (x0 + 90, y0 + 56), (x0 + 170, y0 + 52),
           (x0 + 250, y0 + 80), (x0 + 300, y0 + 100)]
    d.line(pts, fill=RED, width=5, joint="curve")
    d.polygon([(x0 + 300, y0 + 84), (x0 + 314, y0 + 98), (x0 + 292, y0 + 104)],
              fill=RED)
    d.text((x0 + 12, y0 + 8), "NIKKEI  -5.1%", font=F(SANS_B, 20), fill=RED)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def pic_tanker(d, x0, y0, x1, y1):
    """Strait of Hormuz: pale sky, teal sea, tanker with containers."""
    d.rectangle([x0, y0, x1, y1], fill=(250, 214, 140))
    d.rectangle([x0, y0 + 56, x1, y1], fill=(24, 110, 130))
    for wy in range(y0 + 62, y1 - 4, 10):
        d.line([(x0 + 8, wy), (x1 - 8, wy)], fill=(60, 150, 165), width=2)
    # containers stacked on the deck
    for i, col in enumerate([(200, 60, 50), (240, 180, 60), (60, 140, 90),
                             (200, 60, 50)]):
        d.rectangle([x0 + 40 + i * 46, y0 + 34, x0 + 80 + i * 46, y0 + 58],
                    fill=col, outline=INK, width=1)
    # funnel / bridge tower at the stern
    d.rectangle([x0 + 232, y0 + 28, x0 + 254, y0 + 58], fill=(240, 240, 240),
                outline=INK, width=1)
    # hull: dark, with a pointed bow on the right
    d.polygon([(x0 + 16, y0 + 58), (x0 + 268, y0 + 58), (x0 + 288, y0 + 72),
               (x0 + 268, y0 + 86), (x0 + 16, y0 + 86)], fill=(40, 40, 48))
    # missile plume arcing up in the top-right corner, inside the frame
    d.arc([x0 + 300, y0 + 2, x0 + 380, y0 + 52], start=250, end=350,
          fill=(255, 255, 255), width=5)
    d.ellipse([x0 + 352, y0 + 10, x0 + 362, y0 + 20], fill=(255, 90, 60))
    d.text((x0 + 12, y0 + 6), "STRAIT OF HORMUZ", font=F(SANS_B, 14), fill=INK)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def pic_climate(d, x0, y0, x1, y1):
    """A warming globe beside a red thermometer; COP31 in overtime."""
    hh = y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(222, 235, 240))
    cx, cy, r = x0 + 105, y0 + hh // 2, min(34, hh // 2 - 4)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 160, 200),
              outline=INK, width=2)
    d.ellipse([cx - 24, cy - 20, cx - 2, cy - 2], fill=(90, 170, 90))
    d.ellipse([cx + 2, cy + 4, cx + 24, cy + 24], fill=(90, 170, 90))
    d.ellipse([cx - 6, cy - r + 2, cx + 16, cy - 16], fill=(90, 170, 90))
    # thermometer, sized to the box
    tx = x0 + 205
    d.rectangle([tx, y0 + 8, tx + 20, y0 + hh - 18], fill=(255, 255, 255),
                outline=INK, width=2)
    d.rectangle([tx + 3, y0 + hh // 2, tx + 17, y0 + hh - 20], fill=RED)
    d.ellipse([tx - 5, y0 + hh - 24, tx + 25, y0 + hh - 2], fill=RED,
              outline=INK, width=2)
    d.text((tx + 32, y0 + 10), "+2.6°C", font=F(SANS_B, 18), fill=RED)
    d.text((tx + 32, y0 + 34), "by 2100", font=F(SANS, 14), fill=INK)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def pic_flags(d, x0, y0, x1, y1):
    """Union Jack and EU flag flying side by side."""
    d.rectangle([x0, y0, x1, y1], fill=(245, 245, 245))
    # Union Jack (simplified): blue field, white + red crosses
    ux0, uy0, ux1, uy1 = x0 + 10, y0 + 14, x0 + 74, y0 + 62
    d.rectangle([ux0, uy0, ux1, uy1], fill=(18, 50, 120), outline=INK, width=1)
    d.line([(ux0, uy0), (ux1, uy1)], fill=(255, 255, 255), width=8)
    d.line([(ux1, uy0), (ux0, uy1)], fill=(255, 255, 255), width=8)
    d.line([(ux0, uy0), (ux1, uy1)], fill=(200, 30, 40), width=3)
    d.line([(ux1, uy0), (ux0, uy1)], fill=(200, 30, 40), width=3)
    d.rectangle([(ux0 + ux1) // 2 - 6, uy0, (ux0 + ux1) // 2 + 6, uy1],
                fill=(255, 255, 255))
    d.rectangle([ux0, (uy0 + uy1) // 2 - 6, ux1, (uy0 + uy1) // 2 + 6],
                fill=(255, 255, 255))
    d.rectangle([(ux0 + ux1) // 2 - 3, uy0, (ux0 + ux1) // 2 + 3, uy1],
                fill=(200, 30, 40))
    d.rectangle([ux0, (uy0 + uy1) // 2 - 3, ux1, (uy0 + uy1) // 2 + 3],
                fill=(200, 30, 40))
    # EU flag: blue field, ring of yellow stars
    import math
    ex0, ey0, ex1, ey1 = x0 + 88, y0 + 14, x0 + 152, y0 + 62
    d.rectangle([ex0, ey0, ex1, ey1], fill=(0, 40, 130), outline=INK, width=1)
    ecx, ecy = (ex0 + ex1) // 2, (ey0 + ey1) // 2
    for k in range(12):
        a = k * math.pi / 6 - math.pi / 2
        sx, sy = ecx + int(18 * math.cos(a)), ecy + int(14 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 210, 0))
    d.text((x0 + 10, y0 + 72), "UK  •  EU", font=F(SANS_B, 13), fill=INK)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=3)

    # masthead
    name = "THE WORLD TODAY"
    nf = F(SERIF_B, 74)
    d.text(((W - d.textlength(name, font=nf)) / 2, 32), name, font=nf, fill=INK)
    rule(d, 36, W - 36, 122, 3)
    date = "SATURDAY  •  21 NOVEMBER 2026"
    df = F(SANS_B, 30)
    d.text(((W - d.textlength(date, font=df)) / 2, 134), date, font=df, fill=RED)
    tagline = "One day's news — the stories that mattered, from every corner of the world"
    tf = F(SANS, 19)
    d.text(((W - d.textlength(tagline, font=tf)) / 2, 172), tagline, font=tf,
           fill=MUTED)
    rule(d, 36, W - 36, 202, 2)

    # ---- row A: lead (left) + markets (right)
    y = 214
    pic_barrage(d, 36, y, 656, y + 112)
    pic_market(d, 676, y, 988, y + 112)
    y = 336
    tag(d, 36, y, "UKRAINE  •  POLAND — WAR SPILLS OVER")
    tag(d, 676, y, "MARKETS")
    y = 358
    y1 = draw_head(d, 36, y, 620, "RUSSIA'S BIGGEST BARRAGE HITS KYIV — AND LANDS IN POLAND",
                   F(SERIF_B, 33))
    y2 = draw_head(d, 676, y, 312, "STOCKS SLIDE WORLDWIDE AS AI SELL-OFF DEEPENS",
                   F(SERIF_B, 25))
    y = max(y1, y2) + 6
    draw_para(d, 36, y, 620,
              "More than 400 drones and 110 missiles struck Ukraine "
              "overnight, killing at least 8 and damaging three Kyiv "
              "bridges. Two Russian missiles and a suspected drone came "
              "down in Poland; NATO calls it a \u201cgrave violation\u201d.",
              F(SANS, 18), leading=21, max_lines=4)
    draw_para(d, 676, y, 312,
              "The S&P 500 slid into correction and Japan's Nikkei fell "
              "5.1% in a sharp global sell-off led by AI shares.",
              F(SANS, 17), leading=20, max_lines=4)

    rule(d, 36, W - 36, 564, 2)

    # ---- row B: Iran (left) + COP31 (right)
    y = 578
    pic_tanker(d, 36, y, 492, y + 80)
    pic_climate(d, 512, y, 988, y + 80)
    y = 668
    tag(d, 36, y, "MIDDLE EAST")
    tag(d, 512, y, "CLIMATE  •  ANTALYA")
    y = 690
    y1 = draw_head(d, 36, y, 456, "TRUMP WEIGHS NEW STRIKES ON IRAN AS TANKERS ARE HIT",
                   F(SERIF_B, 22))
    y2 = draw_head(d, 512, y, 476, "COP31 IN OVERTIME AS FOSSIL FUELS VANISH",
                   F(SERIF_B, 22))
    y = max(y1, y2) + 4
    draw_para(d, 36, y, 456,
              "Iran struck three tankers near the Strait of Hormuz as "
              "US\u2013Iran talks stalled, and Washington weighs another "
              "round of strikes.",
              F(SANS, 16), leading=20, max_lines=3)
    draw_para(d, 512, y, 476,
              "Nearly 200 nations missed the Friday deadline. The new "
              "draft drops every mention of fossil fuels and a $120bn "
              "adaptation target.",
              F(SANS, 16), leading=20, max_lines=3)

    rule(d, 36, W - 36, 818, 2)

    # ---- row C: UK-EU (left) + Also today (right)
    y = 832
    pic_flags(d, 36, y, 206, y + 122)
    tx = 222
    tag(d, tx, y, "BRUSSELS")
    draw_head(d, tx, y + 24, 318, "UK AND EU SIGN THREE POST-BREXIT DEALS",
              F(SERIF_B, 21))
    draw_para(d, tx, y + 76, 318,
              "PM Andy Burnham signs youth mobility, trade and energy "
              "deals in Brussels.",
              F(SANS, 15), leading=19, max_lines=2)

    ax0, ax1 = 556, 988
    d.rectangle([ax0, y, ax1, y + 122], fill=CREAM_BOX, outline=INK, width=2)
    d.text((ax0 + 14, y + 6), "ALSO TODAY", font=F(SANS_B, 17), fill=RED)
    briefs = [
        ("ANTHROPIC'S $2TN DEBUT",
         "AI firm joins Wall Street's most valuable companies."),
        ("MEXICO NABS CARTEL BOSS",
         "“El Chapo Isidro”, one of the FBI's 10 most wanted, detained."),
        ("PILL VS PANCREATIC CANCER",
         "Trial drug made tumours undetectable in 1 in 12 patients."),
        ("MYANMAR GUILTY OF GENOCIDE",
         "World court finds a state guilty of genocide for the first time."),
    ]
    by = y + 30
    for i, (head, body) in enumerate(briefs):
        cx = ax0 + 14 + (i % 2) * 210
        cy = by + (i // 2) * 44
        d.text((cx, cy), head, font=F(SANS_B, 11), fill=INK)
        draw_para(d, cx, cy + 15, 196, body, F(SANS, 11), leading=13,
                  max_lines=2)

    # ---- footer
    rule(d, 36, W - 36, 966, 2)
    foot = "Sources: AP  •  CNN  •  BBC  •  Reuters  •  NYT  •  ISW  —  21 November 2026"
    ff = F(SANS, 15)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 976), foot, font=ff, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    build()
