import { useState, useEffect } from 'react'
import axios from 'axios'
import { BarChart3, Activity, Database, AlertCircle, Search, Filter, MessageSquare } from 'lucide-react'
import { InfoTooltip } from './components/Tooltip'
import { TimeRangeSelector } from './components/TimeRangeSelector'
import { StatDetailModal } from './components/StatDetailModal'
import { MessageDetailModal } from './components/MessageDetailModal'
import { MessagesView } from './components/MessagesView'
import { ConversationsView } from './components/ConversationsView'
import { getStatDescription } from './statDescriptions'

const API_BASE = 'http://127.0.0.1:8000'

function App() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [summary, setSummary] = useState(null)
  const [stats, setStats] = useState(null)
  const [activeCategory, setActiveCategory] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [filterType, setFilterType] = useState('all')
  const [timeRange, setTimeRange] = useState({ type: 'preset', preset: 'all_time' })
  const [selectedStat, setSelectedStat] = useState(null)
  
  // Message browsing state
  const [messages, setMessages] = useState([])
  const [messagesLoading, setMessagesLoading] = useState(false)
  const [messagesPagination, setMessagesPagination] = useState(null)
  const [selectedMessageId, setSelectedMessageId] = useState(null)
  const [messageFilters, setMessageFilters] = useState({
    page: 1,
    limit: 20,
    sort: 'recent',
    message_type: null,
    has_code: null,
    has_thinking: null,
    has_tools: null,
    search: ''
  })

  // Load stats data on mount and when time range changes
  useEffect(() => {
    loadData()
  }, [timeRange])

  // Load messages when on messages tab or filters change
  useEffect(() => {
    if (activeCategory === 'messages') {
      loadMessages()
    }
  }, [activeCategory, messageFilters])

  const loadMessages = async () => {
    try {
      setMessagesLoading(true)
      
      const params = new URLSearchParams()
      params.append('page', messageFilters.page)
      params.append('limit', messageFilters.limit)
      params.append('sort', messageFilters.sort)
      if (messageFilters.message_type) params.append('message_type', messageFilters.message_type)
      if (messageFilters.has_code !== null) params.append('has_code', messageFilters.has_code)
      if (messageFilters.has_thinking !== null) params.append('has_thinking', messageFilters.has_thinking)
      if (messageFilters.has_tools !== null) params.append('has_tools', messageFilters.has_tools)
      if (messageFilters.search) params.append('search', messageFilters.search)
      
      // Add time range to messages filter
      if (timeRange.type === 'preset') {
        params.append('preset', timeRange.preset)
      } else if (timeRange.type === 'custom') {
        params.append('start_date', timeRange.start)
        params.append('end_date', timeRange.end)
      }
      
      const response = await fetch(`${API_BASE}/api/messages?${params}`)
      const data = await response.json()
      
      setMessages(data.messages)
      setMessagesPagination(data.pagination)
      setMessagesLoading(false)
    } catch (err) {
      console.error('Error loading messages:', err)
      setMessagesLoading(false)
    }
  }

  const handleMessageFilterChange = (key, value) => {
    setMessageFilters(prev => ({ ...prev, [key]: value, page: 1 }))
  }

  const handleMessagePageChange = (newPage) => {
    setMessageFilters(prev => ({ ...prev, page: newPage }))
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)
      
      // Fetch summary for workspace count (only thing not in stats)
      const summaryRes = await axios.get(`${API_BASE}/api/summary`)
      setSummary(summaryRes.data)
      
      // Build query params for time range
      const params = {}
      if (timeRange.type === 'preset') {
        params.preset = timeRange.preset
      } else if (timeRange.type === 'custom') {
        params.start_date = timeRange.start
        params.end_date = timeRange.end
      }
      
      // Fetch stats with time range filter
      const statsRes = await axios.get(`${API_BASE}/api/stats/all`, { params })
      
      // Handle the new response format with stats nested
      if (statsRes.data.stats) {
        setStats(statsRes.data.stats)
      } else {
        setStats(statsRes.data)
      }
      
      setLoading(false)
    } catch (err) {
      console.error('Error loading data:', err)
      setError(err.message)
      setLoading(false)
    }
  }

  const handleTimeRangeChange = (newTimeRange) => {
    setTimeRange(newTimeRange)
  }

  const handleStatClick = (statId, statData, category) => {
    setSelectedStat({ id: statId, data: statData, category })
  }

  const handleCloseModal = () => {
    setSelectedStat(null)
  }

  const renderStatValue = (value, statType) => {
    if (value === null || value === undefined) return 'N/A'
    
    // Handle distribution type - format as nice list
    if (statType === 'distribution' && typeof value === 'object') {
      if (Array.isArray(value)) {
        // Array of items
        return (
          <div className="text-sm space-y-1">
            {value.slice(0, 5).map((item, idx) => (
              <div key={idx} className="flex justify-between">
                <span>{item[0] || item.name || item.label || String(item)}</span>
                <span className="font-semibold">{item[1] || item.count || item.value || ''}</span>
              </div>
            ))}
            {value.length > 5 && <div className="text-slate-500">... and {value.length - 5} more</div>}
          </div>
        )
      } else {
        // Object with keys
        const entries = Object.entries(value).slice(0, 5)
        return (
          <div className="text-sm space-y-1">
            {entries.map(([key, val]) => (
              <div key={key} className="flex justify-between gap-4">
                <span className="text-slate-600">{key}:</span>
                <span className="font-semibold">{typeof val === 'number' ? val.toLocaleString() : String(val)}</span>
              </div>
            ))}
            {Object.keys(value).length > 5 && (
              <div className="text-slate-500">... and {Object.keys(value).length - 5} more</div>
            )}
          </div>
        )
      }
    }
    
    // Handle numeric types
    if (typeof value === 'number') return value.toLocaleString()
    
    // Handle arrays
    if (Array.isArray(value)) {
      if (value.length === 0) return 'None'
      if (value.length <= 3) return value.join(', ')
      return `${value.slice(0, 3).join(', ')} ... (+${value.length - 3} more)`
    }
    
    // Handle objects (last resort)
    if (typeof value === 'object') {
      const entries = Object.entries(value)
      if (entries.length === 0) return 'None'
      if (entries.length <= 2) {
        return entries.map(([k, v]) => `${k}: ${v}`).join(', ')
      }
      return `${entries.length} items`
    }
    
    return String(value)
  }

  // Filter stats based on search query and type filter
  const filterStats = (categoryStats) => {
    return Object.entries(categoryStats).filter(([statId, statData]) => {
      // Search filter
      const matchesSearch = searchQuery === '' || 
        statId.toLowerCase().includes(searchQuery.toLowerCase()) ||
        statData.label.toLowerCase().includes(searchQuery.toLowerCase()) ||
        getStatDescription(statId).toLowerCase().includes(searchQuery.toLowerCase())
      
      // Type filter
      const matchesType = filterType === 'all' || statData.type === filterType
      
      return matchesSearch && matchesType
    })
  }

  // Get all unique stat types
  const getStatTypes = () => {
    if (!stats) return []
    const types = new Set()
    Object.values(stats).forEach(categoryStats => {
      Object.values(categoryStats).forEach(statData => {
        types.add(statData.type)
      })
    })
    return Array.from(types).sort()
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mb-4"></div>
          <p className="text-slate-600 text-lg">Loading Cursor stats...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-slate-800 mb-2 text-center">Error Loading Data</h2>
          <p className="text-slate-600 text-center mb-4">{error}</p>
          <button 
            onClick={loadData}
            className="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white shadow-md border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <BarChart3 className="w-8 h-8 text-primary-600" />
              <h1 className="text-3xl font-bold text-slate-800">Cursor Stats Dashboard</h1>
            </div>
            <div className="flex items-center gap-3">
              <button 
                onClick={loadData}
                className="bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors flex items-center space-x-2"
              >
                <Activity className="w-4 h-4" />
                <span>Refresh</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Summary Cards */}
      {stats && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Time Range Selector */}
          <div className="mb-6">
            <TimeRangeSelector 
              value={timeRange}
              onChange={handleTimeRangeChange}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white rounded-lg shadow-md p-6 border border-slate-200 hover:shadow-lg transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-500 text-sm font-medium">Total Messages</p>
                  <p className="text-3xl font-bold text-slate-800 mt-2">
                    {stats.messages?.total_messages?.value?.toLocaleString() || '0'}
                  </p>
                </div>
                <Database className="w-10 h-10 text-blue-500" />
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6 border border-slate-200 hover:shadow-lg transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-500 text-sm font-medium">Total Sessions</p>
                  <p className="text-3xl font-bold text-slate-800 mt-2">
                    {stats.sessions?.total_sessions?.value?.toLocaleString() || '0'}
                  </p>
                </div>
                <Activity className="w-10 h-10 text-green-500" />
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6 border border-slate-200 hover:shadow-lg transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-500 text-sm font-medium">Code Diffs</p>
                  <p className="text-3xl font-bold text-slate-800 mt-2">
                    {stats.code?.total_diffs?.value?.toLocaleString() || '0'}
                  </p>
                </div>
                <BarChart3 className="w-10 h-10 text-purple-500" />
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6 border border-slate-200 hover:shadow-lg transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-500 text-sm font-medium">Workspaces</p>
                  <p className="text-3xl font-bold text-slate-800 mt-2">
                    {summary?.total_workspaces?.toLocaleString() || '246'}
                  </p>
                </div>
                <Database className="w-10 h-10 text-orange-500" />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Stats Categories */}
      {stats && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
          <div className="bg-white rounded-lg shadow-lg border border-slate-200 overflow-hidden">
            
            {/* Search and Filter Bar */}
            <div className="bg-slate-50 border-b border-slate-200 p-4">
              <div className="flex flex-col md:flex-row gap-4">
                {/* Search Input */}
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input
                    type="text"
                    placeholder="Search stats by name, ID, or description..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
                  />
                </div>
                
                {/* Type Filter */}
                <div className="relative md:w-64">
                  <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <select
                    value={filterType}
                    onChange={(e) => setFilterType(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none appearance-none bg-white"
                  >
                    <option value="all">All Types</option>
                    {getStatTypes().map(type => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                </div>
              </div>
              
              {/* Active Filters Display */}
              {(searchQuery || filterType !== 'all') && (
                <div className="mt-3 flex items-center gap-2 text-sm">
                  <span className="text-slate-600">Active filters:</span>
                  {searchQuery && (
                    <span className="bg-primary-100 text-primary-700 px-2 py-1 rounded-md flex items-center gap-1">
                      Search: "{searchQuery}"
                      <button
                        onClick={() => setSearchQuery('')}
                        className="hover:text-primary-900 ml-1"
                      >
                        ×
                      </button>
                    </span>
                  )}
                  {filterType !== 'all' && (
                    <span className="bg-primary-100 text-primary-700 px-2 py-1 rounded-md flex items-center gap-1">
                      Type: {filterType}
                      <button
                        onClick={() => setFilterType('all')}
                        className="hover:text-primary-900 ml-1"
                      >
                        ×
                      </button>
                    </span>
                  )}
                  <button
                    onClick={() => {
                      setSearchQuery('')
                      setFilterType('all')
                    }}
                    className="text-slate-600 hover:text-slate-800 underline ml-2"
                  >
                    Clear all
                  </button>
                </div>
              )}
            </div>

            {/* Category Tabs */}
            <div className="border-b border-slate-200 bg-slate-50">
              <div className="flex overflow-x-auto">
                <button
                  onClick={() => setActiveCategory('all')}
                  className={`px-6 py-4 text-sm font-medium whitespace-nowrap transition-colors ${
                    activeCategory === 'all'
                      ? 'text-primary-600 border-b-2 border-primary-600 bg-white'
                      : 'text-slate-600 hover:text-slate-800 hover:bg-white'
                  }`}
                >
                  ALL STATS ({Object.values(stats).reduce((acc, cat) => acc + Object.keys(cat).length, 0)})
                </button>
                
                <button
                  onClick={() => setActiveCategory('messages')}
                  className={`px-6 py-4 text-sm font-medium whitespace-nowrap transition-colors ${
                    activeCategory === 'messages'
                      ? 'text-primary-600 border-b-2 border-primary-600 bg-white'
                      : 'text-slate-600 hover:text-slate-800 hover:bg-white'
                  }`}
                >
                  <MessageSquare className="w-4 h-4 inline mr-2" />
                  MESSAGES ({messagesPagination?.total_count?.toLocaleString() || stats.messages?.total_messages?.value?.toLocaleString() || '0'})
                </button>
                
                <button
                  onClick={() => setActiveCategory('conversations')}
                  className={`px-6 py-4 text-sm font-medium whitespace-nowrap transition-colors ${
                    activeCategory === 'conversations'
                      ? 'text-primary-600 border-b-2 border-primary-600 bg-white'
                      : 'text-slate-600 hover:text-slate-800 hover:bg-white'
                  }`}
                >
                  CONVERSATIONS ({stats.sessions?.total_sessions?.value?.toLocaleString() || '0'})
                </button>

                {Object.keys(stats).filter(cat => cat !== 'messages').map((category) => (
                  <button
                    key={category}
                    onClick={() => setActiveCategory(category)}
                    className={`px-6 py-4 text-sm font-medium whitespace-nowrap transition-colors ${
                      activeCategory === category
                        ? 'text-primary-600 border-b-2 border-primary-600 bg-white'
                        : 'text-slate-600 hover:text-slate-800 hover:bg-white'
                    }`}
                  >
                    {category.replace('_', ' ').toUpperCase()} ({Object.keys(stats[category]).length})
                  </button>
                ))}
              </div>
            </div>

            {/* Content Area */}
            <div className="p-6">
              {/* Messages Browse View */}
              {activeCategory === 'messages' && (
                <MessagesView 
                  messages={messages}
                  loading={messagesLoading}
                  pagination={messagesPagination}
                  filters={messageFilters}
                  onFilterChange={handleMessageFilterChange}
                  onPageChange={handleMessagePageChange}
                  onMessageClick={(msgId) => setSelectedMessageId(msgId)}
                />
              )}
              
              {/* Conversations View */}
              {activeCategory === 'conversations' && (
                <ConversationsView />
              )}

              {/* Stats List View */}
              {activeCategory !== 'messages' && activeCategory !== 'conversations' && (
                <div className="space-y-4">
                  {Object.entries(stats)
                    .filter(([category]) => activeCategory === 'all' || activeCategory === category)
                    .filter(([category]) => category !== 'messages')
                    .map(([category, categoryStats]) => {
                      const filteredStats = filterStats(categoryStats)
                      
                      if (filteredStats.length === 0) return null
                      
                      return (
                        <div key={category} className="space-y-3">
                          {activeCategory === 'all' && (
                            <h3 className="text-lg font-semibold text-slate-800 border-b pb-2 mb-3">
                              {category.replace('_', ' ').toUpperCase()}
                            </h3>
                          )}
                          {filteredStats.map(([statId, statData]) => (
                            <div 
                              key={`${category}-${statId}`}
                              className="bg-slate-50 rounded-lg p-4 hover:bg-slate-100 transition-colors border border-slate-200 cursor-pointer"
                              onClick={() => handleStatClick(statId, statData, category)}
                            >
                              <div className="flex items-start justify-between">
                                <div className="flex-1">
                                  <div className="flex items-center space-x-2 mb-2">
                                    <span className="text-xs font-mono bg-primary-100 text-primary-700 px-2 py-1 rounded">
                                      {statId}
                                    </span>
                                    <span className="text-xs font-mono bg-slate-200 text-slate-700 px-2 py-1 rounded">
                                      {statData.type}
                                    </span>
                                    <InfoTooltip description={getStatDescription(statId)} />
                                  </div>
                                  <p className="text-slate-700 font-medium mb-1">{statData.label}</p>
                                  <p className="text-xs text-slate-500">Source: {statData.data_source}</p>
                                </div>
                                <div className="text-right ml-4">
                                  <div className="text-2xl font-bold text-slate-800">
                                    {renderStatValue(statData.value, statData.type)}
                                  </div>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )
                    })}
                  
                  {/* No Results Message */}
                  {Object.entries(stats)
                    .filter(([category]) => activeCategory === 'all' || activeCategory === category)
                    .filter(([category]) => category !== 'messages')
                    .every(([_, categoryStats]) => filterStats(categoryStats).length === 0) && (
                    <div className="text-center py-12">
                      <AlertCircle className="w-16 h-16 text-slate-300 mx-auto mb-4" />
                      <h3 className="text-xl font-semibold text-slate-700 mb-2">No stats found</h3>
                      <p className="text-slate-500">Try adjusting your search or filters</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Message Detail Modal */}
      {selectedMessageId && (
        <MessageDetailModal
          messageId={selectedMessageId}
          onClose={() => setSelectedMessageId(null)}
        />
      )}

      {/* Stat Detail Modal */}
      {selectedStat && (
        <StatDetailModal
          stat={selectedStat.data}
          statId={selectedStat.id}
          category={selectedStat.category}
          onClose={handleCloseModal}
        />
      )}

      {/* Message Detail Modal */}
      {selectedMessageId && (
        <MessageDetailModal
          messageId={selectedMessageId}
          onClose={() => setSelectedMessageId(null)}
        />
      )}
    </div>
  )
}

export default App
