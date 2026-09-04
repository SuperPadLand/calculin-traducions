# -*- coding: utf-8 -*-
"""Lee los map*.tsv, ajusta longitudes y escribe map_fitted.tsv"""
import ast, sys, re
from chk import blen
from fit import fit, VALID
pares = []
for f in sys.argv[1:]:
    for i, line in enumerate(open(f, encoding='utf-8'), 1):
        line = line.rstrip('\n')
        if not line.strip(): continue
        a, b = line.split('\t')
        pares.append((f, i, ast.literal_eval(a), ast.literal_eval(b)))
bad = set(); nfix = 0; nfail = 0
out = []
for f, i, es, gl in pares:
    tgt = blen(es.replace('\n',''), VALID, set())
    got = blen(gl.replace('\n',''), VALID, bad)
    if got != tgt:
        new, rest = fit(es, gl, bad)
        if rest:
            print(f'NO AJUSTABLE {f}:{i} faltan quitar {rest}\n   ES {es!r}\n   GL {gl!r}')
            nfail += 1; new = gl
        else:
            nfix += 1
            if abs(got-tgt) > 3:
                print(f'ajuste grande {f}:{i} ({got}->{tgt})\n   GL {new!r}')
        gl = new
    out.append((es, gl))
if bad: print('CARACTERES FUERA DE TABLA:', sorted(bad))
with open('map_fitted.tsv','w',encoding='utf-8') as fh:
    for es, gl in out: fh.write(f'{es!r}\t{gl!r}\n')
print(f'--- {len(out)} pares | {nfix} ajustados | {nfail} sin ajustar ---')
