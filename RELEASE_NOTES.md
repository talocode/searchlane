## SearchLane v0.1.1 — Agent Web Search & Research

Structured web search, news, and multi-source research briefs with citations — built for AI agents and developers.

### Install (any device with Node 18+)

```bash
npm install -g @talocode/searchlane
# or one-liner
curl -fsSL https://raw.githubusercontent.com/talocode/searchlane/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/talocode/searchlane/main/install.ps1 | iex
```

Works on **Linux, macOS, Windows, Android (Termux), iOS (iSH / node), ChromeOS, WSL** via npm or the portable Node package.

### Standalone binaries (no Node required)

| Platform | Asset |
|----------|--------|
| Linux ARM64 | `searchlane-linux-arm64` / `searchlane-v0.1.1-linux-arm64.tar.gz` |
| Linux x64 | `searchlane-linux-x64` / `searchlane-v0.1.1-linux-x64.tar.gz` |
| macOS Intel | `searchlane-macos-x64` / `searchlane-v0.1.1-macos-x64.tar.gz` |
| macOS Apple Silicon | `searchlane-macos-arm64` / `searchlane-v0.1.1-macos-arm64.tar.gz` |
| Windows x64 | `searchlane-win-x64.exe` / `searchlane-v0.1.1-win-x64.tar.gz` |
| Portable (Node) | `searchlane-v0.1.1-portable-node.tar.gz` |

```bash
# Linux ARM64 example
curl -fsSL -o searchlane https://github.com/talocode/searchlane/releases/download/v0.1.1/searchlane-linux-arm64
chmod +x searchlane && sudo mv searchlane /usr/local/bin/
searchlane query --query "agent-native APIs"
```

### CLI

```bash
searchlane query --query "MCP tools for agents"
searchlane news --query "AI agents"
searchlane research --query "What is llms.txt?"
searchlane pricing
```

### Cloud API (Talocode)

```
POST /v1/searchlane/query      5 credits
POST /v1/searchlane/news       8 credits
POST /v1/searchlane/research  30 credits
```

Auth: `Authorization: Bearer $TALOCODE_API_KEY`

### Demo / launch video

- **searchlane-launch-video.mp4** — ~30s kinetic launch film (Hook → Reveal → Points → Proof → CTA)
- **searchlane-demo.mp4** — terminal-style product demo

Android / iOS: use `npm i -g @talocode/searchlane` or the **portable-node** tarball (Termux / iSH).

### Links

- npm: https://www.npmjs.com/package/@talocode/searchlane
- Repo: https://github.com/talocode/searchlane
- Cloud: https://api.talocode.site
