import React, { useState } from 'react'

export default function KadastrForm({ onResult }) {
  const [parcel, setParcel] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleFetch(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const resp = await fetch(`/api/external/kadastr/${encodeURIComponent(parcel)}/`)
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
      <h3>Kadastr (Parcel)</h3>
      <form onSubmit={handleFetch}>
        <input value={parcel} onChange={(e) => setParcel(e.target.value)} placeholder="Enter parcel id e.g. UZ-ABC-100" />
        <button type="submit" disabled={loading || !parcel}>Fetch</button>
      </form>
      {error && <div className="error">{error}</div>}
    </div>
  )
}
