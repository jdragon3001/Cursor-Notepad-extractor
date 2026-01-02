import { useState, useEffect } from 'react'
import { Wrench, FileText, Search, Terminal, Globe, CheckCircle, XCircle } from 'lucide-react'

const API_BASE = 'http://127.0.0.1:8000'

// Map tool types to icons and colors
const getToolIcon = (toolType) => {
  const iconMap = {
    'read_file': FileText,
    'write': FileText,
    'grep': Search,
    'codebase_search': Search,
    'search_replace': FileText,
    'run_terminal_cmd': Terminal,
    'web_search': Globe,
    'default': Wrench
  }
  return iconMap[toolType] || iconMap['default']
}

const getToolColor = (toolType) => {
  const colorMap = {
    'read_file': 'text-blue-500',
    'write': 'text-green-500',
    'grep': 'text-purple-500',
    'codebase_search': 'text-purple-500',
    'search_replace': 'text-orange-500',
    'run_terminal_cmd': 'text-slate-700',
    'web_search': 'text-cyan-500',
    'default': 'text-slate-500'
  }
  return colorMap[toolType] || colorMap['default']
}

export function ToolsView({ timeRange }) {
  const [tools, setTools] = useState([])
  const [loading, setLoading] = useState(true)
  const [pagination, setPagination] = useState(null)
  const [stats, setStats] = useState(null)
  const [filters, setFilters] = useState({
    page: 1,
    limit: 20,
    tool_type: null,
    search: ''
  })
  const [selectedTool, setSelectedTool] = useState(null)
  const [toolDetail, setToolDetail] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)

  useEffect(() => {
    loadTools()
  }, [filters, timeRange])

  const loadTools = async () => {
    try {
      setLoading(true)
      
      const params = new URLSearchParams()
      params.append('page', filters.page)
      params.append('limit', filters.limit)
      if (filters.tool_type) params.append('tool_type', filters.tool_type)
      if (filters.search) params.append('search', filters.search)
      
      const response = await fetch(`${API_BASE}/api/tools?${params}`)
      const data = await response.json()
      
      setTools(data.tools)
      setPagination(data.pagination)
      setStats(data.stats)
      setLoading(false)
    } catch (err) {
      console.error('Error loading tools:', err)
      setLoading(false)
    }
  }

  const loadToolDetail = async (toolId) => {
    try {
      setDetailLoading(true)
      const response = await fetch(`${API_BASE}/api/tools/${toolId}`)
      const data = await response.json()
      setToolDetail(data)
      setDetailLoading(false)
    } catch (err) {
      console.error('Error loading tool detail:', err)
      setDetailLoading(false)
    }
  }

  const handleToolClick = (tool) => {
    setSelectedTool(tool)
    loadToolDetail(tool.id)
  }

  const handleCloseDetail = () => {
    setSelectedTool(null)
    setToolDetail(null)
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
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading && tools.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mb-4"></div>
          <p className="text-slate-600">Loading tool calls...</p>
        </div>
      </div>
    )
  }

  if (!loading && tools.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <Wrench className="w-16 h-16 text-slate-300 mx-auto mb-4" />
          <p className="text-slate-600 text-lg">No tool calls found</p>
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
            <p className="text-xs text-slate-500 mb-1">Total Tool Calls</p>
            <p className="text-2xl font-bold text-slate-800">{stats.total_calls.toLocaleString()}</p>
          </div>
          <div className="bg-white border border-slate-200 rounded-lg p-4">
            <p className="text-xs text-slate-500 mb-1">Success Rate</p>
            <p className="text-2xl font-bold text-green-600">
              {stats.total_calls > 0 ? Math.round((stats.success_count / stats.total_calls) * 100) : 0}%
            </p>
          </div>
          <div className="bg-white border border-slate-200 rounded-lg p-4">
            <p className="text-xs text-slate-500 mb-1">Tool Types</p>
            <p className="text-2xl font-bold text-purple-600">{Object.keys(stats.tool_types).length}</p>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="bg-slate-50 border border-slate-200 rounded-lg p-4">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <input
            type="text"
            placeholder="Search tool calls..."
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
          />
          
          {/* Tool Type Filter */}
          <select
            value={filters.tool_type || ''}
            onChange={(e) => handleFilterChange('tool_type', e.target.value || null)}
            className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none bg-white"
          >
            <option value="">All Tool Types</option>
            {stats && Object.keys(stats.tool_types).sort().map(type => (
              <option key={type} value={type}>
                {type} ({stats.tool_types[type]})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Tools List */}
      <div className="grid gap-4">
        {tools.map((tool) => {
          const Icon = getToolIcon(tool.tool_type)
          const iconColor = getToolColor(tool.tool_type)
          
          return (
            <div
              key={tool.id}
              onClick={() => handleToolClick(tool)}
              className="bg-white border border-slate-200 rounded-lg p-5 hover:shadow-lg hover:border-primary-300 transition-all cursor-pointer"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3 flex-1">
                  <Icon className={`w-5 h-5 ${iconColor}`} />
                  <div>
                    <h3 className="text-lg font-semibold text-slate-800">
                      {tool.tool_name}
                    </h3>
                    <p className="text-xs text-slate-500 mt-1">
                      {formatDate(tool.created_at)}
                    </p>
                  </div>
                </div>
                <div>
                  {tool.success ? (
                    <CheckCircle className="w-5 h-5 text-green-500" />
                  ) : (
                    <XCircle className="w-5 h-5 text-red-500" />
                  )}
                </div>
              </div>

              {/* Parameters Preview */}
              {tool.parameters && Object.keys(tool.parameters).length > 0 && (
                <div className="bg-slate-50 rounded-lg p-3 border border-slate-100">
                  <p className="text-xs font-semibold text-slate-600 mb-2">Parameters:</p>
                  <div className="space-y-1">
                    {Object.entries(tool.parameters).slice(0, 3).map(([key, value]) => (
                      <div key={key} className="flex gap-2 text-xs">
                        <span className="text-slate-500">{key}:</span>
                        <span className="text-slate-700 truncate">
                          {typeof value === 'string' ? value : JSON.stringify(value)}
                        </span>
                      </div>
                    ))}
                    {Object.keys(tool.parameters).length > 3 && (
                      <p className="text-xs text-slate-500">
                        ... and {Object.keys(tool.parameters).length - 3} more
                      </p>
                    )}
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Pagination */}
      {pagination && pagination.total_pages > 1 && (
        <div className="flex items-center justify-between border-t border-slate-200 pt-4">
          <div className="text-sm text-slate-600">
            Showing {tools.length} of {pagination.total_count.toLocaleString()} tool calls
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

      {/* Tool Detail Modal */}
      {selectedTool && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-6 border-b border-slate-200">
              <div className="flex items-center gap-3">
                {(() => {
                  const Icon = getToolIcon(selectedTool.tool_type)
                  const iconColor = getToolColor(selectedTool.tool_type)
                  return <Icon className={`w-6 h-6 ${iconColor}`} />
                })()}
                <div>
                  <h2 className="text-2xl font-bold text-slate-800">
                    {selectedTool.tool_name}
                  </h2>
                  <p className="text-sm text-slate-500 mt-1">
                    {formatDate(selectedTool.created_at)}
                  </p>
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
              ) : toolDetail ? (
                <div className="space-y-6">
                  {/* Status */}
                  <div className={`p-4 rounded-lg ${toolDetail.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                    <div className="flex items-center gap-2">
                      {toolDetail.success ? (
                        <>
                          <CheckCircle className="w-5 h-5 text-green-600" />
                          <span className="font-semibold text-green-800">Success</span>
                        </>
                      ) : (
                        <>
                          <XCircle className="w-5 h-5 text-red-600" />
                          <span className="font-semibold text-red-800">Failed</span>
                        </>
                      )}
                    </div>
                    {toolDetail.error && (
                      <p className="text-sm text-red-700 mt-2">{toolDetail.error}</p>
                    )}
                  </div>

                  {/* Parameters */}
                  <div>
                    <h3 className="text-lg font-semibold text-slate-800 mb-3">Parameters</h3>
                    <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                      <pre className="text-sm text-slate-700 whitespace-pre-wrap overflow-x-auto">
                        {JSON.stringify(toolDetail.parameters, null, 2)}
                      </pre>
                    </div>
                  </div>

                  {/* Result */}
                  {toolDetail.result && (
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800 mb-3">Result</h3>
                      <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                        <pre className="text-sm text-slate-700 whitespace-pre-wrap overflow-x-auto max-h-96">
                          {typeof toolDetail.result === 'string' ? toolDetail.result : JSON.stringify(toolDetail.result, null, 2)}
                        </pre>
                      </div>
                    </div>
                  )}

                  {/* Session Info */}
                  {toolDetail.session_info && (
                    <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                      <h3 className="text-sm font-semibold text-slate-700 mb-2">Session Context</h3>
                      <p className="text-sm text-slate-600">
                        <strong>Session:</strong> {toolDetail.session_name || toolDetail.session_id}
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-slate-500 text-center py-12">No tool details available</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

