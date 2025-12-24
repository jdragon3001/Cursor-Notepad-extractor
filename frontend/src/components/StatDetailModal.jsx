import { useState, useEffect } from 'react'
import { X, TrendingUp, TrendingDown, Minus, Calendar, BarChart3 } from 'lucide-react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000'

/**
 * StatDetailModal Component
 * 
 * Shows detailed information about a stat including:
 * - Time series chart
 * - Detailed description
 * - Underlying data
 */
export function StatDetailModal({ stat, statId, category, onClose }) {
  const [timeSeriesData, setTimeSeriesData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [granularity, setGranularity] = useState('day')
  const [preset, setPreset] = useState('last_30_days')

  useEffect(() => {
    loadTimeSeriesData()
  }, [statId, granularity, preset])

  const loadTimeSeriesData = async () => {
    try {
      setLoading(true)
      console.log('Loading time series for:', statId, 'preset:', preset, 'granularity:', granularity)
      
      const response = await axios.get(`${API_BASE}/api/stats/time-series/${statId}`, {
        params: {
          preset: preset,
          granularity: granularity
        }
      })
      
      console.log('Time series response:', response.data)
      console.log('Series data:', response.data?.series)
      console.log('Series has entries:', response.data?.series ? Object.keys(response.data.series).length : 0)
      
      setTimeSeriesData(response.data)
      setLoading(false)
    } catch (err) {
      console.error('Error loading time series:', err)
      console.error('Error response:', err.response?.data)
      setLoading(false)
    }
  }

  // Format time series data for charts
  const getChartData = () => {
    if (!timeSeriesData?.series) return []
    
    return Object.entries(timeSeriesData.series).map(([date, count]) => ({
      date: formatDateLabel(date, granularity),
      value: count
    }))
  }

  const formatDateLabel = (dateStr, gran) => {
    const date = new Date(dateStr)
    
    if (gran === 'day') {
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    } else if (gran === 'week') {
      return `Week of ${date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`
    } else if (gran === 'month') {
      return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    }
    return dateStr
  }

  const calculateTrend = () => {
    const data = getChartData()
    if (data.length < 2) return { trend: 'neutral', percent: 0 }

    const firstHalf = data.slice(0, Math.floor(data.length / 2))
    const secondHalf = data.slice(Math.floor(data.length / 2))

    const firstAvg = firstHalf.reduce((sum, d) => sum + d.value, 0) / firstHalf.length
    const secondAvg = secondHalf.reduce((sum, d) => sum + d.value, 0) / secondHalf.length

    if (firstAvg === 0) return { trend: 'neutral', percent: 0 }

    const percentChange = ((secondAvg - firstAvg) / firstAvg) * 100

    return {
      trend: percentChange > 5 ? 'up' : percentChange < -5 ? 'down' : 'neutral',
      percent: Math.abs(percentChange).toFixed(1)
    }
  }

  const trendInfo = calculateTrend()

  // Stop scroll propagation to modal backdrop
  const handleModalClick = (e) => {
    e.stopPropagation()
  }

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <div 
        className="bg-white rounded-xl shadow-2xl max-w-5xl w-full max-h-[90vh] overflow-hidden flex flex-col"
        onClick={handleModalClick}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white p-6 flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-mono bg-white bg-opacity-20 px-2 py-1 rounded">
                {statId}
              </span>
              <span className="text-xs font-mono bg-white bg-opacity-20 px-2 py-1 rounded">
                {stat.type}
              </span>
            </div>
            <h2 className="text-2xl font-bold mb-1">{stat.label}</h2>
            <p className="text-primary-100 text-sm">Category: {category.replace('_', ' ').toUpperCase()}</p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-white hover:bg-opacity-20 rounded-lg p-2 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {/* Current Value Card */}
          <div className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg p-6 mb-6 border border-slate-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-600 mb-1">Current Value</p>
                <p className="text-4xl font-bold text-slate-800">
                  {typeof stat.value === 'number' ? stat.value.toLocaleString() : stat.value}
                </p>
              </div>
              
              {/* Trend Indicator */}
              <div className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                trendInfo.trend === 'up' ? 'bg-green-100 text-green-700' :
                trendInfo.trend === 'down' ? 'bg-red-100 text-red-700' :
                'bg-slate-200 text-slate-700'
              }`}>
                {trendInfo.trend === 'up' && <TrendingUp className="w-5 h-5" />}
                {trendInfo.trend === 'down' && <TrendingDown className="w-5 h-5" />}
                {trendInfo.trend === 'neutral' && <Minus className="w-5 h-5" />}
                <span className="font-semibold">
                  {trendInfo.trend === 'neutral' ? 'Stable' : `${trendInfo.percent}%`}
                </span>
              </div>
            </div>
            
            <div className="mt-4 text-sm text-slate-600">
              <p><strong>Source:</strong> {stat.data_source}</p>
            </div>
          </div>

          {/* Controls */}
          <div className="flex items-center gap-4 mb-4">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-slate-600" />
              <span className="text-sm font-medium text-slate-700">Time Range:</span>
              <select
                value={preset}
                onChange={(e) => setPreset(e.target.value)}
                className="px-3 py-1.5 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
              >
                <option value="last_7_days">Last 7 Days</option>
                <option value="last_30_days">Last 30 Days</option>
                <option value="last_90_days">Last 90 Days</option>
                <option value="this_month">This Month</option>
                <option value="this_year">This Year</option>
              </select>
            </div>

            <div className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-slate-600" />
              <span className="text-sm font-medium text-slate-700">Granularity:</span>
              <select
                value={granularity}
                onChange={(e) => setGranularity(e.target.value)}
                className="px-3 py-1.5 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
              >
                <option value="day">Daily</option>
                <option value="week">Weekly</option>
                <option value="month">Monthly</option>
              </select>
            </div>
          </div>

          {/* Time Series Chart */}
          <div className="bg-white border border-slate-200 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-slate-800 mb-4">Trend Over Time</h3>
            
            {loading ? (
              <div className="h-64 flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
              </div>
            ) : getChartData().length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={getChartData()}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis 
                    dataKey="date" 
                    stroke="#64748b"
                    style={{ fontSize: '12px' }}
                  />
                  <YAxis 
                    stroke="#64748b"
                    style={{ fontSize: '12px' }}
                  />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#fff', 
                      border: '1px solid #e2e8f0',
                      borderRadius: '8px',
                      boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
                    }}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="value" 
                    name={stat.label}
                    stroke="#3b82f6" 
                    strokeWidth={2}
                    dot={{ fill: '#3b82f6', r: 4 }}
                    activeDot={{ r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-64 flex items-center justify-center text-slate-500">
                <div className="text-center">
                  <BarChart3 className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>No time series data available for this stat</p>
                </div>
              </div>
            )}
          </div>

          {/* Additional Info */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="text-sm font-semibold text-blue-900 mb-2">About This Stat</h4>
            <p className="text-sm text-blue-800">
              This statistic is calculated from <strong>{stat.data_source}</strong> data 
              and represents {stat.label.toLowerCase()}.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-slate-50 border-t border-slate-200 p-4 flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 font-medium rounded-lg transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

