# -*- coding: utf-8 -*-
"""Parsea/reconstruye un .ext de Hextractor en unidades numeradas."""
import re

MARK = (';', '@', '|')

def parse(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    units = []   # (n, bloque, cabecera, [ (texto, lim) ], indice_linea_ini, indice_linea_fin)
    out = []     # estructura del fichero para reconstruir
    cur = None; i = 0; n = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('@'):
            cur = ln; out.append(('raw', ln)); i += 1; continue
        if ln.startswith(';'):
            hdr = ln
            buf = []; j = i + 1
            while j < len(lines) and not lines[j].startswith(MARK):
                buf.append(lines[j]); j += 1
            txt = '\n'.join(buf)
            parts = re.findall(r'(.*?)#(\d{3})', txt, re.S)
            item = {'n': n, 'blk': cur, 'hdr': hdr, 'parts': parts}
            units.append(item); out.append(('unit', item))
            n += 1; i = j; continue
        out.append(('raw', ln)); i += 1
    return units, out

def render(out):
    res = []
    for kind, v in out:
        if kind == 'raw':
            res.append(v)
        else:
            res.append(v['hdr'])
            res.append(''.join(t + '#' + l for t, l in v['parts']))
    return '\n'.join(res)
