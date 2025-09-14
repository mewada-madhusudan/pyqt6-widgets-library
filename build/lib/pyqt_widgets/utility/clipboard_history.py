"""
Clipboard history widget - shows recent clipboard contents.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
                             QListWidgetItem, QPushButton, QLabel, QTextEdit,
                             QFrame, QScrollArea, QMenu, QApplication)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QMimeData, QDateTime
from PyQt6.QtGui import QClipboard, QFont, QAction, QPixmap
from ..base.theme_manager import theme_manager
from typing import List, Dict, Any
import json


class ClipboardHistoryWidget(QWidget):
    """Clipboard history manager showing recent copies."""

    item_selected = pyqtSignal(str)  # clipboard content
    item_copied = pyqtSignal(str)  # content copied to clipboard
    history_cleared = pyqtSignal()

    def __init__(self, max_items=50, parent=None):
        super().__init__(parent)
        self._max_items = max_items
        self._history = []
        self._clipboard = QApplication.clipboard()
        self._last_clipboard_text = ""
        self._setup_ui()
        self._setup_monitoring()

    def _setup_ui(self):
        """Setup the clipboard history UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel("Clipboard History")
        title_label.setFont(theme_manager.get_font('heading'))
        title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Clear button
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_history)
        self.clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_manager.get_color('danger')};
                color: white;
                border: none;
                padding: 4px 12px;
                border-radius: {theme_manager.get_border_radius('sm')}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)
        header_layout.addWidget(self.clear_btn)

        layout.addLayout(header_layout)

        # History list
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self._on_item_clicked)
        self.history_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.history_list.customContextMenuRequested.connect(self._show_context_menu)

        # Style list
        self.history_list.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                background-color: {theme_manager.get_color('background')};
                alternate-background-color: {theme_manager.get_color('surface')};
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {theme_manager.get_color('border')};
                color: {theme_manager.get_color('text')};
            }}
            QListWidget::item:selected {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
            }}
            QListWidget::item:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)

        layout.addWidget(self.history_list)

        # Status bar
        status_layout = QHBoxLayout()

        self.status_label = QLabel("0 items")
        self.status_label.setFont(theme_manager.get_font('caption'))
        self.status_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        status_layout.addWidget(self.status_label)

        status_layout.addStretch()

        # Auto-monitor toggle
        self.monitor_btn = QPushButton("Monitoring: ON")
        self.monitor_btn.setCheckable(True)
        self.monitor_btn.setChecked(True)
        self.monitor_btn.toggled.connect(self._toggle_monitoring)
        self.monitor_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_manager.get_color('success')};
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: {theme_manager.get_border_radius('sm')}px;
                font-size: 8pt;
            }}
            QPushButton:checked {{
                background-color: {theme_manager.get_color('success')};
            }}
            QPushButton:!checked {{
                background-color: {theme_manager.get_color('secondary')};
            }}
        """)
        status_layout.addWidget(self.monitor_btn)

        layout.addLayout(status_layout)

    def _setup_monitoring(self):
        """Setup clipboard monitoring."""
        # Monitor clipboard changes
        self._clipboard.dataChanged.connect(self._on_clipboard_changed)

        # Timer for periodic checks (backup method)
        self._monitor_timer = QTimer()
        self._monitor_timer.timeout.connect(self._check_clipboard)
        self._monitor_timer.start(1000)  # Check every second

        # Get initial clipboard content
        self._check_clipboard()

    def _on_clipboard_changed(self):
        """Handle clipboard change signal."""
        self._check_clipboard()

    def _check_clipboard(self):
        """Check clipboard for new content."""
        if not self.monitor_btn.isChecked():
            return

        mime_data = self._clipboard.mimeData()

        if mime_data.hasText():
            text = mime_data.text().strip()
            if text and text != self._last_clipboard_text:
                self._add_to_history(text, "text")
                self._last_clipboard_text = text
        elif mime_data.hasImage():
            # Handle images (store as placeholder)
            image_info = f"Image ({mime_data.formats()})"
            if image_info != self._last_clipboard_text:
                self._add_to_history(image_info, "image", mime_data.imageData())
                self._last_clipboard_text = image_info

    def _add_to_history(self, content: str, content_type: str = "text", data=None):
        """Add item to history."""
        # Check if item already exists
        for item in self._history:
            if item['content'] == content:
                # Move to top
                self._history.remove(item)
                break

        # Add new item
        history_item = {
            'content': content,
            'type': content_type,
            'timestamp': QDateTime.currentDateTime(),
            'data': data
        }

        self._history.insert(0, history_item)

        # Limit history size
        if len(self._history) > self._max_items:
            self._history = self._history[:self._max_items]

        self._update_list()

    def _update_list(self):
        """Update the history list display."""
        self.history_list.clear()

        for item in self._history:
            list_item = ClipboardHistoryItem(item)
            widget_item = QListWidgetItem()
            widget_item.setSizeHint(list_item.sizeHint())

            self.history_list.addItem(widget_item)
            self.history_list.setItemWidget(widget_item, list_item)

        # Update status
        self.status_label.setText(f"{len(self._history)} items")

    def _on_item_clicked(self, item):
        """Handle item click."""
        widget = self.history_list.itemWidget(item)
        if widget:
            content = widget.get_content()

            # Copy to clipboard
            self._clipboard.setText(content)
            self.item_copied.emit(content)
            self.item_selected.emit(content)

    def _show_context_menu(self, position):
        """Show context menu for history item."""
        item = self.history_list.itemAt(position)
        if not item:
            return

        widget = self.history_list.itemWidget(item)
        if not widget:
            return

        menu = QMenu(self)

        # Copy action
        copy_action = QAction("Copy to Clipboard", self)
        copy_action.triggered.connect(lambda: self._copy_item(widget))
        menu.addAction(copy_action)

        # Delete action
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self._delete_item(item))
        menu.addAction(delete_action)

        menu.addSeparator()

        # Copy as plain text
        plain_action = QAction("Copy as Plain Text", self)
        plain_action.triggered.connect(lambda: self._copy_as_plain(widget))
        menu.addAction(plain_action)

        menu.exec(self.history_list.mapToGlobal(position))

    def _copy_item(self, widget):
        """Copy item to clipboard."""
        content = widget.get_content()
        self._clipboard.setText(content)
        self.item_copied.emit(content)

    def _copy_as_plain(self, widget):
        """Copy item as plain text."""
        content = widget.get_content()
        # Remove formatting if any
        plain_text = content.replace('\n', ' ').strip()
        self._clipboard.setText(plain_text)
        self.item_copied.emit(plain_text)

    def _delete_item(self, list_item):
        """Delete item from history."""
        row = self.history_list.row(list_item)
        if 0 <= row < len(self._history):
            self._history.pop(row)
            self._update_list()

    def _toggle_monitoring(self, enabled):
        """Toggle clipboard monitoring."""
        if enabled:
            self.monitor_btn.setText("Monitoring: ON")
            self._monitor_timer.start(1000)
        else:
            self.monitor_btn.setText("Monitoring: OFF")
            self._monitor_timer.stop()

    def clear_history(self):
        """Clear all history."""
        self._history.clear()
        self._update_list()
        self.history_cleared.emit()

    def get_history(self) -> List[Dict]:
        """Get history data."""
        return [
            {
                'content': item['content'],
                'type': item['type'],
                'timestamp': item['timestamp'].toString(Qt.DateFormat.ISODate)
            }
            for item in self._history
        ]

    def set_max_items(self, max_items: int):
        """Set maximum number of items to keep."""
        self._max_items = max_items
        if len(self._history) > max_items:
            self._history = self._history[:max_items]
            self._update_list()

    def add_manual_item(self, content: str):
        """Manually add item to history."""
        self._add_to_history(content, "manual")


class ClipboardHistoryItem(QWidget):
    """Individual clipboard history item widget."""

    def __init__(self, history_item: dict, parent=None):
        super().__init__(parent)
        self._history_item = history_item
        self._setup_ui()

    def _setup_ui(self):
        """Setup item UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # Content preview
        content = self._history_item['content']
        content_type = self._history_item['type']

        # Truncate long content
        if len(content) > 100:
            preview = content[:100] + "..."
        else:
            preview = content

        # Replace newlines for display
        preview = preview.replace('\n', ' ↵ ')

        self.content_label = QLabel(preview)
        self.content_label.setFont(theme_manager.get_font('default'))
        self.content_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        self.content_label.setWordWrap(True)
        layout.addWidget(self.content_label)

        # Metadata
        meta_layout = QHBoxLayout()

        # Type indicator
        type_label = QLabel(content_type.upper())
        type_label.setFont(theme_manager.get_font('caption'))
        type_label.setStyleSheet(f"""
            color: {theme_manager.get_color('primary')};
            font-weight: bold;
            font-size: 7pt;
        """)
        meta_layout.addWidget(type_label)

        meta_layout.addStretch()

        # Timestamp
        timestamp = self._history_item['timestamp'].toString("hh:mm:ss")
        time_label = QLabel(timestamp)
        time_label.setFont(theme_manager.get_font('caption'))
        time_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')}; font-size: 7pt;")
        meta_layout.addWidget(time_label)

        layout.addLayout(meta_layout)

    def get_content(self) -> str:
        """Get item content."""
        return self._history_item['content']


class SimpleClipboardHistory(QWidget):
    """Simplified clipboard history widget."""

    item_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._history = []
        self._clipboard = QApplication.clipboard()
        self._setup_ui()
        self._clipboard.dataChanged.connect(self._on_clipboard_changed)

    def _setup_ui(self):
        """Setup simple clipboard history."""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Recent Clips")
        title.setFont(theme_manager.get_font('heading'))
        layout.addWidget(title)

        # List
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        self.list_widget.setMaximumHeight(200)
        layout.addWidget(self.list_widget)

    def _on_clipboard_changed(self):
        """Handle clipboard change."""
        text = self._clipboard.text()
        if text and text not in self._history:
            self._history.insert(0, text)
            if len(self._history) > 10:  # Keep only 10 items
                self._history = self._history[:10]
            self._update_list()

    def _update_list(self):
        """Update list display."""
        self.list_widget.clear()
        for item in self._history:
            preview = item[:50] + "..." if len(item) > 50 else item
            self.list_widget.addItem(preview)

    def _on_item_clicked(self, item):
        """Handle item click."""
        row = self.list_widget.row(item)
        if 0 <= row < len(self._history):
            content = self._history[row]
            self._clipboard.setText(content)
            self.item_selected.emit(content)