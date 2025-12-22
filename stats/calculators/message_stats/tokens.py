"""Message token usage statistics (Stats 45-49)."""

from typing import Dict, Any, List
from stats.models.message import Message
from .base import MessageStatsBase


class MessageTokensStats(MessageStatsBase):
    """Calculate token usage statistics."""
    
    def __init__(self, messages: List[Message]):
        """Initialize with messages."""
        super().__init__(messages)
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all token stats."""
        return {
            'input_tokens': self.stat_045_input_tokens(),
            'output_tokens': self.stat_046_output_tokens(),
            'total_tokens': self.stat_047_total_tokens(),
            'tokens_per_message': self.stat_048_tokens_per_message(),
            'tokens_by_model': self.stat_049_tokens_by_model(),
        }
    
    def stat_045_input_tokens(self) -> Dict[str, Any]:
        """Stat #45: Input tokens."""
        input_tokens = [m.get_input_tokens() for m in self.messages if m.get_input_tokens() > 0]
        total_input = sum(input_tokens)
        
        if not input_tokens:
            return self.create_stat_result(
                value=0,
                label='Total input tokens',
                category='Messages',
                data_source='bubbleId',
                stat_type='count',
                note='No token data available',
                sample_size=0
            )
        
        return self.create_stat_result(
            value=total_input,
            label='Total input tokens',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            average_per_message=self.average(input_tokens),
            median=self.median(input_tokens),
            min=self.min_val(input_tokens),
            max=self.max_val(input_tokens),
            p95=self.percentile(input_tokens, 95),
            messages_with_tokens=len(input_tokens),
            coverage=self.percentage(len(input_tokens), len(self.messages))
        )
    
    def stat_046_output_tokens(self) -> Dict[str, Any]:
        """Stat #46: Output tokens."""
        output_tokens = [m.get_output_tokens() for m in self.messages if m.get_output_tokens() > 0]
        total_output = sum(output_tokens)
        
        if not output_tokens:
            return self.create_stat_result(
                value=0,
                label='Total output tokens',
                category='Messages',
                data_source='bubbleId',
                stat_type='count',
                note='No token data available',
                sample_size=0
            )
        
        return self.create_stat_result(
            value=total_output,
            label='Total output tokens',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            average_per_message=self.average(output_tokens),
            median=self.median(output_tokens),
            min=self.min_val(output_tokens),
            max=self.max_val(output_tokens),
            p95=self.percentile(output_tokens, 95),
            messages_with_tokens=len(output_tokens),
            coverage=self.percentage(len(output_tokens), len(self.messages))
        )
    
    def stat_047_total_tokens(self) -> Dict[str, Any]:
        """Stat #47: Total tokens (input + output)."""
        total_tokens = [m.get_total_tokens() for m in self.messages if m.get_total_tokens() > 0]
        grand_total = sum(total_tokens)
        
        if not total_tokens:
            return self.create_stat_result(
                value=0,
                label='Total tokens (input + output)',
                category='Messages',
                data_source='bubbleId',
                stat_type='count',
                note='No token data available',
                sample_size=0
            )
        
        return self.create_stat_result(
            value=grand_total,
            label='Total tokens (input + output)',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            average_per_message=self.average(total_tokens),
            median=self.median(total_tokens),
            min=self.min_val(total_tokens),
            max=self.max_val(total_tokens),
            p95=self.percentile(total_tokens, 95),
            messages_with_tokens=len(total_tokens),
            coverage=self.percentage(len(total_tokens), len(self.messages))
        )
    
    def stat_048_tokens_per_message(self) -> Dict[str, Any]:
        """Stat #48: Tokens per message."""
        tokens = [m.get_total_tokens() for m in self.messages if m.get_total_tokens() > 0]
        
        if not tokens:
            return self.create_stat_result(
                value=0,
                label='Tokens per message (average)',
                category='Messages',
                data_source='bubbleId',
                stat_type='numeric',
                note='No token data available',
                sample_size=0
            )
        
        return self.create_stat_result(
            value=self.average(tokens),
            label='Tokens per message (average)',
            category='Messages',
            data_source='bubbleId',
            stat_type='numeric',
            median=self.median(tokens),
            min=self.min_val(tokens),
            max=self.max_val(tokens),
            p95=self.percentile(tokens, 95),
            std_dev=self.std_dev(tokens),
            distribution=self.distribution(tokens, bins=20),
            sample_size=len(tokens)
        )
    
    def stat_049_tokens_by_model(self) -> Dict[str, Any]:
        """Stat #49: Tokens by model."""
        model_tokens = {}
        
        for m in self.messages:
            model = m.get_model_name()
            if model:
                tokens = m.get_total_tokens()
                if tokens > 0:
                    if model not in model_tokens:
                        model_tokens[model] = 0
                    model_tokens[model] += tokens
        
        # Sort by token count
        sorted_models = sorted(model_tokens.items(), key=lambda x: x[1], reverse=True)
        
        return self.create_stat_result(
            value=len(model_tokens),
            label='Models with token data',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            token_breakdown=sorted_models[:20],  # Top 20 models
            total_tokens=sum(model_tokens.values())
        )

