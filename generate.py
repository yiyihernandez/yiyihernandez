"""Genera profile-card.svg con toda la estética Sakura integrada.
Local (opcional):  $env:GITHUB_TOKEN="tu_token"; python generate.py
Automatico: lo ejecuta el workflow .github/workflows/update.yml cada dia."""
import os, json, html, base64, random, textwrap, urllib.request

# ---------- CONFIGURACION ----------
USERNAME = os.environ.get("GITHUB_REPOSITORY_OWNER") or "yiyihernandez"  # tu usuario de GitHub
NAME     = "YIYI"                     # texto grande del titulo
SUBTITLE = "SOFTWARE DEVELOPER"
TAGLINE  = "construyendo cosas bonitas entre pétalos y código"
PINNED   = []                         # nombres de repos a mostrar. Vacio = los 3 con mas estrellas
# -----------------------------------
TOKEN = os.environ.get("GITHUB_TOKEN")
random.seed(7)

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
            for k, v in http(r["languages_url"]).items(): langs[k] = langs.get(k, 0) + v
        except Exception: pass
    try: commits = http(f"{api}/search/commits?q=author:{USERNAME}")["total_count"]
    except Exception: commits = None
    grid, total = None, None
    if TOKEN:
        try:
            q = "query($l:String!){user(login:$l){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount}}}}}}"
            cal = http(f"{api}/graphql", data=json.dumps({"query": q, "variables": {"l": USERNAME}}).encode())
            cal = cal["data"]["user"]["contributionsCollection"]["contributionCalendar"]
            total = cal["totalContributions"]
            grid = [[d["contributionCount"] for d in w["contributionDays"]] for w in cal["weeks"]][-40:]
        except Exception: pass
    cands = [r for r in own if r["name"].lower() != USERNAME.lower()]
    if PINNED: top = [r for n in PINNED for r in cands if r["name"] == n]
    else: top = sorted(cands, key=lambda r: (r["stargazers_count"], r["pushed_at"]), reverse=True)[:3]
    projects = []
    for r in top[:3]:
        try: img = base64.b64encode(http(f"https://opengraph.githubassets.com/1/{USERNAME}/{r['name']}", raw=True)).decode()
        except Exception: img = None
        projects.append(dict(name=r["name"], desc=r["description"] or "Sin descripción", lang=r["language"] or "—", stars=r["stargazers_count"], img=img, url=r["html_url"]))
    return dict(stars=sum(r["stargazers_count"] for r in own), forks=sum(r["forks_count"] for r in own),
                repos=user["public_repos"], commits=commits, langs=langs, grid=grid, total=total, projects=projects)

try: D = fetch()
except Exception as e:
    print("No pude leer GitHub (", e, ") -> uso datos de ejemplo")
    D = dict(stars=0, forks=0, repos=0, commits=None, grid=None, total=None,
             langs={"C++": 40, "Python": 25, "TypeScript": 15, "C": 10, "CSS": 6, "Shell": 4},
             projects=[dict(name=f"proyecto-{i}", desc="Descripción de ejemplo", lang="Python", stars=0, img=None, url="#") for i in (1, 2, 3)])

# lenguajes
tot = sum(D["langs"].values()) or 1
ranked = sorted(D["langs"].items(), key=lambda kv: -kv[1])
LANGS = [(k, round(100 * v / tot), c) for (k, v), c in zip(ranked[:7], ["#f06292", "#ffb7c5", "#b39ddb", "#9fa8da", "#f8bbd0", "#ce93d8", "#f48fb1"])]
rest = sum(v for _, v in ranked[7:])
if rest: LANGS.append(("Otros", round(100 * rest / tot), "#6d4c5e"))
CHIPS = [k for k, _ in ranked[:6]]
STATS = [(str(D["stars"]), "stars"), (str(D["forks"]), "forks"), (str(D["repos"]), "repos"), (f"{D['commits']:,}" if D["commits"] else "–", "commits")]
esc = lambda s: html.escape(str(s))

W, H = 860, 1380
F = "font-family=\"'Segoe UI',Helvetica,Arial,sans-serif\""
M = "font-family=\"'SFMono-Regular',Consolas,'Courier New',monospace\""
o = []; a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a('''<defs>
<radialGradient id="glow" cx="50%" cy="12%" r="60%"><stop offset="0" stop-color="#f06292" stop-opacity=".35"/><stop offset="1" stop-color="#140a14" stop-opacity="0"/></radialGradient>
<linearGradient id="title" x1="0" x2="1"><stop offset="0" stop-color="#ffd6e0"/><stop offset=".5" stop-color="#ffb7c5"/><stop offset="1" stop-color="#f06292"/></linearGradient>
<path id="petal" d="M0,0 C-7,-5 -8,-15 0,-20 C8,-15 7,-5 0,0Z"/>
</defs>''')
a(f'<rect width="{W}" height="{H}" rx="22" fill="#140a14"/><rect width="{W}" height="{H}" rx="22" fill="url(#glow)"/>')
a(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="#3a1f33"/>')

# rama grande superior
a('<g stroke="#5a3a44" fill="none" stroke-linecap="round"><path d="M870,15 C790,25 730,70 650,62 C610,58 585,72 560,90" stroke-width="7"/>'
  '<path d="M780,38 C770,90 790,140 770,205" stroke-width="4"/><path d="M730,62 C735,100 720,125 700,152" stroke-width="3.5"/>'
  '<path d="M655,62 C650,80 640,92 625,100" stroke-width="3"/></g>')
for x, y, r in [(850,24,15),(800,38,14),(745,64,16),(690,62,13),(640,62,15),(600,72,12),(566,88,14),(776,102,13),(786,152,14),(770,205,15),(728,102,12),(702,150,13),(626,100,11)]:
    a(f'<g transform="translate({x},{y}) rotate({random.randint(0,72)})" fill="#ffb7c5">' + ''.join(f'<use href="#petal" transform="rotate({k*72}) scale({r/10})"/>' for k in range(5)) + '<circle r="3" fill="#fff0f3"/></g>')

# titulo
a(f'<text x="{W/2}" y="85" text-anchor="middle" {F} font-size="64" font-weight="800" letter-spacing="14" fill="url(#title)">{esc(NAME)}</text>')
a(f'<text x="{W/2}" y="120" text-anchor="middle" {F} font-size="14" letter-spacing="7" fill="#b39ddb">{esc(SUBTITLE)}</text>')
a(f'<text x="{W/2}" y="148" text-anchor="middle" {F} font-size="13" font-style="italic" fill="#a8808f">{esc(TAGLINE)}</text>')

# SECCION: ABOUT ME (Dentro de la tarjeta)
a(f'<rect x="60" y="175" width="740" height="95" rx="12" fill="#1c0f1c" stroke="#5c2d4d"/>')
a(f'<text x="85" y="208" {F} font-size="13" font-weight="700" fill="#f06292">🌸 About Me</text>')
a(f'<text x="85" y="232" {F} font-size="13" fill="#e8cfd8">Estudiante de Ingeniería de Sistemas enfocada en desarrollo de software, diseño</text>')
a(f'<text x="85" y="252" {F} font-size="13" fill="#e8cfd8">de interfaces y experiencias web interactivas. Amante del código limpio y los detalles visuales.</text>')

# chips de lenguajes / tech stack rapido
tw = [len(c) * 8 + 24 for c in CHIPS]; start_x = (W - (sum(tw) + 8 * (len(tw) - 1))) / 2
for c, w in zip(CHIPS, tw):
    a(f'<rect x="{start_x}" y="290" width="{w}" height="24" rx="12" fill="#241324" stroke="#5c2d4d"/><text x="{start_x+w/2}" y="306" text-anchor="middle" {M} font-size="11" fill="#ffd6e0">{esc(c)}</text>'); start_x += w + 8

# stats
a('<line x1="80" y1="340" x2="780" y2="340" stroke="#3a1f33"/>')
for i, (n, l) in enumerate(STATS):
    cx = 140 + i * 193
    a(f'<text x="{cx}" y="385" text-anchor="middle" {F} font-size="34" font-weight="800" fill="#ffb7c5">{n}</text><text x="{cx}" y="405" text-anchor="middle" {F} font-size="12" fill="#a8808f">{l}</text>')
a('<line x1="80" y1="425" x2="780" y2="425" stroke="#3a1f33"/>')

# lenguajes barra
a(f'<text x="60" y="465" {F} font-size="13" font-weight="700" letter-spacing="3" fill="#f06292">Lenguajes</text>')
x = 60; s = sum(p for _, p, _ in LANGS) or 1
a('<clipPath id="bar"><rect x="60" y="480" width="740" height="10" rx="5"/></clipPath><g clip-path="url(#bar)">')
for n, p, c in LANGS:
    w = 740 * p / s; a(f'<rect x="{x:.1f}" y="480" width="{w:.1f}" height="10" fill="{c}"/>'); x += w
a('</g>')
for i, (n, p, c) in enumerate(LANGS):
    cx = 60 + (i % 4) * 190; cy = 520 + (i // 4) * 26
    a(f'<circle cx="{cx+5}" cy="{cy-4}" r="4" fill="{c}"/><text x="{cx+15}" y="{cy}" {F} font-size="12" fill="#e8cfd8">{esc(n[:14])} <tspan fill="#8a6676">{p}%</tspan></text>')

# actividad
a(f'<text x="60" y="595" {F} font-size="13" font-weight="700" letter-spacing="3" fill="#f06292">Actividad</text>')
if D["total"] is not None: a(f'<text x="800" y="595" text-anchor="end" {F} font-size="12" fill="#a8808f">{D["total"]} contribuciones</text>')
cols = ["#241324", "#5c2d4d", "#a8456f", "#f06292", "#ffb7c5", "#fff0f3"]
lvl = lambda n: 0 if n == 0 else 1 if n < 3 else 2 if n < 6 else 3 if n < 10 else 4 if n < 15 else 5
for ci in range(40):
    for r in range(7):
        if D["grid"]:
            wk = D["grid"][ci] if ci < len(D["grid"]) else []
            v = lvl(wk[r]) if r < len(wk) else None
        else: v = random.choices(range(6), [38, 22, 16, 12, 8, 4])[0]
        if v is not None: a(f'<rect x="{60+ci*18.5:.1f}" y="{610+r*17}" width="13" height="13" rx="3" fill="{cols[v]}"/>')

# proyectos con enlaces interactivos
a(f'<text x="60" y="765" {F} font-size="13" font-weight="700" letter-spacing="3" fill="#f06292">Proyectos destacados</text>')
for i, p in enumerate(D["projects"]):
    x, y = 60 + i * 250, 785
    a(f'<a href="{esc(p["url"])}" target="_blank">')
    a(f'<g style="cursor: pointer;">')
    a(f'<rect x="{x}" y="{y}" width="240" height="200" rx="12" fill="#1c0f1c" stroke="#5c2d4d"/>')
    a(f'<clipPath id="c{i}"><path d="M{x},{y+110} V{y+12} a12,12 0 0 1 12,-12 H{x+228} a12,12 0 0 1 12,12 V{y+110} Z"/></clipPath>')
    if p["img"]: a(f'<image href="data:image/png;base64,{p["img"]}" x="{x}" y="{y}" width="240" height="110" preserveAspectRatio="xMidYMid slice" clip-path="url(#c{i})"/>')
    else: a(f'<rect x="{x}" y="{y}" width="240" height="110" fill="#2a1428" clip-path="url(#c{i})"/><text x="{x+120}" y="{y+68}" text-anchor="middle" {F} font-size="40" fill="#5c2d4d">{esc(p["name"][:1].upper())}</text>')
    a(f'<line x1="{x}" y1="{y+110}" x2="{x+240}" y2="{y+110}" stroke="#5c2d4d"/>')
    a(f'<text x="{x+14}" y="{y+136}" {F} font-size="15" font-weight="700" fill="#ffd6e0">{esc(textwrap.shorten(p["name"], 22, placeholder="…"))}</text>')
    a(f'<text x="{x+14}" y="{y+156}" {F} font-size="11" fill="#a8808f">{esc(textwrap.shorten(p["desc"], 36, placeholder="…"))}</text>')
    a(f'<circle cx="{x+18}" cy="{y+180}" r="4" fill="#f06292"/><text x="{x+28}" y="{y+184}" {M} font-size="11" fill="#e8cfd8">{esc(p["lang"])}</text><text x="{x+226}" y="{y+184}" text-anchor="end" {M} font-size="11" fill="#ffb7c5">★ {p["stars"]}</text>')
    a(f'</g>')
    a(f'</a>')

# petalos animados cayendo
for i in range(18):
    x = random.randint(30, 830); d = random.uniform(11, 20); sc = random.uniform(.5, 1); dx = random.randint(-60, 60)
    a(f'<g opacity="{random.uniform(.35,.8):.2f}" fill="#ffb7c5"><use href="#petal" transform="scale({sc:.2f})"><animateTransform attributeName="transform" type="rotate" values="0;360" dur="{d/2:.1f}s" repeatCount="indefinite" additive="sum"/></use>'
      f'<animateMotion path="M{x},-30 C{x+dx},{H*.3:.0f} {x-dx},{H*.65:.0f} {x+dx//2},{H+30}" dur="{d:.1f}s" begin="-{random.uniform(0,d):.1f}s" repeatCount="indefinite"/></g>')
a('</svg>')
open("profile-card.svg", "w", encoding="utf-8").write("\n".join(o))
print("Listo: profile-card.svg con toda la estética integrada.")