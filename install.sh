#!/usr/bin/env bash
# SearchLane installer — Linux / macOS / Android (Termux) / ChromeOS / WSL
set -euo pipefail

REPO="talocode/searchlane"
VERSION="${SEARCHLANE_VERSION:-v0.1.1}"
PKG="@talocode/searchlane"

echo "==> SearchLane Installer ($VERSION)"
echo ""

OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

if command -v npm &>/dev/null; then
  echo "==> Node.js/npm detected — installing $PKG globally..."
  npm install -g "$PKG"
  echo ""
  echo "==> Done! Run: searchlane --help"
  echo "    Or: npx searchlane query --query \"agent tools\""
  exit 0
fi

asset=""
case "$OS/$ARCH" in
  linux/aarch64|linux/arm64) asset="searchlane-linux-arm64" ;;
  linux/x86_64|linux/amd64)  asset="searchlane-linux-x64" ;;
  darwin/arm64)              asset="searchlane-macos-arm64" ;;
  darwin/x86_64)             asset="searchlane-macos-x64" ;;
esac

if [[ -n "$asset" ]]; then
  echo "==> Downloading $asset..."
  url="https://github.com/$REPO/releases/download/$VERSION/$asset"
  dest="${TMPDIR:-/tmp}/searchlane"
  if curl -fsSL "$url" -o "$dest"; then
    chmod +x "$dest"
    echo ""
    echo "==> Downloaded to $dest"
    echo "    Install: sudo mv $dest /usr/local/bin/searchlane"
    echo "    Then:    searchlane --help"
    exit 0
  fi
  echo "==> Binary download failed; falling back to portable package guidance."
fi

echo "==> Install Node.js 18+, then:"
echo "    npm install -g $PKG"
echo ""
echo "    Portable (any OS with Node):"
echo "    https://github.com/$REPO/releases/download/$VERSION/searchlane-v${VERSION#v}-portable-node.tar.gz"
echo ""
echo "    Cloud API: https://api.talocode.site/v1/searchlane/health"
echo "    Docs: https://github.com/$REPO"
exit 1
