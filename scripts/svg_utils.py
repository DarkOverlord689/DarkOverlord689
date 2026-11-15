"""Palette, paths and SVG primitives shared by the profile generators."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
MONO = "Consolas, 'Liberation Mono', monospace"
SANS = "Segoe UI, Arial, sans-serif"
THEMES = {
    "dark": dict(bg="#050c17", panel="#0a1526", inset="#0e1d33", line="#243a55",
                 text="#e5f1ff", muted="#91a9c5", cyan="#50dcf5", blue="#418dff", violet="#a897ff"),
    "light": dict(bg="#f1f7ff", panel="#ffffff", inset="#e8f1fc", line="#b8cde4",
                  text="#112a46", muted="#496584", cyan="#006c83", blue="#175ad0", violet="#6944ba"),
}


class SVG:
    def __init__(self, width, height, theme, title, description):
        self.width, self.height = width, height
        self.c = THEMES[theme]
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
                      f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>',
                      '<defs><linearGradient id="signal" x2="1" y2="1">',
                      f'<stop stop-color="{self.c["cyan"]}"/><stop offset=".6" stop-color="{self.c["blue"]}"/>'
                      f'<stop offset="1" stop-color="{self.c["violet"]}"/></linearGradient>',
                      f'<pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">'
                      f'<path d="M20 0H0V20" fill="none" stroke="{self.c["line"]}" stroke-width=".6"/></pattern></defs>']

    def add(self, markup):
        self.parts.append(markup)

    def rect(self, x, y, width, height, fill="panel", stroke=None, rx=0, extra=""):
        color = self.c.get(fill, fill)
        outline = f' stroke="{self.c.get(stroke, stroke)}"' if stroke else ""
        self.add(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{rx}" fill="{color}"{outline} {extra}/>')

    def line(self, x1, y1, x2, y2, color="line", extra=""):
        self.add(f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{self.c.get(color, color)}" {extra}/>')

    def text(self, x, y, content, size=16, color="text", weight=400, anchor="start", font=MONO, extra=""):
        self.add(f'<text x="{x}" y="{y}" fill="{self.c.get(color, color)}" font-family="{font}" '
                 f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" {extra}>{escape(str(content))}</text>')

    def dot(self, x, y, color="cyan", radius=3, extra=""):
        self.add(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{self.c.get(color, color)}" {extra}/>')

    def frame(self, label, tab=None):
        self.rect(1, 1, self.width - 2, self.height - 2, "bg", "line", 14)
        self.rect(1, 1, self.width - 2, 40, "panel", rx=14)
        for x, color in ((22, "cyan"), (40, "blue"), (58, "violet")):
            self.dot(x, 21, color, 4)
        self.text(82, 26, label, 12, "muted")
        self.line(1, 41, self.width - 1, 41)
        if tab:
            self.rect(1, 42, self.width - 2, 36, "panel")
            self.line(1, 78, self.width - 1, 78)
            self.line(20, 77, 180, 77, "cyan", 'stroke-width="2"')
            self.text(22, 65, tab, 13, "cyan")
            self.text(206, 65, "README.md", 13, "muted")

    def save(self, filename):
        ASSETS.mkdir(exist_ok=True)
        path = ASSETS / filename
        path.write_text("\n".join(self.parts) + "\n</svg>\n", encoding="utf-8")
        print(f"{path.relative_to(ROOT)} ({path.stat().st_size:,} bytes)")
