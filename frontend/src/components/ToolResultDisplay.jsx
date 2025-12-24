import { ChevronDown, ChevronUp, FileEdit, Code } from 'lucide-react'
import { useState } from 'react'

/**
 * ToolResultDisplay - Display a tool call with file edits as diffs
 */
export function ToolResultDisplay({ tool, index, expanded, onToggle }) {
  const toolName = tool.tool_name || tool.name || tool.toolName || 'Tool'
  const toolArgs = tool.args || tool.arguments || tool.toolArgs || {}
  const toolResult = tool.result || tool.output || tool.toolResult || ''
  const toolStatus = tool.status || 'unknown'
  
  // Check if this is a file edit tool (search_replace, write, etc.)
  const isFileEdit = toolName === 'search_replace' || toolName === 'write' || toolName === 'edit_notebook'
  
  // Extract file path - try many possible fields
  const filePath = 
    toolArgs.file_path || 
    toolArgs.target_file || 
    toolArgs.target_notebook ||
    toolArgs.filePath ||
    toolArgs.targetFile ||
    tool.file_path ||
    tool.filePath ||
    'Unknown file'
  
  // Extract old/new content for diffs
  const oldContent = toolArgs.old_string || toolArgs.oldString || tool.old_string || ''
  const newContent = toolArgs.new_string || toolArgs.newString || toolArgs.contents || toolArgs.content || tool.new_string || ''
  
  // Check if we have usable data
  const hasEditData = isFileEdit && (oldContent || newContent)
  
  return (
    <div className="border border-slate-300 rounded-lg overflow-hidden">
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between p-3 bg-slate-50 hover:bg-slate-100 transition-colors"
      >
        <div className="flex items-center gap-2 min-w-0 flex-1">
          {isFileEdit ? (
            <FileEdit className="w-4 h-4 text-blue-600 flex-shrink-0" />
          ) : (
            <Code className="w-4 h-4 text-slate-600 flex-shrink-0" />
          )}
          <span className="text-sm font-medium text-slate-800 truncate">
            {isFileEdit ? 'File Edit' : toolName}
          </span>
          {isFileEdit && filePath && filePath !== 'Unknown file' && (
            <span className="text-xs text-slate-600 font-mono truncate">
              {filePath}
            </span>
          )}
          {toolStatus && toolStatus !== 'unknown' && (
            <span className={`text-xs px-2 py-0.5 rounded-full flex-shrink-0 ${
              toolStatus === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
            }`}>
              {toolStatus}
            </span>
          )}
        </div>
        {expanded ? <ChevronUp className="w-4 h-4 flex-shrink-0" /> : <ChevronDown className="w-4 h-4 flex-shrink-0" />}
      </button>
      
      {expanded && (
        <div className="bg-slate-900 text-slate-100">
          {hasEditData ? (
            <DiffContent oldContent={oldContent} newContent={newContent} filePath={filePath} />
          ) : (
            <div className="p-3 text-xs font-mono overflow-x-auto max-h-96 overflow-y-auto">
              {/* Show debug info if it's supposed to be a file edit but we can't find the data */}
              {isFileEdit && !hasEditData && (
                <div className="mb-3 p-2 bg-amber-900/30 border border-amber-500/30 rounded text-amber-300">
                  <div className="font-semibold mb-1">⚠️ Debug: File edit tool but missing data</div>
                  <pre className="whitespace-pre-wrap text-xs">
                    {JSON.stringify({ toolName, toolArgs, tool }, null, 2)}
                  </pre>
                </div>
              )}
              <pre className="whitespace-pre-wrap break-words">
                {typeof toolResult === 'string' ? toolResult : JSON.stringify(toolResult, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

/**
 * DiffContent - Show file edit diff with green/red highlighting
 */
function DiffContent({ oldContent, newContent, filePath }) {
  const oldLines = oldContent.split('\n')
  const newLines = newContent.split('\n')
  
  return (
    <div className="font-mono text-xs">
      {/* File path header */}
      {filePath && (
        <div className="px-4 py-2 bg-slate-800 text-slate-300 border-b border-slate-700 font-semibold">
          📄 {filePath}
        </div>
      )}
      
      {/* Old Content (Removed) */}
      {oldLines.length > 0 && oldContent.trim() && (
        <div className="bg-red-900/20 border-l-4 border-red-500">
          <div className="px-4 py-1 bg-red-900/30 text-red-300 text-xs font-semibold border-b border-red-500/30">
            − Removed
          </div>
          {oldLines.map((line, i) => (
            <div key={`old-${i}`} className="flex hover:bg-red-900/30">
              <span className="px-3 py-0.5 text-red-400 select-none w-12 text-right flex-shrink-0 bg-red-900/10">
                {i + 1}
              </span>
              <span className="px-3 py-0.5 text-red-100 flex-1 whitespace-pre">
                {line || ' '}
              </span>
            </div>
          ))}
        </div>
      )}
      
      {/* New Content (Added) */}
      {newLines.length > 0 && (
        <div className="bg-green-900/20 border-l-4 border-green-500">
          <div className="px-4 py-1 bg-green-900/30 text-green-300 text-xs font-semibold border-b border-green-500/30">
            + Added
          </div>
          {newLines.map((line, i) => (
            <div key={`new-${i}`} className="flex hover:bg-green-900/30">
              <span className="px-3 py-0.5 text-green-400 select-none w-12 text-right flex-shrink-0 bg-green-900/10">
                {i + 1}
              </span>
              <span className="px-3 py-0.5 text-green-100 flex-1 whitespace-pre">
                {line || ' '}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

