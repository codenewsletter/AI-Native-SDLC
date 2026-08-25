# "Start anywhere" adoption map — after Anthropic's AI-Native SDLC playbook.
# Every connector is a cubic bezier computed from the two boxes it joins.
W, H = 1000, 800
ROW = {1: 78, 2: 254, 3: 414, 4: 556, 5: 678}
BH  = 54
PAD = 26                      # keeps the long sweeps inside the viewBox

top = [
    (72,  190, 'PLAN',   'Capture intent'),
    (278, 176, 'BUILD',  'CLAUDE.md'),
    (470, 176, 'TEST',   'Feedback loop'),
    (662, 150, 'DEPLOY', 'Hooks'),
    (828, 150, 'BUILD',  'Plan mode'),
]
mid = [
    ('skills',    228, 176, 'BUILD',   'Skills',               2),
    ('subagents', 438, 176, 'BUILD',   'Subagents',            2),
    ('evals',     648, 176, 'TEST',    'Evals',                2),
    ('reqs',      138, 232, 'DESIGN',  'Requirements &amp; design', 3),
    ('pr',        648, 176, 'DEPLOY',  'PR review',            3),
    ('cicd',      648, 176, 'DEPLOY',  'CI/CD',                4),
    ('loop',      618, 236, 'MAINTAIN','Closing the loop',     5),
]

B = {}
for i, (x, w, st, lb) in enumerate(top):
    B['t%d' % i] = {'x': x, 'w': w, 'y': ROW[1]}
for k, x, w, st, lb, row in mid:
    B[k] = {'x': x, 'w': w, 'y': ROW[row]}
for b in B.values():
    b['cx'] = b['x'] + b['w'] / 2
    b['top'] = b['y']
    b['bot'] = b['y'] + BH

def curve(a, b, bow=0.55):
    x1, y1 = B[a]['cx'], B[a]['bot']
    x2, y2 = B[b]['cx'], B[b]['top'] - 9
    dy = (y2 - y1) * bow
    return f'M {x1:.1f} {y1:.1f} C {x1:.1f} {y1+dy:.1f} {x2:.1f} {y2-dy:.1f} {x2:.1f} {y2:.1f}'

def sweep(a, b, side):
    """a long run down one margin — control points clamped inside the frame"""
    if side == 'L':
        x1, y1 = B[a]['x'] + 26, B[a]['bot']
        x2, y2 = B[b]['x'] - 9, B[b]['y'] + BH / 2
        c1x, c2x = PAD, PAD
    else:
        x1, y1 = B[a]['x'] + B[a]['w'] - 26, B[a]['bot']
        x2, y2 = B[b]['x'] + B[b]['w'] + 9, B[b]['y'] + BH / 2
        c1x, c2x = W - PAD, W - PAD
    return f'M {x1:.1f} {y1:.1f} C {c1x:.1f} {y1+90:.1f} {c2x:.1f} {y2-60:.1f} {x2:.1f} {y2:.1f}'

SOLID  = 'stroke="#5C5C5C" stroke-width="1.6" marker-end="url(#gah)"'
DOTTED = 'stroke="#A6A6A6" stroke-width="1.6" stroke-dasharray="2 5" marker-end="url(#gahd)"'

o = []
o.append(f'<svg class="diagram--graph" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         'aria-label="An adoption map. Five entry points sit on the top row — capture intent, a context file, a '
         'feedback loop, hooks, and plan mode — and each feeds downstream: into skills, subagents and evals, then '
         'requirements and design and PR review, then CI/CD, and finally closing the loop. Any entry point is a '
         'valid place to start.">')
o.append('<defs>'
         '<marker id="gah" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L8.5 5 L0 9 Z" fill="#5C5C5C"/></marker>'
         '<marker id="gahd" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L8.5 5 L0 9 Z" fill="#A6A6A6"/></marker>'
         '</defs>')

o.append('<g font-family="ui-monospace,\'JetBrains Mono\',Menlo,monospace" font-size="12" fill="#8A8A8A" letter-spacing="1.6">')
o.append(f'<text x="8" y="{ROW[1]-22}">1 &#183; START ANYWHERE</text>')
for r in (2, 3, 4, 5):
    o.append(f'<text x="8" y="{ROW[r]+34}">{r}</text>')
o.append('</g>')

o.append('<g fill="none">')
for a, b, kind in [('t0','reqs','s'), ('t1','skills','s'), ('t1','subagents','s'), ('t1','evals','s'),
                   ('t2','subagents','d'), ('t3','evals','s'), ('skills','reqs','s'),
                   ('evals','pr','s'), ('pr','cicd','s'), ('cicd','loop','s')]:
    o.append(f'<path d="{curve(a,b)}" {DOTTED if kind=="d" else SOLID}/>')
o.append(f'<path d="{curve("skills","pr",0.8)}" {DOTTED}/>')
o.append(f'<path d="{sweep("t0","loop","L")}" {SOLID}/>')
o.append(f'<path d="{sweep("t4","cicd","R")}" {SOLID}/>')
o.append('</g>')

def draw(x, w, row, stage, label, entry):
    """Entry points carry the ink; everything downstream of them recedes.

    The message of the figure is "any of these five is a valid place to
    start", so the five entry points are the solid blue row and the twelve
    downstream nodes are quiet outlines. Filling all seventeen made the
    downstream tree the loudest thing on the page, which is backwards."""
    y = ROW[row]
    if entry:
        fill, stroke, eyebrow, text = '#288CFF', '#288CFF', '#0A2340', '#000000'
    else:
        fill, stroke, eyebrow, text = '#FFFFFF', '#C9C9C9', '#5C5C5C', '#000000'
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{BH}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
            f'<text x="{x+16}" y="{y+21}" font-family="ui-monospace,\'JetBrains Mono\',Menlo,monospace" '
            f'font-size="10.5" font-weight="600" letter-spacing="1.6" fill="{eyebrow}">{stage}</text>'
            f'<text x="{x+16}" y="{y+42}" font-family="ui-monospace,\'JetBrains Mono\',Menlo,monospace" '
            f'font-size="15" fill="{text}">{label}</text></g>')

for x, w, st, lb in top:
    o.append(draw(x, w, 1, st, lb, True))
for k, x, w, st, lb, row in mid:
    o.append(draw(x, w, row, st, lb, False))

o.append('<g font-family="ui-monospace,\'JetBrains Mono\',Menlo,monospace" font-size="12" fill="#5C5C5C">')
o.append(f'<rect x="8" y="{H-30}" width="26" height="13" fill="#288CFF"/>')
o.append(f'<text x="42" y="{H-19}">entry point &#183; start at any one</text>')
o.append(f'<rect x="290" y="{H-30}" width="26" height="13" fill="#FFFFFF" stroke="#C9C9C9" stroke-width="1.5"/>')
o.append(f'<text x="324" y="{H-19}">follows from whichever you pick</text>')
o.append('</g>')
o.append('</svg>')
print('\n'.join(o))
