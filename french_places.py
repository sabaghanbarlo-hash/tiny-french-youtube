"""French places for Tiny French: a Paris café terrace, the Eiffel Tower view and a marché.

Shared by the lesson engine (lesson.py) and the story engine (story/scenery.py). Each place is a palette (sky, floor, table strip),
keywords that pick it automatically, aliases for `scene:` / `@scene`, named spots (x position as a fraction of the width)
and a drawing function that paints the 1920x1080 background above the floor line (y = 800).
"""
import math

L = None            # the engine module (font, sign, W ...), set by bind()


def bind(mod):
    global L
    L = mod


def register(mod):
    """Add the places to a lesson-style module's tables (lesson.py)."""
    bind(mod)
    mod.SCENES.update(SCENES)
    mod.SCENE_KEYWORDS.update(KEYWORDS)
    mod.SCENE_ALIASES.update(ALIASES)


def register_short(mod):
    """Add the places to the vertical Shorts engine (tinyvideo.py)."""
    bind(mod)
    mod.SCENES.update(SCENES)
    for k, v in KEYWORDS.items():
        mod.SCENE_KEYWORDS.setdefault(k, []).extend(v)
    mod.SCENE_ALIASES.update(ALIASES)
    mod.WEATHER_OUTDOOR.update(OUTDOOR)


SCENES = {
    "terrace": dict(top=(176, 210, 244), bot=(248, 240, 228), floor=(178, 166, 154), table=(176, 112, 84), edge=(132, 80, 60)),
    "eiffel": dict(top=(138, 190, 240), bot=(238, 242, 240), floor=(150, 198, 118), table=(118, 168, 94), edge=(82, 126, 68)),
    "market": dict(top=(184, 216, 246), bot=(250, 240, 222), floor=(192, 178, 150), table=(214, 170, 110), edge=(160, 124, 76)),
}
KEYWORDS = {
    "terrace": ["terrasse", "bistro", "brasserie", "terrace", "sidewalk café", "sidewalk cafe", "parisian café", "parisian cafe"],
    "eiffel": ["tour eiffel", "eiffel", "champ de mars"],
    "market": ["marché", "marche", "fromage", "légumes", "legumes", "market", "cheese", "vegetables", "stall"],
}
ALIASES = {
    "terrace": "terrace", "cafe terrace": "terrace", "café terrace": "terrace", "terrasse": "terrace", "bistro": "terrace",
    "brasserie": "terrace", "paris cafe": "terrace", "parisian cafe": "terrace", "sidewalk cafe": "terrace",
    "eiffel": "eiffel", "eiffel tower": "eiffel", "tour eiffel": "eiffel", "paris": "eiffel", "champ de mars": "eiffel", "paris view": "eiffel",
    "market": "market", "marché": "market", "marche": "market", "farmers market": "market", "open-air market": "market", "market square": "market",
}
LANDMARKS = {
    "terrace": {"street lamp": 0.1, "terrace table": 0.39, "door": 0.62, "menu board": 0.84},
    "eiffel": {"bench": 0.25, "lawn": 0.45, "tower": 0.68},
    "market": {"cheese stall": 0.2, "vegetable stall": 0.5, "fruit stall": 0.8},
}
OUTDOOR = {"terrace", "eiffel", "market"}
BIRD_SCENES = {"terrace", "eiffel", "market"}


# ------------------------------------------------------------------ small drawing helpers
def _building(d, x, w, top, y0, stone, roof, shutter=(120, 138, 158), balcony=True):
    """A cream Paris building: zinc mansard roof with dormers, tall windows with shutters, iron balconies."""
    d.rectangle((x, top, x + w, y0), fill=stone)
    rh = 64
    d.polygon([(x - 6, top), (x + w + 6, top), (x + w - 22, top - rh), (x + 22, top - rh)], fill=roof)
    darker = tuple(int(v * 0.84) for v in roof)
    for dx in range(x + 46, x + w - 64, 86):
        d.polygon([(dx - 4, top - rh + 16), (dx + 17, top - rh - 6), (dx + 38, top - rh + 16)], fill=darker)
        d.rectangle((dx, top - rh + 16, dx + 34, top - 6), fill=(232, 226, 216))
        d.rectangle((dx + 6, top - rh + 24, dx + 28, top - 6), fill=(168, 200, 224))
    for cx in (x + 40, x + w - 60):
        d.rectangle((cx, top - rh - 26, cx + 22, top - rh + 6), fill=(176, 120, 104))
    floors = max(1, (y0 - top - 30) // 100)
    for fi in range(floors):
        wy = top + 22 + fi * 100
        for wx in range(x + 24, x + w - 48, 68):
            d.rectangle((wx - 7, wy, wx - 2, wy + 70), fill=shutter)
            d.rectangle((wx + 38, wy, wx + 43, wy + 70), fill=shutter)
            d.rectangle((wx, wy, wx + 36, wy + 70), fill=(170, 202, 226), outline=(116, 128, 146), width=2)
            d.line([(wx + 18, wy), (wx + 18, wy + 70)], fill=(236, 240, 244), width=2)
        if balcony and fi in (1, floors - 1) and floors > 1:
            d.line([(x + 8, wy + 62), (x + w - 8, wy + 62)], fill=(56, 58, 68), width=5)
            for bx in range(x + 14, x + w - 8, 14):
                d.line([(bx, wy + 62), (bx, wy + 78)], fill=(56, 58, 68), width=2)
    d.line([(x, top), (x + w, top)], fill=tuple(int(v * 0.86) for v in stone), width=5)


def _row_of_buildings(d, rng, y0, x_from, x_to, hmin, hmax, stones, roofs):
    x = x_from
    while x < x_to:
        w = rng.randint(250, 340)
        _building(d, x, w, y0 - rng.randint(hmin, hmax), y0, rng.choice(stones), rng.choice(roofs))
        x += w + rng.randint(0, 6)


def _tree(d, cx, base_y, h, trunk=(120, 102, 88), leaf=(96, 170, 100)):
    d.rectangle((cx - 12, base_y - h * 0.55, cx + 12, base_y), fill=trunk)
    for dx, dy, r in ((0, -h * 0.78, h * 0.34), (-h * 0.2, -h * 0.64, h * 0.26), (h * 0.2, -h * 0.64, h * 0.26)):
        d.ellipse((cx + dx - r, base_y + dy - r, cx + dx + r, base_y + dy + r), fill=leaf)
    d.ellipse((cx - h * 0.18, base_y - h * 0.98, cx + h * 0.06, base_y - h * 0.76), fill=tuple(min(255, v + 22) for v in leaf))


def _awning(d, x0, x1, y_top, y_bot, c1, c2, stripes=10):
    sw = (x1 - x0) / stripes
    for j in range(stripes):
        xa = x0 + j * sw
        col = c1 if j % 2 == 0 else c2
        d.polygon([(xa + 12, y_top), (xa + sw + 12, y_top), (xa + sw, y_bot), (xa - 0, y_bot)], fill=col)
        d.pieslice((xa - 2, y_bot - 20, xa + sw + 2, y_bot + 20), 0, 180, fill=col)


def _sign(d, cx, y, w, h, text, fill, fg=(255, 255, 255), size=54):
    d.rounded_rectangle((cx - w // 2, y, cx + w // 2, y + h), radius=22, fill=fill)
    d.text((cx, y + h // 2), text, font=L.font(size), fill=fg, anchor="mm")


def _cloud(d, cx, cy, s=1.0):
    for dx, dy, rx, ry in ((0, 0, 92, 34), (-52, 8, 60, 26), (54, 10, 64, 26), (8, -22, 52, 34)):
        d.ellipse((cx + (dx - rx) * s, cy + (dy - ry) * s, cx + (dx + rx) * s, cy + (dy + ry) * s), fill=(255, 255, 255))


# ------------------------------------------------------------------ Paris café terrace
def _terrace(d, rng):
    W = L.W
    for cx, cy, s in ((300, 150, 1.0), (1480, 110, 0.8)):
        _cloud(d, cx, cy, s)
    stones = [(238, 228, 208), (232, 222, 200), (240, 232, 214)]
    roofs = [(98, 112, 132), (86, 100, 120)]
    _row_of_buildings(d, rng, 800, -40, W, 400, 520, stones, roofs)
    # the café front: dark green shop front under the cream building
    fx0, fx1 = 340, 1330
    d.rectangle((fx0, 480, fx1, 800), fill=(38, 86, 74))
    d.rectangle((fx0, 480, fx1, 494), fill=(28, 64, 56))
    _sign(d, (fx0 + fx1) // 2 - 120, 400, 520, 74, "Café de Paris", (30, 70, 60), fg=(246, 214, 120), size=46)
    for wx in (380, 760):
        d.rounded_rectangle((wx, 540, wx + 300, 760), radius=10, fill=(176, 214, 230), outline=(246, 214, 120), width=5)
        d.line([(wx + 150, 540), (wx + 150, 760)], fill=(246, 214, 120), width=4)
    d.rounded_rectangle((1150, 540, 1290, 800), radius=10, fill=(150, 96, 70), outline=(246, 214, 120), width=5)    # door (0.62 of the width)
    d.rounded_rectangle((1170, 560, 1270, 700), radius=8, fill=(176, 214, 230))
    d.ellipse((1262, 676, 1276, 690), fill=(246, 214, 120))
    # striped awning over the terrace
    _awning(d, fx0 - 20, fx1 - 220, 478, 548, (196, 52, 60), (250, 244, 232), stripes=12)
    # flower boxes on the first-floor windows
    for bx in range(400, 1200, 190):
        d.rectangle((bx, 442, bx + 90, 462), fill=(96, 70, 56))
        for k in range(6):
            d.ellipse((bx + 4 + k * 14, 424 + (k % 2) * 6, bx + 24 + k * 14, 446 + (k % 2) * 6), fill=(226, 70, 84) if k % 3 else (244, 150, 168))
    # round bistro tables and rattan chairs
    for tx in (470, 749, 1030):
        d.ellipse((tx - 62, 706, tx + 62, 730), fill=(250, 248, 244), outline=(150, 150, 156), width=3)
        d.rectangle((tx - 5, 730, tx + 5, 786), fill=(70, 70, 78))
        d.ellipse((tx - 34, 780, tx + 34, 792), fill=(70, 70, 78))
        d.ellipse((tx - 18, 692, tx + 18, 708), fill=(236, 120, 130))                   # a little cup
        for cxo, flip in ((-110, 1), (110, -1)):
            cx = tx + cxo
            d.arc((cx - 30, 640, cx + 30, 720), 180, 360, fill=(126, 84, 60), width=7)
            d.rounded_rectangle((cx - 32, 716, cx + 32, 730), radius=7, fill=(150, 104, 74))
            for lx in (cx - 26, cx + 20):
                d.line([(lx, 730), (lx + flip * 4, 788)], fill=(70, 70, 78), width=5)
    # street lamp (0.1 of the width)
    lx = int(0.1 * W)
    d.rectangle((lx - 7, 330, lx + 7, 800), fill=(34, 74, 62))
    d.ellipse((lx - 22, 770, lx + 22, 800), fill=(34, 74, 62))
    d.arc((lx - 52, 300, lx + 52, 380), 180, 360, fill=(34, 74, 62), width=6)
    for ox in (-46, 46):
        d.ellipse((lx + ox - 20, 340, lx + ox + 20, 392), fill=(255, 238, 180), outline=(34, 74, 62), width=5)
    d.ellipse((lx - 20, 280, lx + 20, 332), fill=(255, 238, 180), outline=(34, 74, 62), width=5)
    # plane tree on the right and the menu board (0.84)
    _tree(d, 1790, 800, 470, leaf=(104, 170, 98))
    bx = int(0.84 * W)
    d.line([(bx - 62, 780), (bx - 8, 570)], fill=(110, 84, 62), width=7)
    d.line([(bx + 62, 780), (bx + 8, 570)], fill=(110, 84, 62), width=7)
    d.rounded_rectangle((bx - 76, 582, bx + 76, 744), radius=10, fill=(44, 50, 54), outline=(150, 112, 78), width=8)
    d.text((bx, 618), "Menu", font=L.font(40), fill=(250, 244, 232), anchor="mm")
    for k, y in enumerate((664, 696, 726)):
        d.line([(bx - 52, y), (bx + 28 - 10 * k, y)], fill=(250, 244, 232), width=4)


# ------------------------------------------------------------------ the Eiffel Tower view
def _eiffel(d, rng):
    W = L.W
    for cx, cy, s in ((260, 170, 1.1), (900, 110, 0.8), (1700, 210, 0.9)):
        _cloud(d, cx, cy, s)
    # low Paris skyline behind the trees, with a golden dome
    x = -20
    while x < W:
        w = rng.randint(120, 200); h = rng.randint(70, 140)
        col = rng.choice([(226, 214, 196), (216, 206, 192), (232, 222, 204)])
        d.rectangle((x, 780 - h, x + w, 780), fill=col)
        d.polygon([(x - 4, 780 - h), (x + w + 4, 780 - h), (x + w - 16, 780 - h - 26), (x + 16, 780 - h - 26)], fill=(110, 122, 140))
        for wx in range(x + 16, x + w - 24, 44):
            d.rectangle((wx, 780 - h + 14, wx + 20, 780 - h + 46), fill=(170, 200, 224))
        x += w + rng.randint(0, 8)
    d.rectangle((250, 640, 370, 780), fill=(228, 216, 198))
    d.pieslice((250, 560, 370, 700), 180, 360, fill=(226, 184, 70))
    d.line([(310, 560), (310, 520)], fill=(226, 184, 70), width=5)
    # the tower
    cx, base, top = int(0.68 * W), 800, 150
    Ht = base - top
    iron, lattice, dark = (112, 92, 80), (160, 136, 116), (84, 68, 60)

    def hw(y):
        t = (base - y) / Ht
        return 9 + 238 * (1 - t) ** 2.35

    arch_top = base - 128
    a = hw(base) * 0.66

    def inner(y):
        u = (base - y) / 128
        return a * math.sqrt(max(0.0, 1 - u * u))

    ys = list(range(base, arch_top - 1, -4))
    for sgn in (-1, 1):                                         # the two legs, with the arch opening between them
        pts = [(cx + sgn * hw(y), y) for y in ys] + [(cx + sgn * inner(y), y) for y in reversed(ys)]
        d.polygon(pts, fill=iron)
    up = list(range(arch_top, top - 1, -4))
    d.polygon([(cx - hw(y), y) for y in up] + [(cx + hw(y), y) for y in reversed(up)], fill=iron)
    d.rectangle((cx - hw(arch_top) + 2, arch_top - 8, cx + hw(arch_top) - 2, arch_top + 6), fill=dark)
    # lattice: X braces between horizontal bands
    bands = [arch_top, base - 250, base - 360, base - 470, base - 560, top + 10]
    for y1, y2 in zip(bands[:-1], bands[1:]):
        w1, w2 = hw(y1) - 6, hw(y2) - 4
        d.line([(cx - w1, y1), (cx + w2, y2)], fill=lattice, width=3)
        d.line([(cx + w1, y1), (cx - w2, y2)], fill=lattice, width=3)
        d.line([(cx - w1, y1), (cx + w1, y1)], fill=dark, width=4)
    for sgn in (-1, 1):
        d.line([(cx + sgn * (hw(y) - 5), y) for y in range(arch_top - 8, top, -16)], fill=dark, width=3)
    for yp, ext in ((base - 250, 18), (base - 470, 12)):        # platforms
        d.rounded_rectangle((cx - hw(yp) - ext, yp - 8, cx + hw(yp) + ext, yp + 10), radius=4, fill=dark)
    d.polygon([(cx - 12, top + 4), (cx + 12, top + 4), (cx + 3, top - 46), (cx - 3, top - 46)], fill=dark)
    d.line([(cx, top - 46), (cx, top - 84)], fill=dark, width=5)
    # trees and a bench on the Champ de Mars
    for tx, h in ((110, 360), (400, 300), (1740, 340), (1880, 300)):
        _tree(d, tx, 800, h, leaf=(86, 160, 96))
    bx = int(0.25 * W)
    d.rounded_rectangle((bx - 90, 728, bx + 90, 748), radius=6, fill=(110, 86, 64))
    d.rounded_rectangle((bx - 90, 676, bx + 90, 694), radius=6, fill=(126, 98, 72))
    for lx in (bx - 72, bx + 72):
        d.rectangle((lx - 5, 694, lx + 5, 796), fill=(58, 62, 70))
    d.rectangle((0, 770, W, 800), fill=(110, 170, 96))                                  # hedge along the lawn
    for hx in range(0, W, 36):
        d.ellipse((hx, 762, hx + 44, 800), fill=(96, 160, 88))


# ------------------------------------------------------------------ the marché
def _market(d, rng):
    W = L.W
    for cx, cy, s in ((240, 140, 0.9), (1560, 120, 1.0)):
        _cloud(d, cx, cy, s)
    _row_of_buildings(d, rng, 800, -40, W, 300, 440, [(236, 226, 206), (230, 220, 200), (240, 234, 218)], [(98, 112, 132), (86, 100, 120)])
    for tx in (120, 640, 1300, 1800):
        _tree(d, tx, 800, 430, leaf=(112, 172, 100))
    pts = [(x, 250 + 26 * math.sin(x / 150)) for x in range(0, W + 40, 40)]                 # bunting across the square
    d.line(pts, fill=(110, 90, 80), width=3)
    cols = [(40, 80, 190), (250, 250, 250), (210, 50, 60)]
    for j, (x, y) in enumerate(pts[:-1]):
        d.polygon([(x, y), (x + 40, y + 2), (x + 20, y + 50)], fill=cols[j % 3])
    stalls = ((0.2, "Fromages", (236, 184, 60), (252, 246, 226), "cheese"),
              (0.5, "Légumes", (84, 160, 88), (250, 250, 240), "veg"),
              (0.8, "Fruits", (214, 70, 70), (252, 244, 238), "fruit"))
    for fx, label, c1, c2, kind in stalls:
        cx = int(fx * W)
        for px in (cx - 176, cx + 176):
            d.rectangle((px - 6, 460, px + 6, 800), fill=(120, 92, 70))
        _awning(d, cx - 190, cx + 190, 456, 536, c1, c2, stripes=8)
        _sign(d, cx, 372, 270, 70, label, c1, fg=(255, 255, 255) if kind != "cheese" else (96, 64, 20), size=44)
        d.rectangle((cx - 176, 640, cx + 176, 712), fill=(190, 142, 98))
        d.rectangle((cx - 176, 712, cx + 176, 800), fill=(156, 112, 76))
        for j in range(7):
            xj = cx - 150 + j * 50
            if kind == "cheese":
                d.ellipse((xj - 22, 596, xj + 22, 646), fill=(250, 214, 110), outline=(214, 170, 70), width=3)
                if j % 2 == 0:
                    d.polygon([(xj, 621), (xj + 22, 606), (xj + 22, 636)], fill=(236, 190, 80))
            elif kind == "veg":
                col = [(236, 130, 50), (110, 180, 90), (180, 60, 90), (110, 180, 90)][j % 4]
                d.ellipse((xj - 20, 604, xj + 20, 644), fill=col)
                d.polygon([(xj - 8, 604), (xj + 8, 604), (xj, 584)], fill=(70, 150, 80))
            else:
                col = [(226, 60, 60), (250, 190, 60), (130, 200, 90), (240, 130, 60)][j % 4]
                d.ellipse((xj - 21, 606, xj + 21, 648), fill=col)
                d.arc((xj - 12, 614, xj + 8, 636), 200, 300, fill=(255, 255, 255), width=3)
        d.rectangle((cx - 160, 650, cx - 100, 700), fill=(214, 176, 120))                    # a crate
    d.ellipse((1030, 705, 1090, 765), fill=(214, 176, 120))                                 # a straw basket by the middle stall


DRAW = {"terrace": _terrace, "eiffel": _eiffel, "market": _market}


def sparkle(fr, tt):
    """The Eiffel Tower twinkles at night (called for the 'eiffel' place when the time of day is night)."""
    from PIL import ImageDraw
    d = ImageDraw.Draw(fr)
    cx, base, top = int(0.68 * L.W), 800, 150
    for i in range(54):
        y = top + 20 + (i * 59) % (base - top - 60)
        t = (base - y) / (base - top)
        half = (9 + 238 * (1 - t) ** 2.35) * (((i * 37) % 100) / 50.0 - 1.0) * 0.86
        if math.sin(tt * 5.5 + i * 1.9) > 0.45:
            r = 4 + (i % 3)
            d.ellipse((cx + half - r, y - r, cx + half + r, y + r), fill=(255, 236, 160))


# ------------------------------------------------------------------ vertical versions for Shorts (1080 wide, ground at y = 885, art from y = 270)
SW, SG = 1080, 885


def _terrace_s(d, rng):
    _cloud(d, 240, 320, 0.8); _cloud(d, 860, 300, 0.7)
    _row_of_buildings(d, rng, SG, -40, SW, 330, 430, [(238, 228, 208), (232, 222, 200)], [(98, 112, 132), (86, 100, 120)])
    d.rectangle((50, 560, 1030, SG), fill=(38, 86, 74)); d.rectangle((50, 560, 1030, 572), fill=(28, 64, 56))
    _sign(d, 470, 468, 560, 78, "Café de Paris", (30, 70, 60), fg=(246, 214, 120), size=50)
    for wx in (90, 400):
        d.rounded_rectangle((wx, 612, wx + 270, 836), radius=10, fill=(176, 214, 230), outline=(246, 214, 120), width=5)
        d.line([(wx + 135, 612), (wx + 135, 836)], fill=(246, 214, 120), width=4)
    d.rounded_rectangle((740, 612, 870, SG), radius=10, fill=(150, 96, 70), outline=(246, 214, 120), width=5)
    d.rounded_rectangle((760, 632, 850, 770), radius=8, fill=(176, 214, 230))
    _awning(d, 40, 720, 556, 626, (196, 52, 60), (250, 244, 232), stripes=10)
    for bx in (110, 420):
        d.rectangle((bx, 520, bx + 90, 540), fill=(96, 70, 56))
        for k in range(6):
            d.ellipse((bx + 4 + k * 14, 502 + (k % 2) * 6, bx + 24 + k * 14, 524 + (k % 2) * 6), fill=(226, 70, 84) if k % 3 else (244, 150, 168))
    for tx in (250, 560):
        d.ellipse((tx - 62, 780, tx + 62, 804), fill=(250, 248, 244), outline=(150, 150, 156), width=3)
        d.rectangle((tx - 5, 804, tx + 5, 862), fill=(70, 70, 78)); d.ellipse((tx - 34, 856, tx + 34, 868), fill=(70, 70, 78))
        d.ellipse((tx - 18, 766, tx + 18, 782), fill=(236, 120, 130))
    lx = 1010
    d.rectangle((lx - 7, 400, lx + 7, SG), fill=(34, 74, 62)); d.ellipse((lx - 22, 855, lx + 22, SG), fill=(34, 74, 62))
    d.ellipse((lx - 20, 352, lx + 20, 404), fill=(255, 238, 180), outline=(34, 74, 62), width=5)
    d.arc((lx - 50, 380, lx + 50, 450), 180, 360, fill=(34, 74, 62), width=6)


def _eiffel_s(d, rng):
    _cloud(d, 200, 340, 0.9); _cloud(d, 900, 300, 0.7)
    x = -20
    while x < SW:
        w = rng.randint(110, 180); h = rng.randint(60, 120)
        d.rectangle((x, SG - 20 - h, x + w, SG - 20), fill=rng.choice([(226, 214, 196), (216, 206, 192), (232, 222, 204)]))
        d.polygon([(x - 4, SG - 20 - h), (x + w + 4, SG - 20 - h), (x + w - 14, SG - 44 - h), (x + 14, SG - 44 - h)], fill=(110, 122, 140))
        x += w + rng.randint(0, 8)
    cx, base, top = 600, SG, 290
    Ht = base - top
    iron, lattice, dark = (112, 92, 80), (160, 136, 116), (84, 68, 60)
    hw = lambda y: 8 + 196 * (1 - (base - y) / Ht) ** 2.35
    arch = 104
    a = hw(base) * 0.66
    inner = lambda y: a * math.sqrt(max(0.0, 1 - ((base - y) / arch) ** 2))
    ys = list(range(base, base - arch - 1, -4))
    for sgn in (-1, 1):
        d.polygon([(cx + sgn * hw(y), y) for y in ys] + [(cx + sgn * inner(y), y) for y in reversed(ys)], fill=iron)
    up = list(range(base - arch, top - 1, -4))
    d.polygon([(cx - hw(y), y) for y in up] + [(cx + hw(y), y) for y in reversed(up)], fill=iron)
    d.rectangle((cx - hw(base - arch) + 2, base - arch - 7, cx + hw(base - arch) - 2, base - arch + 5), fill=dark)
    bands = [base - arch, base - 200, base - 290, base - 380, base - 450, top + 8]
    for y1, y2 in zip(bands[:-1], bands[1:]):
        w1, w2 = hw(y1) - 5, hw(y2) - 3
        d.line([(cx - w1, y1), (cx + w2, y2)], fill=lattice, width=3); d.line([(cx + w1, y1), (cx - w2, y2)], fill=lattice, width=3)
        d.line([(cx - w1, y1), (cx + w1, y1)], fill=dark, width=4)
    for yp, ext in ((base - 200, 15), (base - 380, 10)):
        d.rounded_rectangle((cx - hw(yp) - ext, yp - 7, cx + hw(yp) + ext, yp + 9), radius=4, fill=dark)
    d.polygon([(cx - 10, top + 3), (cx + 10, top + 3), (cx + 3, top - 38), (cx - 3, top - 38)], fill=dark)
    d.line([(cx, top - 38), (cx, top - 70)], fill=dark, width=5)
    for tx, h in ((70, 300), (1010, 280)):
        _tree(d, tx, SG, h, leaf=(86, 160, 96))
    bx = 210
    d.rounded_rectangle((bx - 80, 808, bx + 80, 826), radius=6, fill=(110, 86, 64)); d.rounded_rectangle((bx - 80, 760, bx + 80, 776), radius=6, fill=(126, 98, 72))
    for lx in (bx - 62, bx + 62):
        d.rectangle((lx - 5, 776, lx + 5, SG - 4), fill=(58, 62, 70))
    d.rectangle((0, SG - 28, SW, SG), fill=(110, 170, 96))
    for hx in range(0, SW, 36):
        d.ellipse((hx, SG - 36, hx + 44, SG), fill=(96, 160, 88))


def _market_s(d, rng):
    _cloud(d, 220, 330, 0.8); _cloud(d, 880, 310, 0.7)
    _row_of_buildings(d, rng, SG, -40, SW, 300, 400, [(236, 226, 206), (230, 220, 200), (240, 234, 218)], [(98, 112, 132), (86, 100, 120)])
    for tx in (60, 1020):
        _tree(d, tx, SG, 340, leaf=(112, 172, 100))
    pts = [(x, 320 + 20 * math.sin(x / 120)) for x in range(0, SW + 40, 40)]
    d.line(pts, fill=(110, 90, 80), width=3)
    cols = [(40, 80, 190), (250, 250, 250), (210, 50, 60)]
    for j, (x, y) in enumerate(pts[:-1]):
        d.polygon([(x, y), (x + 40, y + 2), (x + 20, y + 46)], fill=cols[j % 3])
    for cx, label, c1, c2, kind in ((190, "Fromages", (236, 184, 60), (252, 246, 226), "cheese"),
                                    (540, "Légumes", (84, 160, 88), (250, 250, 240), "veg"),
                                    (890, "Fruits", (214, 70, 70), (252, 244, 238), "fruit")):
        for px in (cx - 150, cx + 150):
            d.rectangle((px - 5, 520, px + 5, SG), fill=(120, 92, 70))
        _awning(d, cx - 160, cx + 160, 512, 580, c1, c2, stripes=8)
        _sign(d, cx, 444, 240, 62, label, c1, fg=(255, 255, 255) if kind != "cheese" else (96, 64, 20), size=40)
        d.rectangle((cx - 150, 720, cx + 150, 790), fill=(190, 142, 98)); d.rectangle((cx - 150, 790, cx + 150, SG), fill=(156, 112, 76))
        for j in range(6):
            xj = cx - 125 + j * 50
            if kind == "cheese":
                d.ellipse((xj - 22, 676, xj + 22, 724), fill=(250, 214, 110), outline=(214, 170, 70), width=3)
            elif kind == "veg":
                d.ellipse((xj - 20, 684, xj + 20, 722), fill=[(236, 130, 50), (110, 180, 90), (180, 60, 90)][j % 3])
                d.polygon([(xj - 8, 684), (xj + 8, 684), (xj, 664)], fill=(70, 150, 80))
            else:
                d.ellipse((xj - 21, 684, xj + 21, 726), fill=[(226, 60, 60), (250, 190, 60), (130, 200, 90), (240, 130, 60)][j % 4])


SHORT_DRAW = {"terrace": _terrace_s, "eiffel": _eiffel_s, "market": _market_s}
