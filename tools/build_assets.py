#!/usr/bin/env python3
"""Build the profile README's SVG plates.

Design: "Statement of Work" — greenbar accounting/line-printer paper.
Display face is Archivo Expanded 800 (printed report title), everything else
is IBM Plex Mono (mainframe heritage). All text is converted to outlines, so
the plates render identically everywhere with no font dependency.

The nameplate prints itself: a print head sweeps across and leaves the name
behind it. Every animated element rests in its finished state, so the plate
still reads complete wherever CSS animation does not run.

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
    "Archivo.ttf": "https://github.com/google/fonts/raw/main/ofl/archivo/Archivo%5Bwdth,wght%5D.ttf",
    "Unbounded.ttf": "https://github.com/google/fonts/raw/main/ofl/unbounded/Unbounded%5Bwght%5D.ttf",
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

    def glyph_paths(
        self,
        text: str,
        size: float,
        x: float,
        y: float,
        tracking: float = 0.0,
        anchor: str = "start",
    ) -> list[tuple[str, float]]:
        """One path per character, plus the pen x after drawing it.

        Spaces come back with empty path data but still advance the pen, so a
        typing sequence keeps its natural rhythm across word gaps.
        """
        scale = size / self.upem
        if anchor == "end":
            x -= self.width(text, size, tracking)
        elif anchor == "middle":
            x -= self.width(text, size, tracking) / 2

        out: list[tuple[str, float]] = []
        cursor = x
        for ch in text:
            gname = self._gname(ch)
            d = ""
            if ch != " ":
                pen = SVGPathPen(self.glyphs, ntos=lambda v: f"{v:.1f}")
                self.glyphs[gname].draw(
                    TransformPen(pen, Transform(scale, 0, 0, -scale, cursor, y))
                )
                d = pen.getCommands()
            cursor += self.hmtx[gname][0] * scale + tracking
            out.append((d, cursor))
        return out


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


def edge_row(face: Face, left: str, right: str, size: float, y: float,
             fill: str, tracking: float, pad: float, width: float,
             gap: float = 40.0) -> str:
    """A band with text flush left and flush right.

    Refuses to emit a row whose two halves would collide — silently overlapping
    type is the one failure mode you cannot see in the generator's output.
    """
    lw = face.width(left, size, tracking)
    rw = face.width(right, size, tracking)
    slack = (width - pad * 2) - lw - rw
    if slack < gap:
        raise ValueError(
            f"edge_row overflow: {left!r} + {right!r} need {gap - slack:.0f}px "
            f"more room at size {size:g}"
        )
    return (text(face, left, size, pad, y, fill, tracking=tracking)
            + text(face, right, size, width - pad, y, fill,
                   tracking=tracking, anchor="end"))


def typed(face: Face, s: str, size: float, x: float, y: float, fill: str,
          start: float, per: float, tracking: float = 0.0,
          anchor: str = "start") -> tuple[list[str], list[float], float]:
    """Draw `s` as one path per character, each keyed to its own delay.

    Returns the paths, the pen x after each character (for a cursor to follow)
    and the moment the last character lands.
    """
    parts: list[str] = []
    stops: list[float] = []
    for i, (d, pen_x) in enumerate(face.glyph_paths(s, size, x, y, tracking, anchor)):
        stops.append(pen_x)
        if d:
            parts.append(
                f'<path class="tp" style="animation-delay:{start + i * per:.3f}s" '
                f'fill="{fill}" d="{d}"/>'
            )
    return parts, stops, start + len(stops) * per


def caret(x: float, y: float, size: float, fill: str, stops: list[float],
          start: float, per: float, name: str) -> tuple[str, str]:
    """A print head that steps along `stops` as each character lands."""
    h = size * 0.74
    total = len(stops) * per
    hold = 0.9                      # blinks here once the line is finished
    dur = start + total + hold

    move = [f"0%{{transform:translateX(0)}}"]
    for i, pen_x in enumerate(stops):
        move.append(
            f"{(i + 1) / len(stops) * 100:.2f}%"
            f"{{transform:translateX({pen_x - x:.1f}px)}}"
        )

    p_in = start / dur * 100
    p_done = (start + total) / dur * 100
    tail = 100 - p_done
    life = (
        f"0%,{p_in:.2f}%{{opacity:0}}"
        f"{p_in + 0.01:.2f}%,{p_done + tail * 0.25:.2f}%{{opacity:1}}"
        f"{p_done + tail * 0.30:.2f}%,{p_done + tail * 0.60:.2f}%{{opacity:0}}"
        f"{p_done + tail * 0.65:.2f}%,{p_done + tail * 0.90:.2f}%{{opacity:1}}"
        f"100%{{opacity:0}}"
    )

    keys = (f"@keyframes {name}-move{{{''.join(move)}}}"
            f"@keyframes {name}-life{{{life}}}")
    # opacity="0" as a presentation attribute, not just CSS: it is the lowest
    # priority style there is, so the keyframes still win while it plays — but a
    # client that drops the <style> block gets a hidden caret instead of a red
    # bar parked next to the first letter.
    el = (f'<rect class="caret" x="{x:.1f}" y="{y - h:.1f}" '
          f'width="{max(4.0, size * 0.055):.1f}" height="{h:.1f}" fill="{fill}" '
          f'opacity="0" '
          f'style="animation:{name}-move {total:.2f}s step-end {start:.2f}s both,'
          f'{name}-life {dur:.2f}s step-end both"/>')
    return el, keys


def svg(width: float, height: float, title: str, body: list[str],
        head: str = "") -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:g} {height:g}" '
        f'width="{width:g}" height="{height:g}" role="img" aria-label="{title}">',
        f"<title>{title}</title>",
    ]
    if head:
        parts.append(head)
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

# The nameplate face. Expanded and heavy, so the ink filter has mass to bite on.
DISPLAY = ("Archivo.ttf", {"wght": 800, "wdth": 125})

HERO_ENTRIES = [
    ("YEARS BUILDING SOFTWARE", "4+", False),
]

# The plate types itself out, top line first, the way the form would come off
# a printer. Every animated element's *resting* style is the finished state, so
# anywhere CSS animation doesn't run — GitHub's mobile app, a feed reader,
# reduced-motion — the plate simply appears complete instead of blank.
#
# (start seconds, seconds per character) for each line of the head, in order.
# Every start is offset past LEAD so that nothing is mid-animation at time
# zero — see the note on the resting state below.
LEAD = 0.02
T_HEAD_L = (LEAD, 0.022)
T_HEAD_R = (LEAD + 0.18, 0.022)
T_NAME = (LEAD + 0.50, 0.052)
T_SUB = (LEAD + 1.32, 0.017)

# The head types itself out, top line first, the way the form would come off a
# printer. Only the head moves; the rules, bars, entry row and footer are
# always drawn, so the plate is legible from the first frame.
#
# `backwards` is load-bearing and its cost is known. Hiding a glyph before its
# turn is only possible by filling backwards, and an SVG timeline that is
# frozen at zero — a directly-opened .svg, a throttled background tab, a
# screenshot pipeline — therefore renders the head blank. Dropping the fill
# mode makes those cases safe but deletes the effect: every glyph would sit
# visible until the 10ms it blinks. Typing wins for the head; everything below
# it (rules, bars, the entry row, the footer) is static, so a frozen renderer
# still gets a plate with its structure and its number intact.
HERO_MOTION = """<style>
@keyframes plate-type { from { opacity: 0 } to { opacity: 1 } }
__KEYS__
.tp { animation: plate-type .01s steps(1, end) backwards }
.caret { opacity: 0 }
@media (prefers-reduced-motion: reduce) {
  .tp, .caret { animation: none !important }
}
</style>"""


def hero(t: Theme, display: Face, mono: Face, mono_md: Face, mono_sb: Face) -> str:
    head_h = 78
    row_h = 56
    foot_h = 46
    rows_top = 276
    height = rows_top + row_h * len(HERO_ENTRIES) + foot_h
    avail = W - PAD * 2

    body: list[str] = [band(0, 0, W, height, t.bar_a)]

    # Greenbar: every other entry row carries the green bar.
    for i in range(len(HERO_ENTRIES)):
        if i % 2 == 0:
            body.append(band(0, rows_top + i * row_h, W, row_h, t.bar_b))

    body.append(
        f'<defs><filter id="ink" x="-1%" y="-6%" width="102%" height="112%" '
        f'color-interpolation-filters="sRGB">'
        f'<feTurbulence type="fractalNoise" baseFrequency="1.7" numOctaves="2" '
        f'seed="11" result="n"/>'
        f'<feDisplacementMap in="SourceGraphic" in2="n" scale="1.0" '
        f'xChannelSelector="R" yChannelSelector="G"/></filter></defs>'
    )

    # Header band — the form's identification line, typed left then right.
    head_l, head_r = "STATEMENT OF WORK", "SHEET 01"
    if avail - mono_md.width(head_l, 20, 4.2) - mono_md.width(head_r, 20, 4.2) < 40:
        raise ValueError("header band halves collide")
    body += typed(mono_md, head_l, 20, PAD, 48, t.muted, *T_HEAD_L, tracking=4.2)[0]
    body += typed(mono_md, head_r, 20, W - PAD, 48, t.muted, *T_HEAD_R,
                  tracking=4.2, anchor="end")[0]
    body.append(rule(PAD, head_h, W - PAD, t.rule))

    # Nameplate. Track the name out to fill the full measure of the plate, then
    # type it character by character with the print head running ahead of it.
    name = "RODRIGO SCHARP"
    size = 98
    tracking = (avail - display.width(name, size)) / (len(name) - 1)
    tracking = max(1.0, min(tracking, 14.0))
    while display.width(name, size, tracking) > avail:
        size -= 1

    glyphs, stops, _ = typed(display, name, size, PAD, 200, t.ink, *T_NAME,
                             tracking=tracking)
    head_el, head_keys = caret(PAD, 200, size, t.red, stops, *T_NAME, "name")
    body += [
        '<g filter="url(#ink)">' + "".join(glyphs) + "</g>",
        head_el,
    ]
    body += typed(mono, "Software Engineer · São Paulo, Brazil", 24, PAD, 244,
                  t.muted, *T_SUB, tracking=2.0)[0]
    body += [
        rule(PAD, rows_top, W - PAD, t.rule),
    ]

    # Entries — label, leader dots, right-aligned figure.
    for i, (label, value, accent) in enumerate(HERO_ENTRIES):
        baseline = rows_top + i * row_h + 36
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
        edge_row(mono_md, "BACKEND · DISTRIBUTED SYSTEMS · FINANCIAL ENGINEERING",
                 "@RODRIGOSCHARP", 18, foot_top + 30, t.muted, 3.2, PAD, W),
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{height - 1}" '
        f'fill="none" stroke="{t.edge}"/>',
    ]

    body.insert(1, HERO_MOTION.replace("__KEYS__", head_keys))

    alt = ("Rodrigo Scharp — Software Engineer, São Paulo, Brazil. "
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
        edge_row(mono_md, "SCHEDULE OF TECHNOLOGIES", "SHEET 02", 20, 48,
                 t.muted, 4.2, PAD, W),
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
        edge_row(mono_md, "AWS · ECS · ALB · CLOUDFRONT · API GATEWAY · LAMBDA",
                 "CI/CD · TESTCONTAINERS", 18, foot_top + 30, t.muted, 3.2, PAD, W),
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

    display = Face(os.path.join(FONTS, DISPLAY[0]), **DISPLAY[1])
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
