import { useState, useEffect } from 'react'
import { AlertCircle, GitBranch, FileCode, ListTodo, Terminal, Book, Folder } from 'lucide-react'

const API_BASE = 'http://127.0.0.1:8000'

// Map context types to icons and colors
const getContextIcon = (contextType) => {
  const iconMap = {
    'linter': AlertCircle,
    'git': GitBranch,
    'file_context': FileCode,
    'code_chunks': FileCode,
    'todos': ListTodo,
    'terminal': Terminal,
    'knowledge': Book,
    'default': Folder
  }
  return iconMap[contextType] || iconMap['default']
}

const getContextColor = (contextType) => {
  const colorMap = {
    'linter': 'text-red-500',
    'git': 'text-orange-500',
    'file_context': 'text-blue-500',
    'code_chunks': 'text-purple-500',
    'todos': 'text-green-500',
    'terminal': 'text-slate-700',
    'knowledge': 'text-cyan-500',
    'default': 'text-slate-500'
  }
  return colorMap[contextType] || colorMap['default']
}

export function ContextView({ timeRange }) {
  const [contexts, setContexts] = useState([])
  const [loading, setLoading] = useState(true)
  const [pagination, setPagination] = useState(null)
  const [stats, setStats] = useState(null)
  const [filters, setFilters] = useState({
    page: 1,
    limit: 20,
    context_type: null,
    search: ''
  })
  const [selectedContext, setSelectedContext] = useState(null)
  const [contextDetail, setContextDetail] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)

  useEffect(() => {
    loadContexts()
  }, [filters, timeRange])

  const loadContexts = async () => {
    try {
      setLoading(true)
      
      const params = new URLSearchParams()
      params.append('page', filters.page)
      params.append('limit', filters.limit)
      if (filters.context_type) params.append('context_type', filters.context_type)
      if (filters.search) params.append('search', filters.search)
      
      const response = await fetch(`${API_BASE}/api/context?${params}`)
      const data = await response.json()
      
      setContexts(data.contexts)
      setPagination(data.pagination)
      setStats(data.stats)
      setLoading(false)
    } catch (err) {
      console.error('Error loading contexts:', err)
      setLoading(false)
    }
  }

  const loadContextDetail = async (contextId) => {
    try {
      setDetailLoading(true)
      const response = await fetch(`${API_BASE}/api/context/${contextId}`)
      const data = await response.json()
      setContextDetail(data)
      setDetailLoading(false)
    } catch (err) {
      console.error('Error loading context detail:', err)
      setDetailLoading(false)
    }
  }

  const handleContextClick = (context) => {
    setSelectedContext(context)
    loadContextDetail(context.id)
  }

  const handleCloseDetail = () => {
    setSelectedContext(null)
    setContextDetail(null)
  }

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value, page: 1 }))
  }

  const handlePageChange = (newPage) => {
    setFilters(prev => ({ ...prev, page: newPage }))
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  if (loading && contexts.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mb-4"></div>
          <p className="text-slate-600">Loading context items...</p>
        </div>
      </div>
    )
  }

  if (!loading && contexts.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <Folder className="w-16 h-16 text-slate-300 mx-auto mb-4" />
          <p className="text-slate-600 text-lg">No context items found</p>
          <p className="text-slate-500 text-sm mt-2">Try adjusting your filters or time range</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Stats Overview */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div className="bg-white border border-slate-200 rounded-lg p-4">
            <p className="text-xs text-slate-500 mb-1">Total Context Items</p>
            <p className="text-2xl font-bold text-slate-800">{stats.total_items.toLocaleString()}</p>
          </div>
          <div className="bg-white border border-slate-200 rounded-lg p-4">
            <p className="text-xs text-slate-500 mb-1">Context Types</p>
            <p className="text-2xl font-bold text-purple-600">{Object.keys(stats.context_types).length}</p>
          </div>
          <div className="bg-white border border-slate-200 rounded-lg p-4">
            <p className="text-xs text-slate-500 mb-1">Most Common</p>
            <p className="text-sm font-bold text-slate-800">
              {stats.context_types && Object.entries(stats.context_types).sort((a, b) => b[1] - a[1])[0]?.[0] || 'N/A'}
            </p>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="bg-slate-50 border border-slate-200 rounded-lg p-4">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <input
            type="text"
            placeholder="Search context items..."
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
          />
          
          {/* Context Type Filter */}
          <select
            value={filters.context_type || ''}
            onChange={(e) => handleFilterChange('context_type', e.target.value || null)}
            className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none bg-white"
          >
            <option value="">All Context Types</option>
            {stats && Object.keys(stats.context_types).sort().map(type => (
              <option key={type} value={type}>
                {type} ({stats.context_types[type]})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Contexts List */}
      <div className="grid gap-4">
        {contexts.map((context) => {
          const Icon = getContextIcon(context.context_type)
          const iconColor = getContextColor(context.context_type)
          
          return (
            <div
              key={context.id}
              onClick={() => handleContextClick(context)}
              className="bg-white border border-slate-200 rounded-lg p-5 hover:shadow-lg hover:border-primary-300 transition-all cursor-pointer"
            >
              <div className="flex items-start gap-3 mb-3">
                <Icon className={`w-5 h-5 ${iconColor} mt-1`} />
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-semibold px-2 py-1 rounded bg-slate-200 text-slate-700">
                      {context.context_type}
                    </span>
                    {context.all_types.length > 1 && (
                      <span className="text-xs text-slate-500">
                        +{context.all_types.length - 1} more
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-slate-700">{context.summary}</p>
                </div>
              </div>

              {/* Context Features */}
              <div className="flex flex-wrap gap-2 mt-3">
                {context.has_linter_errors && (
                  <span className="text-xs px-2 py-1 rounded bg-red-100 text-red-700">
                    <AlertCircle className="w-3 h-3 inline mr-1" />
                    Linter Errors
                  </span>
                )}
                {context.has_git_status && (
                  <span className="text-xs px-2 py-1 rounded bg-orange-100 text-orange-700">
                    <GitBranch className="w-3 h-3 inline mr-1" />
                    Git Status
                  </span>
                )}
                {context.has_code_chunks && (
                  <span className="text-xs px-2 py-1 rounded bg-purple-100 text-purple-700">
                    <FileCode className="w-3 h-3 inline mr-1" />
                    Code Chunks
                  </span>
                )}
                {context.has_todos && (
                  <span className="text-xs px-2 py-1 rounded bg-green-100 text-green-700">
                    <ListTodo className="w-3 h-3 inline mr-1" />
                    TODOs
                  </span>
                )}
                {context.has_terminal && (
                  <span className="text-xs px-2 py-1 rounded bg-slate-100 text-slate-700">
                    <Terminal className="w-3 h-3 inline mr-1" />
                    Terminal
                  </span>
                )}
              </div>
            </div>
          )
        })}
      </div>

      {/* Pagination */}
      {pagination && pagination.total_pages > 1 && (
        <div className="flex items-center justify-between border-t border-slate-200 pt-4">
          <div className="text-sm text-slate-600">
            Showing {contexts.length} of {pagination.total_count.toLocaleString()} context items
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

      {/* Context Detail Modal */}
      {selectedContext && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-6 border-b border-slate-200">
              <div className="flex items-center gap-3">
                {(() => {
                  const Icon = getContextIcon(selectedContext.context_type)
                  const iconColor = getContextColor(selectedContext.context_type)
                  return <Icon className={`w-6 h-6 ${iconColor}`} />
                })()}
                <div>
                  <h2 className="text-2xl font-bold text-slate-800 capitalize">
                    {selectedContext.context_type.replace('_', ' ')}
                  </h2>
                  <p className="text-sm text-slate-500 mt-1">{selectedContext.summary}</p>
                </div>
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
              ) : contextDetail ? (
                <div className="space-y-6">
                  {/* Linter Errors */}
                  {contextDetail.linter_error_count > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800 mb-3 flex items-center gap-2">
                        <AlertCircle className="w-5 h-5 text-red-500" />
                        Linter Errors ({contextDetail.linter_error_count})
                      </h3>
                      <div className="bg-red-50 rounded-lg p-4 border border-red-200">
                        <pre className="text-sm text-red-800 whitespace-pre-wrap overflow-x-auto max-h-60">
                          {JSON.stringify(contextDetail.linter_errors, null, 2)}
                        </pre>
                      </div>
                    </div>
                  )}

                  {/* Git Status */}
                  {contextDetail.git_status && (
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800 mb-3 flex items-center gap-2">
                        <GitBranch className="w-5 h-5 text-orange-500" />
                        Git Status
                      </h3>
                      <div className="bg-orange-50 rounded-lg p-4 border border-orange-200">
                        <pre className="text-sm text-orange-900 whitespace-pre-wrap overflow-x-auto max-h-60">
                          {contextDetail.git_status}
                        </pre>
                      </div>
                    </div>
                  )}

                  {/* File Context */}
                  {(contextDetail.current_file_location || contextDetail.ide_editors_state) && (
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800 mb-3 flex items-center gap-2">
                        <FileCode className="w-5 h-5 text-blue-500" />
                        File Context
                      </h3>
                      <div className="space-y-3">
                        {contextDetail.current_file_location && (
                          <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                            <p className="text-xs font-semibold text-blue-700 mb-2">Current File Location:</p>
                            <pre className="text-sm text-blue-900 whitespace-pre-wrap">
                              {contextDetail.current_file_location}
                            </pre>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Code Chunks */}
                  {contextDetail.attached_file_count > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800 mb-3 flex items-center gap-2">
                        <FileCode className="w-5 h-5 text-purple-500" />
                        Attached Code Chunks ({contextDetail.attached_file_count})
                      </h3>
                      <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                        <p className="text-sm text-purple-800">
                          {contextDetail.attached_file_count} code chunk{contextDetail.attached_file_count > 1 ? 's' : ''} attached
                        </p>
                      </div>
                    </div>
                  )}

                  {/* TODOs */}
                  {contextDetail.todo_count > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800 mb-3 flex items-center gap-2">
                        <ListTodo className="w-5 h-5 text-green-500" />
                        TODOs ({contextDetail.todo_count})
                      </h3>
                      <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                        <pre className="text-sm text-green-900 whitespace-pre-wrap overflow-x-auto max-h-60">
                          {JSON.stringify(contextDetail.todos, null, 2)}
                        </pre>
                      </div>
                    </div>
                  )}

                  {/* Terminal */}
                  {contextDetail.terminal_count > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800 mb-3 flex items-center gap-2">
                        <Terminal className="w-5 h-5 text-slate-700" />
                        Terminal Files ({contextDetail.terminal_count})
                      </h3>
                      <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                        <p className="text-sm text-slate-700">
                          {contextDetail.terminal_count} terminal file{contextDetail.terminal_count > 1 ? 's' : ''} referenced
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Session Info */}
                  {contextDetail.session_info && (
                    <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                      <h3 className="text-sm font-semibold text-slate-700 mb-2">Session Context</h3>
                      <p className="text-sm text-slate-600">
                        <strong>Session:</strong> {contextDetail.session_name || contextDetail.session_id}
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-slate-500 text-center py-12">No context details available</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

