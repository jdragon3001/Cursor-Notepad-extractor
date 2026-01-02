import { useState, useEffect } from 'react'
import { Code, FileText, TrendingUp, TrendingDown } from 'lucide-react'

const API_BASE = 'http://127.0.0.1:8000'

export function CodeDiffsView({ timeRange }) {
  const [diffs, setDiffs] = useState([])
  const [loading, setLoading] = useState(true)
  const [pagination, setPagination] = useState(null)
  const [filters, setFilters] = useState({
    page: 1,
    limit: 20,
    sort: 'recent',
    search: '',
    session_id: null
  })
  const [selectedDiff, setSelectedDiff] = useState(null)
  const [diffDetail, setDiffDetail] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)

  useEffect(() => {
    loadDiffs()
  }, [filters, timeRange])

  const loadDiffs = async () => {
    try {
      setLoading(true)
      
      const params = new URLSearchParams()
      params.append('page', filters.page)
      params.append('limit', filters.limit)
      params.append('sort', filters.sort)
      if (filters.search) params.append('search', filters.search)
      if (filters.session_id) params.append('session_id', filters.session_id)
      
      const response = await fetch(`${API_BASE}/api/code-diffs?${params}`)
      const data = await response.json()
      
      setDiffs(data.diffs)
      setPagination(data.pagination)
      setLoading(false)
    } catch (err) {
      console.error('Error loading code diffs:', err)
      setLoading(false)
    }
  }

  const loadDiffDetail = async (diffId) => {
    try {
      setDetailLoading(true)
      const response = await fetch(`${API_BASE}/api/code-diffs/${diffId}`)
      const data = await response.json()
      setDiffDetail(data)
      setDetailLoading(false)
    } catch (err) {
      console.error('Error loading diff detail:', err)
      setDetailLoading(false)
    }
  }

  const handleDiffClick = (diff) => {
    setSelectedDiff(diff)
    loadDiffDetail(diff.id)
  }

  const handleCloseDetail = () => {
    setSelectedDiff(null)
    setDiffDetail(null)
  }

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value, page: 1 }))
  }

  const handlePageChange = (newPage) => {
    setFilters(prev => ({ ...prev, page: newPage }))
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const formatDate = (isoString) => {
    if (!isoString) return 'Unknown date'
    const date = new Date(isoString)
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading && diffs.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mb-4"></div>
          <p className="text-slate-600">Loading code diffs...</p>
        </div>
      </div>
    )
  }

  if (!loading && diffs.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <Code className="w-16 h-16 text-slate-300 mx-auto mb-4" />
          <p className="text-slate-600 text-lg">No code diffs found</p>
          <p className="text-slate-500 text-sm mt-2">Try adjusting your filters or time range</p>
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
            placeholder="Search in diff data..."
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
            <option value="most_changes">Most Changes</option>
          </select>
        </div>
      </div>

      {/* Diffs List */}
      <div className="grid gap-4">
        {diffs.map((diff) => (
          <div
            key={diff.id}
            onClick={() => handleDiffClick(diff)}
            className="bg-white border border-slate-200 rounded-lg p-6 hover:shadow-lg hover:border-primary-300 transition-all cursor-pointer"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <Code className="w-5 h-5 text-purple-500" />
                  <h3 className="text-lg font-semibold text-slate-800">
                    Code Block: {diff.block_id}
                  </h3>
                </div>
                <p className="text-sm text-slate-500">
                  Session: {diff.session_name || diff.session_id}
                </p>
                {diff.created_at && (
                  <p className="text-xs text-slate-400 mt-1">
                    {formatDate(diff.created_at)}
                  </p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 py-3 border-t border-slate-100">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-green-500" />
                <div>
                  <p className="text-xs text-slate-500">Lines Added</p>
                  <p className="text-sm font-semibold text-green-600">+{diff.lines_added}</p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <TrendingDown className="w-4 h-4 text-red-500" />
                <div>
                  <p className="text-xs text-slate-500">Lines Removed</p>
                  <p className="text-sm font-semibold text-red-600">-{diff.lines_removed}</p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-blue-500" />
                <div>
                  <p className="text-xs text-slate-500">Net Change</p>
                  <p className={`text-sm font-semibold ${
                    diff.net_lines_changed >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {diff.net_lines_changed >= 0 ? '+' : ''}{diff.net_lines_changed}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <Code className="w-4 h-4 text-purple-500" />
                <div>
                  <p className="text-xs text-slate-500">Total Changes</p>
                  <p className="text-sm font-semibold text-slate-800">{diff.total_changes}</p>
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
            Showing {diffs.length} of {pagination.total_count.toLocaleString()} diffs
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

      {/* Diff Detail Modal */}
      {selectedDiff && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-6 border-b border-slate-200">
              <div>
                <h2 className="text-2xl font-bold text-slate-800">
                  Code Block: {selectedDiff.block_id}
                </h2>
                <p className="text-sm text-slate-500 mt-1">
                  Session: {selectedDiff.session_name || selectedDiff.session_id}
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
              ) : diffDetail ? (
                <div className="space-y-6">
                  {/* Diff Stats */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-slate-50 rounded-lg p-4">
                      <p className="text-xs text-slate-500 mb-1">Total Changes</p>
                      <p className="text-lg font-bold text-slate-800">
                        {diffDetail.total_changes}
                      </p>
                    </div>
                    <div className="bg-green-50 rounded-lg p-4">
                      <p className="text-xs text-slate-500 mb-1">Lines Changed</p>
                      <p className="text-lg font-bold text-green-600">
                        {diffDetail.total_lines_changed}
                      </p>
                    </div>
                    <div className="bg-blue-50 rounded-lg p-4">
                      <p className="text-xs text-slate-500 mb-1">Net Change</p>
                      <p className={`text-lg font-bold ${
                        diffDetail.net_lines_changed >= 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {diffDetail.net_lines_changed >= 0 ? '+' : ''}{diffDetail.net_lines_changed}
                      </p>
                    </div>
                    <div className="bg-purple-50 rounded-lg p-4">
                      <p className="text-xs text-slate-500 mb-1">Diff Span</p>
                      <p className="text-lg font-bold text-purple-600">
                        {diffDetail.diff_span} lines
                      </p>
                    </div>
                  </div>

                  {/* New Changes */}
                  {diffDetail.new_changes && diffDetail.new_changes.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800 mb-3">
                        New Model Changes ({diffDetail.new_changes.length})
                      </h3>
                      <div className="space-y-3">
                        {diffDetail.new_changes.map((change, idx) => (
                          <div key={idx} className="bg-green-50 border border-green-200 rounded-lg p-4">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-sm font-semibold text-green-800">
                                Lines {change.original_start_line}-{change.original_end_line}
                              </span>
                              <span className="text-xs text-slate-600">
                                {change.modified_line_count} → {change.net_lines_changed >= 0 ? '+' : ''}{change.net_lines_changed}
                              </span>
                            </div>
                            <div className="bg-white rounded border border-green-100 p-3 overflow-x-auto">
                              <pre className="text-xs text-slate-700 whitespace-pre-wrap">
                                {change.modified_lines.join('\n')}
                              </pre>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Original Changes */}
                  {diffDetail.original_changes && diffDetail.original_changes.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800 mb-3">
                        Original Model Changes ({diffDetail.original_changes.length})
                      </h3>
                      <div className="space-y-3">
                        {diffDetail.original_changes.map((change, idx) => (
                          <div key={idx} className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-sm font-semibold text-blue-800">
                                Lines {change.original_start_line}-{change.original_end_line}
                              </span>
                              <span className="text-xs text-slate-600">
                                {change.modified_line_count} → {change.net_lines_changed >= 0 ? '+' : ''}{change.net_lines_changed}
                              </span>
                            </div>
                            <div className="bg-white rounded border border-blue-100 p-3 overflow-x-auto">
                              <pre className="text-xs text-slate-700 whitespace-pre-wrap">
                                {change.modified_lines.join('\n')}
                              </pre>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Session Info */}
                  {diffDetail.session_info && (
                    <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                      <h3 className="text-sm font-semibold text-slate-700 mb-2">Session Context</h3>
                      <div className="grid grid-cols-2 gap-3 text-sm">
                        <div>
                          <span className="text-slate-500">Name:</span>
                          <span className="ml-2 font-medium text-slate-800">
                            {diffDetail.session_info.name || 'Untitled'}
                          </span>
                        </div>
                        <div>
                          <span className="text-slate-500">Total Lines:</span>
                          <span className="ml-2 font-medium text-green-600">
                            +{diffDetail.session_info.total_lines_added}
                          </span>
                          <span className="ml-1 font-medium text-red-600">
                            -{diffDetail.session_info.total_lines_removed}
                          </span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-slate-500 text-center py-12">No diff details available</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

