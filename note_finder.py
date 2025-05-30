#!/usr/bin/env python3
"""
Note finder module for Cursor Notepad Extractor.

This module provides functionality to search through Cursor workspace databases
and find notepad-related content and reactive storage data.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import re
from collections import defaultdict

from database.cursor_db import CursorDatabase, DataDecoder
from utils.config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NoteFinder:
    """
    Finds notepad and reactive storage data in Cursor workspace databases.
    """
    
    def __init__(self, workspace_path: Optional[str] = None):
        """
        Initialize the NoteFinder.
        
        Args:
            workspace_path: Optional workspace path. If None, uses default from Config.
        """
        self.workspace_path = workspace_path or Config.get_workspace_path()
        self.findings: List[Dict[str, Any]] = []
        
        # Search patterns for notepad-related keys
        self.search_patterns = [
            '%notepad%',
            '%reactive%',
            '%note%',
            '%draft%',
            '%text%',
            '%storage%'
        ]
        
        # Specific key patterns we're looking for
        self.specific_keys = [
            'notepadData',
            'notepad.reactiveStorageId',
            'reactiveStorageId',
            'notepad',
            'notes',
            'drafts'
        ]
    
    def find_notes(self) -> List[Dict[str, Any]]:
        """
        Search through all databases and find notepad-related content.
        
        Returns:
            List of dictionaries containing finding information.
        """
        logger.info("Starting note search...")
        self.findings = []
        
        # Get all database files
        database_files = Config.get_database_files(self.workspace_path)
        
        if not database_files:
            logger.warning(f"No database files found in {self.workspace_path}")
            return self.findings
        
        logger.info(f"Found {len(database_files)} databases to scan")
        
        # Search each database
        databases_scanned = 0
        for db_file in database_files:
            try:
                logger.info(f"Scanning database: {db_file}")
                self._scan_database(db_file)
                databases_scanned += 1
            except Exception as e:
                logger.error(f"Error scanning database {db_file}: {e}")
                continue
        
        # Deduplicate findings - remove reactiveStorageId when notepadData exists for the same database
        self._deduplicate_findings()
        
        logger.info(f"Scan complete. Found {len(self.findings)} findings in {databases_scanned} databases")
        return self.findings
    
    def _scan_database(self, db_file: Path):
        """
        Scan a single database for notepad content.
        
        Args:
            db_file: Path to the database file.
        """
        try:
            with CursorDatabase(db_file) as db:
                # Get all tables
                tables = db.get_tables()
                
                for table in tables:
                    logger.debug(f"Scanning table: {table}")
                    self._scan_table(db, db_file, table)
                    
        except Exception as e:
            logger.error(f"Error scanning database {db_file}: {e}")
            raise
    
    def _scan_table(self, db: CursorDatabase, db_file: Path, table: str):
        """
        Scan a single table for notepad content.
        
        Args:
            db: Database connection.
            db_file: Path to the database file.
            table: Table name to scan.
        """
        try:
            # First, look for specific keys we know about
            for key in self.specific_keys:
                value = db.get_value_by_key(key, table)
                if value:
                    self._process_finding(db_file, table, key, value)
            
            # Then search using patterns
            for pattern in self.search_patterns:
                matching_keys = db.search_keys(pattern, table)
                
                for key in matching_keys:
                    # Skip if we already found this key
                    if any(finding['key'] == key and finding['table'] == table 
                          for finding in self.findings):
                        continue
                    
                    value = db.get_value_by_key(key, table)
                    if value:
                        self._process_finding(db_file, table, key, value)
                        
        except Exception as e:
            logger.error(f"Error scanning table {table}: {e}")
    
    def _process_finding(self, db_file: Path, table: str, key: str, value: bytes):
        """
        Process a found key-value pair and add to findings if relevant.
        
        Args:
            db_file: Path to the database file.
            table: Table name.
            key: Key that was found.
            value: Value data (bytes).
        """
        try:
            # Analyze the data
            analysis = DataDecoder.analyze_data(value)
            
            # Skip if data is too small (likely not notepad content)
            if analysis['size'] < 10:
                return
            
            # Try to decode content - get FULL content, not previews
            content = ""
            
            # JSON extraction is primary for notepad data
            if analysis['is_json']:
                # Extract text content from JSON (optimized for notepad structure)
                content = self._extract_text_from_json(analysis['json_data'])
                
                # If JSON extraction didn't work well or returned nothing substantial, try as raw text
                if not content or len(content.strip()) < 10:
                    raw_text = DataDecoder.try_decode_as_text(value)
                    if raw_text and len(raw_text.strip()) > len(content.strip()):
                        # Only use raw text if it's more substantial than the JSON extraction
                        content = raw_text
            
            # If not JSON or JSON extraction failed, try as plain text
            elif analysis['is_text']:
                # Get the full text, not just preview
                full_text = DataDecoder.try_decode_as_text(value)
                if full_text:
                    content = full_text
            else:
                # Last resort: try basic text decoding for non-text data
                decoded = DataDecoder.try_decode_as_text(value)
                if decoded:
                    content = decoded
            
            # Only include if we have meaningful content
            if content and len(content.strip()) > 5:
                # Check if this is likely to be a notepad by the key name
                is_notepad = False
                if 'notepad' in key.lower():
                    is_notepad = True
                elif 'note' in key.lower() and len(content.strip()) > 10:
                    is_notepad = True
                
                # Extract database ID from file path
                db_id = db_file.parent.name
                
                # For likely notepad entries, prepare better formatting
                if is_notepad:
                    # Clean up content to remove excessive JSON formatting
                    content = self._clean_up_content(content)
                
                finding = {
                    'database': db_id,
                    'table': table,
                    'key': key,
                    'size': analysis['size'],
                    'content': content.strip(),
                    'is_notepad': is_notepad
                }
                
                self.findings.append(finding)
                logger.info(f"Found {'notepad' if is_notepad else 'general'} content: {key} ({analysis['size']} bytes)")
                
        except Exception as e:
            logger.error(f"Error processing finding {key}: {e}")
    
    def _extract_text_from_json(self, json_data: Any) -> str:
        """
        Extract text content from JSON data, focusing specifically on notepad content.
        
        Args:
            json_data: Parsed JSON data.
            
        Returns:
            Extracted text content.
        """
        if not json_data:
            return ""
        
        try:
            # SPECIFIC NOTEPAD DATA EXTRACTION
            # Most notepad data follows this pattern: {"notepads": {"id": {"text": "actual content"}}}
            if isinstance(json_data, dict):
                # Case 1: Direct notepad structure with 'notepads' key
                if 'notepads' in json_data and isinstance(json_data['notepads'], dict):
                    extracted_notes = []
                    
                    # Iterate through each notepad entry
                    for notepad_id, notepad_data in json_data['notepads'].items():
                        if isinstance(notepad_data, dict):
                            note_content = ""
                            
                            # Get the notepad name if available
                            if 'name' in notepad_data and notepad_data['name']:
                                note_content += f"# {notepad_data['name']}\n\n"
                            
                            # Get the actual notepad text content
                            if 'text' in notepad_data and notepad_data['text']:
                                note_content += notepad_data['text']
                            
                            if note_content:
                                extracted_notes.append(note_content)
                    
                    # Return all extracted notepad contents
                    if extracted_notes:
                        return "\n\n---\n\n".join(extracted_notes)
                
                # Case 2: Single notepad entry with direct 'text' field
                elif 'text' in json_data and isinstance(json_data['text'], str):
                    note_content = ""
                    
                    # Get the notepad name if available
                    if 'name' in json_data and json_data['name']:
                        note_content += f"# {json_data['name']}\n\n"
                    
                    # Add the text content
                    note_content += json_data['text']
                    return note_content
                
                # Case 3: Look for specific text fields at root level
                for field in ['content', 'text', 'note', 'data']:
                    if field in json_data and isinstance(json_data[field], str):
                        return json_data[field]
                
                # Case 4: Search recursively for notepad structures
                for key, value in json_data.items():
                    if isinstance(value, dict):
                        # Skip metadata fields
                        if key in ['selectedCommits', 'selectedPullRequests', 'selectedImages', 
                                  'folderSelections', 'fileSelections', 'terminalSelections', 
                                  'useLinterErrors', 'useRules', 'composers', 'quotes']:
                            continue
                        
                        # Recursively check this dictionary
                        nested_result = self._extract_text_from_json(value)
                        if nested_result:
                            return nested_result
                    
                    elif isinstance(value, list) and len(value) > 0:
                        # Check list items for dictionaries that might contain notepad data
                        for item in value:
                            if isinstance(item, dict):
                                nested_result = self._extract_text_from_json(item)
                                if nested_result:
                                    return nested_result
            
            # If we got here, no specific notepad structure was found
            # Fall back to standard text extraction for simpler cases
            if isinstance(json_data, dict):
                for key, value in json_data.items():
                    if key == 'text' and isinstance(value, str):
                        return value
            
            # Last resort: convert the entire JSON to string if it's small enough
            # This is a fallback for unusual formats
            if len(str(json_data)) < 1000:  # Only do this for reasonably small JSON
                json_str = json.dumps(json_data, indent=2)
                return json_str
                
        except Exception as e:
            logger.error(f"Error extracting text from JSON: {e}")
        
        return ""
    
    def _clean_up_content(self, content: str) -> str:
        """
        Clean up content for better display, especially for notepad entries.
        
        Args:
            content: Raw content string.
            
        Returns:
            Cleaned up content.
        """
        # Remove excessive JSON formatting if content looks like raw JSON
        if content.strip().startswith('{') and content.strip().endswith('}'):
            try:
                # Try to parse as JSON and then format better
                data = json.loads(content)
                if isinstance(data, dict) and len(data) > 0:
                    # Try to extract just the text if it's a simple structure
                    if 'text' in data and isinstance(data['text'], str):
                        return data['text']
            except:
                pass  # Not valid JSON, keep original
        
        # Replace consecutive blank lines with just one
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # Replace excessive technical content (which often shows up in notepad data)
        patterns_to_remove = [
            r'{"selectedCommits":\[\].*?"selectedPullRequests":\[\]}',
            r'"selectedImages":\[\].*?"folderSelections":\[\]}',
            r'"terminalSelections":\[\].*?"externalLinks":\[\]}'
        ]
        
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content)
        
        return content.strip()
    
    def save_findings(self, output_file: str = "cursor_notes_found.txt") -> bool:
        """
        Save findings to a text file.
        
        Args:
            output_file: Path to output file.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # Write header
                f.write("Cursor Notes Search Results\n")
                f.write(f"Search completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                # Count unique databases and notepad entries
                unique_dbs = len(set(finding['database'] for finding in self.findings))
                notepad_entries = sum(1 for finding in self.findings if finding.get('is_notepad', False))
                notepad_data_entries = sum(1 for finding in self.findings if finding['key'] == 'notepadData')
                
                f.write(f"Databases scanned: {unique_dbs}\n")
                f.write(f"Total findings: {len(self.findings)}\n")
                f.write(f"Notepad entries: {notepad_entries}\n")
                f.write(f"NotepadData entries: {notepad_data_entries}\n")
                f.write("Note: Duplicate reactiveStorageId entries have been filtered out\n")
                f.write("=" * 80 + "\n\n")
                
                # Write findings - notepad entries first, then sort by database
                findings_sorted = sorted(
                    self.findings, 
                    key=lambda x: (not x.get('is_notepad', False), x['database'], x['key'])
                )
                
                for i, finding in enumerate(findings_sorted, 1):
                    is_notepad = finding.get('is_notepad', False)
                    key_type = "NOTEPAD" if finding['key'] == 'notepadData' else finding['key']
                    
                    f.write(f"FINDING #{i} ({key_type})\n")
                    f.write(f"Database: {finding['database']}\n")
                    f.write(f"Table: {finding['table']}\n")
                    f.write(f"Key: {finding['key']}\n")
                    f.write(f"Size: {finding['size']} bytes\n")
                    f.write("-" * 50 + "\n")
                    
                    # For notepad entries, ensure the content is well-formatted
                    content = finding['content']
                    if is_notepad:
                        # One last cleaning step to ensure it's readable
                        content = self._clean_up_content(content)
                    
                    f.write(content)
                    f.write("\n" + "=" * 80 + "\n\n")
            
            logger.info(f"Findings saved to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving findings to {output_file}: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the findings.
        
        Returns:
            Dictionary with statistics.
        """
        if not self.findings:
            return {
                'total_findings': 0,
                'databases_with_findings': 0,
                'tables_with_findings': 0,
                'average_content_size': 0,
                'largest_finding_size': 0
            }
        
        databases = set(finding['database'] for finding in self.findings)
        tables = set(f"{finding['database']}.{finding['table']}" for finding in self.findings)
        sizes = [finding['size'] for finding in self.findings]
        
        return {
            'total_findings': len(self.findings),
            'databases_with_findings': len(databases),
            'tables_with_findings': len(tables),
            'average_content_size': sum(sizes) // len(sizes) if sizes else 0,
            'largest_finding_size': max(sizes) if sizes else 0,
            'key_patterns_found': list(set(finding['key'] for finding in self.findings))
        }
    
    def _deduplicate_findings(self):
        """
        Deduplicate findings by removing reactiveStorageId entries when notepadData exists.
        This ensures we only show one version of each note in the UI.
        """
        # Group findings by database
        db_groups = defaultdict(list)
        for finding in self.findings:
            db_groups[finding['database']].append(finding)
        
        # Create a new filtered list of findings
        filtered_findings = []
        
        # Process each database group
        for db, entries in db_groups.items():
            # Find all notepadData entries
            notepad_data_entries = [e for e in entries if e['key'] == 'notepadData']
            
            # If we have notepadData entries, only keep those (skip reactiveStorageId)
            if notepad_data_entries:
                filtered_findings.extend(notepad_data_entries)
            else:
                # If no notepadData entries, keep all entries
                filtered_findings.extend(entries)
        
        # Update findings list
        initial_count = len(self.findings)
        self.findings = filtered_findings
        skipped_count = initial_count - len(self.findings)
        
        if skipped_count > 0:
            logger.info(f"Deduplicated {skipped_count} reactive storage entries")
        
        # Update is_notepad flag for remaining entries
        for finding in self.findings:
            finding['is_notepad'] = finding['key'] == 'notepadData' or 'notepad' in finding['key'].lower() 