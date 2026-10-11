#!/usr/bin/env bash
# Check everything the reel editor needs. Prints what's missing and how to fix it.
ok() { printf '  ✅ %s\n' "$1"; }
no() { printf '  ❌ %s\n     fix: %s\n' "$1" "$2"; MISSING=1; }
MISSING=0
echo "Reel editor check"

command -v ffmpeg >/dev/null && ok "ffmpeg" || no "ffmpeg" "macOS: brew install ffmpeg  ·  Windows: winget install ffmpeg"
command -v node >/dev/null && ok "Node.js $(node -v)" || no "Node.js" "install the LTS version from https://nodejs.org"
command -v python3 >/dev/null && ok "Python 3" || no "Python 3" "macOS: xcode-select --install  ·  others: https://python.org"

if ls ~/.claude/skills/hyperframes ~/.agents/skills/hyperframes >/dev/null 2>&1; then ok "HyperFrames skills"
else no "HyperFrames skills" "npx skills add heygen-com/hyperframes"; fi

ENG="$(cd "$(dirname "$0")/.." && pwd)/engine"
if [ -s "$ENG/gsap.min.js" ] && [ -s "$ENG/sfx/whoosh.wav" ]; then ok "reel template engine"
else bash "$(dirname "$0")/setup_engine.sh" >/dev/null 2>&1 && ok "reel template engine (just set up)" || no "reel template engine" "bash scripts/setup_engine.sh"; fi

HOME_DIR="${REELS_HOME:-$HOME/reels}"
if [ -f "$HOME_DIR/brand.json" ]; then
  ok "brand file ($HOME_DIR)"
  if python3 -c "import json,sys;sys.exit(0 if json.load(open('$HOME_DIR/brand.json')).get('capcut') else 1)"; then
    if [ -d "${CAPCUT_SKILLS_DIR:-/nonexistent}/capcut-stdraft-builder" ]; then ok "CapCut helper scripts"
    else no "CapCut helper scripts" "see references/capcut.md step 3 (set CAPCUT_SKILLS_DIR)"; fi
    claude mcp list 2>/dev/null | grep -q capcut_creation && ok "CapCut connector added" \
      || no "CapCut connector" "see references/capcut.md step 2"
  fi
else
  echo "  ➖ no brand file yet - the setup interview will make one"
fi

FREE_GB=$(df -Pk "$HOME" | awk 'NR==2{print int($4/1048576)}')
[ "$FREE_GB" -ge 10 ] && ok "${FREE_GB} GB free disk" || no "only ${FREE_GB} GB free disk" "free up 10+ GB (35+ GB for 4K)"

[ "$MISSING" = 0 ] && echo "All set." || echo "Fix the ❌ items, then run this again."
exit "$MISSING"
