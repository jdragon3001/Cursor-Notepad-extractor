#!/usr/bin/env python3
"""
Note parser module for Cursor Notepad Extractor.

This module provides functionality to parse notepad content
and split it into individual notes based on headers and separators.
"""

import re
from typing import List, Dict, Any

class NoteParser:
    """Parser for splitting notepad content into individual notes."""
    
    @staticmethod
    def parse_notes(note_content: str) -> List[Dict[str, Any]]:
        """
        Parse a single note content string into multiple individual notes.
        
        Args:
            note_content: String containing potentially multiple notes.
            
        Returns:
            List of dictionaries containing individual notes with title and content.
        """
        if not note_content or not note_content.strip():
            # Return a dummy note for completely empty content
            return [{
                'title': "Empty Note",
                'content': "[Empty note content]"
            }]
        
        # Handle JSON-like content specially
        if note_content.strip().startswith('{') and note_content.strip().endswith('}'):
            try:
                # Try to extract meaningful information from JSON
                import json
                data = json.loads(note_content)
                
                # Handle typical Cursor notepad JSON format
                if 'notepads' in data and isinstance(data['notepads'], dict):
                    # Extract notes from notepads structure
                    notes = []
                    for note_id, note_data in data['notepads'].items():
                        if isinstance(note_data, dict):
                            title = note_data.get('name', 'Untitled Note')
                            content = note_data.get('text', '')
                            notes.append({
                                'title': title or 'Untitled Note',
                                'content': content or '[No content]'
                            })
                    if notes:
                        return notes
            except:
                # If JSON parsing fails, continue with normal parsing
                pass
        
        # Split content into lines for processing
        lines = note_content.split('\n')
        
        # Prepare result list
        individual_notes = []
        
        # Track current note being built
        current_title = ""
        current_content = []
        in_note = False
        
        # Process each line
        for line in lines:
            # Check for section headers (titles)
            if line.strip().startswith('# '):
                # If we were already processing a note, save it
                if in_note and (current_title or current_content):
                    individual_notes.append({
                        'title': current_title or "Untitled Note",
                        'content': '\n'.join(current_content).strip() or "[No content]"
                    })
                
                # Start a new note
                current_title = line.strip()[2:].strip()  # Remove '# ' prefix
                current_content = []
                in_note = True
                
            # Check for separator between notes
            elif line.strip() == '---':
                # If we were processing a note, save it
                if in_note and (current_title or current_content):
                    individual_notes.append({
                        'title': current_title or "Untitled Note",
                        'content': '\n'.join(current_content).strip() or "[No content]"
                    })
                
                # Reset for next note
                current_title = ""
                current_content = []
                in_note = False
                
            # Regular content line
            elif in_note:
                current_content.append(line)
            # Content before any header - treat as a note without title
            elif not in_note and line.strip() and not individual_notes:
                current_title = ""
                current_content = [line]
                in_note = True
        
        # Don't forget to add the last note if we were processing one
        if in_note and (current_title or current_content):
            individual_notes.append({
                'title': current_title or "Untitled Note",
                'content': '\n'.join(current_content).strip() or "[No content]"
            })
        
        # If we didn't find any structured notes, treat the whole content as one note
        if not individual_notes and note_content.strip():
            # Try to generate a title from the first line
            lines = note_content.strip().split('\n')
            title = ""
            content = note_content.strip()
            
            if lines and lines[0].strip():
                title = lines[0].strip()
                # If first line is long, truncate it
                if len(title) > 40:
                    title = title[:37] + "..."
                # Use as title and remove from content if it's a significant portion
                if len(title) > 5 and lines[1:]:
                    content = '\n'.join(lines[1:]).strip()
            
            individual_notes.append({
                'title': title or "Untitled Note",
                'content': content or "[No content]"
            })
        
        # Ensure we return at least one note
        if not individual_notes:
            individual_notes.append({
                'title': "Unformatted Note",
                'content': note_content.strip() or "[No content]"
            })
        
        return individual_notes 