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
GOLD = '#DAB47B'
BLUE = '#819BBE'

PROJECTS = [
    ('01', 'webhook-relay', 'WEBHOOK RELAY', 'Entrega controlada de eventos e retentativas', 'NODE.JS  /  TYPESCRIPT  /  POSTGRESQL', GREEN),
    ('02', 'content-manager', 'CONTENT MANAGER', 'Fluxos editoriais, revisão e publicação', 'PHP  /  MYSQL  /  CI', BLUE),
    ('03', 'data-reconciliation', 'DATA RECONCILIATION', 'Conciliação determinística e divergências', 'PYTHON  /  CSV  /  TESTES', GOLD),
    ('04', 'approval-workflow', 'APPROVAL WORKFLOW', 'Estados, aprovações e rastreabilidade', 'PYTHON  /  FASTAPI  /  SQL', GREEN),
    ('05', 'operations-dashboard', 'OPERATIONS DASHBOARD', 'Visão operacional com indicadores acionáveis', 'REACT  /  FASTAPI  /  SQLITE', BLUE),
    ('06', 'process-forge', 'PROCESS FORGE', 'Pipelines declarativos e validação de DAG', 'NODE.JS  /  PIPELINE  /  TESTES', GOLD),
    ('07', 'dispatch-planner', 'DISPATCH PLANNER', 'Planejamento com competências e restrições', 'PYTHON  /  SCHEDULING  /  TESTES', GREEN),
    ('08', 'commerce-control', 'COMMERCE CONTROL', 'Reserva de estoque, idempotência e conciliação', 'PYTHON  /  INVENTORY  /  AUDIT', BLUE),
]


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def make_card(index, slug, title, subtitle, stack, accent):
    # Text fits both desktop 2-column and narrow screen 1-column layouts.
    lines = []
    for offset, opacity in [(0, 0.80), (22, 0.42), (44, 0.20)]:
        lines.append(f'<path d="M670 {65 + offset} L760 {65 + offset} L813 {111 + offset} L931 {111 + offset}" stroke="{accent}" stroke-width="2" stroke-opacity="{opacity}" fill="none"/>')
    nodes = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{accent}" opacity="{o}"/>'
                    for x,y,r,o in [(672,65,5,0.8),(760,65,5,0.75),(813,111,6,0.65),(931,111,5,0.9),(931,154,3,0.4)])
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 280" width="980" height="280" role="img" aria-label="{escape(title)}">
      <rect width="980" height="280" rx="20" fill="{BG}"/>
      <rect x="1" y="1" width="978" height="278" rx="19" fill="none" stroke="{EDGE}" stroke-width="2"/>
      <path d="M0 0H980" stroke="{accent}" stroke-width="5" opacity=".85"/>
      <path d="M34 204 H946" stroke="{EDGE}" stroke-width="1"/>
      <text x="35" y="39" font-family="ui-monospace,Consolas,monospace" font-size="19" letter-spacing="3" fill="{accent}">RA / LAB  {index}</text>
      <text x="35" y="111" font-family="Arial,Helvetica,sans-serif" font-size="44" font-weight="700" fill="{WHITE}">{escape(title)}</text>
      <text x="36" y="157" font-family="Arial,Helvetica,sans-serif" font-size="23" fill="{MUTED}">{escape(subtitle)}</text>
      <text x="36" y="241" font-family="ui-monospace,Consolas,monospace" font-size="19" fill="{accent}" letter-spacing="1.2">{escape(stack)}</text>
      <text x="935" y="239" text-anchor="end" font-family="ui-monospace,Consolas,monospace" font-size="18" fill="{MUTED}">VIEW CODE ></text>
      {''.join(lines)}{nodes}
    </svg>'''
    write(CARDS / f'{slug}.svg', svg)


for item in PROJECTS:
    make_card(*item)

architecture = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="328" viewBox="0 0 1200 328" role="img" aria-label="Pipeline de engenharia: diagnosticar, modelar, implementar e observar">
 <rect width="1200" height="328" rx="18" fill="{BG}" />
 <rect x="1" y="1" width="1198" height="326" rx="17" fill="none" stroke="{EDGE}" stroke-width="2"/>
 <text x="39" y="41" font-family="ui-monospace,Consolas,monospace" font-size="19" letter-spacing="3" fill="{GREEN}">OPERATING MODEL / 04 ESTÁGIOS</text>
 <text x="1160" y="41" text-anchor="end" font-family="ui-monospace,Consolas,monospace" font-size="17" fill="{MUTED}">DESIGN / DELIVERY</text>
 {''.join(f'''<g>
   <rect x="{35 + i*292}" y="75" width="264" height="163" rx="12" fill="{PANEL}" stroke="{EDGE}"/>
   <text x="{57+i*292}" y="108" font-family="ui-monospace,Consolas,monospace" font-size="17" letter-spacing="2" fill="{[GREEN,BLUE,GOLD,GREEN][i]}">0{i+1} / {['DISCOVER','MODEL','BUILD','OBSERVE'][i]}</text>
   <text x="{57+i*292}" y="161" font-family="Arial,Helvetica,sans-serif" font-size="29" font-weight="bold" fill="{WHITE}">{['Contexto','Regras','Entrega','Evidências'][i]}</text>
   <text x="{57+i*292}" y="197" font-family="Arial,Helvetica,sans-serif" font-size="19" fill="{MUTED}">{['Entender a operação','Definir invariantes','Implementar com testes','Logs e manutenção'][i]}</text>
   </g>''' for i in range(4))}
 <path d="M299 155 H327 M591 155 H619 M883 155 H911" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>
 <path d="M317 148 l12 7 -12 7 M609 148 l12 7 -12 7 M901 148 l12 7 -12 7" stroke="{GREEN}" stroke-width="3" fill="none"/>
 <text x="38" y="283" font-family="ui-monospace,Consolas,monospace" font-size="18" letter-spacing="1" fill="{MUTED}">ENTRADA LEGÍVEL    /    DECISÃO EXPLÍCITA    /    MUDANÇA CONTROLADA    /    RESULTADO AUDITÁVEL</text>
 </svg>'''
write(ASSETS/'architecture.svg', architecture)

# GIF animation is used intentionally: image-only, self-hosted, no scripts.
# Geometry is symmetric, with aligned labels and no moving white/orbiting dot.
W, H = 1200, 430
FRAME_COUNT = 48


def pick_font(variants: tuple[str, ...]) -> str:
    roots = (
        Path('/usr/share/fonts/truetype/dejavu'),
        Path('/usr/share/fonts/truetype/liberation2'),
        Path(os.getenv('WINDIR', 'C:/Windows')) / 'Fonts',
        Path('/System/Library/Fonts'),
    )
    for root in roots:
        for name in variants:
            candidate = root / name
            if candidate.is_file():
                return str(candidate)
    raise RuntimeError('Fonte de sistema nao encontrada; ajuste pick_font.')


font_reg = pick_font(('DejaVuSans.ttf', 'Arial.ttf', 'arial.ttf', 'Helvetica.ttc'))
font_bold = pick_font(('DejaVuSans-Bold.ttf', 'Arialbd.ttf', 'arialbd.ttf', 'Helvetica.ttc'))
font_mono = pick_font(('DejaVuSansMono.ttf', 'consola.ttf', 'Menlo.ttc'))
font_mono_b = pick_font(('DejaVuSansMono-Bold.ttf', 'consolab.ttf', 'Menlo.ttc'))
F = lambda path, size: ImageFont.truetype(path, size)
NAME = F(font_bold, 70)
LABEL = F(font_mono_b, 17)
SUB = F(font_reg, 24)
SMALL = F(font_mono, 16)
STEP_NUMBER = F(font_mono_b, 17)
STEP_LABEL = F(font_mono, 16)
STEP_META = F(font_mono, 14)
GREEN_RGB = (118, 197, 162)
BG_RGB = (8, 11, 16)

# The source PNG is copied verbatim to /brand. Cropping whitespace and resizing
# for the header does not alter the actual brand file or redraw its symbol.
ORIGINAL_LOGO = ASSETS / 'brand' / 'rafael-analyst-oficial.png'
if not ORIGINAL_LOGO.is_file():
    raise FileNotFoundError(f'Logomarca oficial ausente: {ORIGINAL_LOGO}')
_logo = Image.open(ORIGINAL_LOGO).convert('RGB')
_bright = _logo.convert('L').point(lambda value: 255 if value >= 90 else 0)
_bbox = _bright.getbbox()
if not _bbox:
    raise RuntimeError('Nao foi possivel localizar a marca oficial')
_logo_crop = _logo.crop(_bbox)
_logo_width = 315
OFFICIAL_LOCKUP = _logo_crop.resize(
    (_logo_width, round(_logo_crop.height * _logo_width / _logo_crop.width)),
    Image.Resampling.LANCZOS,
)


def draw_hero(frame: int) -> Image.Image:
    im = Image.new('RGB', (W, H), BG_RGB)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((3, 3, W - 4, H - 4), radius=19, outline=(48, 60, 71), width=2)
    d.rectangle((0, 0, W, 3), fill=(94, 149, 128))
    for y in range(72, 380, 30):
        for x in range(655, 1170, 30):
            d.ellipse((x, y, x+2, y+2), fill=(22, 32, 37))

    # Official lockup embedded as one proportionate brand element.
    im.paste(OFFICIAL_LOCKUP, (40, 17))
    d.text((1160, 29), 'PORTFOLIO   /   2026', font=SMALL, fill=(125, 139, 151), anchor='ra')
    d.line((38, 79, 1161, 79), fill=(40, 50, 60), width=2)

    # Main title is unchanged from the earlier approved layout.
    d.text((38, 120), 'Rafael', font=NAME, fill=(238, 242, 241))
    d.text((38, 201), 'Eduardo', font=NAME, fill=(238, 242, 241))
    d.text((40, 294), 'DESENVOLVEDOR DE SOLUÇÕES E AUTOMAÇÃO', font=LABEL, fill=GREEN_RGB)
    d.text((41, 334), 'Sistemas web  /  Dados  /  Integrações', font=SUB, fill=(145, 160, 171))
    d.line((38, 379, 1160, 379), fill=(40, 50, 60), width=2)
    d.text((41, 396), 'RAFAELANALYST.COM.BR', font=SMALL, fill=(119, 132, 143))
    d.text((1160, 396), 'REGRAS  /  TESTES  /  MANUTENÇÃO', font=SMALL, fill=(119, 132, 143), anchor='ra')

    # Symmetric execution model: equal spacing, one shared baseline, fixed padding.
    left, top, right, bottom = 682, 113, 1160, 334
    d.rounded_rectangle((left, top, right, bottom), radius=14,
                        fill=(13, 19, 24), outline=(46, 59, 67), width=2)
    d.text((711, 135), 'MODELO  /  EXECUÇÃO', font=SMALL, fill=(128, 148, 161))
    d.ellipse((1126, 134, 1137, 145), fill=(105, 172, 140))
    d.rounded_rectangle((712, 174, 1132, 180), radius=3, fill=(36, 48, 52))
    progress = int(420 * ((frame + 1) / FRAME_COUNT))
    d.rounded_rectangle((712, 174, 712 + max(5, progress), 180), radius=3, fill=(96, 164, 136))

    xs = (763, 921, 1079)
    cy = 228
    r = 31
    # Straight connectors first, then nodes. Nothing overlaps the labels.
    for first, second in zip(xs, xs[1:]):
        d.line((first+r, cy, second-r, cy), fill=(53, 79, 76), width=3)

    labels = ('VALIDAR', 'EXECUTAR', 'AUDITAR')
    subtitles = ('ENTRADA', 'REGRAS', 'EVIDÊNCIA')
    active = min(2, (frame * 3) // FRAME_COUNT)
    for idx, x in enumerate(xs):
        selected = idx == active
        border = (103, 170, 143) if selected else (66, 94, 91)
        d.ellipse((x-r, cy-r, x+r, cy+r), fill=(19, 31, 32), outline=border, width=3)
        # Subtle animated focus ring: no bright, free-floating white circle.
        if selected:
            d.arc((x-r-5, cy-r-5, x+r+5, cy+r+5), start=208, end=333,
                  fill=(132, 204, 172), width=2)
        d.text((x, cy-1), f'0{idx+1}', font=STEP_NUMBER,
               fill=(215, 232, 221), anchor='mm')
        d.text((x, 282), labels[idx], font=STEP_LABEL,
               fill=(188, 204, 205), anchor='mm')
        d.text((x, 306), subtitles[idx], font=STEP_META,
               fill=(111, 143, 149), anchor='mm')
    return im


frames = [draw_hero(frame).quantize(colors=64, method=Image.Quantize.FASTOCTREE)
          for frame in range(FRAME_COUNT)]
frames[0].save(ASSETS/'hero.gif', save_all=True, append_images=frames[1:],
               duration=90, loop=0, optimize=True, disposal=2)
draw_hero(0).save(ASSETS/'hero-still.png', optimize=True)
print('Generated:', len(PROJECTS), 'cards, architecture.svg, hero.gif, hero-still.png')
