import { useMemo } from 'react'
import { useJson } from '../hooks/useJson'

const C_IMPORT = '#4c9be0'
const C_EXPORT = '#efb23a'

// Gleiche Filterlogik wie EnergieFluss.jsx / NettoHandelsbilanz.jsx
function summiere(data, brushRange, fokusLand) {
  let zeilen = data
  if (brushRange) {
    const [s, e] = brushRange
    zeilen = data.filter(r => {
      const t = Date.parse(r.date)
      return t >= s && t <= e
    })
  }
  if (fokusLand) {
    zeilen = zeilen.filter(r =>
      r.richtung_code === `${fokusLand}_CH` || r.richtung_code === `CH_${fokusLand}`,
    )
  }

  let exportSumme = 0
  let importSumme = 0
  for (const r of zeilen) {
    if (r.richtung_code.startsWith('CH_')) exportSumme += r.energie_mwh
    else if (r.richtung_code.endsWith('_CH')) importSumme += r.energie_mwh
  }
  return { exportSumme, importSumme }
}

const LAND_NAME = { DE: 'Deutschland', FR: 'Frankreich', AT: 'Österreich', IT: 'Italien' }

export function HandelsbilanzKPI({ brushRange, fokusLand }) {
  const { data } = useJson('/data/grenzfluss_monat.json')

  const kennzahlen = useMemo(() => {
    if (!data) return null
    const { exportSumme, importSumme } = summiere(data, brushRange, fokusLand)
    const volumen = exportSumme + importSumme
    const nettoMwh = exportSumme - importSumme
    const anteil = volumen > 0 ? (nettoMwh / volumen) * 100 : 0
    return {
      nettoGwh: nettoMwh / 1000,
      exportGwh: exportSumme / 1000,
      importGwh: importSumme / 1000,
      anteil,
    }
  }, [data, brushRange, fokusLand])

  if (!kennzahlen) return null

  const { nettoGwh, exportGwh, importGwh, anteil } = kennzahlen
  const istExport = nettoGwh >= 0
  const farbe = istExport ? C_EXPORT : C_IMPORT
  const label = istExport ? 'Exportüberschuss' : 'Importüberschuss'

  return (
    <div style={{
      border: '1px solid var(--border, #2a2d3a)', borderRadius: 8,
      padding: '16px 20px', display: 'inline-flex', flexDirection: 'column', gap: 4,
      minWidth: 220,
    }}>
      <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
        {fokusLand ? `Handelsbilanz ${LAND_NAME[fokusLand]}` : 'Handelsbilanz'}
      </span>

      <span style={{ fontSize: 28, fontWeight: 500, color: farbe, lineHeight: 1.1 }}>
        {istExport ? '+' : '−'}{Math.abs(nettoGwh).toFixed(0)} GWh
      </span>

      <span style={{ fontSize: 12, color: 'var(--text-secondary)' }}>
        {label} · {Math.abs(anteil).toFixed(1)}% des Handelsvolumens
      </span>

      <span style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 6 }}>
        Export {exportGwh.toFixed(0)} GWh · Import {importGwh.toFixed(0)} GWh
      </span>
    </div>
  )
}