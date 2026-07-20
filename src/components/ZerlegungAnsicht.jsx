import { useState, useEffect, useMemo } from 'react'
import {
  ComposedChart, Line, Scatter, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine,
} from 'recharts'

const C_TREND = '#2b8a78'
const C_SAISON = '#4c9be0'
const C_RESID = '#8a8f9c'
const C_ANOMALIE = '#e24b4a'

const REIHEN = [
  { id: 'landesverbrauch_daily', label: 'Landesverbrauch (täglich)', anomalien: true },
  { id: 'wasserkraft_monthly',   label: 'Wasserkraft (monatlich)',   anomalien: false },
]

const cache = new Map()

async function ladeZerlegung(id) {
  if (cache.has(id)) return cache.get(id)
  const res = await fetch(`/data/${id}_decomp.json`)
  if (!res.ok) throw new Error(`${res.status} für ${id}`)
  const daten = await res.json()
  cache.set(id, daten)
  return daten
}

// Ausduennen: Trend und Saison werden gemittelt, das Residuum behaelt je Bucket
// den betragsmaessig groessten Wert. Sonst verschwinden genau die Ausschlaege,
// auf denen die Anomalieerkennung arbeitet. Ziel 6500 heisst: bei der taeglichen
// Reihe (6297 Punkte) greift das Ausduennen gar nicht.
function ausduennen(punkte, felder, ziel = 6500) {
  if (punkte.length <= ziel) return punkte
  const k = Math.ceil(punkte.length / ziel)
  const out = []
  for (let i = 0; i < punkte.length; i += k) {
    const b = punkte.slice(i, i + k)
    const mittel = f => {
      const w = b.map(p => p[f]).filter(v => v != null)
      return w.length ? w.reduce((a, c) => a + c, 0) / w.length : null
    }
    let extrem = b[0]
    for (const p of b) if (Math.abs(p.resid ?? 0) > Math.abs(extrem.resid ?? 0)) extrem = p
    const rec = { t: b[0].t, date: extrem.date, resid: extrem.resid, score: extrem.score }
    for (const f of felder) rec[f] = mittel(f)
    rec.trend = mittel('trend')
    out.push(rec)
  }
  return out
}

function fmtGWh(v) {
  return (v / 1000).toFixed(0) + ' GWh'
}

// Wichtig: die Prop heisst children, nicht kinder. Sonst rendert der
// ResponsiveContainer nichts und man sieht nur Titel und leere Flaechen.
function Panel({ titel, hinweis, children, hoehe = 110, letzte = false }) {
  return (
    <div style={{ marginBottom: letzte ? 0 : 6 }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginBottom: 2 }}>
        <span style={{ fontSize: 12, fontWeight: 500, color: 'var(--text-secondary)' }}>{titel}</span>
        {hinweis && <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{hinweis}</span>}
      </div>
      <div style={{ width: '100%', height: hoehe }}>
        <ResponsiveContainer>{children}</ResponsiveContainer>
      </div>
    </div>
  )
}

// Eigene Tooltip-Komponente. Ein formatter kann den t-Eintrag (Zeitstempel)
// nicht zuverlaessig ausblenden; hier wird die Nutzlast direkt gefiltert.
function ZerlegungTooltip({ active, payload, label, feld, beschriftung }) {
  if (!active || !payload || !payload.length) return null
  const eintrag = payload.find(p => p.dataKey === feld)
  if (!eintrag) return null
  const d = eintrag.payload
  const istAnomal = d.score != null && payload.some(p => p.dataKey === feld && p.fill === C_ANOMALIE)
  return (
    <div style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)', borderRadius: 8,
                  padding: '8px 10px', fontSize: 12, color: 'var(--text-primary)' }}>
      <div style={{ fontWeight: 500, marginBottom: 3 }}>{d.date ?? new Date(label).toISOString().slice(0, 10)}</div>
      <div style={{ color: 'var(--text-secondary)' }}>
        {beschriftung}: {(eintrag.value / 1000).toFixed(1)} GWh
      </div>
      {feld === 'resid' && d.score != null && (
        <div style={{ marginTop: 3, fontSize: 11, color: istAnomal ? C_ANOMALIE : 'var(--text-muted)' }}>
          Anomalie-Score: {d.score.toFixed(2)}
        </div>
      )}
    </div>
  )
}

export function ZerlegungAnsicht({ brushRange, schwelle }) {
  const [offen, setOffen] = useState(false)
  const [reiheId, setReiheId] = useState(REIHEN[0].id)
  const [daten, setDaten] = useState(null)
  const [anomalieDaten, setAnomalieDaten] = useState(null)
  const [fehler, setFehler] = useState(null)

  const reihe = REIHEN.find(r => r.id === reiheId)

  useEffect(() => {
    if (!offen) return
    let aktiv = true
    setDaten(null); setFehler(null)
    ladeZerlegung(reiheId)
      .then(d => { if (aktiv) setDaten(d) })
      .catch(e => { if (aktiv) setFehler(e.message) })
    return () => { aktiv = false }
  }, [offen, reiheId])

  useEffect(() => {
    if (!offen || !reihe.anomalien || anomalieDaten) return
    let aktiv = true
    fetch('/data/landesverbrauch_daily_anomaly.json')
      .then(r => r.ok ? r.json() : Promise.reject(new Error(r.status)))
      .then(d => { if (aktiv) setAnomalieDaten(d) })
      .catch(() => {})
    return () => { aktiv = false }
  }, [offen, reihe, anomalieDaten])

  const aufbereitet = useMemo(() => {
    if (!daten) return null
    const aMap = anomalieDaten ? new Map(anomalieDaten.map(a => [a.date, a])) : new Map()
    let punkte = daten.punkte.map(p => {
      const a = aMap.get(p.date)
      return { ...p, t: Date.parse(p.date),
               score: a?.anomaly_score ?? null,
               feiertag: a?.feiertag_name ?? null }
    })
    if (brushRange) {
      const [s, e] = brushRange
      punkte = punkte.filter(p => p.t >= s && p.t <= e)
    }
    // punkteVoll = ungeduennt, nur fuer die Anomaliepunkte.
    return { ...daten, punkteVoll: punkte, punkte: ausduennen(punkte, daten.saison_felder) }
  }, [daten, anomalieDaten, brushRange])

  const anomalien = useMemo(() => {
    if (!aufbereitet || !reihe.anomalien) return []
    return aufbereitet.punkteVoll.filter(p =>
      p.score != null && p.score >= schwelle && !p.feiertag)
  }, [aufbereitet, reihe, schwelle])

  const hatPunkte = !!aufbereitet && aufbereitet.punkte.length > 0

  const xDomain = hatPunkte
    ? [aufbereitet.punkte[0].t, aufbereitet.punkte[aufbereitet.punkte.length - 1].t]
    : ['dataMin', 'dataMax']

  const xAchse = zeigeTicks => (
    <XAxis dataKey="t" type="number" scale="time" domain={xDomain}
           tickFormatter={t => new Date(t).getFullYear()}
           tick={zeigeTicks ? { fontSize: 11 } : false}
           axisLine={zeigeTicks} tickLine={zeigeTicks}
           height={zeigeTicks ? 20 : 1} minTickGap={40} />
  )

  // Trend liegt weit von null entfernt und braucht eine eng anliegende Achse.
  const yAchseTrend = () => (
    <YAxis tick={{ fontSize: 10 }} width={64} tickFormatter={fmtGWh}
           domain={['dataMin - 5000', 'dataMax + 5000']} />
  )

  // Saison und Residuum sind um null zentriert. Eine symmetrische Achse
  // verhindert, dass die Nulllinie an den Rand rutscht.
  const yAchseSymmetrisch = () => (
    <YAxis tick={{ fontSize: 10 }} width={64} tickFormatter={fmtGWh}
           domain={([min, max]) => {
             const m = Math.max(Math.abs(min), Math.abs(max))
             return [-m, m]
           }} />
  )

  return (
    <div style={{ marginTop: 12 }}>
      <button onClick={() => setOffen(o => !o)}
        style={{ fontSize: 12, padding: '5px 12px', borderRadius: 6,
                 border: '1px solid var(--border)', background: 'var(--bg-card)',
                 color: 'var(--text-secondary)', cursor: 'pointer' }}>
        {offen ? 'Zerlegung ausblenden' : 'Zerlegung anzeigen'}
      </button>

      {offen && (
        <div style={{ marginTop: 10, padding: 12, border: '1px solid var(--border)', borderRadius: 8 }}>
          <div style={{ display: 'flex', gap: 8, marginBottom: 10, flexWrap: 'wrap' }}>
            {REIHEN.map(r => (
              <button key={r.id} onClick={() => setReiheId(r.id)}
                style={{ fontSize: 12, padding: '4px 10px', borderRadius: 6, cursor: 'pointer',
                         border: `1px solid ${reiheId === r.id ? 'var(--text-secondary)' : 'var(--border)'}`,
                         background: reiheId === r.id ? '#1b1f2a' : 'var(--bg-elevated)',
                         color: reiheId === r.id ? 'var(--text-primary)' : 'var(--text-muted)' }}>
                {r.label}
              </button>
            ))}
          </div>

          {fehler && <p style={{ color: 'var(--text-muted)', fontSize: 12 }}>{fehler}</p>}

          {!aufbereitet && !fehler &&
            <p style={{ color: 'var(--text-muted)', fontSize: 12 }}>Lade Zerlegung…</p>}

          {aufbereitet && !hatPunkte && (
            <p style={{ color: 'var(--text-muted)', fontSize: 12 }}>
              Für den gewählten Zeitraum liegt keine Zerlegung vor. Die Wasserkraftreihe
              reicht von 2000 bis 2024, der Landesverbrauch von 2009 bis 2026.
            </p>
          )}

          {hatPunkte && (
            <>
              <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 0, marginBottom: 10 }}>
                {aufbereitet.methode} mit {aufbereitet.perioden.join(' und ')} Perioden.
                Die Reihe wird additiv in Trend, Saison und Residuum zerlegt (Cleveland et al., 1990).
                Der Isolation Forest arbeitet auf dem Residuum.
              </p>

              <Panel titel="Trend">
                <ComposedChart data={aufbereitet.punkte} margin={{ top: 4, right: 12, bottom: 0, left: 0 }}>
                  {xAchse(false)}{yAchseTrend()}
                  <Tooltip content={<ZerlegungTooltip feld="trend" beschriftung="Trend" />} />
                  <Line dataKey="trend" stroke={C_TREND} dot={false} strokeWidth={1.4} isAnimationActive={false} />
                </ComposedChart>
              </Panel>

              {aufbereitet.saison_felder.map(feld => (
                <Panel key={feld}
                       titel={`Saison (Periode ${feld.replace('saison_', '')})`}
                       hinweis={feld.endsWith('_7') ? 'Wochenrhythmus'
                              : feld.endsWith('_365') ? 'Jahresgang' : null}>
                  <ComposedChart data={aufbereitet.punkte} margin={{ top: 4, right: 12, bottom: 0, left: 0 }}>
                    {xAchse(false)}{yAchseSymmetrisch()}
                    <Tooltip content={<ZerlegungTooltip feld={feld} beschriftung="Saison" />} />
                    <ReferenceLine y={0} stroke="var(--text-muted)" strokeDasharray="2 2" strokeOpacity={0.4} />
                    <Line dataKey={feld} stroke={C_SAISON} dot={false} strokeWidth={1} isAnimationActive={false} />
                  </ComposedChart>
                </Panel>
              ))}

              <Panel titel="Residuum"
                     hinweis={reihe.anomalien
                       ? `${anomalien.length} Anomalien bei Schwellenwert ${schwelle.toFixed(3)}`
                       : null}
                     hoehe={130} letzte>
                <ComposedChart data={aufbereitet.punkte} margin={{ top: 4, right: 12, bottom: 0, left: 0 }}>
                  {xAchse(true)}{yAchseSymmetrisch()}
                  <Tooltip content={<ZerlegungTooltip feld="resid" beschriftung="Residuum" />} />
                  <ReferenceLine y={0} stroke="var(--text-muted)" strokeDasharray="2 2" strokeOpacity={0.4} />
                  <Line dataKey="resid" stroke={C_RESID} dot={false} strokeWidth={0.9} isAnimationActive={false} />
                  {anomalien.length > 0 &&
                    <Scatter data={anomalien} dataKey="resid" fill={C_ANOMALIE} isAnimationActive={false} />}
                </ComposedChart>
              </Panel>

              {reihe.anomalien && (
                <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 8 }}>
                  Die roten Punkte markieren die multivariat erkannten Anomalien. Ihr Residuum ist
                  erhöht, wird aber von den Ausschlägen an Feiertagen übertroffen. Das Residuum
                  allein trennt die Krisentage deshalb nicht von den erwartbaren
                  Feiertagsausschlägen; erst der Preis- und Wetterkontext ordnet sie ein.
                </p>
              )}

              <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>
                Die Saison- und Residuum-Achsen sind symmetrisch um null skaliert.
                Der Wochenrhythmus ist erst bei einem Zeitraum von ein bis zwei Jahren lesbar.
              </p>
            </>
          )}
        </div>
      )}
    </div>
  )
}
