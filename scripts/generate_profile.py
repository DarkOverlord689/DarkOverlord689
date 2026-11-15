"""Generate the banner, whoami terminal and specialties SVGs: python scripts/generate_profile.py."""

from random import Random

from svg_utils import SVG


PARTICLE_CYCLE_SECONDS = 5.6


def inside_polygon(x, y, vertices):
    """Point-in-polygon test (ray crossing) for the D stencil."""
    inside = False
    previous_x, previous_y = vertices[-1]
    for current_x, current_y in vertices:
        if (current_y > y) != (previous_y > y):
            crossing_x = current_x + (y - current_y) * (previous_x - current_x) / (previous_y - current_y)
            if x < crossing_x:
                inside = not inside
        previous_x, previous_y = current_x, current_y
    return inside


def d_particles():
    """Deterministic 6-unit dot lattice with a seeded dispersed starting field."""
    outer = ((76, 40), (138, 40), (190, 80), (190, 148), (138, 188), (76, 188))
    inner = ((100, 66), (130, 66), (164, 92), (164, 136), (130, 162), (100, 162))
    rng = Random(689)
    particles = []
    for y in range(43, 188, 6):
        for x in range(79, 190, 6):
            if inside_polygon(x, y, outer) and not inside_polygon(x, y, inner):
                start_x, start_y = rng.uniform(26, 234), rng.uniform(25, 204)
                gradient = .35 * (x - 76) / 114 + .65 * (y - 40) / 148
                color = "cyan" if gradient < .45 else "blue" if gradient < .88 else "violet"
                particles.append((x, y, round(start_x - x, 1), round(start_y - y, 1), color))
    return particles


def monogram(svg, x, y, scale=1):
    """Particle D with a seamless CSS loop.

    0..12%: dispersed fade-in; 12..48%: converge; 48..82%: hold/pulse;
    82..100%: disperse back to the initial state.
    Unsupported animation and reduced motion show the assembled D.
    """
    svg.add(f'<g transform="translate({x} {y}) scale({scale})">')
    svg.rect(0, 0, 260, 248, "inset", "line", 8)
    svg.rect(1, 1, 258, 246, "url(#grid)", rx=8)
    for r in (78, 100):
        svg.add(f'<circle cx="130" cy="114" r="{r}" fill="none" stroke="{svg.c["line"]}" stroke-dasharray="3 7"/>')
    svg.add('<defs><filter id="particle-glow" x="-15%" y="-15%" width="130%" height="130%">'
            '<feGaussianBlur stdDeviation="1.1" result="bloom"/>'
            '<feMerge><feMergeNode in="bloom"/><feMergeNode in="SourceGraphic"/></feMerge>'
            '</filter></defs>')
    duration = f"{PARTICLE_CYCLE_SECONDS:g}s"
    svg.add('<style>'
            f'#d-particles{{opacity:.86;animation:particle-light {duration} ease-in-out infinite}}'
            f'#d-particles circle{{animation:particle-assemble {duration} cubic-bezier(.4,0,.2,1) infinite}}'
            '@keyframes particle-assemble{'
            '0%,12%,100%{transform:translate(var(--sx),var(--sy))}'
            '48%,82%{transform:translate(0px,0px)}}'
            '@keyframes particle-light{0%,100%{opacity:.08}12%{opacity:.3}'
            '48%,82%{opacity:.8}62%{opacity:1}}'
            '@media(prefers-reduced-motion:reduce){'
            '#d-particles,#d-particles circle{animation:none}'
            '#d-particles circle{transform:none}}'
            '</style>')
    particles = d_particles()
    svg.add('<g id="d-particles" filter="url(#particle-glow)">')
    for color in ("cyan", "blue", "violet"):
        svg.add(f'<g fill="{svg.c[color]}">')
        for px, py, dx, dy, particle_color in particles:
            if particle_color == color:
                svg.add(f'<circle cx="{px}" cy="{py}" r="1.65" style="--sx:{dx:g}px;--sy:{dy:g}px"/>')
        svg.add('</g>')
    svg.add('</g>')
    svg.add(f'<path d="M17 82H56V114H80M180 114H212V157H243M130 181V211H207" '
            f'fill="none" stroke="{svg.c["cyan"]}" stroke-width="2"/>')
    for px, py in ((17, 82), (243, 157), (207, 211)):
        svg.dot(px, py, "cyan", 3)
    svg.text(16, 230, "D / IDENTITY MODULE", 11, "muted")
    svg.add('</g>')


def yaml_rows(svg, x, y):
    rows = [
        ("profile:", "", 0),
        ("name:", 'Gabriel "Darksi"', 1),
        ("handle:", "DarkOverlord689", 1),
        ("location:", "Perú", 1),
        ("focus:", "", 1),
        ("-", "AI Engineering", 2),
        ("-", "Backend Development", 2),
        ("-", "Automation", 2),
        ("-", "DevOps", 2),
    ]
    for i, (key, value, indent) in enumerate(rows):
        yy = y + i * 31
        svg.text(x - 18, yy, f"{i + 1:02}", 12, "muted", anchor="end")
        xx = x + indent * 18
        svg.text(xx, yy, key, 17, "violet" if not indent else "cyan")
        if value:
            svg.text(xx + len(key) * 10.2 + 10, yy, value, 17)


def banner(theme):
    w, h = 960, 486
    svg = SVG(w, h, theme, 'Gabriel “Darksi” · AI Engineering / Backend Development',
              'Original IDE profile. Abstract D formed by animated particles in a subtle 5.6-second loop. DarkOverlord689, Perú. AI Engineering, Backend Development, Automation and DevOps.')
    svg.frame("darksi / profile workspace", "profile.yaml")
    # Activity rail, left identity module and right configuration editor.
    svg.rect(1, 79, 38, 370, "panel")
    for yy in (104, 142, 180):
        svg.rect(13, yy, 14, 17, "none", "muted", 2)
    svg.line(39, 79, 39, 449)
    monogram(svg, 60, 98)
    svg.text(60, 383, "GABRIEL", 31, weight=700, font="Segoe UI, Arial, sans-serif")
    svg.text(60, 414, '“DARKSI”', 25, "cyan", 700)
    svg.line(342, 79, 342, 449)
    svg.text(368, 108, "IDENTITY / CONFIGURATION", 12, "muted")
    yaml_rows(svg, 396, 143)
    svg.text(396, 438, "# AI, automation & scalable systems", 14, "muted")
    svg.rect(1, h - 36, w - 2, 35, "inset", rx=10)
    svg.dot(22, h - 17, "cyan", 3)
    svg.text(34, h - 12, "DarkOverlord689", 12, "cyan")
    svg.text(w - 20, h - 12, "YAML / UTF-8", 12, "muted", anchor="end")
    svg.save(f"banner-{theme}.svg")


def terminal(theme):
    w, h = 960, 340
    svg = SVG(w, h, theme, "$ whoami · Gabriel Darksi",
              "AI Engineer / Backend Developer in Perú. 6+ years building software solutions. Mission: scalable systems, intelligent automation and AI-powered solutions. Generative AI, RAG, LLM integrations, computer vision, OCR and document processing.")
    svg.frame("darksi@profile: ~ / identity")
    svg.text(24, 79, "$ whoami", 20, "cyan", 700)
    svg.text(24, 112, "Gabriel “Darksi”", 23, weight=700)
    svg.text(24, 139, "AI Engineer / Backend Developer", 17, "violet")
    for i, (key, value) in enumerate((
        ("location", "Perú"), ("experience", "6+ years building software solutions"),
        ("mission", "Scalable systems, intelligent automation"), ("", "& AI-powered solutions"),
    )):
        svg.text(24, 180 + i * 28, key, 14, "muted")
        svg.text(144, 180 + i * 28, value, 17)
    svg.line(596, 65, 596, 295)
    svg.text(624, 83, "$ ls engineering/", 18, "cyan", 700)
    for i, text in enumerate(("Generative AI / RAG", "LLM Integrations", "Computer Vision / OCR", "Backend Architecture", "Cloud / Automation")):
        svg.dot(628, 116 + i * 31, "blue", 2)
        svg.text(642, 122 + i * 31, text, 16)
    svg.text(24, 310, "$", 18, "cyan")
    svg.rect(47, 295, 9, 18, "cyan")
    svg.text(w - 24, 310, "gabriel.snk14@gmail.com", 13, "muted", anchor="end")
    svg.save(f"whoami-{theme}.svg")


def typing(theme):
    """Single-line specialties; reduced motion is handled inside the SVG itself."""
    svg = SVG(640, 62, theme, "AI Engineering · Backend · Automation · DevOps",
              "Specialties from the profile, animated locally with CSS. No external typing service or JavaScript.")
    svg.add('<style>.typed{animation:reveal 10s steps(44,end) infinite}@keyframes reveal{0%,5%{clip-path:inset(0 100% 0 0)}'
            '45%,90%{clip-path:inset(0 0 0 0)}100%{clip-path:inset(0 100% 0 0)}}'
            '@media(prefers-reduced-motion:reduce){.typed{animation:none;clip-path:none}}</style>')
    svg.add('<g class="typed">')
    svg.text(12, 49, "AI Engineering · Backend · Automation · DevOps", 20, "cyan", 700)
    svg.add('</g>')
    svg.save(f"typing-{theme}.svg")


def main():
    # One horizontal composition per theme. With a pinned theme, GitHub's
    # <themed-picture> rewrites the whole media attribute of each themed <source>,
    # so README pictures must use only (prefers-color-scheme: dark|light).
    for theme in ("dark", "light"):
        banner(theme)
        terminal(theme)
        typing(theme)


if __name__ == "__main__":
    main()
