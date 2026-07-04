import { useMemo } from 'react'
import { useJson } from '../hooks/useJson'

const LAND = { DE: 'Deutschland', FR: 'Frankreich', AT: 'Österreich', IT: 'Italien' }
const REIHENFOLGE = ['DE', 'FR', 'AT', 'IT']

const C_IMPORT = '#4c9be0'
const C_EXPORT = '#efb23a'

function summierePro(data, brushRange) {
  let zeilen = data
  if (brushRange) {
    const [s, e] = brushRange
    zeilen = data.filter(r => {
      const t = Date.parse(r.date)
      return t >= s && t <= e
    })
  }
  // {DE: {imp, exp}, ...}
  const pro = Object.fromEntries(REIHENFOLGE.map(l => [l, { imp: 0, exp: 0 }]))
  for (const r of zeilen) {
    const code = r.richtung_code
    if (code.endsWith('_CH')) {
      const land = code.slice(0, 2)
      if (pro[land]) pro[land].imp += r.energie_mwh
    } else if (code.startsWith('CH_')) {
      const land = code.slice(3, 5)
      if (pro[land]) pro[land].exp += r.energie_mwh
    }
  }
  return pro
}

function Balken({ wert, max, farbe, ausrichtung }) {
  // ausrichtung: 'links' = wächst nach links (Import), 'rechts' = wächst nach rechts (Export)
  const anteil = max > 0 ? (wert / max) * 100 : 0
  return (
    <div style={{
      position: 'relative', height: 10, background: 'var(--border, #2a2d3a)',
      borderRadius: 2, overflow: 'hidden',
    }}>
      <div style={{
        position: 'absolute', top: 0, bottom: 0,
        [ausrichtung === 'links' ? 'right' : 'left']: 0,
        width: `${anteil}%`,
        background: farbe, opacity: 0.85,
      }} />
    </div>
  )
}

export function HandelsbilanzLaender({ brushRange, fokusLand, onLandKlick }) {
  const { data } = useJson('/data/grenzfluss_monat.json')

  const zeilen = useMemo(() => {
    if (!data) return null
    const pro = summierePro(data, brushRange)
    const maxWert = Math.max(
      ...REIHENFOLGE.flatMap(l => [pro[l].imp, pro[l].exp]),
      1,
    )
    return REIHENFOLGE.map(land => {
      const { imp, exp } = pro[land]
      const netto = exp - imp
      return {
        land,
        name: LAND[land],
        impGwh: imp / 1000,
        expGwh: exp / 1000,
        nettoGwh: netto / 1000,
        maxWert,
      }
    })
  }, [data, brushRange])

  if (!zeilen) return null

  return (
    <div>
      <h3 style={{ fontSize: 14, fontWeight: 500, color: 'var(--text-secondary)', margin: '0 0 12px' }}>
        Handelsbilanz je Land
      </h3>

      {/* Kopfzeile */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '110px 1fr 1fr 90px',
        gap: 12, alignItems: 'center',
        fontSize: 10, color: 'var(--text-muted)',
        textTransform: 'uppercase', letterSpacing: '0.08em',
        paddingBottom: 6, borderBottom: '1px solid var(--border, #2a2d3a)',
      }}>
        <span>Land</span>
        <span style={{ textAlign: 'right' }}>Import (GWh)</span>
        <span>Export (GWh)</span>
        <span style={{ textAlign: 'right' }}>Saldo</span>
      </div>

      {zeilen.map(z => {
        const istExport = z.nettoGwh >= 0
        const istFokus = fokusLand === z.land
        const gedimmt = fokusLand && !istFokus
        const klickbar = !!onLandKlick
        return (
          <div key={z.land}
            onClick={() => klickbar && onLandKlick(z.land)}
            style={{
              display: 'grid',
              gridTemplateColumns: '110px 1fr 1fr 90px',
              gap: 12, alignItems: 'center',
              padding: '10px 6px', borderBottom: '1px solid var(--border, #2a2d3a)',
              opacity: gedimmt ? 0.4 : 1,
              background: istFokus ? 'rgba(255,255,255,0.04)' : 'transparent',
              borderRadius: 4,
              cursor: klickbar ? 'pointer' : 'default',
              transition: 'background 120ms, opacity 120ms',
            }}>
            <span style={{
              fontSize: 13,
              color: 'var(--text-primary)',
              fontWeight: istFokus ? 500 : 400,
            }}>{z.name}</span>

            {/* Import: nach links wachsend */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ flex: 1, fontSize: 12, color: 'var(--text-secondary)', textAlign: 'right', minWidth: 42 }}>
                {z.impGwh.toFixed(0)}
              </span>
              <div style={{ flex: 2 }}>
                <Balken wert={z.impGwh} max={z.maxWert / 1000} farbe={C_IMPORT} ausrichtung="links" />
              </div>
            </div>

            {/* Export: nach rechts wachsend */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{ flex: 2 }}>
                <Balken wert={z.expGwh} max={z.maxWert / 1000} farbe={C_EXPORT} ausrichtung="rechts" />
              </div>
              <span style={{ flex: 1, fontSize: 12, color: 'var(--text-secondary)', minWidth: 42 }}>
                {z.expGwh.toFixed(0)}
              </span>
            </div>

            <span style={{
              textAlign: 'right', fontSize: 13, fontWeight: 500,
              color: istExport ? C_EXPORT : C_IMPORT,
            }}>
              {istExport ? '+' : '−'}{Math.abs(z.nettoGwh).toFixed(0)} GWh
            </span>
          </div>
        )
      })}
    </div>
  )
}
