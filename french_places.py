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



# ======================================================================= more French places (override the Japan-flavoured originals)
# Every scene is drawn once at 1920x800 (ground at y = 800). Shorts reuse it: drawn off-screen, scaled and cropped to the vertical frame.
GROUND = 800
STONE = [(238, 228, 208), (232, 222, 200), (240, 232, 214), (228, 218, 198)]
ZINC = [(98, 112, 132), (86, 100, 120), (108, 120, 138)]
WALLACE = (40, 92, 76)
BORDEAUX = (126, 38, 50)
NAVY = (34, 56, 100)
MUSTARD = (226, 172, 62)
CREAM = (250, 244, 232)
WOOD = (110, 70, 50)
BRASS = (210, 170, 80)
FRAME = (214, 172, 84)


def _lamp(d, x, base=GROUND, h=380, col=WALLACE):
    d.rectangle((x - 6, base - h, x + 6, base), fill=col)
    d.ellipse((x - 22, base - 26, x + 22, base), fill=col)
    d.rectangle((x - 12, base - h * 0.35, x + 12, base - h * 0.35 + 10), fill=col)
    d.arc((x - 46, base - h - 40, x + 46, base - h + 40), 180, 360, fill=col, width=6)
    for ox in (-40, 40):
        d.ellipse((x + ox - 16, base - h - 4, x + ox + 16, base - h + 40), fill=(255, 238, 180), outline=col, width=4)
    d.ellipse((x - 16, base - h - 56, x + 16, base - h - 10), fill=(255, 238, 180), outline=col, width=4)


def _morris(d, x, base=GROUND):
    """Colonne Morris, the green advertising column."""
    d.rectangle((x - 54, base - 250, x + 54, base - 14), fill=WALLACE)
    d.ellipse((x - 62, base - 28, x + 62, base), fill=(28, 70, 58))
    d.polygon([(x - 58, base - 250), (x + 58, base - 250), (x + 40, base - 296), (x - 40, base - 296)], fill=(30, 76, 62))
    d.ellipse((x - 40, base - 312, x + 40, base - 280), fill=(30, 76, 62))
    d.rectangle((x - 6, base - 344, x + 6, base - 312), fill=(30, 76, 62))
    for j, c in enumerate(((236, 220, 160), (232, 140, 120), (150, 190, 214))):
        yy = base - 232 + j * 70
        d.rectangle((x - 44, yy, x + 44, yy + 56), fill=c)
        d.rectangle((x - 30, yy + 10, x + 30, yy + 18), fill=(80, 70, 70)); d.rectangle((x - 30, yy + 28, x + 12, yy + 34), fill=(110, 100, 100))


def _shopfront(d, x, w, y_top, y0, col, label, awn=None, fgc=(250, 244, 232), door=False, size=28):
    d.rectangle((x + 6, y_top, x + w - 6, y0), fill=col)
    d.rectangle((x + 6, y_top, x + w - 6, y_top + 6), fill=tuple(int(v * 0.7) for v in col))
    d.rectangle((x + 14, y_top + 10, x + w - 14, y_top + 52), fill=tuple(int(v * 0.82) for v in col))
    d.text((x + w // 2, y_top + 31), label, font=L.font(size), fill=fgc, anchor="mm")
    wx0 = x + 24
    if door:
        d.rounded_rectangle((x + w - 92, y_top + 64, x + w - 24, y0), radius=6, fill=tuple(int(v * 0.8) for v in col), outline=fgc, width=3)
        d.rectangle((x + w - 82, y_top + 76, x + w - 34, y_top + 140), fill=(176, 208, 224))
        wx1 = x + w - 110
    else:
        wx1 = x + w - 24
    d.rectangle((wx0, y_top + 66, wx1, y0 - 14), fill=(178, 210, 226), outline=fgc, width=3)
    d.line([((wx0 + wx1) // 2, y_top + 66), ((wx0 + wx1) // 2, y0 - 14)], fill=fgc, width=3)
    if awn:
        _awning(d, x + 2, x + w - 2, y_top + 54, y_top + 100, awn[0], awn[1], stripes=max(4, w // 36))


def _bentwood(d, cx, base, s=1.0, col=(70, 44, 34)):
    """A bistro chair seen from the front."""
    d.arc((cx - 28 * s, base - 150 * s, cx + 28 * s, base - 70 * s), 180, 360, fill=col, width=max(3, int(7 * s)))
    d.line([(cx - 26 * s, base - 110 * s), (cx - 24 * s, base - 62 * s)], fill=col, width=max(3, int(6 * s)))
    d.line([(cx + 26 * s, base - 110 * s), (cx + 24 * s, base - 62 * s)], fill=col, width=max(3, int(6 * s)))
    d.ellipse((cx - 32 * s, base - 72 * s, cx + 32 * s, base - 56 * s), fill=(150, 104, 74), outline=col, width=2)
    for lx in (-24, 22):
        d.line([(cx + lx * s, base - 60 * s), (cx + (lx + (3 if lx > 0 else -3)) * s, base)], fill=col, width=max(3, int(6 * s)))


def _round_table(d, cx, base, r=70, top=(250, 248, 244), cloth=None):
    ty = base - 100
    if cloth:
        d.polygon([(cx - r, ty), (cx + r, ty), (cx + r + 14, ty + 56), (cx - r - 14, ty + 56)], fill=cloth[0])
        for k in range(-3, 4):
            d.line([(cx + k * r / 3.5, ty), (cx + k * (r + 14) / 3.5, ty + 56)], fill=cloth[1], width=5)
        d.ellipse((cx - r, ty - 14, cx + r, ty + 14), fill=cloth[1], outline=cloth[0], width=3)
    else:
        d.ellipse((cx - r, ty - 14, cx + r, ty + 14), fill=top, outline=(150, 150, 156), width=3)
        d.rectangle((cx - 5, ty + 12, cx + 5, base - 8), fill=(60, 60, 68))
        d.ellipse((cx - 38, base - 16, cx + 38, base), fill=(60, 60, 68))


def _books(d, x0, y0, x1, rng, rows=1, h=44):
    for r in range(rows):
        x = x0
        while x < x1 - 12:
            w = rng.randint(12, 24); hh = rng.randint(h - 12, h)
            d.rectangle((x, y0 + r * (h + 4) + (h - hh), x + w, y0 + r * (h + 4) + h),
                        fill=rng.choice([(150, 60, 60), (60, 90, 140), (190, 150, 70), (80, 120, 90), (120, 80, 130), (200, 190, 170)]))
            x += w + 2


def _window_street(d, x0, y0, x1, y1, rng, arch=True):
    """A tall French window looking out on cream roofs."""
    d.rounded_rectangle((x0 - 10, y0 - 10, x1 + 10, y1 + 10), radius=30 if arch else 6, fill=(236, 230, 218), outline=(176, 166, 150), width=3)
    d.rounded_rectangle((x0, y0, x1, y1), radius=24 if arch else 4, fill=(176, 212, 238))
    for k in range(4):
        d.ellipse((x0 + 30 + k * 70, y0 + 40 + (k % 2) * 24, x0 + 120 + k * 70, y0 + 74 + (k % 2) * 24), fill=(255, 255, 255))
    by = y1 - 120
    x = x0
    while x < x1:
        w = rng.randint(60, 100)
        d.rectangle((x, by + rng.randint(0, 30), min(x + w, x1), y1), fill=rng.choice(STONE))
        d.polygon([(x - 2, by + 10), (min(x + w, x1) + 2, by + 10), (min(x + w, x1) - 10, by - 12), (x + 10, by - 12)], fill=rng.choice(ZINC))
        x += w
    d.line([((x0 + x1) // 2, y0), ((x0 + x1) // 2, y1)], fill=(236, 230, 218), width=6)
    d.line([(x0, y0 + (y1 - y0) // 3), (x1, y0 + (y1 - y0) // 3)], fill=(236, 230, 218), width=5)


SHOPS = [("Boulangerie", (222, 168, 66), (196, 52, 60), (250, 244, 232)), ("Fromagerie", (110, 40, 52), (250, 244, 232), (230, 176, 60)),
         ("Fleurs", (60, 120, 92), (232, 120, 140), (250, 244, 232)), ("Pharmacie", (44, 110, 84), (250, 250, 250), (250, 250, 250)),
         ("Librairie", (34, 56, 100), (214, 172, 84), (250, 244, 232)), ("Tabac", (126, 38, 50), (250, 244, 232), (230, 176, 60)),
         ("Café", (38, 78, 70), (196, 52, 60), (246, 214, 120)), ("Marché", (186, 120, 60), (60, 120, 92), (250, 244, 232))]


def _street(d, rng, variant="street"):
    W = L.W
    for cx, cy, s in ((260, 130, 1.0), (1000, 90, 0.8), (1640, 150, 0.9)):
        _cloud(d, cx, cy, s)
    x = -30
    while x < W:
        w = rng.randint(230, 300)
        _building(d, x, w, GROUND - rng.randint(470, 560), GROUND - 160, tuple(min(255, v + 8) for v in rng.choice(STONE)), rng.choice(ZINC), shutter=(150, 164, 180))
        x += w
    x, k = -20, rng.randint(0, 7)
    while x < W:
        w = rng.randint(290, 360)
        lab, col, a1, fg = SHOPS[k % len(SHOPS)]
        k += 1
        _building(d, x, w, GROUND - rng.randint(430, 500), GROUND - 190, rng.choice(STONE), rng.choice(ZINC))
        _shopfront(d, x, w, GROUND - 190, GROUND, col, lab, awn=(a1, CREAM) if variant == "town" else None, fgc=fg, door=(k % 2 == 0))
        x += w
    _morris(d, int(0.62 * W))
    _lamp(d, int(0.3 * W), h=360)
    _lamp(d, int(0.88 * W), h=360)
    for tx in (int(0.1 * W), int(0.47 * W), int(0.76 * W)):
        _tree(d, tx, GROUND, 360, leaf=(108, 166, 98))
        d.rectangle((tx - 30, GROUND - 6, tx + 30, GROUND), fill=(58, 60, 66))


def _bakery(d, rng):
    W = L.W
    for cx, cy, s in ((300, 120, 1.0), (1500, 100, 0.8)):
        _cloud(d, cx, cy, s)
    _row_of_buildings(d, rng, GROUND, -40, W, 400, 520, STONE, ZINC)
    fx0, fx1 = 170, 1560
    d.rectangle((fx0, 330, fx1, GROUND), fill=(36, 70, 108))
    d.rectangle((fx0, 330, fx1, 346), fill=(24, 48, 78))
    d.rounded_rectangle((fx0 + 180, 352, fx1 - 180, 436), radius=14, fill=(24, 48, 78), outline=FRAME, width=5)
    d.text(((fx0 + fx1) // 2, 394), "BOULANGERIE", font=L.font(66), fill=(246, 214, 120), anchor="mm")
    d.text(((fx0 + fx1) // 2, 450), "Pâtisserie", font=L.font(30), fill=(246, 214, 120), anchor="mm")
    for wx0, wx1 in ((210, 760), (800, 1350)):
        d.rounded_rectangle((wx0, 500, wx1, 740), radius=10, fill=(244, 226, 190), outline=FRAME, width=5)
        for sy in (590, 676):
            d.rectangle((wx0 + 12, sy, wx1 - 12, sy + 10), fill=(150, 104, 74))
        for j in range(6):
            bx = wx0 + 50 + j * 36
            d.rounded_rectangle((bx, 520, bx + 24, 590), radius=12, fill=(214, 160, 90), outline=(170, 118, 60), width=2)
            d.line([(bx + 4, 534), (bx + 20, 542)], fill=(170, 118, 60), width=3); d.line([(bx + 4, 556), (bx + 20, 564)], fill=(170, 118, 60), width=3)
        for j in range(5):
            cx = wx0 + 280 + j * 52
            d.pieslice((cx - 24, 536, cx + 24, 586), 190, 350, fill=(222, 156, 70), outline=(176, 112, 46))
            d.arc((cx - 14, 548, cx + 14, 584), 200, 340, fill=(176, 112, 46), width=3)
        for j in range(5):
            tx = wx0 + 40 + j * 100
            d.rounded_rectangle((tx, 640, tx + 66, 676), radius=8, fill=[(226, 80, 90), (250, 190, 70), (150, 100, 70), (240, 150, 170), (110, 180, 100)][j])
            d.ellipse((tx + 22, 626, tx + 44, 648), fill=(255, 255, 255))
        for j in range(4):
            tx = wx0 + 300 + j * 60
            d.rounded_rectangle((tx, 704, tx + 40, 740), radius=6, fill=[(240, 214, 150), (200, 120, 90), (240, 214, 150), (130, 90, 70)][j])
    d.rounded_rectangle((1400, 500, 1530, GROUND), radius=10, fill=(26, 52, 84), outline=FRAME, width=5)
    d.rounded_rectangle((1420, 520, 1510, 700), radius=8, fill=(176, 212, 230))
    d.ellipse((1500, 690, 1516, 706), fill=FRAME)
    _awning(d, fx0 - 10, fx1 + 10, 466, 530, (250, 244, 232), BORDEAUX, stripes=18)
    bx = 1710
    d.line([(bx - 66, GROUND - 6), (bx - 20, 590)], fill=(100, 76, 56), width=7); d.line([(bx + 66, GROUND - 6), (bx + 20, 590)], fill=(100, 76, 56), width=7)
    d.rounded_rectangle((bx - 80, 600, bx + 80, 760), radius=8, fill=(44, 50, 54), outline=(150, 112, 78), width=8)
    d.text((bx, 636), "Pain frais", font=L.font(34), fill=CREAM, anchor="mm")
    for y in (680, 712):
        d.line([(bx - 56, y), (bx + 44, y)], fill=CREAM, width=4)
    _tree(d, 70, GROUND, 330, leaf=(108, 166, 98))


def _cafe(d, rng):
    W = L.W
    d.rectangle((0, 0, W, GROUND), fill=(238, 224, 196))
    d.rectangle((0, 0, W, 70), fill=(214, 196, 164))
    d.line([(0, 70), (W, 70)], fill=FRAME, width=6)
    d.rectangle((0, 520, W, GROUND), fill=(88, 54, 42))
    d.rectangle((0, 512, W, 526), fill=BRASS)
    for x in range(30, W, 120):
        d.rounded_rectangle((x, 548, x + 90, 780), radius=6, outline=(120, 78, 58), width=4)
    d.rounded_rectangle((100, 300, 290, GROUND), radius=14, fill=(68, 40, 32), outline=FRAME, width=6)
    d.rounded_rectangle((122, 330, 268, 600), radius=10, fill=(176, 208, 224))
    d.ellipse((262, 560, 278, 576), fill=FRAME)
    d.rounded_rectangle((340, 150, 640, 470), radius=14, fill=FRAME)
    d.rounded_rectangle((358, 168, 622, 452), radius=8, fill=(204, 222, 230))
    d.polygon([(380, 452), (470, 168), (520, 168), (430, 452)], fill=(228, 238, 242))
    d.text((490, 130), "Café", font=L.font(40), fill=(150, 110, 40), anchor="mm")
    _window_street(d, 720, 150, 1030, 500, rng)
    d.text((875, 118), "BRASSERIE", font=L.font(36), fill=(150, 110, 40), anchor="mm")
    d.rounded_rectangle((1110, 170, 1400, 430), radius=8, fill=(44, 50, 54), outline=(150, 112, 78), width=10)
    d.text((1255, 208), "Menu du jour", font=L.font(34), fill=CREAM, anchor="mm")
    for k, wlen in enumerate((200, 170, 220, 150)):
        d.line([(1140, 252 + k * 38), (1140 + wlen, 252 + k * 38)], fill=CREAM, width=4)
    for px in (500, 875, 1255):
        d.line([(px, 70), (px, 100)], fill=(60, 50, 44), width=4)
        d.ellipse((px - 26, 100, px + 26, 154), fill=(255, 240, 190), outline=BRASS, width=4)
    d.rounded_rectangle((330, 590, 700, 700), radius=24, fill=BORDEAUX)
    for bx in range(360, 690, 44):
        d.ellipse((bx - 5, 630, bx + 5, 640), fill=(90, 24, 34))
    for tx in (470, 760):
        _round_table(d, tx, GROUND - 6, r=62)
    for cx in (330, 620, 910):
        _bentwood(d, cx, GROUND - 6, 0.9)
    d.rectangle((1330, 360, 1900, 520), fill=(96, 62, 46))
    for sx in range(1350, 1890, 70):
        for sy in (380, 450):
            for j in range(3):
                d.rounded_rectangle((sx + j * 20, sy, sx + j * 20 + 12, sy + 54), radius=4, fill=rng.choice([(70, 120, 90), (150, 60, 60), (200, 170, 90), (90, 70, 130)]))
    d.rectangle((1330, 520, 1900, 534), fill=FRAME)
    d.rectangle((1360, 560, 1900, GROUND), fill=(96, 62, 46))
    d.rectangle((1340, 540, 1920, 574), fill=(184, 192, 200))
    d.rounded_rectangle((1700, 476, 1790, 540), radius=8, fill=(150, 150, 156))
    d.ellipse((1720, 496, 1740, 516), fill=(210, 210, 214)); d.ellipse((1750, 496, 1770, 516), fill=(210, 210, 214))
    for sx in (1440, 1560, 1680):
        d.ellipse((sx - 26, 690, sx + 26, 712), fill=BORDEAUX); d.rectangle((sx - 4, 712, sx + 4, GROUND - 6), fill=(60, 60, 68))


def _station(d, rng):
    W = L.W
    d.rectangle((0, 0, W, 560), fill=(238, 238, 232))
    for y in range(0, 560, 40):
        d.line([(0, y), (W, y)], fill=(214, 216, 214), width=2)
        for x in range((y // 40 % 2) * 40, W, 80):
            d.line([(x, y), (x, y + 40)], fill=(214, 216, 214), width=2)
    for k in range(9):
        x = k * 240
        d.polygon([(x, 0), (x + 30, 0), (x + 150, 70), (x + 120, 70)], fill=(226, 228, 224))
    d.rectangle((0, 0, W, 64), fill=(60, 120, 100))
    d.rectangle((0, 64, W, 76), fill=(34, 80, 66))
    for cx, name in ((560, "Châtelet"), (1160, "Bastille"), (1760, "Opéra")):
        d.rounded_rectangle((cx - 150, 140, cx + 150, 214), radius=8, fill=(30, 64, 130), outline=(240, 240, 240), width=4)
        d.text((cx, 177), name, font=L.font(46), fill=(250, 250, 250), anchor="mm")
        d.ellipse((cx - 190, 150, cx - 150, 190), fill=(250, 200, 60)); d.text((cx - 170, 170), "1", font=L.font(26), fill=(30, 30, 30), anchor="mm")
    d.rounded_rectangle((1280, 280, 1680, 440), radius=6, fill=(250, 244, 232), outline=(170, 160, 150), width=4)
    d.rectangle((1300, 300, 1660, 360), fill=(226, 120, 100)); d.text((1480, 330), "Exposition", font=L.font(36), fill=CREAM, anchor="mm")
    d.rectangle((1300, 380, 1560, 392), fill=(110, 100, 100)); d.rectangle((1300, 404, 1480, 414), fill=(150, 140, 140))
    d.rounded_rectangle((240, 270, 600, 440), radius=6, fill=(250, 250, 250), outline=(170, 170, 170), width=4)
    for pts, col in (([(270, 400), (360, 330), (450, 340), (570, 300)], (240, 200, 40)), ([(270, 300), (380, 360), (470, 420), (570, 400)], (60, 130, 200)),
                     ([(300, 420), (340, 300), (430, 290)], (100, 170, 90))):
        d.line(pts, fill=col, width=8)
    d.rectangle((0, 560, W, 700), fill=(52, 118, 96))
    d.rectangle((0, 560, W, 574), fill=(34, 80, 66)); d.rectangle((0, 690, W, 706), fill=(30, 70, 58))
    for x in range(40, W, 330):
        d.rounded_rectangle((x, 590, x + 150, 676), radius=10, fill=(184, 214, 226), outline=(34, 80, 66), width=4)
        d.rounded_rectangle((x + 170, 584, x + 250, 700), radius=6, fill=(176, 206, 220), outline=(34, 80, 66), width=4)
        d.line([(x + 210, 584), (x + 210, 700)], fill=(34, 80, 66), width=4)
    d.rectangle((0, 706, W, GROUND), fill=(176, 176, 172))
    d.rectangle((0, 722, W, 736), fill=(244, 206, 70))
    mx = 90
    d.rectangle((mx - 5, 130, mx + 5, 440), fill=WALLACE)
    d.arc((mx - 30, 110, mx + 140, 220), 180, 270, fill=WALLACE, width=7)
    d.rounded_rectangle((mx + 10, 82, mx + 170, 140), radius=12, fill=WALLACE)
    d.text((mx + 90, 111), "MÉTRO", font=L.font(36), fill=(250, 214, 110), anchor="mm")
    tx = int(0.12 * W)
    d.rounded_rectangle((tx - 52, 520, tx + 52, GROUND - 4), radius=8, fill=(70, 78, 90))
    d.rectangle((tx - 38, 540, tx + 38, 610), fill=(150, 206, 230))
    for j in range(3):
        d.rectangle((tx - 30 + j * 22, 640, tx - 12 + j * 22, 660), fill=(210, 210, 214))
    for gx in (int(0.2 * W) - 70, int(0.2 * W) + 40):
        d.rounded_rectangle((gx, 640, gx + 36, GROUND - 4), radius=6, fill=(150, 158, 168))
        d.rectangle((gx + 6, 650, gx + 30, 668), fill=(60, 200, 120))
    d.rounded_rectangle((1500, 700, 1800, 728), radius=6, fill=(120, 80, 56))
    for lx in (1520, 1770):
        d.rectangle((lx, 728, lx + 10, GROUND - 4), fill=(60, 60, 68))


def _park(d, rng):
    W = L.W
    for cx, cy, s in ((300, 120, 1.0), (1100, 90, 0.8), (1700, 140, 0.9)):
        _cloud(d, cx, cy, s)
    d.rectangle((300, 380, 1620, 640), fill=(234, 224, 204))
    d.polygon([(290, 380), (1630, 380), (1590, 330), (330, 330)], fill=(98, 112, 132))
    d.rectangle((880, 300, 1040, 380), fill=(234, 224, 204)); d.pieslice((880, 230, 1040, 370), 180, 360, fill=(98, 112, 132))
    d.line([(960, 232), (960, 196)], fill=(98, 112, 132), width=5)
    for wx in range(330, 1600, 70):
        for wy in (400, 480, 560):
            d.rectangle((wx, wy, wx + 30, wy + 52), fill=(172, 202, 226), outline=(130, 140, 154), width=2)
    d.rectangle((0, 610, W, 700), fill=(104, 160, 92))
    for hx in range(0, W, 200):
        d.rounded_rectangle((hx + 6, 640, hx + 184, 700), radius=18, fill=(80, 140, 78))
    for tx in (130, 420, 700, 1250, 1530, 1800):
        d.rectangle((tx - 10, 560, tx + 10, 720), fill=(110, 90, 76))
        d.rounded_rectangle((tx - 120, 420, tx + 120, 580), radius=60, fill=(88, 150, 84))
        d.rounded_rectangle((tx - 90, 400, tx + 90, 470), radius=40, fill=(104, 168, 98))
    d.ellipse((620, 690, 1300, 790), fill=(120, 176, 206), outline=(214, 208, 192), width=8)
    d.ellipse((760, 706, 1160, 770), fill=(148, 198, 224))
    d.rectangle((954, 640, 966, 730), fill=(190, 214, 226)); d.ellipse((930, 620, 990, 660), fill=(220, 236, 244))
    for cx in (260, 1560):
        for ox in (-70, 70):
            x = cx + ox
            d.arc((x - 36, 650, x + 36, 740), 180, 360, fill=(60, 110, 84), width=10)
            d.rounded_rectangle((x - 40, 736, x + 40, 750), radius=6, fill=(70, 124, 94))
            d.line([(x - 34, 750), (x - 40, 794)], fill=(60, 110, 84), width=7); d.line([(x + 34, 750), (x + 40, 794)], fill=(60, 110, 84), width=7)


def _restaurant(d, rng):
    W = L.W
    d.rectangle((0, 0, W, GROUND), fill=(244, 232, 206))
    d.rectangle((0, 0, W, 60), fill=(86, 52, 40)); d.line([(0, 60), (W, 60)], fill=FRAME, width=5)
    d.rectangle((0, 470, W, GROUND), fill=(40, 78, 66))
    d.rectangle((0, 462, W, 476), fill=BRASS)
    for x in range(40, W, 160):
        d.rounded_rectangle((x, 504, x + 120, 780), radius=6, outline=(64, 110, 92), width=4)
    d.rounded_rectangle((140, 110, 640, 420), radius=14, fill=FRAME)
    d.rounded_rectangle((160, 130, 620, 400), radius=8, fill=(206, 224, 232))
    d.polygon([(190, 400), (320, 130), (370, 130), (240, 400)], fill=(230, 240, 244))
    d.text((390, 94), "Bistro", font=L.font(40), fill=(150, 110, 40), anchor="mm")
    d.rounded_rectangle((760, 130, 1160, 410), radius=8, fill=(44, 50, 54), outline=(150, 112, 78), width=10)
    d.text((960, 176), "Plat du jour", font=L.font(42), fill=CREAM, anchor="mm")
    for k, wlen in enumerate((240, 200, 280, 180)):
        d.line([(800, 232 + k * 42), (800 + wlen, 232 + k * 42)], fill=CREAM, width=4)
    d.rectangle((1280, 140, 1860, 156), fill=(120, 80, 56))
    for x in range(1300, 1850, 46):
        d.rounded_rectangle((x, 102, x + 22, 140), radius=8, fill=rng.choice([(60, 100, 70), (110, 50, 60), (70, 90, 60)]))
        d.rectangle((x + 7, 88, x + 15, 104), fill=(60, 60, 60))
    d.rectangle((1280, 300, 1860, 316), fill=(120, 80, 56))
    for x in range(1300, 1850, 46):
        d.rounded_rectangle((x, 262, x + 22, 300), radius=8, fill=rng.choice([(60, 100, 70), (110, 50, 60), (70, 90, 60)]))
    for px in (460, 960, 1560):
        d.line([(px, 60), (px, 120)], fill=(60, 50, 44), width=4)
        d.polygon([(px - 46, 170), (px + 46, 170), (px + 24, 120), (px - 24, 120)], fill=(34, 80, 66))
        d.ellipse((px - 20, 156, px + 20, 184), fill=(255, 238, 180))
    for tx in (330, 760, 1190, 1620):
        _round_table(d, tx, GROUND - 6, r=74, cloth=((200, 54, 62), (250, 244, 240)))
        _bentwood(d, tx - 118, GROUND - 6, 0.95); _bentwood(d, tx + 118, GROUND - 6, 0.95)
        d.rounded_rectangle((tx - 12, 640, tx + 12, 690), radius=6, fill=(70, 110, 80))
        d.ellipse((tx + 24, 668, tx + 52, 684), fill=(250, 250, 250))


def _store(d, rng):
    W = L.W
    d.rectangle((0, 0, W, GROUND), fill=(240, 228, 204))
    d.rectangle((0, 0, W, 56), fill=(96, 64, 46)); d.line([(0, 56), (W, 56)], fill=FRAME, width=5)
    for k in range(4):
        y = 180 + k * 118
        d.rectangle((420, y + 88, 1500, y + 100), fill=(132, 90, 62))
        x = 440
        while x < 1480:
            w = rng.randint(34, 56); h = rng.randint(56, 84)
            col = rng.choice([(196, 60, 60), (230, 170, 60), (110, 160, 90), (230, 220, 200), (150, 100, 70), (80, 110, 160), (240, 130, 60)])
            d.rounded_rectangle((x, y + 88 - h, x + w, y + 88), radius=8, fill=col, outline=tuple(int(v * 0.75) for v in col), width=2)
            d.rectangle((x + 6, y + 88 - h * 0.6, x + w - 6, y + 88 - h * 0.35), fill=(250, 246, 236))
            x += w + rng.randint(6, 14)
    d.rounded_rectangle((120, 150, 380, 640), radius=8, fill=(116, 78, 56))
    d.rounded_rectangle((140, 176, 360, 470), radius=6, fill=(176, 208, 224))
    d.rounded_rectangle((200, 500, 300, 548), radius=8, fill=(250, 244, 232)); d.text((250, 524), "OUVERT", font=L.font(26), fill=BORDEAUX, anchor="mm")
    _awning(d, 1560, 1900, 150, 220, BORDEAUX, CREAM, stripes=8)
    d.rectangle((1520, 240, 1900, GROUND - 40), fill=(122, 82, 60))
    d.rectangle((1500, 520, 1920, 560), fill=(186, 140, 96))
    d.rounded_rectangle((1560, 440, 1680, 520), radius=8, fill=(86, 90, 100)); d.rectangle((1576, 452, 1664, 482), fill=(150, 206, 230))
    d.ellipse((1760, 470, 1850, 520), fill=(190, 196, 204))
    for cx, col in ((560, (226, 70, 70)), (780, (246, 190, 60)), (1000, (120, 190, 90)), (1220, (236, 130, 60))):
        d.rectangle((cx - 90, 690, cx + 90, 790), fill=(176, 130, 86), outline=(120, 84, 56), width=3)
        for j in range(6):
            d.ellipse((cx - 80 + j * 28, 662 + (j % 2) * 10, cx - 48 + j * 28, 700 + (j % 2) * 10), fill=col)


def _bookstore(d, rng):
    W = L.W
    for cx, cy, s in ((260, 130, 1.0), (1100, 100, 0.8), (1640, 160, 0.9)):
        _cloud(d, cx, cy, s)
    x = -20
    while x < W:
        w = rng.randint(200, 280)
        _building(d, x, w, 340 + rng.randint(0, 70), 560, rng.choice(STONE), rng.choice(ZINC), shutter=(150, 164, 180))
        x += w
    d.rectangle((0, 560, W, 660), fill=(122, 170, 200))
    for y in range(572, 650, 22):
        for x in range(rng.randint(0, 60), W, 150):
            d.line([(x, y), (x + 60, y)], fill=(176, 210, 230), width=3)
    d.polygon([(1180, 560), (1920, 560), (1920, 620), (1180, 620)], fill=(214, 204, 184))
    for ax in (1260, 1480, 1700):
        d.pieslice((ax - 90, 540, ax + 90, 700), 180, 360, fill=(122, 170, 200), outline=(190, 178, 156), width=6)
    d.rectangle((0, 650, W, 720), fill=(200, 190, 170))
    d.rectangle((0, 640, W, 660), fill=(176, 166, 146))
    for bx in (140, 640, 1140, 1640):
        d.rectangle((bx, 596, bx + 380, 720), fill=(40, 84, 70))
        d.polygon([(bx - 10, 596), (bx + 390, 596), (bx + 370, 566), (bx + 10, 566)], fill=(52, 104, 86))
        _books(d, bx + 14, 610, bx + 366, rng, rows=2, h=40)
        d.rectangle((bx, 700, bx + 380, 720), fill=(30, 70, 58))
    _tree(d, 70, 720, 420, leaf=(104, 164, 96)); _tree(d, 1880, 720, 400, leaf=(104, 164, 96))
    _lamp(d, 560, base=720, h=300)


def _classroom(d, rng):
    W = L.W
    d.rectangle((0, 0, W, GROUND), fill=(240, 232, 210))
    d.rectangle((0, 470, W, GROUND), fill=(150, 184, 164))
    d.rectangle((0, 462, W, 476), fill=(110, 140, 124))
    d.rounded_rectangle((560, 130, 1380, 430), radius=8, fill=(130, 90, 60))
    d.rounded_rectangle((580, 150, 1360, 410), radius=4, fill=(46, 92, 78))
    d.text((970, 214), "Bonjour !", font=L.font(76), fill=(244, 244, 236), anchor="mm")
    d.text((970, 296), "a  b  c  d  e  f  g", font=L.font(46), fill=(232, 236, 228), anchor="mm")
    d.line([(660, 350), (1000, 350)], fill=(232, 236, 228), width=4)
    d.text((1200, 352), "1 + 2 = 3", font=L.font(40), fill=(232, 236, 228), anchor="mm")
    d.rectangle((580, 410, 1360, 424), fill=(110, 76, 52))
    for k in range(4):
        d.rounded_rectangle((640 + k * 40, 396, 664 + k * 40, 410), radius=3, fill=rng.choice([(240, 240, 232), (240, 220, 120), (240, 160, 170)]))
    d.polygon([(240, 190), (330, 150), (410, 170), (430, 250), (400, 330), (320, 380), (240, 350), (210, 270)], fill=(236, 214, 156), outline=(150, 120, 80))
    d.text((320, 270), "France", font=L.font(30), fill=(120, 80, 50), anchor="mm")
    d.ellipse((312, 214, 330, 232), fill=BORDEAUX)
    for wx in (1480, 1700):
        _window_street(d, wx, 150, wx + 160, 560, rng)
    d.ellipse((130, 60, 210, 140), fill=(250, 250, 244), outline=(60, 60, 66), width=5)
    d.line([(170, 100), (170, 76)], fill=(60, 60, 66), width=4); d.line([(170, 100), (190, 104)], fill=(60, 60, 66), width=4)
    d.rounded_rectangle((60, 300, 200, 700), radius=10, fill=(120, 80, 56))
    d.rectangle((80, 330, 180, 520), fill=(176, 208, 224))
    for dx in (672, 1180, 1620):
        d.rounded_rectangle((dx - 150, 640, dx + 150, 668), radius=6, fill=(176, 128, 84), outline=(120, 84, 56), width=3)
        d.rectangle((dx - 140, 668, dx - 128, 790), fill=(100, 70, 50)); d.rectangle((dx + 128, 668, dx + 140, 790), fill=(100, 70, 50))
        d.rectangle((dx - 150, 700, dx + 150, 712), fill=(140, 100, 66))
        d.ellipse((dx - 100, 622, dx - 78, 640), fill=(60, 70, 130))
        d.rectangle((dx - 10, 630, dx + 60, 640), fill=(230, 80, 80))


def _home(d, rng):
    W = L.W
    d.rectangle((0, 0, W, GROUND), fill=(244, 236, 220))
    d.rectangle((0, 0, W, 54), fill=(232, 222, 202)); d.line([(0, 54), (W, 54)], fill=(206, 194, 170), width=6)
    for x in range(40, W, 380):
        d.rectangle((x, 100, x + 300, 520), outline=(216, 204, 180), width=5)
        d.rectangle((x + 14, 114, x + 286, 506), outline=(224, 214, 192), width=3)
    d.rectangle((0, 560, W, GROUND), fill=(232, 220, 198)); d.line([(0, 560), (W, 560)], fill=(206, 194, 170), width=5)
    wx0, wx1 = 700, 1180
    d.rounded_rectangle((wx0 - 20, 90, wx1 + 20, GROUND), radius=34, fill=(250, 246, 236), outline=(206, 194, 170), width=4)
    d.rounded_rectangle((wx0, 110, wx1, 790), radius=28, fill=(176, 212, 238))
    for k in range(3):
        d.ellipse((wx0 + 40 + k * 130, 150 + (k % 2) * 30, wx0 + 170 + k * 130, 198 + (k % 2) * 30), fill=(255, 255, 255))
    x = wx0
    while x < wx1:
        w = min(rng.randint(70, 120), wx1 - x)
        d.polygon([(x, 560), (x + w, 560), (x + w - 14, 500), (x + 14, 500)], fill=rng.choice(ZINC))
        d.rectangle((x + w // 3, 470, x + w // 3 + 18, 500), fill=(176, 120, 104))
        x += w
    d.rectangle((wx0, 560, wx1, 790), fill=(232, 226, 214))
    d.line([((wx0 + wx1) // 2, 110), ((wx0 + wx1) // 2, 790)], fill=(250, 246, 236), width=8)
    d.rectangle((wx0, 600, wx1, 616), fill=(56, 58, 68))
    for bx in range(wx0 + 6, wx1, 22):
        d.line([(bx, 616), (bx, 700)], fill=(56, 58, 68), width=4)
    d.rectangle((wx0, 700, wx1, 712), fill=(56, 58, 68))
    for cx in (wx0 - 50, wx1 + 50):
        d.polygon([(cx - 56, 90), (cx + 56, 90), (cx + 70, 790), (cx - 70, 790)], fill=(196, 150, 150))
        for k in range(-2, 3):
            d.line([(cx + k * 20, 90), (cx + k * 24, 790)], fill=(176, 126, 126), width=3)
    d.rounded_rectangle((1300, 520, 1840, 720), radius=36, fill=(104, 134, 170))
    d.rounded_rectangle((1280, 600, 1380, 740), radius=24, fill=(92, 120, 156)); d.rounded_rectangle((1760, 600, 1860, 740), radius=24, fill=(92, 120, 156))
    d.rectangle((1330, 720, 1830, 740), fill=(80, 106, 142))
    d.rounded_rectangle((1400, 560, 1490, 650), radius=14, fill=(226, 170, 90)); d.rounded_rectangle((1640, 560, 1730, 650), radius=14, fill=(196, 90, 100))
    d.rounded_rectangle((200, 170, 520, 440), radius=6, fill=FRAME)
    d.rectangle((218, 188, 502, 422), fill=(176, 206, 226)); d.polygon([(218, 422), (340, 300), (430, 380), (502, 330), (502, 422)], fill=(120, 164, 120))
    d.ellipse((420, 210, 480, 270), fill=(250, 214, 110))
    d.rounded_rectangle((300, 560, 440, 720), radius=10, fill=(176, 128, 84))
    d.polygon([(350, 560), (390, 560), (400, 500), (340, 500)], fill=(120, 164, 200))
    for k, c in enumerate(((226, 90, 110), (250, 200, 90), (240, 150, 170))):
        d.ellipse((330 + k * 22, 450 + (k % 2) * 16, 366 + k * 22, 486 + (k % 2) * 16), fill=c)
    d.rectangle((318, 720, 330, 790), fill=(120, 84, 56)); d.rectangle((410, 720, 422, 790), fill=(120, 84, 56))


NEW_DRAW = {"street": lambda d, rng: _street(d, rng, "street"), "town": lambda d, rng: _street(d, rng, "town"), "bakery": _bakery, "cafe": _cafe,
            "station": _station, "park": _park, "restaurant": _restaurant, "store": _store, "bookstore": _bookstore, "classroom": _classroom, "home": _home}
DRAW.update(NEW_DRAW)

SCENES.update({
    "street": dict(top=(176, 208, 240), bot=(250, 238, 222), floor=(188, 180, 168), table=(168, 160, 150), edge=(120, 112, 104)),
    "town": dict(top=(176, 208, 240), bot=(250, 238, 222), floor=(188, 180, 168), table=(168, 160, 150), edge=(120, 112, 104)),
    "bakery": dict(top=(182, 212, 240), bot=(250, 240, 226), floor=(196, 186, 172), table=(176, 128, 84), edge=(120, 84, 56)),
    "cafe": dict(top=(238, 224, 196), bot=(238, 224, 196), floor=(30, 30, 34), table=(184, 192, 200), edge=(120, 128, 136)),
    "station": dict(top=(238, 238, 232), bot=(238, 238, 232), floor=(176, 176, 172), table=(120, 80, 56), edge=(84, 54, 38)),
    "park": dict(top=(170, 206, 240), bot=(244, 240, 226), floor=(222, 206, 170), table=(70, 124, 94), edge=(44, 84, 64)),
    "restaurant": dict(top=(244, 232, 206), bot=(244, 232, 206), floor=(30, 30, 34), table=(200, 54, 62), edge=(140, 36, 44)),
    "store": dict(top=(240, 228, 204), bot=(240, 228, 204), floor=(190, 130, 96), table=(186, 140, 96), edge=(122, 82, 60)),
    "bookstore": dict(top=(176, 208, 240), bot=(250, 238, 222), floor=(196, 186, 166), table=(40, 84, 70), edge=(28, 62, 52)),
    "classroom": dict(top=(240, 232, 210), bot=(240, 232, 210), floor=(184, 140, 100), table=(176, 128, 84), edge=(120, 84, 56)),
    "home": dict(top=(244, 236, 220), bot=(244, 236, 220), floor=(190, 140, 100), table=(176, 128, 84), edge=(120, 84, 56)),
})
KEYWORDS.update({
    "bakery": ["boulangerie", "baguette", "pain", "pâtisserie", "patisserie", "bakery", "bread", "pastry", "croissant"],
    "cafe": ["café", "cafe", "thé", "chocolat chaud", "coffee", "tea", "hot chocolate", "brasserie"],
    "street": ["rue", "boulevard", "avenue", "nuit", "soir", "bonsoir", "ville", "night", "evening", "street", "directions"],
    "station": ["métro", "metro", "gare", "train", "billet", "quai", "bus", "station", "ticket", "platform"],
    "park": ["parc", "promenade", "jardin", "luxembourg", "météo", "soleil", "park", "walk", "garden", "weather", "sunny"],
    "bookstore": ["librairie", "livre", "bouquiniste", "seine", "bibliothèque", "bibliotheque", "book", "library", "river"],
})
ALIASES.update({"bakery": "bakery", "boulangerie": "bakery", "bread": "bakery", "patisserie": "bakery", "pâtisserie": "bakery",
                "metro": "station", "métro": "station", "subway": "station", "garden": "park", "luxembourg": "park", "jardin": "park",
                "seine": "bookstore", "bouquiniste": "bookstore", "brasserie": "cafe", "école": "classroom", "ecole": "classroom",
                "apartment": "home", "appartement": "home", "épicerie": "store", "epicerie": "store"})
LANDMARKS.update({"classroom": {"door": 0.1, "blackboard": 0.5, "desk": 0.35}, "cafe": {"counter": 0.8, "window": 0.45, "door": 0.1},
                  "station": {"platform": 0.5, "ticket gate": 0.2, "ticket machine": 0.12}, "store": {"register": 0.8, "shelf": 0.5, "door": 0.1}})
OUTDOOR.update({"street", "town", "bakery", "park", "bookstore"})
BIRD_SCENES.update({"street", "town", "bakery", "park", "bookstore"})


def _floor_pave(d, rng, W=1920, y0=GROUND, y1=1080, base=(196, 188, 176)):
    for r, y in enumerate(range(y0, y1, 34)):
        off = 0 if r % 2 == 0 else 34
        for x in range(-off, W, 68):
            tone = rng.randint(-14, 10)
            d.rounded_rectangle((x + 3, y + 3, x + 65, y + 31), radius=8, fill=tuple(max(0, min(255, v + tone)) for v in base))


def _floor_checker(d, W=1920, y0=GROUND, y1=1080):
    for r, y in enumerate(range(y0, y1, 56)):
        for c, x in enumerate(range(0, W, 112)):
            d.rectangle((x, y, x + 112, y + 56), fill=(244, 242, 236) if (r + c) % 2 == 0 else (34, 34, 40))


def _floor_parquet(d, rng, W=1920, y0=GROUND, y1=1080, base=(190, 140, 100)):
    for r, y in enumerate(range(y0, y1, 46)):
        for x in range(-(r % 2) * 90, W, 180):
            tone = rng.randint(-14, 12)
            d.rectangle((x + 2, y + 2, x + 178, y + 44), fill=tuple(max(0, min(255, v + tone)) for v in base), outline=tuple(int(v * 0.8) for v in base))
            d.line([(x + 90, y + 2), (x + 90, y + 44)], fill=tuple(int(v * 0.85) for v in base), width=2)


def _floor_gravel(d, rng, W=1920, y0=GROUND, y1=1080):
    for _ in range(2600):
        x, y = rng.randint(0, W), rng.randint(y0, y1)
        r = rng.randint(2, 5); t = rng.randint(-26, 20)
        d.ellipse((x, y, x + r * 2, y + r), fill=(210 + t, 194 + t, 156 + t))


def _floor_tile(d, W=1920, y0=GROUND, y1=1080):
    for y in range(y0, y1, 70):
        d.line([(0, y), (W, y)], fill=(150, 150, 146), width=3)
    for x in range(0, W, 140):
        d.line([(x, y0), (x, y1)], fill=(150, 150, 146), width=3)


FLOOR = {"street": lambda d, rng: _floor_pave(d, rng), "town": lambda d, rng: _floor_pave(d, rng), "bakery": lambda d, rng: _floor_pave(d, rng),
         "terrace": lambda d, rng: _floor_pave(d, rng), "market": lambda d, rng: _floor_pave(d, rng, base=(196, 182, 156)),
         "bookstore": lambda d, rng: _floor_pave(d, rng, base=(204, 194, 174)), "cafe": lambda d, rng: _floor_checker(d), "restaurant": lambda d, rng: _floor_checker(d),
         "classroom": lambda d, rng: _floor_parquet(d, rng), "home": lambda d, rng: _floor_parquet(d, rng, base=(196, 150, 112)),
         "store": lambda d, rng: _floor_parquet(d, rng, base=(190, 130, 96)), "park": lambda d, rng: _floor_gravel(d, rng), "station": lambda d, rng: _floor_tile(d)}


def draw_short(scene, bg, rng, top=275, ground=885):
    """Shorts: draw the landscape scene off-screen, scale it and crop it to the vertical frame."""
    from PIL import Image, ImageDraw
    lay = Image.new("RGBA", (1920, GROUND), (0, 0, 0, 0))
    save = L.W
    L.W = 1920
    try:
        DRAW[scene](ImageDraw.Draw(lay), rng)
    finally:
        L.W = save
    s = (ground - top) / GROUND
    lay = lay.resize((int(1920 * s), ground - top), Image.LANCZOS)
    x0 = (lay.width - 1080) // 2
    lay = lay.crop((x0, 0, x0 + 1080, lay.height))
    bg.paste(lay, (0, top), lay)


SHORT_SCENES = set(DRAW)
SHORT_DRAW = {}            # kept empty: Shorts use draw_short()
