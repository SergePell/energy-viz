import { useState } from 'react'
import { ChoroplethKarte } from './components/ChoroplethKarte'
import { VerbrauchAnomalie } from './components/VerbrauchAnomalie'
import { EnergieMix } from './components/EnergieMix'
import { EnergieFluss } from './components/EnergieFluss'
import { QuickInfo } from './components/QuickInfo'

const REITER = [
  { id: 'analyse', label: 'Analyse' },
  { id: 'handel', label: 'Grenzüberschreitender Handel' },
]

function App() {
  const [kanton, setKanton] = useState(null)
  const [zeitraum, setZeitraum] = useState(null)
  const [reiter, setReiter] = useState('analyse')
  const waehlen = code => setKanton(prev => (prev === code ? null : code))

  const titel = (text, info) => (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
      <h2 style={{ fontSize: 18, fontWeight: 500, margin: 0, color: 'var(--text-primary)' }}>{text}</h2>
      {info}
    </div>
  )

  return (
    <div style={{ padding: '24px 20px', maxWidth: 1300, margin: '0 auto' }}>
      <p style={{ fontFamily: 'var(--font-mono)', fontSize: 10, letterSpacing: '0.16em', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: 6 }}>
        Visual Analytics · Energie Schweiz
      </p>
      <h1 style={{ fontSize: 30, fontWeight: 400, lineHeight: 1.15, marginBottom: 16, color: 'var(--text-primary)' }}>
        Energie-Dashboard Schweiz
      </h1>

      {/* Reiterleiste */}
      <div style={{ display: 'flex', gap: 4, borderBottom: '1px solid var(--border)', marginBottom: 20 }}>
        {REITER.map(r => (
          <button key={r.id} onClick={() => setReiter(r.id)}
            style={{
              fontSize: 13, padding: '8px 16px', border: 'none', cursor: 'pointer',
              background: 'transparent',
              color: reiter === r.id ? 'var(--text-primary)' : 'var(--text-muted)',
              borderBottom: reiter === r.id ? '2px solid var(--text-primary)' : '2px solid transparent',
              marginBottom: -1, fontWeight: reiter === r.id ? 500 : 400,
            }}>
            {r.label}
          </button>
        ))}
      </div>

      {/* Reiter 1: Analyse */}
      {reiter === 'analyse' && (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: 20, alignItems: 'start' }}>
            <section>
              {titel('Erzeugung pro Kanton',
                <QuickInfo titel="Erzeugung pro Kanton">
                  Erzeugung je Kanton, eingefärbt nach Menge. Sieben Swissgrid-Regionen fassen mehrere Kantone zusammen (z. B. AI, AR), diese teilen sich denselben Wert. Bei gewähltem Zeitraum zeigt die Karte die Summe über diese Monate, sonst die Jahressumme.
                </QuickInfo>)}
              <ChoroplethKarte selected={kanton} onSelect={waehlen} brushRange={zeitraum} />
            </section>

            <section>
              <VerbrauchAnomalie selectedKanton={kanton} onClear={() => setKanton(null)} onBrush={setZeitraum} />
            </section>
          </div>

          <section style={{ marginTop: 24 }}>
            {titel('Energiemix nach Energieträger',
              <QuickInfo titel="Energiemix">
                Monatliche Erzeugung nach Energieträger in GWh, gestapelt. „Andere" und „Thermisch" sind aggregierte Sammelposten der BFE-Bilanz. Vor rund 2020 enthält „Andere" die noch nicht separat ausgewiesenen Träger wie Photovoltaik und Wind, was die grosse Fläche davor erklärt.
              </QuickInfo>)}
            <EnergieMix brushRange={zeitraum} />
          </section>
        </>
      )}

      {/* Reiter 2: Handel */}
      {reiter === 'handel' && (
        <section>
          {titel('Grenzüberschreitender Handel',
            <QuickInfo titel="Grenzüberschreitender Handel">
              Stromflüsse zwischen der Schweiz und den Nachbarländern. Links fliesst der Import in die Schweiz, rechts der Export aus der Schweiz. Die Breite der Bänder zeigt die Menge über den gewählten Zeitraum.
            </QuickInfo>)}
          <EnergieFluss brushRange={zeitraum} />
        </section>
      )}

      <div style={{ marginTop: 24, paddingTop: 12, borderTop: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: 8 }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: 9, color: 'var(--text-muted)', letterSpacing: '0.08em' }}>
          Prototyp · MSc Thesis FHGR
        </span>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: 9, color: 'var(--text-muted)' }}>
          Daten: Swissgrid, BFE, Open-Meteo, ENTSO-E
        </span>
      </div>
    </div>
  )
}

export default App
