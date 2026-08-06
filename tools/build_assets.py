#!/usr/bin/env python3
"""Build the profile README's SVG plates.

Design: "Statement of Work" — greenbar accounting/line-printer paper.
Display face is Bodoni Moda (engraved certificate), everything else is
IBM Plex Mono (mainframe heritage). All text is converted to outlines, so
the plates render identically everywhere with no font dependency.

Both fonts are SIL Open Font License. Run:  python3 tools/build_assets.py
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
FONTS = os.path.join(ROOT, ".fontcache")

FONT_SOURCES = {
    "BodoniModa.ttf": "https://github.com/google/fonts/raw/main/ofl/bodonimoda/BodoniModa%5Bopsz,wght%5D.ttf",
    "PlexMono-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-Regular.ttf",
    "PlexMono-Medium.ttf": "https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-Medium.ttf",
    "PlexMono-SemiBold.ttf": "https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-SemiBold.ttf",
}


# --------------------------------------------------------------------------
# Palette
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Theme:
    name: str
    bar_a: str      # the pale bar of greenbar paper
    bar_b: str      # the green bar
    edge: str       # plate border
    rule: str       # printed rules and leader dots
    ink: str        # primary type
    muted: str      # micro caps, labels
    red: str        # ledger red — the one accent


LIGHT = Theme(
    name="light",
    bar_a="#F7F9F4",
    bar_b="#DFEAD8",
    edge="#C0D2B9",
    rule="#A5BA9E",
    ink="#1B241A",
    muted="#5C6B58",
    red="#AE1420",
)

DARK = Theme(
    name="dark",
    bar_a="#0F140E",
    bar_b="#182017",
    edge="#2B3B28",
    rule="#3A4E36",
    ink="#E6EEE2",
    muted="#93A58D",
    red="#F0655A",
)


# --------------------------------------------------------------------------
# Text -> outlines
# --------------------------------------------------------------------------

class Face:
    """A loaded font instance that can emit SVG path data for a string."""

    def __init__(self, path: str, **axes: float) -> None:
        font = TTFont(path)
        if axes and "fvar" in font:
            font = instancer.instantiateVariableFont(font, axes)
        self.font = font
        self.upem = font["head"].unitsPerEm
        self.cmap = font.getBestCmap()
        self.glyphs = font.getGlyphSet()
        self.hmtx = font["hmtx"]

    def _gname(self, ch: str) -> str:
        return self.cmap.get(ord(ch), ".notdef")

    def width(self, text: str, size: float, tracking: float = 0.0) -> float:
        scale = size / self.upem
        total = 0.0
        for ch in text:
            total += self.hmtx[self._gname(ch)][0] * scale + tracking
        return total - tracking if text else 0.0

    def path(
        self,
        text: str,
        size: float,
        x: float,
        y: float,
        tracking: float = 0.0,
        anchor: str = "start",
    ) -> str:
        """SVG path data for `text` with its baseline at `y`."""
        scale = size / self.upem
        if anchor == "end":
            x -= self.width(text, size, tracking)
        elif anchor == "middle":
            x -= self.width(text, size, tracking) / 2

        pen = SVGPathPen(self.glyphs, ntos=lambda v: f"{v:.1f}")
        cursor = x
        for ch in text:
            gname = self._gname(ch)
            if ch != " ":
                self.glyphs[gname].draw(
                    TransformPen(pen, Transform(scale, 0, 0, -scale, cursor, y))
                )
            cursor += self.hmtx[gname][0] * scale + tracking
        return pen.getCommands()


def ensure_fonts() -> None:
    os.makedirs(FONTS, exist_ok=True)
    for name, url in FONT_SOURCES.items():
        dest = os.path.join(FONTS, name)
        if not os.path.exists(dest):
            print(f"  fetching {name}")
            subprocess.run(["curl", "-sSL", "-o", dest, url], check=True)


# --------------------------------------------------------------------------
# Drawing helpers
# --------------------------------------------------------------------------

def text(face: Face, s: str, size: float, x: float, y: float, fill: str,
         tracking: float = 0.0, anchor: str = "start") -> str:
    d = face.path(s, size, x, y, tracking, anchor)
    if not d:
        return ""
    return f'<path fill="{fill}" d="{d}"/>'


def rule(x1: float, y: float, x2: float, color: str, width: float = 1.0) -> str:
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" '
            f'stroke="{color}" stroke-width="{width}"/>')


def leader(x1: float, y: float, x2: float, color: str) -> str:
    """The dotted leader line of a ledger entry."""
    if x2 - x1 < 12:
        return ""
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" '
            f'stroke-width="2.2" stroke-linecap="round" stroke-dasharray="0.1 9"/>')


def band(x: float, y: float, w: float, h: float, fill: str) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'


def svg(width: float, height: float, title: str, body: list[str]) -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:g} {height:g}" '
        f'width="{width:g}" height="{height:g}" role="img" aria-label="{title}">',
        f"<title>{title}</title>",
    ]
    parts.extend(p for p in body if p)
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def write(name: str, content: str) -> None:
    os.makedirs(ASSETS, exist_ok=True)
    path = os.path.join(ASSETS, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  {name}  ({len(content) / 1024:.1f} KB)")


# --------------------------------------------------------------------------
# Plate 1 — the nameplate
# --------------------------------------------------------------------------

W = 1200
PAD = 72

HERO_ENTRIES = [
    ("YEARS BUILDING SOFTWARE", "4+", False),
    ("SYSTEMS IN PRODUCTION", "6+", False),
    ("CITIZENS SERVED", "100,000+", False),
    ("NATIONAL AWARDS", "2", True),
    ("MATCHING ENGINE · ORDERS/SEC", "100K+", False),
]


def hero(t: Theme, display: Face, mono: Face, mono_md: Face, mono_sb: Face) -> str:
    head_h = 78
    row_h = 48
    foot_h = 46
    rows_top = 272
    height = rows_top + row_h * len(HERO_ENTRIES) + foot_h

    body: list[str] = [band(0, 0, W, height, t.bar_a)]

    # Greenbar: every other entry row carries the green bar.
    for i in range(len(HERO_ENTRIES)):
        if i % 2 == 0:
            body.append(band(0, rows_top + i * row_h, W, row_h, t.bar_b))

    # Header band — the form's identification line.
    body += [
        text(mono_md, "STATEMENT OF WORK", 20, PAD, 48, t.muted, tracking=4.2),
        text(mono_md, "SHEET 01", 20, W - PAD, 48, t.muted, tracking=4.2, anchor="end"),
        rule(PAD, head_h, W - PAD, t.rule),
    ]

    # Nameplate. Track the name out to fill the measure like an engraved title.
    name = "RODRIGO SCHARP"
    size = 98
    avail = W - PAD * 2
    tracking = (avail - display.width(name, size)) / (len(name) - 1)
    tracking = max(2.0, min(tracking, 14.0))
    while display.width(name, size, tracking) > avail:
        size -= 1
    body += [
        text(display, name, size, PAD, 192, t.ink, tracking=tracking),
        text(mono, "Software Engineer · Ubatuba, Brazil", 24, PAD, 236,
             t.muted, tracking=2.0),
        rule(PAD, rows_top, W - PAD, t.rule),
    ]

    # Entries — label, leader dots, right-aligned figure.
    for i, (label, value, accent) in enumerate(HERO_ENTRIES):
        baseline = rows_top + i * row_h + 32
        lw = mono_md.width(label, 23, 3.4)
        vw = mono_sb.width(value, 32, 0.5)
        body += [
            text(mono_md, label, 23, PAD, baseline, t.muted, tracking=3.4),
            leader(PAD + lw + 18, baseline - 8, W - PAD - vw - 18, t.rule),
            text(mono_sb, value, 32, W - PAD, baseline,
                 t.red if accent else t.ink, tracking=0.5, anchor="end"),
        ]

    # Footer band — mirrors the header.
    foot_top = rows_top + row_h * len(HERO_ENTRIES)
    body += [
        rule(PAD, foot_top, W - PAD, t.rule),
        text(mono_md, "SMART CITY AWARD · CIDADE INOVADORA AWARD", 18,
             PAD, foot_top + 30, t.muted, tracking=3.2),
        text(mono_md, "NATIONAL · BRAZIL", 18, W - PAD, foot_top + 30,
             t.muted, tracking=3.2, anchor="end"),
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{height - 1}" '
        f'fill="none" stroke="{t.edge}"/>',
    ]

    alt = ("Rodrigo Scharp — Software Engineer, Ubatuba, Brazil. "
           + " ".join(f"{lbl.title()}: {val}." for lbl, val, _ in HERO_ENTRIES))
    return svg(W, height, alt, body)


# --------------------------------------------------------------------------
# Plate 2 — the stack
# --------------------------------------------------------------------------

STACK_ROWS = [
    ("BACKEND", "Java 21 · Spring Boot 3 · Node.js"),
    ("FULL-STACK", "Next.js · TypeScript · React"),
    ("DATA", "PostgreSQL · MySQL · Redis · Kafka · RabbitMQ"),
    ("CLOUD", "AWS · Docker · GitHub Actions"),
    ("AI", "Groq · LLaMA 3.1 · OpenAI · ElevenLabs"),
]


def stack(t: Theme, mono: Face, mono_md: Face) -> str:
    head_h = 78
    row_h = 56
    foot_h = 46
    height = head_h + row_h * len(STACK_ROWS) + foot_h
    col = 372

    body: list[str] = [band(0, 0, W, height, t.bar_a)]
    for i in range(len(STACK_ROWS)):
        if i % 2 == 0:
            body.append(band(0, head_h + i * row_h, W, row_h, t.bar_b))

    body += [
        text(mono_md, "SCHEDULE OF TECHNOLOGIES", 20, PAD, 48, t.muted, tracking=4.2),
        text(mono_md, "SHEET 02", 20, W - PAD, 48, t.muted, tracking=4.2, anchor="end"),
        rule(PAD, head_h, W - PAD, t.rule),
    ]

    for i, (label, items) in enumerate(STACK_ROWS):
        baseline = head_h + i * row_h + 36
        body += [
            text(mono_md, label, 23, PAD, baseline, t.muted, tracking=3.4),
            text(mono, items, 25, col, baseline, t.ink, tracking=0.4),
        ]

    foot_top = head_h + row_h * len(STACK_ROWS)
    body += [
        rule(PAD, foot_top, W - PAD, t.rule),
        text(mono_md, "AWS · ECS · ALB · CLOUDFRONT · API GATEWAY · LAMBDA", 18,
             PAD, foot_top + 30, t.muted, tracking=3.2),
        text(mono_md, "CI/CD · TESTCONTAINERS", 18, W - PAD, foot_top + 30,
             t.muted, tracking=3.2, anchor="end"),
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{height - 1}" '
        f'fill="none" stroke="{t.edge}"/>',
    ]

    alt = "Stack. " + " ".join(f"{lbl.title()}: {items}." for lbl, items in STACK_ROWS)
    return svg(W, height, alt, body)


# --------------------------------------------------------------------------
# Link chips
# --------------------------------------------------------------------------

CHIPS = [("linkedin", "LINKEDIN"), ("instagram", "INSTAGRAM"), ("email", "EMAIL")]


def chip(t: Theme, mono_md: Face, label: str) -> str:
    size, tracking, pad_x, height = 17, 2.6, 22, 40
    w = mono_md.width(label, size, tracking)
    width = w + pad_x * 2
    body = [
        f'<rect x="0.5" y="0.5" width="{width - 1:.1f}" height="{height - 1}" '
        f'fill="none" stroke="{t.rule}"/>',
        text(mono_md, label, size, pad_x, 26, t.ink, tracking=tracking),
    ]
    return svg(round(width, 1), height, label.title(), body)


# --------------------------------------------------------------------------

def main() -> None:
    print("fonts")
    ensure_fonts()

    display = Face(os.path.join(FONTS, "BodoniModa.ttf"), opsz=96, wght=500)
    mono = Face(os.path.join(FONTS, "PlexMono-Regular.ttf"))
    mono_md = Face(os.path.join(FONTS, "PlexMono-Medium.ttf"))
    mono_sb = Face(os.path.join(FONTS, "PlexMono-SemiBold.ttf"))

    print("plates")
    for t in (LIGHT, DARK):
        write(f"header-{t.name}.svg", hero(t, display, mono, mono_md, mono_sb))
        write(f"stack-{t.name}.svg", stack(t, mono, mono_md))
        for slug, label in CHIPS:
            write(f"chip-{slug}-{t.name}.svg", chip(t, mono_md, label))


if __name__ == "__main__":
    main()
