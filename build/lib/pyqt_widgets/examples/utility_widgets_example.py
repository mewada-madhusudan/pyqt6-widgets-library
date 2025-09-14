"""
Example usage of utility widgets.
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QPushButton, QHBoxLayout, QTabWidget, QLabel,
                             QTextEdit, QSplitter)
from PyQt6.QtCore import Qt

# Add the parent directory to the path to import the widgets
sys.path.append('..')

from utility.quick_settings_panel import QuickSettingsPanel
from utility.pinned_note import NoteManager, PinnedNoteWidget
from utility.clipboard_history import ClipboardHistoryWidget
from utility.global_search import GlobalSearchWidget, file_search_provider, content_search_provider
from utility.shortcut_helper import ShortcutHelperWidget


class UtilityWidgetsExample(QMainWindow):
    """Example application for utility widgets."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Utility Widgets Example")
        self.setGeometry(100, 100, 1200, 800)

        # Central widget with tabs
        central_widget = QTabWidget()
        self.setCentralWidget(central_widget)

        # Settings panel tab
        self.create_settings_tab(central_widget)

        # Notes tab
        self.create_notes_tab(central_widget)

        # Clipboard history tab
        self.create_clipboard_tab(central_widget)

        # Global search tab
        self.create_search_tab(central_widget)

        # Shortcuts tab
        self.create_shortcuts_tab(central_widget)

    def create_settings_tab(self, parent):
        """Create settings panel tab."""
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Settings panel
        self.settings_panel = QuickSettingsPanel("Application Settings")
        self.settings_panel.setting_changed.connect(self.on_setting_changed)
        self.settings_panel.settings_applied.connect(self.on_settings_applied)

        # Add various settings
        self.settings_panel.add_toggle_setting(
            "dark_mode", "Dark Mode", False, "Enable dark theme"
        )
        self.settings_panel.add_toggle_setting(
            "auto_save", "Auto Save", True, "Automatically save changes"
        )
        self.settings_panel.add_choice_setting(
            "language", "Language", ["English", "Spanish", "French", "German"], 0
        )
        self.settings_panel.add_number_setting(
            "font_size", "Font Size", 12, 8, 24, "Application font size"
        )
        self.settings_panel.add_slider_setting(
            "volume", "Volume", 75, 0, 100, "Audio volume level"
        )

        layout.addWidget(self.settings_panel)

        # Settings output
        self.settings_output = QTextEdit()
        self.settings_output.setReadOnly(True)
        self.settings_output.setMaximumWidth(300)
        layout.addWidget(self.settings_output)

        parent.addTab(widget, "Settings Panel")

    def create_notes_tab(self, parent):
        """Create notes tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Note manager
        self.note_manager = NoteManager()
        self.note_manager.notes_changed.connect(self.on_notes_changed)
        layout.addWidget(self.note_manager)

        parent.addTab(widget, "Pinned Notes")

    def create_clipboard_tab(self, parent):
        """Create clipboard history tab."""
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Clipboard history
        self.clipboard_history = ClipboardHistoryWidget(max_items=20)
        self.clipboard_history.item_selected.connect(self.on_clipboard_item_selected)
        self.clipboard_history.item_copied.connect(self.on_clipboard_item_copied)
        layout.addWidget(self.clipboard_history)

        # Test area
        test_widget = QWidget()
        test_layout = QVBoxLayout(test_widget)

        test_layout.addWidget(QLabel("Test Clipboard:"))

        self.test_text = QTextEdit()
        self.test_text.setPlaceholderText("Copy text from here to test clipboard history...")
        test_layout.addWidget(self.test_text)

        # Add manual item button
        add_item_btn = QPushButton("Add Manual Item")
        add_item_btn.clicked.connect(self.add_manual_clipboard_item)
        test_layout.addWidget(add_item_btn)

        layout.addWidget(test_widget)

        parent.addTab(widget, "Clipboard History")

    def create_search_tab(self, parent):
        """Create global search tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Global search
        self.global_search = GlobalSearchWidget("Search files, content, and more...")
        self.global_search.search_performed.connect(self.on_search_performed)
        self.global_search.result_selected.connect(self.on_search_result_selected)

        # Add search providers
        self.global_search.add_search_provider("files", file_search_provider)
        self.global_search.add_search_provider("content", content_search_provider)
        self.global_search.add_search_provider("custom", self.custom_search_provider)

        layout.addWidget(self.global_search)

        parent.addTab(widget, "Global Search")

    def create_shortcuts_tab(self, parent):
        """Create shortcuts helper tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Shortcuts helper
        self.shortcuts_helper = ShortcutHelperWidget()
        self.shortcuts_helper.shortcut_activated.connect(self.on_shortcut_activated)

        # Add custom shortcuts
        self.shortcuts_helper.add_shortcut(
            "custom_action", "Ctrl+Shift+A", "Custom action", "Custom"
        )
        self.shortcuts_helper.add_shortcut(
            "special_mode", "Alt+S", "Enter special mode", "Custom"
        )

        layout.addWidget(self.shortcuts_helper)

        parent.addTab(widget, "Shortcuts Helper")

    def on_setting_changed(self, name, value):
        """Handle setting change."""
        self.settings_output.append(f"Setting changed: {name} = {value}")

    def on_settings_applied(self, all_settings):
        """Handle settings applied."""
        self.settings_output.append(f"Settings applied: {all_settings}")

    def on_notes_changed(self, notes_data):
        """Handle notes change."""
        print(f"Notes changed: {len(notes_data)} notes")

    def on_clipboard_item_selected(self, content):
        """Handle clipboard item selection."""
        print(f"Clipboard item selected: {content[:50]}...")

    def on_clipboard_item_copied(self, content):
        """Handle clipboard item copied."""
        print(f"Clipboard item copied: {content[:50]}...")

    def add_manual_clipboard_item(self):
        """Add manual clipboard item."""
        text = self.test_text.toPlainText()
        if text:
            self.clipboard_history.add_manual_item(text)

    def on_search_performed(self, query, filters):
        """Handle search performed."""
        print(f"Search performed: '{query}' with filters: {filters}")

    def on_search_result_selected(self, result):
        """Handle search result selected."""
        print(f"Search result selected: {result}")

    def custom_search_provider(self, query, filters):
        """Custom search provider."""
        results = []

        # Mock custom search results
        if "test" in query.lower():
            results.append({
                'title': f'Custom Test Result for "{query}"',
                'description': 'This is a custom search result from the example provider',
                'type': 'custom',
                'score': 90.0
            })

        if "example" in query.lower():
            results.append({
                'title': 'Example Custom Item',
                'description': 'Another example result with different content',
                'type': 'custom',
                'score': 85.0
            })

        return results

    def on_shortcut_activated(self, shortcut_name):
        """Handle shortcut activation."""
        print(f"Shortcut activated: {shortcut_name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = UtilityWidgetsExample()
    window.show()

    sys.exit(app.exec())