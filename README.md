# SearchLane

**Agent web search & research API** — structured hits, news search, and multi-source research briefs with citations.

Part of [Talocode](https://docs.talocode.site). Hosted at `/v1/searchlane/*`.

## Install

```bash
npm install @talocode/searchlane
```

```bash
pip install talocode-searchlane
```

## SDK

```ts
import { SearchLaneClient } from '@talocode/searchlane'

const search = new SearchLaneClient({ apiKey: process.env.TALOCODE_API_KEY })
const hits = await search.query({ query: 'MCP agent tools', limit: 5 })
const brief = await search.research({ query: 'What is llms.txt?' })
```

### Cloud SDK

```ts
import { Talocode } from '@talocode/sdk'
const tc = new Talocode({ apiKey: process.env.TALOCODE_API_KEY })
await tc.searchlane.query({ query: 'geolane ai visibility' })
```

### Python

```python
from searchlane import SearchLaneClient

client = SearchLaneClient()  # TALOCODE_API_KEY
hits = client.query(query="MCP agent tools", limit=5)
brief = client.research(query="What is llms.txt?")
```

## CLI

```bash
npx searchlane query --query "open source AI tools"
npx searchlane news --query "AI agents"
npx searchlane research --query "agent-native APIs"
npx searchlane pricing
```

## Routes

| Method | Path | Credits |
|--------|------|---------|
| GET | `/v1/searchlane/health` | — |
| GET | `/v1/searchlane/pricing` | — |
| GET | `/v1/searchlane/capabilities` | — |
| POST | `/v1/searchlane/query` | 5 |
| POST | `/v1/searchlane/news` | 8 |
| POST | `/v1/searchlane/research` | 30 |

## Providers

1. **Brave** — set `BRAVE_API_KEY`
2. **Serper** — set `SERPER_API_KEY`
3. **DuckDuckGo** — free fallback
4. **mock** — offline / test fallback

## Local server

```bash
SEARCHLANE_ALLOW_LOCAL_UNAUTH=true pnpm dev
# http://0.0.0.0:3040
```

## Talocode ecosystem

Part of **[Talocode](https://github.com/talocode)** — open-source workflow layers for builders. Explore sibling projects:

| Project | What it is |
|---------|------------|
| **[ScreenLane](https://github.com/talocode/screenlane)** | Screen-aware voice command layer |
| **[Tera](https://github.com/talocode/tera)** | AI chat & assistant |
| **[Codra](https://github.com/talocode/codra)** | Local coding agent |
| **[GateLane](https://github.com/talocode/gatelane)** | MCP gateway & agent tool control plane |
| **[ContextLane](https://github.com/talocode/contextlane)** | Context ingestion for persistent agents |
| **[MemoryLane](https://github.com/talocode/memorylane)** | Persistent agent memory |
| **[SignalLane](https://github.com/talocode/signallane)** | X growth intelligence |
| **[ReplyLane](https://github.com/talocode/replylane)** | X reply opportunity intelligence |
| **[CrawlerLane](https://github.com/talocode/crawlerlane)** | Crawler / SEO intelligence |
| **[WebDataLane](https://github.com/talocode/webdatalane)** | Web extraction to structured data |
| **[SearchLane](https://github.com/talocode/searchlane)** | Search layer for agents **(this repo)** |
| **[InvoiceLane](https://github.com/talocode/invoicelane)** | Invoicing tools |
| **[GeoLane](https://github.com/talocode/geolane)** | Geo intelligence |
| **[UgcLane](https://github.com/talocode/ugclane)** | UGC workflows |
| **[OpenSourceLane](https://github.com/talocode/opensourcelane)** | Open-source distribution tools |
| **[StackLane](https://github.com/talocode/stacklane)** | Builder stack platform |
| **[Tradia](https://github.com/talocode/tradia)** | Trading intelligence |
| **[Agent Browser](https://github.com/talocode/agent-browser)** | Browser automation for agents |
| **[Talocode](https://github.com/talocode/talocode)** | Org home & control plane |
| **[Skills](https://github.com/talocode/skills)** | Shared agent skills |
| **[X Agent](https://github.com/talocode/x-agent)** | X automation agent |
| **[LaunchPix](https://github.com/talocode/launchpix)** | Launch tooling |
| **[ForgeCAD](https://github.com/talocode/forgecad)** | CAD workflows |
| **[WorkLane](https://github.com/talocode/worklane)** | Work automation |
| **[ClipLoop](https://github.com/talocode/cliploop)** | Clip / video loops |

MCP-compatible agents integrate via each product's MCP server where available ([Model Context Protocol](https://modelcontextprotocol.io/)).

More: [github.com/talocode](https://github.com/talocode) · [talocode.site](https://talocode.site) · [docs.talocode.site](https://docs.talocode.site)

## License

MIT
