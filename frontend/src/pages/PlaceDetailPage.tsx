import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../api/client'
import type { PlaceDetail } from '../types'
import LoadingSpinner from '../components/LoadingSpinner'
import ImageModal from '../components/ImageModal'

function placeImage(place: { id: number; image_urls?: string[] }) {
  if (place.image_urls?.[0]) return place.image_urls[0]
  return `https://picsum.photos/seed/${place.id}/1200/600`
}

export default function PlaceDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [place, setPlace] = useState<PlaceDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    api.places.detail(Number(id))
      .then(setPlace)
      .catch(() => setPlace(null))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <LoadingSpinner />
  if (!place) return <div className="text-center py-20 text-gray-400">Place not found</div>

  return (
    <div>
      <div
        className="relative w-full h-[55vh] min-h-[400px] overflow-hidden bg-gray-100 rounded-2xl group cursor-pointer shadow-lg"
        onClick={() => setModalOpen(true)}
      >
        <img
          src={placeImage(place)}
          alt={place.name}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 via-50% to-transparent" />
        <div className="absolute bottom-0 left-0 right-0 p-10 pb-12">
          <Link
            to="/"
            className="inline-flex items-center gap-1 text-white/70 hover:text-white text-sm mb-3 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            Back to places
          </Link>
          <h1 className="text-4xl font-bold text-white">{place.name}</h1>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-4 mt-8">
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
          <p className="text-gray-700 text-lg leading-relaxed">{place.description}</p>
        </div>
      </div>

      {modalOpen && (
        <ImageModal
          src={placeImage(place)}
          alt={place.name}
          description={place.description}
          onClose={() => setModalOpen(false)}
        />
      )}
    </div>
  )
}
