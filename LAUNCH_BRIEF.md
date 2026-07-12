# SearchLane launch brief

Used with Clueso skill **brief-to-launch-video**.

## Product
**SearchLane** — Agent Web Search & Research API

## Audience
AI agent builders, indie hackers, developers shipping agent tools

## Positioning
Credit-metered web search for agents: structured hits, news, research briefs with citations — not a raw model reseller.

## Key points
1. Structured search hits (title, url, snippet, score)
2. Research mode with multi-source dig + citations
3. REST + MCP + SDK + CLI; pay-per-call credits
4. Providers: Brave / Serper / DuckDuckGo fallback

## CTA
`npm i @talocode/searchlane` · github.com/talocode/searchlane

## Voiceover script (5–7 beats, ~30s)

| Beat | VO |
|------|-----|
| Hook | Agents don't need another chatbot. They need the web. Search is broken for machines. |
| Reveal | SearchLane — agent web search and research API, by Talocode. |
| Point 1 | Structured hits: title, URL, snippet, score. One CLI call. |
| Point 2 | Research mode digs sources and returns a brief with citations. |
| Point 3 | REST, MCP, SDK, CLI — credit-metered for agents. |
| Proof | Five credits to query. Eight for news. Thirty for research. |
| CTA | Ship search as a product. npm install at talocode slash searchlane. |

## Local render (no Clueso)
```bash
python3 scripts/generate-launch-video.py
# → release-assets/searchlane-launch-video.mp4
```
