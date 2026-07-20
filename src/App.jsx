import { useEffect, useState } from 'react'
import { ChoroplethKarte } from './components/ChoroplethKarte'
import { VerbrauchAnomalie } from './components/VerbrauchAnomalie'
import { EnergieMix } from './components/EnergieMix'
import { EnergieFluss } from './components/EnergieFluss'
import { NettoHandelsbilanz } from './components/NettoHandelsbilanz'
import { HandelsbilanzKPI } from './components/HandelsbilanzKPI'
import { HandelsbilanzLaender } from './components/HandelsbilanzLaender'
import { EnergieVergleich } from './components/EnergieVergleich'
import { GesamtenergieSankey } from './components/GesamtenergieSankey'
import { WetterLinie } from './components/WetterLinie'
import { QuickInfo } from './components/QuickInfo'
import { JahrDropdown } from './components/JahrDropdown'
import { useJson } from './hooks/useJson'
import { TagesProfil } from './components/TagesProfil'
import { ZerlegungAnsicht } from './components/ZerlegungAnsicht'
import { ErzeugungZeitreihe } from './components/ErzeugungZeitreihe'

const REITER = [
  { id: 'analyse', label: 'Analyse' },
  { id: 'handel', label: 'Grenzüberschreitender Handel' },
  { id: 'vergleich', label: 'Vergleich' },
  { id: 'gesamt', label: 'Gesamtenergie' },
]

// Fallback-Bereich, bevor Daten geladen sind
const JAHR_FALLBACK_MIN = 2009
const JAHR_FALLBACK_MAX = 2026

// Startwert des Schwellenwertes. Markiert zwei Anomalien; 0.65 markiert drei.
const SCHWELLE_START = 0.68

// Metadaten für den Footer. Datenstand konsistent mit der Pipeline (SNAPSHOT = 2026-05-10).
const META = {
  autor: 'Serge Pellegatta',
  version: '1.0',
  snapshot: '10. Mai 2026',
  repo: 'github.com/SergePell/energy-viz',
}

// Umschalter Dark/Light. currentColor sorgt dafür, dass das Icon die Textfarbe
// des Buttons erbt und in beiden Themes passt.
function ThemeToggle({ theme, onToggle }) {
  const dunkel = theme === 'dark'
  return (
    <button onClick={onToggle} title="Farbschema wechseln"
      style={{
        display: 'inline-flex', alignItems: 'center', gap: 6, flexShrink: 0,
        background: 'var(--bg-elevated)', color: 'var(--text-secondary)',
        border: '1px solid var(--border)', borderRadius: 6,
        padding: '6px 10px', fontSize: 12, cursor: 'pointer',
      }}>
      {dunkel ? (
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round">
          <circle cx="12" cy="12" r="4" />
          <path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4" />
        </svg>
      ) : (
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" />
        </svg>
      )}
      {dunkel ? 'Hell' : 'Dunkel'}
    </button>
  )
}

function App() {
  const [kanton, setKanton] = useState(null)
  const [reiter, setReiter] = useState('analyse')
  const [fokusLand, setFokusLand] = useState(null)  // 'DE' | 'FR' | 'AT' | 'IT' | null
  const [tag, setTag] = useState(null)              // Datum für das Viertelstundenprofil
  // Der Schwellenwert liegt auf App-Ebene, weil er zwei Ansichten koppelt:
  // die Anomaliepunkte auf der Verbrauchslinie und jene im Residuum-Panel.
  const [schwelle, setSchwelle] = useState(SCHWELLE_START)
  const waehlen = code => setKanton(prev => (prev === code ? null : code))
  const landKlick = land => setFokusLand(prev => (prev === land ? null : land))

  // Theme (dark = Default). Wahl wird in localStorage gemerkt und als
  // data-theme-Attribut auf <html> gesetzt, wo die CSS-Variablen umschalten.
  const [theme, setTheme] = useState(() => {
    try { return localStorage.getItem('theme') || 'dark' } catch { return 'dark' }
  })
  useEffect(() => {
    document.documentElement.dataset.theme = theme
    try { localStorage.setItem('theme', theme) } catch { /* localStorage nicht verfügbar */ }
  }, [theme])

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
      {/* Kopfzeile mit Titel links und Theme-Umschalter rechts */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12, marginBottom: 16 }}>
        <div>
          <p style={{ fontFamily: 'var(--font-mono)', fontSize: 10, letterSpacing: '0.16em', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: 6 }}>
            Visual Analytics · Energie Schweiz
          </p>
          <h1 style={{ fontSize: 30, fontWeight: 400, lineHeight: 1.15, margin: 0, color: 'var(--text-primary)' }}>
            Energie-Dashboard Schweiz
          </h1>
        </div>
        <ThemeToggle theme={theme} onToggle={() => setTheme(t => (t === 'dark' ? 'light' : 'dark'))} />
      </div>

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

      {/* Globaler Zeitraumfilter, gilt für Analyse und Handel — im Vergleich- und
          Gesamtenergie-Reiter wird stattdessen die eigene A/B-Auswahl der Komponente genutzt */}
      {reiter !== 'vergleich' && reiter !== 'gesamt' && (
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
      )}

      {/* Reiter 1: Analyse */}
      {reiter === 'analyse' && (
        <>
          {/* Oberer Block: Erzeugung (links) und Verbrauch (rechts) visuell getrennt */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: 20, alignItems: 'start' }}>

            <section>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, letterSpacing: '0.14em', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: 10 }}>Erzeugung</div>
              {titel('Erzeugung pro Kanton',
                <QuickInfo titel="Erzeugung pro Kanton">
                  Erzeugung je Kanton, eingefärbt nach Menge. Sieben Swissgrid-Regionen fassen mehrere Kantone zusammen (z. B. AI, AR), diese teilen sich denselben Wert. Bei gewähltem Zeitraum zeigt die Karte die Summe über diese Monate, sonst die Jahressumme.
                </QuickInfo>)}
              <ChoroplethKarte selected={kanton} onSelect={waehlen} brushRange={zeitraum} />
              <div style={{ marginTop: 24 }}>
                <ErzeugungZeitreihe selectedKanton={kanton} onClear={() => setKanton(null)} brushRange={zeitraum} />
              </div>
            </section>

            <section>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, letterSpacing: '0.14em', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: 10 }}>Verbrauch</div>
              <VerbrauchAnomalie
                brushRange={zeitraum}
                onTagWaehlen={setTag}
                schwelle={schwelle}
                onSchwelleChange={setSchwelle}
              />
              <TagesProfil datum={tag} onClose={() => setTag(null)} />
            </section>
          </div>

          <section style={{ marginTop: 24 }}>
            <ZerlegungAnsicht brushRange={zeitraum} schwelle={schwelle} />
          </section>

          <section style={{ marginTop: 24 }}>
            {titel('Wetter (national)',
              <QuickInfo titel="Wetter">
                Nationaler Tagesdurchschnitt aus 18 Kantonsstationen. Sichtbare Grössen über die Toggle-Buttons umschaltbar. Zeitraum synchron zum Filter oben.
              </QuickInfo>)}
            <WetterLinie brushRange={zeitraum} />
          </section>

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

      {/* Reiter 3: Vergleich */}
      {reiter === 'vergleich' && (
        <section>
          {titel('Vergleich zweier Zeiträume',
            <QuickInfo titel="Zeitraum-Vergleich">
              Vergleicht den Energiemix zweier ausgewählter Perioden (Monat oder Jahr) direkt gegenüber. Die Delta-Spalte zeigt die absolute und prozentuale Veränderung zwischen A und B. Die Balken sind auf den grössten Wert beider Perioden skaliert, wodurch die relative Grösse der Träger direkt ablesbar wird.
            </QuickInfo>)}
          <EnergieVergleich />
        </section>
      )}

      {/* Reiter 4: Gesamtenergie */}
      {reiter === 'gesamt' && (
        <section>
          {titel('Gesamtenergiebilanz Schweiz',
            <QuickInfo titel="Gesamtenergie-Sankey">
              Sankey-Darstellung der Schweizer Energiebilanz nach BFE Gesamtenergiestatistik. Links die Endenergie-Träger, rechts die Verwendungssektoren. Die Breite der Bänder zeigt die transportierte Energiemenge in Terawattstunden pro Jahr. Diese Perspektive ergänzt den Strom-fokussierten Analyse-Reiter um Wärme, Verkehr und weitere Energieanwendungen.
            </QuickInfo>)}
          <GesamtenergieSankey />
        </section>
      )}

      <div style={{ marginTop: 24, paddingTop: 12, borderTop: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '6px 20px', fontFamily: 'var(--font-mono)', fontSize: 9, color: 'var(--text-muted)', letterSpacing: '0.06em' }}>
        <span>Prototyp · MSc-Thesis FHGR · {META.autor} · v{META.version}</span>
        <span>Datenstand: {META.snapshot}</span>
        <span>Quellen: Swissgrid, BFE, Open-Meteo, ENTSO-E</span>
        <a href={`https://${META.repo}`} target="_blank" rel="noreferrer" style={{ color: 'var(--text-muted)', textDecoration: 'underline' }}>{META.repo}</a>
      </div>
    </div>
  )
}

export default App
