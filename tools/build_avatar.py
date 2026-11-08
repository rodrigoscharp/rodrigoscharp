#!/usr/bin/env python3
"""Build assets/avatar-pixel.svg: me, cut out of the GitHub avatar, as pixel art.

assets/avatar-cutout.png is the avatar with the background removed
(swift tools/cutout.swift assets/avatar-src.png assets/avatar-cutout.png).
It is cropped to the person, box-downsampled to a small grid (alpha-weighted,
so edge pixels keep the person's color) and quantized to a short palette with
no dithering, so every pixel is a flat, crisp square on a transparent
background. On load the portrait "resolves": big blocks sharpen step by step
to the final grid, then it stays. Without animation it shows the final image.

Source: assets/avatar-src.png  (https://github.com/rodrigoscharp.png)
Run:    python3 tools/build_avatar.py [rows] [colors]
"""

from __future__ import annotations

import os
import sys

from PIL import Image, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "avatar-cutout.png")
OUT = os.path.join(ROOT, "assets", "avatar-pixel.svg")

ROWS = int(sys.argv[1]) if len(sys.argv) > 1 else 120
COLORS = int(sys.argv[2]) if len(sys.argv) > 2 else 48
CELL = 5                       # output units per pixel of the final grid
DIVS = [8, 4, 2, 1]        # coarse -> final
STEP_DUR = 0.4                 # seconds each coarse stage is shown
ALPHA_CUT = 128


def load() -> Image.Image:
    img = Image.open(SRC).convert("RGBA")
    l, t, r, b = img.getchannel("A").point(lambda a: 255 if a >= ALPHA_CUT else 0).getbbox()
    img = img.crop((l, t, r, b))
    rgb = ImageEnhance.Color(img.convert("RGB")).enhance(1.15)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.08)
    rgb.putalpha(img.getchannel("A"))
    return rgb


def grid_size(img: Image.Image, rows: int) -> tuple[int, int]:
    return max(1, round(rows * img.width / img.height)), rows


def pixelate(img: Image.Image, cols: int, rows: int) -> list[list[tuple[int, int, int] | None]]:
    # alpha-weighted box average: premultiply, shrink, un-premultiply
    a = img.getchannel("A")
    pre = Image.composite(img.convert("RGB"), Image.new("RGB", img.size), a)
    pre_s = pre.resize((cols, rows), Image.Resampling.BOX)
    a_s = a.resize((cols, rows), Image.Resampling.BOX)
    rgb = Image.new("RGB", (cols, rows))
    pp, ap, rp = pre_s.load(), a_s.load(), rgb.load()
    for y in range(rows):
        for x in range(cols):
            al = ap[x, y]
            if al:
                rp[x, y] = tuple(min(255, round(c * 255 / al)) for c in pp[x, y])
    q = rgb.quantize(colors=COLORS, method=Image.Quantize.MEDIANCUT, kmeans=8, dither=Image.Dither.NONE).convert("RGB")
    qp = q.load()
    return [[qp[x, y] if ap[x, y] >= ALPHA_CUT else None for x in range(cols)] for y in range(rows)]


def to_paths(grid: list[list[tuple[int, int, int] | None]], ux: float, uy: float) -> str:
    by: dict[str, list[str]] = {}
    for y, row in enumerate(grid):
        x = 0
        while x < len(row):
            c = row[x]
            x2 = x
            while x2 < len(row) and row[x2] == c:
                x2 += 1
            if c is not None:
                w = (x2 - x) * ux
                by.setdefault("#%02x%02x%02x" % c, []).append(
                    f"M{x * ux:g} {y * uy:g}h{w:g}v{uy:g}h-{w:g}z"
                )
            x = x2
    return "".join(f'<path fill="{c}" d="{"".join(d)}"/>' for c, d in by.items())


def build() -> str:
    img = load()
    cols, rows = grid_size(img, ROWS)
    vw, vh = cols * CELL, rows * CELL
    layers = []
    for i, d in enumerate(DIVS):
        r = max(1, rows // d)
        c = max(1, round(r * cols / rows))
        layers.append(f'<g class="l{i}">{to_paths(pixelate(img, c, r), vw / c, vh / r)}</g>')

    last = len(DIVS) - 1
    total = last * STEP_DUR
    # one stage visible at a time; the final stage is the default state, so it
    # is what shows wherever CSS animation does not run
    css = [
        "*{shape-rendering:crispEdges}",
        "@keyframes show{from,to{opacity:1}}",
        "@keyframes hide{from,to{opacity:0}}",
        *[f".l{i}{{opacity:0;animation:show {STEP_DUR}s {i * STEP_DUR:.2f}s}}" for i in range(last)],
        f".l{last}{{animation:hide {total:.2f}s}}",
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}",
    ]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw} {vh}" role="img" '
        f'aria-label="Rodrigo Scharp in pixel art, cut out from his profile photo: arms crossed, '
        f'glasses, black t-shirt with lanyard, jeans.">'
        f"<style>{''.join(css)}</style>"
        f'{"".join(layers)}'
        "</svg>\n"
    )


if __name__ == "__main__":
    svg = build()
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg) / 1024:.1f} KB) rows={ROWS} colors={COLORS}")
