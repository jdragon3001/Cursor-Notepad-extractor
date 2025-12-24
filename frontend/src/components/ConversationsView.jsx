import { useState, useEffect } from 'react'
import { Calendar, Clock, Code, MessageSquare, Search, FileText } from 'lucide-react'
import { ConversationDetailModal } from './ConversationDetailModal'

const API_BASE = 'http://127.0.0.1:8000'

/**
 * ConversationsView - Browse sessions/conversations
 */
export function ConversationsView() {
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(true)
  const [pagination, setPagination] = useState(null)
  const [selectedSessionId, setSelectedSessionId] = useState(null)
  const [filters, setFilters] = useState({
    page: 1,
    limit: 20,
    sort: 'recent',
    search: ''
  })

  useEffect(() => {
    loadSessions()
  }, [filters])

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

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value, page: 1 }))
  }

  const handlePageChange = (newPage) => {
    setFilters(prev => ({ ...prev, page: newPage }))
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const formatDate = (isoString) => {
    const date = new Date(isoString)
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: date.getFullYear() !== new Date().getFullYear() ? 'numeric' : undefined,
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    })
  }
  
  const formatDuration = (minutes) => {
    if (minutes < 1) return '< 1m'
    if (minutes < 60) return `${Math.round(minutes)}m`
    const hours = Math.floor(minutes / 60)
    const mins = Math.round(minutes % 60)
    if (mins === 0) return `${hours}h`
    return `${hours}h ${mins}m`
  }

  return (
    <div className="space-y-6">
      {/* Filters & Controls */}
      <div className="flex flex-wrap items-center gap-4 pb-4 border-b border-slate-200">
        <input
          type="text"
          placeholder="Search conversations..."
          value={filters.search}
          onChange={(e) => handleFilterChange('search', e.target.value)}
          className="flex-1 min-w-[200px] px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
        />
        
        <select
          value={filters.sort}
          onChange={(e) => handleFilterChange('sort', e.target.value)}
          className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
        >
          <option value="recent">Most Recent</option>
          <option value="oldest">Oldest First</option>
          <option value="longest">Longest Duration</option>
          <option value="shortest">Shortest Duration</option>
        </select>
        
        <select
          value={filters.limit}
          onChange={(e) => handleFilterChange('limit', parseInt(e.target.value))}
          className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
        >
          <option value="10">10 per page</option>
          <option value="20">20 per page</option>
          <option value="50">50 per page</option>
        </select>
      </div>

      {/* Results Count */}
      {pagination && (
        <div className="text-sm text-slate-600">
          Showing {((pagination.page - 1) * pagination.limit) + 1} - {Math.min(pagination.page * pagination.limit, pagination.total_count)} of {pagination.total_count.toLocaleString()} conversations
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="text-slate-600 mt-4">Loading conversations...</p>
        </div>
      )}

      {/* Sessions List */}
      {!loading && sessions && sessions.length > 0 && (
        <div className="space-y-3">
          {sessions.map((session) => (
            <SessionCard 
              key={session.id} 
              session={session} 
              formatDate={formatDate}
              formatDuration={formatDuration}
              onClick={() => setSelectedSessionId(session.id)}
            />
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && (!sessions || sessions.length === 0) && (
        <div className="text-center py-12">
          <Calendar className="w-16 h-16 text-slate-300 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-slate-700 mb-2">No conversations found</h3>
          <p className="text-slate-500">Try adjusting your filters</p>
        </div>
      )}

      {/* Pagination */}
      {pagination && pagination.total_pages > 1 && (
        <div className="flex items-center justify-center gap-2 pt-6">
          <button
            onClick={() => handlePageChange(pagination.page - 1)}
            disabled={!pagination.has_prev}
            className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          
          <span className="px-4 py-2 text-sm text-slate-600">
            Page {pagination.page} of {pagination.total_pages}
          </span>
          
          <button
            onClick={() => handlePageChange(pagination.page + 1)}
            disabled={!pagination.has_next}
            className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      )}

      {/* Conversation Detail Modal */}
      {selectedSessionId && (
        <ConversationDetailModal
          sessionId={selectedSessionId}
          onClose={() => setSelectedSessionId(null)}
        />
      )}
    </div>
  )
}

/**
 * SessionCard - Individual session preview
 */
function SessionCard({ session, formatDate, formatDuration, onClick }) {
  return (
    <div 
      onClick={onClick}
      className="bg-white border border-slate-200 rounded-lg p-5 hover:shadow-md transition-shadow cursor-pointer"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-slate-800 truncate mb-1">
            {session.name || `Session ${session.id.slice(0, 8)}...`}
          </h3>
          <div className="flex items-center gap-3 text-sm text-slate-500">
            <div className="flex items-center gap-1">
              <Calendar className="w-4 h-4" />
              <span>Last active: {formatDate(session.last_updated_at || session.created_at)}</span>
            </div>
          </div>
        </div>
        
        <div className="flex items-center gap-2 text-sm text-slate-600 bg-slate-100 px-3 py-1 rounded-lg">
          <Clock className="w-4 h-4" />
          <span>{formatDuration(session.duration_minutes)}</span>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-4 text-sm text-slate-600">
        {session.message_count > 0 && (
          <div className="flex items-center gap-1">
            <MessageSquare className="w-4 h-4" />
            <span>{session.message_count} messages</span>
          </div>
        )}
        
        {session.files_modified_count > 0 && (
          <div className="flex items-center gap-1">
            <FileText className="w-4 h-4" />
            <span>{session.files_modified_count} files</span>
          </div>
        )}
        
        {(session.total_lines_added > 0 || session.total_lines_removed > 0) && (
          <div className="flex items-center gap-1">
            <Code className="w-4 h-4" />
            <span className="text-green-600">+{session.total_lines_added}</span>
            <span className="text-slate-400">/</span>
            <span className="text-red-600">-{session.total_lines_removed}</span>
          </div>
        )}
      </div>
    </div>
  )
}

