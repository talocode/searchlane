# SearchLane

**Agent web search & research API** — structured hits, news search, and multi-source research briefs with citations.

Part of [Talocode](https://docs.talocode.site). Hosted at `/v1/searchlane/*`.

## Install

```bash
npm install @talocode/searchlane
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

## License

MIT
