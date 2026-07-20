import { useMemo, useState } from 'react'
import {
  ComposedChart, Line, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine,
} from 'recharts'
import { useJson } from '../hooks/useJson'
import { QuickInfo } from './QuickInfo'

const GROESSEN = {
  temp: {
    key: 'temp',
    label: 'Temperatur',
    einheit: '°C',
    farbe: '#e24b4a',
  },
  niederschlag: {
    key: 'niederschlag',
    label: 'Niederschlag',
    einheit: 'mm/Tag',
    farbe: '#4c9be0',
  },
  sonne: {
    key: 'sonne',
    label: 'Globalstrahlung',
    einheit: 'W/m²',
    farbe: '#efb23a',
  },
}

// Ausduennen durch Mittelung statt durch Verwerfen. Das fruehere Verfahren nahm
// jeden k-ten Tag; bei k=3 verschwanden zwei Drittel aller Regentage. Der
// Niederschlag ist spitzenlastig, dort loescht Sampling Information.
function ausduennen(arr, ziel = 1500) {
  if (arr.length <= ziel) return arr
  const k = Math.ceil(arr.length / ziel)
  const out = []
  for (let i = 0; i < arr.length; i += k) {
    const bucket = arr.slice(i, i + k)
    const mittel = feld => {
      const werte = bucket.map(d => d[feld]).filter(v => v != null)
      return werte.length ? werte.reduce((a, b) => a + b, 0) / werte.length : null
    }
    out.push({
      t: bucket[0].t,
      date: bucket[0].date,
      temp: mittel('temp'),
      niederschlag: mittel('niederschlag'),
      sonne: mittel('sonne'),
      istAggregiert: k > 1,
      tageImBucket: bucket.length,
    })
  }
  return out
}

function formatiereDatum(isoDatum) {
  const d = new Date(isoDatum + 'T00:00:00Z')
  return d.toLocaleDateString('de-CH', {
    weekday: 'short', day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC',
  })
}

function WetterTooltip({ active, payload, aktiv }) {
  if (!active || !payload || !payload.length) return null
  const d = payload[0].payload
  return (
    <div style={{
      background: '#12141c', border: '1px solid var(--border)', borderRadius: 8,
      padding: '10px 12px', fontSize: 12, color: 'var(--text-primary)', minWidth: 190,
    }}>
      <div style={{ fontWeight: 500, marginBottom: 6 }}>{formatiereDatum(d.date)}</div>
      <div style={{ display: 'grid', gridTemplateColumns: 'auto auto', gap: '2px 10px', color: 'var(--text-secondary)' }}>
        {aktiv.map(k => {
          const g = GROESSEN[k]
          const val = d[k]
          if (val == null) return null
          return (
            <span key={k} style={{ display: 'contents' }}>
              <span style={{ color: g.farbe }}>{g.label}</span>
              <span style={{ textAlign: 'right' }}>
                {val.toFixed(g.key === 'temp' ? 1 : 0)} {g.einheit}
              </span>
            </span>
          )
        })}
      </div>
      {d.istAggregiert && (
        <div style={{ marginTop: 6, paddingTop: 6, borderTop: '1px solid var(--border)',
                      fontSize: 11, color: 'var(--text-muted)' }}>
          Mittelwert über {d.tageImBucket} Tage
        </div>
      )}
    </div>
  )
}

export function WetterLinie({ brushRange }) {
  const { data } = useJson('/data/wetter_national_daily.json')
  const [aktiv, setAktiv] = useState(['temp', 'niederschlag', 'sonne'])

  const merged = useMemo(() => {
    if (!data) return null
    return data.map(d => ({ ...d, t: Date.parse(d.date) }))
  }, [data])

  const gefiltert = useMemo(() => {
    if (!merged) return []
    if (!brushRange) return ausduennen(merged)
    const [s, e] = brushRange
    return ausduennen(merged.filter(d => d.t >= s && d.t <= e))
  }, [merged, brushRange])

  if (!merged) return <p style={{ color: 'var(--text-muted)' }}>Lade Wetterdaten…</p>
  if (gefiltert.length === 0)
    return <p style={{ color: 'var(--text-muted)' }}>Keine Wetterdaten für den gewählten Zeitraum (verfügbar ab 2017).</p>

  const tVon = brushRange ? brushRange[0] : gefiltert[0].t
  const tBis = brushRange ? brushRange[1] : gefiltert[gefiltert.length - 1].t
  const xDomain = [tVon, tBis]

  // Explizite Ticks statt pixelbasierter Auswahl. Sonst wiederholt sich die
  // Jahreszahl, weil mehrere Ticks in dasselbe Jahr fallen.
  const jahrVon = new Date(tVon).getUTCFullYear()
  const jahrBis = new Date(tBis).getUTCFullYear()
  const spanneJahre = jahrBis - jahrVon
  const kurzeSpanne = spanneJahre <= 2

  const ticks = []
  if (kurzeSpanne) {
    for (let j = jahrVon; j <= jahrBis; j++) {
      for (let m = 0; m < 12; m += 3) {
        const t = Date.UTC(j, m, 1)
        if (t >= tVon && t <= tBis) ticks.push(t)
      }
    }
  } else {
    for (let j = jahrVon; j <= jahrBis; j++) {
      const t = Date.UTC(j, 0, 1)
      if (t >= tVon && t <= tBis) ticks.push(t)
    }
  }
  const tickFmt = t => {
    const d = new Date(t)
    return kurzeSpanne
      ? `${String(d.getUTCMonth() + 1).padStart(2, '0')}/${String(d.getUTCFullYear()).slice(2)}`
      : String(d.getUTCFullYear())
  }

  const zeigeTemp = aktiv.includes('temp')
  const zeigeNsch = aktiv.includes('niederschlag')
  const zeigeSonne = aktiv.includes('sonne')

  function toggle(k) {
    setAktiv(a => a.includes(k) ? a.filter(x => x !== k) : [...a, k])
  }

  return (
    <div>
      {/* Toggle-Buttons */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 10, flexWrap: 'wrap', alignItems: 'center' }}>
        {Object.values(GROESSEN).map(g => {
          const an = aktiv.includes(g.key)
          return (
            <button key={g.key} onClick={() => toggle(g.key)} style={{
              border: `1px solid ${an ? g.farbe : 'var(--border)'}`,
              background: an ? `${g.farbe}22` : '#12141c',
              color: an ? 'var(--text-primary)' : 'var(--text-muted)',
              borderRadius: 6, padding: '5px 10px', fontSize: 12, cursor: 'pointer',
              display: 'inline-flex', alignItems: 'center', gap: 6,
            }}>
              <span style={{ width: 9, height: 9, borderRadius: '50%', background: g.farbe }} />
              {g.label}
            </button>
          )
        })}
        <QuickInfo titel="Wetterdaten">
          Nationaler Tagesdurchschnitt aus 18 Kantonsstationen (Open-Meteo). Temperatur in Grad Celsius, Niederschlag als Tagessumme in Millimetern, Globalstrahlung als Tagesdurchschnitt der kurzwelligen Einstrahlung in Watt pro Quadratmeter. Jede Grösse hat eine eigene Achse, die Kurven sind daher nicht direkt gegeneinander ablesbar, nur ihr zeitlicher Verlauf. Bei langen Zeiträumen werden mehrere Tage zu einem Punkt gemittelt. Daten ab 2017. Synchron zum Zeitraumfilter oben.
        </QuickInfo>
      </div>

      <div style={{ width: '100%', height: 260 }}>
        <ResponsiveContainer>
          <ComposedChart data={gefiltert} margin={{ top: 10, right: 8, bottom: 4, left: 4 }}>
            <XAxis dataKey="t" type="number" domain={xDomain}
       ticks={ticks} tickFormatter={tickFmt} tick={{ fontSize: 11 }} minTickGap={20} />

            {/* Linke Achse: Temperatur */}
            {zeigeTemp && (
              <YAxis yAxisId="temp" orientation="left" tick={{ fontSize: 11 }} width={48}
                tickFormatter={v => v.toFixed(0) + ' °C'}
                domain={['dataMin - 3', 'dataMax + 3']} />
            )}

            {/* Rechte Achse: Niederschlag */}
            {zeigeNsch && (
              <YAxis yAxisId="ns" orientation="right" tick={{ fontSize: 11 }} width={52}
                tickFormatter={v => v.toFixed(0) + ' mm'}
                domain={[0, 'dataMax + 5']} />
            )}

            {/* Eigene Achse fuer die Globalstrahlung. Frueher wurde sie durch 10
                geteilt und gegen die Millimeter-Achse gezeichnet; das mischte
                zwei physikalisch verschiedene Groessen auf einer Skala. */}
            {zeigeSonne && (
              <YAxis yAxisId="sonne" orientation="right" tick={{ fontSize: 11 }} width={58}
                tickFormatter={v => v.toFixed(0) + ' W/m²'}
                domain={[0, 'dataMax + 20']} />
            )}

            <Tooltip content={<WetterTooltip aktiv={aktiv} />} />

            {zeigeTemp && <ReferenceLine y={0} yAxisId="temp" stroke="var(--text-muted)" strokeDasharray="2 2" strokeOpacity={0.4} />}

            {zeigeNsch && (
              <Bar yAxisId="ns" dataKey="niederschlag" fill={GROESSEN.niederschlag.farbe}
                   fillOpacity={0.5} isAnimationActive={false} />
            )}
            {zeigeSonne && (
              <Line yAxisId="sonne" dataKey="sonne" stroke={GROESSEN.sonne.farbe}
                    dot={false} strokeWidth={1.2} isAnimationActive={false} />
            )}
            {zeigeTemp && (
              <Line yAxisId="temp" dataKey="temp" stroke={GROESSEN.temp.farbe}
                    dot={false} strokeWidth={1.4} isAnimationActive={false} />
            )}
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
