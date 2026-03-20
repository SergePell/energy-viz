function App() {
  return (
    <div style={{ padding: '24px 16px', maxWidth: 800, margin: '0 auto' }}>

      {/* Header */}
      <p style={{
        fontFamily: 'var(--font-mono)',
        fontSize: 10,
        letterSpacing: '0.16em',
        textTransform: 'uppercase',
        color: 'var(--text-muted)',
        marginBottom: 6,
      }}>
        Visual Analytics ·
      </p>

      <h1 style={{
        fontSize: 34,
        fontWeight: 400,
        lineHeight: 1.15,
        marginBottom: 4,
        color: 'var(--text-primary)',
      }}>
        Placeholder
      </h1>

      <p style={{
        fontSize: 14,
        color: 'var(--text-secondary)',
        marginBottom: 24,
        maxWidth: 500,
        lineHeight: 1.5,
      }}>
        Interaktive Visualisierung
      </p>

      {/* Platzhalter für die Karte */}
      <div style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: 14,
        height: 400,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <p style={{
          fontFamily: 'var(--font-mono)',
          fontSize: 12,
          color: 'var(--text-muted)',
        }}>
          Palceholder
        </p>
      </div>

      {/* Platzhalter für den Chart */}
      <div style={{
        marginTop: 16,
        background: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: 14,
        height: 220,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <p style={{
          fontFamily: 'var(--font-mono)',
          fontSize: 12,
          color: 'var(--text-muted)',
        }}>
          Placeholder
        </p>
      </div>

      {/* Footer */}
      <div style={{
        marginTop: 24,
        paddingTop: 12,
        borderTop: '1px solid var(--border)',
        display: 'flex',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: 8,
      }}>
        <span style={{
          fontFamily: 'var(--font-mono)',
          fontSize: 9,
          color: 'var(--text-muted)',
          letterSpacing: '0.08em',
        }}>
          Prototyp · MSc Thesis FHGR
        </span>
        <span style={{
          fontFamily: 'var(--font-mono)',
          fontSize: 9,
          color: 'var(--text-muted)',
        }}>
          Datenquellen: XY
        </span>
      </div>
    </div>
  )
}

export default App