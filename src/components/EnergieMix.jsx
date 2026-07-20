import { useState, useMemo } from 'react'
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
} from 'recharts'
import { useJson } from '../hooks/useJson'

const FORMEN = [
  { key: 'Laufwasser', farbe: '#4c9be0' },
  { key: 'Speicher', farbe: '#2b6cb0' },
  { key: 'Kernkraft', farbe: '#8a6fbf' },
  { key: 'Thermisch', farbe: '#b0552f' },
  { key: 'Andere', farbe: '#9aa0a6' },
  { key: 'Wind', farbe: '#6fc3b8' },
  { key: 'Photovoltaik', farbe: '#efb23a' },
]

// Kleine Inline-Icons je Energieträger. Rein visuell, an die Trägerfarbe gebunden.
function TraegerIcon({ typ, farbe, size = 14 }) {
  const p = { width: size, height: size, viewBox: '0 0 24 24', fill: 'none', stroke: farbe, strokeWidth: 2, strokeLinecap: 'round', strokeLinejoin: 'round' }
  switch (typ) {
    case 'Laufwasser':   // fliessendes Wasser: Wellen
      return <svg {...p}><path d="M2 9c2.5-2.5 4.5-2.5 7 0s4.5 2.5 7 0" /><path d="M2 15c2.5-2.5 4.5-2.5 7 0s4.5 2.5 7 0" /></svg>
    case 'Speicher':     // gespeichertes Wasser: Tropfen
      return <svg {...p}><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z" /></svg>
    case 'Kernkraft':    // Atom
      return <svg {...p}><circle cx="12" cy="12" r="1.6" fill={farbe} stroke="none" /><ellipse cx="12" cy="12" rx="10" ry="4" /><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)" /><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)" /></svg>
    case 'Thermisch':    // Flamme
      return <svg {...p}><path d="M12 3c1 3-2 4-2 7a2 2 0 0 0 4 0c0-1-1-2-1-2 2 1 3 3 3 5a5 5 0 0 1-10 0c0-4 4-6 6-10z" /></svg>
    case 'Wind':         // Windböen
      return <svg {...p}><path d="M3 8h10a2.5 2.5 0 1 0-2.5-2.5" /><path d="M3 16h7a2.5 2.5 0 1 1-2.5 2.5" /><path d="M3 12h14a2.5 2.5 0 1 0-2.5-2.5" /></svg>
    case 'Photovoltaik': // Sonne
      return <svg {...p}><circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4" /></svg>
    default:             // Andere: drei Punkte
      return <svg {...p}><circle cx="6" cy="12" r="1.4" fill={farbe} stroke="none" /><circle cx="12" cy="12" r="1.4" fill={farbe} stroke="none" /><circle cx="18" cy="12" r="1.4" fill={farbe} stroke="none" /></svg>
  }
}

function MixTooltip({ active, payload, label }) {
  if (!active || !payload || !payload.length) return null
  const total = payload.reduce((s, p) => s + (p.value || 0), 0)
  const d = new Date(label)
  return (
    <div style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)', borderRadius: 8, padding: '8px 10px', fontSize: 12, color: 'var(--text-primary)' }}>
      <div style={{ fontWeight: 500 }}>{d.getMonth() + 1}/{d.getFullYear()}</div>
      {[...payload].reverse().map(p => (
        <div key={p.name} style={{ color: p.color }}>{p.name}: {p.value.toFixed(0)} GWh</div>
      ))}
      <div style={{ marginTop: 4, borderTop: '1px solid var(--border)', paddingTop: 2 }}>Total: {total.toFixed(0)} GWh</div>
    </div>
  )
}

export function EnergieMix({ brushRange }) {
  const { data } = useJson('/data/energiemix_monat.json')
  const [aktiv, setAktiv] = useState(null)   // hervorgehobener Energieträger | null

  const reihe = useMemo(() => {
    if (!data) return null
    let r = data.map(d => ({ ...d, t: Date.parse(d.date) }))
    if (brushRange) {
      const [s, e] = brushRange
      r = r.filter(d => d.t >= s && d.t <= e)
    }
    return r
  }, [data, brushRange])

  // Aggregierte Summen pro Energieträger für den gewählten Zeitraum
  const kennzahlen = useMemo(() => {
    if (!reihe || reihe.length === 0) return null
    const summen = Object.fromEntries(FORMEN.map(f => [f.key, 0]))
    for (const d of reihe) {
      for (const f of FORMEN) summen[f.key] += d[f.key] || 0
    }
    const total = Object.values(summen).reduce((s, v) => s + v, 0)
    // Nach Grösse sortiert für die KPI-Darstellung
    const rang = [...FORMEN]
      .map(f => ({ ...f, summe: summen[f.key], anteil: total > 0 ? summen[f.key] / total : 0 }))
      .sort((a, b) => b.summe - a.summe)
    return { total, rang }
  }, [reihe])

  if (!reihe) return <p style={{ color: 'var(--text-muted)' }}>Lade Energiemix…</p>
  if (brushRange && reihe.length === 0)
    return <p style={{ color: 'var(--text-muted)' }}>Kein Energiemix für den gewählten Zeitraum (Daten 2000 bis 2024).</p>

  function legendeKlick(e) {
    const key = e && (e.dataKey || e.value)
    if (!key) return
    setAktiv(a => (a === key ? null : key))
  }

  return (
    <div style={{ width: '100%' }}>
      {/* KPI-Kacheln pro Energieträger, sortiert nach Grösse */}
      {kennzahlen && (
        <div style={{ display: 'flex', gap: 6, marginBottom: 10, flexWrap: 'wrap', alignItems: 'stretch' }}>
          {kennzahlen.rang.map(f => {
            const istFokus = aktiv === f.key
            const gedimmt = aktiv && !istFokus
            return (
              <button
                key={f.key}
                onClick={() => setAktiv(a => (a === f.key ? null : f.key))}
                style={{
                  border: `1px solid ${istFokus ? f.farbe : 'var(--border)'}`,
                  background: istFokus ? `${f.farbe}22` : 'var(--bg-elevated)',
                  borderRadius: 6, padding: '6px 10px', cursor: 'pointer',
                  opacity: gedimmt ? 0.35 : 1,
                  display: 'flex', flexDirection: 'column', alignItems: 'flex-start',
                  minWidth: 96, transition: 'opacity 120ms, background 120ms',
                }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: 11, color: 'var(--text-secondary)' }}>
                  <TraegerIcon typ={f.key} farbe={f.farbe} size={14} />
                  {f.key}
                </span>
                <span style={{ fontSize: 14, fontWeight: 500, color: 'var(--text-primary)', marginTop: 2 }}>
                  {(f.summe / 1000).toFixed(1)} TWh
                </span>
                <span style={{ fontSize: 10, color: 'var(--text-muted)' }}>
                  {(f.anteil * 100).toFixed(1)}%
                </span>
              </button>
            )
          })}
          <div style={{
            border: '1px solid var(--border)', background: 'var(--bg-elevated)',
            borderRadius: 6, padding: '6px 10px',
            display: 'flex', flexDirection: 'column', justifyContent: 'center', minWidth: 96,
          }}>
            <span style={{ fontSize: 11, color: 'var(--text-secondary)' }}>Gesamt</span>
            <span style={{ fontSize: 14, fontWeight: 500, color: 'var(--text-primary)', marginTop: 2 }}>
              {(kennzahlen.total / 1000).toFixed(1)} TWh
            </span>
            <span style={{ fontSize: 10, color: 'var(--text-muted)' }}>im Zeitraum</span>
          </div>
        </div>
      )}

      <div style={{ width: '100%', height: 340 }}>
      <ResponsiveContainer>
        <AreaChart data={reihe} margin={{ top: 10, right: 16, bottom: 4, left: 4 }}>
          <XAxis dataKey="t" type="number" scale="time" domain={brushRange ? brushRange : ['dataMin', 'dataMax']}
                 tickFormatter={t => new Date(t).getFullYear()} tick={{ fontSize: 11 }} minTickGap={40} />
          <YAxis tick={{ fontSize: 11 }} width={64} tickFormatter={v => (v / 1000).toFixed(0) + ' TWh'} />
          <Tooltip content={<MixTooltip />} />
          <Legend wrapperStyle={{ fontSize: 12, cursor: 'pointer' }} onClick={legendeKlick} />
          {FORMEN.map(f => {
            const opacity = aktiv ? (aktiv === f.key ? 0.95 : 0.12) : 0.85
            return (
              <Area key={f.key} dataKey={f.key} stackId="mix" stroke={f.farbe}
                    fill={f.farbe} fillOpacity={opacity} strokeOpacity={aktiv && aktiv !== f.key ? 0.2 : 1}
                    isAnimationActive={false} />
            )
          })}
        </AreaChart>
      </ResponsiveContainer>
      </div>
      <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>
        Klick auf einen Energieträger in der Kachel-Reihe oder Legende hebt ihn hervor, erneuter Klick zeigt wieder alle.
      </div>
    </div>
  )
}
