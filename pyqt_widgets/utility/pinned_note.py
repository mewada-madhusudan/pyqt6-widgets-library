"""
Pinned note widget - draggable notes/reminders.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QPushButton, QLabel, QFrame, QColorDialog,
                             QMenu, QApplication)
from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QDateTime, QTimer, QMimeData
from PyQt6.QtGui import (QPainter, QBrush, QPen, QColor, QFont, QDrag,
                         QPixmap, QCursor, QAction)
from ..base.theme_manager import theme_manager
from typing import Dict, List
import json


class PinnedNoteWidget(QWidget):
    """Draggable pinned note widget."""

    note_changed = pyqtSignal(str)  # note content
    note_deleted = pyqtSignal()
    note_moved = pyqtSignal(object)  # new position
    color_changed = pyqtSignal(str)  # color hex

    def __init__(self, content="", color="#FFE066", parent=None):
        super().__init__(parent)
        self._content = content
        self._color = color
        self._created_time = QDateTime.currentDateTime()
        self._is_editing = False
        self._drag_position = None
        self._setup_ui()

    def _setup_ui(self):
        """Setup the pinned note UI."""
        self.setFixedSize(200, 200)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # Header with controls
        header_layout = QHBoxLayout()
        header_layout.setSpacing(4)

        # Color button
        self.color_btn = QPushButton()
        self.color_btn.setFixedSize(16, 16)
        self.color_btn.clicked.connect(self._change_color)
        self.color_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._color};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: 8px;
            }}
            QPushButton:hover {{
                border-width: 2px;
            }}
        """)
        header_layout.addWidget(self.color_btn)

        header_layout.addStretch()

        # Menu button
        self.menu_btn = QPushButton("⋮")
        self.menu_btn.setFixedSize(16, 16)
        self.menu_btn.clicked.connect(self._show_menu)
        self.menu_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-color: transparent;
                color: {theme_manager.get_color('text')};
                font-weight: bold;
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
                border-radius: 8px;
            }}
        """)
        header_layout.addWidget(self.menu_btn)

        # Delete button
        self.delete_btn = QPushButton("×")
        self.delete_btn.setFixedSize(16, 16)
        self.delete_btn.clicked.connect(self.delete_note)
        self.delete_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-color: transparent;
                color: {theme_manager.get_color('danger')};
                font-weight: bold;
                font-size: 12pt;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('danger')};
                color: white;
                border-radius: 8px;
            }}
        """)
        header_layout.addWidget(self.delete_btn)

        layout.addLayout(header_layout)

        # Content area
        self.content_edit = QTextEdit()
        self.content_edit.setPlainText(self._content)
        self.content_edit.textChanged.connect(self._on_content_changed)
        self.content_edit.setStyleSheet(f"""
            QTextEdit {{
                border: none;
                background-color: transparent;
                color: {theme_manager.get_color('text')};
                font-family: 'Segoe UI';
                font-size: 9pt;
            }}
        """)
        layout.addWidget(self.content_edit)

        # Timestamp
        self.timestamp_label = QLabel(self._created_time.toString("MMM dd, hh:mm"))
        self.timestamp_label.setFont(theme_manager.get_font('caption'))
        self.timestamp_label.setStyleSheet(f"""
            color: {theme_manager.get_color('text_secondary')};
            font-size: 7pt;
        """)
        layout.addWidget(self.timestamp_label)

        # Apply note color
        self._update_style()

        # Enable drag and drop
        self.setAcceptDrops(True)

    def _update_style(self):
        """Update note appearance based on color."""
        # Darken color for border
        color = QColor(self._color)
        border_color = color.darker(120).name()

        self.setStyleSheet(f"""
            PinnedNoteWidget {{
                background-color: {self._color};
                border: 2px solid {border_color};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}
        """)

        # Update color button
        self.color_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._color};
                border: 1px solid {border_color};
                border-radius: 8px;
            }}
            QPushButton:hover {{
                border-width: 2px;
            }}
        """)

    def _change_color(self):
        """Change note color."""
        color = QColorDialog.getColor(QColor(self._color), self)
        if color.isValid():
            self._color = color.name()
            self._update_style()
            self.color_changed.emit(self._color)

    def _show_menu(self):
        """Show context menu."""
        menu = QMenu(self)

        # Duplicate action
        duplicate_action = QAction("Duplicate", self)
        duplicate_action.triggered.connect(self._duplicate_note)
        menu.addAction(duplicate_action)

        # Change color action
        color_action = QAction("Change Color", self)
        color_action.triggered.connect(self._change_color)
        menu.addAction(color_action)

        menu.addSeparator()

        # Delete action
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self.delete_note)
        menu.addAction(delete_action)

        # Show menu at button position
        global_pos = self.menu_btn.mapToGlobal(QPoint(0, self.menu_btn.height()))
        menu.exec(global_pos)

    def _duplicate_note(self):
        """Duplicate this note."""
        if self.parent():
            # If part of a note manager, let it handle duplication
            if hasattr(self.parent(), 'duplicate_note'):
                self.parent().duplicate_note(self)

    def _on_content_changed(self):
        """Handle content change."""
        self._content = self.content_edit.toPlainText()
        self.note_changed.emit(self._content)

    def mousePressEvent(self, event):
        """Handle mouse press for dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging."""
        if (event.buttons() == Qt.MouseButton.LeftButton and
                self._drag_position is not None):
            new_pos = event.globalPosition().toPoint() - self._drag_position
            self.move(new_pos)
            self.note_moved.emit(new_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Handle mouse release."""
        self._drag_position = None
        event.accept()

    def delete_note(self):
        """Delete this note."""
        self.note_deleted.emit()
        self.close()

    def get_content(self) -> str:
        """Get note content."""
        return self._content

    def set_content(self, content: str):
        """Set note content."""
        self._content = content
        self.content_edit.setPlainText(content)

    def get_color(self) -> str:
        """Get note color."""
        return self._color

    def set_color(self, color: str):
        """Set note color."""
        self._color = color
        self._update_style()

    def get_data(self) -> dict:
        """Get note data for serialization."""
        return {
            'content': self._content,
            'color': self._color,
            'position': {'x': self.x(), 'y': self.y()},
            'created_time': self._created_time.toString(Qt.DateFormat.ISODate)
        }

    def set_data(self, data: dict):
        """Set note data from serialization."""
        self._content = data.get('content', '')
        self._color = data.get('color', '#FFE066')

        if 'position' in data:
            pos = data['position']
            self.move(pos['x'], pos['y'])

        if 'created_time' in data:
            self._created_time = QDateTime.fromString(data['created_time'], Qt.DateFormat.ISODate)
            self.timestamp_label.setText(self._created_time.toString("MMM dd, hh:mm"))

        self.content_edit.setPlainText(self._content)
        self._update_style()


class NoteManager(QWidget):
    """Manager for multiple pinned notes."""

    notes_changed = pyqtSignal(list)  # list of note data

    def __init__(self, parent=None):
        super().__init__(parent)
        self._notes = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup note manager UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Control panel
        controls = QHBoxLayout()

        self.add_btn = QPushButton("Add Note")
        self.add_btn.clicked.connect(self.add_note)

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_notes)

        self.save_btn = QPushButton("Save Notes")
        self.save_btn.clicked.connect(self.save_notes)

        self.load_btn = QPushButton("Load Notes")
        self.load_btn.clicked.connect(self.load_notes)

        controls.addWidget(self.add_btn)
        controls.addWidget(self.clear_btn)
        controls.addStretch()
        controls.addWidget(self.save_btn)
        controls.addWidget(self.load_btn)

        layout.addLayout(controls)

        # Notes area (parent widget for notes)
        self.notes_area = QWidget()
        self.notes_area.setMinimumSize(800, 600)
        self.notes_area.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_manager.get_color('background')};
                border: 1px solid {theme_manager.get_color('border')};
            }}
        """)
        layout.addWidget(self.notes_area)

    def add_note(self, content="New note", color="#FFE066", position=None):
        """Add a new note."""
        note = PinnedNoteWidget(content, color, self.notes_area)

        # Position note
        if position:
            note.move(position.x(), position.y())
        else:
            # Position randomly or in grid
            import random
            x = random.randint(10, self.notes_area.width() - 210)
            y = random.randint(10, self.notes_area.height() - 210)
            note.move(x, y)

        note.show()

        # Connect signals
        note.note_deleted.connect(lambda: self._remove_note(note))
        note.note_changed.connect(self._on_notes_changed)
        note.note_moved.connect(self._on_notes_changed)
        note.color_changed.connect(self._on_notes_changed)

        self._notes.append(note)
        self._on_notes_changed()

        return note

    def _remove_note(self, note):
        """Remove a note."""
        if note in self._notes:
            self._notes.remove(note)
            self._on_notes_changed()

    def duplicate_note(self, note):
        """Duplicate a note."""
        new_note = self.add_note(
            note.get_content(),
            note.get_color(),
            QPoint(note.x() + 20, note.y() + 20)
        )
        return new_note

    def clear_notes(self):
        """Clear all notes."""
        for note in self._notes[:]:
            note.close()
        self._notes.clear()
        self._on_notes_changed()

    def _on_notes_changed(self):
        """Handle notes change."""
        note_data = [note.get_data() for note in self._notes]
        self.notes_changed.emit(note_data)

    def get_notes_data(self) -> list:
        """Get all notes data."""
        return [note.get_data() for note in self._notes]

    def load_notes_data(self, notes_data: list):
        """Load notes from data."""
        self.clear_notes()

        for data in notes_data:
            note = PinnedNoteWidget(parent=self.notes_area)
            note.set_data(data)
            note.show()

            # Connect signals
            note.note_deleted.connect(lambda n=note: self._remove_note(n))
            note.note_changed.connect(self._on_notes_changed)
            note.note_moved.connect(self._on_notes_changed)
            note.color_changed.connect(self._on_notes_changed)

            self._notes.append(note)

        self._on_notes_changed()

    def save_notes(self):
        """Save notes to file (placeholder - would need file dialog)."""
        # In a real implementation, this would open a file dialog
        notes_data = self.get_notes_data()
        print("Notes data:", json.dumps(notes_data, indent=2))

    def load_notes(self):
        """Load notes from file (placeholder - would need file dialog)."""
        # In a real implementation, this would open a file dialog
        # For demo, load some sample notes
        sample_data = [
            {
                'content': 'Sample note 1',
                'color': '#FFE066',
                'position': {'x': 50, 'y': 50},
                'created_time': QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)
            },
            {
                'content': 'Sample note 2\nWith multiple lines',
                'color': '#FF9999',
                'position': {'x': 270, 'y': 80},
                'created_time': QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)
            }
        ]
        self.load_notes_data(sample_data)


class SimpleNoteWidget(QWidget):
    """Simplified note widget."""

    content_changed = pyqtSignal(str)

    def __init__(self, content="", parent=None):
        super().__init__(parent)
        self._content = content
        self._setup_ui()

    def _setup_ui(self):
        """Setup simple note."""
        layout = QVBoxLayout(self)

        # Content
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(self._content)
        self.text_edit.textChanged.connect(self._on_content_changed)
        self.text_edit.setMaximumHeight(100)
        layout.addWidget(self.text_edit)

        # Timestamp
        timestamp = QDateTime.currentDateTime().toString("MMM dd, hh:mm")
        self.timestamp_label = QLabel(timestamp)
        self.timestamp_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        layout.addWidget(self.timestamp_label)

        # Style
        self.setStyleSheet(f"""
            SimpleNoteWidget {{
                background-color: {theme_manager.get_color('surface')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                padding: 8px;
            }}
        """)

    def _on_content_changed(self):
        """Handle content change."""
        self._content = self.text_edit.toPlainText()
        self.content_changed.emit(self._content)

    def get_content(self) -> str:
        """Get content."""
        return self._content

    def set_content(self, content: str):
        """Set content."""
        self._content = content
        self.text_edit.setPlainText(content)