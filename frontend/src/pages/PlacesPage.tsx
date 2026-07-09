import PlaceCard from '../components/PlaceCard'
import LoadingSpinner from '../components/LoadingSpinner'
import { usePlaces } from '../hooks/usePlaces'

export default function PlacesPage() {
  const { places, loading } = usePlaces()

  return (
    <div>
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-1 h-7 bg-gradient-to-b from-brand-500 to-brand-700 rounded-full" />
          <h1 className="text-3xl font-bold text-gray-900 tracking-tight">Discover</h1>
        </div>
        <p className="text-gray-500 ml-4">
          Browse places or ask our AI for personalized recommendations
        </p>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : places.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-gray-400">
          <p className="text-6xl mb-4">🗺️</p>
          <p className="text-lg font-medium text-gray-500">Nothing here yet</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {places.map((p) => (
            <PlaceCard key={p.id} place={p} />
          ))}
        </div>
      )}
    </div>
  )
}
