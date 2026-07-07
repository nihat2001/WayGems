import { Link } from 'react-router-dom'
import type { Place } from '../types'

function placeImage(place: Place) {
  if (place.image_urls?.[0]) return place.image_urls[0]
  return `https://picsum.photos/seed/${place.id}/400/300`
}

export default function PlaceCard({ place }: { place: Place }) {
  return (
    <Link
      to={`/places/${place.id}`}
      className="group block bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-xl hover:border-brand-100 transition-all duration-300 overflow-hidden"
    >
      <div className="relative aspect-[4/3] overflow-hidden bg-gray-100">
        <img
          src={placeImage(place)}
          alt={place.name}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        <div className="absolute bottom-0 left-0 right-0 p-3 bg-gradient-to-t from-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          <span className="text-white/90 text-xs font-medium">Explore →</span>
        </div>
      </div>

      <div className="p-4">
        <h3 className="font-semibold text-gray-900 group-hover:text-brand-700 transition-colors truncate">
          {place.name}
        </h3>
        <p className="text-sm text-gray-500 line-clamp-2 mt-1 leading-relaxed">
          {place.description}
        </p>
      </div>
    </Link>
  )
}
