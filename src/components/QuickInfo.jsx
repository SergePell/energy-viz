import { useState } from 'react'

// Wiederverwendbarer Info-Knopf (Details-on-Demand, Shneiderman).
export function QuickInfo({ titel, children }) {
  const [offen, setOffen] = useState(false)
  return (
    <span style={{ position: 'relative', display: 'inline-block' }}>
      <button onClick={() => setOffen(o => !o)} aria-label="Info"
        style={{ width: 20, height: 20, borderRadius: '50%', border: '1px solid var(--border)',
          background: 'var(--bg-elevated)', color: 'var(--text-secondary)', fontSize: 12,
          cursor: 'pointer', lineHeight: 1, padding: 0 }}>
        i
      </button>
      {offen && (
        <span style={{ position: 'absolute', top: 26, left: 0, zIndex: 20, width: 270,
          background: 'var(--bg-elevated)', border: '1px solid var(--border)', borderRadius: 8,
          padding: '10px 12px', fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.5,
          boxShadow: '0 4px 16px rgba(0,0,0,0.35)', fontWeight: 400, whiteSpace: 'normal' }}>
          {titel && <span style={{ display: 'block', fontWeight: 500, color: 'var(--text-primary)', marginBottom: 4 }}>{titel}</span>}
          {children}
        </span>
      )}
    </span>
  )
}
