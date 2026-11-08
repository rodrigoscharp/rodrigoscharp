#!/usr/bin/env python3
"""Build assets/card.svg: the pixel-art portrait next to a list of qualities.

Left: the cut-out portrait from build_avatar.py, which resolves from big blocks
to the final pixel grid. Right: a character-sheet panel in a 3x5 pixel font
(drawn as rects, so it renders the same everywhere), with stat bars that fill
in and traits that appear one by one after the portrait resolves.

Every animated element rests in its finished state, so the card reads complete
wherever CSS animation does not run.

Edit the CONTENT block below, then run:  python3 tools/build_card.py
"""

from __future__ import annotations

import os

import build_avatar as av

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "card.svg")

# ---------------------------------------------------------------- CONTENT
NAME = "RODRIGO SCHARP"
BADGES = [("FOUNDER", True), ("TECH LEAD", False), ("STARTUP BUILDER", False)]  # (text, filled)
TAGLINE = "TAKING PRODUCTS FROM ZERO TO PRODUCTION"
STATS = [  # label, filled segments out of 10, note shown after the bar
    ("BACKEND", 9, ""),
    ("PRODUCT", 8, ""),
    ("CLOUD + AWS", 7, ""),
    ("AI", 9, ""),
    ("COFFEE", 10, "MAX"),
]
TRAITS = [
    "FOUNDED MUNO, A FOOD-TECH, FROM ZERO",
    "LEADS TECH ON SYSTEMS 100K+ PEOPLE USE",
    "BUILDS LOCK-FREE ENGINES FOR FUN",
]
PORTRAIT_ROWS = 120     # fewer rows = chunkier pixels
PORTRAIT_COLORS = 48
PORTRAIT_OUTLINE = False
PORTRAIT_FADE = 0.12     # share of the portrait height that fades out at the bottom
# -------------------------------------------------------------------------

VW, VH = 900, 476
# text and UI in black and white; only the portrait keeps the photo's colors
BRIGHT, TEXT, MUTED, DIM, INK = "#ffffff", "#e4e4e4", "#8a8a8a", "#2a2a2a", "#0b0b0b"

FONT = {
    "A": [".#.", "#.#", "###", "#.#", "#.#"], "B": ["##.", "#.#", "##.", "#.#", "##."],
    "C": [".##", "#..", "#..", "#..", ".##"], "D": ["##.", "#.#", "#.#", "#.#", "##."],
    "E": ["###", "#..", "##.", "#..", "###"], "F": ["###", "#..", "##.", "#..", "#.."],
    "G": [".##", "#..", "#.#", "#.#", ".##"], "H": ["#.#", "#.#", "###", "#.#", "#.#"],
    "I": ["###", ".#.", ".#.", ".#.", "###"], "J": ["..#", "..#", "..#", "#.#", ".#."],
    "K": ["#.#", "#.#", "##.", "#.#", "#.#"], "L": ["#..", "#..", "#..", "#..", "###"],
    "M": ["#.#", "###", "###", "#.#", "#.#"], "N": ["##.", "#.#", "#.#", "#.#", "#.#"],
    "O": [".#.", "#.#", "#.#", "#.#", ".#."], "P": ["##.", "#.#", "##.", "#..", "#.."],
    "Q": [".#.", "#.#", "#.#", "##.", ".##"], "R": ["##.", "#.#", "##.", "#.#", "#.#"],
    "S": [".##", "#..", ".#.", "..#", "##."], "T": ["###", ".#.", ".#.", ".#.", ".#."],
    "U": ["#.#", "#.#", "#.#", "#.#", "###"], "V": ["#.#", "#.#", "#.#", ".#.", ".#."],
    "W": ["#.#", "#.#", "###", "###", "#.#"], "X": ["#.#", "#.#", ".#.", "#.#", "#.#"],
    "Y": ["#.#", "#.#", ".#.", ".#.", ".#."], "Z": ["###", "..#", ".#.", "#..", "###"],
    "0": ["###", "#.#", "#.#", "#.#", "###"], "1": [".#.", "##.", ".#.", ".#.", "###"],
    "2": ["##.", "..#", ".#.", "#..", "###"], "3": ["##.", "..#", ".#.", "..#", "##."],
    "4": ["#.#", "#.#", "###", "..#", "..#"], "5": ["###", "#..", "##.", "..#", "##."],
    "6": [".##", "#..", "###", "#.#", "###"], "7": ["###", "..#", ".#.", ".#.", ".#."],
    "8": ["###", "#.#", "###", "#.#", "###"], "9": ["###", "#.#", "###", "..#", "##."],
    "+": ["...", ".#.", "###", ".#.", "..."], "-": ["...", "...", "###", "...", "..."],
    "/": ["..#", "..#", ".#.", "#..", "#.."], "!": [".#.", ".#.", ".#.", "...", ".#."],
    ".": ["...", "...", "...", "...", ".#."], ",": ["...", "...", "...", ".#.", "#.."],
    ":": ["...", ".#.", "...", ".#.", "..."], ">": ["#..", ".#.", "..#", ".#.", "#.."],
    " ": ["...", "...", "...", "...", "..."],
}


def text(s: str, x: float, y: float, color: str, px: float = 3) -> str:
    d = []
    for i, ch in enumerate(s.upper()):
        g = FONT.get(ch, FONT[" "])
        gx = x + i * 4 * px
        for r, row in enumerate(g):
            c = 0
            while c < 3:
                if row[c] == "#":
                    c2 = c
                    while c2 < 3 and row[c2] == "#":
                        c2 += 1
                    d.append(f"M{gx + c * px:g} {y + r * px:g}h{(c2 - c) * px:g}v{px:g}h-{(c2 - c) * px:g}z")
                    c = c2
                else:
                    c += 1
    return f'<path fill="{color}" d="{"".join(d)}"/>'


def text_w(s: str, px: float = 3) -> float:
    return (len(s) * 4 - 1) * px


def outlined(grid: list[list[tuple[int, int, int] | None]]) -> list[list[tuple[int, int, int] | None]]:
    """Pad by one pixel and draw a dark outline around the silhouette."""
    h, w = len(grid), len(grid[0])
    g = [[None] * (w + 2)] + [[None] + row + [None] for row in grid] + [[None] * (w + 2)]
    out = [row[:] for row in g]
    ink = tuple(int(INK[i:i + 2], 16) for i in (1, 3, 5))
    for y in range(h + 2):
        for x in range(w + 2):
            if g[y][x] is None and any(
                0 <= y + dy < h + 2 and 0 <= x + dx < w + 2 and g[y + dy][x + dx] is not None
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))
            ):
                out[y][x] = ink
    return out


def portrait(x: float, y: float, h: float) -> tuple[str, list[str], float]:
    av.COLORS = PORTRAIT_COLORS
    img = av.load()
    cols, rows = av.grid_size(img, PORTRAIT_ROWS)
    w = h * cols / rows
    layers = []
    for i, d in enumerate(av.DIVS):
        r = max(1, rows // d)
        c = max(1, round(r * cols / rows))
        grid = av.pixelate(img, c, r)
        if PORTRAIT_OUTLINE:
            grid = outlined(grid)
        cu, ru = w / c, h / r
        shift = 1 if PORTRAIT_OUTLINE else 0   # the outline ring sits one pixel outside
        layers.append(
            f'<g class="p{i}" transform="translate({-cu * shift:g} {-ru * shift:g})">{av.to_paths(grid, cu, ru)}</g>'
        )
    last = len(av.DIVS) - 1
    css = [f".p{i}{{opacity:0;animation:show {av.STEP_DUR}s {i * av.STEP_DUR:.2f}s}}" for i in range(last)]
    css.append(f".p{last}{{animation:hide {last * av.STEP_DUR:.2f}s}}")
    svg = (
        # the photo cuts the legs off: fade the last stretch into the background
        '<linearGradient id="pfadeg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="{1 - PORTRAIT_FADE:.3f}" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
        f'<mask id="pfade" maskUnits="userSpaceOnUse" x="{x - 20:g}" y="{y - 20:g}" width="{w + 40:g}" height="{h + 20:g}">'
        f'<rect x="{x - 20:g}" y="{y - 20:g}" width="{w + 40:g}" height="{h + 20:g}" fill="url(#pfadeg)"/></mask>'
        f'<g mask="url(#pfade)"><g transform="translate({x:g} {y:g})">{"".join(layers)}</g></g>'
    )
    return svg, css, w


def build() -> str:
    reveal_end = (len(av.DIVS) - 1) * av.STEP_DUR
    css = [
        "*{shape-rendering:crispEdges}",
        "ellipse,circle{shape-rendering:auto}",
        "@keyframes show{from,to{opacity:1}}",
        "@keyframes hide{from,to{opacity:0}}",
        "@keyframes pop{from{opacity:0}}",
        ".pop{animation:pop .01s backwards}",
        "@keyframes blink{50%{opacity:0}}",
        ".cur{animation:blink 1s step-end infinite}",
    ]

    # portrait column
    ph = 372
    psvg, pcss, pw = portrait(56, (VH - ph) // 2, ph)
    css += pcss
    glow = f'<circle cx="{56 + pw / 2:g}" cy="{VH // 2}" r="170" fill="url(#glow)"/>'
    col_x = 56 + pw + 64

    out = [glow, psvg]
    out.append(f'<rect x="{col_x - 32}" y="40" width="2" height="{VH - 80}" fill="{DIM}"/>')

    # header
    y = 46
    out.append(text(NAME, col_x, y, BRIGHT, 5))
    y += 25 + 22
    bx = col_x
    for label, filled in BADGES:
        bw = text_w(label) + 20
        if filled:
            out.append(f'<rect x="{bx}" y="{y}" width="{bw:g}" height="27" fill="{BRIGHT}"/>')
            out.append(text(label, bx + 10, y + 6, INK))
        else:
            out.append(f'<path fill="{MUTED}" d="M{bx} {y}h{bw:g}v3h-{bw:g}zM{bx} {y + 24}h{bw:g}v3h-{bw:g}z'
                       f'M{bx} {y}h3v27h-3zM{bx + bw - 3:g} {y}h3v27h-3z"/>')
            out.append(text(label, bx + 10, y + 6, TEXT))
        bx += bw + 12
    y += 27 + 16
    out.append(text(TAGLINE, col_x, y, MUTED))
    y += 15 + 30

    # stats
    out.append(text("STATS", col_x, y, MUTED, 2))
    y += 10 + 14
    t = reveal_end + 0.2
    bar_x = col_x + max(text_w(l) for l, _, _ in STATS) + 36
    seg_w, seg_gap = 18, 4
    for label, filled, note in STATS:
        out.append(text(label, col_x, y, TEXT))
        for k in range(10):
            sx = bar_x + k * (seg_w + seg_gap)
            out.append(f'<rect x="{sx}" y="{y}" width="{seg_w}" height="15" fill="{DIM}"/>')
            if k < filled:
                out.append(
                    f'<g class="pop" style="animation-delay:{t + k * 0.05:.2f}s">'
                    f'<rect x="{sx}" y="{y}" width="{seg_w}" height="15" fill="{TEXT}"/>'
                    f'<rect x="{sx}" y="{y}" width="{seg_w}" height="3" fill="{BRIGHT}"/>'
                    f'<rect x="{sx}" y="{y + 12}" width="{seg_w}" height="3" fill="#a8a8a8"/></g>'
                )
        if note:
            nx = bar_x + 10 * (seg_w + seg_gap) + 8
            out.append(f'<g class="pop" style="animation-delay:{t + filled * 0.05:.2f}s">{text(note, nx, y, BRIGHT)}</g>')
        t += 0.25
        y += 15 + 11
    y += 18

    # traits
    out.append(text("TRAITS", col_x, y, MUTED, 2))
    y += 10 + 14
    t += 0.2
    for tr in TRAITS:
        out.append(
            f'<g class="pop" style="animation-delay:{t:.2f}s">'
            f'{text(">", col_x, y, MUTED)}{text(tr, col_x + 20, y, TEXT)}</g>'
        )
        last_y, last_x = y, col_x + 20 + text_w(tr) + 8
        t += 0.35
        y += 15 + 11
    out.append(f'<g class="pop" style="animation-delay:{t - 0.35:.2f}s">'
               f'<rect class="cur" x="{last_x:g}" y="{last_y}" width="9" height="15" fill="{BRIGHT}"/></g>')

    css.append("@media (prefers-reduced-motion:reduce){*{animation:none!important}.cur{opacity:1}}")
    label = (
        f"{NAME.title()} in pixel art, arms crossed, next to a character sheet: "
        + ", ".join(b.lower() for b, _ in BADGES) + f". {TAGLINE.lower()}. Stats: "
        + ", ".join(f"{l.lower()} {f}/10" for l, f, _ in STATS)
        + ". Traits: " + "; ".join(t.lower() for t in TRAITS) + "."
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" role="img" aria-label="{label}">'
        f"<style>{''.join(css)}</style>"
        "<defs>"
        '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#161616"/>'
        '<stop offset="1" stop-color="#0a0a0a"/></linearGradient>'
        f'<radialGradient id="glow"><stop offset="0" stop-color="#ffffff" stop-opacity=".07"/>'
        f'<stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#000" stop-opacity=".45"/></radialGradient>'
        f'<clipPath id="frame"><rect width="{VW}" height="{VH}" rx="14"/></clipPath>'
        "</defs>"
        f'<g clip-path="url(#frame)"><rect width="{VW}" height="{VH}" fill="url(#bg)"/>{"".join(out)}'
        f'<rect width="{VW}" height="{VH}" fill="url(#vig)"/></g>'
        f'<rect x=".75" y=".75" width="{VW - 1.5}" height="{VH - 1.5}" rx="14" fill="none" stroke="#3a3a3a" stroke-width="1.5"/>'
        "</svg>\n"
    )


if __name__ == "__main__":
    svg = build()
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg) / 1024:.1f} KB)")
