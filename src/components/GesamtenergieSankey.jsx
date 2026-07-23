import { useMemo, useState } from 'react'
import * as d3 from 'd3'
import { sankey, sankeyLinkHorizontal, sankeyLeft } from 'd3-sankey'
import { useJson } from '../hooks/useJson'
import { JahrDropdown } from './JahrDropdown'

const W = 900
const H = 520
const MARGIN = { top: 10, right: 150, bottom: 10, left: 150 }

// Feste Reihenfolge für Nodes: Träger links, Verwendungen rechts
const TRAEGER = [
  'Elektrizität', 'Erdölprodukte', 'Gas', 'Fernwärme',
  'Holzenergie', 'Uebrige erneuerbare Energien',
  'Müll und Industrieabfälle', 'Kohle',
]
const VERWENDUNG = [
  'Haushalte', 'Industrie', 'Verkehr', 'Dienstleistungen',
  'Landwirtschaft', 'Nichtenergetisch', 'Verluste', 'Export',
]

const FARBEN = {
  // Träger
  'Elektrizität':                '#8a6fbf',
  'Erdölprodukte':               '#b0552f',
  'Gas':                         '#e0a234',
  'Fernwärme':                   '#c93d3d',
  'Holzenergie':                 '#8b6b3d',
  'Uebrige erneuerbare Energien': '#4a9d7c',
  'Müll und Industrieabfälle':   '#7a8a9a',
  'Kohle':                       '#3a3a3a',
  // Verwendung
  'Haushalte':        '#4c9be0',
  'Industrie':        '#2b6cb0',
  'Verkehr':          '#efb23a',
  'Dienstleistungen': '#6fc3b8',
  'Landwirtschaft':   '#8fbf5a',
  'Nichtenergetisch': '#9aa0a6',
  'Verluste':         '#5a5a5a',
  'Export':           '#2b8a78',
}

// Kurze Labels für die Anzeige
const LABEL = {
  'Uebrige erneuerbare Energien': 'Übrige EE',
  'Müll und Industrieabfälle':    'Müll',
}
const kurz = (name) => LABEL[name] || name

// Dezente, einfarbige SVG-Glyphen je Kategorie (14x14). fill/stroke erben
// die Node-Farbe über currentColor. Nur die sichtbaren Kategorien sind
// belegt; fehlt ein Icon, wird schlicht keines gezeichnet.
const ICON = {
  'Elektrizität':                <path d="M8 1 L3 8 H6.5 L6 13 L11 6 H7.5 Z" />,
  'Erdölprodukte':               <path d="M7 1 C7 1 2.5 6.5 2.5 9.5 A4.5 4.5 0 0 0 11.5 9.5 C11.5 6.5 7 1 7 1 Z" />,
  'Gas':                         <path d="M7 1 C9 4 10.5 5 9.8 8.5 A3.3 3.3 0 1 1 4.2 8.5 C3.9 6.8 5 6 5 4.2 C6 5.2 7 5 7 1 Z" />,
  'Fernwärme':                   <path d="M3 4 Q5 2 7 4 T11 4 M3 7 Q5 5 7 7 T11 7 M3 10 Q5 8 7 10 T11 10" fill="none" stroke="currentColor" strokeWidth="1.2" />,
  'Holzenergie':                 <g><rect x="2" y="5.5" width="10" height="3.5" rx="1.75" /><circle cx="4" cy="7.25" r="0.8" fill="#0a0c12" /></g>,
  'Uebrige erneuerbare Energien': <path d="M12 2 C5.5 2 2 5.5 2 12 C8.5 12 12 8.5 12 2 Z M4 10 L10 4" fill="currentColor" stroke="#0a0c12" strokeWidth="0.6" />,
  'Haushalte':        <path d="M7 1.5 L12.5 6 H11 V12 H3 V6 H1.5 Z" />,
  'Industrie':        <path d="M2 12 V6 L5.5 8 V6 L9 8 V4 H12 V12 Z" />,
  'Verkehr':          <g><path d="M2.5 9 L3.7 6 H10.3 L11.5 9 V10.7 H2.5 Z" /><circle cx="4.7" cy="10.8" r="1.1" /><circle cx="9.3" cy="10.8" r="1.1" /></g>,
  'Dienstleistungen': <g><rect x="3.5" y="2" width="7" height="10" /><rect x="5" y="4" width="1.4" height="1.4" fill="#0a0c12" /><rect x="7.6" y="4" width="1.4" height="1.4" fill="#0a0c12" /><rect x="5" y="7" width="1.4" height="1.4" fill="#0a0c12" /><rect x="7.6" y="7" width="1.4" height="1.4" fill="#0a0c12" /></g>,
  'Landwirtschaft':   <path d="M2 12 C2 8 4.5 6 7 6 C7 9 5 12 2 12 Z M12 12 C12 8 9.5 6 7 6" fill="currentColor" stroke="#0a0c12" strokeWidth="0.5" />,
  'Export':           <path d="M2 7 H9 M6 3.5 L10.5 7 L6 10.5" fill="none" stroke="currentColor" strokeWidth="1.4" />,
}

// Icon rendern: kleines g, das die Node-Farbe erbt
function NodeIcon({ name, x, y, farbe }) {
  if (!ICON[name]) return null
  return (
    <g transform={`translate(${x},${y})`} color={farbe} fill={farbe} style={{ pointerEvents: 'none' }}>
      {ICON[name]}
    </g>
  )
}

const ICON_SIZE = 14

export function GesamtenergieSankey() {
  const { data } = useJson('/data/gesamtenergie_sankey.json')
  const [jahr, setJahr] = useState(2024)
  const [hover, setHover] = useState(null)
  const [locked, setLocked] = useState(null)

  // Hover zeigt eine Vorschau, Klick fixiert die Auswahl.
  const active = hover || locked

  const jahre = useMemo(() => {
    if (!data) return [2000, 2024]
    return Object.keys(data).map(Number).sort((a, b) => a - b)
  }, [data])

  const { nodes, links, total } = useMemo(() => {
    if (!data || !data[jahr]) return { nodes: [], links: [], total: 0 }
    const rohLinks = data[jahr]

    // Alle Nodes ableiten und in fester Reihenfolge platzieren
    const nodeNames = []
    for (const t of TRAEGER) if (rohLinks.some(l => l.source === t)) nodeNames.push(t)
    for (const v of VERWENDUNG) if (rohLinks.some(l => l.target === v)) nodeNames.push(v)
    const nodeIndex = Object.fromEntries(nodeNames.map((n, i) => [n, i]))
    const inputNodes = nodeNames.map(n => ({ name: n, kategorie: TRAEGER.includes(n) ? 'traeger' : 'verwendung' }))
    const inputLinks = rohLinks.map(l => ({
      source: nodeIndex[l.source],
      target: nodeIndex[l.target],
      value: l.value,
    }))

    const gen = sankey()
      .nodeWidth(14)
      .nodePadding(10)
      .nodeAlign(sankeyLeft)
      .iterations(32)   // mehr Relaxationsschritte -> weniger Kreuzungen
      .extent([[MARGIN.left, MARGIN.top], [W - MARGIN.right, H - MARGIN.bottom]])

    const graph = gen({ nodes: inputNodes.map(n => ({ ...n })), links: inputLinks.map(l => ({ ...l })) })

    const gesamt = rohLinks.reduce((s, l) => s + l.value, 0)
    return { nodes: graph.nodes, links: graph.links, total: gesamt }
  }, [data, jahr])

  if (!data) return <p style={{ color: 'var(--text-muted)' }}>Lade Daten…</p>

  const linkPath = sankeyLinkHorizontal()

  // Klick auf einen Node/Link fixiert die Auswahl bzw. hebt sie wieder auf
  const toggleNode = (name, wert) => setLocked(prev =>
    prev && prev.type === 'node' && prev.name === name ? null : { type: 'node', name, value: wert })
  const toggleLink = (i, l) => setLocked(prev =>
    prev && prev.type === 'link' && prev.i === i ? null : { type: 'link', i, source: l.source.name, target: l.target.name, value: l.value })

  return (
    <div>
      {/* Auswahlleiste */}
      <div style={{
        display: 'flex', gap: 14, marginBottom: 14, alignItems: 'center', flexWrap: 'wrap',
        padding: '10px 12px', border: '1px solid var(--border)', borderRadius: 6,
      }}>
        <span style={{ fontSize: 11, color: 'var(--text-muted)', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
          Jahr
        </span>
        <JahrDropdown wert={jahr} optionen={jahre} onChange={setJahr} />
        <div style={{ marginLeft: 'auto', display: 'flex', gap: 20, alignItems: 'center' }}>
          {locked && (
            <button onClick={() => setLocked(null)} style={{
              fontSize: 11, color: 'var(--text-secondary)', background: 'transparent',
              border: '1px solid var(--border)', borderRadius: 5, padding: '3px 8px', cursor: 'pointer',
            }}>
              Auswahl aufheben
            </button>
          )}
          <span style={{ fontSize: 12, color: 'var(--text-secondary)' }}>
            Endenergieverbrauch <span style={{ color: 'var(--text-primary)', fontWeight: 500 }}>{total.toFixed(1)} TWh</span>
          </span>
        </div>
      </div>

      {/* Sankey-SVG */}
      <div style={{ position: 'relative' }}>
        <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: 'auto', userSelect: 'none' }}
          onClick={() => setLocked(null)}>
          {/* Links (Flüsse) */}
          <g>
            {links.map((l, i) => {
              const farbe = FARBEN[l.source.name] || '#666'
              const istHervor = active && (active.type === 'link' && active.i === i
                || active.type === 'node' && (active.name === l.source.name || active.name === l.target.name))
              return (
                <path key={i} d={linkPath(l)} fill="none"
                  stroke={farbe}
                  strokeOpacity={active ? (istHervor ? 0.8 : 0.08) : 0.35}
                  strokeWidth={Math.max(1, l.width)}
                  style={{ cursor: 'pointer' }}
                  onMouseEnter={() => setHover({ type: 'link', i, source: l.source.name, target: l.target.name, value: l.value })}
                  onMouseLeave={() => setHover(null)}
                  onClick={(e) => { e.stopPropagation(); toggleLink(i, l) }} />
              )
            })}
          </g>

          {/* Nodes */}
          <g>
            {nodes.map(n => {
              const farbe = FARBEN[n.name] || '#888'
              const istHervor = active && ((active.type === 'node' && active.name === n.name)
                || (active.type === 'link' && (active.source === n.name || active.target === n.name)))
              const gedimmt = active && !istHervor
              const wert = (n.value || 0)
              const cy = (n.y0 + n.y1) / 2
              const istTraeger = n.kategorie === 'traeger'
              // Icon aussen neben dem Balken, Text dahinter
              const iconX = istTraeger ? n.x0 - 6 - ICON_SIZE : n.x1 + 6
              const textX = istTraeger ? n.x0 - 6 - ICON_SIZE - 4 : n.x1 + 6 + ICON_SIZE + 4
              return (
                <g key={n.name}
                  onMouseEnter={() => setHover({ type: 'node', name: n.name, value: wert })}
                  onMouseLeave={() => setHover(null)}
                  onClick={(e) => { e.stopPropagation(); toggleNode(n.name, wert) }}
                  style={{ cursor: 'pointer', opacity: gedimmt ? 0.4 : 1 }}>
                  <rect x={n.x0} y={n.y0} width={n.x1 - n.x0} height={Math.max(1, n.y1 - n.y0)}
                    fill={farbe} fillOpacity={0.9}
                    stroke="#0a0c12" strokeWidth={0.6} />
                  {(n.y1 - n.y0) >= 12 && (
                    <NodeIcon name={n.name} x={iconX} y={cy - ICON_SIZE / 2} farbe={farbe} />
                  )}
                  {(n.y1 - n.y0) >= 10 && (
                    <text x={textX}
                      y={cy}
                      dy="0.35em"
                      textAnchor={istTraeger ? 'end' : 'start'}
                      fontSize={11}
                      fill="var(--text-primary)"
                      style={{ userSelect: 'none', pointerEvents: 'none' }}>
                      {kurz(n.name)}
                    </text>
                  )}
                  {(n.y1 - n.y0) >= 22 && (
                    <text x={textX}
                      y={cy + 12}
                      textAnchor={istTraeger ? 'end' : 'start'}
                      fontSize={10}
                      fill="var(--text-muted)"
                      style={{ userSelect: 'none', pointerEvents: 'none' }}>
                      {wert.toFixed(1)} TWh
                    </text>
                  )}
                </g>
              )
            })}
          </g>
        </svg>

        {/* Tooltip */}
        {active && (
          <div style={{
            position: 'absolute', top: 8, left: '50%', transform: 'translateX(-50%)', pointerEvents: 'none',
            background: 'var(--bg-elevated)', border: '1px solid var(--border)', borderRadius: 8,
            padding: '8px 12px', fontSize: 12, color: 'var(--text-primary)', maxWidth: 320,
          }}>
            {active.type === 'link' ? (
              <>
                <div style={{ fontWeight: 500 }}>{kurz(active.source)} → {kurz(active.target)}</div>
                <div style={{ color: 'var(--text-secondary)' }}>{active.value.toFixed(2)} TWh ({(active.value / total * 100).toFixed(1)}%)</div>
              </>
            ) : (
              <>
                <div style={{ fontWeight: 500 }}>{kurz(active.name)}</div>
                <div style={{ color: 'var(--text-secondary)' }}>{active.value.toFixed(2)} TWh ({(active.value / total * 100).toFixed(1)}%)</div>
              </>
            )}
          </div>
        )}
      </div>

      <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 8 }}>
        Datenquelle: BFE Gesamtenergiestatistik (opendata.swiss OGD115). Endenergieverbrauch je Träger und Sektor plus nichtenergetischer Verbrauch, Umwandlungs- und Netzverluste sowie Nettoexport der Elektrizität. Rohöl und Kernbrennstoffe werden in der Sankey nicht separat gezeigt, da sie vollständig zu Erdölprodukten bzw. Elektrizität umgewandelt werden.
      </div>
    </div>
  )
}