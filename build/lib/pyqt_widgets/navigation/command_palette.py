"""
Command palette widget for searchable actions.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QListWidget, QListWidgetItem, QLabel, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QKeySequence
from ..base.base_popup import BasePopupWidget
from ..base.theme_manager import theme_manager


class CommandPaletteWidget(BasePopupWidget):
    """Searchable command palette overlay."""

    command_executed = pyqtSignal(str, dict)  # Emits command name and data

    def __init__(self, parent=None):
        super().__init__(parent, modal=True)
        self._commands = {}
        self._filtered_commands = []
        self._setup_palette_ui()

    def _setup_palette_ui(self):
        """Setup the command palette UI."""
        self.setFixedSize(600, 400)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type a command...")
        self.search_input.textChanged.connect(self._filter_commands)
        self.search_input.returnPressed.connect(self._execute_selected_command)

        search_font = theme_manager.get_font('default')
        search_font.setPointSize(14)
        self.search_input.setFont(search_font)

        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                border: none;
                border-bottom: 2px solid {theme_manager.get_color('border')};
                padding: 12px 16px;
                font-size: 14px;
                background-color: {theme_manager.get_color('surface')};
                color: {theme_manager.get_color('text')};
            }}
            QLineEdit:focus {{
                border-bottom-color: {theme_manager.get_color('primary')};
            }}
        """)

        main_layout.addWidget(self.search_input)

        # Commands list
        self.commands_list = QListWidget()
        self.commands_list.setFrameShape(self.commands_list.Shape.NoFrame)
        self.commands_list.itemClicked.connect(self._on_item_clicked)
        self.commands_list.itemActivated.connect(self._on_item_activated)

        self.commands_list.setStyleSheet(f"""
            QListWidget {{
                border: none;
                background-color: {theme_manager.get_color('surface')};
                alternate-background-color: {theme_manager.get_color('hover')};
            }}
            QListWidget::item {{
                padding: 8px 16px;
                border-bottom: 1px solid {theme_manager.get_color('border')};
            }}
            QListWidget::item:selected {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
            }}
            QListWidget::item:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)

        main_layout.addWidget(self.commands_list)

        # Footer with help text
        footer_label = QLabel("↑↓ to navigate • Enter to execute • Esc to close")
        footer_label.setStyleSheet(f"""
            QLabel {{
                color: {theme_manager.get_color('text_secondary')};
                padding: 8px 16px;
                background-color: {theme_manager.get_color('light')};
                border-top: 1px solid {theme_manager.get_color('border')};
            }}
        """)
        footer_label.setFont(theme_manager.get_font('caption'))
        main_layout.addWidget(footer_label)

        # Set layout
        self.layout.addLayout(main_layout)

        # Setup keyboard navigation
        self._setup_keyboard_navigation()

    def _setup_keyboard_navigation(self):
        """Setup keyboard navigation."""
        self.search_input.keyPressEvent = self._handle_key_press

    def _handle_key_press(self, event):
        """Handle key press events for navigation."""
        if event.key() == Qt.Key.Key_Down:
            if self.commands_list.count() > 0:
                current_row = self.commands_list.currentRow()
                if current_row < self.commands_list.count() - 1:
                    self.commands_list.setCurrentRow(current_row + 1)
                else:
                    self.commands_list.setCurrentRow(0)
        elif event.key() == Qt.Key.Key_Up:
            if self.commands_list.count() > 0:
                current_row = self.commands_list.currentRow()
                if current_row > 0:
                    self.commands_list.setCurrentRow(current_row - 1)
                else:
                    self.commands_list.setCurrentRow(self.commands_list.count() - 1)
        elif event.key() == Qt.Key.Key_Escape:
            self.close_animated()
        else:
            # Pass other keys to default handler
            QLineEdit.keyPressEvent(self.search_input, event)

    def add_command(self, name: str, description: str = "", shortcut: str = "",
                    icon: QIcon = None, data: dict = None, category: str = ""):
        """Add a command to the palette."""
        command_info = {
            'name': name,
            'description': description,
            'shortcut': shortcut,
            'icon': icon,
            'data': data or {},
            'category': category,
            'search_text': f"{name} {description} {category}".lower()
        }

        self._commands[name] = command_info
        self._update_commands_display()

    def remove_command(self, name: str):
        """Remove a command from the palette."""
        if name in self._commands:
            del self._commands[name]
            self._update_commands_display()

    def clear_commands(self):
        """Clear all commands."""
        self._commands.clear()
        self._update_commands_display()

    def _filter_commands(self, search_text: str):
        """Filter commands based on search text."""
        search_text = search_text.lower().strip()

        if not search_text:
            self._filtered_commands = list(self._commands.values())
        else:
            self._filtered_commands = [
                cmd for cmd in self._commands.values()
                if search_text in cmd['search_text']
            ]

        # Sort by relevance (exact name matches first)
        self._filtered_commands.sort(key=lambda cmd: (
            0 if cmd['name'].lower().startswith(search_text) else 1,
            cmd['name'].lower()
        ))

        self._update_commands_display()

        # Select first item
        if self.commands_list.count() > 0:
            self.commands_list.setCurrentRow(0)

    def _update_commands_display(self):
        """Update the commands list display."""
        self.commands_list.clear()

        current_category = None
        for command in self._filtered_commands:
            # Add category separator if needed
            if command['category'] and command['category'] != current_category:
                if current_category is not None:  # Not the first category
                    separator_item = QListWidgetItem()
                    separator_item.setSizeHint(separator_item.sizeHint())
                    separator_widget = self._create_category_separator(command['category'])
                    self.commands_list.addItem(separator_item)
                    self.commands_list.setItemWidget(separator_item, separator_widget)

                current_category = command['category']

            # Add command item
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, command)

            # Create custom widget for command item
            item_widget = self._create_command_item_widget(command)
            item.setSizeHint(item_widget.sizeHint())

            self.commands_list.addItem(item)
            self.commands_list.setItemWidget(item, item_widget)

    def _create_category_separator(self, category: str) -> QWidget:
        """Create category separator widget."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 8, 16, 8)

        label = QLabel(category.upper())
        label.setFont(theme_manager.get_font('caption'))
        label.setStyleSheet(f"""
            QLabel {{
                color: {theme_manager.get_color('text_secondary')};
                font-weight: bold;
            }}
        """)

        layout.addWidget(label)
        layout.addStretch()

        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_manager.get_color('light')};
                border-bottom: 1px solid {theme_manager.get_color('border')};
            }}
        """)

        return widget

    def _create_command_item_widget(self, command: dict) -> QWidget:
        """Create widget for command item."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(12)

        # Icon
        if command['icon']:
            icon_label = QLabel()
            icon_label.setPixmap(command['icon'].pixmap(20, 20))
            icon_label.setFixedSize(20, 20)
            layout.addWidget(icon_label)

        # Command info
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2)

        # Command name
        name_label = QLabel(command['name'])
        name_font = theme_manager.get_font('default')
        name_font.setWeight(QFont.Weight.Bold)
        name_label.setFont(name_font)
        info_layout.addWidget(name_label)

        # Description
        if command['description']:
            desc_label = QLabel(command['description'])
            desc_label.setFont(theme_manager.get_font('caption'))
            desc_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            info_layout.addWidget(desc_label)

        layout.addLayout(info_layout)
        layout.addStretch()

        # Shortcut
        if command['shortcut']:
            shortcut_label = QLabel(command['shortcut'])
            shortcut_label.setFont(theme_manager.get_font('caption'))
            shortcut_label.setStyleSheet(f"""
                QLabel {{
                    color: {theme_manager.get_color('text_secondary')};
                    background-color: {theme_manager.get_color('light')};
                    padding: 2px 6px;
                    border-radius: 3px;
                    border: 1px solid {theme_manager.get_color('border')};
                }}
            """)
            layout.addWidget(shortcut_label)

        return widget

    def _on_item_clicked(self, item: QListWidgetItem):
        """Handle item click."""
        self._execute_command_from_item(item)

    def _on_item_activated(self, item: QListWidgetItem):
        """Handle item activation (double-click or Enter)."""
        self._execute_command_from_item(item)

    def _execute_selected_command(self):
        """Execute currently selected command."""
        current_item = self.commands_list.currentItem()
        if current_item:
            self._execute_command_from_item(current_item)

    def _execute_command_from_item(self, item: QListWidgetItem):
        """Execute command from list item."""
        command_data = item.data(Qt.ItemDataRole.UserRole)
        if command_data:
            self.command_executed.emit(command_data['name'], command_data['data'])
            self.close_animated()

    def show_palette(self):
        """Show the command palette."""
        self.search_input.clear()
        self._filter_commands("")
        self.show_centered()
        self.search_input.setFocus()

    def get_commands(self) -> dict:
        """Get all registered commands."""
        return self._commands.copy()


class QuickCommandPalette(CommandPaletteWidget):
    """Simplified command palette for common actions."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._add_default_commands()

    def _add_default_commands(self):
        """Add default common commands."""
        self.add_command("New File", "Create a new file", "Ctrl+N", category="File")
        self.add_command("Open File", "Open an existing file", "Ctrl+O", category="File")
        self.add_command("Save", "Save current file", "Ctrl+S", category="File")
        self.add_command("Save As", "Save file with new name", "Ctrl+Shift+S", category="File")

        self.add_command("Copy", "Copy selection", "Ctrl+C", category="Edit")
        self.add_command("Paste", "Paste from clipboard", "Ctrl+V", category="Edit")
        self.add_command("Undo", "Undo last action", "Ctrl+Z", category="Edit")
        self.add_command("Redo", "Redo last undone action", "Ctrl+Y", category="Edit")

        self.add_command("Settings", "Open application settings", category="View")
        self.add_command("Help", "Show help documentation", "F1", category="Help")


class ApplicationCommandPalette(CommandPaletteWidget):
    """Command palette integrated with application actions."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._action_registry = {}

    def register_action(self, action_name: str, callback, description: str = "",
                        shortcut: str = "", icon: QIcon = None, category: str = ""):
        """Register an application action."""
        self._action_registry[action_name] = callback
        self.add_command(action_name, description, shortcut, icon,
                         {'callback': callback}, category)

    def unregister_action(self, action_name: str):
        """Unregister an application action."""
        if action_name in self._action_registry:
            del self._action_registry[action_name]
            self.remove_command(action_name)

    def _execute_command_from_item(self, item: QListWidgetItem):
        """Override to execute registered callbacks."""
        command_data = item.data(Qt.ItemDataRole.UserRole)
        if command_data and 'callback' in command_data['data']:
            callback = command_data['data']['callback']
            if callable(callback):
                try:
                    callback()
                except Exception as e:
                    print(f"Error executing command {command_data['name']}: {e}")

        super()._execute_command_from_item(item)


class SearchableCommandPalette(CommandPaletteWidget):
    """Command palette with advanced search features."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._perform_search)

    def _filter_commands(self, search_text: str):
        """Override with debounced search."""
        self._search_timer.stop()
        self._pending_search = search_text
        self._search_timer.start(150)  # 150ms debounce

    def _perform_search(self):
        """Perform the actual search."""
        search_text = getattr(self, '_pending_search', '').lower().strip()

        if not search_text:
            self._filtered_commands = list(self._commands.values())
        else:
            # Advanced fuzzy search
            scored_commands = []
            for cmd in self._commands.values():
                score = self._calculate_search_score(cmd, search_text)
                if score > 0:
                    scored_commands.append((score, cmd))

            # Sort by score (higher is better)
            scored_commands.sort(key=lambda x: x[0], reverse=True)
            self._filtered_commands = [cmd for score, cmd in scored_commands]

        self._update_commands_display()

        if self.commands_list.count() > 0:
            self.commands_list.setCurrentRow(0)

    def _calculate_search_score(self, command: dict, search_text: str) -> int:
        """Calculate search relevance score."""
        name = command['name'].lower()
        description = command['description'].lower()
        category = command['category'].lower()

        score = 0

        # Exact name match gets highest score
        if search_text == name:
            score += 100
        elif name.startswith(search_text):
            score += 80
        elif search_text in name:
            score += 60

        # Description matches
        if search_text in description:
            score += 30

        # Category matches
        if search_text in category:
            score += 20

        # Fuzzy matching for individual words
        search_words = search_text.split()
        for word in search_words:
            if word in name:
                score += 10
            if word in description:
                score += 5

        return score