#!/usr/bin/env bash
# Build SearchLane multi-platform release assets (disk-conscious)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

VERSION="${VERSION:-0.1.1}"
NODE_VERSION="${NODE_VERSION:-24.15.0}"
OUT="$ROOT/release-assets"
CACHE="$ROOT/.cache/node-bins"
mkdir -p "$OUT" "$CACHE" "$ROOT/dist"

echo "==> Building TypeScript"
npm run build

echo "==> Bundling CLI (CJS for SEA)"
npx --yes esbuild src/cli.ts \
  --bundle --platform=node --format=cjs --target=node18 \
  --outfile=dist/cli.bundle.cjs --legal-comments=none

printf '%s\n' '#!/usr/bin/env node' | cat - dist/cli.bundle.cjs > dist/searchlane-portable.cjs
chmod +x dist/searchlane-portable.cjs

cat > sea-config.json <<EOF
{
  "main": "dist/cli.bundle.cjs",
  "output": "sea-prep.blob",
  "disableExperimentalSEAWarning": true,
  "useSnapshot": false,
  "useCodeCache": false
}
EOF

echo "==> Generating SEA blob"
node --experimental-sea-config sea-config.json

PLATFORMS=(
  "linux-arm64|searchlane-linux-arm64|linux"
  "linux-x64|searchlane-linux-x64|linux"
  "darwin-x64|searchlane-macos-x64|darwin"
  "darwin-arm64|searchlane-macos-arm64|darwin"
  "win-x64|searchlane-win-x64.exe|win"
)

download_and_inject() {
  local platform="$1" asset="$2" family="$3"
  local bin="$OUT/$asset"
  echo "--> $asset ($platform)"
  if [[ -f "$bin" ]]; then
    echo "  exists, skip"
    return 0
  fi

  if [[ "$platform" == win-x64 ]]; then
    local zip="$CACHE/node-win.zip"
    curl -fsSL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-win-x64.zip" -o "$zip"
    rm -rf "$CACHE/w" && mkdir -p "$CACHE/w"
    unzip -q -o "$zip" -d "$CACHE/w"
    cp "$CACHE/w/node-v${NODE_VERSION}-win-x64/node.exe" "$bin"
    rm -rf "$CACHE/w" "$zip"
  else
    local tgz="$CACHE/node.tgz"
    curl -fsSL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-${platform}.tar.gz" -o "$tgz"
    rm -rf "$CACHE/n" && mkdir -p "$CACHE/n"
    tar -xzf "$tgz" -C "$CACHE/n"
    cp "$CACHE/n/node-v${NODE_VERSION}-${platform}/bin/node" "$bin"
    rm -rf "$CACHE/n" "$tgz"
  fi
  chmod +x "$bin" 2>/dev/null || true

  if [[ "$family" == darwin ]]; then
    npx --yes postject "$bin" NODE_SEA_BLOB sea-prep.blob \
      --sentinel-fuse NODE_SEA_FUSE_fce680ab2cc467b6e072b8b5df1996b2 \
      --macho-segment-name NODE_SEA
  else
    npx --yes postject "$bin" NODE_SEA_BLOB sea-prep.blob \
      --sentinel-fuse NODE_SEA_FUSE_fce680ab2cc467b6e072b8b5df1996b2
  fi

  case "$platform" in
    linux-arm64) tar -C "$OUT" -czf "$OUT/searchlane-v${VERSION}-linux-arm64.tar.gz" "$asset" ;;
    linux-x64)   tar -C "$OUT" -czf "$OUT/searchlane-v${VERSION}-linux-x64.tar.gz" "$asset" ;;
    darwin-x64)  tar -C "$OUT" -czf "$OUT/searchlane-v${VERSION}-macos-x64.tar.gz" "$asset" ;;
    darwin-arm64) tar -C "$OUT" -czf "$OUT/searchlane-v${VERSION}-macos-arm64.tar.gz" "$asset" ;;
    win-x64)     tar -C "$OUT" -czf "$OUT/searchlane-v${VERSION}-win-x64.tar.gz" "$asset" ;;
  esac
  echo "  ok $(du -h "$bin" | cut -f1)  free=$(df -h / | awk 'NR==2{print $4}')"
}

for entry in "${PLATFORMS[@]}"; do
  IFS='|' read -r platform asset family <<< "$entry"
  download_and_inject "$platform" "$asset" "$family"
done

# Portable Node package
PORTABLE_DIR="$OUT/searchlane-portable"
rm -rf "$PORTABLE_DIR" && mkdir -p "$PORTABLE_DIR"
cp dist/searchlane-portable.cjs "$PORTABLE_DIR/searchlane.js"
cat > "$PORTABLE_DIR/package.json" <<EOF
{"name":"searchlane-cli","version":"${VERSION}","bin":{"searchlane":"./searchlane.js"},"private":true}
EOF
cat > "$PORTABLE_DIR/searchlane" <<'EOF'
#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec node "$SCRIPT_DIR/searchlane.js" "$@"
EOF
cat > "$PORTABLE_DIR/searchlane.cmd" <<'EOF'
@echo off
node "%~dp0searchlane.js" %*
EOF
chmod +x "$PORTABLE_DIR/searchlane" "$PORTABLE_DIR/searchlane.js"
(cd "$OUT" && tar -czf "searchlane-v${VERSION}-portable-node.tar.gz" searchlane-portable)

cp "$ROOT/install.sh" "$ROOT/install.ps1" "$OUT/"
echo "==> Assets:"
ls -lh "$OUT"
echo DONE
