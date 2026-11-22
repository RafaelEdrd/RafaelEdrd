"""Regenerate ONLY the animated hero, using the official brand asset.

Optional command, not used by CI or the regular visual build. Fonts can render
slightly differently across platforms. The published, approved GIF and PNG are
versioned and must not be regenerated during routine profile refactoring.
"""
from __future__ import annotations

from pathlib import Path
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'profile'


def main() -> None:
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


    # Use the exact official horizontal RA + Rafael Analyst lockup in the hero.
    # Only whitespace is cropped before proportional scaling. The original asset is
    # byte-identical and kept separately under /brand/ for provenance.
    ORIGINAL_LOGO = ASSETS / 'brand' / 'rafael-analyst-oficial.png'
    if not ORIGINAL_LOGO.is_file():
        raise FileNotFoundError(f'Logomarca oficial ausente: {ORIGINAL_LOGO}')
    _official = Image.open(ORIGINAL_LOGO).convert('RGB')
    _luma = _official.convert('L').point(lambda v: 255 if v > 90 else 0)
    _bbox = _luma.getbbox()
    if not _bbox:
        raise RuntimeError('Nao foi possivel localizar a logomarca oficial')
    _logo_crop = _official.crop((max(0,_bbox[0]-8), max(0,_bbox[1]-8),
                                min(_official.width,_bbox[2]+8),
                                min(_official.height,_bbox[3]+8)))
    _logo_width = 302
    OFFICIAL_LOCKUP = _logo_crop.resize(
        (_logo_width, round(_logo_crop.height*_logo_width/_logo_crop.width)),
        Image.Resampling.LANCZOS,
    )
    # Draw shapes at native size with 16-color palette to keep animation compact.
    frames = []
    for frame in range(FPS):
        im = Image.new('RGB', (W,H), (8,11,16))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((3,3,W-4,H-4),radius=19,outline=(48,60,71),width=2)
        d.rectangle((0,0,W,3),fill=(94,149,128))
        # Subtle technical dotted canvas on the right, quiet around type.
        for gy in range(68,385,30):
            for gx in range(655,1150,30):
                d.ellipse((gx,gy,gx+2,gy+2), fill=(22,32,37))
        im.paste(OFFICIAL_LOCKUP, (40, 12))
        d.text((1160,29), 'PORTFÓLIO   /   2026',font=SMALL,fill=(125,139,151),anchor='ra')
        d.line((38,79,1161,79),fill=(40,50,60),width=2)
        d.text((38,120), 'Rafael',font=NAME,fill=(238,242,241))
        d.text((38,201), 'Eduardo',font=NAME,fill=(238,242,241))
        d.text((40,294), 'DESENVOLVEDOR DE SOLUÇÕES E AUTOMAÇÃO',font=LABEL,fill=GREEN_RGB)
        d.text((41,334), 'Sistemas web  /  Dados  /  Integrações',font=SUB,fill=(145,160,171))
        d.line((38,379,1160,379),fill=(40,50,60),width=2)
        d.text((41,396), 'RAFAELANALYST.COM.BR',font=SMALL,fill=(119,132,143))
        d.text((1160,396), 'REGRAS  /  TESTES  /  MANUTENÇÃO',font=SMALL,fill=(119,132,143),anchor='ra')
        # Schematic panel on the right.
        d.rounded_rectangle((687,110,1160,336),radius=13,fill=(13,19,24),outline=(46,59,67),width=2)
        d.text((713,132),'CONTROLE  /  EXECUÇÃO',font=SMALL,fill=(128,148,161))
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
    print('Generated: hero.gif, hero-still.png (approved hero may differ across font installations)')


if __name__ == '__main__':
    main()
