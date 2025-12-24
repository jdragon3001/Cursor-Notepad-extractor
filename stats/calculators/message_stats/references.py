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
        """Stat #27: Web search usage (from toolFormerData)."""
        web_search_count = 0
        messages_with_search = set()
        
        for m in self.messages:
            if isinstance(m.tool_former_data, dict):
                tool_name = m.tool_former_data.get('name', '')
                if tool_name == 'web_search':
                    web_search_count += 1
                    messages_with_search.add(m.bubble_id)
        
        return self.create_stat_result(
            value=web_search_count,
            label='Web searches performed',
            category='Messages',
            data_source='toolFormerData',
            stat_type='count',
            messages_with_web_search=len(messages_with_search),
            percentage=self.percentage(len(messages_with_search), len(self.messages))
        )
    
    def stat_028_web_searches_performed(self) -> Dict[str, Any]:
        """Stat #28: Duplicate - returns same as stat_027."""
        # This is kept for backward compatibility but returns same data
        return self.stat_027_web_references()
    
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
        """Stat #30: Messages using browser tools (MCP)."""
        browser_tool_count = 0
        messages_with_browser = set()
        browser_tools_used = {}
        
        for m in self.messages:
            if isinstance(m.tool_former_data, dict):
                tool_name = m.tool_former_data.get('name', '')
                if 'browser' in tool_name.lower() or tool_name == 'web_search':
                    browser_tool_count += 1
                    messages_with_browser.add(m.bubble_id)
                    browser_tools_used[tool_name] = browser_tools_used.get(tool_name, 0) + 1
        
        top_browser_tools = sorted(browser_tools_used.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return self.create_stat_result(
            value=browser_tool_count,
            label='Browser tool invocations',
            category='Messages',
            data_source='toolFormerData',
            stat_type='count',
            messages_with_browser_tools=len(messages_with_browser),
            percentage=self.percentage(len(messages_with_browser), len(self.messages)),
            top_browser_tools=top_browser_tools
        )
