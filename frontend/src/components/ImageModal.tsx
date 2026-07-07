import { useEffect } from 'react'

interface ImageModalProps {
  src: string
  alt: string
  description: string
  onClose: () => void
}

function formatBold(text: string) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g)
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i} className="font-semibold">{part.slice(2, -2)}</strong>
    }
    return part
  })
}

export default function ImageModal({ src, alt, description, onClose }: ImageModalProps) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', handler)
    document.body.style.overflow = 'hidden'
    return () => {
      document.removeEventListener('keydown', handler)
      document.body.style.overflow = ''
    }
  }, [onClose])

  return (
    <div
      className="fixed inset-0 z-50 bg-black/85 animate-fade-in overflow-y-auto"
      onClick={onClose}
    >
      <button
        onClick={onClose}
        className="fixed top-4 right-4 text-white/70 hover:text-white text-2xl cursor-pointer z-20 transition-colors"
      >
        ✕
      </button>

      <div
        className="min-h-screen flex items-center justify-center px-4 py-24"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="w-full max-w-4xl">
          <img
            src={src}
            alt={alt}
            className="w-full rounded-lg"
          />
          <h2 className="text-white text-xl font-bold text-center mt-5">
            {alt}
          </h2>
          <p className="text-white/80 text-base leading-relaxed text-center max-w-2xl mx-auto mt-3">
            {formatBold(description)}
          </p>
        </div>
      </div>
    </div>
  )
}
