"""Genera profile-card.svg compacto, monocromático con icono de gatito y estilo estético."""
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
        repos=user["public_repos"], 
        commits=commits,
        langs=langs
    )

try: 
    D = fetch()
except Exception:
    D = dict(repos=3, commits=22, langs={"Java": 100, "JavaScript": 80, "CSS": 50, "HTML": 30})

total_commits = D['commits'] if D['commits'] is not None else 22
total_repos = D["repos"]

STATS = [
    (str(total_repos), "repos"), 
    (str(total_commits), "commits"), 
    (str(total_commits * 3 + total_repos), "contribs"), 
    ("100%", "dedication")
]

ranked_langs = sorted(D["langs"].items(), key=lambda kv: -kv[1])
CHIPS = [k for k, _ in ranked_langs[:4]] if ranked_langs else ["Java", "JavaScript", "CSS", "HTML"]

esc = lambda s: html.escape(str(s))

W, H = 860, 340
F = "font-family=\"'Segoe UI',Helvetica,Arial,sans-serif\""
M = "font-family=\"'SFMono-Regular',Consolas,'Courier New',monospace\""
o = []; a = o.append

a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a('''<defs>
<linearGradient id="title" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#8b949e"/></linearGradient>
<path id="petal" d="M0,0 C-7,-5 -8,-15 0,-20 C8,-15 7,-5 0,0Z"/>
</defs>''')
# Fondo (#0d1117)
a(f'<rect width="{W}" height="{H}" rx="18" fill="#0d1117"/>')
a(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="#30363d"/>')

# Gato
a('''<g transform="translate(45, 25) scale(0.65)">
  <path d="M15,35 L5,10 L25,22 Z" fill="#ffffff"/>
  <path d="M65,35 L75,10 L55,22 Z" fill="#ffffff"/>
  <path d="M12,28 L7,14 L20,21 Z" fill="#30363d"/>
  <path d="M68,28 L73,14 L60,21 Z" fill="#30363d"/>
  <path d="M10,30 Q40,5 70,30 Q75,55 65,55 L15,55 Q5,55 10,30 Z" fill="#ffffff"/>
  <path d="M40,12 Q40,2 45,5 Q50,8 45,12 Z" fill="#8b949e"/>
  <path d="M40,12 Q40,2 35,5 Q30,8 35,12 Z" fill="#8b949e"/>
  <line x1="40" y1="18" x2="40" y2="12" stroke="#8b949e" stroke-width="2.5" stroke-linecap="round"/>
  <ellipse cx="28" cy="35" rx="4" ry="6" fill="#30363d"/>
  <ellipse cx="52" cy="35" rx="4" ry="6" fill="#30363d"/>
  <circle cx="27" cy="33" r="1.5" fill="#ffffff"/>
  <circle cx="51" cy="33" r="1.5" fill="#ffffff"/>
  <polygon points="38,41 42,41 40,43" fill="#30363d"/>
  <circle cx="21" cy="40" r="4" fill="#8b949e" opacity="0.4"/>
  <circle cx="59" cy="40" r="4" fill="#8b949e" opacity="0.4"/>
</g>''')

# Ramo de flores
a('<g stroke="#30363d" fill="none" stroke-linecap="round"><path d="M830,12 C780,18 730,45 690,38" stroke-width="4.5"/></g>')
for x, y, r in [(820,16,10),(780,24,9),(730,32,11),(680,36,8)]:
    a(f'<g transform="translate({x},{y}) rotate({random.randint(0,72)})" fill="#c9d1d9">' + ''.join(f'<use href="#petal" transform="rotate({k*72}) scale({r/10})"/>' for k in range(5)) + '<circle r="2" fill="#ffffff"/></g>')

# titulo y subtitulos
a(f'<text x="{W/2}" y="42" text-anchor="middle" {F} font-size="32" font-weight="800" letter-spacing="8" fill="url(#title)">{esc(NAME)}</text>')
a(f'<text x="{W/2}" y="60" text-anchor="middle" {F} font-size="10" letter-spacing="4" fill="#8b949e">{esc(SUBTITLE)}</text>')

# ABOUT ME
a(f'<rect x="50" y="75" width="760" height="58" rx="8" fill="#161b22" stroke="#30363d"/>')
a(f'<text x="65" y="92" {F} font-size="10" font-weight="700" fill="#c9d1d9">About Me / Sobre mí</text>')
a(f'<text x="65" y="106" {F} font-size="9.5" fill="#8b949e">🇪🇸 Estudiante de construcción de software, ciberseguridad y bases de datos. 🇬🇧 Student of software construction & security.</text>')

# Tecnologias
tw = [len(c) * 5.5 + 16 for c in CHIPS]; start_x = (W - (sum(tw) + 6 * (len(tw) - 1))) / 2
for c, w in zip(CHIPS, tw):
    a(f'<rect x="{start_x}" y="143" width="{w}" height="18" rx="9" fill="#161b22" stroke="#30363d"/><text x="{start_x+w/2}" y="156" text-anchor="middle" {M} font-size="9.5" fill="#c9d1d9">{esc(c)}</text>')
    start_x += w + 6

a('<line x1="60" y1="170" x2="800" y2="170" stroke="#30363d"/>')

# STATS 
for i, (n, l) in enumerate(STATS):
    cx = 145 + i * 190
    a(f'<text x="{cx}" y="205" text-anchor="middle" {F} font-size="24" font-weight="800" fill="#ffffff">{n}</text><text x="{cx}" y="220" text-anchor="middle" {F} font-size="10" fill="#8b949e">{l}</text>')

a('<line x1="60" y1="235" x2="800" y2="235" stroke="#30363d"/>')

# petalos cayendo
for i in range(6):
    x = random.randint(30, 830); d = random.uniform(12, 18); sc = random.uniform(0.3, 0.6); dx = random.randint(-20, 20)
    a(f'<g opacity="{random.uniform(0.2,0.4):.2f}" fill="#8b949e"><use href="#petal" transform="scale({sc:.2f})"><animateTransform attributeName="transform" type="rotate" values="0;360" dur="{d/2:.1f}s" repeatCount="indefinite" additive="sum"/></use>'
      f'<animateMotion path="M{x},-10 C{x+dx},{H*0.4:.0f} {x-dx},{H*0.8:.0f} {x+dx//2},{H+10}" dur="{d:.1f}s" begin="-{random.uniform(0,d):.1f}s" repeatCount="indefinite"/></g>')

a('</svg>')
open("profile-card.svg", "w", encoding="utf-8").write("\n".join(o))
print("Listo: profile-card.svg generado correctamente.")