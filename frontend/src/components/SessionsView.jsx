import { useState, useEffect } from 'react'
import { Clock, MessageSquare, Code, FileText, Bot, Sparkles } from 'lucide-react'

const API_BASE = 'http://127.0.0.1:8000'

export function SessionsView({ timeRange }) {
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(true)
  const [pagination, setPagination] = useState(null)
  const [filters, setFilters] = useState({
    page: 1,
    limit: 20,
    sort: 'recent',
    search: ''
  })
  const [selectedSession, setSelectedSession] = useState(null)
  const [sessionDetail, setSessionDetail] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)

  useEffect(() => {
    loadSessions()
  }, [filters, timeRange])

  const loadSessions = async () => {
    try {
      setLoading(true)
      
      const params = new URLSearchParams()
      params.append('page', filters.page)
      params.append('limit', filters.limit)
      params.append('sort', filters.sort)
      if (filters.search) params.append('search', filters.search)
      
      const response = await fetch(`${API_BASE}/api/sessions?${params}`)
      const data = await response.json()
      
      setSessions(data.sessions)
      setPagination(data.pagination)
      setLoading(false)
    } catch (err) {
      console.error('Error loading sessions:', err)
      setLoading(false)
    }
  }

  const loadSessionDetail = async (sessionId) => {
    try {
      setDetailLoading(true)
      const response = await fetch(`${API_BASE}/api/sessions/${sessionId}`)
      const data = await response.json()
      setSessionDetail(data)
      setDetailLoading(false)
    } catch (err) {
      console.error('Error loading session detail:', err)
      setDetailLoading(false)
    }
  }

  const handleSessionClick = (session) => {
    setSelectedSession(session)
    loadSessionDetail(session.id)
  }

  const handleCloseDetail = () => {
    setSelectedSession(null)
    setSessionDetail(null)
  }

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value, page: 1 }))
  }

  const handlePageChange = (newPage) => {
    setFilters(prev => ({ ...prev, page: newPage }))
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const formatDuration = (minutes) => {
    if (minutes < 60) return `${Math.round(minutes)}m`
    const hours = Math.floor(minutes / 60)
    const mins = Math.round(minutes % 60)
    return `${hours}h ${mins}m`
  }

  const formatDate = (isoString) => {
    const date = new Date(isoString)
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading && sessions.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mb-4"></div>
          <p className="text-slate-600">Loading sessions...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Filters */}
      <div className="bg-slate-50 border border-slate-200 rounded-lg p-4">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <input
            type="text"
            placeholder="Search sessions by name..."
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
          />
          
          {/* Sort */}
          <select
            value={filters.sort}
            onChange={(e) => handleFilterChange('sort', e.target.value)}
            className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none bg-white"
          >
            <option value="recent">Most Recent</option>
            <option value="oldest">Oldest First</option>
            <option value="longest">Longest Duration</option>
            <option value="shortest">Shortest Duration</option>
          </select>
        </div>
      </div>

      {/* Sessions List */}
      <div className="grid gap-4">
        {sessions.map((session) => (
          <div
            key={session.id}
            onClick={() => handleSessionClick(session)}
            className="bg-white border border-slate-200 rounded-lg p-6 hover:shadow-lg hover:border-primary-300 transition-all cursor-pointer"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-slate-800 mb-1">
                  {session.name || 'Untitled Session'}
                </h3>
                <p className="text-sm text-slate-500">
                  {formatDate(session.created_at)}
                </p>
              </div>
              <div className="flex items-center gap-2 text-slate-600">
                <Clock className="w-4 h-4" />
                <span className="text-sm font-medium">{formatDuration(session.duration_minutes)}</span>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 py-3 border-t border-slate-100">
              <div className="flex items-center gap-2">
                <MessageSquare className="w-4 h-4 text-blue-500" />
                <div>
                  <p className="text-xs text-slate-500">Messages</p>
                  <p className="text-sm font-semibold text-slate-800">{session.message_count || 0}</p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <Code className="w-4 h-4 text-green-500" />
                <div>
                  <p className="text-xs text-slate-500">Lines Changed</p>
                  <p className="text-sm font-semibold text-slate-800">
                    +{session.total_lines_added} -{session.total_lines_removed}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-purple-500" />
                <div>
                  <p className="text-xs text-slate-500">Files</p>
                  <p className="text-sm font-semibold text-slate-800">{session.files_modified_count}</p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <Bot className="w-4 h-4 text-orange-500" />
                <div>
                  <p className="text-xs text-slate-500">Mode</p>
                  <p className="text-sm font-semibold text-slate-800">Normal</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Pagination */}
      {pagination && pagination.total_pages > 1 && (
        <div className="flex items-center justify-between border-t border-slate-200 pt-4">
          <div className="text-sm text-slate-600">
            Showing {sessions.length} of {pagination.total_count.toLocaleString()} sessions
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => handlePageChange(pagination.page - 1)}
              disabled={!pagination.has_prev}
              className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Previous
            </button>
            <span className="px-4 py-2 text-slate-600">
              Page {pagination.page} of {pagination.total_pages}
            </span>
            <button
              onClick={() => handlePageChange(pagination.page + 1)}
              disabled={!pagination.has_next}
              className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Next
            </button>
          </div>
        </div>
      )}

      {/* Session Detail Modal */}
      {selectedSession && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-6 border-b border-slate-200">
              <div>
                <h2 className="text-2xl font-bold text-slate-800">
                  {selectedSession.name || 'Untitled Session'}
                </h2>
                <p className="text-sm text-slate-500 mt-1">
                  {formatDate(selectedSession.created_at)}
                </p>
              </div>
              <button
                onClick={handleCloseDetail}
                className="text-slate-400 hover:text-slate-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Modal Body */}
            <div className="flex-1 overflow-y-auto p-6">
              {detailLoading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                </div>
              ) : sessionDetail ? (
                <div className="space-y-6">
                  {/* Session Stats */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-slate-50 rounded-lg p-4">
                      <p className="text-xs text-slate-500 mb-1">Duration</p>
                      <p className="text-lg font-bold text-slate-800">
                        {formatDuration(sessionDetail.session.duration_minutes)}
                      </p>
                    </div>
                    <div className="bg-slate-50 rounded-lg p-4">
                      <p className="text-xs text-slate-500 mb-1">Messages</p>
                      <p className="text-lg font-bold text-slate-800">
                        {sessionDetail.session.message_count}
                      </p>
                    </div>
                    <div className="bg-slate-50 rounded-lg p-4">
                      <p className="text-xs text-slate-500 mb-1">Lines Added</p>
                      <p className="text-lg font-bold text-green-600">
                        +{sessionDetail.session.total_lines_added}
                      </p>
                    </div>
                    <div className="bg-slate-50 rounded-lg p-4">
                      <p className="text-xs text-slate-500 mb-1">Lines Removed</p>
                      <p className="text-lg font-bold text-red-600">
                        -{sessionDetail.session.total_lines_removed}
                      </p>
                    </div>
                  </div>

                  {/* Messages */}
                  <div>
                    <h3 className="text-lg font-semibold text-slate-800 mb-4">
                      Conversation ({sessionDetail.messages.length} messages)
                    </h3>
                    <div className="space-y-4">
                      {sessionDetail.messages.map((message) => (
                        <div
                          key={message.id}
                          className={`p-4 rounded-lg border ${
                            message.type === 'user'
                              ? 'bg-blue-50 border-blue-200'
                              : 'bg-slate-50 border-slate-200'
                          }`}
                        >
                          <div className="flex items-center gap-2 mb-2">
                            <span className={`text-xs font-semibold px-2 py-1 rounded ${
                              message.type === 'user'
                                ? 'bg-blue-200 text-blue-800'
                                : 'bg-slate-200 text-slate-800'
                            }`}>
                              {message.type === 'user' ? 'USER' : 'AI'}
                            </span>
                            {message.is_agentic && (
                              <span className="text-xs font-semibold px-2 py-1 rounded bg-purple-200 text-purple-800">
                                <Bot className="w-3 h-3 inline mr-1" />
                                AGENT
                              </span>
                            )}
                            {message.thinking && (
                              <span className="text-xs font-semibold px-2 py-1 rounded bg-yellow-200 text-yellow-800">
                                <Sparkles className="w-3 h-3 inline mr-1" />
                                THINKING
                              </span>
                            )}
                            <span className="text-xs text-slate-500 ml-auto">
                              {new Date(message.created_at).toLocaleTimeString()}
                            </span>
                          </div>
                          <p className="text-sm text-slate-700 whitespace-pre-wrap line-clamp-3">
                            {message.text || '[No text content]'}
                          </p>
                          {message.tool_count > 0 && (
                            <p className="text-xs text-slate-500 mt-2">
                              🛠️ {message.tool_count} tool call{message.tool_count > 1 ? 's' : ''}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-slate-500 text-center py-12">No session details available</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

