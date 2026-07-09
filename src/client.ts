export class SearchLaneError extends Error {
  code?: string
  status?: number
  constructor(message: string, options?: { code?: string; status?: number }) {
    super(message)
    this.name = 'SearchLaneError'
    this.code = options?.code
    this.status = options?.status
  }
}

export class SearchLaneClient {
  private apiKey: string | undefined
  private baseUrl: string

  constructor(options: { apiKey?: string; baseUrl?: string } = {}) {
    this.apiKey = options.apiKey || process.env.TALOCODE_API_KEY
    this.baseUrl = (
      options.baseUrl ||
      process.env.TALOCODE_BASE_URL ||
      'https://api.talocode.site'
    ).replace(/\/+$/, '')
  }

  private async request<T>(method: string, path: string, body?: unknown): Promise<T> {
    const headers: Record<string, string> = { 'Content-Type': 'application/json' }
    if (this.apiKey) headers.Authorization = `Bearer ${this.apiKey}`
    const response = await fetch(`${this.baseUrl}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    })
    if (!response.ok) {
      const data = (await response.json().catch(() => ({}))) as { error?: string; code?: string }
      throw new SearchLaneError(data.error || `Request failed (${response.status})`, {
        code: data.code,
        status: response.status,
      })
    }
    return (await response.json()) as T
  }

  health() {
    return this.request<{ ok: boolean; service: string; version: string }>('GET', '/v1/searchlane/health')
  }
  pricing() {
    return this.request<Record<string, unknown>>('GET', '/v1/searchlane/pricing')
  }
  capabilities() {
    return this.request<Record<string, unknown>>('GET', '/v1/searchlane/capabilities')
  }
  query(input: { query?: string; q?: string; limit?: number }) {
    return this.request<Record<string, unknown>>('POST', '/v1/searchlane/query', input)
  }
  news(input: { query?: string; q?: string; limit?: number }) {
    return this.request<Record<string, unknown>>('POST', '/v1/searchlane/news', input)
  }
  research(input: { query?: string; q?: string; limit?: number; fetchPages?: boolean }) {
    return this.request<Record<string, unknown>>('POST', '/v1/searchlane/research', input)
  }
}

export function createSearchLaneClient(options?: { apiKey?: string; baseUrl?: string }) {
  return new SearchLaneClient(options)
}
