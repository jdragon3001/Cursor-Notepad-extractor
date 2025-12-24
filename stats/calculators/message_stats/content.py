"""Message content statistics (Stats 5-11)."""

from typing import Dict, Any, List
from stats.models.message import Message
from .base import MessageStatsBase


class MessageContentStats(MessageStatsBase):
    """Calculate message content statistics."""
    
    def __init__(self, messages: List[Message]):
        """Initialize with messages."""
        super().__init__(messages)
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all content stats."""
        return {
            'message_text_length': self.stat_005_message_text_length(),
            'messages_with_text': self.stat_006_messages_with_text(),
            'messages_with_code_blocks': self.stat_007_messages_with_code_blocks(),
            'code_blocks_generated': self.stat_008_code_blocks_generated(),
            'lines_of_code_in_blocks': self.stat_009_lines_of_code_in_blocks(),
            'code_block_languages': self.stat_010_code_block_languages(),
            'files_referenced_in_code': self.stat_011_files_referenced_in_code(),
        }
    
    def stat_005_message_text_length(self) -> Dict[str, Any]:
        """Stat #5: Message text length."""
        lengths = [m.get_text_length() for m in self.messages if m.has_text]
        
        return self.create_stat_result(
            value=self.average(lengths),
            label='Message text length (characters)',
            category='Messages',
            data_source='bubbleId',
            stat_type='numeric',
            median=self.median(lengths),
            min=self.min_val(lengths),
            max=self.max_val(lengths),
            p95=self.percentile(lengths, 95),
            std_dev=self.std_dev(lengths),
            distribution=self.distribution(lengths, bins=20),
            sample_size=len(lengths)
        )
    
    def stat_006_messages_with_text(self) -> Dict[str, Any]:
        """Stat #6: Messages with text."""
        with_text = self.filter_by(self.messages, lambda m: m.has_text)
        total = len(self.messages)
        
        return self.create_stat_result(
            value=len(with_text),
            label='Messages with text',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(len(with_text), total),
            breakdown={
                'with_text': len(with_text),
                'without_text': total - len(with_text)
            }
        )
    
    def stat_007_messages_with_code_blocks(self) -> Dict[str, Any]:
        """Stat #7: Messages with code blocks."""
        with_code = self.filter_by(self.messages, lambda m: m.has_code)
        total = len(self.messages)
        
        return self.create_stat_result(
            value=len(with_code),
            label='Messages with code blocks',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(len(with_code), total),
            breakdown={
                'with_code': len(with_code),
                'without_code': total - len(with_code)
            }
        )
    
    def stat_008_code_blocks_generated(self) -> Dict[str, Any]:
        """Stat #8: Code blocks generated."""
        total_blocks = sum(m.get_code_block_count() for m in self.messages)
        
        return self.create_stat_result(
            value=total_blocks,
            label='Code blocks generated',
            category='Messages',
            data_source='bubbleId',
            stat_type='count'
        )
    
    def stat_009_lines_of_code_in_blocks(self) -> Dict[str, Any]:
        """Stat #9: Lines of code in code blocks."""
        total_lines = sum(m.get_code_line_count() for m in self.messages)
        
        return self.create_stat_result(
            value=total_lines,
            label='Lines of code in code blocks',
            category='Messages',
            data_source='bubbleId',
            stat_type='count'
        )
    
    def stat_010_code_block_languages(self) -> Dict[str, Any]:
        """Stat #10: Code block languages."""
        languages = []
        for msg in self.messages:
            for block in msg.code_blocks + msg.suggested_code_blocks:
                lang = block.get('languageId') or block.get('language') or block.get('lang')
                if lang:
                    languages.append(lang)
        
        top_languages = self.most_common(languages, n=20)
        
        return self.create_stat_result(
            value=len(set(languages)),
            label='Unique code block languages',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            top_languages=top_languages,
            total_blocks=len(languages)
        )
    
    def stat_011_files_referenced_in_code(self) -> Dict[str, Any]:
        """Stat #11: Files referenced in code blocks."""
        files = []
        for msg in self.messages:
            for block in msg.code_blocks + msg.suggested_code_blocks:
                file_path = block.get('filePath') or block.get('file') or block.get('uri')
                # If uri is a dict, extract path
                if isinstance(file_path, dict):
                    file_path = file_path.get('path') or file_path.get('_fsPath')
                if file_path:
                    files.append(file_path)
        
        unique_files = len(set(files))
        top_files = self.most_common(files, n=20)
        
        return self.create_stat_result(
            value=unique_files,
            label='Unique files referenced in code',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            top_files=top_files,
            total_references=len(files)
        )

