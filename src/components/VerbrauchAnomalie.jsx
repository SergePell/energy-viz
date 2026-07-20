import { useState, useMemo } from 'react'
import {
  ComposedChart, Line, Scatter, XAxis, YAxis, Tooltip, ResponsiveContainer,
} from 'recharts'
import { useJson } from '../hooks/useJson'
import { QuickInfo } from './QuickInfo'

const C_LINIE = '#2b8a78'
const C_ANOMALIE = '#e24b4a'
const C_FEIERTAG = '#ef9f27'

// Der Anomalie-Score folgt Liu et al. (2008) und liegt bei dieser Zeitreihe
// zwischen 0.39 und 0.71. Ein Regler von 0 bis 1 waere daher groesstenteils
// toter Weg. Schrittweite 0.005, weil zwischen 0.647 und 0.638 mehrere Tage
// dicht beieinanderliegen.
const SCHWELLE_MIN = 0.60
const SCHWELLE_MAX = 0.72
const SCHWELLE_STEP = 0.005
const SCHWELLE_START = 0.68   // markiert 2 Anomalien; 0.65 markiert 3

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

function formatiereDatum(isoDatum) {
  // Ausgabe z.B.: "Do, 5. Juli 2024"
  const d = new Date(isoDatum + 'T00:00:00Z')
  return d.toLocaleDateString('de-CH', {
    weekday: 'short', day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC',
  })
}

function InfoTooltip({ active, payload, einheit, schwelle }) {
  if (!active || !payload || !payload.length) return null
  const d = payload[0].payload
  // Reihenfolge wichtig: hatScore muss vor istAnomal deklariert sein,
  // sonst ReferenceError (temporal dead zone).
  const hatKontext = d.temp != null || d.preis != null || d.feiertag != null
  const hatScore = d.score != null
  const istAnomal = hatScore && d.score >= schwelle
  return (
    <div style={{
      background: 'var(--bg-elevated)', border: '1px solid var(--border)', borderRadius: 8,
      padding: '10px 12px', fontSize: 12, color: 'var(--text-primary)', minWidth: 180,
    }}>
      <div style={{ fontWeight: 500, marginBottom: 4 }}>{formatiereDatum(d.date)}</div>
      <div style={{ fontSize: 13, fontWeight: 500, marginBottom: hatKontext || hatScore ? 6 : 0 }}>
        {einheit}: {(d.mwh / 1000).toFixed(1)} GWh
      </div>
      {hatKontext && (
        <div style={{ display: 'grid', gridTemplateColumns: 'auto auto', gap: '2px 10px', color: 'var(--text-secondary)' }}>
          {d.temp != null && <><span>Temperatur</span><span style={{ textAlign: 'right' }}>{d.temp.toFixed(1)} °C</span></>}
          {d.preis != null && <><span>Preis</span><span style={{ textAlign: 'right' }}>{d.preis.toFixed(0)} €/MWh</span></>}
          {d.feiertag && <><span style={{ color: C_FEIERTAG }}>Feiertag</span><span style={{ textAlign: 'right', color: C_FEIERTAG }}>{d.feiertag}</span></>}
        </div>
      )}
      {hatScore && (
        <div style={{
          marginTop: 6, paddingTop: 6, borderTop: '1px solid var(--border)',
          fontSize: 11, color: istAnomal ? C_ANOMALIE : 'var(--text-muted)',
        }}>
          Anomalie-Score: {d.score.toFixed(2)}
          {istAnomal && !d.feiertag && ' — Anomalie'}
          {istAnomal && d.feiertag && ' — durch Feiertag erklärt'}
        </div>
      )}
    </div>
  )
}

export function VerbrauchAnomalie({ selectedKanton, onClear, brushRange, onTagWaehlen, schwelle, onSchwelleChange }) {
  const { data: verbrauch } = useJson('/data/verbrauch_national_daily.json')
  const { data: anomalie } = useJson('/data/landesverbrauch_daily_anomaly.json')
  const { data: kantonMonat } = useJson('/data/erzeugung_kanton_monat.json')


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

  const kantonModus = !!selectedKanton

  if (kantonModus && !kantonReihe) return <p style={{ color: 'var(--text-muted)' }}>Lade Kanton…</p>
  if (!kantonModus && !merged) return <p style={{ color: 'var(--text-muted)' }}>Lade Daten…</p>

  // Zeitbereich kommt jetzt vollständig aus dem globalen Filter (brushRange).
  // Fallback: gesamter Datenbereich, falls kein Filter gesetzt ist.
  const tVon = brushRange ? brushRange[0] : (linieVoll[0]?.t ?? 0)
  const tBis = brushRange ? brushRange[1] : (linieVoll[linieVoll.length - 1]?.t ?? Date.now())
  const imBereich = t => t >= tVon && t <= tBis

  // Variante A: Linie und Anomalien folgen dem gewählten Zeitraum
  const linie = linieVoll.filter(d => imBereich(d.t))
  const anomalien = merged ? merged.filter(d => d.score != null && d.score >= schwelle && !d.feiertag && imBereich(d.t)) : []
  const feiertage = merged ? merged.filter(d => d.score != null && d.score >= schwelle && d.feiertag && imBereich(d.t)) : []
  const xDomain = [tVon, tBis]

  const einheit = kantonModus ? 'Erzeugung' : 'Verbrauch'

  // Recharts liefert bei Scatter je nach Version den Datensatz direkt oder
  // in .payload. Beide Faelle abfangen.
  const punktGeklickt = p => {
    const datum = p?.payload?.date ?? p?.date
    if (datum && onTagWaehlen) onTagWaehlen(datum)
  }

  // Klick auf die Linie: activeLabel ist der Zeitstempel (Zahl) des naechsten
  // Punktes. Achtung: die Linie ist auf ~1500 Punkte ausgeduennt, der Treffer
  // ist daher der naechstgelegene ausgeduennte Tag. Anomaliepunkte sind exakt.
  const chartGeklickt = e => {
    if (kantonModus || !onTagWaehlen || e?.activeLabel == null) return
    onTagWaehlen(new Date(e.activeLabel).toISOString().slice(0, 10))
  }

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
        <h2 style={{ fontSize: 18, fontWeight: 500, margin: 0, color: 'var(--text-primary)' }}>
          {kantonModus ? `Erzeugung ${selectedKanton.replace('CH-', '')} (monatlich)` : 'Nationaler Stromverbrauch'}
        </h2>
        {kantonModus
          ? <button onClick={onClear} style={{ fontSize: 12, padding: '3px 10px', borderRadius: 6, border: '1px solid var(--border)', background: 'var(--bg-card)', color: 'var(--text-secondary)', cursor: 'pointer' }}>← national</button>
          : <QuickInfo titel="Verbrauch, Anomalien & Schwellenwert">
              Die grüne Linie ist der tägliche Landesverbrauch. Rote Punkte sind erkannte Anomalien, gelbe als Feiertag erwartete Ausschläge, die deshalb nicht als Anomalie gezählt werden. Der Anomalie-Score nach Liu et al. (2008) liegt zwischen 0 und 1: Werte nahe 1 bedeuten, dass sich ein Tag sehr leicht von allen anderen abtrennen lässt und damit klar auffällig ist; Werte um 0.5 bedeuten unauffällig. In dieser Zeitreihe reichen die Scores von 0.39 bis 0.71. Der Schwellenwert steuert die Empfindlichkeit: je höher, desto weniger und nur die stärksten Tage. Anomalien gibt es erst ab 2017, weil dafür Wetter und Preis als Kontext nötig sind. Ein Klick auf einen Punkt oder auf die Linie öffnet das Viertelstundenprofil des Tages. Der Zeitraum wird über den globalen Filter oben gesteuert.
            </QuickInfo>}
      </div>

      <div style={{ width: '100%', height: 320 }}>
        <ResponsiveContainer>
          <ComposedChart data={kantonModus ? kantonReihe : linie}
                         onClick={chartGeklickt}
                         margin={{ top: 10, right: 16, bottom: 4, left: 4 }}>
            <XAxis dataKey="t" type="number" scale="time"
                   domain={kantonModus ? ['dataMin', 'dataMax'] : xDomain}
                   tickFormatter={t => new Date(t).getFullYear()} tick={{ fontSize: 11 }} minTickGap={40} />
            <YAxis tick={{ fontSize: 11 }} width={64}
                   domain={kantonModus ? ['dataMin - 5000', 'dataMax + 5000'] : [110000, 240000]}
                   tickFormatter={v => (v / 1000).toFixed(0) + ' GWh'} />
            <Tooltip content={<InfoTooltip einheit={einheit} schwelle={schwelle} />} />
            <Line dataKey="mwh" stroke={C_LINIE} dot={false} strokeWidth={1} isAnimationActive={false} />
            {!kantonModus && feiertage.length > 0 &&
              <Scatter data={feiertage} dataKey="mwh" fill={C_FEIERTAG} isAnimationActive={false}
                       onClick={punktGeklickt} style={{ cursor: 'pointer' }} />}
            {!kantonModus && anomalien.length > 0 &&
              <Scatter data={anomalien} dataKey="mwh" fill={C_ANOMALIE} isAnimationActive={false}
                       onClick={punktGeklickt} style={{ cursor: 'pointer' }} />}
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {!kantonModus && (
        <>
          <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginTop: 8, flexWrap: 'wrap' }}>
            <Punkt farbe={C_ANOMALIE} text="Anomalie" />
            <Punkt farbe={C_FEIERTAG} text="Feiertag (erwartet)" />
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginTop: 10, flexWrap: 'wrap' }}>
            <span style={{ fontSize: 12, color: 'var(--text-secondary)', whiteSpace: 'nowrap' }}>Schwellenwert</span>
            <input type="range" min={SCHWELLE_MIN} max={SCHWELLE_MAX} step={SCHWELLE_STEP} value={schwelle}
                   onChange={e => onSchwelleChange(parseFloat(e.target.value))} style={{ flex: 1, minWidth: 140 }} />
            <span style={{ fontSize: 12, fontWeight: 500, minWidth: 40 }}>{schwelle.toFixed(3)}</span>
            <span style={{ fontSize: 12, color: C_ANOMALIE }}>{anomalien.length} Anomalien</span>
            <span style={{ fontSize: 12, color: C_FEIERTAG }}>{feiertage.length} Feiertage erklärt</span>
          </div>
        </>
      )}
    </div>
  )
}
