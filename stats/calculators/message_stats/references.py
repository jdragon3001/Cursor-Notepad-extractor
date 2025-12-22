"""Message external references statistics (Stats 27-30)."""

from typing import Dict, Any, List
from stats.models.message import Message
from .base import MessageStatsBase


class MessageReferencesStats(MessageStatsBase):
    """Calculate external references statistics."""
    
    def __init__(self, messages: List[Message]):
        """Initialize with messages."""
        super().__init__(messages)
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all reference stats."""
        return {
            'web_references': self.stat_027_web_references(),
            'web_searches_performed': self.stat_028_web_searches_performed(),
            'docs_references': self.stat_029_docs_references(),
            'messages_using_web': self.stat_030_messages_using_web(),
        }
    
    def stat_027_web_references(self) -> Dict[str, Any]:
        """Stat #27: Web references."""
        total_refs = sum(len(m.web_references) for m in self.messages)
        messages_with_refs = len([m for m in self.messages if len(m.web_references) > 0])
        
        # Extract URLs
        urls = []
        for m in self.messages:
            for ref in m.web_references:
                if isinstance(ref, dict):
                    url = ref.get('url') or ref.get('link') or ref.get('href')
                    if url:
                        urls.append(url)
                elif isinstance(ref, str):
                    urls.append(ref)
        
        top_refs = self.most_common(urls, n=20) if urls else []
        
        return self.create_stat_result(
            value=total_refs,
            label='Web references',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            messages_with_refs=messages_with_refs,
            percentage=self.percentage(messages_with_refs, len(self.messages)),
            top_references=top_refs
        )
    
    def stat_028_web_searches_performed(self) -> Dict[str, Any]:
        """Stat #28: Web searches performed."""
        # Count messages where web search was used
        searches = 0
        for m in self.messages:
            if m.raw_data:
                # Check for web search indicators
                if m.raw_data.get('useWeb') or m.raw_data.get('webSearch'):
                    searches += 1
                elif m.raw_data.get('capabilities') and 'web' in str(m.raw_data.get('capabilities')):
                    if len(m.web_references) > 0:
                        searches += 1
        
        return self.create_stat_result(
            value=searches,
            label='Web searches performed',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(searches, len(self.messages))
        )
    
    def stat_029_docs_references(self) -> Dict[str, Any]:
        """Stat #29: Documentation references."""
        total_refs = sum(len(m.docs_references) for m in self.messages)
        messages_with_refs = len([m for m in self.messages if len(m.docs_references) > 0])
        
        # Extract doc sources
        sources = []
        for m in self.messages:
            for ref in m.docs_references:
                if isinstance(ref, dict):
                    source = ref.get('source') or ref.get('name') or ref.get('title')
                    if source:
                        sources.append(source)
        
        top_sources = self.most_common(sources, n=20) if sources else []
        
        return self.create_stat_result(
            value=total_refs,
            label='Documentation references',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            messages_with_refs=messages_with_refs,
            percentage=self.percentage(messages_with_refs, len(self.messages)),
            top_sources=top_sources
        )
    
    def stat_030_messages_using_web(self) -> Dict[str, Any]:
        """Stat #30: Messages using web (useWeb=true)."""
        using_web = 0
        for m in self.messages:
            if m.raw_data:
                if m.raw_data.get('useWeb') is True:
                    using_web += 1
                elif 'web' in m.capabilities:
                    using_web += 1
        
        return self.create_stat_result(
            value=using_web,
            label='Messages using web capability',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(using_web, len(self.messages))
        )

