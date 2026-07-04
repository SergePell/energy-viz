import { useEffect, useState } from 'react'
import { ChoroplethKarte } from './components/ChoroplethKarte'
import { VerbrauchAnomalie } from './components/VerbrauchAnomalie'
import { EnergieMix } from './components/EnergieMix'
import { EnergieFluss } from './components/EnergieFluss'
import { NettoHandelsbilanz } from './components/NettoHandelsbilanz'
import { HandelsbilanzKPI } from './components/HandelsbilanzKPI'
import { HandelsbilanzLaender } from './components/HandelsbilanzLaender'
import { QuickInfo } from './components/QuickInfo'
import { JahrDropdown } from './components/JahrDropdown'
import { useJson } from './hooks/useJson'

const REITER = [
  { id: 'analyse', label: 'Analyse' },
  { id: 'handel', label: 'Grenzüberschreitender Handel' },
]

// Fallback-Bereich, bevor Daten geladen sind
const JAHR_FALLBACK_MIN = 2009
const JAHR_FALLBACK_MAX = 2026

function App() {
  const [kanton, setKanton] = useState(null)
  const [reiter, setReiter] = useState('analyse')
  const [fokusLand, setFokusLand] = useState(null)  // 'DE' | 'FR' | 'AT' | 'IT' | null
  const waehlen = code => setKanton(prev => (prev === code ? null : code))
  const landKlick = land => setFokusLand(prev => (prev === land ? null : land))

  // Jahresbereich aus den Handelsdaten ableiten (deckt 2009–2026 ab, der weiteste vorhandene Range)
  const { data: fluesse } = useJson('/data/grenzfluss_monat.json')
  const jahre = fluesse && fluesse.length
    ? [...new Set(fluesse.map(r => new Date(r.date).getUTCFullYear()))].sort((a, b) => a - b)
    : Array.from({ length: JAHR_FALLBACK_MAX - JAHR_FALLBACK_MIN + 1 }, (_, i) => JAHR_FALLBACK_MIN + i)
  const jahrMin = jahre[0]
  const jahrMax = jahre[jahre.length - 1]

  const [vonJahr, setVonJahr] = useState(jahrMin)
  const [bisJahr, setBisJahr] = useState(jahrMax)

  // Sobald die Daten geladen sind, die Auswahl einmalig auf den vollen Bereich setzen
  useEffect(() => {
    if (!fluesse || !fluesse.length) return
    setVonJahr(jahre[0])
    setBisJahr(jahre[jahre.length - 1])
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fluesse])

  // Abgeleiteter Zeitraum in ms, den alle Kinderkomponenten als brushRange erwarten.
  // Wenn der volle Bereich gewählt ist, null durchreichen — dann greift überall der jeweilige Fallback.
  const istVoll = vonJahr === jahrMin && bisJahr === jahrMax
  const zeitraum = istVoll
    ? null
    : [
        Date.UTC(Math.min(vonJahr, bisJahr), 0, 1),
        Date.UTC(Math.max(vonJahr, bisJahr), 11, 31, 23, 59, 59),
      ]

  // Klick auf einen Punkt in der Netto-Handelsbilanz: Zeitraum auf dieses Jahr setzen
  const zeitpunktKlick = datumStr => {
    if (!datumStr) return
    const y = new Date(datumStr).getUTCFullYear()
    setVonJahr(y)
    setBisJahr(y)
  }

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

      {/* Globaler Zeitraumfilter, gilt über beide Reiter */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: 12, marginBottom: 20,
        padding: '10px 12px', border: '1px solid var(--border)', borderRadius: 6,
      }}>
        <span style={{ fontSize: 11, color: 'var(--text-muted)', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
          Zeitraum
        </span>
        <JahrDropdown wert={vonJahr} optionen={jahre}
          onChange={j => { setVonJahr(j); if (j > bisJahr) setBisJahr(j) }} />
        <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>bis</span>
        <JahrDropdown wert={bisJahr} optionen={jahre}
          onChange={j => { setBisJahr(j); if (j < vonJahr) setVonJahr(j) }} />
        <button
          onClick={() => { setVonJahr(jahrMin); setBisJahr(jahrMax) }}
          style={{
            marginLeft: 'auto',
            background: 'var(--bg-card)', color: 'var(--text-secondary)',
            border: '1px solid var(--border)', borderRadius: 6,
            padding: '4px 10px', fontSize: 12, cursor: 'pointer',
          }}>
          Zurücksetzen
        </button>
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
              <VerbrauchAnomalie selectedKanton={kanton} onClear={() => setKanton(null)} brushRange={zeitraum} />
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
          <HandelsbilanzKPI brushRange={zeitraum} fokusLand={fokusLand} />
          <div style={{ marginTop: 24 }}>
            <HandelsbilanzLaender brushRange={zeitraum} fokusLand={fokusLand} onLandKlick={landKlick} />
          </div>
          {fokusLand && (
            <div style={{ marginTop: 12, fontSize: 12, color: 'var(--text-muted)' }}>
              Fokus auf {({ DE: 'Deutschland', FR: 'Frankreich', AT: 'Österreich', IT: 'Italien' })[fokusLand]}.{' '}
              <button onClick={() => setFokusLand(null)}
                style={{
                  background: 'transparent', color: 'var(--text-secondary)',
                  border: 'none', textDecoration: 'underline', cursor: 'pointer',
                  fontSize: 12, padding: 0,
                }}>Zurücksetzen</button>
            </div>
          )}
          <div style={{ marginTop: 16 }}>
            <EnergieFluss brushRange={zeitraum} fokusLand={fokusLand} onLandKlick={landKlick} />
          </div>
          <div style={{ marginTop: 24 }}>
            <NettoHandelsbilanz brushRange={zeitraum} fokusLand={fokusLand} onZeitpunktKlick={zeitpunktKlick} />
          </div>
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
