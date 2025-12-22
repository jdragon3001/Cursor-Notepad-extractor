"""Message model information statistics (Stats 42-44)."""

from typing import Dict, Any, List
from stats.models.message import Message
from .base import MessageStatsBase


class MessageModelsStats(MessageStatsBase):
    """Calculate model information statistics."""
    
    def __init__(self, messages: List[Message]):
        """Initialize with messages."""
        super().__init__(messages)
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all model stats."""
        return {
            'messages_with_model_info': self.stat_042_messages_with_model_info(),
            'model_usage_breakdown': self.stat_043_model_usage_breakdown(),
            'model_switches': self.stat_044_model_switches(),
        }
    
    def stat_042_messages_with_model_info(self) -> Dict[str, Any]:
        """Stat #42: Messages with model info."""
        with_model_info = self.filter_by(self.messages, lambda m: m.has_model_info)
        total = len(self.messages)
        
        return self.create_stat_result(
            value=len(with_model_info),
            label='Messages with model info',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(len(with_model_info), total),
            breakdown={
                'with_model_info': len(with_model_info),
                'without_model_info': total - len(with_model_info)
            }
        )
    
    def stat_043_model_usage_breakdown(self) -> Dict[str, Any]:
        """Stat #43: Model usage breakdown."""
        models = []
        for m in self.messages:
            model_name = m.get_model_name()
            if model_name:
                models.append(model_name)
        
        model_counts = self.most_common(models, n=20) if models else []
        unique_models = len(set(models))
        
        return self.create_stat_result(
            value=unique_models,
            label='Unique models used',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            model_breakdown=model_counts,
            total_messages_with_model=len(models),
            coverage_percentage=self.percentage(len(models), len(self.messages))
        )
    
    def stat_044_model_switches(self) -> Dict[str, Any]:
        """Stat #44: Model switches within sessions."""
        # Group messages by session
        sessions = self.group_by(self.messages, lambda m: m.composer_id)
        
        total_switches = 0
        sessions_with_switches = 0
        
        for session_id, msgs in sessions.items():
            # Sort by timestamp
            sorted_msgs = sorted(msgs, key=lambda m: m.created_at)
            
            # Track model changes
            prev_model = None
            switches_in_session = 0
            
            for msg in sorted_msgs:
                model = msg.get_model_name()
                if model:
                    if prev_model and model != prev_model:
                        switches_in_session += 1
                    prev_model = model
            
            if switches_in_session > 0:
                sessions_with_switches += 1
                total_switches += switches_in_session
        
        return self.create_stat_result(
            value=total_switches,
            label='Model switches',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            sessions_with_switches=sessions_with_switches,
            sessions_analyzed=len(sessions),
            percentage_sessions=self.percentage(sessions_with_switches, len(sessions))
        )

