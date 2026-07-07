import type { ChatResponse } from '../types'

function formatText(text: string) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g)
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i} className="font-semibold text-gray-900">{part.slice(2, -2)}</strong>
    }
    return part
  })
}

function formatAnswer(text: string) {
  const lines = text.split('\n')
  const blocks: { type: 'paragraph' | 'heading' | 'list-item'; content: string }[] = []
  let current = ''

  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) {
      if (current) {
        blocks.push({ type: 'paragraph', content: current })
        current = ''
      }
      continue
    }

    const numberedMatch = trimmed.match(/^\d+\.\s+(.*)/)
    const bulletMatch = trimmed.match(/^[-*]\s+(.*)/)

    if (numberedMatch || bulletMatch) {
      if (current) {
        blocks.push({ type: 'paragraph', content: current })
        current = ''
      }
      const inner = numberedMatch ? numberedMatch[1] : bulletMatch![1]
      const hasLabel = inner.match(/^(\*\*[^*]+\*\*)/)
      if (hasLabel) {
        blocks.push({ type: 'heading', content: inner })
      } else {
        blocks.push({ type: 'list-item', content: inner })
      }
      continue
    }

    current = current ? current + ' ' + trimmed : trimmed
  }
  if (current) {
    blocks.push({ type: 'paragraph', content: current })
  }

  return blocks.map((block, i) => {
    switch (block.type) {
      case 'heading':
        return (
          <p key={i} className="text-base font-semibold text-gray-900 mt-4 first:mt-0">
            {formatText(block.content)}
          </p>
        )
      case 'list-item':
        return (
          <p key={i} className="text-sm text-gray-700 pl-3 border-l-2 border-brand-200 ml-1 mt-1.5">
            {formatText(block.content)}
          </p>
        )
      default:
        return (
          <p key={i} className="text-sm text-gray-700 mt-2 first:mt-0 leading-relaxed">
            {formatText(block.content)}
          </p>
        )
    }
  })
}

export default function ChatBubble({ response }: { response: ChatResponse }) {
  return (
    <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm p-4 max-w-[90%] shadow-sm">
      <div className="space-y-0.5">
        {formatAnswer(response.answer)}
      </div>
      {response.matches.length > 0 && (
        <div className="mt-4 border-t border-gray-100 pt-3">
          <p className="text-xs font-semibold text-brand-600 mb-3 uppercase tracking-wider">
            Matched places
          </p>
          {response.matches.map((m, i) => (
            <div key={i} className="flex items-start gap-2.5 mb-2.5 last:mb-0">
              <span className="text-xs font-medium bg-brand-100 text-brand-700 rounded-md px-2 py-0.5 shrink-0">
                {(m.confidence * 100).toFixed(0)}%
              </span>
              <div>
                <p className="text-sm font-medium text-gray-900">{m.place?.name ?? '—'}</p>
                {m.reasoning && (
                  <p className="text-xs text-gray-500 mt-0.5 leading-relaxed">{m.reasoning}</p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
