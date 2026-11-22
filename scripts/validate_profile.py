"""Fail-closed offline checks for a GitHub profile README.

Run before publishing and in GitHub Actions. Does not request external URLs,
so its results are reproducible and do not require network access.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / 'README.md'
REQUIRED_REPOS = (
    'webhook-relay',
    'content-manager',
    'data-reconciliation',
    'approval-workflow',
    'operations-dashboard',
    'process-forge',
    'dispatch-planner',
    'commerce-control',
)
ASSETS = ROOT / 'assets' / 'profile'
BRAND = ASSETS / 'brand' / 'rafael-analyst-oficial.png'
BRAND_SHA256 = '0adf5742f1c31309a0ee640cfa4f3998274e2d1aae3f77206518b12ba39b2de5'


def inspect(require_logo: bool) -> list[str]:
    errors: list[str] = []
    if not README.is_file():
        return ['README.md ausente']

    content = README.read_text(encoding='utf-8')

    for slug in REQUIRED_REPOS:
        if f'https://github.com/RafaelEdrd/{slug}' not in content:
            errors.append(f'Repositorio ausente: {slug}')
        if not (ASSETS / 'cards' / f'{slug}.svg').is_file():
            errors.append(f'Card ausente: {slug}')

    if 'https://github.com/RafaelEdrd/conversa-studio' in content:
        errors.append('Conversa Studio continua sem verificacao publica: remova o link ate validar')

    if re.search(r'<\s*(script|iframe|object|embed)\b', content, re.I):
        errors.append('HTML executavel ou incorporado nao permitido no README')
    if 'javascript:' in content.lower():
        errors.append('Link javascript: nao permitido')
    if len(content.encode('utf-8')) > 180_000:
        errors.append('README muito extenso para leitura e manutencao')
    if content.count('<details>') != content.count('</details>') or content.count('<details>') < 3:
        errors.append('Blocos expansivos <details> inconsistentes')

    # Inspect image tags and all local paths, not just known assets.
    for img_src in re.findall(r'<(?:img|source)\s+[^>]*?(?:src|srcset)="([^"]+)"', content, re.I | re.S):
        if img_src.startswith(('https://', 'http://', 'data:')):
            continue
        if not img_src.startswith('./'):
            errors.append(f'Imagem local com caminho inesperado: {img_src}')
            continue
        target = (ROOT / img_src.removeprefix('./')).resolve()
        if not target.is_relative_to(ROOT.resolve()):
            errors.append(f'Imagem escapa da raiz do repositorio: {img_src}')
        elif not target.is_file() and (require_logo or target != BRAND):
            errors.append(f'Imagem nao encontrada: {img_src}')

    for path in ASSETS.rglob('*.svg'):
        try:
            ET.parse(path)
        except ET.ParseError as ex:
            errors.append(f'SVG invalido: {path.relative_to(ROOT)}: {ex}')
        if path.stat().st_size > 130_000:
            errors.append(f'SVG muito grande: {path.name}')

    for image in (ASSETS / 'hero.gif', ASSETS / 'hero-still.png', BRAND):
        if not image.is_file():
            errors.append(f'Asset essencial ausente: {image.relative_to(ROOT)}')
        elif image.stat().st_size > 3_500_000:
            errors.append(f'Asset excessivo: {image.relative_to(ROOT)}')

    if not (ROOT / 'scripts' / 'generate_visuals.py').is_file():
        errors.append('Gerador dos assets ausente')

    if require_logo and not BRAND.is_file():
        errors.append('Logomarca original ausente: assets/profile/brand/ra-original.png')

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-logo', action='store_true')
    args = parser.parse_args()
    errors = inspect(args.require_logo)
    if errors:
        print('ERRO NA VALIDACAO:')
        for message in errors:
            print(f' - {message}')
        return 1
    print('OK: README, 8 links, SVGs, GIF, marca, paths e interatividade verificados.')
    if not args.require_logo and not BRAND.exists():
        print('AVISO: logomarca original ausente; use o arquivo autorizado da marca.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
