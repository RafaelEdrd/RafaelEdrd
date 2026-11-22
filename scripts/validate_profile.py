"""Offline, fail-closed validation of the Rafael Analyst profile distribution.

The profile is a static GitHub README. These tests do not make network calls and
cannot assert availability of external repositories or icon CDN URLs.
"""
from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from xml.etree import ElementTree as ET

from generate_visuals import PROJECTS, SECTIONS

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / 'README.md'
ASSETS = ROOT / 'assets' / 'profile'

# Official, approved brand and hero files. Modifying these requires an explicit
# design review and corresponding checksum update; routine asset generation
# must never change them.
PINNED_SHA256 = {
    'brand/rafael-analyst-oficial.png': '0adf5742f1c31309a0ee640cfa4f3998274e2d1aae3f77206518b12ba39b2de5',
    'hero.gif': '11d1ec36525852b49d2c4b92b5e5e1027e0b8aaa8289d32b2de5e5c6b4391c88',
    'hero-still.png': '55827b8779a4efaa1df7d7cc574706364540af8c3e8995fd35088cb509658dcd',
}


def check() -> list[str]:
    errors: list[str] = []
    if not README.is_file():
        return ['README.md ausente']
    content = README.read_text(encoding='utf-8')

    for project in PROJECTS:
        slug = project['slug']
        if f'href="https://github.com/RafaelEdrd/{slug}"' not in content:
            errors.append(f'Link publico do projeto ausente: {slug}')
        if f'src="./assets/profile/cards/{slug}.svg"' not in content:
            errors.append(f'Card nao utilizado no README: {slug}')
        if not (ASSETS / 'cards' / f'{slug}.svg').is_file():
            errors.append(f'Card inexistente: {slug}')
    cards = re.findall(r'src="\./assets/profile/cards/([\w-]+)\.svg"',content)
    if len(cards) != len(PROJECTS) or len(set(cards)) != len(PROJECTS):
        errors.append('Os cards publicados devem corresponder exatamente aos oito projetos')

    for _,_,_,slug in SECTIONS:
        if f'<a name="{slug}"></a>' not in content:
            errors.append(f'Anchor de secao ausente: {slug}')
        if f'src="./assets/profile/sections/{slug}.svg"' not in content:
            errors.append(f'Cabecalho da secao ausente: {slug}')
        if f'href="#{slug}"' not in content:
            errors.append(f'Navegacao da secao ausente: {slug}')
        if f'src="./assets/profile/navigation/{slug}.svg"' not in content:
            errors.append(f'Botao de navegacao ausente: {slug}')

    for name in ('site','linkedin','contato'):
        if f'src="./assets/profile/navigation/{name}.svg"' not in content:
            errors.append(f'Link externo na barra de navegacao ausente: {name}')
    for name in ('focus.svg','architecture.svg','footer.svg'):
        if f'src="./assets/profile/{name}"' not in content:
            errors.append(f'Componente grafico ausente: {name}')
    if 'src="./assets/profile/brand/rafael-analyst-oficial.png"' in content:
        errors.append('Logo duplicada no corpo: ja integra o hero aprovado')
    if 'https://github.com/RafaelEdrd/conversa-studio' in content:
        errors.append('Conversa Studio exige confirmacao de visibilidade antes de receber card')
    if content.count('<details>') != 4 or content.count('</details>') != 4:
        errors.append('Esperados exatamente quatro paineis expansivos completos')
    if '<source media="(prefers-reduced-motion: reduce)"' not in content:
        errors.append('Fallback de movimento reduzido ausente')
    if len(content.encode('utf-8')) > 180_000:
        errors.append('README acima do limite interno de manutencao')
    if re.search(r'<\s*(script|iframe|object|embed|style)\b', content, re.I):
        errors.append('HTML nao suportado ou executavel no README')
    if 'javascript:' in content.lower():
        errors.append('Link javascript: nao permitido')

    # Verify all self-hosted images and their meaningful alternative text.
    for match in re.finditer(r'<img\b[^>]+>', content, flags=re.I | re.S):
        tag = match.group(0)
        src_match = re.search(r'\bsrc="([^"]+)"', tag)
        alt_match = re.search(r'\balt="([^"]*)"', tag)
        if not src_match:
            errors.append('Elemento img sem src')
            continue
        if not alt_match or not alt_match.group(1).strip():
            errors.append(f'Imagem sem descricao alternativa: {src_match.group(1)}')
        src = src_match.group(1)
        if src.startswith('https://'):
            continue
        if not src.startswith('./'):
            errors.append(f'Imagem com caminho incorreto: {src}')
            continue
        target = (ROOT / src[2:]).resolve()
        if not target.is_relative_to(ROOT.resolve()):
            errors.append(f'Caminho fora do repositorio: {src}')
        elif not target.is_file():
            errors.append(f'Imagem nao encontrada: {src}')

    for path in ASSETS.rglob('*.svg'):
        try:
            tree = ET.parse(path)
            for node in tree.iter():
                if node.tag.rsplit('}', 1)[-1] in ('script','foreignObject'):
                    errors.append(f'SVG contem elemento potencialmente inseguro: {path.name}')
        except ET.ParseError as exc:
            errors.append(f'SVG invalido {path.name}: {exc}')
        if path.stat().st_size > 130_000:
            errors.append(f'SVG muito grande: {path.name}')

    for rel,expected in PINNED_SHA256.items():
        path = ASSETS / rel
        if not path.is_file():
            errors.append(f'Arquivo aprovado ausente: {rel}')
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected:
            errors.append(f'Arquivo aprovado alterado: {rel} (revisar versao antes de publicar)')
        if path.stat().st_size > 3_500_000:
            errors.append(f'Arquivo grande demais: {rel}')

    for script in ('generate_visuals.py','generate_hero.py'):
        if not (ROOT/'scripts'/script).is_file():
            errors.append(f'Script de geracao ausente: {script}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-logo', action='store_true', help='Compatibilidade com o publicador v2.3; validacao da marca agora e obrigatoria')
    parser.parse_args()
    errors = check()
    if errors:
        print('VALIDACAO REPROVADA:')
        for error in errors:
            print(' -', error)
        return 1
    print('OK: 5 secoes, 8 repositorios, 4 paineis expansivos e imagens locais.')
    print('OK: logomarca e hero aprovados, sem alteracoes (SHA-256).')
    print('AVISO: disponibilidade de URLs externas depende de verificacao remota.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
