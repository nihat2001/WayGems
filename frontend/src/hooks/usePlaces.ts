import { useState, useEffect, useCallback } from 'react'
import { api } from '../api/client'
import type { Place, Category } from '../types'


export function usePlaces(categoryId?: number) {
  const [places, setPlaces] = useState<Place[]>([])
  const [loading, setLoading] = useState(true)

  const fetch = useCallback(async () => {
    setLoading(true)
    try {
      const data = await api.places.list({
        category_id: categoryId,
        limit: 50,
      })
      setPlaces(data)
    } catch {
      setPlaces([])
    } finally {
      setLoading(false)
    }
  }, [categoryId])

  useEffect(() => { fetch() }, [fetch])

  return { places, loading, refetch: fetch }
}

export function useCategories() {
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.categories.list()
      .then(setCategories)
      .catch(() => setCategories([]))
      .finally(() => setLoading(false))
  }, [])

  return { categories, loading }
}
