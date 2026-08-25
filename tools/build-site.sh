#!/usr/bin/env bash
# Assembles the publishable site into _site/.
#
# Both netlify.toml and .github/workflows/netlify.yml call this, so a
# Git-linked Netlify build and a CI deploy always publish identical output.
set -euo pipefail

# The palette gate. Netlify's build images do not all ship a Python, so a
# missing interpreter must not fail a deploy — but when Python is there the
# check is enforced, and a failing colour pair stops the build.
if command -v python3 >/dev/null 2>&1; then
  echo "Checking palette contrast..."
  python3 tools/contrast.py
else
  echo "python3 not available in this build image — skipping the palette check."
fi

rm -rf _site
mkdir -p _site
cp index.html _site/
cp -r assets _site/

echo "Assembled _site:"
find _site -type f | sort
