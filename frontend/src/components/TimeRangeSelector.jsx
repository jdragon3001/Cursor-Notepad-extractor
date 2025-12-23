import { useState, useEffect } from 'react'
import { Calendar, ChevronDown } from 'lucide-react'

/**
 * TimeRangeSelector Component
 * 
 * Allows users to select time ranges for filtering stats.
 * Supports preset ranges and custom date ranges.
 */
export function TimeRangeSelector({ value, onChange, className = '' }) {
  const [presets, setPresets] = useState([])
  const [showCustom, setShowCustom] = useState(false)
  const [customStart, setCustomStart] = useState('')
  const [customEnd, setCustomEnd] = useState('')

  // Load presets from API
  useEffect(() => {
    const defaultPresets = [
      { id: 'all_time', label: 'All Time' },
      { id: 'last_7_days', label: 'Last 7 Days' },
      { id: 'last_30_days', label: 'Last 30 Days' },
      { id: 'last_90_days', label: 'Last 90 Days' },
      { id: 'this_month', label: 'This Month' },
      { id: 'last_month', label: 'Last Month' },
      { id: 'this_quarter', label: 'This Quarter' },
      { id: 'this_year', label: 'This Year' },
    ]
    setPresets(defaultPresets)
  }, [])

  const handlePresetClick = (presetId) => {
    setShowCustom(false)
    onChange({ type: 'preset', preset: presetId })
  }

  const handleCustomApply = () => {
    if (customStart && customEnd) {
      onChange({
        type: 'custom',
        start: customStart,
        end: customEnd
      })
      setShowCustom(false)
    }
  }

  const getActiveLabel = () => {
    if (value?.type === 'preset') {
      const preset = presets.find(p => p.id === value.preset)
      return preset?.label || 'Select Range'
    } else if (value?.type === 'custom') {
      return `${value.start} to ${value.end}`
    }
    return 'All Time'
  }

  return (
    <div className={`relative ${className}`}>
      <div className="flex items-center gap-2">
        {/* Preset Buttons */}
        <div className="flex items-center gap-2 flex-wrap">
          {presets.slice(0, 4).map((preset) => (
            <button
              key={preset.id}
              onClick={() => handlePresetClick(preset.id)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                value?.preset === preset.id
                  ? 'bg-primary-600 text-white shadow-md'
                  : 'bg-white text-slate-700 border border-slate-300 hover:border-primary-500 hover:bg-primary-50'
              }`}
            >
              {preset.label}
            </button>
          ))}
        </div>

        {/* More Options Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowCustom(!showCustom)}
            className="px-4 py-2 bg-white border border-slate-300 rounded-lg text-sm font-medium text-slate-700 hover:border-primary-500 hover:bg-primary-50 transition-all flex items-center gap-2"
          >
            <Calendar className="w-4 h-4" />
            <span>More</span>
            <ChevronDown className={`w-4 h-4 transition-transform ${showCustom ? 'rotate-180' : ''}`} />
          </button>

          {/* Dropdown Menu */}
          {showCustom && (
            <div className="absolute right-0 mt-2 w-80 bg-white border border-slate-200 rounded-lg shadow-xl z-50">
              <div className="p-4">
                <h3 className="text-sm font-semibold text-slate-700 mb-3">Select Time Range</h3>
                
                {/* Remaining Presets */}
                <div className="space-y-1 mb-4">
                  {presets.slice(4).map((preset) => (
                    <button
                      key={preset.id}
                      onClick={() => handlePresetClick(preset.id)}
                      className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors ${
                        value?.preset === preset.id
                          ? 'bg-primary-100 text-primary-700 font-medium'
                          : 'text-slate-700 hover:bg-slate-100'
                      }`}
                    >
                      {preset.label}
                    </button>
                  ))}
                </div>

                {/* Custom Date Range */}
                <div className="border-t border-slate-200 pt-4">
                  <h4 className="text-sm font-medium text-slate-700 mb-2">Custom Range</h4>
                  <div className="space-y-2">
                    <div>
                      <label className="text-xs text-slate-600 mb-1 block">Start Date</label>
                      <input
                        type="date"
                        value={customStart}
                        onChange={(e) => setCustomStart(e.target.value)}
                        className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
                      />
                    </div>
                    <div>
                      <label className="text-xs text-slate-600 mb-1 block">End Date</label>
                      <input
                        type="date"
                        value={customEnd}
                        onChange={(e) => setCustomEnd(e.target.value)}
                        className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
                      />
                    </div>
                    <button
                      onClick={handleCustomApply}
                      disabled={!customStart || !customEnd}
                      className="w-full px-4 py-2 bg-primary-600 text-white rounded-md text-sm font-medium hover:bg-primary-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors"
                    >
                      Apply Custom Range
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Current Selection Display */}
      {value && (
        <div className="mt-2 text-sm text-slate-600">
          <span className="font-medium">Showing:</span> {getActiveLabel()}
        </div>
      )}

      {/* Click outside to close */}
      {showCustom && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setShowCustom(false)}
        />
      )}
    </div>
  )
}

