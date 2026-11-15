"""Generate the outline symbols of the AI & Engineering and Models tables:
python scripts/generate_engineering.py.

Writes assets/icons/symbols-<theme>.svg. The README shows each symbol as
symbols-<theme>.svg#<name>: one 40-unit tile every 48 units, exposed as a <view>.
"""

from svg_utils import ASSETS, THEMES

SYMBOLS = {
    "generative": '<path d="M20 5L24 16L35 20L24 24L20 35L16 24L5 20L16 16Z"/>'
                  '<path d="M32 4V10M29 7H35M5 30V36M2 33H8"/>',
    "vision": '<path d="M3 20Q20 1 37 20Q20 39 3 20Z"/>'
              '<circle cx="20" cy="20" r="6"/>'
              '<path d="M4 9V4H9M31 4H36V9M4 31V36H9M31 36H36V31"/>',
    "backend": '<rect x="5" y="4" width="30" height="12" rx="3"/>'
               '<rect x="5" y="24" width="30" height="12" rx="3"/>'
               '<path d="M12 10H20M12 30H20M20 16V24"/>'
               '<circle cx="28" cy="10" r="1"/><circle cx="28" cy="30" r="1"/>',
    "cloud": '<path d="M10 25H29A7 7 0 0 0 30 11A10 10 0 0 0 11 12A6.5 6.5 0 0 0 10 25Z"/>'
             '<path d="M28 31A10 10 0 0 1 11 32M11 28V33H6M12 37A10 10 0 0 0 29 36M29 39V34H34"/>',
    "attention": '<circle cx="20" cy="20" r="5"/>'
                 '<circle cx="5" cy="6" r="3"/><circle cx="35" cy="6" r="3"/>'
                 '<circle cx="5" cy="34" r="3"/><circle cx="35" cy="34" r="3"/>'
                 '<path d="M8 9L16 16M24 16L32 9M8 31L16 24M24 24L32 31"/>',
    "boosting": '<rect x="15" y="3" width="10" height="9" rx="2"/>'
                '<path d="M20 12V20H7V28M20 20H33V28"/>'
                '<rect x="2" y="28" width="10" height="9" rx="2"/>'
                '<rect x="28" y="28" width="10" height="9" rx="2"/>',
}
STEP = 48


def sprite(theme):
    width = STEP * len(SYMBOLS) - 8
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="40" viewBox="0 0 {width} 40">',
             f'<g fill="none" stroke="{THEMES[theme]["cyan"]}" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round">']
    for i, markup in enumerate(SYMBOLS.values()):
        parts.append(f'<g transform="translate({STEP * i} 0)">{markup}</g>')
    parts.append('</g>')
    # 2-unit margin keeps round caps on the tile edge visible.
    parts += [f'<view id="{name}" viewBox="{STEP * i - 2} -2 44 44"/>' for i, name in enumerate(SYMBOLS)]
    path = ASSETS / "icons" / f"symbols-{theme}.svg"
    path.write_text("\n".join(parts) + "\n</svg>\n", encoding="utf-8")
    print(f"{path.relative_to(ASSETS.parent)} ({path.stat().st_size:,} bytes)")


def main():
    for theme in ("dark", "light"):
        sprite(theme)


if __name__ == "__main__":
    main()
