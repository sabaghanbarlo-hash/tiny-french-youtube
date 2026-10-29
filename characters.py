"""Adrien and Marinette artwork shared by every video type (the approved Tiny French look).

portrait(name, mouth, blink)        -> 504x684 head-and-torso sprite (Shorts, lessons, thumbnails)
head(name, expr, mouth, blink, S)   -> (image, anchor_x, anchor_y) head for the full-body acting rig, scaled for rig scale S
"""
import functools
from PIL import Image
import sprites as _sprites
from frchars import faces

NAMES = ("Adrien", "Marinette")
MOUTH_Q = {0: 0.0, 1: 0.35, 2: 0.85}


def portrait(name, mouth, blink):
    return _sprites.sprite(name, int(mouth), bool(blink))


@functools.lru_cache(maxsize=256)
def _head(name, expr, mq, blink, S):
    h = faces.head(name, expr, MOUTH_Q.get(mq, 0.0), blink)
    k = S / faces.SCALE
    im = h.resize((int(h.width * k), int(h.height * k)), Image.LANCZOS)
    return im, int(faces.ANCHOR[0] * k), int(faces.ANCHOR[1] * k)


def head(name, expr, mouth, blink, S):
    return _head(name, expr, int(mouth), bool(blink), S)
