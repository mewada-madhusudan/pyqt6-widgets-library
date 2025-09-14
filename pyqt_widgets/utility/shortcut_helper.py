"""
Keyboard shortcuts helper widget showing available shortcuts.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QScrollArea, QFrame, QPushButton, QLineEdit,
                             QTreeWidget, QTreeWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QKeySequence, QShortcut, QKeyEvent
from ..base.theme_manager import theme_manager
from typing import Dict, List, Tuple, Optional


class ShortcutHelperWidget(QWidget):
    """Keyboard shortcuts helper showing available shortcuts."""

    shortcut_activated = pyqtSignal(str)  # shortcut name
    help_requested = pyqtSignal(str)  # shortcut name

    def __init__(self, parent=None):
        super().__init__(parent)
        self._shortcuts = {}  # name -> (key_sequence, description, category)
        self._categories = {}  # category -> list of shortcuts
        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._perform_search)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the shortcut helper UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel("Keyboard Shortcuts")
        title_label.setFont(theme_manager.get_font('heading'))
        title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Quick help toggle
        self.quick_help_btn = QPushButton("Quick Help")
        self.quick_help_btn.setCheckable(True)
        self.quick_help_btn.toggled.connect(self._toggle_quick_help)
        self.quick_help_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
                border: none;
                padding: 4px 12px;
                border-radius: {theme_manager.get_border_radius('sm')}px;
                font-weight: bold;
            }}
            QPushButton:checked {{
                background-color: {theme_manager.get_color('success')};
            }}
        """)
        header_layout.addWidget(self.quick_help_btn)

        layout.addLayout(header_layout)

        # Search bar
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search shortcuts...")
        self.search_input.textChanged.connect(self._on_search_changed)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                padding: 6px 8px;
                background-color: {theme_manager.get_color('background')};
                color: {theme_manager.get_color('text')};
            }}
            QLineEdit:focus {{
                border-color: {theme_manager.get_color('primary')};
            }}
        """)
        search_layout.addWidget(self.search_input)

        # Clear search
        clear_btn = QPushButton("×")
        clear_btn.setFixedSize(24, 24)
        clear_btn.clicked.connect(self._clear_search)
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                border-radius: 12px;
                background-color: {theme_manager.get_color('text_secondary')};
                color: white;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('danger')};
            }}
        """)
        search_layout.addWidget(clear_btn)

        layout.addLayout(search_layout)

        # Shortcuts tree
        self.shortcuts_tree = QTreeWidget()
        self.shortcuts_tree.setHeaderLabels(["Shortcut", "Key", "Description"])
        self.shortcuts_tree.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.shortcuts_tree.itemDoubleClicked.connect(self._on_shortcut_activated)

        # Style tree
        self.shortcuts_tree.setStyleSheet(f"""
            QTreeWidget {{
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                background-color: {theme_manager.get_color('background')};
                alternate-background-color: {theme_manager.get_color('surface')};
                color: {theme_manager.get_color('text')};
            }}
            QTreeWidget::item {{
                padding: 4px;
                border-bottom: 1px solid {theme_manager.get_color('border')};
            }}
            QTreeWidget::item:selected {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
            }}
            QTreeWidget::item:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {{
                border-image: none;
                image: url(none);
            }}
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {{
                border-image: none;
                image: url(none);
            }}
        """)

        layout.addWidget(self.shortcuts_tree)

        # Quick help overlay (hidden by default)
        self.quick_help_overlay = self._create_quick_help_overlay()
        self.quick_help_overlay.hide()
        layout.addWidget(self.quick_help_overlay)

        # Load default shortcuts
        self._load_default_shortcuts()

    def _create_quick_help_overlay(self):
        """Create quick help overlay."""
        overlay = QFrame()
        overlay.setFrameStyle(QFrame.Shape.Box)
        overlay.setStyleSheet(f"""
            QFrame {{
                background-color: {theme_manager.get_color('surface')};
                border: 2px solid {theme_manager.get_color('primary')};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}
        """)

        layout = QVBoxLayout(overlay)
        layout.setContentsMargins(12, 12, 12, 12)

        # Title
        title = QLabel("Quick Help Mode")
        title.setFont(theme_manager.get_font('heading'))
        title.setStyleSheet(f"color: {theme_manager.get_color('primary')}; font-weight: bold;")
        layout.addWidget(title)

        # Instructions
        instructions = QLabel(
            "Press any key combination to see if it has a shortcut assigned.\n"
            "Press Escape to exit quick help mode."
        )
        instructions.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        # Current key display
        self.current_key_label = QLabel("Press a key combination...")
        self.current_key_label.setFont(theme_manager.get_font('code'))
        self.current_key_label.setStyleSheet(f"""
            color: {theme_manager.get_color('primary')};
            background-color: {theme_manager.get_color('background')};
            padding: 8px;
            border: 1px solid {theme_manager.get_color('border')};
            border-radius: {theme_manager.get_border_radius('sm')}px;
        """)
        layout.addWidget(self.current_key_label)

        # Shortcut info
        self.shortcut_info_label = QLabel("")
        self.shortcut_info_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        self.shortcut_info_label.setWordWrap(True)
        layout.addWidget(self.shortcut_info_label)

        return overlay

    def _load_default_shortcuts(self):
        """Load default application shortcuts."""
        # File operations
        self.add_shortcut("new_file", "Ctrl+N", "Create new file", "File")
        self.add_shortcut("open_file", "Ctrl+O", "Open file", "File")
        self.add_shortcut("save_file", "Ctrl+S", "Save file", "File")
        self.add_shortcut("save_as", "Ctrl+Shift+S", "Save file as", "File")
        self.add_shortcut("close_file", "Ctrl+W", "Close file", "File")
        self.add_shortcut("quit", "Ctrl+Q", "Quit application", "File")

        # Edit operations
        self.add_shortcut("undo", "Ctrl+Z", "Undo last action", "Edit")
        self.add_shortcut("redo", "Ctrl+Y", "Redo last action", "Edit")
        self.add_shortcut("cut", "Ctrl+X", "Cut selection", "Edit")
        self.add_shortcut("copy", "Ctrl+C", "Copy selection", "Edit")
        self.add_shortcut("paste", "Ctrl+V", "Paste from clipboard", "Edit")
        self.add_shortcut("select_all", "Ctrl+A", "Select all", "Edit")
        self.add_shortcut("find", "Ctrl+F", "Find text", "Edit")
        self.add_shortcut("replace", "Ctrl+H", "Find and replace", "Edit")

        # View operations
        self.add_shortcut("zoom_in", "Ctrl++", "Zoom in", "View")
        self.add_shortcut("zoom_out", "Ctrl+-", "Zoom out", "View")
        self.add_shortcut("zoom_reset", "Ctrl+0", "Reset zoom", "View")
        self.add_shortcut("fullscreen", "F11", "Toggle fullscreen", "View")

        # Navigation
        self.add_shortcut("go_back", "Alt+Left", "Go back", "Navigation")
        self.add_shortcut("go_forward", "Alt+Right", "Go forward", "Navigation")
        self.add_shortcut("refresh", "F5", "Refresh/Reload", "Navigation")

        # Help
        self.add_shortcut("help", "F1", "Show help", "Help")
        self.add_shortcut("shortcuts", "Ctrl+/", "Show shortcuts", "Help")

        self._update_tree()

    def add_shortcut(self, name: str, key_sequence: str, description: str,
                     category: str = "General"):
        """Add a shortcut to the helper."""
        self._shortcuts[name] = (key_sequence, description, category)

        if category not in self._categories:
            self._categories[category] = []
        self._categories[category].append(name)

    def remove_shortcut(self, name: str):
        """Remove a shortcut from the helper."""
        if name in self._shortcuts:
            _, _, category = self._shortcuts[name]
            del self._shortcuts[name]

            if category in self._categories:
                self._categories[category].remove(name)
                if not self._categories[category]:
                    del self._categories[category]

    def _update_tree(self):
        """Update the shortcuts tree display."""
        self.shortcuts_tree.clear()

        for category, shortcut_names in self._categories.items():
            category_item = QTreeWidgetItem([category, "", ""])
            category_item.setFont(0, theme_manager.get_font('heading'))

            for name in shortcut_names:
                key_sequence, description, _ = self._shortcuts[name]
                shortcut_item = QTreeWidgetItem([name, key_sequence, description])
                shortcut_item.setData(0, Qt.ItemDataRole.UserRole, name)
                category_item.addChild(shortcut_item)

            self.shortcuts_tree.addTopLevelItem(category_item)

        # Expand all categories
        self.shortcuts_tree.expandAll()

    def _on_search_changed(self, text):
        """Handle search text change."""
        self._search_timer.start(300)  # Debounce search

    def _perform_search(self):
        """Perform shortcut search."""
        query = self.search_input.text().lower().strip()

        if not query:
            self._update_tree()
            return

        # Filter shortcuts
        filtered_categories = {}

        for name, (key_sequence, description, category) in self._shortcuts.items():
            if (query in name.lower() or
                    query in key_sequence.lower() or
                    query in description.lower()):

                if category not in filtered_categories:
                    filtered_categories[category] = []
                filtered_categories[category].append(name)

        # Update tree with filtered results
        self.shortcuts_tree.clear()

        for category, shortcut_names in filtered_categories.items():
            category_item = QTreeWidgetItem([category, "", ""])
            category_item.setFont(0, theme_manager.get_font('heading'))

            for name in shortcut_names:
                key_sequence, description, _ = self._shortcuts[name]
                shortcut_item = QTreeWidgetItem([name, key_sequence, description])
                shortcut_item.setData(0, Qt.ItemDataRole.UserRole, name)
                category_item.addChild(shortcut_item)

            self.shortcuts_tree.addTopLevelItem(category_item)

        self.shortcuts_tree.expandAll()

    def _clear_search(self):
        """Clear search and show all shortcuts."""
        self.search_input.clear()
        self._update_tree()

    def _on_shortcut_activated(self, item, column):
        """Handle shortcut activation."""
        name = item.data(0, Qt.ItemDataRole.UserRole)
        if name:
            self.shortcut_activated.emit(name)

    def _toggle_quick_help(self, enabled):
        """Toggle quick help mode."""
        if enabled:
            self.quick_help_overlay.show()
            self.shortcuts_tree.hide()
            self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self.setFocus()
        else:
            self.quick_help_overlay.hide()
            self.shortcuts_tree.show()

    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press in quick help mode."""
        if self.quick_help_btn.isChecked():
            # Convert key event to sequence
            key_sequence = QKeySequence(event.key() | int(event.modifiers()))
            key_text = key_sequence.toString()

            self.current_key_label.setText(f"Key: {key_text}")

            # Check if this key sequence matches any shortcut
            matching_shortcuts = []
            for name, (sequence, description, category) in self._shortcuts.items():
                if sequence.lower() == key_text.lower():
                    matching_shortcuts.append((name, description, category))

            if matching_shortcuts:
                info_text = "Found shortcuts:\n"
                for name, description, category in matching_shortcuts:
                    info_text += f"• {name}: {description} ({category})\n"
                self.shortcut_info_label.setText(info_text.strip())
            else:
                self.shortcut_info_label.setText("No shortcut assigned to this key combination.")

            # Exit quick help on Escape
            if event.key() == Qt.Key.Key_Escape:
                self.quick_help_btn.setChecked(False)

        else:
            super().keyPressEvent(event)

    def get_shortcuts(self) -> Dict[str, Tuple[str, str, str]]:
        """Get all shortcuts."""
        return self._shortcuts.copy()

    def get_shortcut(self, name: str) -> Optional[Tuple[str, str, str]]:
        """Get specific shortcut."""
        return self._shortcuts.get(name)

    def export_shortcuts(self) -> str:
        """Export shortcuts as formatted text."""
        output = "Keyboard Shortcuts\n"
        output += "=" * 50 + "\n\n"

        for category, shortcut_names in self._categories.items():
            output += f"{category}:\n"
            output += "-" * len(category) + "\n"

            for name in shortcut_names:
                key_sequence, description, _ = self._shortcuts[name]
                output += f"  {key_sequence:<20} {description}\n"

            output += "\n"

        return output


class CompactShortcutHelper(QWidget):
    """Compact version of shortcut helper."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._shortcuts = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup compact helper."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # Title
        title = QLabel("Shortcuts")
        title.setFont(theme_manager.get_font('heading'))
        layout.addWidget(title)

        # Common shortcuts
        shortcuts_text = """
Ctrl+N - New
Ctrl+O - Open  
Ctrl+S - Save
Ctrl+Z - Undo
Ctrl+C - Copy
Ctrl+V - Paste
F1 - Help
        """.strip()

        shortcuts_label = QLabel(shortcuts_text)
        shortcuts_label.setFont(theme_manager.get_font('caption'))
        shortcuts_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        layout.addWidget(shortcuts_label)

    def add_shortcut(self, key: str, description: str):
        """Add a shortcut to display."""
        self._shortcuts[key] = description
        self._update_display()

    def _update_display(self):
        """Update shortcut display."""
        # This would update the display with current shortcuts
        pass


class ShortcutCapture(QWidget):
    """Widget for capturing keyboard shortcuts."""

    shortcut_captured = pyqtSignal(str)  # key sequence

    def __init__(self, parent=None):
        super().__init__(parent)
        self._capturing = False
        self._setup_ui()

    def _setup_ui(self):
        """Setup shortcut capture UI."""
        layout = QHBoxLayout(self)

        self.capture_label = QLabel("Press keys to capture shortcut...")
        layout.addWidget(self.capture_label)

        self.capture_btn = QPushButton("Capture")
        self.capture_btn.clicked.connect(self.start_capture)
        layout.addWidget(self.capture_btn)

    def start_capture(self):
        """Start capturing shortcuts."""
        self._capturing = True
        self.capture_label.setText("Press key combination...")
        self.capture_btn.setText("Cancel")
        self.capture_btn.clicked.disconnect()
        self.capture_btn.clicked.connect(self.stop_capture)
        self.setFocus()

    def stop_capture(self):
        """Stop capturing shortcuts."""
        self._capturing = False
        self.capture_label.setText("Press keys to capture shortcut...")
        self.capture_btn.setText("Capture")
        self.capture_btn.clicked.disconnect()
        self.capture_btn.clicked.connect(self.start_capture)

    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press for capture."""
        if self._capturing:
            key_sequence = QKeySequence(event.key() | int(event.modifiers()))
            key_text = key_sequence.toString()

            self.capture_label.setText(f"Captured: {key_text}")
            self.shortcut_captured.emit(key_text)
            self.stop_capture()
        else:
            super().keyPressEvent(event)