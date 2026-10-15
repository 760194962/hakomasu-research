#!/usr/bin/env python3
"""Decrypt + decompress default.xex (XEX2, retail-encrypted, "basic" compression) to a raw image.

Usage:
  python3 xex_decrypt.py default.xex default.pe --key <32 hex chars, Xbox 360 retail XEX key>

The retail key is not included in this repository.
The output is the memory image loaded at 0x82000000 (file offset = VA - 0x82000000).
Requires: pip install cryptography
"""
import argparse
import struct

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('xex')
    ap.add_argument('out')
    ap.add_argument('--key', required=True)
    a = ap.parse_args()
    d = open(a.xex, 'rb').read()
    magic, flags, peoff, _res, secoff, optcnt = struct.unpack('>4sIIIII', d[:24])
    assert magic == b'XEX2'
    opts = dict(struct.unpack('>II', d[24 + 8 * i:32 + 8 * i]) for i in range(optcnt))
    fi = opts[0x3FF]                                   # file format info
    isz, enc, comp = struct.unpack('>IHH', d[fi:fi + 8])
    assert comp == 1, 'only basic compression is handled'
    session = Cipher(algorithms.AES(bytes.fromhex(a.key)), modes.ECB()).decryptor().update(d[secoff + 0x150:secoff + 0x160])
    data = d[peoff:]
    data = data[:len(data) // 16 * 16]
    dec = Cipher(algorithms.AES(session), modes.CBC(bytes(16))).decryptor().update(data) if enc else data
    out, pos = bytearray(), 0
    for i in range((isz - 8) // 8):
        ds, zs = struct.unpack('>II', d[fi + 8 + 8 * i:fi + 16 + 8 * i])
        out += dec[pos:pos + ds]
        pos += ds
        out += bytes(zs)
    assert out[:2] == b'MZ', 'wrong key?'
    open(a.out, 'wb').write(out)
    print('image size', hex(len(out)))


if __name__ == '__main__':
    main()
