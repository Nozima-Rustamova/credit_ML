import React, { useState } from 'react'

export default function ScoreForm({ onResult }) {
  const [kind, setKind] = useState('individual')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Individual fields
  const [yearlyIncome, setYearlyIncome] = useState('50000')
  const [existingDebt, setExistingDebt] = useState('5000')
  const [requestedAmount, setRequestedAmount] = useState('10000')
  const [collateralValue, setCollateralValue] = useState('0')
  const [creditHistoryScore, setCreditHistoryScore] = useState('650')
  const [criminalHistory, setCriminalHistory] = useState(false)

  // Company fields
  const [revenue, setRevenue] = useState('200000')
  const [netIncome, setNetIncome] = useState('30000')
  const [assets, setAssets] = useState('150000')
  const [liabilities, setLiabilities] = useState('50000')

  function numberOrNull(v) {
    if (v === null || v === undefined || v === '') return null
    const n = Number(v)
    return Number.isFinite(n) ? n : null
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)

    let features = {}

    if (kind === 'individual') {
      const yi = numberOrNull(yearlyIncome)
      const ed = numberOrNull(existingDebt)
      const ra = numberOrNull(requestedAmount)
      const cv = numberOrNull(collateralValue)
      const ch = numberOrNull(creditHistoryScore)
      if (yi === null) return setError('Yearly income must be a number')

      features = {
        yearly_income: yi,
        existing_debt: ed,
        requested_amount: ra,
        collateral_value: cv,
        credit_history_score: ch,
        criminal_history: !!criminalHistory,
      }
    } else {
      const r = numberOrNull(revenue)
      const ni = numberOrNull(netIncome)
      const a = numberOrNull(assets)
      const l = numberOrNull(liabilities)
      if (r === null) return setError('Revenue must be a number')

      features = { revenue: r, net_income: ni, assets: a, liabilities: l }
    }

    setLoading(true)
    try {
      const resp = await fetch(`/api/score/${kind}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(features),
      })
      const data = await resp.json()
      onResult({ status: resp.status, data })
    } catch (err) {
      setError(String(err))
    } finally {
      setLoading(false)
    }
  }

  function renderIndividual() {
    return (
      <>
        <label>Yearly income</label>
        <input type="number" value={yearlyIncome} onChange={(e) => setYearlyIncome(e.target.value)} />

        <label>Existing debt</label>
        <input type="number" value={existingDebt} onChange={(e) => setExistingDebt(e.target.value)} />

        <label>Requested amount</label>
        <input type="number" value={requestedAmount} onChange={(e) => setRequestedAmount(e.target.value)} />

        <label>Collateral value</label>
        <input type="number" value={collateralValue} onChange={(e) => setCollateralValue(e.target.value)} />

        <label>Credit history score</label>
        <input type="number" value={creditHistoryScore} onChange={(e) => setCreditHistoryScore(e.target.value)} />

        <label>
          <input type="checkbox" checked={criminalHistory} onChange={(e) => setCriminalHistory(e.target.checked)} /> Criminal history
        </label>
      </>
    )
  }

  function renderCompany() {
    return (
      <>
        <label>Revenue</label>
        <input type="number" value={revenue} onChange={(e) => setRevenue(e.target.value)} />

        <label>Net income</label>
        <input type="number" value={netIncome} onChange={(e) => setNetIncome(e.target.value)} />

        <label>Assets</label>
        <input type="number" value={assets} onChange={(e) => setAssets(e.target.value)} />

        <label>Liabilities</label>
        <input type="number" value={liabilities} onChange={(e) => setLiabilities(e.target.value)} />
      </>
    )
  }

  return (
    <div className="card ai-card">
      <h3>AI Scoring</h3>
      <div className="muted">Choose model and enter numeric features</div>

      <form onSubmit={handleSubmit}>
        <select value={kind} onChange={(e) => setKind(e.target.value)}>
          <option value="individual">Individual</option>
          <option value="company">Company</option>
        </select>

        <div className="fields">
          {kind === 'individual' ? renderIndividual() : renderCompany()}
        </div>

        <button type="submit" disabled={loading}>{loading ? 'Predicting…' : 'Predict risk'}</button>
      </form>

      {error && <div className="error">{error}</div>}
    </div>
  )
}
