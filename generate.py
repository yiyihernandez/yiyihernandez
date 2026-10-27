# Edita los datos y ejecuta: python generate.py  -> crea profile-card.svg
import random
random.seed(7)

NAME      = "SAKURA"            # tu nombre/alias
SUBTITLE  = "SOFTWARE DEVELOPER"
TAGLINE   = "construyendo cosas bonitas entre pétalos y código"
STATS     = [("41","stars"),("4","forks"),("62","repos"),("966","commits")]
CHIPS     = ["C","C++","Python","JavaScript","Rust","TypeScript"]
LANGS     = [("C++",34,"#f06292"),("C",18,"#ffb7c5"),("TypeScript",14,"#b39ddb"),
             ("Python",12,"#9fa8da"),("CSS",8,"#f8bbd0"),("Shell",8,"#ce93d8"),("Otros",6,"#6d4c5e")]
PROJECTS  = [("Proyecto Uno","Descripción corta de tu proyecto","C++"),
             ("Proyecto Dos","Descripción corta de tu proyecto","Python"),
             ("Proyecto Tres","Descripción corta de tu proyecto","Rust")]
CONTRIB   = "876 contribuciones"

W,H = 860,1000
F  = "font-family=\"'Segoe UI',Helvetica,Arial,sans-serif\""
M  = "font-family=\"'SFMono-Regular',Consolas,'Courier New',monospace\""
o=[]
a=o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a('''<defs>
<radialGradient id="glow" cx="50%" cy="22%" r="60%"><stop offset="0" stop-color="#f06292" stop-opacity=".35"/><stop offset="1" stop-color="#140a14" stop-opacity="0"/></radialGradient>
<linearGradient id="title" x1="0" x2="1"><stop offset="0" stop-color="#ffd6e0"/><stop offset=".5" stop-color="#ffb7c5"/><stop offset="1" stop-color="#f06292"/></linearGradient>
<path id="petal" d="M0,0 C-7,-5 -8,-15 0,-20 C8,-15 7,-5 0,0Z"/>
</defs>''')
a(f'<rect width="{W}" height="{H}" rx="22" fill="#140a14"/><rect width="{W}" height="{H}" rx="22" fill="url(#glow)"/>')
a(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="#3a1f33"/>')
# rama de cerezo (esquina superior derecha)
a('<g stroke="#5a3a44" stroke-width="5" fill="none" stroke-linecap="round"><path d="M860,40 C760,60 700,50 630,95"/><path d="M730,58 C720,90 700,105 680,130" stroke-width="3"/></g>')
for x,y,r in [(640,92,9),(682,128,8),(735,60,10),(780,52,8),(700,70,7),(825,44,9)]:
    a(f'<g transform="translate({x},{y})" fill="#ffb7c5">'+''.join(f'<use href="#petal" transform="rotate({k*72}) scale({r/10})"/>' for k in range(5))+'<circle r="2.5" fill="#fff0f3"/></g>')
# título
a(f'<text x="{W/2}" y="165" text-anchor="middle" {F} font-size="76" font-weight="800" letter-spacing="18" fill="url(#title)">{NAME}</text>')
a(f'<text x="{W/2}" y="205" text-anchor="middle" {F} font-size="15" letter-spacing="9" fill="#b39ddb">{SUBTITLE}</text>')
a(f'<text x="{W/2}" y="238" text-anchor="middle" {F} font-size="14" font-style="italic" fill="#a8808f">{TAGLINE}</text>')
# chips
tw=[len(c)*9+30 for c in CHIPS]; x=(W-(sum(tw)+10*(len(tw)-1)))/2
for c,w in zip(CHIPS,tw):
    a(f'<rect x="{x}" y="270" width="{w}" height="28" rx="14" fill="#241324" stroke="#5c2d4d"/><text x="{x+w/2}" y="289" text-anchor="middle" {M} font-size="12" fill="#ffd6e0">{c}</text>'); x+=w+10
# stats
a('<line x1="80" y1="345" x2="780" y2="345" stroke="#3a1f33"/>')
for i,(n,l) in enumerate(STATS):
    cx=140+i*193
    a(f'<text x="{cx}" y="400" text-anchor="middle" {F} font-size="38" font-weight="800" fill="#ffb7c5">{n}</text><text x="{cx}" y="424" text-anchor="middle" {F} font-size="12" fill="#a8808f">{l}</text>')
a('<line x1="80" y1="450" x2="780" y2="450" stroke="#3a1f33"/>')
# lenguajes
a(f'<text x="60" y="500" {F} font-size="13" font-weight="700" letter-spacing="3" fill="#f06292">Lenguajes</text>')
x=60; tot=sum(p for _,p,_ in LANGS); bw=740
a('<clipPath id="bar"><rect x="60" y="518" width="740" height="10" rx="5"/></clipPath><g clip-path="url(#bar)">')
for n,p,c in LANGS:
    w=bw*p/tot; a(f'<rect x="{x:.1f}" y="518" width="{w:.1f}" height="10" fill="{c}"/>'); x+=w
a('</g>')
for i,(n,p,c) in enumerate(LANGS):
    cx=60+(i%4)*190; cy=560+(i//4)*26
    a(f'<circle cx="{cx+5}" cy="{cy-4}" r="5" fill="{c}"/><text x="{cx+16}" y="{cy}" {F} font-size="13" fill="#e8cfd8">{n} <tspan fill="#8a6676">{p}%</tspan></text>')
# actividad
a(f'<text x="60" y="650" {F} font-size="13" font-weight="700" letter-spacing="3" fill="#f06292">Actividad</text><text x="800" y="650" text-anchor="end" {F} font-size="12" fill="#a8808f">{CONTRIB}</text>')
cols=["#241324","#5c2d4d","#a8456f","#f06292","#ffb7c5","#fff0f3"]
for cI in range(40):
    for r in range(7):
        v=random.choices(range(6),[38,22,16,12,8,4])[0]
        a(f'<rect x="{60+cI*18.5:.1f}" y="{668+r*18}" width="14" height="14" rx="3" fill="{cols[v]}"/>')
# proyectos
a(f'<text x="60" y="835" {F} font-size="13" font-weight="700" letter-spacing="3" fill="#f06292">Proyectos destacados</text>')
for i,(t,d,l) in enumerate(PROJECTS):
    x=60+i*250
    a(f'<rect x="{x}" y="855" width="240" height="105" rx="12" fill="#1c0f1c" stroke="#5c2d4d"/><text x="{x+18}" y="887" {F} font-size="17" font-weight="700" fill="#ffd6e0">{t}</text><text x="{x+18}" y="911" {F} font-size="12" fill="#a8808f">{d}</text><circle cx="{x+22}" cy="940" r="5" fill="#f06292"/><text x="{x+34}" y="944" {M} font-size="12" fill="#e8cfd8">{l}</text>')
# pétalos cayendo (animados)
for i in range(16):
    x=random.randint(30,830); d=random.uniform(11,20); s=random.uniform(.5,1); dx=random.randint(-60,60)
    op=random.uniform(.35,.8)
    a(f'<g opacity="{op:.2f}" fill="#ffb7c5"><use href="#petal" transform="scale({s:.2f})"><animateTransform attributeName="transform" type="rotate" values="0;360" dur="{d/2:.1f}s" repeatCount="indefinite" additive="sum"/></use>'
      f'<animateMotion path="M{x},-30 C{x+dx},300 {x-dx},650 {x+dx//2},{H+30}" dur="{d:.1f}s" begin="-{random.uniform(0,d):.1f}s" repeatCount="indefinite"/></g>')
a('</svg>')
open('profile-card.svg','w',encoding='utf-8').write('\n'.join(o))
