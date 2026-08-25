#!/usr/bin/env python3
"""Inline index.html into one self-contained file.

    python3 tools/build-single.py dist/ai-native-sdlc.html

Local <link rel=stylesheet> and <script src> become <style>/<script>, and
assets/mark.svg becomes a data URI. Google Fonts stays a remote link — it is
the one external host an Artifact's CSP allows.

Pass --fragment to omit the <!DOCTYPE>/<html>/<head>/<body> shell, which is
what the Artifact publisher wants (it supplies its own).
"""
import base64, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / 'index.html').read_text()
fragment = '--fragment' in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith('--')]
out = pathlib.Path(args[0]) if args else ROOT / 'dist' / 'ai-native-sdlc.html'

def read(rel):
    return (ROOT / rel).read_text()

# stylesheets -> <style>
def inline_css(m):
    href = m.group(1)
    if href.startswith('http'):
        return m.group(0)
    return '<style>\n/* %s */\n%s</style>' % (href, read(href))
src = re.sub(r'<link rel="stylesheet" href="([^"]+)">', inline_css, src)

# scripts -> inline
def inline_js(m):
    return '<script>\n%s</script>' % read(m.group(1))
src = re.sub(r'<script src="([^"]+)"></script>', inline_js, src)

# favicon -> data URI
svg = base64.b64encode((ROOT / 'assets' / 'mark.svg').read_bytes()).decode()
src = src.replace('href="assets/mark.svg"', 'href="data:image/svg+xml;base64,%s"' % svg)

if fragment:
    src = re.sub(r'^.*?<head>\s*', '', src, flags=re.S)
    src = src.replace('</head>\n<body>', '').replace('</head>', '')
    src = re.sub(r'\s*</body>\s*</html>\s*$', '\n', src)
    # the charset/viewport metas are supplied by the publisher's own shell
    src = re.sub(r'<meta charset="utf-8">\n', '', src)
    src = re.sub(r'<meta name="viewport"[^>]*>\n', '', src)

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(src)
print('%s  %.1f KB' % (out, len(src) / 1024))
