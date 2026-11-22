"""Generate the versioned, original visual assets used in the profile README.

No network calls. Dependencies: Pillow (only needed to regenerate the GIF).
The user's official brand mark is included separately in assets/profile/brand.
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'profile'
CARDS = ASSETS / 'cards'
CARDS.mkdir(parents=True, exist_ok=True)

BG = '#080B0F'
PANEL = '#0C1116'
EDGE = '#293440'
WHITE = '#EBF0EF'
MUTED = '#8C9BA5'
GREEN = '#76C5A2'
GOLD = '#8E9CA9'
BLUE = '#8CA9BA'

PROJECTS = [
    ('01', 'webhook-relay', 'WEBHOOK RELAY', 'Entrega controlada de eventos e retentativas', 'NODE.JS  /  TYPESCRIPT  /  POSTGRESQL', GREEN),
    ('02', 'data-reconciliation', 'DATA RECONCILIATION', 'Conciliação determinística e divergências', 'PYTHON  /  CSV  /  TESTES', GOLD),
    ('03', 'process-forge', 'PROCESS FORGE', 'Pipelines declarativos e validação de DAG', 'NODE.JS  /  PIPELINE  /  TESTES', GREEN),
    ('04', 'approval-workflow', 'APPROVAL WORKFLOW', 'Estados, aprovações e rastreabilidade', 'PYTHON  /  FASTAPI  /  SQL', BLUE),
    ('05', 'dispatch-planner', 'DISPATCH PLANNER', 'Planejamento com competências e restrições', 'PYTHON  /  SCHEDULING  /  TESTES', GREEN),
    ('06', 'commerce-control', 'COMMERCE CONTROL', 'Reserva de estoque, idempotência e conciliação', 'PYTHON  /  INVENTORY  /  AUDIT', BLUE),
    ('07', 'operations-dashboard', 'OPERATIONS DASHBOARD', 'Visão operacional com indicadores acionáveis', 'REACT  /  FASTAPI  /  SQLITE', BLUE),
    ('08', 'content-manager', 'CONTENT MANAGER', 'Fluxos editoriais, revisão e publicação', 'PHP  /  MYSQL  /  CI', GOLD),
]


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def make_card(index, slug, title, subtitle, stack, accent):
    # Text fits both desktop 2-column and narrow screen 1-column layouts.
    lines = []
    for offset, opacity in [(0, 0.62), (22, 0.27), (44, 0.12)]:
        lines.append(f'<path d="M670 {65 + offset} L760 {65 + offset} L813 {111 + offset} L931 {111 + offset}" stroke="{accent}" stroke-width="2" stroke-opacity="{opacity}" fill="none"/>')
    nodes = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{accent}" opacity="{o}"/>'
                    for x,y,r,o in [(672,65,5,0.8),(760,65,5,0.75),(813,111,6,0.65),(931,111,5,0.9),(931,154,3,0.4)])
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 280" width="980" height="280" role="img" aria-label="{escape(title)}">
      <rect width="980" height="280" rx="20" fill="{BG}"/>
      <rect x="1" y="1" width="978" height="278" rx="19" fill="none" stroke="{EDGE}" stroke-width="2"/>
      <path d="M0 0H980" stroke="{accent}" stroke-width="5" opacity=".85"/>
      <path d="M34 204 H946" stroke="{EDGE}" stroke-width="1"/>
      <text x="35" y="39" font-family="ui-monospace,Consolas,monospace" font-size="19" letter-spacing="3" fill="{accent}">RA  /  PROJETO {index}</text>
      <text x="35" y="111" font-family="Arial,Helvetica,sans-serif" font-size="44" font-weight="700" fill="{WHITE}">{escape(title)}</text>
      <text x="36" y="157" font-family="Arial,Helvetica,sans-serif" font-size="23" fill="{MUTED}">{escape(subtitle)}</text>
      <text x="36" y="241" font-family="ui-monospace,Consolas,monospace" font-size="19" fill="{accent}" letter-spacing="1.2">{escape(stack)}</text>
      <text x="935" y="239" text-anchor="end" font-family="ui-monospace,Consolas,monospace" font-size="18" fill="{MUTED}">VER CÓDIGO  ›</text>
      {''.join(lines)}{nodes}
    </svg>'''
    write(CARDS / f'{slug}.svg', svg)


for item in PROJECTS:
    make_card(*item)

architecture = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="328" viewBox="0 0 1200 328" role="img" aria-label="Pipeline de engenharia: diagnosticar, modelar, implementar e observar">
 <rect width="1200" height="328" rx="18" fill="{BG}" />
 <rect x="1" y="1" width="1198" height="326" rx="17" fill="none" stroke="{EDGE}" stroke-width="2"/>
 <text x="39" y="41" font-family="ui-monospace,Consolas,monospace" font-size="19" letter-spacing="3" fill="{GREEN}">MODELO OPERACIONAL  /  04 ETAPAS</text>
 <text x="1160" y="41" text-anchor="end" font-family="ui-monospace,Consolas,monospace" font-size="17" fill="{MUTED}">PRÁTICA / ENTREGA</text>
 {''.join(f'''<g>
   <rect x="{35 + i*292}" y="75" width="264" height="163" rx="12" fill="{PANEL}" stroke="{EDGE}"/>
   <text x="{57+i*292}" y="108" font-family="ui-monospace,Consolas,monospace" font-size="17" letter-spacing="2" fill="{[GREEN,BLUE,GOLD,GREEN][i]}">0{i+1} / {['ENTENDER','MODELAR','ENTREGAR','ACOMPANHAR'][i]}</text>
   <text x="{57+i*292}" y="161" font-family="Arial,Helvetica,sans-serif" font-size="29" font-weight="bold" fill="{WHITE}">{['Contexto','Regras','Entrega','Evidências'][i]}</text>
   <text x="{57+i*292}" y="197" font-family="Arial,Helvetica,sans-serif" font-size="19" fill="{MUTED}">{['Entender a operação','Definir invariantes','Implementar com testes','Logs e manutenção'][i]}</text>
   </g>''' for i in range(4))}
 <path d="M299 155 H327 M591 155 H619 M883 155 H911" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>
 <path d="M317 148 l12 7 -12 7 M609 148 l12 7 -12 7 M901 148 l12 7 -12 7" stroke="{GREEN}" stroke-width="3" fill="none"/>
 <text x="38" y="283" font-family="ui-monospace,Consolas,monospace" font-size="18" letter-spacing="1" fill="{MUTED}">ENTRADA LEGÍVEL    /    DECISÃO EXPLÍCITA    /    MUDANÇA CONTROLADA    /    RESULTADO AUDITÁVEL</text>
 </svg>'''
write(ASSETS/'architecture.svg', architecture)

# GIF animation is used intentionally: it is image-only, self-hosted, no JavaScript
# execution and does not depend on third-party stat/image services.
W, H = 1200, 430
FPS = 58
def pick_font(variants: tuple[str, ...]) -> str:
    # Keep regeneration possible on Linux, Windows and macOS without bundling font files.
    search_roots = (
        Path('/usr/share/fonts/truetype/dejavu'),
        Path('/usr/share/fonts/truetype/liberation2'),
        Path(os.getenv('WINDIR', 'C:/Windows')) / 'Fonts',
        Path('/System/Library/Fonts'),
    )
    for root in search_roots:
        for name in variants:
            candidate = root / name
            if candidate.is_file():
                return str(candidate)
    raise RuntimeError('Fonte de sistema nao encontrada. Ajuste pick_font para uma fonte instalada.')

font_reg = pick_font(('DejaVuSans.ttf', 'Arial.ttf', 'arial.ttf', 'Helvetica.ttc'))
font_bold = pick_font(('DejaVuSans-Bold.ttf', 'Arialbd.ttf', 'arialbd.ttf', 'Helvetica.ttc'))
font_mono = pick_font(('DejaVuSansMono.ttf', 'consola.ttf', 'Menlo.ttc'))
font_mono_b = pick_font(('DejaVuSansMono-Bold.ttf', 'consolab.ttf', 'Menlo.ttc'))
F = lambda path, size: ImageFont.truetype(path, size)
NAME = F(font_bold, 70)
LABEL = F(font_mono_b, 17)
SUB = F(font_reg, 24)
SMALL = F(font_mono, 16)
CARD = F(font_mono_b, 17)
GREEN_RGB = (118,197,162)


# Extract the official RA symbol from the user's full-resolution PNG.
# We crop only the left part of the *same* raster; no tracing, reinterpretation
# or alpha-matting of the lettering. The unmodified master remains in /brand/.
ORIGINAL_LOGO = ASSETS / 'brand' / 'rafael-analyst-oficial.png'
if not ORIGINAL_LOGO.is_file():
    raise FileNotFoundError(f'Logomarca oficial ausente: {ORIGINAL_LOGO}')
_official = Image.open(ORIGINAL_LOGO).convert('RGB')
_mark_region = _official.crop((0, 0, min(309, _official.width), _official.height))
_mask = _mark_region.convert('L').point(lambda v: 255 if v >= 80 else 0)
_bbox = _mask.getbbox()
if not _bbox:
    raise RuntimeError('Nao foi possivel localizar o monograma oficial')
_mark_region = _mark_region.crop(_bbox)
_scale = min(75 / _mark_region.width, 44 / _mark_region.height)
MONOGRAM = _mark_region.resize(
    (round(_mark_region.width * _scale), round(_mark_region.height * _scale)),
    Image.Resampling.LANCZOS,
)
# Draw shapes at native size with 16-color palette to keep animation compact.
frames = []
for frame in range(FPS):
    im = Image.new('RGB', (W,H), (8,11,15))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((3,3,W-4,H-4),radius=19,outline=(48,60,71),width=2)
    d.rectangle((0,0,W,5),fill=(118,197,162))
    # Subtle technical dotted canvas on the right, quiet around type.
    for gy in range(68,385,30):
        for gx in range(655,1150,30):
            d.ellipse((gx,gy,gx+2,gy+2), fill=(22,32,37))
    im.paste(MONOGRAM, (38, 12 + (44 - MONOGRAM.height)//2))
    d.text((128,26), 'ENGENHARIA  /  OPERAÇÕES  /  DADOS',font=LABEL,fill=(118,197,162))
    d.text((1160,27), '2026  /  PROFILE',font=SMALL,fill=(125,139,151),anchor='ra')
    d.line((38,64,1161,64),fill=(40,50,60),width=2)
    d.text((38,111), 'Rafael',font=NAME,fill=(238,242,241))
    d.text((38,191), 'Eduardo',font=NAME,fill=(238,242,241))
    d.text((40,289), 'DESENVOLVEDOR DE SOLUÇÕES E AUTOMAÇÃO',font=LABEL,fill=GREEN_RGB)
    d.text((41,328), 'Sistemas web  /  Dados  /  Integrações',font=SUB,fill=(145,160,171))
    d.line((38,379,1160,379),fill=(40,50,60),width=2)
    d.text((41,396), 'RAFAELANALYST.COM.BR',font=SMALL,fill=(119,132,143))
    d.text((1160,396), 'REGRAS  /  TESTES  /  MANUTENÇÃO',font=SMALL,fill=(119,132,143),anchor='ra')
    # Schematic panel on the right.
    d.rounded_rectangle((687,110,1160,336),radius=13,fill=(13,19,24),outline=(46,59,67),width=2)
    d.text((713,132),'MODELO  /  EXECUÇÃO',font=SMALL,fill=(128,148,161))
    xys = [(735,237),(895,204),(1086,237)]
    lab = ['VALIDAR','EXECUTAR','AUDITAR']
    status = ['ENTRADA','REGRAS','EVIDÊNCIA']
    for i,((x,y),l,st) in enumerate(zip(xys,lab,status)):
        rr=35
        d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=(19,31,32),outline=(65,93,90),width=3)
        d.text((x,y-9),f'0{i+1}',font=CARD,fill=(214,231,220),anchor='mm')
        d.text((x,y+58),l,font=SMALL,fill=(185,198,205),anchor='mm')
        d.text((x,316),st,font=SMALL,fill=(107,133,145),anchor='mm')
    d.line((770,231,858,209),fill=(46,71,68),width=5)
    d.line((932,210,1048,233),fill=(46,71,68),width=5)
    # A time-dependent packet flowing through two links.
    phase = (frame / FPS) * 2
    seg = int(phase) % 2
    t = phase % 1
    a,b = ((770,231),(858,209)) if seg == 0 else ((932,210),(1048,233))
    xx=a[0]+(b[0]-a[0])*t
    yy=a[1]+(b[1]-a[1])*t
    d.ellipse((xx-7,yy-7,xx+7,yy+7),fill=(211,244,224))
    d.ellipse((xx-13,yy-13,xx+13,yy+13),outline=(100,176,143),width=2)
    # Progress strip.
    d.rounded_rectangle((713,171,1135,177),radius=3,fill=(38,51,52))
    d.rounded_rectangle((713,171,713+int(422*(frame+1)/FPS),177),radius=3,fill=GREEN_RGB)
    frame_brightness = 190 + int(50*abs(math.sin(frame/FPS*math.pi*2)))
    d.ellipse((1123,132,1136,145),fill=(80,frame_brightness,135))
    # Palette conversion keeps upload small while preserving crisp edges.
    frames.append(im.quantize(colors=54,method=Image.Quantize.FASTOCTREE))

frames[0].save(ASSETS/'hero.gif',save_all=True,append_images=frames[1:],duration=90,loop=0,optimize=True,disposal=2)
frames[0].convert('RGB').save(ASSETS/'hero-still.png',optimize=True)
print('Generated:', len(PROJECTS),'cards, architecture.svg, hero.gif, hero-still.png')
