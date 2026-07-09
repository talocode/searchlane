# SearchLane Windows Installer
$ErrorActionPreference = "Stop"
$REPO = "talocode/searchlane"
$VERSION = if ($env:SEARCHLANE_VERSION) { $env:SEARCHLANE_VERSION } else { "v0.1.1" }
$PKG = "@talocode/searchlane"

Write-Host "==> SearchLane Installer ($VERSION)" -ForegroundColor Cyan
Write-Host ""

$npm = Get-Command npm -ErrorAction SilentlyContinue
if ($npm) {
    Write-Host "==> Node.js detected — installing $PKG globally..." -ForegroundColor Green
    npm install -g $PKG
    Write-Host ""
    Write-Host "==> Done! Run: searchlane --help" -ForegroundColor Green
    exit 0
}

$asset = "searchlane-win-x64.exe"
$url = "https://github.com/$REPO/releases/download/$VERSION/$asset"
$dest = Join-Path $env:TEMP "searchlane.exe"
try {
    Write-Host "==> Downloading $asset..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing
    Write-Host ""
    Write-Host "==> Downloaded to $dest" -ForegroundColor Green
    Write-Host "    Move it to a folder on your PATH, or run it directly."
    exit 0
} catch {
    Write-Host "==> Binary download failed." -ForegroundColor Yellow
}

Write-Host "==> Install Node.js from https://nodejs.org then run:" -ForegroundColor Yellow
Write-Host "    npm install -g $PKG"
Write-Host ""
Write-Host "    Portable: https://github.com/$REPO/releases/download/$VERSION/searchlane-v$($VERSION.TrimStart('v'))-portable-node.tar.gz"
Write-Host "    Cloud:    https://api.talocode.site/v1/searchlane/health"
Write-Host "    GitHub:   https://github.com/$REPO"
exit 1
