import { useMemo } from 'react'
import { ComposedChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { useJson } from '../hooks/useJson'

const C_LINIE = '#4c9be0'  // Erzeugungs-Blau, konsistent mit der Karte

function ErzTooltip({ active, payload }) {
  if (!active || !payload || !payload.length) return null
  const d = payload[0].payload
  const dat = new Date(d.date + 'T00:00:00Z')
  return (
    <div style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)', borderRadius: 8, padding: '8px 10px', fontSize: 12, color: 'var(--text-primary)' }}>
      <div style={{ fontWeight: 500, marginBottom: 2 }}>
        {dat.toLocaleDateString('de-CH', { month: 'short', year: 'numeric', timeZone: 'UTC' })}
      </div>
      <div>Erzeugung: {(d.mwh / 1000).toFixed(1)} GWh</div>
    </div>
  )
}

export function ErzeugungZeitreihe({ selectedKanton, onClear, brushRange }) {
  const { data: kantonMonat } = useJson('/data/erzeugung_kanton_monat.json')

  const reihe = useMemo(() => {
    if (!selectedKanton || !kantonMonat) return null
    let rows = kantonMonat.filter(r => r.kanton === selectedKanton)
      .map(r => ({ t: Date.parse(r.date), date: r.date, mwh: r.mwh }))
      .sort((a, b) => a.t - b.t)
    if (brushRange) rows = rows.filter(r => r.t >= brushRange[0] && r.t <= brushRange[1])
    return rows
  }, [selectedKanton, kantonMonat, brushRange])

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
        <h2 style={{ fontSize: 18, fontWeight: 500, margin: 0, color: 'var(--text-primary)' }}>
          {selectedKanton ? `Erzeugung ${selectedKanton.replace('CH-', '')} (monatlich)` : 'Kantonale Erzeugung'}
        </h2>
        {selectedKanton && (
          <button onClick={onClear} style={{ fontSize: 12, padding: '3px 10px', borderRadius: 6, border: '1px solid var(--border)', background: 'var(--bg-card)', color: 'var(--text-secondary)', cursor: 'pointer' }}>
            ← national
          </button>
        )}
      </div>

      {!selectedKanton ? (
        <div style={{ height: 320, display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px dashed var(--border)', borderRadius: 8, color: 'var(--text-muted)', fontSize: 13, textAlign: 'center', padding: 16 }}>
          Einen Kanton auf der Karte wählen, um die monatliche Erzeugung zu sehen.
        </div>
      ) : !reihe ? (
        <p style={{ color: 'var(--text-muted)' }}>Lade Kanton…</p>
      ) : (
        <div style={{ width: '100%', height: 320 }}>
          <ResponsiveContainer>
            <ComposedChart data={reihe} margin={{ top: 10, right: 16, bottom: 4, left: 4 }}>
              <XAxis dataKey="t" type="number" scale="time" domain={['dataMin', 'dataMax']}
                     tickFormatter={t => new Date(t).getFullYear()} tick={{ fontSize: 11 }} minTickGap={40} />
              <YAxis tick={{ fontSize: 11 }} width={64} domain={['dataMin - 5000', 'dataMax + 5000']}
                     tickFormatter={v => (v / 1000).toFixed(0) + ' GWh'} />
              <Tooltip content={<ErzTooltip />} />
              <Line dataKey="mwh" stroke={C_LINIE} dot={false} strokeWidth={1} isAnimationActive={false} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
