import { useState, useEffect } from 'react'
import axios from 'axios'
import { X, User, Bot, Clock, Code, Terminal, FileText, Lightbulb, ChevronDown, ChevronUp, FileEdit } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { DiffViewer } from './DiffViewer'
import { ToolResultDisplay } from './ToolResultDisplay'

const API_BASE = 'http://127.0.0.1:8000'

/**
 * ConversationDetailModal - Full narrative timeline of a conversation
 */
export function ConversationDetailModal({ sessionId, onClose }) {
  const [loading, setLoading] = useState(true)
  const [session, setSession] = useState(null)
  const [messages, setMessages] = useState([])
  const [fileChanges, setFileChanges] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    if (sessionId) {
      loadSessionDetail()
    }
  }, [sessionId])

  const loadSessionDetail = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await axios.get(`${API_BASE}/api/sessions/${sessionId}`)
      setSession(response.data.session)
      setMessages(response.data.messages)
      setFileChanges(response.data.file_changes || [])
    } catch (err) {
      console.error('Error loading session detail:', err)
      setError(err.response?.data?.detail || 'Failed to load conversation')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-5xl max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-200">
          <div className="flex-1 min-w-0">
            <h2 className="text-2xl font-bold text-slate-800 truncate">
              {session?.name || 'Conversation'}
            </h2>
            {session && (
              <div className="flex items-center gap-4 mt-2 text-sm text-slate-600">
                <span>{new Date(session.created_at).toLocaleString()}</span>
                <span>•</span>
                <span>{messages.length} messages</span>
                <span>•</span>
                <span>{Math.round(session.duration_minutes)}m</span>
              </div>
            )}
          </div>
          <button
            onClick={onClose}
            className="ml-4 p-2 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <X className="w-6 h-6 text-slate-600" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {loading && (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
              {error}
            </div>
          )}

          {!loading && !error && messages.length === 0 && (
            <div className="text-center py-12 text-slate-500">
              No messages in this conversation.
            </div>
          )}

          {!loading && !error && messages.length > 0 && (
            <div className="space-y-6">
              {/* Files Changed Section */}
              {fileChanges && fileChanges.length > 0 && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                  <div className="flex items-center gap-2 mb-3">
                    <FileEdit className="w-5 h-5 text-blue-600" />
                    <h3 className="font-semibold text-blue-900">Files Changed ({fileChanges.length})</h3>
                  </div>
                  <div className="space-y-2">
                    {fileChanges.map((file, index) => (
                      <div key={index} className="flex items-center justify-between text-sm bg-white rounded px-3 py-2 border border-blue-100">
                        <div className="flex items-center gap-2 min-w-0 flex-1">
                          <FileText className="w-4 h-4 text-slate-600 flex-shrink-0" />
                          <span className="font-mono text-slate-700 truncate" title={file.file_name}>
                            {file.file_name.split('/').pop() || file.file_name}
                          </span>
                          <span className="text-xs text-slate-500">
                            ({file.file_extension || 'file'})
                          </span>
                        </div>
                        <span className="text-xs text-slate-500 whitespace-nowrap ml-2">
                          {file.line_count} {file.line_count === 1 ? 'edit' : 'edits'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Messages */}
              {messages.map((message, index) => (
                <MessageBubble key={message.id || index} message={message} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

/**
 * MessageBubble - Individual message in the conversation
 */
function MessageBubble({ message }) {
  const isUser = message.type === 'user'
  const [showThinking, setShowThinking] = useState(false)
  const [expandedTools, setExpandedTools] = useState({})

  const toggleTool = (index) => {
    setExpandedTools(prev => ({
      ...prev,
      [index]: !prev[index]
    }))
  }

  return (
    <div className={`flex gap-4 ${isUser ? 'flex-row' : 'flex-row'}`}>
      {/* Avatar */}
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isUser ? 'bg-primary-600' : 'bg-slate-700'
      }`}>
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>

      {/* Message Content */}
      <div className="flex-1 min-w-0">
        {/* Header */}
        <div className="flex items-center gap-2 mb-2">
          <span className="font-semibold text-slate-800">
            {isUser ? 'You' : (message.model_name || 'AI')}
          </span>
          <span className="text-xs text-slate-500">
            {new Date(message.created_at).toLocaleTimeString()}
          </span>
          {message.is_agentic && (
            <span className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full">
              Agent Mode
            </span>
          )}
          {message.is_consolidated && (
            <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">
              {message.fragment_count} fragments
            </span>
          )}
        </div>

        {/* Thinking (for AI messages) */}
        {message.thinking && (
          <div className="mb-3">
            <button
              onClick={() => setShowThinking(!showThinking)}
              className="flex items-center gap-2 text-sm text-slate-600 hover:text-slate-800 transition-colors"
            >
              <Lightbulb className="w-4 h-4" />
              <span>Thinking</span>
              {showThinking ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              {message.thinking_duration_ms && (
                <span className="text-xs text-slate-500">
                  ({(message.thinking_duration_ms / 1000).toFixed(1)}s)
                </span>
              )}
            </button>
            {showThinking && (
              <div className="mt-2 p-3 bg-amber-50 border border-amber-200 rounded-lg text-sm text-slate-700 whitespace-pre-wrap">
                {typeof message.thinking === 'string' ? message.thinking : JSON.stringify(message.thinking, null, 2)}
              </div>
            )}
          </div>
        )}

        {/* Main Text */}
        {message.text && (
          <div className="prose prose-slate prose-sm max-w-none mb-3">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.text}
            </ReactMarkdown>
          </div>
        )}

        {/* Tool Results */}
        {message.tool_results && message.tool_results.length > 0 && (
          <div className="space-y-2 mb-3">
            {message.tool_results.map((tool, index) => (
              <ToolResultDisplay 
                key={index} 
                tool={tool} 
                index={index}
                expanded={expandedTools[index]}
                onToggle={() => toggleTool(index)}
              />
            ))}
          </div>
        )}

        {/* Code Blocks */}
        {message.code_blocks && message.code_blocks.length > 0 && (
          <div className="space-y-3 mb-3">
            {message.code_blocks.map((block, index) => (
              <DiffViewer key={index} codeBlock={block} />
            ))}
          </div>
        )}

        {/* Suggested Code Blocks */}
        {message.suggested_code_blocks && message.suggested_code_blocks.length > 0 && (
          <div className="space-y-3 mb-3">
            <div className="text-sm font-semibold text-blue-600 mb-2">Suggested Edits</div>
            {message.suggested_code_blocks.map((block, index) => (
              <DiffViewer key={index} codeBlock={block} />
            ))}
          </div>
        )}

        {/* Context Chunks */}
        {message.codebase_context_chunks && message.codebase_context_chunks.length > 0 && (
          <details className="mb-3">
            <summary className="text-xs text-slate-600 cursor-pointer hover:text-slate-800 flex items-center gap-2">
              <FileText className="w-3 h-3" />
              <span>{message.codebase_context_chunks.length} context files</span>
            </summary>
            <div className="mt-2 text-xs text-slate-600 space-y-1 pl-5">
              {message.codebase_context_chunks.map((chunk, index) => (
                <div key={index} className="truncate">
                  {chunk.file_path || chunk.name || `Context ${index + 1}`}
                </div>
              ))}
            </div>
          </details>
        )}

        {/* Web References */}
        {message.web_references && message.web_references.length > 0 && (
          <div className="text-xs text-slate-600 flex items-center gap-2 mb-2">
            <span>🔗 {message.web_references.length} web references</span>
          </div>
        )}

        {/* Metadata */}
        <div className="flex items-center gap-3 text-xs text-slate-500 mt-2">
          {message.word_count > 0 && <span>{message.word_count} words</span>}
          {message.tool_count > 0 && (
            <span className="flex items-center gap-1">
              <Terminal className="w-3 h-3" />
              {message.tool_count} tools
            </span>
          )}
        </div>
      </div>
    </div>
  )
}



