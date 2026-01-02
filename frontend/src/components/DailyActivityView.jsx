import { useState, useEffect } from 'react'
import { Calendar, Clock, MessageSquare, Code, TrendingUp, Activity } from 'lucide-react'

const API_BASE = 'http://127.0.0.1:8000'

export function DailyActivityView({ timeRange }) {
  const [dailyData, setDailyData] = useState([])
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedDate, setSelectedDate] = useState(null)
  const [dayDetail, setDayDetail] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [viewMode, setViewMode] = useState('calendar') // 'calendar' or 'list'

  useEffect(() => {
    loadDailyActivity()
  }, [timeRange])

  const loadDailyActivity = async () => {
    try {
      setLoading(true)
      
      const params = new URLSearchParams()
      // Use last 90 days by default
      const endDate = new Date()
      const startDate = new Date()
      startDate.setDate(startDate.getDate() - 90)
      
      params.append('start_date', startDate.toISOString().split('T')[0])
      params.append('end_date', endDate.toISOString().split('T')[0])
      
      const response = await fetch(`${API_BASE}/api/daily-activity?${params}`)
      const data = await response.json()
      
      setDailyData(data.daily_data)
      setSummary(data.summary)
      setLoading(false)
    } catch (err) {
      console.error('Error loading daily activity:', err)
      setLoading(false)
    }
  }

  const loadDayDetail = async (date) => {
    try {
      setDetailLoading(true)
      const response = await fetch(`${API_BASE}/api/daily-activity/${date}`)
      const data = await response.json()
      setDayDetail(data)
      setDetailLoading(false)
    } catch (err) {
      console.error('Error loading day detail:', err)
      setDetailLoading(false)
    }
  }

  const handleDateClick = (dayData) => {
    if (dayData.has_activity) {
      setSelectedDate(dayData.date)
      loadDayDetail(dayData.date)
    }
  }

  const handleCloseDetail = () => {
    setSelectedDate(null)
    setDayDetail(null)
  }

  const getActivityColor = (dayData) => {
    if (!dayData.has_activity) return 'bg-slate-100'
    const intensity = dayData.session_count
    if (intensity >= 10) return 'bg-green-600'
    if (intensity >= 5) return 'bg-green-500'
    if (intensity >= 3) return 'bg-green-400'
    if (intensity >= 1) return 'bg-green-300'
    return 'bg-green-200'
  }

  const formatDate = (isoString) => {
    const date = new Date(isoString)
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric'
    })
  }

  const formatDuration = (minutes) => {
    if (minutes < 60) return `${Math.round(minutes)}m`
    const hours = Math.floor(minutes / 60)
    const mins = Math.round(minutes % 60)
    return `${hours}h ${mins}m`
  }

  // Group data by weeks for calendar view
  const getCalendarWeeks = () => {
    if (!dailyData.length) return []
    
    const weeks = []
    let currentWeek = []
    
    dailyData.forEach((day, idx) => {
      const date = new Date(day.date)
      const dayOfWeek = date.getDay()
      
      // Start a new week on Sunday
      if (idx === 0 && dayOfWeek !== 0) {
        // Fill empty days at the start
        for (let i = 0; i < dayOfWeek; i++) {
          currentWeek.push(null)
        }
      }
      
      currentWeek.push(day)
      
      // End of week (Saturday) or last day
      if (dayOfWeek === 6 || idx === dailyData.length - 1) {
        weeks.push(currentWeek)
        currentWeek = []
      }
    })
    
    return weeks
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mb-4"></div>
          <p className="text-slate-600">Loading daily activity...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white border border-slate-200 rounded-lg p-4">
            <p className="text-xs text-slate-500 mb-1">Days Active</p>
            <p className="text-2xl font-bold text-slate-800">
              {summary.days_active} / {summary.total_days}
            </p>
          </div>
          <div className="bg-white border border-slate-200 rounded-lg p-4">
            <p className="text-xs text-slate-500 mb-1">Total Sessions</p>
            <p className="text-2xl font-bold text-blue-600">{summary.total_sessions}</p>
          </div>
          <div className="bg-white border border-slate-200 rounded-lg p-4">
            <p className="text-xs text-slate-500 mb-1">Total Messages</p>
            <p className="text-2xl font-bold text-purple-600">{summary.total_messages.toLocaleString()}</p>
          </div>
          <div className="bg-white border border-slate-200 rounded-lg p-4">
            <p className="text-xs text-slate-500 mb-1">Lines Changed</p>
            <p className="text-2xl font-bold text-green-600">
              +{summary.total_lines_added.toLocaleString()}
            </p>
          </div>
        </div>
      )}

      {/* View Toggle */}
      <div className="flex items-center gap-2">
        <button
          onClick={() => setViewMode('calendar')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            viewMode === 'calendar'
              ? 'bg-primary-600 text-white'
              : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
          }`}
        >
          <Calendar className="w-4 h-4 inline mr-2" />
          Calendar View
        </button>
        <button
          onClick={() => setViewMode('list')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            viewMode === 'list'
              ? 'bg-primary-600 text-white'
              : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
          }`}
        >
          <Activity className="w-4 h-4 inline mr-2" />
          List View
        </button>
      </div>

      {/* Calendar View */}
      {viewMode === 'calendar' && (
        <div className="bg-white border border-slate-200 rounded-lg p-6">
          <h2 className="text-xl font-bold text-slate-800 mb-4">Activity Calendar (Last 90 Days)</h2>
          
          {/* Day labels */}
          <div className="grid grid-cols-7 gap-2 mb-2">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
              <div key={day} className="text-center text-xs font-medium text-slate-500">
                {day}
              </div>
            ))}
          </div>

          {/* Calendar grid */}
          <div className="space-y-2">
            {getCalendarWeeks().map((week, weekIdx) => (
              <div key={weekIdx} className="grid grid-cols-7 gap-2">
                {week.map((day, dayIdx) => (
                  <div
                    key={dayIdx}
                    onClick={() => day && handleDateClick(day)}
                    className={`aspect-square rounded-lg flex items-center justify-center text-xs font-medium transition-all ${
                      day ? getActivityColor(day) : 'bg-transparent'
                    } ${
                      day && day.has_activity
                        ? 'cursor-pointer hover:ring-2 hover:ring-primary-500 hover:scale-105'
                        : ''
                    } ${
                      selectedDate === day?.date
                        ? 'ring-2 ring-primary-600 scale-105'
                        : ''
                    }`}
                    title={day ? `${formatDate(day.date)}: ${day.session_count} sessions` : ''}
                  >
                    {day && new Date(day.date).getDate()}
                  </div>
                ))}
              </div>
            ))}
          </div>

          {/* Legend */}
          <div className="flex items-center gap-4 mt-6 text-xs text-slate-600">
            <span>Less</span>
            <div className="flex gap-1">
              <div className="w-4 h-4 rounded bg-slate-100"></div>
              <div className="w-4 h-4 rounded bg-green-200"></div>
              <div className="w-4 h-4 rounded bg-green-300"></div>
              <div className="w-4 h-4 rounded bg-green-400"></div>
              <div className="w-4 h-4 rounded bg-green-500"></div>
              <div className="w-4 h-4 rounded bg-green-600"></div>
            </div>
            <span>More</span>
          </div>
        </div>
      )}

      {/* List View */}
      {viewMode === 'list' && (
        <div className="space-y-3">
          {dailyData.filter(day => day.has_activity).reverse().map((day) => (
            <div
              key={day.date}
              onClick={() => handleDateClick(day)}
              className="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-lg hover:border-primary-300 transition-all cursor-pointer"
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-semibold text-slate-800">
                  {formatDate(day.date)}
                </h3>
                <span className="text-sm text-slate-500">
                  {day.active_hours}h active
                </span>
              </div>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 text-blue-500" />
                  <span className="text-slate-600">{day.session_count} sessions</span>
                </div>
                <div className="flex items-center gap-2">
                  <MessageSquare className="w-4 h-4 text-purple-500" />
                  <span className="text-slate-600">{day.message_count} messages</span>
                </div>
                <div className="flex items-center gap-2">
                  <Code className="w-4 h-4 text-green-500" />
                  <span className="text-slate-600">+{day.lines_added} lines</span>
                </div>
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-orange-500" />
                  <span className="text-slate-600">{day.composer_acceptance_rate}% accepted</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Day Detail Modal */}
      {selectedDate && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-6 border-b border-slate-200">
              <div>
                <h2 className="text-2xl font-bold text-slate-800">
                  {formatDate(selectedDate)}
                </h2>
                <p className="text-sm text-slate-500 mt-1">Daily Activity Summary</p>
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
              ) : dayDetail ? (
                <div className="space-y-6">
                  {/* Day Stats */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-blue-50 rounded-lg p-4">
                      <p className="text-xs text-slate-500 mb-1">Sessions</p>
                      <p className="text-2xl font-bold text-blue-600">
                        {dayDetail.stats.session_count}
                      </p>
                    </div>
                    <div className="bg-purple-50 rounded-lg p-4">
                      <p className="text-xs text-slate-500 mb-1">Messages</p>
                      <p className="text-2xl font-bold text-purple-600">
                        {dayDetail.stats.message_count}
                      </p>
                    </div>
                    <div className="bg-green-50 rounded-lg p-4">
                      <p className="text-xs text-slate-500 mb-1">Lines Added</p>
                      <p className="text-2xl font-bold text-green-600">
                        +{dayDetail.stats.lines_added}
                      </p>
                    </div>
                    <div className="bg-orange-50 rounded-lg p-4">
                      <p className="text-xs text-slate-500 mb-1">Active Time</p>
                      <p className="text-2xl font-bold text-orange-600">
                        {dayDetail.stats.active_hours}h
                      </p>
                    </div>
                  </div>

                  {/* Composer/Tab Stats */}
                  <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                    <h3 className="text-sm font-semibold text-slate-700 mb-3">Code Suggestions</h3>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-slate-600 mb-1">Composer</p>
                        <p className="font-semibold">
                          {dayDetail.stats.composer_accepted_lines} / {dayDetail.stats.composer_suggested_lines}
                          <span className="text-green-600 ml-2">
                            ({dayDetail.stats.composer_acceptance_rate}%)
                          </span>
                        </p>
                      </div>
                      <div>
                        <p className="text-slate-600 mb-1">Tab Completion</p>
                        <p className="font-semibold">
                          {dayDetail.stats.tab_accepted_lines} / {dayDetail.stats.tab_suggested_lines}
                          <span className="text-green-600 ml-2">
                            ({dayDetail.stats.tab_acceptance_rate}%)
                          </span>
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Sessions */}
                  {dayDetail.sessions && dayDetail.sessions.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800 mb-4">
                        Sessions ({dayDetail.sessions.length})
                      </h3>
                      <div className="space-y-3">
                        {dayDetail.sessions.map((session) => (
                          <div key={session.id} className="bg-slate-50 border border-slate-200 rounded-lg p-4">
                            <div className="flex items-start justify-between mb-2">
                              <h4 className="font-semibold text-slate-800">
                                {session.name || 'Untitled Session'}
                              </h4>
                              <span className="text-xs text-slate-500">
                                {new Date(session.created_at).toLocaleTimeString()}
                              </span>
                            </div>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm text-slate-600">
                              <div>
                                <Clock className="w-3 h-3 inline mr-1" />
                                {formatDuration(session.duration_minutes)}
                              </div>
                              <div>
                                <MessageSquare className="w-3 h-3 inline mr-1" />
                                {session.message_count} messages
                              </div>
                              <div>
                                <TrendingUp className="w-3 h-3 inline mr-1 text-green-600" />
                                +{session.lines_added}
                              </div>
                              <div>
                                <TrendingUp className="w-3 h-3 inline mr-1 text-red-600 transform rotate-180" />
                                -{session.lines_removed}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-slate-500 text-center py-12">No details available</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

