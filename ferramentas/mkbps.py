# -*- coding: utf-8 -*-
"""Genera un parche BPS (con checksums CRC32) entre dos ficheros del mismo tamano o no."""
import sys, zlib


def varint(n):
    out = bytearray()
    while True:
        x = n & 0x7F
        n >>= 7
        if n == 0:
            out.append(0x80 | x)
            break
        out.append(x)
        n -= 1
    return bytes(out)


def make(src_path, dst_path, out_path, metadata=b''):
    src = open(src_path, 'rb').read()
    dst = open(dst_path, 'rb').read()
    body = bytearray()
    body += b'BPS1'
    body += varint(len(src)) + varint(len(dst)) + varint(len(metadata)) + metadata

    i = 0
    n = len(dst)
    while i < n:
        same = i < len(src) and dst[i] == src[i]
        j = i
        while j < n and ((j < len(src) and dst[j] == src[j]) == same) and \
              (same or not (j < len(src) and dst[j] == src[j])):
            j += 1
        run = j - i
        if same:                      # SourceRead
            body += varint(((run - 1) << 2) | 0)
        else:                         # TargetRead (literales)
            body += varint(((run - 1) << 2) | 1)
            body += dst[i:j]
        i = j

    body += zlib.crc32(src).to_bytes(4, 'little')
    body += zlib.crc32(dst).to_bytes(4, 'little')
    body += zlib.crc32(bytes(body)).to_bytes(4, 'little')
    open(out_path, 'wb').write(bytes(body))
    return len(body)


def apply_bps(src_path, patch_path):
    """Aplica el parche para comprobar que es correcto."""
    src = open(src_path, 'rb').read()
    p = open(patch_path, 'rb').read()
    assert p[:4] == b'BPS1'
    pos = 4

    def rv():
        nonlocal pos
        data = 0; shift = 1
        while True:
            x = p[pos]; pos += 1
            data += (x & 0x7F) * shift
            if x & 0x80:
                break
            shift <<= 7
            data += shift
        return data

    ssize, tsize, msize = rv(), rv(), rv()
    pos += msize
    assert ssize == len(src), 'tamano de origen distinto'
    out = bytearray(); so = to = 0
    end = len(p) - 12
    while pos < end:
        cmd = rv()
        action, length = cmd & 3, (cmd >> 2) + 1
        if action == 0:
            out += src[len(out):len(out) + length]
        elif action == 1:
            out += p[pos:pos + length]; pos += length
        elif action == 2:
            so += (-1 if rv() & 1 else 1) * 0  # no usado
        else:
            to += 0
    assert len(out) == tsize, f'tamano destino {len(out)} != {tsize}'
    assert zlib.crc32(bytes(out)) == int.from_bytes(p[-8:-4], 'little'), 'crc destino mal'
    assert zlib.crc32(src) == int.from_bytes(p[-12:-8], 'little'), 'crc origen mal'
    assert zlib.crc32(p[:-4]) == int.from_bytes(p[-4:], 'little'), 'crc parche mal'
    return bytes(out)


if __name__ == '__main__':
    size = make(sys.argv[1], sys.argv[2], sys.argv[3],
                sys.argv[4].encode('utf-8') if len(sys.argv) > 4 else b'')
    print(f'{sys.argv[3]}: {size} bytes')
    res = apply_bps(sys.argv[1], sys.argv[3])
    assert res == open(sys.argv[2], 'rb').read(), 'el parche no reproduce el destino'
    print('BPS verificado: reproduce la ROM destino y los tres CRC32 cuadran')
