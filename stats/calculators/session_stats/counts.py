"""Session count statistics (Stats 67-70)."""

from typing import Dict, Any, List
from stats.models.session import Session
from stats.models.message import Message
from .base import SessionStatsBase


class SessionCountStats(SessionStatsBase):
    """Calculate session count statistics."""
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all session count stats."""
        return {
            'total_sessions': self.stat_067_total_sessions(),
            'sessions_per_workspace': self.stat_068_sessions_per_workspace(),
            'agent_mode_sessions': self.stat_069_agent_mode_sessions(),
            'chat_mode_sessions': self.stat_070_chat_mode_sessions(),
        }
    
    def stat_067_total_sessions(self) -> Dict[str, Any]:
        """Stat #67: Total sessions."""
        return self.create_stat_result(
            value=self.count(self.sessions),
            label='Total sessions',
            category='Sessions',
            data_source='composerData',
            stat_type='count'
        )
    
    def stat_068_sessions_per_workspace(self) -> Dict[str, Any]:
        """Stat #68: Sessions per workspace."""
        # This would need workspace data from workspace DBs
        # For now, return placeholder based on available data
        return self.create_stat_result(
            value=len(self.sessions),
            label='Sessions per workspace',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            note='From global DB only - workspace breakdown requires workspace DB extraction'
        )
    
    def stat_069_agent_mode_sessions(self) -> Dict[str, Any]:
        """Stat #69: Agent mode sessions."""
        agentic = self.filter_by(self.sessions, lambda s: s.is_agentic)
        total = len(self.sessions)
        
        return self.create_stat_result(
            value=len(agentic),
            label='Agent mode sessions',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            percentage=self.percentage(len(agentic), total),
            breakdown={
                'agentic': len(agentic),
                'chat': total - len(agentic)
            }
        )
    
    def stat_070_chat_mode_sessions(self) -> Dict[str, Any]:
        """Stat #70: Chat mode sessions."""
        chat = self.filter_by(self.sessions, lambda s: not s.is_agentic)
        total = len(self.sessions)
        
        return self.create_stat_result(
            value=len(chat),
            label='Chat mode sessions',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            percentage=self.percentage(len(chat), total),
            breakdown={
                'chat': len(chat),
                'agentic': total - len(chat)
            }
        )

