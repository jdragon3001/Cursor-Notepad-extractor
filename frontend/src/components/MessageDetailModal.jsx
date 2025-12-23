import { useState, useEffect } from 'react'
import { X, User, Bot, Code, Brain, Wrench, Clock, MessageSquare, Calendar, Database, Eye, EyeOff, Copy, Check } from 'lucide-react'
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000'

/**
 * MessageDetailModal - Full message details with raw/formatted toggle
 */
export function MessageDetailModal({ messageId, onClose }) {
  const [message, setMessage] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showRaw, setShowRaw] = useState(false)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    loadMessageDetail()
  }, [messageId])

  const loadMessageDetail = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_BASE}/api/messages/${messageId}`)
      setMessage(response.data)
      setLoading(false)
    } catch (err) {
      console.error('Error loading message detail:', err)
      setLoading(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const formatDate = (isoString) => {
    const date = new Date(isoString)
    return date.toLocaleString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    })
  }

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl p-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="text-slate-600 mt-4">Loading message...</p>
        </div>
      </div>
    )
  }

  if (!message) {
    return null
  }

  const isUser = message.type === 'user'

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto"
      onClick={onClose}
    >
      <div 
        className="bg-white rounded-xl shadow-2xl max-w-5xl w-full my-8 flex flex-col max-h-[90vh]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className={`${isUser ? 'bg-gradient-to-r from-blue-600 to-blue-700' : 'bg-gradient-to-r from-purple-600 to-purple-700'} text-white p-6 rounded-t-xl`}>
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-4">
              <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                isUser ? 'bg-blue-500' : 'bg-purple-500'
              }`}>
                {isUser ? <User className="w-6 h-6" /> : <Bot className="w-6 h-6" />}
              </div>
              <div>
                <h2 className="text-2xl font-bold">{isUser ? 'User Message' : 'AI Response'}</h2>
                <p className="text-sm opacity-90">{formatDate(message.created_at)}</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-white hover:bg-opacity-20 rounded-lg p-2 transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* View Toggle & Actions */}
          <div className="flex items-center justify-between border-b border-slate-200 pb-4">
            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowRaw(false)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  !showRaw
                    ? 'bg-primary-600 text-white'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                <Eye className="w-4 h-4 inline mr-1" />
                Formatted
              </button>
              <button
                onClick={() => setShowRaw(true)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  showRaw
                    ? 'bg-primary-600 text-white'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                <EyeOff className="w-4 h-4 inline mr-1" />
                Raw Data
              </button>
            </div>

            <button
              onClick={() => copyToClipboard(message.text || JSON.stringify(message.raw_data, null, 2))}
              className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
            >
              {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </div>

          {/* Formatted View */}
          {!showRaw && (
            <div className="space-y-6">
              {/* Message Text */}
              <div>
                <h3 className="text-lg font-semibold text-slate-800 mb-3">Message Content</h3>
                <div className="bg-slate-50 border border-slate-200 rounded-lg p-4">
                  <pre className="whitespace-pre-wrap font-sans text-slate-700">
                    {message.text || <em className="text-slate-400">No text content</em>}
                  </pre>
                </div>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-blue-600 font-medium">Words</p>
                  <p className="text-2xl font-bold text-blue-900">{message.word_count}</p>
                </div>
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <p className="text-sm text-green-600 font-medium">Characters</p>
                  <p className="text-2xl font-bold text-green-900">{message.char_count}</p>
                </div>
                <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                  <p className="text-sm text-purple-600 font-medium">Tokens</p>
                  <p className="text-2xl font-bold text-purple-900">{message.total_tokens || 0}</p>
                </div>
                <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                  <p className="text-sm text-orange-600 font-medium">Tools</p>
                  <p className="text-2xl font-bold text-orange-900">{message.tool_count}</p>
                </div>
              </div>

              {/* Code Blocks */}
              {message.code_block_count > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-slate-800 mb-3 flex items-center gap-2">
                    <Code className="w-5 h-5" />
                    Code Blocks ({message.code_block_count})
                  </h3>
                  <div className="space-y-2">
                    {message.code_blocks?.map((block, idx) => (
                      <details key={idx} className="bg-slate-50 border border-slate-200 rounded-lg">
                        <summary className="cursor-pointer p-4 font-medium text-slate-700 hover:bg-slate-100">
                          Block {idx + 1} {block.language && `(${block.language})`}
                        </summary>
                        <pre className="p-4 overflow-x-auto bg-slate-900 text-slate-100 text-sm">
                          {block.code || block.content || JSON.stringify(block)}
                        </pre>
                      </details>
                    ))}
                  </div>
                </div>
              )}

              {/* Thinking */}
              {message.has_thinking && (
                <div>
                  <h3 className="text-lg font-semibold text-slate-800 mb-3 flex items-center gap-2">
                    <Brain className="w-5 h-5" />
                    Thinking Process
                    {message.thinking_duration_ms && (
                      <span className="text-sm text-slate-500">({(message.thinking_duration_ms / 1000).toFixed(1)}s)</span>
                    )}
                  </h3>
                  <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
                    <pre className="whitespace-pre-wrap font-sans text-slate-700 text-sm">
                      {typeof message.thinking === 'string' 
                        ? message.thinking 
                        : JSON.stringify(message.thinking, null, 2)}
                    </pre>
                  </div>
                </div>
              )}

              {/* Tools Used */}
              {message.tool_count > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-slate-800 mb-3 flex items-center gap-2">
                    <Wrench className="w-5 h-5" />
                    Tools Used ({message.tool_count})
                  </h3>
                  <div className="space-y-2">
                    {message.tool_types?.map((tool, idx) => (
                      <div key={idx} className="bg-slate-50 border border-slate-200 rounded-lg p-3 flex items-center gap-2">
                        <Wrench className="w-4 h-4 text-slate-500" />
                        <span className="font-mono text-sm text-slate-700">{tool}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Session Info */}
              {message.session_info && (
                <div>
                  <h3 className="text-lg font-semibold text-slate-800 mb-3 flex items-center gap-2">
                    <MessageSquare className="w-5 h-5" />
                    Session Context
                  </h3>
                  <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 space-y-2">
                    {message.session_info.name && (
                      <p className="text-slate-700">
                        <strong>Name:</strong> {message.session_info.name}
                      </p>
                    )}
                    <p className="text-slate-700">
                      <strong>Duration:</strong> {message.session_info.duration_minutes} minutes
                    </p>
                    <p className="text-slate-700">
                      <strong>Code Changes:</strong> +{message.session_info.total_lines_added} / -{message.session_info.total_lines_removed} lines
                    </p>
                    <button
                      onClick={() => {/* Navigate to session view */}}
                      className="mt-2 text-primary-600 hover:text-primary-700 font-medium text-sm"
                    >
                      View Full Session →
                    </button>
                  </div>
                </div>
              )}

              {/* Model Info */}
              {message.model_name && (
                <div>
                  <h3 className="text-lg font-semibold text-slate-800 mb-3">Model Information</h3>
                  <div className="bg-slate-50 border border-slate-200 rounded-lg p-4">
                    <p className="text-slate-700">
                      <strong>Model:</strong> {message.model_name}
                    </p>
                    {message.is_agentic && (
                      <p className="text-slate-700 mt-2">
                        <strong>Mode:</strong> <span className="text-purple-600">Agent Mode</span>
                      </p>
                    )}
                    {message.capabilities && message.capabilities.length > 0 && (
                      <div className="mt-2">
                        <strong className="text-slate-700">Capabilities:</strong>
                        <div className="flex flex-wrap gap-2 mt-1">
                          {message.capabilities.map((cap, idx) => (
                            <span key={idx} className="px-2 py-1 bg-slate-200 text-slate-700 rounded text-xs">
                              {cap}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Raw Data View */}
          {showRaw && (
            <div>
              <h3 className="text-lg font-semibold text-slate-800 mb-3">Raw JSON Data</h3>
              <pre className="bg-slate-900 text-slate-100 rounded-lg p-4 overflow-x-auto text-sm">
                {JSON.stringify(message.raw_data || message, null, 2)}
              </pre>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-slate-50 border-t border-slate-200 p-4 rounded-b-xl flex justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 font-medium rounded-lg transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

