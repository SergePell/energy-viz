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

function MixTooltip({ active, payload, label }) {
  if (!active || !payload || !payload.length) return null
  const total = payload.reduce((s, p) => s + (p.value || 0), 0)
  const d = new Date(label)
  return (
    <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 8, padding: '8px 10px', fontSize: 12, color: 'var(--text-primary)' }}>
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

  if (!reihe) return <p style={{ color: 'var(--text-muted)' }}>Lade Energiemix…</p>
  if (brushRange && reihe.length === 0)
    return <p style={{ color: 'var(--text-muted)' }}>Kein Energiemix für den gewählten Zeitraum (Daten 2000 bis 2024).</p>

  function legendeKlick(e) {
    const key = e && (e.dataKey || e.value)
    if (!key) return
    setAktiv(a => (a === key ? null : key))
  }

  return (
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
      <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>
        Klick auf einen Energieträger in der Legende hebt ihn hervor, erneuter Klick zeigt wieder alle.
      </div>
    </div>
  )
}