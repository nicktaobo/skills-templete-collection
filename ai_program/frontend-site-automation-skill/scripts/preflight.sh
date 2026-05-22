#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:-.}"
cd "$PROJECT_DIR"

echo "== Path =="
pwd -P

echo "== Tool versions =="
node -v || true
npm -v || true
git --version || true
npx wrangler --version || true

echo "== Git =="
git status --short || true

echo "== Package scripts =="
node -e 'const p=require("./package.json"); console.log(p.scripts||{})' 2>/dev/null || true

echo "== Risk scans =="
if command -v rg >/dev/null 2>&1; then
  rg 'dangerouslySetInnerHTML|output:\s*["'"'`]export["'"'`]|href="#"|Lorem ipsum|example.com|Your Company|NEXT_PUBLIC_.*SECRET|NEXT_PUBLIC_.*KEY' src app components package.json next.config.* wrangler.* 2>/dev/null || true
else
  grep -RInE 'dangerouslySetInnerHTML|output:\s*["'"'`]export["'"'`]|href="#"|Lorem ipsum|example.com|Your Company|NEXT_PUBLIC_.*SECRET|NEXT_PUBLIC_.*KEY' src app components package.json next.config.* wrangler.* 2>/dev/null || true
fi

echo "== Expected files =="
for f in src/app/page.tsx src/app/layout.tsx src/app/sitemap.ts src/app/robots.ts; do
  if [ -f "$f" ]; then echo "OK $f"; else echo "MISSING $f"; fi
done

echo "== Done =="
