import { useState, useEffect } from 'react'

// Lädt eine JSON aus public/ und gibt {data, loading} zurück
export function useJson(pfad) {
  const [data, setData] = useState(null)
  useEffect(() => {
    fetch(pfad).then(r => r.json()).then(setData)
  }, [pfad])
  return { data, loading: data === null }
}