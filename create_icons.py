#!/usr/bin/env python3
"""Generate PWA icons for RAPH BRAIN Mobile — no dependencies required."""
import struct, zlib, math, os

# 8×9 "R" pixel-art bitmap (1 = white pixel)
R_MAP = [
    "11111110",
    "10000001",
    "10000001",
    "10000001",
    "11111110",
    "10001000",
    "10000100",
    "10000010",
    "10000001",
]
R_W, R_H = 8, 9

def in_R(nx, ny):
    row, col = int(ny * R_H), int(nx * R_W)
    if row < 0 or row >= R_H or col < 0 or col >= R_W:
        return False
    return R_MAP[row][col] == '1'

def make_pixel(x, y, size):
    cx = cy = size / 2
    acc = (214, 40, 40)
    bg  = (10, 10, 10)
    wht = (255, 255, 255)

    dist  = math.hypot(x - cx, y - cy)
    r     = size * 0.40
    edge  = max(1.0, size * 0.010)

    if dist > r + edge:
        return bg

    # Letter R centered in circle
    lh = size * 0.52
    lw = lh * R_W / R_H
    nx = (x - (cx - lw / 2)) / lw
    ny = (y - (cy - lh / 2)) / lh
    letter = (0.0 < nx < 1.0 and 0.0 < ny < 1.0 and in_R(nx, ny))

    color = wht if letter else acc

    # Anti-aliased circle edge
    alpha = max(0.0, min(1.0, (r + edge - dist) / (2 * edge)))
    if alpha >= 1.0:
        return color
    return tuple(round(color[i] * alpha + bg[i] * (1 - alpha)) for i in range(3))

def make_png(w, h, pixel_fn):
    def crc(d):
        return zlib.crc32(d) & 0xFFFFFFFF
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', crc(tag + data))

    ihdr = struct.pack('>II', w, h) + bytes([8, 2, 0, 0, 0])
    rows = bytearray()
    for y in range(h):
        rows.append(0)  # filter: None
        for x in range(w):
            rows.extend(pixel_fn(x, y))
    idat = zlib.compress(bytes(rows), 6)

    return (
        b'\x89PNG\r\n\x1a\n'
        + chunk(b'IHDR', ihdr)
        + chunk(b'IDAT', idat)
        + chunk(b'IEND', b'')
    )

os.makedirs('icons', exist_ok=True)
for sz in [180, 192, 512]:
    def fn(x, y, s=sz): return make_pixel(x, y, s)
    data = make_png(sz, sz, fn)
    path = f'icons/icon-{sz}.png'
    with open(path, 'wb') as f:
        f.write(data)
    print(f'  {path}  ({sz}×{sz}, {len(data)//1024}KB)')

print('Done.')
