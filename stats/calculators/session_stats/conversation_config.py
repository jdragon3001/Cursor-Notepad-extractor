"""Session conversation structure and configuration statistics (Stats 85-91)."""

from typing import Dict, Any, List
from stats.models.session import Session
from stats.models.message import Message
from .base import SessionStatsBase


class SessionConversationConfigStats(SessionStatsBase):
    """Calculate conversation structure and configuration statistics."""
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all conversation and config stats."""
        return {
            'conversation_length': self.stat_085_conversation_length(),
            'user_messages_per_session': self.stat_086_user_messages_per_session(),
            'ai_messages_per_session': self.stat_087_ai_messages_per_session(),
            'user_ai_message_ratio': self.stat_088_user_ai_message_ratio(),
            'sessions_by_model': self.stat_089_sessions_by_model(),
            'sessions_with_max_mode': self.stat_090_sessions_with_max_mode(),
            'sessions_with_capabilities': self.stat_091_sessions_with_capabilities(),
        }
    
    def stat_085_conversation_length(self) -> Dict[str, Any]:
        """Stat #85: Conversation length (number of messages)."""
        # Count messages per session
        message_counts = {}
        for msg in self.messages:
            composer_id = msg.composer_id
            if composer_id not in message_counts:
                message_counts[composer_id] = 0
            message_counts[composer_id] += 1
        
        counts = list(message_counts.values())
        
        return self.create_stat_result(
            value=self.average(counts) if counts else 0,
            label='Conversation length (messages)',
            category='Sessions',
            data_source='composerData + bubbleId',
            stat_type='numeric',
            median=self.median(counts) if counts else 0,
            min=self.min_val(counts) if counts else 0,
            max=self.max_val(counts) if counts else 0,
            p95=self.percentile(counts, 95) if counts else 0,
            sample_size=len(counts)
        )
    
    def stat_086_user_messages_per_session(self) -> Dict[str, Any]:
        """Stat #86: User messages per session."""
        user_counts = {}
        for msg in self.messages:
            if msg.is_user_message:
                composer_id = msg.composer_id
                if composer_id not in user_counts:
                    user_counts[composer_id] = 0
                user_counts[composer_id] += 1
        
        counts = list(user_counts.values())
        
        return self.create_stat_result(
            value=self.average(counts) if counts else 0,
            label='User messages per session',
            category='Sessions',
            data_source='bubbleId',
            stat_type='numeric',
            median=self.median(counts) if counts else 0,
            min=self.min_val(counts) if counts else 0,
            max=self.max_val(counts) if counts else 0,
            sample_size=len(counts)
        )
    
    def stat_087_ai_messages_per_session(self) -> Dict[str, Any]:
        """Stat #87: AI messages per session."""
        ai_counts = {}
        for msg in self.messages:
            if msg.is_ai_message:
                composer_id = msg.composer_id
                if composer_id not in ai_counts:
                    ai_counts[composer_id] = 0
                ai_counts[composer_id] += 1
        
        counts = list(ai_counts.values())
        
        return self.create_stat_result(
            value=self.average(counts) if counts else 0,
            label='AI messages per session',
            category='Sessions',
            data_source='bubbleId',
            stat_type='numeric',
            median=self.median(counts) if counts else 0,
            min=self.min_val(counts) if counts else 0,
            max=self.max_val(counts) if counts else 0,
            sample_size=len(counts)
        )
    
    def stat_088_user_ai_message_ratio(self) -> Dict[str, Any]:
        """Stat #88: User/AI message ratio."""
        # Calculate ratio per session
        ratios = []
        user_counts = {}
        ai_counts = {}
        
        for msg in self.messages:
            composer_id = msg.composer_id
            if msg.is_user_message:
                user_counts[composer_id] = user_counts.get(composer_id, 0) + 1
            elif msg.is_ai_message:
                ai_counts[composer_id] = ai_counts.get(composer_id, 0) + 1
        
        for composer_id in user_counts:
            user = user_counts.get(composer_id, 0)
            ai = ai_counts.get(composer_id, 0)
            if ai > 0:
                ratios.append(user / ai)
        
        return self.create_stat_result(
            value=self.average(ratios) if ratios else 0,
            label='User/AI message ratio',
            category='Sessions',
            data_source='bubbleId',
            stat_type='numeric',
            median=self.median(ratios) if ratios else 0,
            sample_size=len(ratios)
        )
    
    def stat_089_sessions_by_model(self) -> Dict[str, Any]:
        """Stat #89: Sessions by model."""
        models = []
        for s in self.sessions:
            model = s.get_model_name()
            if model:
                models.append(model)
        
        model_counts = self.most_common(models, n=20) if models else []
        
        return self.create_stat_result(
            value=len(set(models)),
            label='Unique models used in sessions',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            model_breakdown=model_counts,
            sessions_with_model_data=len(models),
            coverage=self.percentage(len(models), len(self.sessions))
        )
    
    def stat_090_sessions_with_max_mode(self) -> Dict[str, Any]:
        """Stat #90: Sessions with max context mode."""
        # Check for max mode indicator in model_config
        with_max = 0
        for s in self.sessions:
            if s.model_config and s.model_config.get('maxContext'):
                with_max += 1
        
        return self.create_stat_result(
            value=with_max,
            label='Sessions with max context mode',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            percentage=self.percentage(with_max, len(self.sessions))
        )
    
    def stat_091_sessions_with_capabilities(self) -> Dict[str, Any]:
        """Stat #91: Sessions with capabilities."""
        capability_counts = {}
        
        for s in self.sessions:
            for cap in s.capabilities:
                # Handle both string and dict capabilities
                if isinstance(cap, str):
                    key = cap
                elif isinstance(cap, dict):
                    # Use 'type' or 'name' field from dict
                    key = cap.get('type') or cap.get('name') or str(cap)
                else:
                    key = str(cap)
                
                if key not in capability_counts:
                    capability_counts[key] = 0
                capability_counts[key] += 1
        
        sorted_caps = sorted(capability_counts.items(), key=lambda x: x[1], reverse=True)
        
        return self.create_stat_result(
            value=len(capability_counts),
            label='Unique capabilities used',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            capability_breakdown=sorted_caps,
            sessions_with_capabilities=len([s for s in self.sessions if len(s.capabilities) > 0])
        )

