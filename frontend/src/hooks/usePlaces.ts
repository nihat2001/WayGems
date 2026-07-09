import { useState, useEffect, useCallback } from 'react'
import { api } from '../api/client'
import type { Place } from '../types'


export function usePlaces() {
  const [places, setPlaces] = useState<Place[]>([])
  const [loading, setLoading] = useState(true)

  const fetch = useCallback(async () => {
    setLoading(true)
    try {
      const data = await api.places.list({
        limit: 50,
      })
      setPlaces(data)
    } catch {
      setPlaces([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetch() }, [fetch])

  return { places, loading, refetch: fetch }
}
