#!/usr/bin/env python3
"""
Simple GUI for searching and exporting specific Cursor notes.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import re
from pathlib import Path
import os
import time
from datetime import datetime
from note_finder import NoteFinder
from note_parser import NoteParser
from utils.config import Config
import threading

# Import modules for export formats
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    import docx
    from docx.shared import Inches
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False

class NoteSearchGUI:
    """Simple GUI for searching through Cursor notes."""
    
    def __init__(self):
        """Initialize the GUI."""
        self.root = tk.Tk()
        self.root.title("Cursor Note Search & Export")
        self.root.geometry("1000x700")
        
        # Data
        self.all_notes = []
        self.filtered_notes = []
        self.selected_note = None
        
        # Get Downloads folder path
        self.downloads_folder = str(Path.home() / "Downloads")
        
        # Create UI
        self._create_widgets()
        
        # Auto-scan for notes on startup
        self._auto_scan_on_startup()
    
    def _create_widgets(self):
        """Create the GUI widgets."""
        
        # Top frame - Controls
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Scan button
        ttk.Button(control_frame, text="Rescan Databases", 
                  command=self._scan_notes).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(control_frame, text="Ready")
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.search_entry.bind('<KeyRelease>', self._on_search_change)
        
        ttk.Button(search_frame, text="Clear", 
                  command=self._clear_search).pack(side=tk.LEFT, padx=5)
        
        # Sort options
        sort_frame = ttk.Frame(self.root)
        sort_frame.pack(fill=tk.X, padx=10, pady=2)
        
        ttk.Label(sort_frame, text="Sort by:").pack(side=tk.LEFT)
        
        self.sort_var = tk.StringVar(value="Title")
        sort_options = ["Title", "Most Recent"]
        self.sort_combobox = ttk.Combobox(sort_frame, textvariable=self.sort_var, 
                                          values=sort_options, width=15, state="readonly")
        self.sort_combobox.pack(side=tk.LEFT, padx=5)
        self.sort_combobox.bind("<<ComboboxSelected>>", self._apply_sort)
        
        # Sort direction
        self.sort_direction = tk.StringVar(value="Ascending")
        sort_direction_options = ["Ascending", "Descending"]
        self.sort_direction_combobox = ttk.Combobox(sort_frame, textvariable=self.sort_direction, 
                                                    values=sort_direction_options, width=12, state="readonly")
        self.sort_direction_combobox.pack(side=tk.LEFT, padx=5)
        self.sort_direction_combobox.bind("<<ComboboxSelected>>", self._apply_sort)
        
        # Main content frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Note list
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(left_frame, text="Found Notes:").pack(anchor=tk.W)
        
        # Note listbox with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.note_listbox = tk.Listbox(list_frame, width=50)
        list_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.note_listbox.yview)
        self.note_listbox.configure(yscrollcommand=list_scrollbar.set)
        
        self.note_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.note_listbox.bind('<<ListboxSelect>>', self._on_note_select)
        
        # Separator
        ttk.Separator(main_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Right panel - Note content
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Content header
        content_header = ttk.Frame(right_frame)
        content_header.pack(fill=tk.X)
        
        ttk.Label(content_header, text="Note Content:").pack(side=tk.LEFT)
        
        # Action buttons
        action_frame = ttk.Frame(content_header)
        action_frame.pack(side=tk.RIGHT)
        
        ttk.Button(action_frame, text="Copy", 
                  command=self._copy_note).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="Export", 
                  command=self._export_note).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="Export All Filtered", 
                  command=self._export_filtered).pack(side=tk.LEFT, padx=2)
        
        # Content text area
        content_frame = ttk.Frame(right_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.content_text = tk.Text(content_frame, wrap=tk.WORD, state=tk.DISABLED)
        content_scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.content_text.yview)
        self.content_text.configure(yscrollcommand=content_scrollbar.set)
        
        self.content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        content_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _process_findings_into_individual_notes(self, findings):
        """
        Process the findings into individual notes.
        
        Args:
            findings: List of note findings from NoteFinder.
            
        Returns:
            List of individual notes with proper titles.
        """
        individual_notes = []
        
        # Get current time for "last modified" timestamp
        current_time = time.time()
        
        for finding in findings:
            # Get the original finding data
            database = finding['database']
            table = finding['table']
            key = finding['key']
            size = finding['size']
            content = finding['content']
            
            # Try to extract timestamp from database file modification time
            db_path = Path(Config.get_default_workspace_path()) / database / "state.vscdb"
            
            # Get file modification time if possible
            try:
                mod_time = os.path.getmtime(db_path)
            except:
                mod_time = current_time  # Use current time as fallback
            
            # Skip empty JSON structures
            if '{"notepads": {}' in content and '"notepadDataVersion": 0' in content:
                continue
                
            # Parse the content into individual notes
            parsed_notes = NoteParser.parse_notes(content)
            
            if parsed_notes:
                # Create individual note entries for each parsed note
                for parsed_note in parsed_notes:
                    title = parsed_note['title']
                    note_content = parsed_note['content']
                    
                    # Only include notes with actual titles
                    if title and title not in ["Untitled Note", "Empty Note", "Unformatted Note"]:
                        individual_notes.append({
                            'database': database,
                            'table': table,
                            'key': key,
                            'original_key': key,
                            'title': title,
                            'size': len(note_content),
                            'content': note_content,
                            'modified': mod_time  # Add modification time
                        })
            
        return individual_notes
    
    def _auto_scan_on_startup(self):
        """Automatically scan for notes when GUI starts."""
        def startup_scan_worker():
            try:
                self.status_label.config(text="Auto-scanning databases...")
                self.root.update()
                
                # Scan for notes
                finder = NoteFinder()
                findings = finder.find_notes()
                
                if findings:
                    # Process findings into individual notes
                    individual_notes = self._process_findings_into_individual_notes(findings)
                    self.all_notes = individual_notes
                    self.filtered_notes = individual_notes  # Set filtered notes same as all notes initially
                    
                    # Apply initial sorting
                    self._apply_sort()
                    
                    # Update the display
                    self._update_note_list()
                    self.status_label.config(text=f"Auto-scan complete: Found {len(individual_notes)} notes")
                else:
                    self.status_label.config(text="No notes found - Database scan complete")
                
            except Exception as e:
                print(f"Auto-scan failed: {e}")
                self.status_label.config(text=f"Scan failed: {str(e)[:50]}...")
        
        # Run in background thread to prevent GUI freezing
        thread = threading.Thread(target=startup_scan_worker, daemon=True)
        thread.start()
    
    def _scan_notes(self):
        """Scan for notes in a background thread."""
        def scan_worker():
            try:
                self.status_label.config(text="Scanning databases...")
                self.root.update()
                
                finder = NoteFinder()
                findings = finder.find_notes()
                
                if findings:
                    # Process findings into individual notes
                    individual_notes = self._process_findings_into_individual_notes(findings)
                    self.all_notes = individual_notes
                    self._update_note_list()
                    
                    self.status_label.config(text=f"Found {len(individual_notes)} notes")
                else:
                    self.status_label.config(text="No notes found")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to scan notes: {e}")
                self.status_label.config(text="Scan failed")
        
        # Run in background thread to prevent GUI freezing
        thread = threading.Thread(target=scan_worker, daemon=True)
        thread.start()
    
    def _on_search_change(self, event=None):
        """Handle search text changes."""
        self._filter_notes()
    
    def _clear_search(self):
        """Clear the search."""
        self.search_var.set("")
        self._filter_notes()
    
    def _filter_notes(self):
        """Filter notes based on search term."""
        search_term = self.search_var.get().lower().strip()
        
        # Start with all notes
        self.filtered_notes = self.all_notes
        
        # Apply search filter if there's a search term
        if search_term:
            self.filtered_notes = []
            for note in self.all_notes:
                # Search in title and content
                title = note.get('title', '').lower()
                if search_term in title or search_term in note['content'].lower():
                    self.filtered_notes.append(note)
        
        # Apply current sort after filtering
        self._apply_sort()
        
        # Update the listbox
        self._update_note_list()
    
    def _update_note_list(self):
        """Update the note listbox."""
        self.note_listbox.delete(0, tk.END)
        
        if not hasattr(self, 'filtered_notes') or self.filtered_notes is None:
            self.filtered_notes = self.all_notes
        
        # Ensure we have notes to display
        if not self.filtered_notes:
            self.note_listbox.insert(tk.END, "No notes found")
            return
            
        # Add each note to the listbox
        for note in self.filtered_notes:
            # Create a display string with just the title or a clean preview
            title = note.get('title', '')
            
            if title:
                # If we have a title, just use that
                display = title
            else:
                # Otherwise use the first line of content as title
                content_preview = note['content'].split('\n')[0].strip()
                # Limit length for display
                if len(content_preview) > 60:
                    content_preview = content_preview[:57] + "..."
                display = content_preview
            
            self.note_listbox.insert(tk.END, display)
        
        # Update status
        if hasattr(self, 'search_var') and self.search_var.get().strip():
            self.status_label.config(text=f"Showing {len(self.filtered_notes)} of {len(self.all_notes)} notes")
        else:
            self.status_label.config(text=f"Showing {len(self.all_notes)} notes")
            
        # Force update GUI
        self.root.update_idletasks()
    
    def _on_note_select(self, event):
        """Handle note selection."""
        selection = self.note_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if index < len(self.filtered_notes):
            self.selected_note = self.filtered_notes[index]
            self._display_note_content()
    
    def _display_note_content(self):
        """Display the selected note content."""
        if not self.selected_note:
            return
        
        note = self.selected_note
        
        # Prepare content for display
        title = note.get('title', '')
        original_key = note.get('original_key', note['key'])
        
        content = f"Key: {original_key}\n"
        if title:
            content += f"Title: {title}\n"
        content += f"Database: {note['database']}\n"
        content += f"Table: {note['table']}\n"
        content += f"Size: {note['size']} bytes\n"
        content += "=" * 50 + "\n\n"
        content += note['content']
        
        # Update text widget
        self.content_text.config(state=tk.NORMAL)
        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(1.0, content)
        self.content_text.config(state=tk.DISABLED)
    
    def _copy_note(self):
        """Copy the selected note to clipboard."""
        if not self.selected_note:
            messagebox.showwarning("Warning", "No note selected")
            return
        
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.selected_note['content'])
            messagebox.showinfo("Success", "Note copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy note: {e}")
    
    def _export_note(self):
        """Export the selected note to a file."""
        if not self.selected_note:
            messagebox.showwarning("Warning", "No note selected")
            return
        
        note = self.selected_note
        title = note.get('title', '')
        original_key = note.get('original_key', note['key'])
        
        # Create filename suggestion
        if title:
            filename_suggestion = f"{title.replace(' ', '_')}"
        else:
            filename_suggestion = f"{original_key.replace(' ', '_')}"
        
        # Define file types based on available modules
        filetypes = [(".txt", "*.txt"), (".md", "*.md")]
        if PDF_SUPPORT:
            filetypes.append((".pdf", "*.pdf"))
        if DOCX_SUPPORT:
            filetypes.append((".docx", "*.docx"))
        filetypes.append(("All files", "*.*"))
        
        # Ask for filename
        filename = filedialog.asksaveasfilename(
            title="Export Note",
            initialdir=self.downloads_folder,
            initialfile=filename_suggestion,
            defaultextension=".txt",
            filetypes=filetypes
        )
        
        if not filename:
            return
        
        try:
            # Determine export format based on file extension
            file_ext = os.path.splitext(filename)[1].lower()
            
            if file_ext == ".pdf" and PDF_SUPPORT:
                self._export_as_pdf(filename, note)
            elif file_ext == ".docx" and DOCX_SUPPORT:
                self._export_as_docx(filename, note)
            elif file_ext == ".md":
                self._export_as_markdown(filename, note)
            else:
                # Default to text export
                self._export_as_text(filename, note)
            
            messagebox.showinfo("Success", f"Note exported to: {filename}")
            
            # Open containing folder
            self._open_containing_folder(filename)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export note: {e}")
    
    def _export_as_text(self, filename, note):
        """Export note as text file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Cursor Note Export\n")
            f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Key: {note.get('original_key', note['key'])}\n")
            if note.get('title'):
                f.write(f"Title: {note['title']}\n")
            f.write(f"Database: {note['database']}\n")
            f.write(f"Size: {note['size']} bytes\n")
            f.write("-" * 30 + "\n\n")
            f.write(note['content'])
    
    def _export_as_pdf(self, filename, note):
        """Export note as PDF file."""
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create story elements
        story = []
        
        # Add header
        story.append(Paragraph(f"<b>Cursor Note Export</b>", styles['Title']))
        story.append(Paragraph(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Add metadata
        story.append(Paragraph(f"<b>Key:</b> {note.get('original_key', note['key'])}", styles['Normal']))
        if note.get('title'):
            story.append(Paragraph(f"<b>Title:</b> {note['title']}", styles['Normal']))
        story.append(Paragraph(f"<b>Database:</b> {note['database']}", styles['Normal']))
        story.append(Paragraph(f"<b>Size:</b> {note['size']} bytes", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Add content (handle line breaks)
        content_lines = note['content'].split('\n')
        for line in content_lines:
            if line.strip():
                story.append(Paragraph(line, styles['Normal']))
            else:
                story.append(Spacer(1, 6))
        
        # Build PDF
        doc.build(story)
    
    def _export_as_docx(self, filename, note):
        """Export note as DOCX file."""
        doc = docx.Document()
        
        # Add title
        doc.add_heading("Cursor Note Export", 0)
        
        # Add metadata
        doc.add_paragraph(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc.add_paragraph()
        
        meta_table = doc.add_table(rows=1, cols=2)
        meta_table.style = 'Table Grid'
        
        header_cells = meta_table.rows[0].cells
        header_cells[0].text = "Property"
        header_cells[1].text = "Value"
        
        # Add key
        row = meta_table.add_row().cells
        row[0].text = "Key"
        row[1].text = note.get('original_key', note['key'])
        
        # Add title if available
        if note.get('title'):
            row = meta_table.add_row().cells
            row[0].text = "Title"
            row[1].text = note['title']
        
        # Add other metadata
        row = meta_table.add_row().cells
        row[0].text = "Database"
        row[1].text = note['database']
        
        row = meta_table.add_row().cells
        row[0].text = "Size"
        row[1].text = f"{note['size']} bytes"
        
        # Add content
        doc.add_heading("Content", level=1)
        
        # Handle line breaks and paragraphs
        content_lines = note['content'].split('\n')
        current_paragraph = None
        
        for line in content_lines:
            if line.strip():
                if current_paragraph is None:
                    current_paragraph = doc.add_paragraph()
                current_paragraph.add_run(line)
            else:
                current_paragraph = None
                doc.add_paragraph()
        
        # Save document
        doc.save(filename)
    
    def _export_as_markdown(self, filename, note):
        """Export note as Markdown file."""
        with open(filename, 'w', encoding='utf-8') as f:
            # Add header with metadata
            f.write(f"# Cursor Note Export\n\n")
            f.write(f"*Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            
            # Add metadata table
            f.write("## Metadata\n\n")
            f.write("| Property | Value |\n")
            f.write("| --- | --- |\n")
            f.write(f"| Key | {note.get('original_key', note['key'])} |\n")
            if note.get('title'):
                f.write(f"| Title | {note['title']} |\n")
            f.write(f"| Database | {note['database']} |\n")
            f.write(f"| Size | {note['size']} bytes |\n\n")
            
            # Add content section
            f.write("## Content\n\n")
            
            # Preserve any markdown formatting in the content
            f.write(note['content'])
    
    def _open_containing_folder(self, filename):
        """Open the folder containing the exported file."""
        try:
            folder_path = os.path.dirname(os.path.abspath(filename))
            
            if os.name == 'nt':  # Windows
                os.startfile(folder_path)
            elif os.name == 'posix':  # macOS, Linux
                import subprocess
                if 'darwin' in os.uname().sysname.lower():  # macOS
                    subprocess.call(['open', folder_path])
                else:  # Linux
                    subprocess.call(['xdg-open', folder_path])
        except:
            # Silently fail if we can't open the folder
            pass
    
    def _export_filtered(self):
        """Export all filtered notes to a file."""
        if not self.filtered_notes:
            messagebox.showwarning("Warning", "No notes to export")
            return
        
        # Define file types based on available modules
        filetypes = [(".txt", "*.txt"), (".md", "*.md")]
        if PDF_SUPPORT:
            filetypes.append((".pdf", "*.pdf"))
        if DOCX_SUPPORT:
            filetypes.append((".docx", "*.docx"))
        filetypes.append(("All files", "*.*"))
        
        # Ask for filename
        filename = filedialog.asksaveasfilename(
            title="Export Filtered Notes",
            initialdir=self.downloads_folder,
            initialfile=f"cursor_notes_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            defaultextension=".txt",
            filetypes=filetypes
        )
        
        if not filename:
            return
        
        try:
            # Determine export format based on file extension
            file_ext = os.path.splitext(filename)[1].lower()
            
            if file_ext == ".pdf" and PDF_SUPPORT:
                self._export_filtered_as_pdf(filename)
            elif file_ext == ".docx" and DOCX_SUPPORT:
                self._export_filtered_as_docx(filename)
            elif file_ext == ".md":
                self._export_filtered_as_markdown(filename)
            else:
                # Default to text export
                self._export_filtered_as_text(filename)
            
            messagebox.showinfo("Success", f"Exported {len(self.filtered_notes)} notes to: {filename}")
            
            # Open containing folder
            self._open_containing_folder(filename)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export notes: {e}")
    
    def _export_filtered_as_text(self, filename):
        """Export filtered notes as text file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Cursor Notes Export (Filtered)\n")
            f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Search term: '{self.search_var.get()}'\n")
            f.write(f"Notes exported: {len(self.filtered_notes)}\n")
            f.write("=" * 70 + "\n\n")
            
            for i, note in enumerate(self.filtered_notes, 1):
                f.write(f"NOTE #{i}\n")
                f.write(f"Key: {note.get('original_key', note['key'])}\n")
                if note.get('title'):
                    f.write(f"Title: {note['title']}\n")
                f.write(f"Database: {note['database']}\n")
                f.write(f"Size: {note['size']} bytes\n")
                f.write("-" * 40 + "\n")
                f.write(note['content'])
                f.write("\n" + "=" * 70 + "\n\n")
    
    def _export_filtered_as_pdf(self, filename):
        """Export filtered notes as PDF file."""
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create story elements
        story = []
        
        # Add header
        story.append(Paragraph(f"<b>Cursor Notes Export (Filtered)</b>", styles['Title']))
        story.append(Paragraph(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Paragraph(f"Search term: '{self.search_var.get()}'", styles['Normal']))
        story.append(Paragraph(f"Notes exported: {len(self.filtered_notes)}", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Add each note
        for i, note in enumerate(self.filtered_notes, 1):
            # Add separator for notes after the first one
            if i > 1:
                story.append(Spacer(1, 12))
                story.append(Paragraph("=" * 40, styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Add note header
            story.append(Paragraph(f"<b>NOTE #{i}</b>", styles['Heading1']))
            
            # Add metadata
            story.append(Paragraph(f"<b>Key:</b> {note.get('original_key', note['key'])}", styles['Normal']))
            if note.get('title'):
                story.append(Paragraph(f"<b>Title:</b> {note['title']}", styles['Normal']))
            story.append(Paragraph(f"<b>Database:</b> {note['database']}", styles['Normal']))
            story.append(Paragraph(f"<b>Size:</b> {note['size']} bytes", styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Add content (handle line breaks)
            content_lines = note['content'].split('\n')
            for line in content_lines:
                if line.strip():
                    story.append(Paragraph(line, styles['Normal']))
                else:
                    story.append(Spacer(1, 6))
        
        # Build PDF
        doc.build(story)
    
    def _export_filtered_as_docx(self, filename):
        """Export filtered notes as DOCX file."""
        doc = docx.Document()
        
        # Add title
        doc.add_heading("Cursor Notes Export (Filtered)", 0)
        
        # Add metadata
        doc.add_paragraph(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc.add_paragraph(f"Search term: '{self.search_var.get()}'")
        doc.add_paragraph(f"Notes exported: {len(self.filtered_notes)}")
        doc.add_paragraph()
        
        # Add each note
        for i, note in enumerate(self.filtered_notes, 1):
            # Add separator for notes after the first one
            if i > 1:
                doc.add_paragraph("=" * 40)
                doc.add_paragraph()
            
            # Add note header
            doc.add_heading(f"NOTE #{i}", level=1)
            
            # Add metadata table
            meta_table = doc.add_table(rows=1, cols=2)
            meta_table.style = 'Table Grid'
            
            header_cells = meta_table.rows[0].cells
            header_cells[0].text = "Property"
            header_cells[1].text = "Value"
            
            # Add key
            row = meta_table.add_row().cells
            row[0].text = "Key"
            row[1].text = note.get('original_key', note['key'])
            
            # Add title if available
            if note.get('title'):
                row = meta_table.add_row().cells
                row[0].text = "Title"
                row[1].text = note['title']
            
            # Add other metadata
            row = meta_table.add_row().cells
            row[0].text = "Database"
            row[1].text = note['database']
            
            row = meta_table.add_row().cells
            row[0].text = "Size"
            row[1].text = f"{note['size']} bytes"
            
            # Add content heading
            doc.add_heading("Content", level=2)
            
            # Handle line breaks and paragraphs
            content_lines = note['content'].split('\n')
            current_paragraph = None
            
            for line in content_lines:
                if line.strip():
                    if current_paragraph is None:
                        current_paragraph = doc.add_paragraph()
                    current_paragraph.add_run(line)
                else:
                    current_paragraph = None
                    doc.add_paragraph()
        
        # Save document
        doc.save(filename)
    
    def _export_filtered_as_markdown(self, filename):
        """Export filtered notes as Markdown file."""
        with open(filename, 'w', encoding='utf-8') as f:
            # Add header
            f.write(f"# Cursor Notes Export (Filtered)\n\n")
            f.write(f"*Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write(f"**Search term:** '{self.search_var.get()}'\n\n")
            f.write(f"**Notes exported:** {len(self.filtered_notes)}\n\n")
            
            # Add each note
            for i, note in enumerate(self.filtered_notes, 1):
                # Add separator for notes after the first one
                if i > 1:
                    f.write("\n---\n\n")
                
                # Add note header
                f.write(f"## NOTE #{i}\n\n")
                
                # Add metadata table
                f.write("| Property | Value |\n")
                f.write("| --- | --- |\n")
                f.write(f"| Key | {note.get('original_key', note['key'])} |\n")
                if note.get('title'):
                    f.write(f"| Title | {note['title']} |\n")
                f.write(f"| Database | {note['database']} |\n")
                f.write(f"| Size | {note['size']} bytes |\n\n")
                
                # Add content section
                f.write("### Content\n\n")
                f.write(f"{note['content']}\n\n")
    
    def _apply_sort(self, event=None):
        """Sort the note list based on selected criteria."""
        if not hasattr(self, 'filtered_notes') or not self.filtered_notes:
            return
            
        sort_by = self.sort_var.get()
        direction = self.sort_direction.get()
        reverse = (direction == "Descending")
        
        if sort_by == "Title":
            # Sort by title
            self.filtered_notes.sort(key=lambda x: x.get('title', '').lower(), reverse=reverse)
        elif sort_by == "Most Recent":
            # Sort by modification time
            self.filtered_notes.sort(key=lambda x: x.get('modified', 0), reverse=not reverse)
        
        # Update the displayed list
        self._update_note_list()
    
    def run(self):
        """Start the GUI."""
        self.root.mainloop()

def main():
    """Main function."""
    app = NoteSearchGUI()
    app.run()

if __name__ == "__main__":
    main() 