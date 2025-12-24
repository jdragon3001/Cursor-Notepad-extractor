"""Session naming statistics (Stats 92-93)."""

from typing import Dict, Any, List
from stats.models.session import Session
from stats.models.message import Message
from .base import SessionStatsBase


class SessionNamingStats(SessionStatsBase):
    """Calculate session naming statistics."""
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all session naming stats."""
        return {
            'named_sessions': self.stat_092_named_sessions(),
            'session_name_keywords': self.stat_093_session_name_keywords(),
        }
    
    def stat_092_named_sessions(self) -> Dict[str, Any]:
        """Stat #92: Named sessions."""
        named = self.filter_by(self.sessions, lambda s: s.has_name)
        total = len(self.sessions)
        
        return self.create_stat_result(
            value=len(named),
            label='Named sessions',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            percentage=self.percentage(len(named), total),
            breakdown={
                'named': len(named),
                'unnamed': total - len(named)
            }
        )
    
    def stat_093_session_name_keywords(self) -> Dict[str, Any]:
        """Stat #93: Session name keywords."""
        words = []
        
        # Extract words from session names
        for s in self.sessions:
            if s.has_name and s.name:
                # Split by common separators and filter
                name_words = s.name.lower().split()
                # Filter out very short words and common words
                filtered_words = [
                    w for w in name_words 
                    if len(w) > 2 and w not in ['the', 'and', 'for', 'with', 'from']
                ]
                words.extend(filtered_words)
        
        top_keywords = self.most_common(words, n=30) if words else []
        
        return self.create_stat_result(
            value=len(set(words)),
            label='Unique keywords in session names',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            top_keywords=top_keywords,
            total_words=len(words)
        )

