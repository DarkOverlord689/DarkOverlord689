"""Generate the 2x3 technology dashboard: python scripts/generate_stack.py.

Logos are embedded from the local Skill Icons sprites in assets/icons/ (MIT, see
assets/icons/LICENSE.skill-icons). IDs and references are scoped per logo, so the
final SVG has no external images or dependencies.
"""

from copy import deepcopy
from html import escape
import re
import xml.etree.ElementTree as ET

from svg_utils import ASSETS, SVG, SANS

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")

CATEGORIES = (
    ("cloud", "Cloud & DevOps", ("AWS", "Docker", "Kubernetes", "Linux")),
    ("ai", "AI / Machine Learning", ("Python", "PyTorch", "TensorFlow", "OpenCV")),
    ("backend", "Backend & Frameworks", ("FastAPI", "Spring", "Node.js", "Java", "Kotlin")),
    ("databases", "Databases", ("PostgreSQL", "MySQL", "MongoDB", "Supabase")),
    ("frontend", "Frontend", ("React", "Next.js", "Tailwind CSS", "JavaScript", "TypeScript")),
    ("tools", "Tools & Automation", ("Git", "GitHub Actions")),
)


def local_icons(category, theme, count):
    """Extract each 256-unit logo viewport without altering the branded vectors."""
    source = ASSETS / "icons" / f"{category}-{theme}.svg"
    root = ET.parse(source).getroot()
    icons = [group.find(f"{{{NS}}}svg") for group in root.findall(f"{{{NS}}}g")]
    if len(icons) != count or any(icon is None for icon in icons):
        raise ValueError(f"{source.name}: expected {count} individual logo viewports")
    return icons


def embed_icon(svg, source, prefix, name, x, y, size):
    icon = deepcopy(source)
    ids = {element.get("id"): f"{prefix}-{element.get('id')}" for element in icon.iter() if element.get("id")}

    def scope(value):
        value = re.sub(r"url\(#([^)]+)\)", lambda match: f"url(#{ids[match[1]]})", value)
        if value.startswith("#") and value[1:] in ids:
            value = "#" + ids[value[1:]]
        return value

    for element in icon.iter():
        for key, value in list(element.attrib.items()):
            element.set(key, ids[value] if key == "id" else scope(value))
        if element.tag == f"{{{NS}}}style" and element.text:
            element.text = scope(element.text)
    for key, value in {"x": x, "y": y, "width": size, "height": size}.items():
        icon.set(key, f"{value:g}")
    icon.set("preserveAspectRatio", "xMidYMid meet")
    svg.add(f'<g id="{prefix}" data-tech="{escape(name, quote=True)}">'
            f'<title>{escape(name)}</title>{ET.tostring(icon, encoding="unicode")}</g>')


def dashboard(theme):
    w, h = 960, 654
    summary = "; ".join(f"{title}: {', '.join(names)}" for _, title, names in CATEGORIES)
    svg = SVG(w, h, theme, "$ cat tech-stack.yaml · Technology dashboard", summary)
    svg.frame("darksi@profile: ~ / stack")
    card_width, card_height, logo_size = 447, 178, 64
    for index, (key, title, names) in enumerate(CATEGORIES):
        x = 24 + (index % 2) * 465
        y = 64 + (index // 2) * 194
        svg.add(f'<g id="stack-card-{key}" data-category="{escape(title, quote=True)}">')
        svg.rect(x, y, card_width, card_height, "inset", "line", 11)
        svg.rect(x + 16, y + 15, 32, 25, "panel", "line", 6)
        svg.text(x + 32, y + 32, f"{index + 1:02}", 12, "cyan", 700, anchor="middle")
        svg.text(x + 62, y + 34, title, 20, weight=700, font=SANS)
        svg.line(x + 18, y + 53, x + card_width - 18, y + 53)
        svg.line(x + 18, y + 53, x + 72, y + 53, "blue", 'stroke-width="2"')
        # Equal-width slots make all logo baselines and captions line up.
        logos = local_icons(key, theme, len(names))
        count = len(names)
        slot = min(144 if count == 2 else 100, (card_width - 40) / count)
        left = x + (card_width - slot * count) / 2
        for i in range(count):
            center = left + slot * (i + .5)
            embed_icon(svg, logos[i], f"stack-icon-{key}-{i}", names[i], center - logo_size / 2, y + 70, logo_size)
            svg.text(f"{center:.2f}", y + 157, names[i], 14, "text", anchor="middle", font=SANS)
        svg.add('</g>')
    svg.save(f"tech-stack-{theme}.svg")


def main():
    for theme in ("dark", "light"):
        dashboard(theme)


if __name__ == "__main__":
    main()
