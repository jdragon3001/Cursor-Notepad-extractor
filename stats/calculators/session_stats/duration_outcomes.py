"""Session duration and outcomes statistics (Stats 71-76)."""

from typing import Dict, Any, List
from stats.models.session import Session
from stats.models.message import Message
from .base import SessionStatsBase


class SessionDurationOutcomesStats(SessionStatsBase):
    """Calculate session duration and outcome statistics."""
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all duration and outcome stats."""
        return {
            'session_duration': self.stat_071_session_duration(),
            'sessions_by_duration_bucket': self.stat_072_sessions_by_duration_bucket(),
            'lines_added': self.stat_073_lines_added(),
            'lines_removed': self.stat_074_lines_removed(),
            'net_lines': self.stat_075_net_lines(),
            'sessions_with_code_output': self.stat_076_sessions_with_code_output(),
        }
    
    def stat_071_session_duration(self) -> Dict[str, Any]:
        """Stat #71: Session duration."""
        durations = [s.duration_minutes for s in self.sessions]
        
        return self.create_stat_result(
            value=self.average(durations),
            label='Session duration (minutes)',
            category='Sessions',
            data_source='composerData',
            stat_type='numeric',
            median=self.median(durations),
            min=self.min_val(durations),
            max=self.max_val(durations),
            p95=self.percentile(durations, 95),
            std_dev=self.std_dev(durations),
            distribution=self.distribution(durations, bins=20),
            sample_size=len(durations)
        )
    
    def stat_072_sessions_by_duration_bucket(self) -> Dict[str, Any]:
        """Stat #72: Sessions by duration bucket."""
        buckets = {
            'very_short': 0,   # < 5 min
            'short': 0,         # 5-15 min
            'medium': 0,        # 15-60 min
            'long': 0,          # 1-4 hours
            'very_long': 0      # > 4 hours
        }
        
        for s in self.sessions:
            duration_min = s.duration_minutes
            if duration_min < 5:
                buckets['very_short'] += 1
            elif duration_min < 15:
                buckets['short'] += 1
            elif duration_min < 60:
                buckets['medium'] += 1
            elif duration_min < 240:
                buckets['long'] += 1
            else:
                buckets['very_long'] += 1
        
        return self.create_stat_result(
            value=len(self.sessions),
            label='Sessions by duration bucket',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            buckets=buckets
        )
    
    def stat_073_lines_added(self) -> Dict[str, Any]:
        """Stat #73: Lines added."""
        lines_per_session = [s.total_lines_added for s in self.sessions if s.total_lines_added > 0]
        total_lines = sum(s.total_lines_added for s in self.sessions)
        
        return self.create_stat_result(
            value=total_lines,
            label='Total lines added',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            average_per_session=self.average(lines_per_session) if lines_per_session else 0,
            median=self.median(lines_per_session) if lines_per_session else 0,
            sessions_with_additions=len(lines_per_session)
        )
    
    def stat_074_lines_removed(self) -> Dict[str, Any]:
        """Stat #74: Lines removed."""
        lines_per_session = [s.total_lines_removed for s in self.sessions if s.total_lines_removed > 0]
        total_lines = sum(s.total_lines_removed for s in self.sessions)
        
        return self.create_stat_result(
            value=total_lines,
            label='Total lines removed',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            average_per_session=self.average(lines_per_session) if lines_per_session else 0,
            median=self.median(lines_per_session) if lines_per_session else 0,
            sessions_with_removals=len(lines_per_session)
        )
    
    def stat_075_net_lines(self) -> Dict[str, Any]:
        """Stat #75: Net lines (added - removed)."""
        net_per_session = [s.net_lines_changed for s in self.sessions]
        total_net = sum(net_per_session)
        
        return self.create_stat_result(
            value=total_net,
            label='Net lines (added - removed)',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            average_per_session=self.average(net_per_session),
            median=self.median(net_per_session),
            positive_sessions=len([s for s in self.sessions if s.net_lines_changed > 0]),
            negative_sessions=len([s for s in self.sessions if s.net_lines_changed < 0])
        )
    
    def stat_076_sessions_with_code_output(self) -> Dict[str, Any]:
        """Stat #76: Sessions with code output."""
        with_code = self.filter_by(self.sessions, lambda s: s.has_code_changes)
        total = len(self.sessions)
        
        return self.create_stat_result(
            value=len(with_code),
            label='Sessions with code output',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            percentage=self.percentage(len(with_code), total)
        )

