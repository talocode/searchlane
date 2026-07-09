import http from 'node:http'
import crypto from 'node:crypto'
import { config } from './config.js'
import { extractApiKey, validateApiKey, requireAuth } from './auth.js'
import { chargeCredits } from './billing.js'
import {
  SEARCHLANE_VERSION,
  runSearchQuery,
  runSearchNews,
  runResearch,
  getSearchLanePricing,
  getSearchLaneCapabilities,
} from './engine.js'

const CREDITS = { query: 5, news: 8, research: 30 } as const

function json(res: http.ServerResponse, status: number, data: unknown, requestId?: string) {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (requestId) headers['x-request-id'] = requestId
  res.writeHead(status, headers)
  res.end(JSON.stringify(data))
}

function readBody(req: http.IncomingMessage): Promise<string> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = []
    req.on('data', (c: Buffer) => chunks.push(c))
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf-8')))
    req.on('error', reject)
  })
}

async function handle(req: http.IncomingMessage, res: http.ServerResponse) {
  const requestId = crypto.randomUUID()
  try {
    const url = new URL(req.url || '/', `http://${req.headers.host || 'localhost'}`)
    const method = req.method || 'GET'
    const path = url.pathname

    if (method === 'GET' && (path === '/health' || path === '/v1/searchlane/health')) {
      return json(res, 200, {
        ok: true,
        service: 'searchlane',
        version: SEARCHLANE_VERSION,
        endpoints: getSearchLaneCapabilities().endpoints,
      }, requestId)
    }
    if (method === 'GET' && path === '/v1/searchlane/pricing') {
      return json(res, 200, getSearchLanePricing(), requestId)
    }
    if (method === 'GET' && path === '/v1/searchlane/capabilities') {
      return json(res, 200, getSearchLaneCapabilities(), requestId)
    }
    if (method !== 'POST') return json(res, 405, { error: 'Method not allowed' }, requestId)

    let body: Record<string, unknown>
    try {
      body = JSON.parse((await readBody(req)) || '{}')
    } catch {
      return json(res, 400, { error: 'Invalid JSON body' }, requestId)
    }

    let apiKey: string | null = null
    if (!config.allowLocalUnauth) {
      apiKey = requireAuth(req).key
    } else {
      apiKey = extractApiKey(req)
      if (apiKey && !validateApiKey(apiKey)) apiKey = null
    }
    if (apiKey) process.env.TALOCODE_API_KEY = apiKey

    const query =
      typeof body.query === 'string' ? body.query.trim() : typeof body.q === 'string' ? body.q.trim() : ''
    const limit = typeof body.limit === 'number' ? body.limit : undefined

    const bill = async (action: string, credits: number) => {
      if (!apiKey) return null
      const r = await chargeCredits(action, credits, { route: path, query })
      if (!r.success) {
        json(res, 402, { error: r.error, code: 'INSUFFICIENT_CREDITS' }, requestId)
        return false
      }
      return r
    }

    if (path === '/v1/searchlane/query') {
      if (!query) return json(res, 422, { error: 'query is required', code: 'VALIDATION_ERROR' }, requestId)
      const b = await bill('searchlane.query', CREDITS.query)
      if (b === false) return
      const result = await runSearchQuery(query, { limit })
      return json(res, 200, { ...result, creditsRemaining: b?.remainingCredits }, requestId)
    }
    if (path === '/v1/searchlane/news') {
      if (!query) return json(res, 422, { error: 'query is required', code: 'VALIDATION_ERROR' }, requestId)
      const b = await bill('searchlane.news', CREDITS.news)
      if (b === false) return
      const result = await runSearchNews(query, { limit })
      return json(res, 200, { ...result, creditsRemaining: b?.remainingCredits }, requestId)
    }
    if (path === '/v1/searchlane/research') {
      if (!query) return json(res, 422, { error: 'query is required', code: 'VALIDATION_ERROR' }, requestId)
      const b = await bill('searchlane.research', CREDITS.research)
      if (b === false) return
      const result = await runResearch(query, { limit, fetchPages: body.fetchPages !== false })
      return json(res, 200, { ...result, creditsRemaining: b?.remainingCredits }, requestId)
    }
    return json(res, 404, { error: 'Not found', code: 'NOT_FOUND' }, requestId)
  } catch (err: unknown) {
    const error = err as { status?: number; body?: string; message?: string }
    if (error.status && error.body) {
      res.writeHead(error.status, { 'Content-Type': 'application/json', 'x-request-id': requestId })
      res.end(error.body)
      return
    }
    return json(res, 500, { error: error.message || 'Internal error', code: 'INTERNAL_ERROR' }, requestId)
  }
}

const server = http.createServer(handle)
server.listen(config.port, '0.0.0.0', () => {
  console.log(`SearchLane server v${SEARCHLANE_VERSION} listening on 0.0.0.0:${config.port}`)
})
process.on('SIGTERM', () => server.close(() => process.exit(0)))
process.on('SIGINT', () => server.close(() => process.exit(0)))
export { server }
