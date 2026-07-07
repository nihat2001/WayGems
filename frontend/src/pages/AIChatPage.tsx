import { useState, useRef, useEffect } from 'react'
import { api } from '../api/client'
import ChatBubble from '../components/ChatBubble'
import type { ChatResponse } from '../types'

interface Message {
  role: 'user' | 'ai'
  content: string
  response?: ChatResponse
}

export default function AIChatPage() {
  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'ai',
      content: "Hi! I'm WayGems AI. Tell me what kind of place you're looking for in Baku.",
    },
  ])
  const [loading, setLoading] = useState(false)
  const endRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    const q = query.trim()
    if (!q || loading) return

    setQuery('')
    setMessages((prev) => [...prev, { role: 'user', content: q }])
    setLoading(true)

    try {
      const data = await api.ai.search(q)
      setMessages((prev) => [
        ...prev,
        { role: 'ai', content: data.answer, response: data },
      ])
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'ai', content: 'Sorry, something went wrong. Try again.', response: undefined },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-1 h-7 bg-gradient-to-b from-brand-500 to-brand-700 rounded-full" />
          <h1 className="text-3xl font-bold text-gray-900 tracking-tight">AI Search</h1>
        </div>
        <p className="text-gray-500 ml-4">Describe what you're looking for in natural language</p>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 h-[550px] flex flex-col overflow-hidden">
        <div className="flex-1 overflow-y-auto p-5 space-y-4">
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}>
              {m.role === 'user' ? (
                <div className="bg-brand-600 text-white rounded-2xl rounded-tr-sm px-4 py-2.5 max-w-[75%] shadow-sm">
                  <p className="text-sm">{m.content}</p>
                </div>
              ) : (
                <div className="max-w-[90%]">
                  {m.response ? (
                    <ChatBubble response={m.response} />
                  ) : (
                    <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm px-4 py-2.5 shadow-sm">
                      <p className="text-base text-gray-800 leading-relaxed">{m.content}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex justify-start animate-fade-in">
              <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm">
                <div className="flex gap-1.5">
                  <div className="w-2 h-2 bg-brand-400 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-brand-500 rounded-full animate-bounce [animation-delay:0.1s]" />
                  <div className="w-2 h-2 bg-brand-600 rounded-full animate-bounce [animation-delay:0.2s]" />
                </div>
              </div>
            </div>
          )}
          <div ref={endRef} />
        </div>

        <div className="border-t border-gray-100 p-4 bg-gray-50/50">
          <div className="flex gap-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="e.g. a quiet cafe with sea view..."
              className="flex-1 border border-gray-200 rounded-xl px-4 py-2.5 text-sm outline-none focus:ring-2 focus:ring-brand-300 focus:border-brand-400 transition-all bg-white"
              disabled={loading}
            />
            <button
              onClick={handleSend}
              disabled={loading || !query.trim()}
              className="bg-brand-600 text-white px-5 py-2.5 rounded-xl text-sm font-medium hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm hover:shadow-md active:scale-95"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 19V5m0 0l-7 7m7-7l7 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
