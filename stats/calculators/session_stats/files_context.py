"""Session files and context statistics (Stats 77-84)."""

from typing import Dict, Any, List
import json
from stats.models.session import Session
from stats.models.message import Message
from .base import SessionStatsBase


class SessionFilesContextStats(SessionStatsBase):
    """Calculate session files and context statistics."""
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all files and context stats."""
        return {
            'files_added': self.stat_077_files_added(),
            'files_removed': self.stat_078_files_removed(),
            'files_modified': self.stat_079_files_modified(),
            'most_modified_files': self.stat_080_most_modified_files(),
            'context_tokens_used': self.stat_081_context_tokens_used(),
            'context_token_limit': self.stat_082_context_token_limit(),
            'context_usage_percentage': self.stat_083_context_usage_percentage(),
            'sessions_near_context_limit': self.stat_084_sessions_near_context_limit(),
        }
    
    def _extract_file_path_from_tool(self, tool_data: Dict[str, Any]) -> str:
        """Extract file path from tool data."""
        if not isinstance(tool_data, dict):
            return None
        
        # Try to get file path from rawArgs
        raw_args = tool_data.get('rawArgs')
        if raw_args:
            try:
                if isinstance(raw_args, str):
                    args = json.loads(raw_args)
                else:
                    args = raw_args
                
                # Different tools use different field names
                file_path = args.get('file_path') or args.get('target_file') or args.get('filepath') or args.get('path')
                if file_path:
                    return file_path
            except:
                pass
        
        return None
    
    def stat_077_files_added(self) -> Dict[str, Any]:
        """Stat #77: Files added (from write tool)."""
        import logging
        logger = logging.getLogger(__name__)
        
        files_written = []
        unique_files = set()
        
        logger.info(f"FILES_ADDED: Checking {len(self.messages)} messages")
        
        for msg in self.messages:
            if isinstance(msg.tool_former_data, dict):
                tool_name = msg.tool_former_data.get('name', '')
                if tool_name == 'write':
                    file_path = self._extract_file_path_from_tool(msg.tool_former_data)
                    if file_path:
                        files_written.append(file_path)
                        unique_files.add(file_path)
        
        logger.info(f"FILES_ADDED: Found {len(files_written)} write operations, {len(unique_files)} unique files")
        
        top_files = self.most_common(files_written, n=20) if files_written else []
        
        return self.create_stat_result(
            value=len(files_written),
            label='Files added',
            category='Sessions',
            data_source='toolFormerData',
            stat_type='count',
            unique_files=len(unique_files),
            top_files=top_files
        )
    
    def stat_078_files_removed(self) -> Dict[str, Any]:
        """Stat #78: Files removed (from delete_file tool)."""
        files_deleted = []
        unique_files = set()
        
        for msg in self.messages:
            if isinstance(msg.tool_former_data, dict):
                tool_name = msg.tool_former_data.get('name', '')
                if tool_name == 'delete_file':
                    file_path = self._extract_file_path_from_tool(msg.tool_former_data)
                    if file_path:
                        files_deleted.append(file_path)
                        unique_files.add(file_path)
        
        top_files = self.most_common(files_deleted, n=20) if files_deleted else []
        
        return self.create_stat_result(
            value=len(files_deleted),
            label='Files removed',
            category='Sessions',
            data_source='toolFormerData',
            stat_type='count',
            unique_files=len(unique_files),
            top_files=top_files
        )
    
    def stat_079_files_modified(self) -> Dict[str, Any]:
        """Stat #79: Files modified (from edit tools)."""
        files_modified = set()
        modification_tools = ['search_replace', 'apply_patch', 'edit_file', 'edit_file_v2']
        
        for msg in self.messages:
            if isinstance(msg.tool_former_data, dict):
                tool_name = msg.tool_former_data.get('name', '')
                if tool_name in modification_tools:
                    file_path = self._extract_file_path_from_tool(msg.tool_former_data)
                    if file_path:
                        files_modified.add(file_path)
        
        return self.create_stat_result(
            value=len(files_modified),
            label='Unique files modified',
            category='Sessions',
            data_source='toolFormerData',
            stat_type='count'
        )
    
    def stat_080_most_modified_files(self) -> Dict[str, Any]:
        """Stat #80: Most modified files (all file operations)."""
        file_operations = []
        file_tools = ['write', 'delete_file', 'search_replace', 'apply_patch', 'edit_file', 'edit_file_v2']
        
        for msg in self.messages:
            if isinstance(msg.tool_former_data, dict):
                tool_name = msg.tool_former_data.get('name', '')
                if tool_name in file_tools:
                    file_path = self._extract_file_path_from_tool(msg.tool_former_data)
                    if file_path:
                        file_operations.append(file_path)
        
        top_files = self.most_common(file_operations, n=30) if file_operations else []
        
        return self.create_stat_result(
            value=len(top_files),
            label='Files with modification data',
            category='Sessions',
            data_source='toolFormerData',
            stat_type='count',
            top_modified_files=top_files,
            total_operations=len(file_operations)
        )
    
    def stat_081_context_tokens_used(self) -> Dict[str, Any]:
        """Stat #81: Context tokens used."""
        tokens = [s.context_tokens_used for s in self.sessions if s.context_tokens_used > 0]
        
        if not tokens:
            return self.create_stat_result(
                value=0,
                label='Context tokens used',
                category='Sessions',
                data_source='composerData',
                stat_type='numeric',
                sample_size=0
            )
        
        return self.create_stat_result(
            value=self.average(tokens),
            label='Average context tokens used',
            category='Sessions',
            data_source='composerData',
            stat_type='numeric',
            median=self.median(tokens),
            min=self.min_val(tokens),
            max=self.max_val(tokens),
            p95=self.percentile(tokens, 95),
            total=sum(tokens),
            sample_size=len(tokens)
        )
    
    def stat_082_context_token_limit(self) -> Dict[str, Any]:
        """Stat #82: Context token limit."""
        limits = [s.context_token_limit for s in self.sessions if s.context_token_limit > 0]
        most_common_limit = self.most_common(limits, n=1)[0] if limits else (128000, 0)
        
        return self.create_stat_result(
            value=most_common_limit[0],
            label='Most common context token limit',
            category='Sessions',
            data_source='composerData',
            stat_type='numeric',
            sessions_with_this_limit=most_common_limit[1]
        )
    
    def stat_083_context_usage_percentage(self) -> Dict[str, Any]:
        """Stat #83: Context usage percentage."""
        percentages = [s.context_usage_percent for s in self.sessions if s.context_usage_percent > 0]
        
        if not percentages:
            return self.create_stat_result(
                value=0,
                label='Context usage percentage',
                category='Sessions',
                data_source='composerData',
                stat_type='percentage',
                sample_size=0
            )
        
        return self.create_stat_result(
            value=self.average(percentages),
            label='Average context usage (%)',
            category='Sessions',
            data_source='composerData',
            stat_type='percentage',
            median=self.median(percentages),
            min=self.min_val(percentages),
            max=self.max_val(percentages),
            p95=self.percentile(percentages, 95),
            sample_size=len(percentages)
        )
    
    def stat_084_sessions_near_context_limit(self) -> Dict[str, Any]:
        """Stat #84: Sessions near context limit (>80% usage)."""
        near_limit = len([s for s in self.sessions if s.context_usage_percent >= 80])
        
        return self.create_stat_result(
            value=near_limit,
            label='Sessions near context limit (≥80%)',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            percentage=self.percentage(near_limit, len(self.sessions))
        )
