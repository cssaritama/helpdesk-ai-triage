import React, { useEffect, useState } from 'react'
import { api } from '../api'

type Ticket = any

export function TicketsView() {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [selected, setSelected] = useState<Ticket | null>(null)

  const [title, setTitle] = useState('Payment failed')
  const [description, setDescription] = useState('My card payment is failing and I am frustrated.')
  const [email, setEmail] = useState('user@example.com')

  const [triage, setTriage] = useState<any | null>(null)
  const [reply, setReply] = useState<any | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function refresh() {
    try {
      const res = await api.listTickets()
      setTickets(res.items)
      if (selected) {
        const updated = res.items.find((t: any) => t.id === selected.id) || null
        setSelected(updated)
      }
    } catch (e: any) {
      setError(e.message)
    }
  }

  useEffect(() => {
    refresh()
  }, [])

  async function create() {
    setError(null)
    try {
      const t = await api.createTicket({ title, description, requester_email: email })
      await refresh()
      setSelected(t)
    } catch (e: any) {
      setError(e.message)
    }
  }

  async function runTriage() {
    if (!selected) return
    setError(null)
    try {
      const r = await api.runTriage(selected.id)
      setTriage(r)
    } catch (e: any) {
      setError(e.message)
    }
  }

  async function suggestReply() {
    if (!selected) return
    setError(null)
    try {
      const r = await api.suggestReply(selected.id)
      setReply(r)
    } catch (e: any) {
      setError(e.message)
    }
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '420px 1fr', gap: 16 }}>
      <section>
        <h3>Create Ticket</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Title" />
          <textarea value={description} onChange={e => setDescription(e.target.value)} placeholder="Description" rows={5} />
          <input value={email} onChange={e => setEmail(e.target.value)} placeholder="Requester email" />
          <button onClick={create}>Create</button>
        </div>

        <h3 style={{ marginTop: 24 }}>Tickets</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          {tickets.map((t: any) => (
            <button
              key={t.id}
              onClick={() => { setSelected(t); setTriage(null); setReply(null) }}
              style={{ textAlign: 'left', padding: 8, border: selected?.id === t.id ? '2px solid #000' : '1px solid #ccc' }}
            >
              <div><b>{t.title}</b></div>
              <div style={{ fontSize: 12 }}>Status: {t.status}</div>
            </button>
          ))}
        </div>
      </section>

      <section>
        <h3>Ticket Details</h3>
        {selected ? (
          <div>
            <div><b>{selected.title}</b></div>
            <div style={{ whiteSpace: 'pre-wrap', marginTop: 8 }}>{selected.description}</div>

            <div style={{ marginTop: 16, display: 'flex', gap: 10 }}>
              <button onClick={runTriage}>Run AI Triage</button>
              <button onClick={suggestReply}>Suggest Reply</button>
              <button onClick={refresh}>Refresh</button>
            </div>

            <div style={{ marginTop: 16 }}>
              <h4>Triage Result</h4>
              <pre style={{ background: '#f6f6f6', padding: 12, overflow: 'auto' }}>{triage ? JSON.stringify(triage, null, 2) : '—'}</pre>
            </div>

            <div style={{ marginTop: 16 }}>
              <h4>Suggested Reply</h4>
              <pre style={{ background: '#f6f6f6', padding: 12, overflow: 'auto' }}>{reply ? JSON.stringify(reply, null, 2) : '—'}</pre>
            </div>

          </div>
        ) : (
          <div>Select a ticket.</div>
        )}

        {error ? <div style={{ marginTop: 12, color: 'darkred' }}>{error}</div> : null}
      </section>
    </div>
  )
}
