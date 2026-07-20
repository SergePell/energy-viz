import { useMemo, useState, useEffect, useRef, useCallback } from 'react'
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

const C_WOLKEN = '#9fb0c3'
const C_WIND = '#7fbf9f'
const C_HOCH = '#f2a1a0'
const C_TIEF = '#c23b3a'

// Zustands-Icon aus der mittleren Bewölkung. Rein beobachtend, keine Vorhersage.
function wetterZustand(wolken) {
  if (wolken == null) return { label: 'unbekannt', icon: 'cloud' }
  if (wolken < 35) return { label: 'Meist sonnig', icon: 'sun' }
  if (wolken < 65) return { label: 'Wechselnd bewölkt', icon: 'partly' }
  return { label: 'Meist bewölkt', icon: 'cloud' }
}

function ZustandIcon({ typ, size = 40 }) {
  if (typ === 'sun') {
    return (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={GROESSEN.sonne.farbe} strokeWidth="1.6" strokeLinecap="round">
        <circle cx="12" cy="12" r="4" />
        <path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4" />
      </svg>
    )
  }
  if (typ === 'partly') {
    return (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        <g stroke={GROESSEN.sonne.farbe}>
          <circle cx="8" cy="8" r="3" />
          <path d="M8 1.8v1.4M1.8 8h1.4M3.6 3.6l1 1M12.4 3.6l-1 1" />
        </g>
        <path d="M7 19h9a3.5 3.5 0 0 0 .4-6.98A5 5 0 0 0 7 13a3 3 0 0 0 0 6z" fill="var(--bg-card)" stroke={C_WOLKEN} />
      </svg>
    )
  }
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={C_WOLKEN} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
      <path d="M6 18h10a4 4 0 0 0 .5-7.97A6 6 0 0 0 5 9.5 3.5 3.5 0 0 0 6 18z" />
    </svg>
  )
}

function StatKachel({ farbe, label, wert }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
      <span style={{ width: 8, height: 8, borderRadius: '50%', background: farbe, flexShrink: 0 }} />
      <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>{label}</span>
      <span style={{ color: 'var(--text-primary)', fontSize: 12, fontWeight: 500 }}>{wert}</span>
    </div>
  )
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
      wolken: mittel('wolken'),
      wind: mittel('wind'),
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

// Der Tooltip meldet den aktiven Punkt über onAktiv nach oben (in einen Ref),
// damit ein Klick auf den Chart den Punkt anheften kann. In Recharts v3 liefert
// der Chart-onMouseMove kein verlässliches activePayload mehr; die active/payload-
// Props des Tooltips schon.
function WetterTooltip({ active, payload, aktiv, onAktiv }) {
  const d = active && payload && payload.length ? payload[0].payload : null
  useEffect(() => {
    if (d && onAktiv) onAktiv(d)
  }, [d, onAktiv])

  if (!d) return null
  const zeigeExtrem = !d.istAggregiert && d.temp_max != null && d.temp_min != null
  return (
    <div style={{
      background: 'var(--bg-elevated)', border: '1px solid var(--border)', borderRadius: 8,
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
        {zeigeExtrem && (
          <>
            <span style={{ color: C_HOCH }}>Tageshoch</span>
            <span style={{ textAlign: 'right' }}>{d.temp_max.toFixed(1)} °C</span>
            <span style={{ color: C_TIEF }}>Tagestief</span>
            <span style={{ textAlign: 'right' }}>{d.temp_min.toFixed(1)} °C</span>
          </>
        )}
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
  const [pinPunkt, setPinPunkt] = useState(null)         // per Klick angehefteter Punkt
  const aktiverPunktRef = useRef(null)                   // zuletzt gehoverter Punkt (kein Re-Render)
  const merkePunkt = useCallback(d => { aktiverPunktRef.current = d }, [])

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

  // Beobachtete Periodenmittel für die Kopfkarte. Auf den ungefilterten Tageswerten
  // gerechnet (nicht auf der ausgeduennten Reihe), damit die Mittel exakt sind.
  const zusammenfassung = useMemo(() => {
    if (!merged) return null
    const rows = brushRange ? merged.filter(d => d.t >= brushRange[0] && d.t <= brushRange[1]) : merged
    if (!rows.length) return null
    const mittel = feld => {
      const v = rows.map(d => d[feld]).filter(x => x != null)
      return v.length ? v.reduce((a, b) => a + b, 0) / v.length : null
    }
    return {
      temp: mittel('temp'),
      niederschlag: mittel('niederschlag'),
      sonne: mittel('sonne'),
      wolken: mittel('wolken'),
      wind: mittel('wind'),
      vonJahr: new Date(rows[0].t).getUTCFullYear(),
      bisJahr: new Date(rows[rows.length - 1].t).getUTCFullYear(),
    }
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

  // Klick auf den Chart heftet den zuletzt gehoverten Punkt an; nochmal derselbe löst.
  function chartGeklickt() {
    const p = aktiverPunktRef.current
    if (!p) return
    setPinPunkt(prev => (prev && prev.date === p.date ? null : p))
  }

  const spanne = zusammenfassung.vonJahr === zusammenfassung.bisJahr
    ? `${zusammenfassung.vonJahr}`
    : `${zusammenfassung.vonJahr}–${zusammenfassung.bisJahr}`

  // Kopfkarte zeigt entweder den angehefteten Punkt oder das Periodenmittel.
  const anzeige = pinPunkt ?? zusammenfassung
  const zustand = wetterZustand(anzeige.wolken)
  const unterzeile = pinPunkt
    ? `${zustand.label} · ${formatiereDatum(pinPunkt.date)}${pinPunkt.istAggregiert ? ` (Ø ${pinPunkt.tageImBucket} Tage)` : ''}`
    : `${zustand.label} · Mittelwerte ${spanne}`
  const zeigeExtrem = pinPunkt && !pinPunkt.istAggregiert && pinPunkt.temp_max != null && pinPunkt.temp_min != null

  return (
    <div>
      {/* Kopfkarte: angehefteter Tag (Klick) oder beobachtete Periodenmittel, keine Vorhersage */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap',
        padding: '12px 14px', marginBottom: 14,
        border: `1px solid ${pinPunkt ? 'var(--text-muted)' : 'var(--border)'}`, borderRadius: 8, background: 'var(--bg-card)',
      }}>
        <ZustandIcon typ={zustand.icon} size={40} />
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <span style={{ fontSize: 22, fontWeight: 500, color: 'var(--text-primary)', lineHeight: 1.1 }}>
            {anzeige.temp != null ? anzeige.temp.toFixed(1) : '–'} °C
          </span>
          <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
            {unterzeile}
            {pinPunkt && (
              <button onClick={() => setPinPunkt(null)} style={{
                marginLeft: 8, background: 'transparent', color: 'var(--text-secondary)',
                border: 'none', textDecoration: 'underline', cursor: 'pointer', fontSize: 12, padding: 0,
              }}>× lösen</button>
            )}
          </span>
        </div>
        <div style={{ display: 'flex', gap: 18, flexWrap: 'wrap', marginLeft: 'auto' }}>
          {zeigeExtrem && (
            <>
              <StatKachel farbe={C_HOCH} label="Tageshoch" wert={`${pinPunkt.temp_max.toFixed(1)} °C`} />
              <StatKachel farbe={C_TIEF} label="Tagestief" wert={`${pinPunkt.temp_min.toFixed(1)} °C`} />
            </>
          )}
          {anzeige.niederschlag != null &&
            <StatKachel farbe={GROESSEN.niederschlag.farbe} label="Niederschlag" wert={`${anzeige.niederschlag.toFixed(1)} mm/Tag`} />}
          {anzeige.sonne != null &&
            <StatKachel farbe={GROESSEN.sonne.farbe} label="Globalstrahlung" wert={`${anzeige.sonne.toFixed(0)} W/m²`} />}
          {anzeige.wolken != null &&
            <StatKachel farbe={C_WOLKEN} label="Bewölkung" wert={`${anzeige.wolken.toFixed(0)} %`} />}
          {anzeige.wind != null &&
            <StatKachel farbe={C_WIND} label="Wind" wert={`${anzeige.wind.toFixed(1)} m/s`} />}
        </div>
      </div>

      {/* Toggle-Buttons */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 10, flexWrap: 'wrap', alignItems: 'center' }}>
        {Object.values(GROESSEN).map(g => {
          const an = aktiv.includes(g.key)
          return (
            <button key={g.key} onClick={() => toggle(g.key)} style={{
              border: `1px solid ${an ? g.farbe : 'var(--border)'}`,
              background: an ? `${g.farbe}22` : 'var(--bg-elevated)',
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
          Nationaler Tagesdurchschnitt aus 18 Kantonsstationen (Open-Meteo). Temperatur in Grad Celsius, Niederschlag als Tagessumme in Millimetern, Globalstrahlung als Tagesdurchschnitt der kurzwelligen Einstrahlung in Watt pro Quadratmeter. Jede Grösse hat eine eigene Achse, die Kurven sind daher nicht direkt gegeneinander ablesbar, nur ihr zeitlicher Verlauf. Bei langen Zeiträumen werden mehrere Tage zu einem Punkt gemittelt. Die Kopfkarte zeigt die beobachteten Mittelwerte des gewählten Zeitraums; ein Klick auf die Zeitreihe heftet einen einzelnen Tag an, samt Tageshoch und Tagestief. Keine Vorhersage. Daten ab 2017. Synchron zum Zeitraumfilter oben.
        </QuickInfo>
      </div>

      <div style={{ width: '100%', height: 260 }}>
        <ResponsiveContainer>
          <ComposedChart data={gefiltert} margin={{ top: 10, right: 8, bottom: 4, left: 4 }}
                         onClick={chartGeklickt}>
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

            <Tooltip content={<WetterTooltip aktiv={aktiv} onAktiv={merkePunkt} />} />

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
