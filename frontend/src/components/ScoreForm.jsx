import React, { useState } from 'react'

export default function ScoreForm({ onResult }) {
  const [kind, setKind] = useState('individual')
  const [payload, setPayload] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    let json
    try {
      json = payload ? JSON.parse(payload) : {}
    } catch (err) {
      setError('Invalid JSON payload')
      return
    }

    setLoading(true)
    try {
      const resp = await fetch(`/api/score/${kind}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(json),
      })
      const data = await resp.json()
      onResult({ status: resp.status, data })
    } catch (err) {
      setError(String(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card ai-card">
      <h3>AI Scoring</h3>
      <div className="muted">Choose model and provide JSON features</div>
      <form onSubmit={handleSubmit}>
        <select value={kind} onChange={(e) => setKind(e.target.value)}>
          <option value="individual">Individual</option>
          <option value="company">Company</option>
        </select>
        <textarea value={payload} onChange={(e) => setPayload(e.target.value)} placeholder='e.g. {"yearly_income":50000, "existing_debt":5000}' />
        <button type="submit" disabled={loading}>Predict risk</button>
      </form>
      {error && <div className="error">{error}</div>}
    </div>
  )
}
