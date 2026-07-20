import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

const C_LINIE = '#2b8a78'
const cache = new Map()   // jahr -> {datum: [[minuten, mwh], ...]}

async function ladeJahr(jahr) {
  if (cache.has(jahr)) return cache.get(jahr)
  const res = await fetch(`/data/viertelstunde/${jahr}.json`)
  if (!res.ok) throw new Error(`${res.status} für Jahr ${jahr}`)
  const daten = await res.json()
  cache.set(jahr, daten)
  return daten
}

function hhmm(minuten) {
  const h = String(Math.floor(minuten / 60)).padStart(2, '0')
  const m = String(minuten % 60).padStart(2, '0')
  return `${h}:${m}`
}

// Tagesminimum, Tagesmaximum und deren Verhaeltnis. Das Verhaeltnis ist die
// Kennzahl, an der sich ein gewoehnliches Werktagsprofil erkennen laesst.
function kennzahlen(punkte) {
  if (!punkte || !punkte.length) return null
  let min = punkte[0], max = punkte[0]
  for (const p of punkte) {
    if (p.mwh < min.mwh) min = p
    if (p.mwh > max.mwh) max = p
  }
  return { min, max, verhaeltnis: min.mwh > 0 ? max.mwh / min.mwh : null }
}

function Kachel({ label, wert, zusatz }) {
  return (
    <div style={{
      flex: '1 1 120px', minWidth: 120, padding: '8px 10px',
      border: '1px solid var(--border)', borderRadius: 6, background: 'var(--bg-card)',
    }}>
      <div style={{ fontSize: 10, letterSpacing: '0.08em', textTransform: 'uppercase',
                    color: 'var(--text-muted)', marginBottom: 3 }}>{label}</div>
      <div style={{ fontSize: 16, fontWeight: 500, color: 'var(--text-primary)' }}>{wert}</div>
      {zusatz && <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 1 }}>{zusatz}</div>}
    </div>
  )
}

export function TagesProfil({ datum, onClose }) {
  const [punkte, setPunkte] = useState(null)
  const [fehler, setFehler] = useState(null)

  useEffect(() => {
    if (!datum) return
    let aktiv = true
    setPunkte(null); setFehler(null)
    ladeJahr(datum.slice(0, 4))
      .then(d => {
        if (!aktiv) return
        const roh = d[datum]
        if (!roh) { setFehler('Für diesen Tag liegen keine Viertelstundenwerte vor.'); return }
        setPunkte(roh.map(([min, mwh]) => ({ min, zeit: hhmm(min), mwh })))
      })
      .catch(e => { if (aktiv) setFehler(e.message) })
    return () => { aktiv = false }
  }, [datum])

  if (!datum) return null

  const k = kennzahlen(punkte)

  return (
    <div style={{ marginTop: 12, padding: 12, border: '1px solid var(--border)', borderRadius: 8 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
        <h3 style={{ fontSize: 15, fontWeight: 500, margin: 0, color: 'var(--text-primary)' }}>
          Viertelstundenprofil {datum}
        </h3>
        <button onClick={onClose} style={{ fontSize: 12, padding: '3px 10px', borderRadius: 6,
          border: '1px solid var(--border)', background: 'var(--bg-card)',
          color: 'var(--text-secondary)', cursor: 'pointer' }}>schliessen</button>
      </div>

      {fehler && <p style={{ color: 'var(--text-muted)', fontSize: 12 }}>{fehler}</p>}
      {!punkte && !fehler && <p style={{ color: 'var(--text-muted)', fontSize: 12 }}>Lade Tagesprofil…</p>}

      {punkte && (
        <>
          {k && (
            <div style={{ display: 'flex', gap: 10, marginBottom: 10, flexWrap: 'wrap' }}>
              <Kachel label="Maximum" wert={`${k.max.mwh.toFixed(1)} MWh`} zusatz={`um ${k.max.zeit} Uhr`} />
              <Kachel label="Minimum" wert={`${k.min.mwh.toFixed(1)} MWh`} zusatz={`um ${k.min.zeit} Uhr`} />
              {k.verhaeltnis != null &&
                <Kachel label="Verhältnis" wert={k.verhaeltnis.toFixed(2)} zusatz="Maximum zu Minimum" />}
            </div>
          )}

          <div style={{ width: '100%', height: 220 }}>
            <ResponsiveContainer>
              <LineChart data={punkte} margin={{ top: 8, right: 16, bottom: 4, left: 4 }}>
                {/* X-Achse: Minuten seit Mitternacht, fest 0 bis 1440 */}
                <XAxis dataKey="min" type="number" domain={[0, 1440]}
                       ticks={[0, 360, 720, 1080, 1440]} tickFormatter={hhmm}
                       tick={{ fontSize: 11 }} />
                {/* Y-Achse bewusst nicht bei null beginnend, sonst wird die
                    Tageskurve gestaucht. In der Abbildungsunterschrift nennen. */}
                <YAxis tick={{ fontSize: 11 }} width={56}
                       domain={['dataMin - 200', 'dataMax + 200']}
                       tickFormatter={v => v.toFixed(0) + ' MWh'} />
                <Tooltip
                  labelFormatter={m => hhmm(m) + ' Uhr'}
                  formatter={v => [`${v.toFixed(1)} MWh`, 'Verbrauch']} />
                <Line dataKey="mwh" stroke={C_LINIE} dot={false} strokeWidth={1.2}
                      isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 6 }}>
            {punkte.length} Viertelstundenwerte. Werte in MWh je Viertelstunde,
            nicht in GWh je Tag wie in der Übersicht. Die vertikale Achse beginnt
            nicht bei null.
          </p>
        </>
      )}
    </div>
  )
}
