"""Generate the AI & Engineering and Models panels: python scripts/generate_engineering.py."""

from svg_utils import SVG, SANS


def icon(svg, kind, x, y, size=44):
    """Outline symbol drawn on a 40-unit grid and scaled to `size`."""
    svg.add(f'<g transform="translate({x} {y}) scale({size / 40:g})" '
            f'fill="none" stroke="{svg.c["cyan"]}" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round">')
    if kind == "generative":
        svg.add('<path d="M20 5L24 16L35 20L24 24L20 35L16 24L5 20L16 16Z"/>'
                '<path d="M32 4V10M29 7H35M5 30V36M2 33H8"/>')
    elif kind == "vision":
        svg.add('<path d="M3 20Q20 1 37 20Q20 39 3 20Z"/>'
                '<circle cx="20" cy="20" r="6"/>'
                '<path d="M4 9V4H9M31 4H36V9M4 31V36H9M31 36H36V31"/>')
    elif kind == "backend":
        svg.add('<rect x="5" y="4" width="30" height="12" rx="3"/>'
                '<rect x="5" y="24" width="30" height="12" rx="3"/>'
                '<path d="M12 10H20M12 30H20M20 16V24"/>'
                '<circle cx="28" cy="10" r="1"/><circle cx="28" cy="30" r="1"/>')
    elif kind == "cloud":
        svg.add('<path d="M10 25H29A7 7 0 0 0 30 11A10 10 0 0 0 11 12A6.5 6.5 0 0 0 10 25Z"/>'
                '<path d="M28 31A10 10 0 0 1 11 32M11 28V33H6M12 37A10 10 0 0 0 29 36M29 39V34H34"/>')
    elif kind == "attention":
        svg.add('<circle cx="20" cy="20" r="5"/>'
                '<circle cx="5" cy="6" r="3"/><circle cx="35" cy="6" r="3"/>'
                '<circle cx="5" cy="34" r="3"/><circle cx="35" cy="34" r="3"/>'
                '<path d="M8 9L16 16M24 16L32 9M8 31L16 24M24 24L32 31"/>')
    elif kind == "boosting":
        svg.add('<rect x="15" y="3" width="10" height="9" rx="2"/>'
                '<path d="M20 12V20H7V28M20 20H33V28"/>'
                '<rect x="2" y="28" width="10" height="9" rx="2"/>'
                '<rect x="28" y="28" width="10" height="9" rx="2"/>')
    else:
        raise ValueError(f"Unknown icon: {kind}")
    svg.add('</g>')


CAPABILITIES = (
    ("Generative AI", "generative", "RAG Systems", "LLM Integrations"),
    ("Computer Vision", "vision", "OCR & Document Processing", "Computer Vision"),
    ("Backend Systems", "backend", "Backend Architecture", "Scalable systems"),
    ("Cloud / Automation", "cloud", "Cloud Infrastructure", "Intelligent automation"),
)


def engineering(theme):
    w, h = 960, 464
    svg = SVG(w, h, theme, "AI & Engineering · four focus areas",
              "Generative AI: RAG Systems and LLM Integrations. Computer Vision: OCR and Document Processing. "
              "Backend Systems: Backend Architecture and scalable systems. Cloud / Automation: Cloud Infrastructure and intelligent automation.")
    svg.frame("engineering / capabilities")
    svg.text(24, 77, "capabilities.map", 17, "cyan", 700)
    svg.text(w - 24, 76, "AI / VISION / SYSTEMS / CLOUD", 11, "muted", anchor="end")
    card_w, card_h = 447, 156
    for i, (title, symbol, first, second) in enumerate(CAPABILITIES):
        x = 24 + (i % 2) * 465
        y = 100 + (i // 2) * 174
        svg.rect(x, y, card_w, card_h, "inset", "line", 9)
        svg.line(x + 1, y + 20, x + 1, y + card_h - 20, "blue", 'stroke-width="2"')
        svg.rect(x + 18, y + 22, 50, 50, "panel", "line", 12)
        icon(svg, symbol, x + 26, y + 30, 34)
        svg.text(x + card_w - 18, y + 25, f"0{i + 1}", 11, "muted", anchor="end")
        svg.text(x + 84, y + 48, title, 22, weight=700, font=SANS)
        svg.line(x + 84, y + 67, x + card_w - 20, y + 67)
        svg.text(x + 84, y + 99, first, 18, "text", font=SANS)
        if symbol != "vision":
            svg.text(x + 84, y + 127, second, 18, "muted", font=SANS)
        else:
            svg.text(x + 84, y + 127, "Image & document workflows", 18, "muted", font=SANS)
    svg.line(24, h - 26, w - 24, h - 26)
    svg.text(24, h - 10, "focus / intelligent systems", 11, "muted")
    svg.save(f"engineering-{theme}.svg")


def models(theme):
    w, h = 960, 416
    svg = SVG(w, h, theme, "Models · architecture registry",
              "Vision / CNN architectures: EfficientNetV2, ResNet, MobileNet, Inception, Xception. "
              "Attention architectures: Transformers. Gradient-boosted trees: XGBoost. Model names from the profile, no scores or deployment claims.")
    svg.frame("models / architecture registry")
    svg.text(24, 77, "models.registry", 17, "cyan", 700)
    svg.text(w - 24, 76, "FAMILY / MODEL NAMES", 11, "muted", anchor="end")
    svg.rect(24, 100, 912, 278, "inset", "line", 9)
    svg.line(244, 101, 244, 377)
    svg.line(24, 218, 936, 218)
    svg.line(24, 298, 936, 298)
    for y, symbol, title, subtitle in (
        (100, "vision", "Vision", "CNN architectures"),
        (218, "attention", "Attention", "Transformer family"),
        (298, "boosting", "Boosting", "Tree ensembles"),
    ):
        icon(svg, symbol, 44, y + 23, 34)
        svg.text(96, y + 41, title, 21, weight=700, font=SANS)
        svg.text(96, y + 64, subtitle, 13, "muted", font=SANS)
    svg.text(270, 146, "EfficientNetV2 · ResNet · MobileNet", 22, font=SANS)
    svg.text(270, 184, "Inception · Xception", 22, "muted", font=SANS)
    svg.text(270, 267, "Transformers", 23, font=SANS)
    svg.text(270, 347, "XGBoost", 23, font=SANS)
    svg.line(24, h - 26, w - 24, h - 26)
    svg.text(24, h - 10, "registry / documented model families", 11, "muted")
    svg.save(f"models-{theme}.svg")


def main():
    for theme in ("dark", "light"):
        engineering(theme)
        models(theme)


if __name__ == "__main__":
    main()
