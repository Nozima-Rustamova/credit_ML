import React, { useState } from 'react'

export default function SoliqForm({ onResult }) {
  const [inn, setInn] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleFetch(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const resp = await fetch(`/api/external/soliq/${encodeURIComponent(inn)}/`)
      const data = await resp.json()
      onResult({ status: resp.status, data })
    } catch (err) {
      setError(String(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h3>Soliq (INN)</h3>
      <form onSubmit={handleFetch}>
        <input value={inn} onChange={(e) => setInn(e.target.value)} placeholder="Enter INN e.g. 123456789" />
        <button type="submit" disabled={loading || !inn}>Fetch</button>
      </form>
      {error && <div className="error">{error}</div>}
    </div>
  )
}
