import React, { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function App() {
  const [form, setForm] = useState({
    sepal_length: 5.1,
    sepal_width: 3.5,
    petal_length: 1.4,
    petal_width: 0.2
  })
  const [resp, setResp] = useState(null)
  const [error, setError] = useState(null)

  const onChange = e => {
    const { name, value } = e.target
    setForm(s => ({ ...s, [name]: parseFloat(value) }))
  }

  const predict = async () => {
    setError(null); setResp(null)
    try {
      const r = await fetch(`${API_BASE}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items: [form] })
      })
      if (!r.ok) throw new Error(await r.text())
      const data = await r.json()
      setResp(data)
    } catch (e) {
      setError(String(e))
    }
  }

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', maxWidth: 720, margin: '40px auto' }}>
      <h1>Iris AI Service Demo</h1>
      <p>Fill the inputs then click Predict. Open <a href={`${API_BASE}/docs`} target="_blank">Swagger</a> to explore the API.</p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
        {['sepal_length','sepal_width','petal_length','petal_width'].map(k => (
          <label key={k} style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            {k.replace('_',' ')}
            <input name={k} type="number" step="0.1" value={form[k]} onChange={onChange} />
          </label>
        ))}
      </div>

      <button onClick={predict} style={{ marginTop: 16, padding: '8px 16px', borderRadius: 8 }}>
        Predict
      </button>

      {error && <pre style={{ color: 'crimson', marginTop: 16 }}>{error}</pre>}
      {resp && (
        <pre style={{ background: '#f6f8fa', padding: 12, borderRadius: 8, marginTop: 16 }}>
{JSON.stringify(resp, null, 2)}
        </pre>
      )}
    </div>
  )
}
