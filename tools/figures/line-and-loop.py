# "The line and the loop" — after Anthropic's AI-Native SDLC playbook.
# Vendor-neutral: the hub reads "agents", not a product mark.
import math
W, H = 1000, 520
STAGES = ['Plan', 'Design', 'Build', 'Test', 'Deploy', 'Maintain']

o = [f'<svg class="diagram--loop2" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
     'aria-label="Left: the traditional lifecycle as a straight line, plan through maintain, where one loop back '
     'is a whole new release cycle. Right: the same six stages drawn as a ring around the agents that run them, '
     'turning in hours rather than weeks, with humans above the loop.">']
o.append('<defs><marker id="lah2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto-start-reverse"><path d="M0 1 L8 5 L0 9 Z" fill="#288CFF"/></marker>'
         '<marker id="lahd" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6.5" markerHeight="6.5" '
         'orient="auto-start-reverse"><path d="M0 1.6 L7.5 5 L0 8.4" fill="none" stroke="#8A8A8A" stroke-width="1.6"/></marker></defs>')

# ---- left: the line -------------------------------------------------
BW, BH, GAP = 296, 42, 26
x0, y0 = 20, 40
for i, s in enumerate(STAGES):
    y = y0 + i * (BH + GAP)
    o.append(f'<rect x="{x0}" y="{y}" width="{BW}" height="{BH}" rx="8" fill="#000000"/>')
    o.append(f'<text x="{x0+BW/2}" y="{y+27}" text-anchor="middle" font-family="Inter,system-ui,sans-serif" '
             f'font-size="15" font-weight="500" fill="#FFFFFF">{s}</text>')
    if i < len(STAGES) - 1:
        o.append(f'<path d="M {x0+BW/2} {y+BH+5} L {x0+BW/2} {y+BH+GAP-7}" stroke="#8A8A8A" stroke-width="1.5" '
                 'marker-end="url(#lahd)"/>')

o.append(f'<line x1="376" y1="26" x2="376" y2="{H-64}" stroke="#E4E4E4" stroke-width="1.5"/>')

# ---- right: the loop ------------------------------------------------
cx, cy, R, r = 700, 228, 170, 46
pts = []
for i, s in enumerate(STAGES):
    a = math.radians(-90 + i * 60)
    px, py = cx + R * math.cos(a), cy + R * math.sin(a)
    pts.append((px, py))
    o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="#000000"/>')

# arrows along the ring, trimmed clear of both circles
for i in range(6):
    a1 = -90 + i * 60
    # angular half-width the node circle subtends on the ring path
    d = math.degrees(math.asin(min(1, (r + 14) / (2 * R)))) + 1.5
    s1, s2 = math.radians(a1 + d), math.radians(a1 + 60 - d)
    x1, y1 = cx + R * math.cos(s1), cy + R * math.sin(s1)
    x2, y2 = cx + R * math.cos(s2), cy + R * math.sin(s2)
    o.append(f'<path d="M {x1:.1f} {y1:.1f} A {R} {R} 0 0 1 {x2:.1f} {y2:.1f}" fill="none" stroke="#288CFF" '
             'stroke-width="5" stroke-linecap="round" marker-end="url(#lah2)"/>')

o.append(f'<circle cx="{cx}" cy="{cy}" r="86" fill="#288CFF"/>')
o.append(f'<text x="{cx}" y="{cy+7}" text-anchor="middle" font-family="ui-monospace,\'JetBrains Mono\',Menlo,monospace" '
         'font-size="19" fill="#000000">agents</text>')
for i, s in enumerate(STAGES):
    px, py = pts[i]
    o.append(f'<text x="{px:.1f}" y="{py+6:.1f}" text-anchor="middle" font-family="Inter,system-ui,sans-serif" '
             f'font-size="15" font-weight="500" fill="#FFFFFF">{s}</text>')

SUB = [(x0, 'Traditional &#8212; the line.', 'One slow loop back is a new release cycle.'),
       (404, 'AI-native &#8212; the loop.', 'Hours, not weeks, with humans above the loop.')]
for sx, strong, rest in SUB:
    o.append(f'<text x="{sx}" y="{H-40}" font-family="Inter,system-ui,sans-serif" font-size="14.5" '
             f'font-weight="600" fill="#000000">{strong}</text>')
    o.append(f'<text x="{sx}" y="{H-19}" font-family="Inter,system-ui,sans-serif" font-size="14.5" '
             f'fill="#5C5C5C">{rest}</text>')
o.append('</svg>')
print('\n'.join(o))
