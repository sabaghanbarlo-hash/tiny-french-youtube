#!/usr/bin/env python3
"""Tiny French course art v3 = the SAME look as the YouTube videos.

* Lesson thumbnails: story/make_cover.py, run on each course lesson's own script (scene, Marinette and Adrien from the
  story rig, title banner, TINY FRENCH pill). Exactly what the lesson gets on YouTube.
* Course covers: the same recipe (scene + rig characters + banner + brand pill) with the course title, a colour per course
  and a level / lesson-count pill. Text sits inside the safe zone because the website crops covers to a wide card.

    python course_art_v3.py thumbs [out_dir]    # 42 lesson thumbnails -> <stem>.thumbnail.png (1280x720)
    python course_art_v3.py covers [out_dir]    # 8 covers -> cover-*.png (1500x843)
Needs resvg-py (pip install resvg-py) for the real character rig.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "story"))
_argv = sys.argv; sys.argv = sys.argv[:1]
import make_cover as MC           # noqa: E402  (the YouTube cover maker)
sys.argv = _argv
import rigsvg                      # noqa: E402
from PIL import Image, ImageDraw, ImageFilter   # noqa: E402

L, A = MC.L, MC.A
W, H = MC.W, MC.H
THEMES = {   # course -> (accent colour, scene, level, chip)
    "free-lessons":                     ((222, 70, 134), "eiffel",    "A1",    "7 FREE LESSONS"),
    "first-conversations":              ((16, 150, 148), "terrace",   "A1",    "7 VIDEO LESSONS"),
    "french-sounds-starter":            ((122, 86, 224), "bookstore", "A1",    "7 VIDEO LESSONS"),
    "everyday-french":                  ((214, 108, 16), "town",      "A1",    "7 VIDEO LESSONS"),
    "french-grammar-starter":           ((44, 98, 224),  "classroom", "A1",    "7 VIDEO LESSONS"),
    "real-life-french":                 ((36, 142, 80),  "market",    "A1–A2", "7 VIDEO LESSONS"),
    "travel-french":                    ((222, 78, 60),  "airport",   "A1–A2", "7 VIDEO LESSONS"),
    "from-zero-to-first-conversations": ((58, 72, 138),  "river",     "A1",    "COMING SOON"),
    "tiny-1000":                        ((14, 118, 186), "street",    "A1–A2", "100 LESSONS · 1,000 WORDS"),
    "tiny-conversations":               ((160, 52, 150), "cafe",      "A1–A2", "100 CONVERSATIONS"),
}
FILES = {"free-lessons": "cover-free-lessons.png", "first-conversations": "cover-first-conversations.png",
         "french-sounds-starter": "cover-french-sounds.png", "everyday-french": "cover-everyday-french.png",
         "french-grammar-starter": "cover-french-grammar.png", "real-life-french": "cover-real-life-french.png",
         "travel-french": "cover-travel-french.png", "from-zero-to-first-conversations": "cover-zero-to-conversations.png",
         "tiny-1000": "cover-tiny-1000.png", "tiny-conversations": "cover-tiny-conversations.png"}
TITLES = {"free-lessons": "Free French Lessons", "first-conversations": "First Conversations", "french-sounds-starter": "French Sounds Starter",
          "everyday-french": "Everyday French", "french-grammar-starter": "French Grammar Starter", "real-life-french": "Real-Life French",
          "travel-french": "Travel French", "from-zero-to-first-conversations": "From Zero to Your First Conversations", "tiny-1000": "Tiny 1000", "tiny-conversations": "Tiny Conversations"}


def banner(fr, title, accent, y0=104):
    d = ImageDraw.Draw(fr)
    box_w = 1700
    size, ls, f = 118, [title], None
    while size > 64:
        f = MC.title_font(size); ls = L.wrap(title, f, box_w - 140)
        if len(ls) <= 2 and max(f.getlength(x) for x in ls) <= box_w - 140:
            break
        size -= 6
    lh = int(size * 1.18); bh = lh * len(ls) + 70
    bw = min(box_w, int(max(f.getlength(x) for x in ls)) + 190)
    x0 = (W - bw) // 2
    sh = Image.new("RGBA", fr.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x0 + 8, y0 + 18, x0 + bw + 8, y0 + bh + 18), radius=70, fill=(0, 0, 0, 110))
    blur = sh.filter(ImageFilter.GaussianBlur(14)); fr.alpha_composite(blur)
    d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), radius=70, fill=(255, 253, 249), outline=accent, width=12)
    y = y0 + 35
    for x in ls:
        d.text((W // 2, y), x, font=f, fill=MC.INK, anchor="ma"); y += lh


def pill(fr, x, cy, text, size, fg, bg, outline):
    d = ImageDraw.Draw(fr); f = MC.title_font(size)
    w = int(f.getlength(text)) + 76; h = int(size * 1.72)
    d.rounded_rectangle((x, cy - h / 2, x + w, cy + h / 2), radius=h / 2, fill=bg, outline=outline, width=7)
    d.text((x + w / 2, cy), text, font=f, fill=fg, anchor="mm")
    return x + w


def course_cover(cid, out_path, size=(1500, 843)):
    accent, scene, level, chip = THEMES[cid]
    bg, fg = L.make_scene(scene, 0)
    seg = dict(scene=scene, variant=0, start=0.0, weather=None, prev_weather=None, tod=None, kind="story")
    holder = type("R", (), {})()
    fr, fg = A.atmos_frame(holder, scene, 0, bg, fg, seg, 3.0)
    fr = fr.convert("RGBA"); fr.paste(fg, (0, L.FLOOR_Y - 40), fg)
    sprites = []
    for nm, cx in (("Marinette", 640), ("Adrien", 1280)):
        s = A.rig(nm, 0, False, "happy", 0, 0, MC.OUT)
        pad = s.height - s.getchannel("A").getbbox()[3]
        sprites.append((nm, cx, s, 1050 - (s.height - pad)))
    for nm, cx, s, top in sprites:
        sh = Image.new("RGBA", fr.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse((cx - 170, 1030, cx + 170, 1075), fill=(0, 0, 0, 70))
        fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
        fr.paste(s, (int(cx - s.width // 2), int(top)), s)
    vg = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vg).ellipse((-380, -300, W + 380, H + 360), fill=255); vg = vg.filter(ImageFilter.GaussianBlur(200))
    fr = Image.composite(fr, Image.alpha_composite(fr, Image.new("RGBA", (W, H), (20, 14, 40, 90))), vg)
    cy = 925
    x = pill(fr, 46, cy, "TINY FRENCH", 50, accent, (255, 253, 249), accent)
    pill(fr, x + 18, cy, f"{level} · {chip}", 46, (255, 255, 255), accent, (255, 255, 255))
    banner(fr, TITLES[cid], accent)
    img = fr.convert("RGB").resize(size, Image.LANCZOS)
    img.save(out_path, optimize=True)
    return os.path.getsize(out_path)


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "output", "course_art_v3")
    only = sys.argv[3] if len(sys.argv) > 3 else None
    os.makedirs(out, exist_ok=True)
    assert rigsvg.resvg_py is not None, "resvg-py is missing: pip install resvg-py (otherwise the old triangle characters are used)"
    if what in ("thumbs", "all"):
        lessons = json.load(open(os.path.join(HERE, "assets", "course_art", "lessons.json"), encoding="utf-8"))
        for l in lessons:
            if only and only not in l["stem"]: continue
            p = os.path.join(out, l["stem"] + ".thumbnail.png")
            MC.make_cover(os.path.join(HERE, "lessons", l["stem"] + ".txt"), p)
            print(l["stem"], os.path.getsize(p) // 1024, "KB", flush=True)
    if what in ("covers", "all"):
        for cid in THEMES:
            if only and only not in cid: continue
            p = os.path.join(out, FILES[cid])
            print(FILES[cid], course_cover(cid, p) // 1024, "KB", flush=True)

if __name__ == "__main__":
    main()
