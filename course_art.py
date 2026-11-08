#!/usr/bin/env python3
"""Tiny French course art: course covers (16:9), lesson-video thumbnails (16:9) and the vertical poster of the free video.

One design system for everything: a scene from the lesson engine (blurred) behind a coloured wave panel with the title,
Marinette and Adrien as outlined stickers, and a round emoji badge. Each course has its own colour.

Usage (from the repository root):
    python course_art.py thumbs  [out_dir]    # 42 lesson thumbnails  -> <stem>.thumbnail.png  (1280x720)
    python course_art.py covers  [out_dir]    # 8 course covers       -> cover-*.png           (1500x843)
    python course_art.py poster  [out_dir]    # vertical poster of the free video (1080x1920)
    python course_art.py all     [out_dir]
Needs assets/course_art/ (Poppins fonts, Twemoji icons, lessons.json). Fonts: SIL OFL. Icons: Twemoji, CC-BY 4.0.
"""
import json, math, os, sys
import numpy as np
from scipy import ndimage as ndi
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "assets", "course_art")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "story"))   # the story engine has the full set of scenes
_argv = sys.argv
sys.argv = sys.argv[:1]
import lesson as L            # noqa: E402  (scene painter)
import characters as CH       # noqa: E402  (Adrien and Marinette)
sys.argv = _argv

W, H = 1920, 1080

THEMES = {
    "free-lessons":                     dict(main=(222, 70, 134), dark=(140, 28, 88),  tint=(255, 224, 238), scene="eiffel",    pill="FREE LESSONS"),
    "first-conversations":              dict(main=(16, 150, 148), dark=(6, 88, 102),   tint=(208, 250, 244), scene="terrace",   pill="FIRST CONVERSATIONS"),
    "french-sounds-starter":            dict(main=(122, 86, 224), dark=(66, 38, 156),  tint=(232, 224, 255), scene="bookstore", pill="FRENCH SOUNDS"),
    "everyday-french":                  dict(main=(214, 108, 16), dark=(150, 60, 8),   tint=(255, 234, 200), scene="town",      pill="EVERYDAY FRENCH"),
    "french-grammar-starter":           dict(main=(44, 98, 224),  dark=(20, 48, 148),  tint=(216, 232, 255), scene="classroom", pill="FRENCH GRAMMAR"),
    "real-life-french":                 dict(main=(36, 142, 80),  dark=(16, 90, 52),   tint=(214, 247, 226), scene="market",    pill="REAL-LIFE FRENCH"),
    "travel-french":                    dict(main=(222, 78, 60),  dark=(146, 34, 34),  tint=(255, 226, 218), scene="airport",   pill="TRAVEL FRENCH"),
    "from-zero-to-first-conversations": dict(main=(58, 72, 138),  dark=(28, 36, 90),   tint=(224, 228, 255), scene="river",     pill="COMING SOON"),
}

COVERS = {  # id -> file, main title, subtitle, level chip, right chip, icon strip (lesson emoji files or None = the course's lessons)
    "free-lessons":                     ("cover-free-lessons.png",          "Free French Lessons",             "Short dialogues with Marinette and Adrien, vocabulary and quizzes", "A1", "7 FREE LESSONS", ["1f44b", "1f956", "1f9ed", "1f686", "1f37d", "1f6d2", "2708"]),
    "first-conversations":              ("cover-first-conversations.png",   "First Conversations",             "Greetings, cafés, directions and your first real chats",           "A1", "7 VIDEO LESSONS", None),
    "french-sounds-starter":            ("cover-french-sounds.png",         "French Sounds Starter",           "Accents, nasal vowels and the French u and r",                      "A1", "7 VIDEO LESSONS", None),
    "everyday-french":                  ("cover-everyday-french.png",       "Everyday French",                 "Time and plans: days, hours, weather and the hotel",                "A1", "7 VIDEO LESSONS", None),
    "french-grammar-starter":           ("cover-french-grammar.png",        "French Grammar Starter",          "Être, avoir, questions and describing things",                      "A1", "7 VIDEO LESSONS", None),
    "real-life-french":                 ("cover-real-life-french.png",      "Real-Life French",                "Daily routines and errands, from the market to the phone",          "A1–A2", "7 VIDEO LESSONS", None),
    "travel-french":                    ("cover-travel-french.png",         "Travel French",                   "Getting around and getting help on your trip",                      "A1–A2", "7 VIDEO LESSONS", None),
    "from-zero-to-first-conversations": ("cover-zero-to-conversations.png", "From Zero to Your First Conversations", "A step-by-step beginner course, built on the free lessons",       "A1", "COMING SOON", ["1f524", "1f44b", "1f522", "1f4da", "1f9e9", "2753", "2615", "1f4ac"]),
}

LESSON_SCENE = {
    "greetings-through-the-day": "street", "introducing-yourself": "terrace", "numbers-and-prices": "store", "ordering-at-the-cafe": "cafe",
    "asking-for-directions": "town", "family-and-friends": "park", "buying-a-train-ticket": "station",
    "accents-and-the-alphabet": "classroom", "silent-letters-and-liaison": "bookstore", "nasal-vowels": "schoolyard", "the-french-u-and-r": "classroom",
    "reading-signs-and-menus": "restaurant", "vowel-combinations": "bookstore", "rhythm-and-questions": "festival",
    "days-and-today": "home", "telling-the-time": "station", "likes-and-dislikes": "market", "making-plans": "amusement",
    "asking-for-help": "street", "weather-and-seasons": "beach", "at-the-hotel": "town",
    "the-verb-etre": "schoolyard", "the-verb-avoir": "store", "articles-and-gender": "bakery", "regular-er-verbs": "park",
    "saying-no": "restaurant", "asking-questions": "cafe", "adjectives-and-agreement": "kitchen",
    "my-morning-routine": "bedroom", "at-the-market": "market", "at-the-pharmacy": "hospital", "on-the-phone": "home",
    "work-and-study": "classroom", "what-did-you-do": "beach", "booking-a-table": "restaurant",
    "taking-a-taxi": "street", "shopping-for-clothes": "store", "at-the-museum": "town", "lost-wallet": "station",
    "at-the-post-office": "street", "renting-a-bike": "park", "wifi-and-sim": "airport",
}
SHORT = {"first-conversations": "FIRST CONVERSATIONS", "french-sounds-starter": "FRENCH SOUNDS", "everyday-french": "EVERYDAY FRENCH",
         "french-grammar-starter": "FRENCH GRAMMAR", "real-life-french": "REAL-LIFE FRENCH", "travel-french": "TRAVEL FRENCH"}

WHITE = (255, 255, 255)


# ---------------------------------------------------------------- helpers
def font(weight, size):
    return ImageFont.truetype(os.path.join(ART, "fonts", f"Poppins-{weight}.ttf"), int(size))


def mix(a, b, t):
    return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))


def lum(c):
    f = lambda v: (v / 255 / 12.92) if v / 255 <= 0.03928 else (((v / 255) + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


_scene_cache = {}
def scene_image(name):
    if name not in _scene_cache:
        _scene_cache[name] = L.make_scene(name)[0].convert("RGB")
    return _scene_cache[name].copy()


def scene_bg(name, w, h, blur=5, focus=0.5):
    im = scene_image(name)
    s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s + 0.5), int(im.height * s + 0.5)), Image.LANCZOS)
    x0 = int((im.width - w) * focus); y0 = (im.height - h) // 2
    im = im.crop((x0, y0, x0 + w, y0 + h)).filter(ImageFilter.GaussianBlur(blur))
    return ImageEnhance.Color(im).enhance(1.08)


def wrap_options(words, n):
    """All ways to split words into n lines (as lists of strings)."""
    if n == 1:
        return [[" ".join(words)]]
    out = []
    for i in range(1, len(words) - n + 2):
        for rest in wrap_options(words[i:], n - 1):
            out.append([" ".join(words[:i])] + rest)
    return out


def fit_text(text, weight, max_w, max_h, sizes, max_lines, lh=1.1):
    """Largest size (then fewest lines) whose most balanced wrap fits the box. Returns (lines, font, size, line_height)."""
    words = text.split()
    for size in sizes:
        f = font(weight, size)
        for n in range(1, min(max_lines, len(words)) + 1):
            best = None
            for opt in wrap_options(words, n):
                widths = [f.getlength(x) for x in opt]
                score = (max(widths), max(widths) - min(widths))
                if best is None or score < best[0]:
                    best = (score, opt)
            if best and best[0][0] <= max_w and (0.72 * size + (n - 1) * size * lh + 0.25 * size) <= max_h:
                return best[1], f, size, size * lh
    f = font(weight, sizes[-1]); words = text.split()
    raise ValueError(f"text does not fit: {text!r}")


def fit_title_sub(title, sub, maxw, avail_h, title_sizes, sub_sizes, title_lines=3, sub_lines=2, gap=26, sub_weight="MediumItalic"):
    """Biggest title that still leaves room for the subtitle inside avail_h. Returns ((lines,f,size,lh),(lines,f,size,lh), total_h)."""
    for ts in title_sizes:
        try:
            t = fit_text(title, "ExtraBold", maxw, 10 ** 6, [ts], title_lines, 1.06)
        except ValueError:
            continue
        for ss in sub_sizes:
            try:
                u = fit_text(sub, sub_weight, maxw, 10 ** 6, [ss], sub_lines, 1.18)
            except ValueError:
                continue
            total = block_height(t[0], t[2], t[3]) + gap + block_height(u[0], u[2], u[3])
            if total <= avail_h:
                return t, u, total
            break
    raise ValueError(f"title/subtitle do not fit: {title!r}")


def block_height(lines, size, lh):
    return 0.72 * size + (len(lines) - 1) * lh + 0.25 * size


def draw_lines(im, lines, f, size, lh, x, y_top, fill, shadow=70, blur=5, off=6, anchor_x="l"):
    """Baseline-positioned text block with a soft shadow. Returns bottom y of the block."""
    lay = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(lay)
    sx = x
    base0 = y_top + 0.72 * size
    for i, t in enumerate(lines):
        d.text((sx, base0 + i * lh + off), t, font=f, fill=255, anchor="l" + "s" if anchor_x == "l" else "ms")
    lay = lay.filter(ImageFilter.GaussianBlur(blur))
    sh = Image.new("RGBA", im.size, (10, 6, 30, 0)); sh.putalpha(lay.point(lambda v: int(v * shadow / 255)))
    im.alpha_composite(sh)
    d = ImageDraw.Draw(im)
    for i, t in enumerate(lines):
        d.text((sx, base0 + i * lh), t, font=f, fill=fill, anchor="l" + "s" if anchor_x == "l" else "ms")
    return y_top + block_height(lines, size, lh)


def pill(im, x, cy, text, size, fg, bg, padx=None, weight="Bold", outline=None, outline_w=4):
    f = font(weight, size)
    padx = padx if padx is not None else int(size * 0.8)
    tw = f.getlength(text)
    h = int(size * 1.9)
    w = int(tw + 2 * padx)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((x, cy - h / 2, x + w, cy + h / 2), radius=h / 2, fill=bg, outline=outline, width=outline_w if outline else 0)
    d.text((x + w / 2, cy + 0.35 * size), text, font=f, fill=fg, anchor="ms")
    im.alpha_composite(lay)
    return x + w, h


def flag(im, x, cy, w=64, h=44):
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rectangle((0, 0, w // 3, h), fill=(0, 85, 164)); d.rectangle((w // 3, 0, 2 * w // 3, h), fill=(255, 255, 255)); d.rectangle((2 * w // 3, 0, w, h), fill=(239, 65, 53))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=10, fill=255)
    lay.putalpha(m)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); 
    ms = Image.new("L", im.size, 0); ImageDraw.Draw(ms).rounded_rectangle((x, cy - h / 2 + 4, x + w, cy + h / 2 + 4), radius=10, fill=110)
    sh.putalpha(ms.filter(ImageFilter.GaussianBlur(5))); im.alpha_composite(sh)
    im.alpha_composite(lay, (int(x), int(cy - h / 2)))
    d = ImageDraw.Draw(im); d.rounded_rectangle((x, cy - h / 2, x + w, cy + h / 2), radius=10, outline=(255, 255, 255, 230), width=3)


def wordmark(im, x, cy, size=40):
    flag(im, x, cy)
    f = font("ExtraBold", size)
    lines = ["TINY FRENCH"]
    lay = Image.new("L", im.size, 0); ImageDraw.Draw(lay).text((x + 84, cy + 0.35 * size + 4), lines[0], font=f, fill=255, anchor="ls")
    sh = Image.new("RGBA", im.size, (10, 6, 30, 0)); sh.putalpha(lay.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.5))); im.alpha_composite(sh)
    ImageDraw.Draw(im).text((x + 84, cy + 0.35 * size), lines[0], font=f, fill=WHITE, anchor="ls")


def sticker(img, outline=12, shadow_alpha=100, shadow_dy=12, blur=16):
    """Sprite with a white outline and a soft shadow. Returns (image, pad)."""
    w, h = img.size
    pad = outline + blur * 3 + shadow_dy
    a = np.zeros((h + 2 * pad, w + 2 * pad), np.uint8)
    a[pad:pad + h, pad:pad + w] = np.array(img.getchannel("A"))
    dist = ndi.distance_transform_edt(a < 128)
    dil = (np.clip(outline + 0.5 - dist, 0, 1) * 255).astype(np.float32)
    dil = ndi.gaussian_filter(dil, 0.8)
    sh = ndi.gaussian_filter(dil, blur) * shadow_alpha / 255
    sh = np.roll(sh, shadow_dy, axis=0)
    dil = np.clip(dil, 0, 255).astype(np.uint8)
    out = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    shl = Image.new("RGBA", out.size, (24, 14, 50, 0)); shl.putalpha(Image.fromarray(np.clip(sh, 0, 255).astype(np.uint8)))
    out.alpha_composite(shl)
    wl = Image.new("RGBA", out.size, (255, 255, 255, 0)); wl.putalpha(Image.fromarray(dil))
    out.alpha_composite(wl)
    out.alpha_composite(img, (pad, pad))
    return out, pad


def character(name, scale, mouth=1):
    sp = CH.portrait(name, mouth, False).convert("RGBA")
    sp = sp.resize((int(sp.width * scale + 0.5), int(sp.height * scale + 0.5)), Image.LANCZOS)
    return sp


def place_character(im, name, center_x, bottom_y, scale, mouth=1):
    sp = character(name, scale, mouth)
    st, pad = sticker(sp)
    bx = (68 + 436) / 2 * scale if name == "Marinette" else (61 + 443) / 2 * scale
    x = int(center_x - bx - pad); y = int(bottom_y - sp.height - pad)
    paste_clipped(im, st, x, y)


def paste_clipped(im, src, x, y):
    big = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sx0, sy0 = max(0, -x), max(0, -y)
    cw = min(src.width - sx0, im.width - max(x, 0)); ch = min(src.height - sy0, im.height - max(y, 0))
    if cw > 0 and ch > 0:
        big.paste(src.crop((sx0, sy0, sx0 + cw, sy0 + ch)), (max(x, 0), max(y, 0)))
        im.alpha_composite(big)


def emoji_badge(im, cx, cy, radius, emoji_file, ring):
    """White round badge with a coloured ring, a shadow and the lesson's emoji."""
    pad = 60
    d_ = radius * 2
    lay = Image.new("RGBA", (d_ + 2 * pad, d_ + 2 * pad), (0, 0, 0, 0))
    m = Image.new("L", lay.size, 0); ImageDraw.Draw(m).ellipse((pad, pad + 10, pad + d_, pad + d_ + 10), fill=120)
    sh = Image.new("RGBA", lay.size, (24, 14, 50, 0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(14))); lay.alpha_composite(sh)
    d = ImageDraw.Draw(lay)
    d.ellipse((pad, pad, pad + d_, pad + d_), fill=(255, 255, 255, 255))
    rw = max(8, radius // 9)
    d.ellipse((pad + rw, pad + rw, pad + d_ - rw, pad + d_ - rw), outline=ring + (255,), width=rw)
    e = Image.open(os.path.join(ART, "emoji", emoji_file)).convert("RGBA")
    es = int(radius * 1.12)
    e = e.resize((es, es), Image.LANCZOS)
    lay.alpha_composite(e, (pad + radius - es // 2, pad + radius - es // 2 + 3))
    im.alpha_composite(lay, (int(cx - radius - pad), int(cy - radius - pad)))


# ---------------------------------------------------------------- panel
def panel(im_rgb, theme, mode="left", base=None, amp=None, w=None, h=None, phase=0.0):
    """Coloured wave panel over a scene. mode 'left' = vertical wave edge on the right side, 'top' = wave edge along the bottom."""
    w, h = im_rgb.size
    a = np.asarray(im_rgb).astype(np.float32)
    ys = np.arange(h, dtype=np.float32)[:, None]; xs = np.arange(w, dtype=np.float32)[None, :]
    if mode == "left":
        edge = base + amp * np.sin(2 * np.pi * 0.9 * ys / h + phase)
        m = np.clip(edge - xs + 0.5, 0, 1)
        t = (ys / h)[..., None] * np.ones((1, w, 1), np.float32)
        edge_pts = [(float(edge[y, 0]), y) for y in range(0, h, 4)]
    else:
        edge = base + amp * np.sin(2 * np.pi * 1.1 * xs / w + phase)
        m = np.clip(edge - ys + 0.5, 0, 1)
        t = (ys / h)[..., None] * np.ones((1, w, 1), np.float32)
        edge_pts = [(x, float(edge[0, x])) for x in range(0, w, 4)]
    top = np.array(mix(theme["main"], theme["dark"], 0.18), np.float32)[None, None, :]
    bot = np.array(mix(theme["main"], theme["dark"], 0.95), np.float32)[None, None, :]
    tt = t if mode == "left" else np.clip(ys / (base + amp), 0, 1)[..., None] * np.ones((1, w, 1), np.float32)
    fill = top * (1 - tt) + bot * tt
    alpha = (m * 0.97)[..., None]
    out = a * (1 - alpha) + fill * alpha
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")
    # decoration inside the panel: soft rings and a dot grid
    deco = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(deco)
    tint = theme["tint"]
    if mode == "left":
        d.ellipse((-220, h - 420, 380, h + 180), outline=tint + (46,), width=44)
        d.ellipse((w * 0.30, -160, w * 0.30 + 380, 220), outline=tint + (34,), width=30)
        for gx in range(0, 7):
            for gy in range(0, 5):
                cx, cy = 560 + gx * 46, 820 + gy * 46
                d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=tint + (60,))
    else:
        d.ellipse((-160, -160, 380, 380), outline=tint + (46,), width=40)
        d.ellipse((w - 380, 120, w + 120, 620), outline=tint + (34,), width=34)
    dm = Image.fromarray((m * 255).astype(np.uint8))
    deco.putalpha(Image.fromarray((np.asarray(deco.getchannel("A")).astype(np.float32) * m).astype(np.uint8)))
    img.alpha_composite(deco)
    # white highlight line just inside the edge
    hl = Image.new("RGBA", (w, h), (0, 0, 0, 0)); hd = ImageDraw.Draw(hl)
    if mode == "left":
        hd.line([(x - 22, y) for x, y in edge_pts], fill=(255, 255, 255, 215), width=8, joint="curve")
    else:
        hd.line([(x, y - 22) for x, y in edge_pts], fill=(255, 255, 255, 215), width=8, joint="curve")
    img.alpha_composite(hl)
    return img


def vignette(im, strength=0.16):
    w, h = im.size
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    v = ((xs - w / 2) / (w / 2)) ** 2 + ((ys - h / 2) / (h / 2)) ** 2
    k = 1 - strength * np.clip(v - 0.35, 0, 1.6)
    a = np.asarray(im.convert("RGB")).astype(np.float32) * k[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")


def to_png(im, path, size, colors=224):
    im = im.convert("RGB").resize(size, Image.LANCZOS)
    q = im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    q.save(path, optimize=True)
    return os.path.getsize(path)


# ---------------------------------------------------------------- designs
def lesson_thumbnail(meta, course_theme_id, number, total, out_path, size=(1280, 720)):
    th = THEMES[course_theme_id]
    bg = scene_bg(LESSON_SCENE[meta["id"]], W, H, blur=5)
    im = panel(bg, th, "left", base=1040, amp=64, phase=0.6)
    im = vignette(im, 0.10)
    place_character(im, "Marinette", 1245, H + 36, 1.38, mouth=1)
    place_character(im, "Adrien", 1655, H + 36, 1.38, mouth=1)
    emoji_badge(im, 96 + 150, 872, 150, meta["emoji_file"], th["main"])
    # text zone
    X0, MAXW = 96, 840
    cy = 112
    r, ph = pill(im, X0, cy, SHORT.get(course_theme_id, th["pill"]), 30, th["dark"], WHITE + (255,))
    pill(im, r + 16, cy, f"LESSON {number}", 30, WHITE, (255, 255, 255, 56), outline=(255, 255, 255, 235), outline_w=3)
    (lines, f, sz, lh), (fr_lines, ff, fsz, flh), tot = fit_title_sub(meta["title"], meta["fr"], MAXW, 490, list(range(188, 80, -4)), list(range(64, 38, -2)))
    ytop = 198 + (490 - tot) / 2
    y = draw_lines(im, lines, f, sz, lh, X0, ytop, WHITE)
    y2 = draw_lines(im, fr_lines, ff, fsz, flh, X0, y + 26, th["tint"], shadow=60, blur=4, off=4)
    assert y2 <= 690, (meta["id"], y2)
    wordmark(im, 96 + 300 + 34, 872)
    return to_png(im, out_path, size)


def course_cover(cid, lessons, out_path, size=(1500, 843)):
    th = THEMES[cid]
    fname, main, sub, level, chip, strip = COVERS[cid]
    bg = scene_bg(th["scene"], W, H, blur=5)
    im = panel(bg, th, "left", base=1090, amp=70, phase=0.2)
    im = vignette(im, 0.10)
    place_character(im, "Marinette", 1275, H + 36, 1.42, mouth=1)
    place_character(im, "Adrien", 1650, H + 36, 1.42, mouth=1)
    X0, MAXW = 96, 900
    wordmark(im, X0, 100)
    (lines, f, sz, lh), (sl, sf, ssz, slh), tot = fit_title_sub(main, sub, MAXW, 500, list(range(168, 80, -4)), list(range(50, 34, -2)), sub_lines=3, gap=24, sub_weight="SemiBold")
    ytop = 190 + (500 - tot) / 2
    y = draw_lines(im, lines, f, sz, lh, X0, ytop, WHITE)
    y2 = draw_lines(im, sl, sf, ssz, slh, X0, y + 24, th["tint"], shadow=60, blur=4, off=4)
    assert y2 <= 700, (cid, y2)
    # chips
    cy = 770
    r, _ = pill(im, X0, cy, level, 32, th["dark"], WHITE + (255,), weight="ExtraBold")
    pill(im, r + 16, cy, chip, 32, WHITE, (255, 255, 255, 56), outline=(255, 255, 255, 235), outline_w=3)
    # icon strip: what is inside
    files = strip if strip else [l["emoji_file"][:-4] for l in lessons if l["course"] == cid]
    n = len(files); gap = 16; d = min(104, int((MAXW - (n - 1) * gap) / n))
    total = n * d + (n - 1) * gap
    assert total <= MAXW + 20, (cid, total)
    for i, ef in enumerate(files):
        cx = X0 + d / 2 + i * (d + gap)
        emoji_badge(im, cx, 930, d // 2, ef + ".png", th["main"])
    return to_png(im, out_path, size)


def poster_vertical(meta, out_path, size=(1080, 1920), theme_id="free-lessons"):
    th = THEMES[theme_id]
    w, h = 1080, 1920
    bg = scene_bg(meta.get("scene", "cafe"), w, h, blur=6)
    im = panel(bg, th, "top", base=900, amp=50, phase=0.4)
    im = vignette(im, 0.10)
    place_character(im, "Marinette", 300, h + 36, 1.46, mouth=1)
    place_character(im, "Adrien", 790, h + 36, 1.46, mouth=1)
    X0, MAXW = 80, 920
    wordmark(im, X0, 110)
    pill(im, X0, 205, meta["pill"], 34, th["dark"], WHITE + (255,))
    (lines, f, sz, lh), (fr_lines, ff, fsz, flh), tot = fit_title_sub(meta["title"], meta["fr"], MAXW, 500, list(range(168, 80, -4)), list(range(66, 44, -2)))
    ytop = 290 + (500 - tot) / 2
    y = draw_lines(im, lines, f, sz, lh, X0, ytop, WHITE)
    y2 = draw_lines(im, fr_lines, ff, fsz, flh, X0, y + 26, th["tint"], shadow=60, blur=4, off=4)
    assert y2 <= 810, y2
    return to_png(im, out_path, size)


# ---------------------------------------------------------------- cli
def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "output", "course_art")
    os.makedirs(out, exist_ok=True)
    lessons = json.load(open(os.path.join(ART, "lessons.json"), encoding="utf-8"))
    if what in ("thumbs", "all"):
        for l in lessons:
            p = os.path.join(out, l["stem"] + ".thumbnail.png")
            print(l["stem"], lesson_thumbnail(l, l["course"], l["number"], 7, p) // 1024, "KB"); _scene_cache.clear()
    if what in ("covers", "all"):
        for cid, spec in COVERS.items():
            p = os.path.join(out, spec[0])
            print(spec[0], course_cover(cid, lessons, p) // 1024, "KB"); _scene_cache.clear()
    if what in ("poster", "all"):
        meta = dict(title="Meeting for the First Time", fr="Faire connaissance", pill="FREE LESSON 1", scene="cafe")
        p = os.path.join(out, "poster-meeting-for-the-first-time.png")
        print(p, poster_vertical(meta, p) // 1024, "KB")


if __name__ == "__main__":
    main()
