import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { useJson } from '../hooks/useJson'

export function VerbrauchLine() {
  const { data, loading } = useJson('/data/verbrauch_national_monthly.json')
  if (loading) return <p>Lade Daten…</p>

  return (
    <div style={{ width: '100%', height: 360 }}>
      <ResponsiveContainer>
        <LineChart data={data} margin={{ top: 10, right: 20, bottom: 10, left: 10 }}>
          <XAxis dataKey="date" tick={{ fontSize: 11 }} minTickGap={40} />
          <YAxis tick={{ fontSize: 11 }} width={70}
                 tickFormatter={v => (v / 1000).toFixed(0) + ' GWh'} />
          <Tooltip />
          <Line dataKey="mwh" stroke="#2b7" dot={false} strokeWidth={1.5} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}