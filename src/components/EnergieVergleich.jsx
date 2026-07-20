import { useMemo, useState } from 'react'
import { useJson } from '../hooks/useJson'
import { JahrDropdown } from './JahrDropdown'

const FORMEN = [
  { key: 'Laufwasser', farbe: '#4c9be0' },
  { key: 'Speicher', farbe: '#2b6cb0' },
  { key: 'Kernkraft', farbe: '#8a6fbf' },
  { key: 'Thermisch', farbe: '#b0552f' },
  { key: 'Andere', farbe: '#9aa0a6' },
  { key: 'Wind', farbe: '#6fc3b8' },
  { key: 'Photovoltaik', farbe: '#efb23a' },
]

const MONATE = [
  'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
  'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember',
]

// Aggregiert energiemix_monat.json entweder auf einen einzelnen Monat oder ein ganzes Jahr
function aggregieren(data, jahr, monat, modus) {
  const summen = Object.fromEntries(FORMEN.map(f => [f.key, 0]))
  if (!data) return { summen, total: 0 }

  const gefiltert = data.filter(d => {
    const t = new Date(d.date)
    if (t.getUTCFullYear() !== jahr) return false
    if (modus === 'monat' && (t.getUTCMonth() + 1) !== monat) return false
    return true
  })

  for (const d of gefiltert) {
    for (const f of FORMEN) summen[f.key] += d[f.key] || 0
  }
  const total = Object.values(summen).reduce((s, v) => s + v, 0)
  return { summen, total }
}

function MonatDropdown({ wert, onChange }) {
  const [offen, setOffen] = useState(false)
  return (
    <span style={{ position: 'relative', display: 'inline-block' }}>
      <button onClick={() => setOffen(o => !o)} style={{
        fontSize: 12, padding: '3px 8px', borderRadius: 6, border: '1px solid var(--border)',
        background: 'var(--bg-elevated)', color: 'var(--text-primary)', cursor: 'pointer',
        minWidth: 90, display: 'inline-flex', justifyContent: 'space-between', gap: 6, alignItems: 'center',
      }}>
        {MONATE[wert - 1]}<span style={{ color: 'var(--text-muted)', fontSize: 10 }}>▾</span>
      </button>
      {offen && (
        <span style={{
          position: 'absolute', top: 28, left: 0, zIndex: 30, maxHeight: 300, overflowY: 'auto',
          background: 'var(--bg-elevated)', border: '1px solid var(--border)', borderRadius: 8,
          boxShadow: '0 4px 16px rgba(0,0,0,0.55)', padding: 4, minWidth: 110,
        }}>
          {MONATE.map((m, i) => (
            <span key={m} onClick={() => { onChange(i + 1); setOffen(false) }} style={{
              display: 'block', fontSize: 12, padding: '5px 10px', borderRadius: 5, cursor: 'pointer',
              color: (i + 1) === wert ? 'var(--text-primary)' : 'var(--text-secondary)',
              background: (i + 1) === wert ? '#242835' : 'var(--bg-elevated)',
            }}
              onMouseEnter={e => { if ((i + 1) !== wert) e.currentTarget.style.background = '#1c1f2a' }}
              onMouseLeave={e => { if ((i + 1) !== wert) e.currentTarget.style.background = 'var(--bg-elevated)' }}>
              {m}
            </span>
          ))}
        </span>
      )}
    </span>
  )
}

export function EnergieVergleich() {
  const { data } = useJson('/data/energiemix_monat.json')
  const [modus, setModus] = useState('monat') // 'monat' oder 'jahr'
  const [jahrA, setJahrA] = useState(2021)
  const [monatA, setMonatA] = useState(7)
  const [jahrB, setJahrB] = useState(2024)
  const [monatB, setMonatB] = useState(7)

  const jahre = useMemo(() => {
    if (!data) return [2000, 2024]
    const alle = [...new Set(data.map(d => new Date(d.date).getUTCFullYear()))].sort((a, b) => a - b)
    return alle
  }, [data])

  const aggA = useMemo(() => aggregieren(data, jahrA, monatA, modus), [data, jahrA, monatA, modus])
  const aggB = useMemo(() => aggregieren(data, jahrB, monatB, modus), [data, jahrB, monatB, modus])

  if (!data) return <p style={{ color: 'var(--text-muted)' }}>Lade Daten…</p>

  // Skala für Balken: grösster Wert aus beiden Perioden
  const maxWert = Math.max(
    ...FORMEN.map(f => Math.max(aggA.summen[f.key], aggB.summen[f.key])),
    1,
  )

  // Sortiert nach Grösse in Periode B (die "spätere") für stabile Reihenfolge
  const traegerSortiert = [...FORMEN].sort((a, b) => aggB.summen[b.key] - aggB.summen[a.key])

  const labelA = modus === 'monat' ? `${MONATE[monatA - 1]} ${jahrA}` : `${jahrA}`
  const labelB = modus === 'monat' ? `${MONATE[monatB - 1]} ${jahrB}` : `${jahrB}`

  return (
    <div>
      {/* Auswahlleiste */}
      <div style={{
        display: 'flex', gap: 12, marginBottom: 20, alignItems: 'center', flexWrap: 'wrap',
        padding: '10px 12px', border: '1px solid var(--border)', borderRadius: 6,
      }}>
        {/* Modus-Toggle */}
        <div style={{ display: 'flex', gap: 0, border: '1px solid var(--border)', borderRadius: 6, overflow: 'hidden' }}>
          {['monat', 'jahr'].map(m => (
            <button key={m} onClick={() => setModus(m)}
              style={{
                fontSize: 12, padding: '4px 12px', border: 'none', cursor: 'pointer',
                background: modus === m ? '#242835' : 'var(--bg-elevated)',
                color: modus === m ? 'var(--text-primary)' : 'var(--text-muted)',
                fontWeight: modus === m ? 500 : 400,
              }}>
              {m === 'monat' ? 'Monat' : 'Jahr'}
            </button>
          ))}
        </div>

        {/* Auswahl A */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ fontSize: 11, color: 'var(--text-muted)', letterSpacing: '0.08em', textTransform: 'uppercase' }}>A</span>
          <JahrDropdown wert={jahrA} optionen={jahre} onChange={setJahrA} />
          {modus === 'monat' && <MonatDropdown wert={monatA} onChange={setMonatA} />}
        </div>

        <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>vs.</span>

        {/* Auswahl B */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ fontSize: 11, color: 'var(--text-muted)', letterSpacing: '0.08em', textTransform: 'uppercase' }}>B</span>
          <JahrDropdown wert={jahrB} optionen={jahre} onChange={setJahrB} />
          {modus === 'monat' && <MonatDropdown wert={monatB} onChange={setMonatB} />}
        </div>
      </div>

      {/* Gesamtsummen-KPIs */}
      <div style={{ display: 'flex', gap: 16, marginBottom: 20, flexWrap: 'wrap' }}>
        <div style={{
          border: '1px solid var(--border)', borderRadius: 8, padding: '12px 16px', minWidth: 160,
          background: 'var(--bg-elevated)',
        }}>
          <div style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>A</div>
          <div style={{ fontSize: 14, color: 'var(--text-secondary)', marginBottom: 4 }}>{labelA}</div>
          <div style={{ fontSize: 22, fontWeight: 500, color: 'var(--text-primary)' }}>
            {(aggA.total / 1000).toFixed(1)} TWh
          </div>
        </div>
        <div style={{
          border: '1px solid var(--border)', borderRadius: 8, padding: '12px 16px', minWidth: 160,
          background: 'var(--bg-elevated)',
        }}>
          <div style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>B</div>
          <div style={{ fontSize: 14, color: 'var(--text-secondary)', marginBottom: 4 }}>{labelB}</div>
          <div style={{ fontSize: 22, fontWeight: 500, color: 'var(--text-primary)' }}>
            {(aggB.total / 1000).toFixed(1)} TWh
          </div>
        </div>
        <div style={{
          border: '1px solid var(--border)', borderRadius: 8, padding: '12px 16px', minWidth: 160,
          background: 'var(--bg-elevated)',
        }}>
          <div style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Delta B − A</div>
          <div style={{ fontSize: 14, color: 'var(--text-secondary)', marginBottom: 4 }}>Gesamt</div>
          {(() => {
            const delta = aggB.total - aggA.total
            const proz = aggA.total > 0 ? (delta / aggA.total) * 100 : 0
            const farbe = delta >= 0 ? '#efb23a' : '#4c9be0'
            return (
              <div style={{ fontSize: 22, fontWeight: 500, color: farbe }}>
                {delta >= 0 ? '+' : '−'}{Math.abs(delta / 1000).toFixed(1)} TWh
                <span style={{ fontSize: 13, marginLeft: 8, color: farbe }}>
                  ({delta >= 0 ? '+' : '−'}{Math.abs(proz).toFixed(1)}%)
                </span>
              </div>
            )
          })()}
        </div>
      </div>

      {/* Vergleichs-Tabelle je Träger */}
      <div>
        <div style={{
          display: 'grid',
          gridTemplateColumns: '110px 1fr 90px 1fr 90px 110px',
          gap: 12, alignItems: 'center', fontSize: 10, color: 'var(--text-muted)',
          textTransform: 'uppercase', letterSpacing: '0.08em',
          paddingBottom: 6, borderBottom: '1px solid var(--border)',
        }}>
          <span>Energieträger</span>
          <span style={{ textAlign: 'right' }}>A ({labelA})</span>
          <span style={{ textAlign: 'right' }}>GWh</span>
          <span>B ({labelB})</span>
          <span>GWh</span>
          <span style={{ textAlign: 'right' }}>Delta</span>
        </div>

        {traegerSortiert.map(f => {
          const a = aggA.summen[f.key]
          const b = aggB.summen[f.key]
          const delta = b - a
          const proz = a > 0 ? (delta / a) * 100 : (b > 0 ? Infinity : 0)
          const anteilA = maxWert > 0 ? (a / maxWert) * 100 : 0
          const anteilB = maxWert > 0 ? (b / maxWert) * 100 : 0
          const deltaFarbe = delta >= 0 ? '#efb23a' : '#4c9be0'

          return (
            <div key={f.key} style={{
              display: 'grid',
              gridTemplateColumns: '110px 1fr 90px 1fr 90px 110px',
              gap: 12, alignItems: 'center',
              padding: '10px 0', borderBottom: '1px solid var(--border)',
            }}>
              <span style={{ fontSize: 13, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: 6 }}>
                <span style={{ width: 10, height: 10, borderRadius: 2, background: f.farbe }} />
                {f.key}
              </span>

              {/* Balken A (nach links wachsend) */}
              <div style={{ position: 'relative', height: 10, background: 'var(--border)', borderRadius: 2, overflow: 'hidden' }}>
                <div style={{
                  position: 'absolute', top: 0, bottom: 0, right: 0, width: `${anteilA}%`,
                  background: f.farbe, opacity: 0.55,
                }} />
              </div>
              <span style={{ fontSize: 12, color: 'var(--text-secondary)', textAlign: 'right' }}>
                {a.toFixed(0)}
              </span>

              {/* Balken B (nach rechts wachsend) */}
              <div style={{ position: 'relative', height: 10, background: 'var(--border)', borderRadius: 2, overflow: 'hidden' }}>
                <div style={{
                  position: 'absolute', top: 0, bottom: 0, left: 0, width: `${anteilB}%`,
                  background: f.farbe,
                }} />
              </div>
              <span style={{ fontSize: 12, color: 'var(--text-secondary)' }}>
                {b.toFixed(0)}
              </span>

              {/* Delta */}
              <span style={{ fontSize: 13, fontWeight: 500, color: deltaFarbe, textAlign: 'right' }}>
                {delta >= 0 ? '+' : '−'}{Math.abs(delta).toFixed(0)} GWh
                <span style={{ fontSize: 10, marginLeft: 6, color: deltaFarbe }}>
                  ({isFinite(proz) ? (delta >= 0 ? '+' : '−') + Math.abs(proz).toFixed(0) + '%' : 'neu'})
                </span>
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
