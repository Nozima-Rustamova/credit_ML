import React, { useState } from 'react'
import SoliqForm from './components/SoliqForm'
import KadastrForm from './components/KadastrForm'
import ScoreForm from './components/ScoreForm'

export default function App() {
  const [lastResult, setLastResult] = useState(null)

  return (
    <div className="app">
      <header>
        <h1>credit_ML — AI Risk Assistant</h1>
        <p>Interactively fetch external records and let the scoring engine predict credit risk.</p>
      </header>

      <main>
        <div className="forms">
          <div className="left">
            <SoliqForm onResult={setLastResult} />
            <KadastrForm onResult={setLastResult} />
          </div>
          <div className="right">
            <ScoreForm onResult={setLastResult} />
          </div>
        </div>

        <section className="result">
          <h2>Last result</h2>
          {lastResult ? (
            lastResult.data && typeof lastResult.data.score === 'number' ? (
              <div className="score-card">
                <div className="score-value">{lastResult.data.score}</div>
                <div className="score-meta">model: {lastResult.data.model_version || 'rule/v1'}</div>
                <pre>{JSON.stringify(lastResult.data.explanation || lastResult.data, null, 2)}</pre>
              </div>
            ) : (
              <pre>{JSON.stringify(lastResult, null, 2)}</pre>
            )
          ) : (
            <p>No result yet.</p>
          )}
        </section>
      </main>

      <footer>
        <small>Frontend (Vite + React) - proxying /api to Django dev server</small>
      </footer>
    </div>
  )
}
