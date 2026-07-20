import { useState, useRef, useEffect } from 'react'

// Deckendes Dropdown-Panel, unabhängig davon ob --bg-card selbst transparent ist.
const PANEL_BG = 'var(--bg-elevated)'
const HOVER_BG = '#1c1f2a'
const AKTIV_BG = '#242835'

// Dunkles, eigenes Dropdown (ersetzt das native <select>, dessen aufgeklappte Liste hell bleibt).
export function JahrDropdown({ wert, optionen, onChange }) {
  const [offen, setOffen] = useState(false)
  const ref = useRef(null)

  useEffect(() => {
    function ausserhalb(e) { if (ref.current && !ref.current.contains(e.target)) setOffen(false) }
    document.addEventListener('mousedown', ausserhalb)
    return () => document.removeEventListener('mousedown', ausserhalb)
  }, [])

  return (
    <span ref={ref} style={{ position: 'relative', display: 'inline-block' }}>
      <button onClick={() => setOffen(o => !o)} style={{
        fontSize: 12, padding: '3px 8px', borderRadius: 6, border: '1px solid var(--border)',
        background: PANEL_BG, color: 'var(--text-primary)', cursor: 'pointer',
        minWidth: 58, display: 'inline-flex', justifyContent: 'space-between', gap: 6, alignItems: 'center',
      }}>
        {wert}<span style={{ color: 'var(--text-muted)', fontSize: 10 }}>▾</span>
      </button>
      {offen && (
        <span style={{
          position: 'absolute', top: 28, left: 0, zIndex: 30, maxHeight: 220, overflowY: 'auto',
          background: PANEL_BG, border: '1px solid var(--border)', borderRadius: 8,
          boxShadow: '0 4px 16px rgba(0,0,0,0.55)', padding: 4, minWidth: 72,
        }}>
          {optionen.map(o => (
            <span key={o} onClick={() => { onChange(o); setOffen(false) }} style={{
              display: 'block', fontSize: 12, padding: '5px 10px', borderRadius: 5, cursor: 'pointer',
              color: o === wert ? 'var(--text-primary)' : 'var(--text-secondary)',
              background: o === wert ? AKTIV_BG : PANEL_BG,
            }}
              onMouseEnter={e => { if (o !== wert) e.currentTarget.style.background = HOVER_BG }}
              onMouseLeave={e => { if (o !== wert) e.currentTarget.style.background = PANEL_BG }}>
              {o}
            </span>
          ))}
        </span>
      )}
    </span>
  )
}
