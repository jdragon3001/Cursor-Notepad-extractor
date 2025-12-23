import { useState } from 'react'
import { HelpCircle } from 'lucide-react'

/**
 * Tooltip component that shows on hover
 * @param {Object} props
 * @param {string} props.content - The tooltip text to display
 * @param {React.ReactNode} props.children - The element to attach tooltip to
 * @param {string} props.position - Position of tooltip (top, right, bottom, left)
 */
export default function Tooltip({ content, children, position = 'top' }) {
  const [isVisible, setIsVisible] = useState(false)

  if (!content) return children

  const positionClasses = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
  }

  const arrowClasses = {
    top: 'top-full left-1/2 -translate-x-1/2 border-l-transparent border-r-transparent border-b-transparent border-t-slate-800',
    bottom: 'bottom-full left-1/2 -translate-x-1/2 border-l-transparent border-r-transparent border-t-transparent border-b-slate-800',
    left: 'left-full top-1/2 -translate-y-1/2 border-t-transparent border-b-transparent border-r-transparent border-l-slate-800',
    right: 'right-full top-1/2 -translate-y-1/2 border-t-transparent border-b-transparent border-l-transparent border-r-slate-800',
  }

  return (
    <div className="relative inline-block">
      <div
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
        className="cursor-help"
      >
        {children}
      </div>
      
      {isVisible && (
        <div
          className={`absolute z-50 ${positionClasses[position]} pointer-events-none`}
          style={{ width: 'max-content', maxWidth: '300px' }}
        >
          <div className="bg-slate-800 text-white text-sm rounded-lg px-3 py-2 shadow-lg">
            {content}
          </div>
          <div
            className={`absolute w-0 h-0 border-4 ${arrowClasses[position]}`}
          />
        </div>
      )}
    </div>
  )
}

/**
 * Info icon with tooltip - used for stat descriptions
 * @param {Object} props
 * @param {string} props.description - The description to show in tooltip
 */
export function InfoTooltip({ description }) {
  return (
    <Tooltip content={description} position="top">
      <HelpCircle className="w-4 h-4 text-slate-400 hover:text-slate-600 transition-colors" />
    </Tooltip>
  )
}

