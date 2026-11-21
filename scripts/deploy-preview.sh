#!/usr/bin/env bash
#
# Deploy the PawWatch site to Cloudflare Pages as a PREVIEW.
#
# Preview only. This does NOT touch paw-watch.app. Production waits for
# John saying "ship it".
#
# The deploy goes to the branch `preview`, not to `main`, so it lands
# on a preview alias and the production branch is untouched.
#
# Usage:
#   bash scripts/deploy-preview.sh
#
# It reads CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID from the
# active Hermes profile's .env. It never prints either value.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITE="$(cd "$HERE/.." && pwd)"
PROJECT="pawwatch-site"
BRANCH="preview"

# Python is a native Windows program, so it cannot be given an MSYS
# path. The shell's /c/Users/... form is not a path Windows
# understands, and Python reports the file as missing even though the
# shell can read it. cygpath converts the path to the Windows form.
PYTHON_SCRIPT="$(cygpath -w "$HERE/verify_site.py" 2>/dev/null || echo "$HERE/verify_site.py")"
DIST_PATH="$(cygpath -w "$SITE/dist" 2>/dev/null || echo "$SITE/dist")"

ENV_FILE="${CLOUDFLARE_ENV_FILE:-$HOME/AppData/Local/hermes/.env}"
if [ ! -f "$ENV_FILE" ] && [ -f "$HOME/.hermes/.env" ]; then
  ENV_FILE="$HOME/.hermes/.env"
fi

read_env_key() {
  local key="$1" file="$2" line
  line="$(grep -E "^${key}=" "$file" 2>/dev/null | tail -1 || true)"
  [ -z "$line" ] && return 1
  line="${line#*=}"
  line="${line%\"}"; line="${line#\"}"
  line="${line%\'}"; line="${line#\'}"
  printf '%s' "$line"
}

echo "== PawWatch site, preview deploy =="
echo "   project: $PROJECT"
echo "   branch:  $BRANCH (preview, not production)"
echo "   NOT touching paw-watch.app"
echo

if [ ! -f "$ENV_FILE" ]; then
  echo "FAIL: no .env at $ENV_FILE"
  exit 1
fi

CLOUDFLARE_API_TOKEN="$(read_env_key CLOUDFLARE_API_TOKEN "$ENV_FILE" || true)"
CLOUDFLARE_ACCOUNT_ID="$(read_env_key CLOUDFLARE_ACCOUNT_ID "$ENV_FILE" || true)"

if [ -z "${CLOUDFLARE_API_TOKEN:-}" ]; then
  echo "FAIL: CLOUDFLARE_API_TOKEN is not set in $ENV_FILE"
  echo "      Nothing was deployed."
  exit 1
fi
if [ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]; then
  echo "FAIL: CLOUDFLARE_ACCOUNT_ID is not set in $ENV_FILE"
  echo "      Nothing was deployed."
  exit 1
fi
echo "   credentials found in $ENV_FILE (values not shown)"
echo

# --- Build -------------------------------------------------------------------

echo "-- building --"
cd "$SITE"
npm run build 2>&1 | tail -15
echo

if [ ! -d "$SITE/dist" ]; then
  echo "FAIL: the build produced no dist directory. Nothing was deployed."
  exit 1
fi

echo "-- checking the built site --"
if ! python "$PYTHON_SCRIPT" "$DIST_PATH"; then
  echo ""
  echo "FAIL: the site check failed. Nothing was deployed."
  exit 1
fi
echo

# --- Deploy ------------------------------------------------------------------

echo "-- deploying to Cloudflare Pages (preview branch) --"
cd "$SITE"

export CLOUDFLARE_API_TOKEN
export CLOUDFLARE_ACCOUNT_ID
export CLOUDFLARE_ACCOUNT_NAME="Cerminara Consulting"

npx --yes wrangler@latest pages deploy dist \
  --project-name="$PROJECT" \
  --branch="$BRANCH" \
  --commit-message="PawWatch preview: self-hosted fonts, home page at /, PawWatch name" \
  2>&1 | tail -20

echo
echo "== done =="
echo "   preview alias: https://$BRANCH.$PROJECT.pages.dev"
echo "   paw-watch.app was not touched"
