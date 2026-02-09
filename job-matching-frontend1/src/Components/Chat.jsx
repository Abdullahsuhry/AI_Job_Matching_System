import React, { useState } from 'react'
import axios from 'axios'

export default function Chat() {
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState([]) // {role, text}

  const send = async () => {
    if (!prompt.trim()) return
    const userMsg = { role: 'user', text: prompt }
    setMessages((m) => [...m, userMsg])
    setPrompt('')
    setLoading(true)
    try {
      // forward entire body to /api/chat; backend will proxy to configured LLM
      const res = await axios.post('/api/chat', { prompt })
      // assume provider returns { reply: '...' } or similar
      const replyText = res.data.reply || res.data.text || JSON.stringify(res.data)
      setMessages((m) => [...m, { role: 'assistant', text: replyText }])
    } catch (err) {
      console.error(err)
      setMessages((m) => [...m, { role: 'assistant', text: 'Error: failed to get response' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Career AI Chat</h2>
      <div className="border rounded p-4 mb-4 h-64 overflow-y-auto bg-white">
        {messages.length === 0 && <p className="text-gray-500">Ask career questions or request tailored advice.</p>}
        {messages.map((m, i) => (
          <div key={i} className={m.role === 'user' ? 'text-right my-2' : 'text-left my-2'}>
            <div className={`inline-block p-2 rounded ${m.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-900'}`}>
              {m.text}
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="flex-1 p-2 border rounded"
          placeholder="Ask about job matching, skill gaps, or courses..."
        />
        <button onClick={send} disabled={loading} className="bg-indigo-600 text-white px-4 py-2 rounded">
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  )
}
