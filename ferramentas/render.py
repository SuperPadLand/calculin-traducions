# -*- coding: utf-8 -*-
"""Dibuja texto con la fuente real de la ROM para revisar como se vera en pantalla.

Uso: python3 render.py <rom.nes> <tabla.tbl> <offset_fuente> <salida.png> "linea 1" ["linea 2" ...]
La fuente debe ser de tiles 1bpp de 8x8 (8 bytes por tile) a partir de <offset_fuente> (p. ej. 0x2F910).
Los codigos ~XX~ dentro de una linea pintan el tile XX directamente.
"""
import re
import sys
from PIL import Image, ImageDraw

ROM = open(sys.argv[1], 'rb').read()
BASE = int(sys.argv[3], 0)
tbl = {}
for line in open(sys.argv[2], encoding='utf-8'):
    line = line.rstrip('\n')
    if '=' in line:
        b, c = line.split('=', 1)
        if len(b) == 2:
            tbl[c] = int(b, 16)


def tile(idx):
    im = Image.new('L', (8, 8), 0)
    px = im.load()
    for y in range(8):
        b = ROM[BASE + idx * 8 + y]
        for x in range(8):
            if b & (0x80 >> x):
                px[x, y] = 255
    return im


def tokens(s):
    out = []
    i = 0
    while i < len(s):
        m = re.match(r'~([0-9A-Fa-f]{2})~', s[i:])
        if m:
            out.append(int(m.group(1), 16))
            i += len(m.group())
            continue
        out.append(tbl.get(s[i]))
        i += 1
    return out


def render(lines, title, path, cols=16, scale=4):
    h = len(lines)
    img = Image.new('RGB', (cols * 8 * scale, (h * 10 + 14) * scale), (16, 16, 30))
    d = ImageDraw.Draw(img)
    d.text((5, 4), title, fill=(255, 205, 110))
    for r, ln in enumerate(lines):
        for c, t in enumerate(tokens(ln)[:cols]):
            if t is None or t == 0xFF:
                continue
            g = tile(t).resize((8 * scale, 8 * scale), Image.NEAREST)
            img.paste(Image.new('RGB', g.size, (255, 255, 255)),
                      (c * 8 * scale, (14 + r * 10) * scale), g)
    img.save(path)
    return path


if __name__ == '__main__':
    lineas = sys.argv[5:]
    render(lineas, sys.argv[4], sys.argv[4], cols=max(len(l) for l in lineas))
    print('renderizado:', sys.argv[4])
