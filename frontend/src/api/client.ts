import type { paths } from './schema'

export type TicketOut = paths['/tickets']['post']['responses']['200']['content']['application/json']
export type TicketListOut = paths['/tickets']['get']['responses']['200']['content']['application/json']
export type KBArticleOut = paths['/kb/articles']['get']['responses']['200']['content']['application/json'][number]

export class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl.replace(/\/$/, '')
  }

  private async request<T>(path: string, init?: RequestInit): Promise<T> {
    const res = await fetch(`${this.baseUrl}${path}`, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        ...(init?.headers || {})
      }
    })
    if (!res.ok) {
      const text = await res.text()
      throw new Error(`HTTP ${res.status}: ${text}`)
    }
    return res.json() as Promise<T>
  }

  health(): Promise<{ status: string }> {
    return this.request('/health')
  }

  createTicket(payload: { title: string; description: string; requester_email?: string | null }): Promise<TicketOut> {
    return this.request('/tickets', { method: 'POST', body: JSON.stringify(payload) })
  }

  listTickets(status?: string): Promise<TicketListOut> {
    const qs = status ? `?status=${encodeURIComponent(status)}` : ''
    return this.request(`/tickets${qs}`)
  }

  getTicket(ticketId: string): Promise<TicketOut> {
    return this.request(`/tickets/${ticketId}`)
  }

  runTriage(ticketId: string) {
    return this.request(`/tickets/${ticketId}/triage`, { method: 'POST' })
  }

  suggestReply(ticketId: string) {
    return this.request(`/tickets/${ticketId}/suggest-reply`, { method: 'POST' })
  }

  listArticles(): Promise<KBArticleOut[]> {
    return this.request('/kb/articles')
  }

  createArticle(payload: { title: string; body_markdown: string; tags?: string[] }): Promise<KBArticleOut> {
    return this.request('/kb/articles', { method: 'POST', body: JSON.stringify(payload) })
  }

  searchKb(payload: { query: string; k?: number }) {
    return this.request('/kb/search', { method: 'POST', body: JSON.stringify(payload) })
  }
}
