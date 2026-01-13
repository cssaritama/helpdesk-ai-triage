import React, { useEffect, useState } from 'react'
import { api } from '../api'
import { TicketsView } from './TicketsView'
import { KnowledgeBaseView } from './KnowledgeBaseView'

type Tab = 'tickets' | 'kb'

export function App() {
  const [tab, setTab] = useState<Tab>('tickets')
  const [health, setHealth] = useState<string>('unknown')

  useEffect(() => {
    api.health().then(r => setHealth(r.status)).catch(() => setHealth('error'))
  }, [])

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', margin: 24, maxWidth: 1100 }}>
      <header style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h2>Helpdesk AI Triage</h2>
        <div>Backend health: <b>{health}</b></div>
      </header>

      <nav style={{ marginTop: 16, marginBottom: 16, display: 'flex', gap: 12 }}>
        <button onClick={() => setTab('tickets')} disabled={tab === 'tickets'}>Tickets</button>
        <button onClick={() => setTab('kb')} disabled={tab === 'kb'}>Knowledge Base</button>
      </nav>

      {tab === 'tickets' ? <TicketsView /> : <KnowledgeBaseView />}
    </div>
  )
}
