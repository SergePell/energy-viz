import { useMemo } from 'react'
import { sankey, sankeyLinkHorizontal } from 'd3-sankey'
import { useJson } from '../hooks/useJson'

// Ländercodes zu Klartext
const LAND = { AT: 'Österreich', DE: 'Deutschland', FR: 'Frankreich', IT: 'Italien' }
const LAENDER = ['DE', 'FR', 'AT', 'IT']

function baueGraph(data, brushRange) {
  // 1. Zeitraum filtern
  let zeilen = data
  if (brushRange) {
    const [s, e] = brushRange
    zeilen = data.filter(r => {
      const t = Date.parse(r.date)
      return t >= s && t <= e
    })
  }

  // 2. Summe je Richtung über den Zeitraum
  const summe = {}
  for (const r of zeilen) {
    summe[r.richtung_code] = (summe[r.richtung_code] || 0) + r.energie_mwh
  }

  // 3. Knoten anlegen: Länder links (Import), Schweiz Mitte, Länder rechts (Export)
  const nodes = []
  const index = {}
  function knoten(id, name) {
    if (index[id] === undefined) {
      index[id] = nodes.length
      nodes.push({ id, name })
    }
    return index[id]
  }

  LAENDER.forEach(l => knoten('imp_' + l, LAND[l]))   // links
  knoten('CH', 'Schweiz')                              // Mitte
  LAENDER.forEach(l => knoten('exp_' + l, LAND[l]))   // rechts

  // 4. Kanten anlegen
  const links = []
  for (const l of LAENDER) {
    const imp = summe[l + '_CH'] || 0     // z. B. DE_CH
    const exp = summe['CH_' + l] || 0     // z. B. CH_DE
    if (imp > 0) links.push({ source: index['imp_' + l], target: index['CH'], value: imp })
    if (exp > 0) links.push({ source: index['CH'], target: index['exp_' + l], value: exp })
  }

  return { nodes, links }
}

const W = 720, H = 400
const C_IMPORT = '#4c9be0'
const C_EXPORT = '#efb23a'
const C_CH = '#e24b4a'
const C_LAND = '#2b8a78'

export function EnergieFluss({ brushRange }) {
  const { data } = useJson('/data/grenzfluss_monat.json')

  const graph = useMemo(() => {
    if (!data) return null
    return baueGraph(data, brushRange)
  }, [data, brushRange])

  if (!graph) return <p style={{ color: 'var(--text-muted)' }}>Lade Flussdaten…</p>
  if (graph.links.length === 0) return <p style={{ color: 'var(--text-muted)' }}>Kein Handel für den gewählten Zeitraum.</p>

  const { nodes, links } = sankey()
    .nodeWidth(16)
    .nodePadding(20)
    .extent([[10, 10], [W - 10, H - 10]])({
      nodes: graph.nodes.map(d => ({ ...d })),
      links: graph.links.map(d => ({ ...d })),
    })

  return (
    <div style={{ width: '100%' }}>
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: 'auto' }}>
        {links.map((l, i) => {
          const istImport = l.target.id === 'CH'
          return (
            <path key={i} d={sankeyLinkHorizontal()(l)}
              fill="none" stroke={istImport ? C_IMPORT : C_EXPORT} strokeOpacity={0.45}
              strokeWidth={Math.max(1, l.width)}>
              <title>
                {istImport
                  ? `${l.source.name} → Schweiz: ${(l.value / 1000).toFixed(0)} GWh`
                  : `Schweiz → ${l.target.name}: ${(l.value / 1000).toFixed(0)} GWh`}
              </title>
            </path>
          )
        })}
        {nodes.map((n, i) => {
          const istExport = n.id.startsWith('exp_')
          return (
            <g key={i}>
              <rect x={n.x0} y={n.y0} width={n.x1 - n.x0} height={n.y1 - n.y0}
                fill={n.id === 'CH' ? C_CH : C_LAND} rx={2} />
              <text x={istExport ? n.x0 - 6 : n.x1 + 6}
                y={(n.y0 + n.y1) / 2} dy="0.35em"
                textAnchor={istExport ? 'end' : 'start'}
                fontSize={11} fill="var(--text-secondary)">
                {n.name}
              </text>
            </g>
          )
        })}
        <text x={20} y={H - 4} fontSize={10} fill="var(--text-muted)">Import →</text>
        <text x={W - 20} y={H - 4} textAnchor="end" fontSize={10} fill="var(--text-muted)">← Export</text>
      </svg>
    </div>
  )
}
