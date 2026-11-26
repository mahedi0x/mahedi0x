"""
Self-hosted GitHub stats card for mahedi0x -> assets/stats-card.svg

    GITHUB_TOKEN=... python assets/stats.py

The token is optional for public data but needed for contribution counts.
The workflow .github/workflows/stats.yml runs this every day automatically,
so the card never breaks the way the free Vercel-hosted cards often do.
"""
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

USER = os.environ.get("GH_USER", "mahedi0x")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = Path(__file__).resolve().parent / "stats-card.svg"

BG, BG2, LINE, FG, MUTED = "#0B0F1A", "#111729", "#1F2A44", "#C0CAF5", "#7A84A8"
BLUE, CYAN, GREEN, PURPLE, ORANGE = "#7AA2F7", "#7DCFFF", "#9ECE6A", "#BB9AF7", "#FF9E64"
MONO = "'JetBrains Mono','Fira Code',Consolas,'Liberation Mono',Menlo,monospace"
SANS = "'Segoe UI','Inter',-apple-system,Helvetica,Arial,sans-serif"
LANG_COLORS = {
    "JavaScript": "#F1E05A", "TypeScript": "#3178C6", "HTML": "#E34C26", "CSS": "#663399",
    "Python": "#3572A5", "PHP": "#4F5D95", "C++": "#F34B7D", "C": "#555555", "Java": "#B07219",
    "SCSS": "#C6538C", "Vue": "#41B883", "Shell": "#89E051", "EJS": "#A91E50",
}


def api(url, data=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers,
                                 data=json.dumps(data).encode() if data else None)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    user = api(f"https://api.github.com/users/{USER}")
    repos, page = [], 1
    while True:
        batch = api(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}&type=owner")
        repos += batch
        if len(batch) < 100:
            break
        page += 1
    own = [r for r in repos if not r["fork"]]
    langs = {}
    for r in own:
        for k, v in api(r["languages_url"]).items():
            langs[k] = langs.get(k, 0) + v
    stats = {
        "repos": user["public_repos"],
        "followers": user["followers"],
        "stars": sum(r["stargazers_count"] for r in own),
        "forks": sum(r["forks_count"] for r in own),
        "langs": sorted(langs.items(), key=lambda kv: -kv[1])[:6],
        "contrib": None, "commits": None, "prs": None,
    }
    if TOKEN:
        q = """query($u:String!){user(login:$u){contributionsCollection{
              totalCommitContributions restrictedContributionsCount totalPullRequestContributions
              contributionCalendar{totalContributions}}}}"""
        c = api("https://api.github.com/graphql", {"query": q, "variables": {"u": USER}})
        cc = c["data"]["user"]["contributionsCollection"]
        stats["contrib"] = cc["contributionCalendar"]["totalContributions"]
        stats["commits"] = cc["totalCommitContributions"] + cc["restrictedContributionsCount"]
        stats["prs"] = cc["totalPullRequestContributions"]
    return stats


def fmt(n):
    if n is None:
        return "—"
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)


def render(s):
    w, h = 1200, 330
    tiles = [
        ("Contributions (1y)", s["contrib"], GREEN), ("Commits (1y)", s["commits"], BLUE),
        ("Pull requests (1y)", s["prs"], PURPLE), ("Public repos", s["repos"], CYAN),
        ("Stars earned", s["stars"], ORANGE), ("Followers", s["followers"], FG),
    ]
    tile_svg = ""
    for i, (label, val, color) in enumerate(tiles):
        x, y = 40 + (i % 3) * 190, 84 + (i // 3) * 112
        tile_svg += f"""
<g class="t" style="animation-delay:{i*0.12:.2f}s">
  <rect x="{x}" y="{y}" width="176" height="98" rx="12" fill="{BG2}" stroke="{LINE}"/>
  <text x="{x+18}" y="{y+52}" font-family="{SANS}" font-size="34" font-weight="800" fill="{color}">{fmt(val)}</text>
  <text x="{x+18}" y="{y+78}" font-family="{MONO}" font-size="13" fill="{MUTED}">{label}</text>
</g>"""
    total = sum(v for _, v in s["langs"]) or 1
    bx, bw = 650, 510
    bar, legend, off = "", "", 0.0
    for i, (name, v) in enumerate(s["langs"]):
        pct = v / total
        color = LANG_COLORS.get(name, "#8B949E")
        bar += f'<rect x="{bx+off*bw:.1f}" y="96" width="{max(pct*bw,2):.1f}" height="12" fill="{color}"/>'
        off += pct
        lx, ly = bx + (i % 2) * 260, 146 + (i // 2) * 34
        legend += (f'<circle cx="{lx+6}" cy="{ly-5}" r="6" fill="{color}"/>'
                   f'<text x="{lx+20}" y="{ly}" font-family="{MONO}" font-size="15" fill="{FG}">{escape(name)}'
                   f'<tspan fill="{MUTED}"> {pct*100:.1f}%</tspan></text>')
    if not s["langs"]:
        legend = f'<text x="{bx}" y="150" font-family="{MONO}" font-size="15" fill="{MUTED}">run stats.py to fill this in</text>'
    stamp = datetime.now(timezone.utc).strftime("%d %b %Y")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xml:space="preserve">
<defs><clipPath id="bar"><rect x="{bx}" y="96" width="{bw}" height="12" rx="6"/></clipPath></defs>
<style>.t{{opacity:0;animation:up .6s ease-out forwards}}@keyframes up{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}</style>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="{BG}" stroke="{LINE}"/>
<text x="40" y="54" font-family="{MONO}" font-size="16"><tspan fill="{GREEN}">$</tspan><tspan fill="{FG}"> gh stats {USER}</tspan></text>
<text x="{w-40}" y="54" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">updated {stamp}</text>
{tile_svg}
<text x="{bx}" y="80" font-family="{MONO}" font-size="14" fill="{MUTED}">most used languages</text>
<rect x="{bx}" y="96" width="{bw}" height="12" rx="6" fill="{LINE}"/>
<g clip-path="url(#bar)">{bar}</g>
{legend}
</svg>
"""


if __name__ == "__main__":
    try:
        data = collect()
    except Exception as e:  # keep the old card rather than failing the README
        print("could not reach GitHub:", e)
        data = {"repos": None, "followers": None, "stars": None, "forks": None,
                "langs": [], "contrib": None, "commits": None, "prs": None}
        if OUT.exists():
            raise SystemExit(0)
    OUT.write_text(render(data), encoding="utf-8")
    print("wrote", OUT.name)
