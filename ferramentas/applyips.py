import sys
def apply_ips(rom, patch):
    d = bytearray(open(rom,'rb').read())
    p = open(patch,'rb').read()
    assert p[:5] == b'PATCH', 'no es IPS'
    i = 5
    while True:
        if p[i:i+3] == b'EOF': break
        off = int.from_bytes(p[i:i+3],'big'); i += 3
        size = int.from_bytes(p[i:i+2],'big'); i += 2
        if size == 0:  # RLE
            rle = int.from_bytes(p[i:i+2],'big'); i += 2
            val = p[i]; i += 1
            if off+rle > len(d): d.extend(b'\x00'*(off+rle-len(d)))
            d[off:off+rle] = bytes([val])*rle
        else:
            if off+size > len(d): d.extend(b'\x00'*(off+size-len(d)))
            d[off:off+size] = p[i:i+size]; i += size
    return bytes(d)
open(sys.argv[3],'wb').write(apply_ips(sys.argv[1], sys.argv[2]))
