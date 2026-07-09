import { describe, it, before, after } from 'node:test'
import assert from 'node:assert/strict'
import http from 'node:http'

const PORT = 3049

function request(method: string, path: string, body?: unknown): Promise<{ status: number; data: unknown }> {
  return new Promise((resolve, reject) => {
    const req = http.request(
      {
        hostname: '127.0.0.1',
        port: PORT,
        path,
        method,
        headers: { 'Content-Type': 'application/json' },
      },
      (res) => {
        const chunks: Buffer[] = []
        res.on('data', (c) => chunks.push(c))
        res.on('end', () => {
          const raw = Buffer.concat(chunks).toString('utf-8')
          try {
            resolve({ status: res.statusCode || 0, data: JSON.parse(raw) })
          } catch {
            resolve({ status: res.statusCode || 0, data: raw })
          }
        })
      },
    )
    req.on('error', reject)
    if (body !== undefined) req.write(JSON.stringify(body))
    req.end()
  })
}

void describe('searchlane server', () => {
  let server: http.Server
  before(async () => {
    process.env.PORT = String(PORT)
    process.env.SEARCHLANE_ALLOW_LOCAL_UNAUTH = 'true'
    const mod = await import('../src/server.js')
    server = mod.server
    await new Promise<void>((r) => server.on('listening', r))
  })
  after(() => {
    server.close()
    delete process.env.PORT
    delete process.env.SEARCHLANE_ALLOW_LOCAL_UNAUTH
  })

  void it('health', async () => {
    const res = await request('GET', '/health')
    assert.equal(res.status, 200)
    assert.equal((res.data as { service: string }).service, 'searchlane')
  })

  void it('pricing', async () => {
    const res = await request('GET', '/v1/searchlane/pricing')
    assert.equal(res.status, 200)
    assert.equal((res.data as { credits: Record<string, number> }).credits['searchlane.query'], 5)
  })

  void it('query requires query', async () => {
    const res = await request('POST', '/v1/searchlane/query', {})
    assert.equal(res.status, 422)
  })

  void it('query works', async () => {
    const res = await request('POST', '/v1/searchlane/query', { query: 'hello', limit: 2 })
    assert.equal(res.status, 200)
    assert.ok(Array.isArray((res.data as { results: unknown[] }).results))
  })
})
