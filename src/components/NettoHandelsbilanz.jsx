import { useMemo } from 'react'
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, ResponsiveContainer,
} from 'recharts'
import { useJson } from '../hooks/useJson'

const C_IMPORT = '#4c9be0'
const C_EXPORT = '#efb23a'

// Gleiche Datenbasis wie EnergieFluss.jsx: pro Zeile ein Monat + richtung_code (z.B. DE_CH, CH_DE)
function baueNettoZeitreihe(data, brushRange, fokusLand) {
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

  // Pro Datum Export- und Importsumme über alle relevanten Länder aufaddieren
  const perDatum = new Map()
  for (const r of zeilen) {
    const istExport = r.richtung_code.startsWith('CH_')
    const istImport = r.richtung_code.endsWith('_CH')
    if (!istExport && !istImport) continue
    const eintrag = perDatum.get(r.date) || { export: 0, import: 0 }
    if (istExport) eintrag.export += r.energie_mwh
    if (istImport) eintrag.import += r.energie_mwh
    perDatum.set(r.date, eintrag)
  }

  return [...perDatum.entries()]
    .map(([date, { export: exp, import: imp }]) => ({
      date,
      dateLabel: new Date(date).toLocaleDateString('de-CH', { month: 'short', year: '2-digit' }),
      netto: +((exp - imp) / 1000).toFixed(1), // GWh, positiv = Exportüberschuss
    }))
    .sort((a, b) => Date.parse(a.date) - Date.parse(b.date))
}

function NettoTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  const v = payload[0].value
  const richtung = v >= 0 ? 'Exportüberschuss' : 'Importüberschuss'
  return (
    <div style={{
      background: 'var(--bg-elevated)', border: '1px solid var(--border, #2a2d3a)',
      borderRadius: 6, padding: '8px 12px', fontSize: 12, color: 'var(--text-secondary)',
    }}>
      <div style={{ marginBottom: 4, opacity: 0.7 }}>{label}</div>
      <div>{richtung}: {Math.abs(v).toFixed(1)} GWh</div>
    </div>
  )
}

const LAND_NAME = { DE: 'Deutschland', FR: 'Frankreich', AT: 'Österreich', IT: 'Italien' }

export function NettoHandelsbilanz({ brushRange, fokusLand, onZeitpunktKlick }) {
  const { data } = useJson('/data/grenzfluss_monat.json')

  const reihe = useMemo(() => {
    if (!data) return null
    return baueNettoZeitreihe(data, brushRange, fokusLand)
  }, [data, brushRange, fokusLand])

  if (!reihe) return <p style={{ color: 'var(--text-muted)' }}>Lade Flussdaten…</p>
  if (reihe.length === 0) return <p style={{ color: 'var(--text-muted)' }}>Kein Handel für den gewählten Zeitraum.</p>

  // Zweifarbiger Gradient: oberhalb 0 Gold (Export), unterhalb Blau (Import)
  const werte = reihe.map(d => d.netto)
  const max = Math.max(...werte, 0)
  const min = Math.min(...werte, 0)
  const spanne = max - min
  const nulloffset = spanne === 0 ? 0.5 : max / spanne

  return (
    <div style={{ width: '100%' }}>
      <h3 style={{ fontSize: 14, fontWeight: 500, color: 'var(--text-secondary)', margin: '0 0 8px' }}>
        {fokusLand ? `Netto-Handelsbilanz ${LAND_NAME[fokusLand]}` : 'Netto-Handelsbilanz'}
      </h3>
      <ResponsiveContainer width="100%" height={220}>
        <AreaChart data={reihe} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="nettoGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset={0} stopColor={C_EXPORT} stopOpacity={0.85} />
              <stop offset={nulloffset} stopColor={C_EXPORT} stopOpacity={0.85} />
              <stop offset={nulloffset} stopColor={C_IMPORT} stopOpacity={0.85} />
              <stop offset={1} stopColor={C_IMPORT} stopOpacity={0.85} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border, #2a2d3a)" vertical={false} />
          <XAxis dataKey="dateLabel" tick={{ fontSize: 10, fill: 'var(--text-muted)' }} axisLine={false} tickLine={false} />
          <YAxis
            tick={{ fontSize: 10, fill: 'var(--text-muted)' }}
            axisLine={false} tickLine={false}
            width={40}
            label={{ value: 'GWh', angle: -90, position: 'insideLeft', fontSize: 10, fill: 'var(--text-muted)' }}
          />
          <ReferenceLine y={0} stroke="var(--text-muted)" strokeDasharray="4 4" />
          <Tooltip content={<NettoTooltip />} />
          <Area
            type="monotone" dataKey="netto"
            stroke="url(#nettoGradient)" strokeWidth={2}
            fill="url(#nettoGradient)" fillOpacity={0.35}
            isAnimationActive={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
