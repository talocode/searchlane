# SearchLane (Python)

Agent web search & research API — structured hits, news search, and multi-source research briefs with citations.

Part of [Talocode](https://docs.talocode.site). Hosted at `/v1/searchlane/*`.

## Install

```bash
pip install talocode-searchlane
```

## Usage

```python
from searchlane import SearchLaneClient

client = SearchLaneClient(api_key="your_talocode_key")
# or: export TALOCODE_API_KEY=...

hits = client.query(query="MCP agent tools", limit=5)
news = client.news(query="AI agents", limit=5)
brief = client.research(query="What is llms.txt?", fetch_pages=True)
```

## CLI

```bash
export TALOCODE_API_KEY=...
searchlane health
searchlane pricing
searchlane query --query "open source AI tools"
searchlane news --query "AI agents"
searchlane research --query "agent-native APIs"
```

## Auth & base URL

| Env | Default |
|-----|---------|
| `TALOCODE_API_KEY` | — |
| `TALOCODE_BASE_URL` | `https://api.talocode.site` |

## Routes / credits

| Method | Path | Credits |
|--------|------|---------|
| GET | `/v1/searchlane/health` | — |
| GET | `/v1/searchlane/pricing` | — |
| GET | `/v1/searchlane/capabilities` | — |
| POST | `/v1/searchlane/query` | 5 |
| POST | `/v1/searchlane/news` | 8 |
| POST | `/v1/searchlane/research` | 30 |

## License

MIT
