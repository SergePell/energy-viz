import { useState, useMemo } from 'react'
import {
  ComposedChart, Line, Scatter, XAxis, YAxis, Tooltip, ResponsiveContainer,
} from 'recharts'
import { useJson } from '../hooks/useJson'
import { QuickInfo } from './QuickInfo'
import { JahrDropdown } from './JahrDropdown'

const C_LINIE = '#2b8a78'
const C_ANOMALIE = '#e24b4a'
const C_FEIERTAG = '#ef9f27'

function ausduennen(arr, ziel = 1500) {
  if (arr.length <= ziel) return arr
  const k = Math.ceil(arr.length / ziel)
  const out = arr.filter((_, i) => i % k === 0)
  if (out[out.length - 1] !== arr[arr.length - 1]) out.push(arr[arr.length - 1])
  return out
}

function Punkt({ farbe, text }) {
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5, fontSize: 12, color: 'var(--text-secondary)' }}>
      <span style={{ width: 9, height: 9, borderRadius: '50%', background: farbe }} />{text}
    </span>
  )
}

function InfoTooltip({ active, payload, einheit }) {
  if (!active || !payload || !payload.length) return null
  const d = payload[0].payload
  return (
    <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 8, padding: '8px 10px', fontSize: 12, color: 'var(--text-primary)' }}>
      <div style={{ fontWeight: 500 }}>{d.date}</div>
      <div>{einheit}: {(d.mwh / 1000).toFixed(0)} GWh</div>
      {d.score != null && (<>
        <div>Anomalie-Score: {d.score.toFixed(2)}</div>
        {d.temp != null && <div>Temperatur: {d.temp.toFixed(1)} °C</div>}
        {d.preis != null && <div>Preis: {d.preis.toFixed(0)} €/MWh</div>}
        {d.feiertag && <div style={{ color: C_FEIERTAG }}>Feiertag: {d.feiertag}</div>}
      </>)}
    </div>
  )
}

export function VerbrauchAnomalie({ selectedKanton, onClear, onBrush }) {
  const { data: verbrauch } = useJson('/data/verbrauch_national_daily.json')
  const { data: anomalie } = useJson('/data/landesverbrauch_daily_anomaly.json')
  const { data: kantonMonat } = useJson('/data/erzeugung_kanton_monat.json')
  const [schwelle, setSchwelle] = useState(0.9)
  const [von, setVon] = useState(null)
  const [bis, setBis] = useState(null)

  const merged = useMemo(() => {
    if (!verbrauch || !anomalie) return null
    const aMap = new Map(anomalie.map(a => [a.date, a]))
    return verbrauch.map(v => {
      const a = aMap.get(v.date) || {}
      return { t: Date.parse(v.date), date: v.date, mwh: v.mwh,
        score: a.anomaly_score ?? null, feiertag: a.feiertag_name ?? null,
        temp: a.temp ?? null, preis: a.preis ?? null }
    })
  }, [verbrauch, anomalie])

  const kantonReihe = useMemo(() => {
    if (!selectedKanton || !kantonMonat) return null
    return kantonMonat.filter(r => r.kanton === selectedKanton)
      .map(r => ({ t: Date.parse(r.date), date: r.date, mwh: r.mwh }))
      .sort((a, b) => a.t - b.t)
  }, [selectedKanton, kantonMonat])

  const linieVoll = useMemo(() => (merged ? ausduennen(merged) : []), [merged])

  const jahre = useMemo(() => {
    if (!linieVoll.length) return []
    const y0 = new Date(linieVoll[0].t).getFullYear()
    const y1 = new Date(linieVoll[linieVoll.length - 1].t).getFullYear()
    return Array.from({ length: y1 - y0 + 1 }, (_, i) => y0 + i)
  }, [linieVoll])

  const kantonModus = !!selectedKanton

  if (kantonModus && !kantonReihe) return <p style={{ color: 'var(--text-muted)' }}>Lade Kanton…</p>
  if (!kantonModus && !merged) return <p style={{ color: 'var(--text-muted)' }}>Lade Daten…</p>

  const y0 = jahre[0], y1 = jahre[jahre.length - 1]
  const effVon = von ?? y0
  const effBis = bis ?? y1
  const tVon = Date.parse(`${effVon}-01-01`)
  const tBis = Date.parse(`${effBis}-12-31`)
  const imBereich = t => t >= tVon && t <= tBis

  // Variante A: Linie und Anomalien folgen dem gewählten Zeitraum
  const linie = linieVoll.filter(d => imBereich(d.t))
  const anomalien = merged ? merged.filter(d => d.score != null && d.score >= schwelle && !d.feiertag && imBereich(d.t)) : []
  const feiertage = merged ? merged.filter(d => d.score != null && d.score >= schwelle && d.feiertag && imBereich(d.t)) : []
  const xDomain = [tVon, tBis]

  function melde(v, b) {
    const voll = v === y0 && b === y1
    if (onBrush) onBrush(voll ? null : [Date.parse(`${v}-01-01`), Date.parse(`${b}-12-31`)])
  }
  function aendereVon(v) { const b = Math.max(v, effBis); setVon(v); setBis(b); melde(v, b) }
  function aendereBis(b) { const v = Math.min(effVon, b); setVon(v); setBis(b); melde(v, b) }
  function zuruecksetzen() { setVon(null); setBis(null); if (onBrush) onBrush(null) }

  const einheit = kantonModus ? 'Erzeugung' : 'Verbrauch'

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
        <h2 style={{ fontSize: 18, fontWeight: 500, margin: 0, color: 'var(--text-primary)' }}>
          {kantonModus ? `Erzeugung ${selectedKanton.replace('CH-', '')} (monatlich)` : 'Nationaler Stromverbrauch'}
        </h2>
        {kantonModus
          ? <button onClick={onClear} style={{ fontSize: 12, padding: '3px 10px', borderRadius: 6, border: '1px solid var(--border)', background: 'var(--bg-card)', color: 'var(--text-secondary)', cursor: 'pointer' }}>← national</button>
          : <QuickInfo titel="Verbrauch, Anomalien & Schwellenwert">
              Die grüne Linie ist der tägliche Landesverbrauch (ab 2009). Rote Punkte sind erkannte Anomalien, gelbe als Feiertag erwartete Ausschläge, die deshalb nicht als Anomalie gezählt werden. Der Schwellenwert steuert die Empfindlichkeit: je höher, desto weniger und nur die stärksten Tage. Anomalien gibt es erst ab 2017, weil dafür Wetter und Preis als Kontext nötig sind. Über die Jahresauswahl filterst du den Zeitraum, der Linie und Karte gemeinsam einschränkt.
            </QuickInfo>}
      </div>

      <div style={{ width: '100%', height: 320 }}>
        <ResponsiveContainer>
          <ComposedChart data={kantonModus ? kantonReihe : linie} margin={{ top: 10, right: 16, bottom: 4, left: 4 }}>
            <XAxis dataKey="t" type="number" scale="time"
                   domain={kantonModus ? ['dataMin', 'dataMax'] : xDomain}
                   tickFormatter={t => new Date(t).getFullYear()} tick={{ fontSize: 11 }} minTickGap={40} />
            <YAxis tick={{ fontSize: 11 }} width={64}
                   domain={kantonModus ? ['dataMin - 5000', 'dataMax + 5000'] : [110000, 240000]}
                   tickFormatter={v => (v / 1000).toFixed(0) + ' GWh'} />
            <Tooltip content={<InfoTooltip einheit={einheit} />} />
            <Line dataKey="mwh" stroke={C_LINIE} dot={false} strokeWidth={1} isAnimationActive={false} />
            {!kantonModus && feiertage.length > 0 && <Scatter data={feiertage} dataKey="mwh" fill={C_FEIERTAG} isAnimationActive={false} />}
            {!kantonModus && anomalien.length > 0 && <Scatter data={anomalien} dataKey="mwh" fill={C_ANOMALIE} isAnimationActive={false} />}
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {!kantonModus && (
        <>
          <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginTop: 8, flexWrap: 'wrap' }}>
            <Punkt farbe={C_ANOMALIE} text="Anomalie" />
            <Punkt farbe={C_FEIERTAG} text="Feiertag (erwartet)" />
            <span style={{ marginLeft: 'auto', display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: 12, color: 'var(--text-secondary)' }}>
              Zeitraum
              <JahrDropdown wert={effVon} optionen={jahre} onChange={aendereVon} />
              bis
              <JahrDropdown wert={effBis} optionen={jahre} onChange={aendereBis} />
              <button onClick={zuruecksetzen} style={{ fontSize: 12, padding: '3px 10px', borderRadius: 6, border: '1px solid var(--border)', background: 'var(--bg-card)', color: 'var(--text-secondary)', cursor: 'pointer' }}>
                ganzer Zeitraum
              </button>
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginTop: 10, flexWrap: 'wrap' }}>
            <span style={{ fontSize: 12, color: 'var(--text-secondary)', whiteSpace: 'nowrap' }}>Schwellenwert</span>
            <input type="range" min="0" max="1" step="0.01" value={schwelle}
                   onChange={e => setSchwelle(parseFloat(e.target.value))} style={{ flex: 1, minWidth: 140 }} />
            <span style={{ fontSize: 12, fontWeight: 500, minWidth: 34 }}>{schwelle.toFixed(2)}</span>
            <span style={{ fontSize: 12, color: C_ANOMALIE }}>{anomalien.length} Anomalien</span>
            <span style={{ fontSize: 12, color: C_FEIERTAG }}>{feiertage.length} Feiertage erklärt</span>
          </div>
        </>
      )}
    </div>
  )
}