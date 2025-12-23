import { MessageSquare, User, Bot, Code, Brain, Wrench, ChevronRight } from 'lucide-react'

/**
 * MessagesView - Browse messages with filtering (embedded in main dashboard)
 */
export function MessagesView({ messages, loading, pagination, filters, onFilterChange, onPageChange, onMessageClick }) {
  
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

  return (
    <div className="space-y-6">
      {/* Filters & Controls */}
      <div className="flex flex-wrap items-center gap-4 pb-4 border-b border-slate-200">
        {/* Search */}
        <input
          type="text"
          placeholder="Search messages..."
          value={filters.search}
          onChange={(e) => onFilterChange('search', e.target.value)}
          className="flex-1 min-w-[200px] px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
        />
        
        {/* Sort */}
        <select
          value={filters.sort}
          onChange={(e) => onFilterChange('sort', e.target.value)}
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
          onChange={(e) => onFilterChange('message_type', e.target.value === 'all' ? null : e.target.value)}
          className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
        >
          <option value="all">All Messages</option>
          <option value="user">User Only</option>
          <option value="ai">AI Only</option>
        </select>
        
        {/* Items per page */}
        <select
          value={filters.limit}
          onChange={(e) => onFilterChange('limit', parseInt(e.target.value))}
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
          onClick={() => onFilterChange('has_code', filters.has_code === true ? null : true)}
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
          onClick={() => onFilterChange('has_thinking', filters.has_thinking === true ? null : true)}
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
          onClick={() => onFilterChange('has_tools', filters.has_tools === true ? null : true)}
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
              formatDate={formatDate}
              onClick={() => onMessageClick(message.id)}
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
            onClick={() => onPageChange(pagination.page - 1)}
            disabled={!pagination.has_prev}
            className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          
          <span className="px-4 py-2 text-sm text-slate-600">
            Page {pagination.page} of {pagination.total_pages}
          </span>
          
          <button
            onClick={() => onPageChange(pagination.page + 1)}
            disabled={!pagination.has_next}
            className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}

/**
 * MessageCard - Individual message preview card
 */
function MessageCard({ message, formatDate, onClick }) {
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

