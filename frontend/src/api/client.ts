const BASE = '/api'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`)
  }
  return res.json()
}

export const api = {
  places: {
    list: (params: Record<string, string | number | undefined>) => {
      const qs = new URLSearchParams()
      Object.entries(params).forEach(([k, v]) => {
        if (v !== undefined && v !== null && v !== '') qs.set(k, String(v))
      })
      const q = qs.toString()
      return request<import('../types').Place[]>(`/places${q ? `?${q}` : ''}`)
    },
    detail: (id: number) =>
      request<import('../types').PlaceDetail>(`/places/${id}`),
  },
  ai: {
    search: (query: string, history: import('../types').ChatMessage[] = [], top_k = 5) =>
      request<import('../types').ChatResponse>('/ai/search', {
        method: 'POST',
        body: JSON.stringify({ query, history, top_k }),
      }),
    recommend: (query: string, history: import('../types').ChatMessage[] = [], top_k = 5) =>
      request<import('../types').ChatResponse>('/ai/recommend', {
        method: 'POST',
        body: JSON.stringify({ query, history, top_k }),
      }),
  },
}
