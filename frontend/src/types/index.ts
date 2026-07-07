export interface Category {
  id: number
  name: string
  icon: string
  description: string
}

export interface Place {
  id: number
  name: string
  description: string
  address: string
  category_id: number
  rating: number
  price_level: number
  image_urls: string[]
  latitude: number | null
  longitude: number | null
}

export interface PlaceDetail extends Place {
  place_metadata: Record<string, unknown>
  category: Category | null
}

export interface AIPlaceResult {
  place: Place | null
  confidence: number
  reasoning: string
}

export interface ChatResponse {
  answer: string
  matches: AIPlaceResult[]
}

export interface PlaceFilter {
  category_id?: number
  min_rating?: number
  max_price?: number
  search?: string
  page?: number
  limit?: number
}
