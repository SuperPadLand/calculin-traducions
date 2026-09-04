# -*- coding: utf-8 -*-
"""Ajusta la traduccion para que cada linea de pantalla mida lo mismo que en el original."""
import os, re
from chk import blen, load_tbl
# táboa de caracteres do xogo en galego: TBL=ruta/da.tbl python3 buildmap.py ...
VALID = load_tbl(os.environ.get('TBL', 'xogo_gl.tbl'))
SEP = re.compile(r'(?<!~)([=/])')

def split_seg(s):
    """divide en segmentos conservando separadores; ignora los = / dentro de ~XX~."""
    out = []; buf = ''; i = 0
    while i < len(s):
        m = re.match(r'~[0-9A-Fa-f]{2}~', s[i:])
        if m: buf += m.group(); i += len(m.group()); continue
        ch = s[i]
        if ch in '=/':
            out.append(buf); out.append(ch); buf = ''
        else:
            buf += ch
        i += 1
    out.append(buf)
    return out

def w(s): return blen(s.replace('\n',''), VALID, set())

def pad_to(seg, target):
    """ajusta un segmento a `target` bytes tocando solo espacios."""
    cur = w(seg)
    if cur == target: return seg, True
    if cur < target:
        m = re.search(r'( *)(\n*)$', seg)
        return seg[:m.start()] + m.group(1) + ' '*(target-cur) + m.group(2), True
    need = cur - target
    while need:
        runs = [m for m in re.finditer(r'  +', seg)]
        runs += [m for m in re.finditer(r' +(?=$|\n)', seg) if m not in runs]
        runs = sorted(set(runs), key=lambda m: m.end()-m.start(), reverse=True)
        if not runs: return seg, False
        m = runs[0]
        keep = 1 if m.end() < len(seg) and seg[m.end():].strip('\n') else 0
        avail = (m.end()-m.start()) - keep
        if avail <= 0: return seg, False
        take = min(need, avail)
        seg = seg[:m.start()] + seg[m.start()+take:]; need -= take
    return seg, True

def fit(es, gl, bad=None):
    if bad is not None: blen(gl.replace('\n',''), VALID, bad)
    a, b = split_seg(es), split_seg(gl)
    if len(a) == len(b) and all(x == y for x, y in zip(a[1::2], b[1::2])):
        out = []; ok = True
        for x, y in zip(a, b):
            if x in '=/': out.append(y); continue
            ny, good = pad_to(y, w(x)); ok &= good; out.append(ny)
        res = ''.join(out)
        if ok and w(res) == w(es): return res, 0
    # fallback: ajuste global por el final
    d = w(es) - w(gl)
    if d > 0:
        m = re.search(r'~FF~$', gl); pos = m.start() if m else len(gl)
        return gl[:pos] + ' '*d + gl[pos:], 0
    need = -d
    while need:
        runs = sorted(re.finditer(r'  +', gl), key=lambda m: m.end()-m.start(), reverse=True)
        if not runs: return gl, need
        m = runs[0]; take = min(need, (m.end()-m.start())-1)
        if take <= 0: return gl, need
        gl = gl[:m.start()] + gl[m.start()+take:]; need -= take
    return gl, 0
