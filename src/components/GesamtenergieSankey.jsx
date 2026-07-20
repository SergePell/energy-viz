import { useMemo, useState } from 'react'
import * as d3 from 'd3'
import { sankey, sankeyLinkHorizontal, sankeyLeft } from 'd3-sankey'
import { useJson } from '../hooks/useJson'
import { JahrDropdown } from './JahrDropdown'

const W = 900
const H = 520
const MARGIN = { top: 10, right: 140, bottom: 10, left: 140 }

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

export function GesamtenergieSankey() {
  const { data } = useJson('/data/gesamtenergie_sankey.json')
  const [jahr, setJahr] = useState(2024)
  const [hover, setHover] = useState(null)

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
      .extent([[MARGIN.left, MARGIN.top], [W - MARGIN.right, H - MARGIN.bottom]])

    const graph = gen({ nodes: inputNodes.map(n => ({ ...n })), links: inputLinks.map(l => ({ ...l })) })

    const gesamt = rohLinks.reduce((s, l) => s + l.value, 0)
    return { nodes: graph.nodes, links: graph.links, total: gesamt }
  }, [data, jahr])

  if (!data) return <p style={{ color: 'var(--text-muted)' }}>Lade Daten…</p>

  const linkPath = sankeyLinkHorizontal()

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
          <span style={{ fontSize: 12, color: 'var(--text-secondary)' }}>
            Endenergieverbrauch <span style={{ color: 'var(--text-primary)', fontWeight: 500 }}>{total.toFixed(1)} TWh</span>
          </span>
        </div>
      </div>

      {/* Sankey-SVG */}
      <div style={{ position: 'relative' }}>
        <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: 'auto', userSelect: 'none' }}>
          {/* Links (Flüsse) */}
          <g>
            {links.map((l, i) => {
              const farbe = FARBEN[l.source.name] || '#666'
              const istHervor = hover && (hover.type === 'link' && hover.i === i
                || hover.type === 'node' && (hover.name === l.source.name || hover.name === l.target.name))
              return (
                <path key={i} d={linkPath(l)} fill="none"
                  stroke={farbe}
                  strokeOpacity={hover ? (istHervor ? 0.75 : 0.15) : 0.35}
                  strokeWidth={Math.max(1, l.width)}
                  style={{ cursor: 'pointer' }}
                  onMouseEnter={() => setHover({ type: 'link', i, source: l.source.name, target: l.target.name, value: l.value })}
                  onMouseLeave={() => setHover(null)} />
              )
            })}
          </g>

          {/* Nodes */}
          <g>
            {nodes.map(n => {
              const farbe = FARBEN[n.name] || '#888'
              const istHervor = hover && ((hover.type === 'node' && hover.name === n.name)
                || (hover.type === 'link' && (hover.source === n.name || hover.target === n.name)))
              const wert = (n.value || 0)
              return (
                <g key={n.name}
                  onMouseEnter={() => setHover({ type: 'node', name: n.name, value: wert })}
                  onMouseLeave={() => setHover(null)}
                  style={{ cursor: 'pointer' }}>
                  <rect x={n.x0} y={n.y0} width={n.x1 - n.x0} height={Math.max(1, n.y1 - n.y0)}
                    fill={farbe} fillOpacity={hover && !istHervor ? 0.35 : 0.9}
                    stroke="#0a0c12" strokeWidth={0.6} />
                  {(n.y1 - n.y0) >= 10 && (
                    <text x={n.kategorie === 'traeger' ? n.x0 - 6 : n.x1 + 6}
                      y={(n.y0 + n.y1) / 2}
                      dy="0.35em"
                      textAnchor={n.kategorie === 'traeger' ? 'end' : 'start'}
                      fontSize={11}
                      fill="var(--text-primary)"
                      style={{ userSelect: 'none', pointerEvents: 'none' }}>
                      {kurz(n.name)}
                    </text>
                  )}
                  {(n.y1 - n.y0) >= 22 && (
                    <text x={n.kategorie === 'traeger' ? n.x0 - 6 : n.x1 + 6}
                      y={(n.y0 + n.y1) / 2 + 12}
                      textAnchor={n.kategorie === 'traeger' ? 'end' : 'start'}
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
        {hover && (
          <div style={{
            position: 'absolute', top: 8, left: '50%', transform: 'translateX(-50%)', pointerEvents: 'none',
            background: 'var(--bg-elevated)', border: '1px solid var(--border)', borderRadius: 8,
            padding: '8px 12px', fontSize: 12, color: 'var(--text-primary)', maxWidth: 320,
          }}>
            {hover.type === 'link' ? (
              <>
                <div style={{ fontWeight: 500 }}>{kurz(hover.source)} → {kurz(hover.target)}</div>
                <div style={{ color: 'var(--text-secondary)' }}>{hover.value.toFixed(2)} TWh ({(hover.value / total * 100).toFixed(1)}%)</div>
              </>
            ) : (
              <>
                <div style={{ fontWeight: 500 }}>{kurz(hover.name)}</div>
                <div style={{ color: 'var(--text-secondary)' }}>{hover.value.toFixed(2)} TWh ({(hover.value / total * 100).toFixed(1)}%)</div>
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
