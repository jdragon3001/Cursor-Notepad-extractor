import { useState, useEffect } from 'react'
import { MessageSquare, User, Bot, Calendar, Code, Brain, Wrench, ChevronRight, ArrowLeft } from 'lucide-react'
import { MessageDetailModal } from '../components/MessageDetailModal'

const API_BASE = 'http://127.0.0.1:8000'

/**
 * BrowsePage - Explore actual messages, sessions, and data
 */
export function BrowsePage({ onBack }) {
  const [activeTab, setActiveTab] = useState('messages')

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white shadow-md border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <button
                onClick={onBack}
                className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                title="Back to Stats"
              >
                <ArrowLeft className="w-6 h-6 text-slate-600" />
              </button>
              <MessageSquare className="w-8 h-8 text-primary-600" />
              <div>
                <h1 className="text-3xl font-bold text-slate-800">Browse Data</h1>
                <p className="text-sm text-slate-600">Explore your messages, sessions, and activity</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="bg-white rounded-lg shadow-md border border-slate-200">
          <div className="border-b border-slate-200">
            <div className="flex">
              <button
                onClick={() => setActiveTab('messages')}
                className={`px-6 py-4 text-sm font-medium transition-colors ${
                  activeTab === 'messages'
                    ? 'text-primary-600 border-b-2 border-primary-600 bg-white'
                    : 'text-slate-600 hover:text-slate-800 hover:bg-slate-50'
                }`}
              >
                <div className="flex items-center gap-2">
                  <MessageSquare className="w-4 h-4" />
                  <span>MESSAGES</span>
                </div>
              </button>
              
              <button
                onClick={() => setActiveTab('sessions')}
                className={`px-6 py-4 text-sm font-medium transition-colors ${
                  activeTab === 'sessions'
                    ? 'text-primary-600 border-b-2 border-primary-600 bg-white'
                    : 'text-slate-600 hover:text-slate-800 hover:bg-slate-50'
                }`}
                disabled
              >
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  <span>SESSIONS</span>
                  <span className="text-xs bg-slate-200 px-2 py-0.5 rounded">Coming Soon</span>
                </div>
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="p-6">
            {activeTab === 'messages' && <MessagesTab />}
            {activeTab === 'sessions' && <div className="text-center py-12 text-slate-500">Coming soon...</div>}
          </div>
        </div>
      </div>
    </div>
  )
}

/**
 * MessagesTab - Browse and filter messages
 */
function MessagesTab() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(true)
  const [pagination, setPagination] = useState(null)
  const [selectedMessageId, setSelectedMessageId] = useState(null)
  const [filters, setFilters] = useState({
    page: 1,
    limit: 20,
    sort: 'recent',
    message_type: null,
    has_code: null,
    has_thinking: null,
    has_tools: null,
    search: ''
  })

  // Load messages when filters change
  useEffect(() => {
    loadMessages()
  }, [filters])

  const loadMessages = async () => {
    try {
      setLoading(true)
      
      const params = new URLSearchParams()
      params.append('page', filters.page)
      params.append('limit', filters.limit)
      params.append('sort', filters.sort)
      if (filters.message_type) params.append('message_type', filters.message_type)
      if (filters.has_code !== null) params.append('has_code', filters.has_code)
      if (filters.has_thinking !== null) params.append('has_thinking', filters.has_thinking)
      if (filters.has_tools !== null) params.append('has_tools', filters.has_tools)
      if (filters.search) params.append('search', filters.search)
      
      const response = await fetch(`${API_BASE}/api/messages?${params}`)
      const data = await response.json()
      
      setMessages(data.messages)
      setPagination(data.pagination)
      setLoading(false)
    } catch (err) {
      console.error('Error loading messages:', err)
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

  return (
    <div className="space-y-6">
      {/* Filters & Controls */}
      <div className="flex flex-wrap items-center gap-4 pb-4 border-b border-slate-200">
        {/* Search */}
        <input
          type="text"
          placeholder="Search messages..."
          value={filters.search}
          onChange={(e) => handleFilterChange('search', e.target.value)}
          className="flex-1 min-w-[200px] px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
        />
        
        {/* Sort */}
        <select
          value={filters.sort}
          onChange={(e) => handleFilterChange('sort', e.target.value)}
          className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
        >
          <option value="recent">Most Recent</option>
          <option value="oldest">Oldest First</option>
          <option value="longest">Longest</option>
          <option value="shortest">Shortest</option>
        </select>
        
        {/* Type Filter */}
        <select
          value={filters.message_type || 'all'}
          onChange={(e) => handleFilterChange('message_type', e.target.value === 'all' ? null : e.target.value)}
          className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
        >
          <option value="all">All Messages</option>
          <option value="user">User Only</option>
          <option value="ai">AI Only</option>
        </select>
        
        {/* Items per page */}
        <select
          value={filters.limit}
          onChange={(e) => handleFilterChange('limit', parseInt(e.target.value))}
          className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
        >
          <option value="10">10 per page</option>
          <option value="20">20 per page</option>
          <option value="50">50 per page</option>
          <option value="100">100 per page</option>
        </select>
      </div>

      {/* Feature Filters */}
      <div className="flex flex-wrap gap-3">
        <button
          onClick={() => handleFilterChange('has_code', filters.has_code === true ? null : true)}
          className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
            filters.has_code === true
              ? 'bg-primary-600 text-white'
              : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
          }`}
        >
          <Code className="w-4 h-4 inline mr-1" />
          Has Code
        </button>
        
        <button
          onClick={() => handleFilterChange('has_thinking', filters.has_thinking === true ? null : true)}
          className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
            filters.has_thinking === true
              ? 'bg-primary-600 text-white'
              : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
          }`}
        >
          <Brain className="w-4 h-4 inline mr-1" />
          Has Thinking
        </button>
        
        <button
          onClick={() => handleFilterChange('has_tools', filters.has_tools === true ? null : true)}
          className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
            filters.has_tools === true
              ? 'bg-primary-600 text-white'
              : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
          }`}
        >
          <Wrench className="w-4 h-4 inline mr-1" />
          Has Tools
        </button>
      </div>

      {/* Results Count */}
      {pagination && (
        <div className="text-sm text-slate-600">
          Showing {((pagination.page - 1) * pagination.limit) + 1} - {Math.min(pagination.page * pagination.limit, pagination.total_count)} of {pagination.total_count.toLocaleString()} messages
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="text-slate-600 mt-4">Loading messages...</p>
        </div>
      )}

      {/* Messages List */}
      {!loading && messages.length > 0 && (
        <div className="space-y-3">
          {messages.map((message) => (
            <MessageCard 
              key={message.id} 
              message={message} 
              onClick={() => setSelectedMessageId(message.id)}
            />
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && messages.length === 0 && (
        <div className="text-center py-12">
          <MessageSquare className="w-16 h-16 text-slate-300 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-slate-700 mb-2">No messages found</h3>
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

/**
 * MessageCard - Individual message preview card
 */
function MessageCard({ message, onClick }) {
  const formatDate = (isoString) => {
    const date = new Date(isoString)
    const now = new Date()
    const diff = now - date
    
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    const days = Math.floor(diff / 86400000)
    
    if (minutes < 1) return 'Just now'
    if (minutes < 60) return `${minutes}m ago`
    if (hours < 24) return `${hours}h ago`
    if (days < 7) return `${days}d ago`
    return date.toLocaleDateString()
  }

  const isUser = message.type === 'user'

  return (
    <div 
      onClick={onClick}
      className="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
    >
      <div className="flex items-start gap-4">
        {/* Icon */}
        <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
          isUser ? 'bg-blue-100' : 'bg-purple-100'
        }`}>
          {isUser ? (
            <User className="w-5 h-5 text-blue-600" />
          ) : (
            <Bot className="w-5 h-5 text-purple-600" />
          )}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          {/* Header */}
          <div className="flex items-center gap-2 mb-2">
            <span className={`font-semibold ${isUser ? 'text-blue-700' : 'text-purple-700'}`}>
              {isUser ? 'USER' : 'AI'}
            </span>
            <span className="text-slate-400">•</span>
            <span className="text-sm text-slate-500">{formatDate(message.created_at)}</span>
          </div>

          {/* Preview Text */}
          <p className="text-slate-700 mb-3 line-clamp-3">
            {message.text_preview || message.text || <em className="text-slate-400">No text content</em>}
          </p>

          {/* Metadata */}
          <div className="flex flex-wrap items-center gap-4 text-sm text-slate-500">
            <span>{message.word_count} words</span>
            
            {message.has_code && (
              <span className="flex items-center gap-1">
                <Code className="w-3.5 h-3.5" />
                {message.code_block_count} blocks
              </span>
            )}
            
            {message.has_thinking && (
              <span className="flex items-center gap-1">
                <Brain className="w-3.5 h-3.5" />
                Thinking
              </span>
            )}
            
            {message.has_tools && (
              <span className="flex items-center gap-1">
                <Wrench className="w-3.5 h-3.5" />
                {message.tool_count} tools
              </span>
            )}
            
            {message.token_count > 0 && (
              <span>{message.token_count.toLocaleString()} tokens</span>
            )}
          </div>
        </div>

        {/* Arrow */}
        <ChevronRight className="w-5 h-5 text-slate-400 flex-shrink-0" />
      </div>
    </div>
  )
}

