"""
neofetch style "About Me" card with an ASCII portrait -> assets/neofetch-card.svg

    GITHUB_TOKEN=... python assets/neofetch.py

Edit INFO / CONTACT below to change the text. The GitHub Stats block and the
Uptime line (age of the GitHub account) are fetched live; the stats workflow
re-runs this daily. The portrait comes from assets/avatar-ascii.json (ascii.py).
"""
import json
import os
import urllib.request
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
USER = os.environ.get("GH_USER", "mahedi0x")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

INFO = [
    [("OS", "macOS, Linux"),
     ("Uptime", "{uptime}"),
     ("Role", "Full Stack JavaScript Developer"),
     ("Host", "Cerrow, Sylhet, Bangladesh"),
     ("Kernel", "Node.js (JavaScript runtime)"),
     ("IDE", "VS Code")],
    [("Languages.Programming", "JavaScript, Python, PHP"),
     ("Languages.Computer", "HTML, CSS, SQL, JSON"),
     ("Languages.Real", "Bangla, English")],
    [("Stack.Frontend", "React, Next.js, Tailwind CSS"),
     ("Stack.Backend", "Node.js, Express"),
     ("Stack.Database", "MongoDB, Firebase, MySQL"),
     ("Stack.Learning", "Machine Learning, Web Security")],
]
CONTACT = [
    ("Email", "mahedi.swe04@gmail.com"),
    ("LinkedIn", "mahedi0x"),
    ("GitHub", "mahedi0x"),
    ("Facebook", "mahdihasan.sun"),
]

BG, BORDER, FG, KEY, DOTS = "#0B0F1A", "#1F2A44", "#C0CAF5", "#7AA2F7", "#2A3352"
GREEN, PURPLE, ORANGE, MUTED = "#9ECE6A", "#BB9AF7", "#FF9E64", "#565F89"
MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"


def api(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return json.load(r)


def uptime(created):
    a, b = datetime.fromisoformat(created.replace("Z", "+00:00")).date(), date.today()
    months = (b.year - a.year) * 12 + b.month - a.month - (b.day < a.day)
    anchor_m = a.month + months
    anchor = date(a.year + (anchor_m - 1) // 12, (anchor_m - 1) % 12 + 1, min(a.day, 28))
    days = (b - anchor).days
    y, m = divmod(months, 12)
    return f"{y} years, {m} months, {days} days"


def github():
    try:
        u = api(f"https://api.github.com/users/{USER}")
        repos, page = [], 1
        while True:
            batch = api(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}&type=owner")
            repos += batch
            if len(batch) < 100:
                break
            page += 1
        own = [r for r in repos if not r["fork"]]
        langs = Counter(r["language"] for r in own if r["language"]).most_common(3)
        return {
            "uptime": uptime(u["created_at"]),
            "repos": f"{u['public_repos']} {{Stars: {sum(r['stargazers_count'] for r in own)}}}",
            "community": f"Followers: {u['followers']} | Following: {u['following']}",
            "langs": ", ".join(f"{k} {v}" for k, v in langs) or "—",
        }
    except Exception as e:
        print("could not reach GitHub:", e)
        return None


def render(gh):
    W = 1200
    art = json.loads((HERE / "avatar-ascii.json").read_text())
    rows, cols = art["rows"], art["cols"]
    fs, lh = 6.9, 6.7
    art_w = 500
    # Every run of characters is placed at its own x position, so browsers that
    # collapse whitespace (GitHub's image view does) cannot squash the portrait.
    cw = art_w / cols
    art_cells = []  # (row, x, color, text)
    for i, runs in enumerate(rows):
        col = 0
        for c, t in runs:
            if c and t.strip():
                lead = len(t) - len(t.lstrip(" "))
                body = t.strip(" ")
                art_cells.append((i, 34 + (col + lead) * cw, c, body))
            col += len(t)
    x0, x1, y = 560, 1160, 58
    out = [f'<text x="{x0}" y="{y}" fill="{GREEN}" font-weight="700">{USER}@github</text>',
           f'<line x1="{x0 + 150}" y1="{y - 5}" x2="{x1}" y2="{y - 5}" stroke="{DOTS}" stroke-dasharray="4 5"/>']
    y += 34
    stats = gh or {"uptime": "—", "repos": "—", "community": "—", "langs": "—"}

    def row(k, v, color=FG):
        nonlocal y
        out.append(f'<text x="{x0}" y="{y}" fill="{MUTED}">.</text>')
        out.append(f'<text x="{x0 + 18}" y="{y}" fill="{KEY}">{escape(k)}:</text>')
        kw = 18 + (len(k) + 2) * 9.0
        vw = len(v) * 9.0
        out.append(f'<line x1="{x0 + kw:.0f}" y1="{y - 4}" x2="{x1 - vw - 10:.0f}" y2="{y - 4}" '
                   f'stroke="{DOTS}" stroke-dasharray="1 5" stroke-linecap="round"/>')
        out.append(f'<text x="{x1}" y="{y}" fill="{color}" text-anchor="end">{escape(v)}</text>')
        y += 24

    def header(title):
        nonlocal y
        y += 6
        out.append(f'<text x="{x0}" y="{y}" fill="{MUTED}">-</text>')
        out.append(f'<text x="{x0 + 18}" y="{y}" fill="{FG}" font-weight="700">{title}</text>')
        out.append(f'<line x1="{x0 + 30 + len(title) * 9.5:.0f}" y1="{y - 5}" x2="{x1}" y2="{y - 5}" '
                   f'stroke="{DOTS}" stroke-dasharray="4 5"/>')
        y += 24

    for gi, group in enumerate(INFO):
        if gi:
            y += 10
        for k, v in group:
            row(k, v.format(uptime=stats["uptime"]))
    header("Contact")
    for k, v in CONTACT:
        row(k, v, PURPLE)
    header("GitHub Stats")
    row("Repos", stats["repos"], GREEN)
    row("Community", stats["community"], GREEN)
    row("Top Languages", stats["langs"], ORANGE)
    out.append(f'<text x="{x0}" y="{y + 4}" fill="{GREEN}">$</text>'
               f'<rect class="cur" x="{x0 + 16}" y="{y - 10}" width="9" height="17" fill="{FG}"/>')

    H = int(max(y + 40, len(rows) * lh + 60))
    oy = (H - len(rows) * lh) / 2 + 6
    art_svg = [
        f'<text x="{x:.1f}" y="{oy + i * lh:.1f}" fill="{c}" textLength="{len(t) * cw:.1f}" '
        f'lengthAdjust="spacingAndGlyphs">{escape(t)}</text>'
        for i, x, c, t in art_cells]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xml:space="preserve">
<style>
.art text{{font-family:{MONO};font-size:{fs}px}}
.info text{{font-family:{MONO};font-size:15px;white-space:pre}}
.art{{animation:fade 1.6s ease-out both}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
.cur{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="{BG}" stroke="{BORDER}"/>
<g class="art">{''.join(art_svg)}</g>
<g class="info">{''.join(out)}</g>
</svg>
"""


if __name__ == "__main__":
    gh = github()
    target = HERE / "neofetch-card.svg"
    if gh is None and target.exists() and "@github" in target.read_text() and "textLength" in target.read_text():
        raise SystemExit(0)  # keep the last good card
    target.write_text(render(gh), encoding="utf-8")
    print("wrote", target.name)
