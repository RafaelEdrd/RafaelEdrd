"""Build the static profile illustrations.

All assets are local, deterministic and self-hosted. This command intentionally does
not regenerate the approved animated hero; see docs/profile-design.md.

Usage:
    python scripts/generate_visuals.py
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "assets" / "profile"

# Match the APPROVED hero palette. Do not modify the user's brand PNG.
BG = "#080B0F"
PANEL = "#0C1116"
PANEL_2 = "#10171D"
EDGE = "#293440"
WHITE = "#EDF1F0"
MUTED = "#8C9BA5"
FAINT = "#627783"
GREEN = "#76C5A2"
SOFT_GREEN = "#3D7060"
MONO = "'DejaVu Sans Mono',Consolas,monospace"
SANS = "'DejaVu Sans',Arial,Helvetica,sans-serif"

PROJECTS = [
    {"n": "01", "slug": "webhook-relay", "title": "WEBHOOK RELAY", "description": "Entrega, validação e retentativas de eventos", "stack": "NODE.JS   /   TYPESCRIPT   /   POSTGRESQL", "kind": "INTEGRAÇÕES"},
    {"n": "02", "slug": "data-reconciliation", "title": "DATA RECONCILIATION", "description": "Conciliação determinística e divergências", "stack": "PYTHON   /   CSV   /   TESTES", "kind": "DADOS"},
    {"n": "03", "slug": "process-forge", "title": "PROCESS FORGE", "description": "Pipelines declarativos e validação de DAG", "stack": "NODE.JS   /   PIPELINES   /   TESTES", "kind": "AUTOMAÇÃO"},
    {"n": "04", "slug": "approval-workflow", "title": "APPROVAL WORKFLOW", "description": "Estados, aprovações e rastreabilidade", "stack": "PYTHON   /   FASTAPI   /   SQL", "kind": "PROCESSOS"},
    {"n": "05", "slug": "dispatch-planner", "title": "DISPATCH PLANNER", "description": "Agenda com competências e restrições", "stack": "PYTHON   /   SCHEDULING   /   TESTES", "kind": "OPERAÇÃO"},
    {"n": "06", "slug": "commerce-control", "title": "COMMERCE CONTROL", "description": "Reserva, idempotência e conciliação", "stack": "PYTHON   /   ESTOQUE   /   AUDITORIA", "kind": "CONSISTÊNCIA"},
    {"n": "07", "slug": "operations-dashboard", "title": "OPERATIONS DASHBOARD", "description": "Indicadores com contexto operacional", "stack": "REACT   /   FASTAPI   /   SQLITE", "kind": "ANÁLISE"},
    {"n": "08", "slug": "content-manager", "title": "CONTENT MANAGER", "description": "Revisão e publicação editorial", "stack": "PHP   /   MYSQL   /   CI", "kind": "SISTEMAS"},
]

SECTIONS = [
    ("01", "SOBRE", "TRAJETÓRIA  /  CONTEXTO", "sobre"),
    ("02", "ENGENHARIA", "REGRAS  /  IMPLEMENTAÇÃO", "engenharia"),
    ("03", "PROJETOS", "CÓDIGO  /  DOCUMENTAÇÃO", "projetos"),
    ("04", "TECNOLOGIAS", "FERRAMENTAS  /  APLICAÇÃO", "tecnologias"),
    ("05", "BASTIDORES", "DECISÕES  /  TRADE-OFFS", "bastidores"),
]


def write_svg(path: Path, source: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source.strip() + "\n", encoding="utf-8")


def shell(w: int, h: int, radius: int = 14) -> str:
    return (
        f'<rect width="{w}" height="{h}" rx="{radius}" fill="{BG}"/>'
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{radius-1}" fill="none" stroke="{EDGE}" stroke-width="2"/>'
    )


def label(x: int, y: int, content: str, *, size: int=16, color: str=MUTED, weight: int=400, family: str=MONO, anchor: str="start", spacing: float=0) -> str:
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}" letter-spacing="{spacing}">{escape(content)}</text>'


def section(n: str, title: str, metadata: str, slug: str) -> None:
    w, h = 1200, 106
    body = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(n+" / "+title)}">'
        f'<rect width="{w}" height="{h}" fill="{BG}"/>'
        f'<path d="M0 2H1200" stroke="{EDGE}" stroke-width="2"/>'
        f'<path d="M0 2H98" stroke="{GREEN}" stroke-width="4"/>'
        f'<rect x="2" y="27" width="68" height="53" rx="9" fill="{PANEL_2}" stroke="{EDGE}"/>'
        + label(36, 63, n, size=27, color=GREEN, weight=700, anchor="middle")
        + label(91, 66, title, size=37, color=WHITE, weight=700, family=SANS)
        + label(1182, 63, metadata, size=16, color=FAINT, anchor="end", spacing=1)
        + f'<path d="M0 104H1200" stroke="{EDGE}" stroke-width="1"/>'
        + '</svg>'
    )
    write_svg(BASE / "sections" / f"{slug}.svg", body)


def focus() -> None:
    w, h = 1200, 247
    names = [
        ("SISTEMAS WEB", "Regras, interfaces, APIs", "01"),
        ("AUTOMAÇÃO", "Integrações e rotinas", "02"),
        ("DADOS", "Conciliação e indicadores", "03"),
    ]
    elements = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Atuação em sistemas web, automação e dados">', shell(w,h),
                label(32, 38, "CAMPOS DE ATUAÇÃO", size=16,color=GREEN,spacing=1.4),
                label(1167,38, "UMA OPERAÇÃO   /   TRÊS FRENTES",size=15,color=FAINT,anchor="end"),
                f'<path d="M30 57H1170" stroke="{EDGE}"/>']
    for i,(name, desc, n) in enumerate(names):
        x = 32 + i*392
        elements += [
            f'<rect x="{x}" y="75" width="366" height="138" rx="11" fill="{PANEL}" stroke="{EDGE}"/>',
            label(x+18,105,n,size=15,color=GREEN),
            label(x+18,151,name,size=28,color=WHITE,weight=700,family=SANS),
            label(x+18,188,desc,size=19,color=MUTED,family=SANS),
            f'<path d="M{x+331} 95 h14 v14" fill="none" stroke="{SOFT_GREEN}" stroke-width="2"/>',
        ]
    elements.append('</svg>')
    write_svg(BASE / "focus.svg", ''.join(elements))


def architecture() -> None:
    w,h=1200,338
    blocks = [
        ("01", "DIAGNÓSTICO", "Contexto", "Entradas e exceções"),
        ("02", "CONTRATO", "Regras", "Invariantes e limites"),
        ("03", "IMPLEMENTAÇÃO", "Código", "Testes e integração"),
        ("04", "OPERAÇÃO", "Evidência", "Logs e manutenção"),
    ]
    el = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Fluxo de engenharia: diagnóstico, contrato, implementação e operação">',
        shell(w,h),
        label(32,42,"MODELO DE EXECUÇÃO",size=16,color=GREEN,spacing=1.2),
        label(1167,42,"DO PROBLEMA AO MONITORAMENTO",size=15,color=FAINT,anchor="end"),
        f'<path d="M30 60H1170" stroke="{EDGE}"/>']
    for i,(n,tag,big,desc) in enumerate(blocks):
        x=30+i*293
        el += [
            f'<rect x="{x}" y="85" width="268" height="177" rx="12" fill="{PANEL}" stroke="{EDGE}" stroke-width="2"/>',
            label(x+19,119,f"{n}  /  {tag}",size=14,color=GREEN),
            label(x+18,179,big,size=36,color=WHITE,weight=700,family=SANS),
            label(x+19,220,desc,size=17,color=MUTED,family=SANS),
            f'<path d="M{x+19} 241h{212 if i<3 else 160}" stroke="{SOFT_GREEN}" stroke-width="3"/>',
            f'<circle cx="{x+243}" cy="241" r="4" fill="{GREEN}"/>'
        ]
        if i<3:
            el += [f'<path d="M{x+268} 173h25" stroke="{GREEN}" stroke-width="3"/>',
                   f'<path d="M{x+285} 165l8 8 -8 8" stroke="{GREEN}" stroke-width="3" fill="none"/>']
    el.extend([f'<path d="M30 291H1170" stroke="{EDGE}"/>',
        label(32,315,"VALIDAR ANTES DE ALTERAR   /   TESTAR ANTES DE ENTREGAR   /   MEDIR DEPOIS DE PUBLICAR",size=17,color=MUTED),
        '</svg>'])
    write_svg(BASE / 'architecture.svg', ''.join(el))


def motif(slug: str) -> str:
    """A small schematic for each project, describing its actual domain.

    Coordinates are relative to the card's right-side panel at x=712 y=52.
    """
    stroke=f'stroke="{SOFT_GREEN}" stroke-width="3" fill="none"'
    br=f'fill="{PANEL_2}" stroke="{SOFT_GREEN}" stroke-width="2"'
    dot=f'fill="{GREEN}"'
    if slug=='webhook-relay':
        return f'''<path d="M741 97H800M825 97H878M900 97H932" {stroke}/>
        <circle cx="733" cy="97" r="14" {br}/><rect x="801" y="83" width="27" height="28" rx="5" {br}/>
        <circle cx="889" cy="97" r="14" {br}/><circle cx="940" cy="97" r="8" {dot}/>
        <path d="M835 122h67v17h-67" {stroke}/><path d="M839 130l-7 -8 7 -8" {stroke}/>
        {label(841,161,"RETRY",size=14,color=MUTED,anchor='middle')}'''
    if slug=='data-reconciliation':
        return f'''<rect x="723" y="63" width="80" height="110" rx="6" {br}/><rect x="853" y="63" width="80" height="110" rx="6" {br}/>
        {''.join(f'<path d="M735 {78+i*20}h52M865 {78+i*20}h52" stroke="{SOFT_GREEN}" stroke-opacity="{0.38 if i!=2 else 1}" stroke-width="4"/>' for i in range(4))}
        <path d="M804 102h48M827 94l8 8-8 8" {stroke}/>
        <circle cx="827" cy="139" r="7" {dot}/>'''
    if slug=='process-forge':
        return f'''<path d="M754 113L833 73M754 113L833 154M850 73L932 113M850 154L932 113" {stroke}/>
        <circle cx="747" cy="113" r="15" {br}/><circle cx="841" cy="73" r="15" {br}/><circle cx="841" cy="154" r="15" {br}/><circle cx="940" cy="113" r="15" {br}/>
        <circle cx="747" cy="113" r="4" {dot}/><circle cx="940" cy="113" r="4" {dot}/>'''
    if slug=='approval-workflow':
        return f'''<path d="M731 116H941" {stroke}/><circle cx="742" cy="116" r="17" {br}/>
        <circle cx="837" cy="116" r="17" {br}/><circle cx="930" cy="116" r="17" {br}/>
        <path d="M734 116l5 5 9-11 M827 116l7 7 12-15" stroke="{GREEN}" stroke-width="3" fill="none"/>
        {label(742,158,"ABERTO",size=11,color=MUTED,anchor='middle')}
        {label(837,158,"REVISÃO",size=11,color=MUTED,anchor='middle')}
        {label(931,158,"FINAL",size=11,color=MUTED,anchor='middle')}'''
    if slug=='dispatch-planner':
        cells=[]
        for r in range(3):
            for c in range(5):
                active = ((r,c) in ((0,0),(0,1),(1,2),(1,3),(2,1),(2,4)))
                cells.append(f'<rect x="{725+c*47}" y="{61+r*34}" width="39" height="27" rx="4" fill="{SOFT_GREEN if active else PANEL_2}" stroke="{EDGE}"/>')
        return ''.join(cells) + label(725,178,"CAPACIDADE  /  CONFLITOS",size=13,color=MUTED)
    if slug=='commerce-control':
        return f'''<rect x="721" y="84" width="66" height="69" rx="5" {br}/><rect x="802" y="70" width="66" height="83" rx="5" {br}/><rect x="883" y="94" width="66" height="59" rx="5" {br}/>
        <path d="M734 107h39M734 119h39M815 96h39M815 108h39M896 117h39" stroke="{SOFT_GREEN}" stroke-width="3"/>
        <path d="M728 162h217" stroke="{GREEN}" stroke-width="2"/>
        {label(835,182,"MOVIMENTOS",size=14,color=MUTED,anchor='middle')}'''
    if slug=='operations-dashboard':
        bars=[43,68,34,81,59,98,72]
        return ''.join(f'<rect x="{725+i*33}" y="{161-v}" width="20" height="{v}" rx="3" fill="{SOFT_GREEN if i!=5 else GREEN}"/>' for i,v in enumerate(bars)) + f'<path d="M715 165h243" stroke="{EDGE}" stroke-width="3"/>'
    if slug=='content-manager':
        return f'''<rect x="725" y="61" width="63" height="99" rx="6" {br}/><rect x="813" y="61" width="63" height="99" rx="6" {br}/>
        <rect x="900" y="61" width="55" height="99" rx="6" {br}/>
        <path d="M736 84h39m-39 13h39m-39 13h29M824 84h39m-39 13h39m-39 13h29M911 84h31m-31 13h31" stroke="{SOFT_GREEN}" stroke-width="3"/>
        <path d="M746 132l10 10 17-21M831 132l10 10 17-21" stroke="{GREEN}" stroke-width="3" fill="none"/>'''
    raise ValueError(f"Missing project motif: {slug}")


def card(project: dict[str,str]) -> None:
    w,h=980,264
    slug=project['slug']
    body=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(project['title'])}: {escape(project['description'])}">
        {shell(w,h,16)}
        <path d="M0 3h980" stroke="{SOFT_GREEN}" stroke-width="4"/>
        {label(32,39,project['n']+'  /  '+project['kind'],size=17,color=GREEN,spacing=1.0)}
        <path d="M32 57h914" stroke="{EDGE}" stroke-width="1"/>
        <rect x="706" y="61" width="240" height="127" rx="9" fill="{PANEL}" stroke="{EDGE}"/>
        {motif(slug)}
        {label(32,125,project['title'],size=41,color=WHITE,weight=700,family=SANS)}
        {label(33,170,project['description'],size=21,color=MUTED,family=SANS)}
        <path d="M32 203h914" stroke="{EDGE}"/>
        {label(33,239,project['stack'],size=17,color=MUTED)}
        {label(945,239,'EXPLORAR  ↗',size=16,color=GREEN,anchor='end')}
        </svg>'''
    write_svg(BASE / 'cards' / f'{slug}.svg', body)


def footer() -> None:
    w,h=1200,105
    el = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Projetos explicáveis, decisões rastreáveis, manutenção possível">
      <rect width="{w}" height="{h}" fill="{BG}"/>
      <path d="M0 1h1200" stroke="{EDGE}" stroke-width="2"/>
      <path d="M0 1h140" stroke="{GREEN}" stroke-width="4"/>
      {label(20,58,'PROJETOS EXPLICÁVEIS.  DECISÕES RASTREÁVEIS.  MANUTENÇÃO POSSÍVEL.',size=24,color=WHITE,weight=700,family=SANS)}
      {label(1180,90,'RA / 2026',size=15,color=FAINT,anchor='end')}
      </svg>'''
    write_svg(BASE/'footer.svg',el)


def main() -> None:
    for props in SECTIONS:
        section(*props)
    focus()
    architecture()
    for project in PROJECTS:
        card(project)
    footer()
    print('OK: 5 section headers, focus, architecture, 8 project cards, footer.')
    print('Approved hero.gif, hero-still.png and brand PNG were NOT modified.')


if __name__ == '__main__':
    main()
