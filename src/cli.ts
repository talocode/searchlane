#!/usr/bin/env node
import { runSearchQuery, runSearchNews, runResearch, getSearchLanePricing, getSearchLaneCapabilities } from './engine.js'

function usage(): never {
  console.error(`SearchLane — Agent Web Search & Research

Usage:
  searchlane query --query "..." [--limit 8]
  searchlane news --query "..." [--limit 8]
  searchlane research --query "..." [--limit 6] [--no-fetch]
  searchlane pricing
  searchlane capabilities
  searchlane --help
`)
  process.exit(1)
}

function parseArgs() {
  const args = process.argv.slice(2)
  if (!args.length || args[0] === '--help' || args[0] === '-h') usage()
  const command = args[0]
  const out: Record<string, string> = { command }
  for (let i = 1; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2)
      const val = args[i + 1]
      if (val && !val.startsWith('--')) {
        out[key] = val
        i++
      } else out[key] = 'true'
    }
  }
  return out
}

async function main() {
  try {
    const a = parseArgs()
    const q = a.query || a.q || ''
    const limit = a.limit ? Number(a.limit) : undefined
    switch (a.command) {
      case 'query': {
        if (!q) throw new Error('--query is required')
        process.stdout.write(JSON.stringify(await runSearchQuery(q, { limit }), null, 2) + '\n')
        break
      }
      case 'news': {
        if (!q) throw new Error('--query is required')
        process.stdout.write(JSON.stringify(await runSearchNews(q, { limit }), null, 2) + '\n')
        break
      }
      case 'research': {
        if (!q) throw new Error('--query is required')
        process.stdout.write(
          JSON.stringify(
            await runResearch(q, { limit, fetchPages: a['no-fetch'] !== 'true' }),
            null,
            2,
          ) + '\n',
        )
        break
      }
      case 'pricing':
        process.stdout.write(JSON.stringify(getSearchLanePricing(), null, 2) + '\n')
        break
      case 'capabilities':
        process.stdout.write(JSON.stringify(getSearchLaneCapabilities(), null, 2) + '\n')
        break
      default:
        usage()
    }
  } catch (err) {
    console.error(`Error: ${err instanceof Error ? err.message : String(err)}`)
    process.exit(1)
  }
}

main()
