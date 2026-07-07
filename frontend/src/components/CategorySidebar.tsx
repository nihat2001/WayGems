import type { Category } from '../types'

interface Props {
  categories: Category[]
  selected: number | undefined
  onSelect: (id: number | undefined) => void
}

export default function CategorySidebar({ categories, selected, onSelect }: Props) {
  return (
    <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-thin">
      <button
        onClick={() => onSelect(undefined)}
        className={`shrink-0 flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
          selected === undefined
            ? 'bg-brand-600 text-white shadow-sm shadow-brand-600/20'
            : 'bg-white text-gray-500 border border-gray-200 hover:border-brand-300 hover:text-brand-600'
        }`}
      >
        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
        </svg>
        All
      </button>
      {categories.map((c) => (
        <button
          key={c.id}
          onClick={() => onSelect(c.id)}
          className={`shrink-0 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
            selected === c.id
              ? 'bg-brand-600 text-white shadow-sm shadow-brand-600/20'
              : 'bg-white text-gray-500 border border-gray-200 hover:border-brand-300 hover:text-brand-600'
          }`}
        >
          <span className="capitalize">{c.name}</span>
        </button>
      ))}
    </div>
  )
}
