import crypto from 'node:crypto'
import { config } from './config.js'

export async function chargeCredits(
  action: string,
  credits: number,
  metadata?: Record<string, unknown>,
): Promise<{ success: boolean; remainingCredits?: number; error?: string }> {
  const apiKey = process.env.TALOCODE_API_KEY
  if (!apiKey) return { success: false, error: 'TALOCODE_API_KEY not configured' }

  try {
    const response = await fetch(`${config.talocodeBaseUrl}/api/v1/cloud/usage/charge`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
        'Idempotency-Key': crypto.randomUUID(),
      },
      body: JSON.stringify({
        product: 'searchlane',
        action,
        credits,
        metadata: { product: 'searchlane', action, credits, ...metadata },
      }),
    })
    if (response.status === 401) return { success: false, error: 'Invalid or expired TALOCODE_API_KEY' }
    if (response.status === 402) {
      const body = (await response.json().catch(() => ({}))) as { error?: string }
      return { success: false, error: body.error || 'Insufficient credits' }
    }
    if (!response.ok) {
      const body = (await response.json().catch(() => ({}))) as { error?: string }
      return { success: false, error: body.error || `Billing failed (${response.status})` }
    }
    const body = (await response.json().catch(() => ({}))) as {
      remainingCredits?: number
      remaining?: number
    }
    return { success: true, remainingCredits: body.remainingCredits ?? body.remaining }
  } catch (err) {
    return { success: false, error: err instanceof Error ? err.message : 'Billing request failed' }
  }
}
