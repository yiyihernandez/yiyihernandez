import os, json, base64, random, textwrap, urllib.request, html

USERNAME = os.environ.get("GITHUB_REPOSITORY_OWNER") or "yiyihernandez"
NAME     = "YIYI"
SUBTITLE = "SOFTWARE & CREATIVITY"
TAGLINE  = ""

TOKEN = os.environ.get("GITHUB_TOKEN")
random.seed(42)

def http(url, data=None, accept=None, raw=False):
    h = {"User-Agent": "sakura-profile"}
    if TOKEN and "api.github.com" in url: h["Authorization"] = f"Bearer {TOKEN}"
    if accept: h["Accept"] = accept
    if data: h["Content-Type"] = "application/json"
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h), timeout=30) as r:
        b = r.read()
    return b if raw else json.loads(b)

def fetch():
    api = "https://api.github.com"
    user = http(f"{api}/users/{USERNAME}")
    repos, page = [], 1
    while True:
        r = http(f"{api}/users/{USERNAME}/repos?per_page=100&type=owner&page={page}")
        repos += r
        if len(r) < 100: break
        page += 1
    own = [r for r in repos if not r["fork"]]
    
    langs = {}
    for r in own:
        try:
            for k, v in http(r["languages_url"]).items():
                langs[k] = langs.get(k, 0) + v
        except Exception:
            pass

    try: 
        commits = http(f"{api}/search/commits?q=author:{USERNAME}")["total_count"]
    except Exception: 
        commits = None

    return dict(
        stars=sum(r["stargazers_count"] for r in own), 
        forks=sum(r["forks_count"] for r in own),
        repos=user["public_repos"], 
        commits=commits,
        langs=langs
    )

try: 
    D = fetch()
except Exception:
    D = dict(stars=0, forks=0, repos=3, commits=22, langs={"Java": 100, "JavaScript": 80, "CSS": 50, "Python": 40})

STATS = [(str(D["stars"]), "stars"), (str(D["forks"]), "forks"), (str(D["repos"]), "repos"), (str(D['commits']) if D['commits'] is not None else "22", "commits")]

ranked_langs = sorted(D["langs"].items(), key=lambda kv: -kv[1])
CHIPS = [k for k, _ in ranked_langs[:4]] if ranked_langs else ["Java", "JavaScript", "CSS", "Python"]

esc = lambda s: html.escape(str(s))

# Altura
W, H = 860, 370
F = "font-family=\"'Segoe UI',Helvetica,Arial,sans-serif\""
M = "font-family=\"'SFMono-Regular',Consolas,'Courier New',monospace\""
o = []; a = o.append

a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a('''<defs>
<linearGradient id="title" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#8b949e"/></linearGradient>
<path id="petal" d="M0,0 C-7,-5 -8,-15 0,-20 C8,-15 7,-5 0,0Z"/>
</defs>''')
# Fondo(#0d1117)
a(f'<rect width="{W}" height="{H}" rx="18" fill="#0d1117"/>')
a(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="#30363d"/>')

# Ramo de flores
a('<g stroke="#30363d" fill="none" stroke-linecap="round"><path d="M870,12 C790,18 730,55 650,45 C610,40 585,55 560,75" stroke-width="5.5"/>'
  '<path d="M780,30 C770,75 790,115 770,155" stroke-width="3"/><path d="M730,48 C735,75 720,95 700,112" stroke-width="2.5"/></g>')
for x, y, r in [(850,18,13),(800,30,12),(745,52,14),(690,48,11),(640,48,13),(600,58,10),(566,72,12),(776,85,11),(770,145,12),(728,85,10),(626,75,9)]:
    a(f'<g transform="translate({x},{y}) rotate({random.randint(0,72)})" fill="#c9d1d9">' + ''.join(f'<use href="#petal" transform="rotate({k*72}) scale({r/10})"/>' for k in range(5)) + '<circle r="2.5" fill="#ffffff"/></g>')

# Titulo y subtitulos
a(f'<text x="{W/2}" y="85" text-anchor="middle" {F} font-size="52" font-weight="800" letter-spacing="12" fill="url(#title)">{esc(NAME)}</text>')
a(f'<text x="{W/2}" y="118" text-anchor="middle" {F} font-size="13" letter-spacing="6" fill="#8b949e">{esc(SUBTITLE)}</text>')

#ABOUT ME
a(f'<rect x="60" y="155" width="740" height="75" rx="10" fill="#161b22" stroke="#30363d"/>')
a(f'<text x="85" y="182" {F} font-size="12" font-weight="700" fill="#c9d1d9">About me</text>')
a(f'<text x="85" y="202" {F} font-size="12" fill="#8b949e">Student of software construction, cybersecurity, and databases.</text>')
a(f'<text x="85" y="218" {F} font-size="12" fill="#8b949e">I love learning every day, paying attention to visual details and creating unique experiences for users.</text>')

# Tecnologias
tw = [len(c) * 7 + 22 for c in CHIPS]; start_x = (W - (sum(tw) + 8 * (len(tw) - 1))) / 2
for c, w in zip(CHIPS, tw):
    a(f'<rect x="{start_x}" y="248" width="{w}" height="22" rx="11" fill="#161b22" stroke="#30363d"/><text x="{start_x+w/2}" y="263" text-anchor="middle" {M} font-size="11" fill="#c9d1d9">{esc(c)}</text>')
    start_x += w + 8

a('<line x1="80" y1="290" x2="780" y2="290" stroke="#30363d"/>')

# STATS
for i, (n, l) in enumerate(STATS):
    cx = 140 + i * 193
    a(f'<text x="{cx}" y="332" text-anchor="middle" {F} font-size="28" font-weight="800" fill="#ffffff">{n}</text><text x="{cx}" y="350" text-anchor="middle" {F} font-size="11.5" fill="#8b949e">{l}</text>')

# petalos cayendo animados
for i in range(7):
    x = random.randint(40, 820); d = random.uniform(12, 18); sc = random.uniform(.35, .65); dx = random.randint(-25, 25)
    a(f'<g opacity="{random.uniform(.25,.45):.2f}" fill="#8b949e"><use href="#petal" transform="scale({sc:.2f})"><animateTransform attributeName="transform" type="rotate" values="0;360" dur="{d/2:.1f}s" repeatCount="indefinite" additive="sum"/></use>'
      f'<animateMotion path="M{x},-20 C{x+dx},{H*.3:.0f} {x-dx},{H*.7:.0f} {x+dx//2},{H+10}" dur="{d:.1f}s" begin="-{random.uniform(0,d):.1f}s" repeatCount="indefinite"/></g>')

a('</svg>')
open("profile-card.svg", "w", encoding="utf-8").write("\n".join(o))
print("Listo: profile-card.svg hecho.")