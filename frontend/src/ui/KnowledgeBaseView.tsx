import React, { useEffect, useState } from 'react'
import { api } from '../api'

export function KnowledgeBaseView() {
  const [articles, setArticles] = useState<any[]>([])
  const [title, setTitle] = useState('Example KB Article')
  const [body, setBody] = useState('# Heading\n\nDetails...')
  const [tags, setTags] = useState('example,howto')

  const [query, setQuery] = useState('password reset')
  const [hits, setHits] = useState<any | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function refresh() {
    try {
      const res = await api.listArticles()
      setArticles(res)
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
      await api.createArticle({
        title,
        body_markdown: body,
        tags: tags.split(',').map(t => t.trim()).filter(Boolean)
      })
      await refresh()
    } catch (e: any) {
      setError(e.message)
    }
  }

  async function search() {
    setError(null)
    try {
      const r = await api.searchKb({ query, k: 5 })
      setHits(r)
    } catch (e: any) {
      setError(e.message)
    }
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '420px 1fr', gap: 16 }}>
      <section>
        <h3>Create Article</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Title" />
          <textarea value={body} onChange={e => setBody(e.target.value)} placeholder="Body (Markdown)" rows={6} />
          <input value={tags} onChange={e => setTags(e.target.value)} placeholder="tags,comma,separated" />
          <button onClick={create}>Create</button>
        </div>

        <h3 style={{ marginTop: 24 }}>Search</h3>
        <div style={{ display: 'flex', gap: 8 }}>
          <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search query" style={{ flex: 1 }} />
          <button onClick={search}>Search</button>
        </div>
        <pre style={{ marginTop: 12, background: '#f6f6f6', padding: 12, overflow: 'auto' }}>
          {hits ? JSON.stringify(hits, null, 2) : '—'}
        </pre>
      </section>

      <section>
        <h3>Articles</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {articles.map(a => (
            <div key={a.id} style={{ border: '1px solid #ccc', padding: 10 }}>
              <div><b>{a.title}</b></div>
              <div style={{ fontSize: 12, marginTop: 4 }}>Tags: {a.tags.join(', ')}</div>
              <pre style={{ marginTop: 8, whiteSpace: 'pre-wrap' }}>{a.body_markdown}</pre>
            </div>
          ))}
        </div>

        {error ? <div style={{ marginTop: 12, color: 'darkred' }}>{error}</div> : null}
      </section>
    </div>
  )
}
