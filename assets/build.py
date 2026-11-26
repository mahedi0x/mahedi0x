"""
Builds the animated SVG cards for the mahedi0x profile README.

    python assets/build.py

Writes hero.svg, now.svg, neofetch-card.svg, orbit.svg and footer.svg next to
this file. Edit the PROFILE block below and run it again to change any text.
No third-party packages needed.
"""
import math
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent

# ---------------------------------------------------------------- profile ---
PROFILE = {
    "name": "Mahedi Hasan",
    "handle": "mahedi0x",
    "title": "Full Stack Web Developer",
    "roles": [
        "Full Stack Web Developer",
        "React & Next.js on the front",
        "Node.js, Python & PHP on the back",
        "Learning ML to bring AI into web apps",
    ],
    "email": "mahedi.swe04@gmail.com",
    "now": [
        ("building", "dynamic, scalable full stack web apps"),
        ("learning", "Machine Learning to integrate AI into web apps"),
        ("improving", "advanced web security practices"),
        ("practicing", "Data Structures & Algorithms"),
        ("portfolio", "coming soon..."),
        ("contact", "mahedi.swe04@gmail.com"),
    ],
}

# Tokyo Night palette (matches the old README theme)
BG, BG2, LINE = "#0B0F1A", "#111729", "#1F2A44"
FG, MUTED = "#C0CAF5", "#7A84A8"
BLUE, CYAN, GREEN, PURPLE, PINK, ORANGE, YELLOW = (
    "#7AA2F7", "#7DCFFF", "#9ECE6A", "#BB9AF7", "#F7768E", "#FF9E64", "#E0AF68")
MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
SANS = "'Segoe UI','Inter',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"

# Tech stack: (label, brand colour, ring)
STACK = [
    ("React", "#61DAFB", 0), ("Next.js", "#FFFFFF", 0), ("Node.js", "#5FA04E", 0),
    ("JavaScript", "#F7DF1E", 0), ("Tailwind", "#38BDF8", 0),
    ("HTML5", "#E34F26", 1), ("CSS3", "#1572B6", 1), ("Python", "#FFD43B", 1),
    ("PHP", "#8892BF", 1), ("MySQL", "#4479A1", 1), ("Git", "#F05032", 1),
    ("GitHub", "#E6EDF3", 1),
]


def write(name, body):
    (OUT / name).write_text(body.strip() + "\n", encoding="utf-8")
    print("wrote", name)


def frame(w, h, inner, extra_defs="", style=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xml:space="preserve">
<defs>
  <linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{BLUE}"/><stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{CYAN}"/>
  </linearGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M32 0H0V32" stroke="{LINE}" stroke-width="1" opacity=".45"/>
  </pattern>
  {extra_defs}
</defs>
<style>{style}</style>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="{BG}" stroke="{LINE}"/>
{inner}
</svg>"""


# ------------------------------------------------------------------ hero ---
def hero():
    w, h = 1200, 360
    roles = PROFILE["roles"]
    n, slot = len(roles), 3.2
    total = n * slot
    style = f"""
    .role{{opacity:0;animation:cycle {total}s infinite}}
    {''.join(f'.r{i}{{animation-delay:{i*slot}s}}' for i in range(n))}
    @keyframes cycle{{0%{{opacity:0;transform:translateY(8px)}}
      3%,{100/n-4:.1f}%{{opacity:1;transform:translateY(0)}}
      {100/n:.1f}%,100%{{opacity:0;transform:translateY(-8px)}}}}
    .blink{{animation:blink 1s steps(1) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    .float{{animation:float 7s ease-in-out infinite}}
    .float2{{animation:float 9s ease-in-out infinite reverse}}
    @keyframes float{{50%{{transform:translate(18px,-12px)}}}}
    .dot{{animation:pulse 2s ease-in-out infinite}}
    @keyframes pulse{{50%{{opacity:.3}}}}
    """
    defs = f"""
  <radialGradient id="g1"><stop offset="0" stop-color="{BLUE}" stop-opacity=".45"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".35"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>
  <clipPath id="card"><rect width="{w}" height="{h}" rx="18"/></clipPath>"""
    role_text = "".join(
        f'<text class="role r{i}" x="80" y="232" font-family="{MONO}" font-size="26" fill="{CYAN}">'
        f'<tspan fill="{GREEN}">&gt; </tspan>{escape(r)}</text>' for i, r in enumerate(roles))
    code = [
        ("const", PURPLE, " dev", FG, " = {", MUTED),
        ("  name", BLUE, ': "Mahedi"', GREEN, ",", MUTED),
        ("  stack", BLUE, ': "MERN+"', GREEN, ",", MUTED),
        ("  coffee", BLUE, ": Infinity", ORANGE, ",", MUTED),
        ("  learning", BLUE, ': "ML"', GREEN, "", MUTED),
        ("}", MUTED, "", FG, ";", MUTED),
    ]
    code_svg = "".join(
        f'<text x="20" y="{58+i*24}" font-family="{MONO}" font-size="15">'
        f'<tspan fill="{a2}">{escape(a)}</tspan><tspan fill="{b2}">{escape(b)}</tspan><tspan fill="{c2}">{escape(c)}</tspan></text>'
        for i, (a, a2, b, b2, c, c2) in enumerate(code))
    inner = f"""
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="url(#grid)"/>
  <circle class="float" cx="980" cy="70" r="260" fill="url(#g1)"/>
  <circle class="float2" cx="160" cy="330" r="220" fill="url(#g2)"/>
</g>
<text x="80" y="96" font-family="{MONO}" font-size="18" fill="{MUTED}">// hello world</text>
<text x="80" y="164" font-family="{SANS}" font-size="56" font-weight="800" fill="{FG}">Hi, I'm <tspan fill="url(#brand)">{escape(PROFILE['name'])}</tspan></text>
{role_text}
<rect class="blink" x="80" y="252" width="14" height="4" fill="{CYAN}"/>
<g transform="translate(80 290)">
  <circle class="dot" cx="6" cy="0" r="5" fill="{GREEN}"/>
  <text x="20" y="5" font-family="{MONO}" font-size="15" fill="{MUTED}">github.com/{PROFILE['handle']}  ·  {escape(PROFILE['email'])}</text>
</g>
<g transform="translate(830 92)">
  <rect width="300" height="186" rx="12" fill="{BG2}" stroke="{LINE}"/>
  <circle cx="20" cy="18" r="5" fill="{PINK}"/><circle cx="38" cy="18" r="5" fill="{YELLOW}"/><circle cx="56" cy="18" r="5" fill="{GREEN}"/>
  <text x="280" y="22" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">dev.js</text>
  {code_svg}
</g>"""
    write("hero.svg", frame(w, h, inner, defs, style))


# ------------------------------------------------------------------- now ---
def now():
    rows = PROFILE["now"]
    w, h = 1200, 110 + len(rows) * 34
    colors = [GREEN, CYAN, ORANGE, PURPLE, YELLOW, BLUE, PINK]
    style = "".join(
        f".l{i}{{opacity:0;animation:in .5s ease-out {0.4+i*0.45:.2f}s forwards}}"
        for i in range(len(rows) + 1))
    style += "@keyframes in{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}"
    style += ".blink{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
    lines = "".join(
        f'<text class="l{i}" x="44" y="{108+i*34}" font-family="{MONO}" font-size="19">'
        f'<tspan fill="{colors[i % len(colors)]}">{k:<11}</tspan><tspan fill="{MUTED}">→ </tspan>'
        f'<tspan fill="{FG}">{escape(v)}</tspan></text>'
        for i, (k, v) in enumerate(rows))
    end_y = 108 + len(rows) * 34
    inner = f"""
<rect x="1" y="1" width="{w-2}" height="44" rx="17" fill="{BG2}"/>
<rect x="1" y="30" width="{w-2}" height="16" fill="{BG2}"/>
<line x1="0" y1="46" x2="{w}" y2="46" stroke="{LINE}"/>
<circle cx="28" cy="23" r="6" fill="{PINK}"/><circle cx="48" cy="23" r="6" fill="{YELLOW}"/><circle cx="68" cy="23" r="6" fill="{GREEN}"/>
<text x="{w/2}" y="28" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{MUTED}">mahedi@github: ~/now</text>
<text x="44" y="78" font-family="{MONO}" font-size="19"><tspan fill="{GREEN}">$</tspan><tspan fill="{FG}"> cat status.txt</tspan></text>
{lines}
<text class="l{len(rows)}" x="44" y="{end_y}" font-family="{MONO}" font-size="19" fill="{GREEN}">$<tspan class="blink" fill="{FG}"> _</tspan></text>"""
    write("now.svg", frame(w, h, inner, style=style))


# -------------------------------------------------------------- neofetch ---
def neofetch():
    w, h = 1200, 420
    # "MH" drawn as a pixel grid (5x7 per letter)
    glyphs = {
        "M": ["1...1", "11.11", "1.1.1", "1.1.1", "1...1", "1...1", "1...1"],
        "H": ["1...1", "1...1", "1...1", "11111", "1...1", "1...1", "1...1"],
    }
    px, gap, ox, oy = 26, 4, 70, 104
    art_svg = ""
    for li, ch in enumerate("MH"):
        for r, row in enumerate(glyphs[ch]):
            for c, bit in enumerate(row):
                if bit == "1":
                    x = ox + (li * 6 + c) * (px + gap)
                    y = oy + r * (px + gap)
                    d = (li * 6 + c + r) * 0.06
                    art_svg += (f'<rect class="px" style="animation-delay:{d:.2f}s" x="{x}" y="{y}" '
                                f'width="{px}" height="{px}" rx="5" fill="url(#brand)"/>')
    info = [
        ("OS", "Full Stack Web Developer"),
        ("Host", f"github.com/{PROFILE['handle']}"),
        ("Kernel", "JavaScript / TypeScript"),
        ("Frontend", "React, Next.js, Tailwind CSS"),
        ("Backend", "Node.js, Python, PHP"),
        ("Database", "MySQL"),
        ("Tools", "Git, GitHub, VS Code"),
        ("Learning", "Machine Learning, Security, DSA"),
        ("Uptime", "∞ cups of coffee"),
        ("Email", PROFILE["email"]),
    ]
    x0 = 520
    info_svg = "".join(
        f'<text x="{x0}" y="{124+i*24}" font-family="{MONO}" font-size="16">'
        f'<tspan fill="{BLUE}" font-weight="700">{escape(k)}</tspan><tspan fill="{MUTED}">: </tspan>'
        f'<tspan fill="{FG}">{escape(v)}</tspan></text>' for i, (k, v) in enumerate(info))
    swatches = "".join(
        f'<rect x="{x0+i*34}" y="{124+len(info)*24}" width="28" height="16" rx="3" fill="{c}"/>'
        for i, c in enumerate([PINK, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, FG]))
    user = f"{PROFILE['handle']}@github"
    inner = f"""
<text x="60" y="66" font-family="{MONO}" font-size="16"><tspan fill="{GREEN}">➜ </tspan><tspan fill="{CYAN}">~ </tspan><tspan fill="{FG}">neofetch</tspan></text>
{art_svg}
<text x="60" y="354" font-family="{MONO}" font-size="14" fill="{MUTED}">"Breaking complex ideas into simple solutions."</text>
<text x="{x0}" y="78" font-family="{MONO}" font-size="18" font-weight="700"><tspan fill="{PURPLE}">{PROFILE['handle']}</tspan><tspan fill="{FG}">@</tspan><tspan fill="{CYAN}">github</tspan></text>
<text x="{x0}" y="98" font-family="{MONO}" font-size="16" fill="{MUTED}">{'─'*len(user)}</text>
{info_svg}
{swatches}"""
    style = ".px{animation:glow 3s ease-in-out infinite}@keyframes glow{50%{opacity:.45}}"
    defs = f'<linearGradient id="brand2" gradientUnits="userSpaceOnUse" x1="70" y1="0" x2="420" y2="0"><stop offset="0" stop-color="{BLUE}"/><stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>'
    write("neofetch-card.svg", frame(w, h, inner.replace("url(#brand)\"/>", "url(#brand2)\"/>"), defs, style))


# ----------------------------------------------------------------- orbit ---
def orbit():
    w, h = 1200, 600
    cx, cy = w / 2, h / 2
    radii = [150, 240]
    durations = [40, 60]
    rings, chips = "", {0: "", 1: ""}
    for r in radii:
        rings += f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{LINE}" stroke-dasharray="4 8"/>'
    for ring in (0, 1):
        items = [s for s in STACK if s[2] == ring]
        for i, (label, color, _) in enumerate(items):
            a = 2 * math.pi * i / len(items) - math.pi / 2
            x, y = cx + radii[ring] * math.cos(a), cy + radii[ring] * math.sin(a)
            tw = 11 + len(label) * 9.6
            d = durations[ring]
            sign = -1 if ring == 0 else 1
            chips[ring] += f"""
<g>
  <animateTransform attributeName="transform" type="rotate" from="0 {x:.1f} {y:.1f}" to="{-360*sign} {x:.1f} {y:.1f}" dur="{d}s" repeatCount="indefinite"/>
  <rect x="{x-tw/2-10:.1f}" y="{y-17:.1f}" width="{tw+20:.1f}" height="34" rx="17" fill="{BG2}" stroke="{color}" stroke-opacity=".7"/>
  <circle cx="{x-tw/2+4:.1f}" cy="{y:.1f}" r="4" fill="{color}"/>
  <text x="{x+6:.1f}" y="{y+5:.1f}" text-anchor="middle" font-family="{MONO}" font-size="15" fill="{FG}">{escape(label)}</text>
</g>"""
    groups = ""
    for ring in (0, 1):
        sign = -1 if ring == 0 else 1
        groups += f"""
<g>
  <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="{360*sign} {cx} {cy}" dur="{durations[ring]}s" repeatCount="indefinite"/>
  {chips[ring]}
</g>"""
    defs = f"""<radialGradient id="core"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".55"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>"""
    inner = f"""
<rect width="{w}" height="{h}" rx="18" fill="url(#grid)" opacity=".6"/>
<text x="40" y="54" font-family="{MONO}" font-size="15" fill="{MUTED}">// tech stack in orbit</text>
<text x="40" y="{h-34}" font-family="{MONO}" font-size="13" fill="{MUTED}">inner: frontend &amp; runtime   ·   outer: languages, data &amp; tools</text>
{rings}
<circle cx="{cx}" cy="{cy}" r="110" fill="url(#core)"/>
<circle cx="{cx}" cy="{cy}" r="54" fill="{BG2}" stroke="url(#brand)" stroke-width="2"/>
<text x="{cx}" y="{cy+11}" text-anchor="middle" font-family="{SANS}" font-size="32" font-weight="800" fill="url(#brand)">MH</text>
{groups}"""
    write("orbit.svg", frame(w, h, inner, defs))


# ---------------------------------------------------------------- footer ---
def footer():
    w, h = 1200, 200
    style = """.w1{animation:wave 8s linear infinite}.w2{animation:wave 12s linear infinite reverse}
    @keyframes wave{to{transform:translateX(-600px)}}"""

    def wave(y, amp):
        d = f"M0 {y}"
        for i in range(0, 2400, 150):
            d += f" Q{i+75} {y-amp} {i+150} {y} T{i+300} {y}" if i % 300 == 0 else ""
        return d + f" V{h} H0Z"

    defs = f'<clipPath id="card"><rect width="{w}" height="{h}" rx="18"/></clipPath>'
    inner = f"""
<g clip-path="url(#card)">
  <path class="w2" d="{wave(150, 18)}" fill="{PURPLE}" opacity=".18"/>
  <path class="w1" d="{wave(160, 14)}" fill="{BLUE}" opacity=".22"/>
</g>
<text x="{w/2}" y="84" text-anchor="middle" font-family="{SANS}" font-size="34" font-weight="800" fill="url(#brand)">Thanks for visiting!</text>
<text x="{w/2}" y="122" text-anchor="middle" font-family="{MONO}" font-size="17" fill="{MUTED}">Keep Coding &amp; Keep Growing  ·  github.com/{PROFILE['handle']}</text>"""
    write("footer.svg", frame(w, h, inner, defs, style))


if __name__ == "__main__":
    hero(); now(); neofetch(); orbit(); footer()
