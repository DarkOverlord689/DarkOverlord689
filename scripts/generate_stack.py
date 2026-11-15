"""Expose each Skill Icons logo as a named view: python scripts/generate_stack.py.

The README shows a logo as assets/icons/<category>-<theme>.svg#<id>. Each sprite comes
from Skill Icons (MIT, see assets/icons/LICENSE.skill-icons) and holds one 256-unit tile
every 300 units; this script rewrites one <view> per tile without touching the logos.
"""

import re

from svg_utils import ASSETS

CATEGORIES = (
    ("cloud", "Cloud & DevOps",
     (("aws", "AWS"), ("docker", "Docker"), ("kubernetes", "Kubernetes"), ("linux", "Linux"))),
    ("ai", "AI / Machine Learning",
     (("python", "Python"), ("pytorch", "PyTorch"), ("tensorflow", "TensorFlow"), ("opencv", "OpenCV"))),
    ("backend", "Backend & Frameworks",
     (("fastapi", "FastAPI"), ("spring", "Spring"), ("nodejs", "Node.js"), ("java", "Java"), ("kotlin", "Kotlin"))),
    ("databases", "Databases",
     (("postgresql", "PostgreSQL"), ("mysql", "MySQL"), ("mongodb", "MongoDB"), ("supabase", "Supabase"))),
    ("frontend", "Frontend",
     (("react", "React"), ("nextjs", "Next.js"), ("tailwindcss", "Tailwind CSS"),
      ("javascript", "JavaScript"), ("typescript", "TypeScript"))),
    ("tools", "Tools & Automation", (("git", "Git"), ("githubactions", "GitHub Actions"))),
)
VIEW = re.compile(r'\n *<view id="[^"]*" viewBox="[^"]*"/>')
TILE = re.compile(r'<g transform="translate\((\d+), 0\)">')


def add_views(category, theme, logos):
    path = ASSETS / "icons" / f"{category}-{theme}.svg"
    text = VIEW.sub("", path.read_text(encoding="utf-8"))
    offsets = [int(x) for x in TILE.findall(text)]
    if offsets != [300 * i for i in range(len(logos))]:
        raise ValueError(f"{path.name}: expected {len(logos)} tiles every 300 units, found {offsets}")
    views = "".join(f'\n  <view id="{slug}" viewBox="{x} 0 256 256"/>' for x, (slug, _) in zip(offsets, logos))
    end = text.rindex("</svg>")
    path.write_text(f"{text[:end].rstrip()}{views}\n{text[end:]}", encoding="utf-8")
    print(f"{path.relative_to(ASSETS.parent)}: {len(logos)} views")


def main():
    for category, _, logos in CATEGORIES:
        for theme in ("dark", "light"):
            add_views(category, theme, logos)


if __name__ == "__main__":
    main()
