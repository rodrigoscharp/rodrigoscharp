#!/usr/bin/env python3
"""Build assets/avatar-pixel.svg: the GitHub avatar redrawn as pixel art.

The photo is box-downsampled to a small grid and quantized to a short palette
(no dithering), so every pixel is a flat, crisp square. On load the portrait
"resolves": it starts as big blocks and sharpens step by step until it reaches
the final grid, then stays there. Without animation it shows the final image.

Source: assets/avatar-src.png  (https://github.com/rodrigoscharp.png)
Run:    python3 tools/build_avatar.py [grid] [colors]
"""

from __future__ import annotations

import os
import sys

from PIL import Image, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "avatar-src.png")
OUT = os.path.join(ROOT, "assets", "avatar-pixel.svg")

GRID = int(sys.argv[1]) if len(sys.argv) > 1 else 96
COLORS = int(sys.argv[2]) if len(sys.argv) > 2 else 64
CELL = 6                       # output units per pixel of the final grid
STEPS = [GRID // 16, GRID // 8, GRID // 4, GRID // 2, GRID]
STEP_DUR = 0.45                # seconds each coarse stage is held


def load() -> Image.Image:
    img = Image.open(SRC).convert("RGB")
    side = min(img.size)
    left, top = (img.width - side) // 2, (img.height - side) // 2
    img = img.crop((left, top, left + side, top + side))
    img = ImageEnhance.Color(img).enhance(1.15)
    img = ImageEnhance.Contrast(img).enhance(1.08)
    return img


def pixelate(img: Image.Image, n: int) -> Image.Image:
    small = img.resize((n, n), Image.Resampling.BOX)
    q = small.quantize(colors=COLORS, method=Image.Quantize.MEDIANCUT, kmeans=8, dither=Image.Dither.NONE)
    return q.convert("RGB")


def to_paths(small: Image.Image, unit: float) -> str:
    n = small.width
    px = small.load()
    by: dict[str, list[str]] = {}
    for y in range(n):
        x = 0
        while x < n:
            c = px[x, y]
            x2 = x
            while x2 < n and px[x2, y] == c:
                x2 += 1
            hexc = "#%02x%02x%02x" % c
            w = (x2 - x) * unit
            by.setdefault(hexc, []).append(f"M{x * unit:g} {y * unit:g}h{w:g}v{unit:g}h-{w:g}z")
            x = x2
    return "".join(f'<path fill="{c}" d="{"".join(d)}"/>' for c, d in by.items())


def build() -> str:
    img = load()
    size = GRID * CELL
    layers = []
    for i, n in enumerate(STEPS):
        unit = size / n
        layers.append(f'<g class="l l{i}">{to_paths(pixelate(img, n), unit)}</g>')

    last = len(STEPS) - 1
    # each coarse layer sits on top of the final image and is removed in turn,
    # so the portrait sharpens: 1/16 -> 1/8 -> 1/4 -> 1/2 -> full
    css = [
        "*{shape-rendering:crispEdges}",
        "@keyframes off{to{opacity:0}}",
        *[
            f".l{i}{{animation:off 0s step-end {0.25 + (i + 1) * STEP_DUR:.2f}s forwards}}"
            for i in range(last)
        ],
        "@media (prefers-reduced-motion:reduce){.l{animation:none!important;opacity:0}.l%d{opacity:1}}" % last,
    ]
    # draw final first, coarse layers above it, coarsest on top
    ordered = [layers[last]] + layers[last - 1::-1]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" role="img" '
        f'aria-label="Rodrigo Scharp, pixel-art version of his profile photo: arms crossed, glasses, '
        f'black t-shirt and lanyard, in front of the AWS sign at a conference.">'
        f"<style>{''.join(css)}</style>"
        f'<defs><clipPath id="c"><rect width="{size}" height="{size}" rx="{size * 0.04:g}"/></clipPath></defs>'
        f'<g clip-path="url(#c)">{"".join(ordered)}</g>'
        "</svg>\n"
    )


if __name__ == "__main__":
    svg = build()
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg) / 1024:.1f} KB) grid={GRID} colors={COLORS}")
