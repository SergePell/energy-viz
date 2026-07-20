import { useMemo, useState } from 'react'
import * as d3 from 'd3'
import { useJson } from '../hooks/useJson'
import { QuickInfo } from './QuickInfo'

const W = 600
const H = 380
const JAHR_DATEN = '/data/erzeugung_kanton_2026.json'
const C_HINWEIS = '#ef9f27'

// Farbcode je Anlagentyp (angelehnt an EnergieMix)
const ANLAGE_FARBE = {
  Laufkraftwerk:         '#4c9be0',
  Speicherkraftwerk:     '#2b6cb0',
  Umwälzwerk:            '#2b6cb0',
  Pumpspeicherkraftwerk: '#2b6cb0',
  Kernkraftwerk:         '#8a6fbf',
}

// Zuordnung Anlagenlabel -> Filter-Kategorie
function anlageKategorie(a) {
  if (a.typ === 'Kernkraft') return 'kernkraft'
  if (a.typ_label === 'Pumpspeicherkraftwerk' || a.typ_label === 'Umwälzwerk') return 'pumpspeicher'
  return 'wasserkraft'
}

function firstCoord(geo) {
  let c = geo.features[0].geometry.coordinates
  while (Array.isArray(c[0])) c = c[0]
  return c
}

function fmtDatum(ms) {
  const d = new Date(ms)
  const p = n => String(n).padStart(2, '0')
  return `${p(d.getUTCDate())}.${p(d.getUTCMonth() + 1)}.${String(d.getUTCFullYear()).slice(2)}`
}

export function ChoroplethKarte({ selected, onSelect, brushRange }) {
  const { data: geo } = useJson('/data/kanton_geometry.geojson')
  const { data: jahr } = useJson(JAHR_DATEN)
  const { data: monat } = useJson('/data/erzeugung_kanton_monat.json')
  const { data: anlagen } = useJson('/data/anlagen_standorte.json')
  const [hover, setHover] = useState(null)
  const [hoverAnlage, setHoverAnlage] = useState(null)
  const [zeigen, setZeigen] = useState({ wasserkraft: true, pumpspeicher: true, kernkraft: true })

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

  const { proj, path, viewBox } = useMemo(() => {
    if (!geo) return { proj: null, path: null, viewBox: `0 0 ${W} ${H}` }
    const s = firstCoord(geo)
    const p = Math.abs(s[0]) > 400 ? d3.geoIdentity().reflectY(true) : d3.geoMercator()
    p.fitSize([W, H], geo)
    const pfad = d3.geoPath(p)
    // viewBox eng auf die Kartengrenzen schneiden, damit kein dunkler Rand
    // oben/unten bleibt und die Schweiz die Panelbreite ausfuellt.
    const [[x0, y0], [x1, y1]] = pfad.bounds(geo)
    const pad = 6
    const vb = `${x0 - pad} ${y0 - pad} ${(x1 - x0) + pad * 2} ${(y1 - y0) + pad * 2}`
    return { proj: p, path: pfad, viewBox: vb }
  }, [geo])

  const color = useMemo(() => {
    if (!werte || !werte.length) return null
    const vals = werte.map(d => d.mwh)
    return d3.scaleSequential(d3.interpolateGreens).domain([d3.min(vals), d3.max(vals)])
  }, [werte])

  // Anlagen filtern + projizieren + Radius nach log(Produktion) skalieren
  const marker = useMemo(() => {
    if (!anlagen || !proj) return []
    const gefiltert = anlagen.filter(a => zeigen[anlageKategorie(a)])
    return gefiltert.map(a => {
      const p = proj([a.longitude, a.latitude])
      if (!p || !isFinite(p[0]) || !isFinite(p[1])) return null
      // log-Skala: 20 GWh -> ~2.5, 200 GWh -> ~4.5, 1000 GWh -> ~7, 2000 GWh -> ~8
      const r = 1.6 + Math.log(1 + Math.max(a.produktion_gwh || 0, 5)) * 0.9
      const stillgelegt = a.status_label && a.status_label.toLowerCase().includes('stillgelegt')
      return { ...a, x: p[0], y: p[1], r, stillgelegt }
    })
      .filter(Boolean)
      // grosse zuerst zeichnen, damit kleine oben liegen
      .sort((a, b) => b.r - a.r)
  }, [anlagen, proj, zeigen])



  if (!geo || !path) return <p style={{ color: 'var(--text-muted)' }}>Lade Karte…</p>

  return (
    <div style={{ position: 'relative' }}>
      <div style={{ display: 'flex', gap: 14, marginBottom: 6, fontSize: 12, color: 'var(--text-secondary)', flexWrap: 'wrap' }}>
        {[
          { key: 'wasserkraft',  label: 'Wasserkraft',   farbe: '#4c9be0' },
          { key: 'pumpspeicher', label: 'Pumpspeicher',  farbe: '#2b6cb0' },
          { key: 'kernkraft',    label: 'Kernkraft',     farbe: '#8a6fbf' },
        ].map(t => (
          <label key={t.key} style={{ display: 'inline-flex', alignItems: 'center', gap: 5, cursor: 'pointer' }}>
            <input type="checkbox" checked={zeigen[t.key]}
              onChange={e => setZeigen(z => ({ ...z, [t.key]: e.target.checked }))}
              style={{ accentColor: t.farbe }} />
            <span style={{ width: 9, height: 9, borderRadius: '50%', background: t.farbe }} />
            {t.label}
          </label>
        ))}
        <QuickInfo titel="Anlagen">
          Marker zeigen Kraftwerksstandorte. Radius skaliert mit erwarteter Jahresproduktion (log-Skala). Wasserkraftanlagen ab 20 GWh/Jahr aus WASTA (BFE), alle fünf Schweizer Kernkraftwerke. Umwälz- und Pumpspeicherkraftwerke unter „Pumpspeicher" zusammengefasst. Mühleberg mit gestricheltem Rand als stillgelegte Anlage markiert.
        </QuickInfo>
      </div>

      <svg viewBox={viewBox} style={{ width: '100%', height: 'auto' }}>
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

        {/* Anlagen-Marker als SVG-Kreise, oberhalb der Kantone gezeichnet */}
        {marker.map(a => {
          const farbe = ANLAGE_FARBE[a.typ_label] || '#4c9be0'
          return (
            <circle key={`${a.typ}-${a.name}-${a.longitude.toFixed(3)}-${a.latitude.toFixed(3)}`}
              cx={a.x} cy={a.y} r={a.r}
              fill={farbe}
              fillOpacity={a.stillgelegt ? 0.3 : 0.85}
              stroke={a.stillgelegt ? '#a0a0a0' : '#0a0c12'}
              strokeWidth={a.stillgelegt ? 0.7 : 0.9}
              strokeDasharray={a.stillgelegt ? '2,1.5' : undefined}
              style={{ cursor: 'pointer' }}
              onMouseEnter={() => setHoverAnlage(a)}
              onMouseLeave={() => setHoverAnlage(null)} />
          )
        })}
      </svg>

      {/* Anlagen-Tooltip (oben rechts) — hat Vorrang vor Kantons-Tooltip wenn beide aktiv */}
      {hoverAnlage && (
        <div style={{
          position: 'absolute', top: 34, right: 8, pointerEvents: 'none', maxWidth: 250,
          background: '#12141c', border: '1px solid var(--border)', borderRadius: 8,
          padding: '9px 11px', fontSize: 12, color: 'var(--text-primary)',
          zIndex: 10,
        }}>
          <div style={{ fontWeight: 500 }}>{hoverAnlage.name}</div>
          <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 4 }}>
            {hoverAnlage.standort}
            {hoverAnlage.kanton_code ? `, ${hoverAnlage.kanton_code.replace('CH-', '')}` : ''}
            {hoverAnlage.standort_hinweis ? ` · ${hoverAnlage.standort_hinweis}` : ''}
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'auto auto', gap: '2px 10px', color: 'var(--text-secondary)' }}>
            <span>Typ</span><span style={{ textAlign: 'right' }}>{hoverAnlage.typ_label}</span>
            {hoverAnlage.leistung_mw > 0 && <><span>Leistung</span><span style={{ textAlign: 'right' }}>{hoverAnlage.leistung_mw.toFixed(0)} MW</span></>}
            {hoverAnlage.produktion_gwh > 0 && <><span>Produktion</span><span style={{ textAlign: 'right' }}>{hoverAnlage.produktion_gwh.toFixed(0)} GWh/Jahr</span></>}
            {hoverAnlage.inbetriebnahme_jahr && <><span>Baujahr</span><span style={{ textAlign: 'right' }}>{hoverAnlage.inbetriebnahme_jahr}</span></>}
          </div>
          {hoverAnlage.stillgelegt && (
            <div style={{ marginTop: 6, paddingTop: 6, borderTop: '1px solid var(--border)', fontSize: 11, color: C_HINWEIS }}>
              {hoverAnlage.status_label}
            </div>
          )}
        </div>
      )}

      {/* Kantons-Tooltip (oben links) */}
      {hover && !hoverAnlage && (
        <div style={{
          position: 'absolute', top: 34, left: 8, pointerEvents: 'none', maxWidth: 230,
          background: '#12141c', border: '1px solid var(--border)', borderRadius: 8,
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
