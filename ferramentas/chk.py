# -*- coding: utf-8 -*-
"""Verifica las longitudes de un .ext de Hextractor contando bytes segun la .tbl."""
import re, sys

def load_tbl(path):
    chars = set()
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if '=' not in line: continue
        b, c = line.split('=', 1)
        if len(b) == 2:
            chars.add(c)
    return chars

TOK = re.compile(r'~[0-9A-Fa-f]{2}~')

def blen(s, valid, bad):
    n = 0; i = 0
    while i < len(s):
        m = TOK.match(s, i)
        if m:
            n += 1; i = m.end(); continue
        ch = s[i]
        if ch not in valid: bad.add(ch)
        n += 1; i += 1
    return n

def check(ext, tbl):
    valid = load_tbl(tbl)
    lines = open(ext, encoding='utf-8').read().split('\n')
    errs = []; bad = set(); blocks = {}; cur = None
    i = 0; total = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('@'):
            cur = ln.split('-')[0][1:]; blocks[cur] = 0
        elif ln.startswith(';'):
            m = re.search(r'\}#(\d+)#(\d+)', ln)
            declared_off = ln[1:].split('{')[0]
            # recoger lineas de traduccion
            buf = []; j = i + 1
            while j < len(lines) and not lines[j].startswith((';', '@', '|')):
                buf.append(lines[j]); j += 1
            txt = ''.join(buf)
            for part in re.split(r'(#\d{3})', txt):
                pass
            # dividir en unidades por #NNN
            units = re.findall(r'(.*?)#(\d{3})', txt, re.S)
            consumed = ''.join(u[0] + '#' + u[1] for u in units)
            if consumed != txt:
                errs.append((cur, declared_off, 'RESTO SIN PARSEAR', repr(txt[len(consumed):])))
            for text, dec in units:
                got = blen(text, valid, bad)
                total += int(dec)
                blocks[cur] = blocks.get(cur, 0) + int(dec)
                if got != int(dec):
                    errs.append((cur, declared_off, f'declara {dec}', f'cuenta {got}: {text!r}'))
            i = j - 1
        elif ln.startswith('|'):
            want = int(ln[1:])
            if blocks.get(cur, 0) != want:
                errs.append((cur, '-', f'bloque declara |{want}', f'suma {blocks.get(cur,0)}'))
            blocks[cur] = 0
        i += 1
    return errs, bad, total

if __name__ == '__main__':
    errs, bad, total = check(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'xogo.tbl')
    if bad: print('CARACTERES FUERA DE TABLA:', sorted(bad))
    for e in errs: print(' | '.join(str(x) for x in e))
    print(f'--- {len(errs)} problemas | {total} bytes de texto ---')
