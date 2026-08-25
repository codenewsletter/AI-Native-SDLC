#!/usr/bin/env python3
"""WCAG contrast checker for The Code palette.

Run:  python3 tools/contrast.py
Every colour pair the design depends on is asserted here, so a palette
change that breaks accessibility fails loudly instead of shipping.
"""
import sys

def lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lum(hexstr):
    h = hexstr.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

BG      = '#F9F9F9'
SURFACE = '#FFFFFF'
PRIMARY = '#288CFF'

PAIRS = [
    # (label, fg, bg, minimum required)
    ('ink on bg',                 '#000000', BG,      7.0),
    ('ink-2 (secondary) on bg',   '#3F3F3F', BG,      7.0),
    ('ink-3 (meta/mono) on bg',   '#5C5C5C', BG,      4.5),
    ('ink-3 on surface',          '#5C5C5C', SURFACE, 4.5),
    ('accent-ink (links) on bg',  '#0F6FDB', BG,      4.5),
    ('accent-ink on surface',     '#0F6FDB', SURFACE, 4.5),
    ('accent-ink-on-wash on wash','#0D66CC', '#E9F2FF', 4.5),
    ('ink on wash',               '#000000', '#E9F2FF', 7.0),
    ('alert on bg',               '#BF2E1C', BG,      4.5),
    ('alert on alert-wash',       '#BF2E1C', '#FDF0EE', 4.5),
    ('on-primary on primary',     '#FFFFFF', PRIMARY, 3.0),   # large/bold only
    ('primary fill vs bg',        PRIMARY,   BG,      3.0),   # non-text contrast
    ('border vs bg',              '#E4E4E4', BG,      1.0),   # decorative
]

fail = 0
print(f'{"pair":34} {"ratio":>7}  {"min":>5}  verdict')
print('-' * 62)
for label, fg, bg, need in PAIRS:
    r = ratio(fg, bg)
    ok = r >= need
    fail += not ok
    print(f'{label:34} {r:6.2f}:1  {need:5.1f}  {"ok" if ok else "FAIL"}')
print('-' * 62)
print('all pairs pass' if not fail else f'{fail} pair(s) FAILED')
sys.exit(1 if fail else 0)
