import { useState, useEffect } from 'react'

// Lädt eine JSON aus public/ und gibt {data, loading, error} zurück
export function useJson(pfad) {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  useEffect(() => {
    let aktiv = true
    setData(null)
    setError(null)
    fetch(pfad)
      .then(r => {
        if (!r.ok) throw new Error(`${r.status} ${r.statusText} für ${pfad}`)
        return r.json()
      })
      .then(d => { if (aktiv) setData(d) })
      .catch(e => {
        if (aktiv) setError(e)
        console.error('[useJson] Laden fehlgeschlagen:', pfad, e)
      })
    return () => { aktiv = false }
  }, [pfad])
  return { data, loading: data === null && error === null, error }
}