"""Generate the two radar charts: python scripts/radar.py.

Edit assets/skills.json and assets/langmix.json, then regenerate. Values 0..5
control the illustrative shape only; they never claim measured proficiency.
"""

import json
import math

from svg_utils import ASSETS, SVG, SANS


def load_data(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("kind") != "illustrative":
        raise ValueError(f"{path.name}: kind must remain illustrative; measured skills need separate evidence.")
    axes = data["axes"]
    if not 3 <= len(axes) <= 8:
        raise ValueError("A radar needs 3 to 8 axes.")
    for axis in axes:
        value = axis["value"]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or not 0 <= value <= 5:
            raise ValueError(f"Invalid illustrative value for {axis['label']}: expected 0..5.")
        if not isinstance(axis["label"], str) or not 1 <= len(axis["label"]) <= 18:
            raise ValueError("Axis labels must have 1 to 18 characters.")
    return data


def render(data, theme, filename, index):
    svg = SVG(460, 430, theme, f"{data['title']} · illustrative only",
              "Illustrative radar, not a skill assessment, proficiency score, percentage or repository language distribution. "
              + ", ".join(axis["label"] for axis in data["axes"]))
    svg.rect(1, 1, 458, 428, "panel", "line", 12)
    svg.text(22, 28, f"0{index} / PROFILE MAP", 11, "muted")
    svg.text(22, 58, data["title"], 23, weight=700, font=SANS)
    svg.line(22, 77, 438, 77)
    cx, cy, radius = 230, 230, 104
    axes = data["axes"]
    count = len(axes)
    vectors = [(math.cos(-math.pi / 2 + i * math.tau / count), math.sin(-math.pi / 2 + i * math.tau / count)) for i in range(count)]

    def points(factors):
        return " ".join(f"{cx + dx * radius * value:.2f},{cy + dy * radius * value:.2f}" for (dx, dy), value in zip(vectors, factors))

    for ring in (1, .75, .5, .25):
        svg.add(f'<polygon points="{points([ring] * count)}" fill="none" stroke="{svg.c["line"]}"/>')
    for dx, dy in vectors:
        svg.line(cx, cy, f"{cx + radius * dx:.2f}", f"{cy + radius * dy:.2f}")
    svg.add(f'<polygon points="{points([axis["value"] / 5 for axis in axes])}" fill="{svg.c["cyan"]}" '
            f'fill-opacity=".13" stroke="{svg.c["cyan"]}" stroke-width="2.5" stroke-linejoin="round"/>')
    for (dx, dy), axis in zip(vectors, axes):
        value = axis["value"] / 5
        svg.dot(f"{cx + radius * dx * value:.2f}", f"{cy + radius * dy * value:.2f}", "cyan", 3.5)
        x, y = cx + dx * (radius + 19), cy + dy * (radius + 19)
        anchor = "middle" if abs(dx) < .1 else ("start" if dx > 0 else "end")
        svg.text(f"{x:.2f}", f"{y + (17 if dy > .8 else -8 if dy < -.8 else 5):.2f}", axis["label"], 15, anchor=anchor, font=SANS)
    svg.line(22, 382, 438, 382)
    svg.dot(26, 405, "violet", 3)
    svg.text(38, 410, "ILLUSTRATIVE / NOT A SKILL SCORE", 11, "muted")
    svg.save(f"{filename}-{theme}.svg")


def main():
    for i, (source, target) in enumerate((("skills.json", "radar"), ("langmix.json", "radar-langs")), 1):
        data = load_data(ASSETS / source)
        for theme in ("dark", "light"):
            render(data, theme, target, i)


if __name__ == "__main__":
    main()
