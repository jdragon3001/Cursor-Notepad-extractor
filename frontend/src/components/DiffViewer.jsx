import { ChevronDown, ChevronUp, FileEdit } from 'lucide-react'
import { useState } from 'react'

/**
 * DiffViewer - Display code diffs with file edits highlighted
 */
export function DiffViewer({ codeBlock }) {
  const [expanded, setExpanded] = useState(false) // Changed to false (collapsed by default)
  
  // Extract file path - try many possible field names
  const filePath = 
    codeBlock.file_path || 
    codeBlock.filePath || 
    codeBlock.path || 
    codeBlock.file ||
    codeBlock.fileName ||
    codeBlock.filename ||
    // For tool results that might have target_file
    codeBlock.target_file ||
    codeBlock.targetFile ||
    // Extract from raw data if available
    (codeBlock.raw_data && (
      codeBlock.raw_data.file_path ||
      codeBlock.raw_data.filePath ||
      codeBlock.raw_data.path
    )) ||
    'Code Block'
  
  // Check if this is a diff/edit
  const isDiff = codeBlock.old_string || codeBlock.oldString || codeBlock.diff
  
  // Parse diff or code - try many possible field names
  const content = 
    codeBlock.code || 
    codeBlock.content || 
    codeBlock.new_string || 
    codeBlock.newString ||
    codeBlock.text ||
    codeBlock.value ||
    ''
    
  const oldContent = 
    codeBlock.old_string || 
    codeBlock.oldString ||
    ''
  
  // Check if this is a full file (many lines) vs a snippet
  const lineCount = content.split('\n').length
  const isLargeFile = lineCount > 30
  
  return (
    <div className="border border-slate-300 rounded-lg overflow-hidden mb-3">
      {/* File Header */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between px-4 py-2 bg-slate-700 text-slate-100 hover:bg-slate-600 transition-colors"
      >
        <div className="flex items-center gap-2 min-w-0">
          <FileEdit className="w-4 h-4 flex-shrink-0" />
          <span className="font-mono text-sm truncate">{filePath}</span>
          {isDiff && (
            <span className="text-xs bg-blue-600 px-2 py-0.5 rounded flex-shrink-0">EDIT</span>
          )}
          {!isDiff && isLargeFile && (
            <span className="text-xs bg-amber-600 px-2 py-0.5 rounded flex-shrink-0">FULL FILE</span>
          )}
          {!isDiff && lineCount > 0 && (
            <span className="text-xs text-slate-400">{lineCount} lines</span>
          )}
        </div>
        {expanded ? <ChevronUp className="w-4 h-4 flex-shrink-0" /> : <ChevronDown className="w-4 h-4 flex-shrink-0" />}
      </button>
      
      {/* Code Content */}
      {expanded && (
        <div className="bg-slate-900 text-slate-100">
          {isDiff ? (
            <DiffContent oldContent={oldContent} newContent={content} />
          ) : content ? (
            <CodeContent content={content} language={codeBlock.language || codeBlock.lang || 'text'} />
          ) : (
            <div className="p-4 text-slate-400 text-xs font-mono">
              <div className="mb-2 text-amber-400">Debug: Raw code block data</div>
              <pre className="whitespace-pre-wrap">{JSON.stringify(codeBlock, null, 2)}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

/**
 * DiffContent - Show side-by-side or unified diff
 */
function DiffContent({ oldContent, newContent }) {
  const oldLines = oldContent.split('\n')
  const newLines = newContent.split('\n')
  
  return (
    <div className="font-mono text-xs">
      {/* Old Content (Removed) */}
      {oldLines.length > 0 && oldContent.trim() && (
        <div className="bg-red-900/20 border-l-4 border-red-500">
          {oldLines.map((line, i) => (
            <div key={`old-${i}`} className="flex hover:bg-red-900/30">
              <span className="px-3 py-0.5 text-red-400 select-none w-12 text-right flex-shrink-0">
                -{i + 1}
              </span>
              <span className="px-2 py-0.5 text-red-200 flex-1 whitespace-pre">
                {line || ' '}
              </span>
            </div>
          ))}
        </div>
      )}
      
      {/* New Content (Added) */}
      {newLines.length > 0 && (
        <div className="bg-green-900/20 border-l-4 border-green-500">
          {newLines.map((line, i) => (
            <div key={`new-${i}`} className="flex hover:bg-green-900/30">
              <span className="px-3 py-0.5 text-green-400 select-none w-12 text-right flex-shrink-0">
                +{i + 1}
              </span>
              <span className="px-2 py-0.5 text-green-200 flex-1 whitespace-pre">
                {line || ' '}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

/**
 * CodeContent - Display regular code (not a diff)
 * With smart truncation for long files
 */
function CodeContent({ content, language }) {
  const lines = content.split('\n')
  const [showAll, setShowAll] = useState(false)
  
  // If more than 30 lines, truncate unless expanded
  const shouldTruncate = lines.length > 30
  const displayLines = shouldTruncate && !showAll ? lines.slice(0, 30) : lines
  
  return (
    <div>
      <div className="font-mono text-xs">
        {displayLines.map((line, i) => (
          <div key={i} className="flex hover:bg-slate-800">
            <span className="px-3 py-0.5 text-slate-500 select-none w-12 text-right flex-shrink-0">
              {i + 1}
            </span>
            <span className="px-2 py-0.5 text-slate-200 flex-1 whitespace-pre">
              {line || ' '}
            </span>
          </div>
        ))}
      </div>
      
      {shouldTruncate && (
        <div className="p-3 bg-slate-800 border-t border-slate-700 text-center">
          <button
            onClick={() => setShowAll(!showAll)}
            className="text-xs text-blue-400 hover:text-blue-300 font-medium"
          >
            {showAll ? (
              <>▲ Show less ({lines.length} lines total)</>
            ) : (
              <>▼ Show all ({lines.length - 30} more lines)</>
            )}
          </button>
        </div>
      )}
    </div>
  )
}

