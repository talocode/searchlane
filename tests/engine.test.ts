import { describe, it } from 'node:test'
import assert from 'node:assert/strict'
import {
  mockSearchResults,
  buildResearchAnswer,
  validatePublicUrl,
  getSearchLanePricing,
  getSearchLaneCapabilities,
  runSearchQuery,
  SEARCHLANE_VERSION,
} from '../src/engine.js'

void describe('searchlane engine', () => {
  void it('validatePublicUrl', () => {
    assert.equal(validatePublicUrl('https://example.com').hostname, 'example.com')
    assert.throws(() => validatePublicUrl('http://localhost/'), /private|localhost/i)
  })

  void it('mock results ranked', () => {
    const hits = mockSearchResults('agents', 4)
    assert.equal(hits.length, 4)
    assert.equal(hits[0].position, 1)
  })

  void it('research answer', () => {
    const hits = mockSearchResults('mcp tools', 2)
    const a = buildResearchAnswer('mcp tools', hits, [])
    assert.ok(a.includes('mcp tools'))
  })

  void it('pricing', () => {
    assert.equal(getSearchLanePricing().credits['searchlane.query'], 5)
    assert.equal(getSearchLaneCapabilities().version, SEARCHLANE_VERSION)
  })

  void it('runSearchQuery returns data', async () => {
    const res = await runSearchQuery('nodejs', { limit: 2 })
    assert.ok(res.results.length >= 1)
  })
})
