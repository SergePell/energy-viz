import { useMemo, useState } from 'react'
import * as d3 from 'd3'
import { useJson } from '../hooks/useJson'
import { QuickInfo } from './QuickInfo'

const W = 600
const H = 380
const JAHR_DATEN = '/data/erzeugung_kanton_2026.json'
const C_HINWEIS = '#ef9f27'

function firstCoord(geo) {
  let c = geo.features[0].geometry.coordinates
  while (Array.isArray(c[0])) c = c[0]
  return c
}

function fmtDatum(ms) {
  const d = new Date(ms)
  const p = n => String(n).padStart(2, '0')
  return `${p(d.getDate())}.${p(d.getMonth() + 1)}.${String(d.getFullYear()).slice(2)}`
}

export function ChoroplethKarte({ selected, onSelect, brushRange }) {
  const { data: geo } = useJson('/data/kanton_geometry.geojson')
  const { data: jahr } = useJson(JAHR_DATEN)
  const { data: monat } = useJson('/data/erzeugung_kanton_monat.json')
  const [hover, setHover] = useState(null)

  const werte = useMemo(() => {
    if (brushRange && monat) {
      const [s, e] = brushRange
      const sum = new Map()
      for (const r of monat) {
        const t = Date.parse(r.date)
        if (t >= s && t <= e) {
          const cur = sum.get(r.kanton) || { kanton: r.kanton, mwh: 0 }
          cur.mwh += r.mwh
          sum.set(r.kanton, cur)
        }
      }
      return [...sum.values()]
    }
    return jahr
  }, [brushRange, monat, jahr])

  const keineDaten = brushRange && (!werte || werte.length === 0)
  const vmap = useMemo(() => (werte ? new Map(werte.map(w => [w.kanton, w])) : new Map()), [werte])

  const path = useMemo(() => {
    if (!geo) return null
    const s = firstCoord(geo)
    const proj = Math.abs(s[0]) > 400 ? d3.geoIdentity().reflectY(true) : d3.geoMercator()
    proj.fitSize([W, H], geo)
    return d3.geoPath(proj)
  }, [geo])

  const color = useMemo(() => {
    if (!werte || !werte.length) return null
    const vals = werte.map(d => d.mwh)
    return d3.scaleSequential(d3.interpolateGreens).domain([d3.min(vals), d3.max(vals)])
  }, [werte])

  if (!geo || !path) return <p style={{ color: 'var(--text-muted)' }}>Lade Karte…</p>

  return (
    <div style={{ position: 'relative' }}>
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: 'auto' }}>
        {geo.features.map((f, i) => {
          const code = f.properties.kanton_code
          const v = vmap.get(code)
          const fill = v && color ? color(v.mwh) : 'var(--border)'
          const istGewaehlt = selected === code
          const gedimmt = selected && !istGewaehlt
          return (
            <path key={code || i} d={path(f)} fill={fill}
              stroke={istGewaehlt ? 'var(--text-primary)' : 'var(--bg-card)'}
              strokeWidth={istGewaehlt ? 2 : 0.75}
              style={{ cursor: 'pointer', opacity: gedimmt ? 0.45 : 1 }}
              onClick={() => onSelect && onSelect(code)}
              onMouseEnter={() => setHover({ code, name: f.properties.kanton_name_de || code, v })}
              onMouseLeave={() => setHover(null)} />
          )
        })}
      </svg>

      {hover && (
        <div style={{
          position: 'absolute', top: 8, left: 8, pointerEvents: 'none', maxWidth: 230,
          background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 8,
          padding: '8px 10px', fontSize: 12, color: 'var(--text-primary)',
        }}>
          <div style={{ fontWeight: 500 }}>{hover.name}</div>
          {hover.v
            ? <>
                <div>{(hover.v.mwh / 1000).toFixed(0)} GWh Erzeugung</div>
                {hover.v.ist_gruppe && (
                  <div style={{ color: 'var(--text-muted)' }}>
                    Wert gilt für die Gruppe {hover.v.einheit.replace('CH-', '').replace(/_/g, ', ')}
                  </div>
                )}
              </>
            : <div style={{ color: 'var(--text-muted)' }}>kein Wert für diesen Zeitraum</div>}
        </div>
      )}

      {keineDaten && (
        <div style={{ fontSize: 12, color: C_HINWEIS, marginTop: 6 }}>
          Für den gewählten Zeitraum liegen keine kantonalen Daten vor (erst ab 2015).
        </div>
      )}

      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 6, fontSize: 11, color: 'var(--text-muted)' }}>
        <span>wenig</span>
        <span style={{ flex: 1, height: 8, borderRadius: 4, background: 'linear-gradient(to right, #e5f5e0, #006d2c)' }} />
        <span>viel Erzeugung</span>
        <QuickInfo titel="Farbskala">
          Die Farbe kodiert die erzeugte Energiemenge eines Kantons, dunkler bedeutet mehr Erzeugung. Sieben Swissgrid-Regionen fassen mehrere Kantone zusammen, diese teilen sich denselben Wert. Bei gewähltem Zeitraum zeigt die Karte die Summe über diese Monate, sonst die Jahressumme.
        </QuickInfo>
        {brushRange
          ? <span style={{ marginLeft: 4, color: 'var(--text-secondary)' }}>· Zeitraum {fmtDatum(brushRange[0])}–{fmtDatum(brushRange[1])}</span>
          : <span style={{ marginLeft: 4 }}>· Jahressumme</span>}
        {selected && <span style={{ color: 'var(--text-secondary)' }}>· gewählt: {selected.replace('CH-', '')}</span>}
      </div>
    </div>
  )
}