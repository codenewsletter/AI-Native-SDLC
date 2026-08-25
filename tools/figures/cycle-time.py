# Cycle-time bars. Rows 1-2 follow Anthropic's AI-Native SDLC playbook;
# row 3 is this page's own correction and is labelled as such.
W, H = 1000, 424
X0, BH, GAP = 20, 46, 10
LAB = {'plan': 92, 'design': 110, 'test': 100, 'deploy': 110, 'maintain': 118}
BUILD_BIG, BUILD_SM, RECLAIM = 330, 16, 304

o = [f'<svg class="diagram--bars" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
     'aria-label="Three cycle-time rows drawn to one scale. Before agents, build is the widest stage. The promise: '
     'build collapses to a sliver and the rest of the cycle time is reclaimed. What teams see: the reclaimed time '
     'refills with queue in front of review, so the row ends exactly where the first one did.">']

def bar(x, w, y, label, fill, text, dash=None, stroke=None):
    # every stage bar carries a border, so the pale fill has a real edge
    # against the white card behind it
    if stroke is None and fill == '#E9F2FF':
        stroke = '#288CFF'
    d = f' stroke-dasharray="{dash}"' if dash else ''
    s = f' stroke="{stroke}" stroke-width="1.5"{d}' if stroke else ''
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" fill="{fill}"{s}/>']
    if label:
        g.append(f'<text x="{x+w/2:.1f}" y="{y+28}" text-anchor="middle" font-family="Inter,system-ui,sans-serif" '
                 f'font-size="14.5" font-weight="500" fill="{text}">{label}</text>')
    return ''.join(g)

def head(y, strong, rest):
    return (f'<text x="{X0}" y="{y}" font-family="Inter,system-ui,sans-serif" font-size="14.5">'
            f'<tspan font-weight="600" fill="#000000">{strong}</tspan>'
            f'<tspan fill="#5C5C5C"> {rest}</tspan></text>')

# row 1 — before agents
y = 44
o.append(head(y - 14, 'Before agents', '&#8212; every stage runs at human speed'))
x = X0
for k, lbl in [('plan','Plan'), ('design','Design')]:
    o.append(bar(x, LAB[k], y, lbl, '#E9F2FF', '#000000')); x += LAB[k] + GAP
o.append(bar(x, BUILD_BIG, y, 'Build', '#288CFF', '#000000')); x += BUILD_BIG + GAP
for k, lbl in [('test','Test'), ('deploy','Deploy'), ('maintain','Maintain')]:
    o.append(bar(x, LAB[k], y, lbl, '#E9F2FF', '#000000')); x += LAB[k] + GAP
END = x - GAP

# row 2 — the promise
y = 184
o.append(head(y - 14, 'The promise', '&#8212; build runs at agent speed, the cycle shortens'))
x = X0
for k, lbl in [('plan','Plan'), ('design','Design')]:
    o.append(bar(x, LAB[k], y, lbl, '#E9F2FF', '#000000')); x += LAB[k] + GAP
o.append(bar(x, BUILD_SM, y, '', '#288CFF', '#000000')); x += BUILD_SM + GAP
for k, lbl in [('test','Test'), ('deploy','Deploy'), ('maintain','Maintain')]:
    o.append(bar(x, LAB[k], y, lbl, '#E9F2FF', '#000000')); x += LAB[k] + GAP
o.append(bar(x, END - x, y, 'cycle time reclaimed', 'none', '#8A8A8A', dash='6 5', stroke='#C9C9C9'))

# row 3 — what teams see
y = 324
o.append(head(y - 14, 'What teams see', '&#8212; the reclaimed time refills with queue'))
x = X0
for k, lbl in [('plan','Plan'), ('design','Design')]:
    o.append(bar(x, LAB[k], y, lbl, '#E9F2FF', '#000000')); x += LAB[k] + GAP
o.append(bar(x, BUILD_SM, y, '', '#288CFF', '#000000')); x += BUILD_SM + GAP
o.append(bar(x, RECLAIM, y, 'queue', '#FDF0EE', '#BF2E1C', dash='6 5', stroke='#BF2E1C')); x += RECLAIM + GAP
for k, lbl in [('test','Test'), ('deploy','Deploy'), ('maintain','Maintain')]:
    o.append(bar(x, LAB[k], y, lbl, '#E9F2FF', '#000000')); x += LAB[k] + GAP

o.append(f'<line x1="{END+10}" y1="30" x2="{END+10}" y2="{H-16}" stroke="#D6D6D6" stroke-width="1.5" stroke-dasharray="4 5"/>')
o.append('</svg>')
print('\n'.join(o))
