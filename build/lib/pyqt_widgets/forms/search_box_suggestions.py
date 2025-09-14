"""
Search box with live suggestions and autocomplete.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QListWidget,
                             QListWidgetItem, QLabel, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont
from ..base.theme_manager import theme_manager


class SearchBoxWithSuggestions(QWidget):
    """Search input with dropdown suggestions."""

    search_requested = pyqtSignal(str)  # Emits search query
    suggestion_selected = pyqtSignal(str)  # Emits selected suggestion
    text_changed = pyqtSignal(str)  # Emits current text

    def __init__(self, placeholder="Search...", parent=None):
        super().__init__(parent)
        self._placeholder = placeholder
        self._suggestions = []
        self._filtered_suggestions = []
        self._max_suggestions = 10
        self._min_chars = 1
        self._search_delay = 300  # ms
        self._setup_ui()

    def _setup_ui(self):
        """Setup the search box UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self._placeholder)
        self.search_input.textChanged.connect(self._on_text_changed)
        self.search_input.returnPressed.connect(self._on_search_requested)

        # Input styling
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px 12px;
                border: 2px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
                background-color: {theme_manager.get_color('surface')};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {theme_manager.get_color('primary')};
            }}
        """)

        main_layout.addWidget(self.search_input)

        # Suggestions dropdown
        self.suggestions_list = QListWidget()
        self.suggestions_list.setMaximumHeight(200)
        self.suggestions_list.hide()
        self.suggestions_list.itemClicked.connect(self._on_suggestion_clicked)

        # Suggestions styling
        self.suggestions_list.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid {theme_manager.get_color('border')};
                border-top: none;
                border-radius: 0px 0px {theme_manager.get_border_radius('md')}px {theme_manager.get_border_radius('md')}px;
                background-color: {theme_manager.get_color('surface')};
            }}
            QListWidget::item {{
                padding: 8px 12px;
                border-bottom: 1px solid {theme_manager.get_color('border')};
            }}
            QListWidget::item:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
            QListWidget::item:selected {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
            }}
        """)

        main_layout.addWidget(self.suggestions_list)

        # Search delay timer
        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._perform_search)

        # Handle focus events
        self.search_input.focusOutEvent = self._on_focus_out

    def _on_text_changed(self, text: str):
        """Handle text change in search input."""
        self.text_changed.emit(text)

        # Filter suggestions
        self._filter_suggestions(text)

        # Start search timer
        self._search_timer.stop()
        if len(text) >= self._min_chars:
            self._search_timer.start(self._search_delay)
        else:
            self.suggestions_list.hide()

    def _filter_suggestions(self, query: str):
        """Filter suggestions based on query."""
        if not query or len(query) < self._min_chars:
            self.suggestions_list.hide()
            return

        # Filter suggestions
        query_lower = query.lower()
        self._filtered_suggestions = [
            suggestion for suggestion in self._suggestions
            if query_lower in suggestion.lower()
        ][:self._max_suggestions]

        # Update suggestions list
        self._update_suggestions_display()

    def _update_suggestions_display(self):
        """Update the suggestions dropdown."""
        self.suggestions_list.clear()

        if not self._filtered_suggestions:
            self.suggestions_list.hide()
            return

        # Add suggestions to list
        for suggestion in self._filtered_suggestions:
            item = QListWidgetItem(suggestion)
            self.suggestions_list.addItem(item)

        # Show suggestions
        self.suggestions_list.show()

        # Adjust height based on items
        item_height = 32  # Approximate item height
        total_height = min(len(self._filtered_suggestions) * item_height, 200)
        self.suggestions_list.setMaximumHeight(total_height)

    def _on_suggestion_clicked(self, item: QListWidgetItem):
        """Handle suggestion selection."""
        suggestion = item.text()
        self.search_input.setText(suggestion)
        self.suggestions_list.hide()
        self.suggestion_selected.emit(suggestion)

    def _on_search_requested(self):
        """Handle search request (Enter pressed)."""
        query = self.search_input.text().strip()
        if query:
            self.suggestions_list.hide()
            self.search_requested.emit(query)

    def _on_focus_out(self, event):
        """Handle focus out to hide suggestions."""
        # Delay hiding to allow clicking on suggestions
        QTimer.singleShot(150, self.suggestions_list.hide)
        QLineEdit.focusOutEvent(self.search_input, event)

    def _perform_search(self):
        """Perform search with current text."""
        query = self.search_input.text().strip()
        if query and len(query) >= self._min_chars:
            self.search_requested.emit(query)

    def set_suggestions(self, suggestions: list):
        """Set available suggestions."""
        self._suggestions = suggestions

    def add_suggestion(self, suggestion: str):
        """Add single suggestion."""
        if suggestion not in self._suggestions:
            self._suggestions.append(suggestion)

    def clear_suggestions(self):
        """Clear all suggestions."""
        self._suggestions.clear()
        self.suggestions_list.hide()

    def set_placeholder(self, placeholder: str):
        """Update placeholder text."""
        self._placeholder = placeholder
        self.search_input.setPlaceholderText(placeholder)

    def set_max_suggestions(self, max_count: int):
        """Set maximum number of suggestions to show."""
        self._max_suggestions = max_count

    def set_min_chars(self, min_chars: int):
        """Set minimum characters before showing suggestions."""
        self._min_chars = min_chars

    def set_search_delay(self, delay_ms: int):
        """Set delay before triggering search."""
        self._search_delay = delay_ms

    def get_text(self) -> str:
        """Get current search text."""
        return self.search_input.text()

    def set_text(self, text: str):
        """Set search text."""
        self.search_input.setText(text)

    def clear(self):
        """Clear search text."""
        self.search_input.clear()
        self.suggestions_list.hide()


class AdvancedSearchBox(SearchBoxWithSuggestions):
    """Search box with advanced features like recent searches."""

    def __init__(self, placeholder="Search...", parent=None):
        super().__init__(placeholder, parent)
        self._recent_searches = []
        self._max_recent = 5
        self._show_recent = True

    def _filter_suggestions(self, query: str):
        """Override to include recent searches."""
        if not query:
            if self._show_recent and self._recent_searches:
                self._show_recent_searches()
            else:
                self.suggestions_list.hide()
            return

        # Regular suggestion filtering
        super()._filter_suggestions(query)

    def _show_recent_searches(self):
        """Show recent searches when input is empty."""
        self.suggestions_list.clear()

        if not self._recent_searches:
            self.suggestions_list.hide()
            return

        # Add "Recent searches" header
        header_item = QListWidgetItem("Recent searches")
        header_item.setFlags(header_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        header_font = theme_manager.get_font('caption')
        header_font.setWeight(QFont.Weight.Bold)
        header_item.setFont(header_font)
        self.suggestions_list.addItem(header_item)

        # Add recent searches
        for search in self._recent_searches:
            item = QListWidgetItem(f"🕐 {search}")
            self.suggestions_list.addItem(item)

        self.suggestions_list.show()

    def _on_search_requested(self):
        """Override to save to recent searches."""
        query = self.search_input.text().strip()
        if query:
            self._add_to_recent(query)

        super()._on_search_requested()

    def _add_to_recent(self, query: str):
        """Add query to recent searches."""
        # Remove if already exists
        if query in self._recent_searches:
            self._recent_searches.remove(query)

        # Add to front
        self._recent_searches.insert(0, query)

        # Limit size
        self._recent_searches = self._recent_searches[:self._max_recent]

    def clear_recent_searches(self):
        """Clear recent searches."""
        self._recent_searches.clear()

    def get_recent_searches(self) -> list:
        """Get recent searches list."""
        return self._recent_searches.copy()


class CategorySearchBox(SearchBoxWithSuggestions):
    """Search box with category filtering."""

    category_changed = pyqtSignal(str)  # Emits selected category

    def __init__(self, placeholder="Search...", parent=None):
        super().__init__(placeholder, parent)
        self._categories = {}  # category -> suggestions mapping
        self._current_category = "all"
        self._setup_category_ui()

    def _setup_category_ui(self):
        """Add category selection to UI."""
        from PyQt6.QtWidgets import QComboBox, QHBoxLayout

        # Create container for input and category
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(0)

        # Category selector
        self.category_combo = QComboBox()
        self.category_combo.addItem("All Categories", "all")
        self.category_combo.currentTextChanged.connect(self._on_category_changed)
        self.category_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 8px 12px;
                border: 2px solid {theme_manager.get_color('border')};
                border-right: none;
                border-radius: {theme_manager.get_border_radius('md')}px 0px 0px {theme_manager.get_border_radius('md')}px;
                background-color: {theme_manager.get_color('light')};
                min-width: 120px;
            }}
        """)

        input_layout.addWidget(self.category_combo)

        # Update search input styling for connected appearance
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px 12px;
                border: 2px solid {theme_manager.get_color('border')};
                border-left: none;
                border-radius: 0px {theme_manager.get_border_radius('md')}px {theme_manager.get_border_radius('md')}px 0px;
                background-color: {theme_manager.get_color('surface')};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {theme_manager.get_color('primary')};
            }}
        """)

        input_layout.addWidget(self.search_input)

        # Replace search input in main layout
        self.layout().replaceWidget(self.search_input, input_container)

    def add_category(self, category_name: str, suggestions: list):
        """Add category with its suggestions."""
        self._categories[category_name] = suggestions
        self.category_combo.addItem(category_name, category_name.lower())

    def _on_category_changed(self, category_text: str):
        """Handle category selection change."""
        category_data = self.category_combo.currentData()
        self._current_category = category_data

        # Update suggestions based on category
        if category_data == "all":
            all_suggestions = []
            for suggestions in self._categories.values():
                all_suggestions.extend(suggestions)
            self.set_suggestions(all_suggestions)
        else:
            category_suggestions = self._categories.get(category_text, [])
            self.set_suggestions(category_suggestions)

        self.category_changed.emit(category_data)

        # Re-filter current text
        current_text = self.search_input.text()
        if current_text:
            self._filter_suggestions(current_text)


class SearchBoxWithHistory(SearchBoxWithSuggestions):
    """Search box that maintains search history."""

    def __init__(self, placeholder="Search...", parent=None):
        super().__init__(placeholder, parent)
        self._search_history = []
        self._max_history = 20

    def _on_search_requested(self):
        """Override to save search history."""
        query = self.search_input.text().strip()
        if query:
            self._add_to_history(query)

        super()._on_search_requested()

    def _add_to_history(self, query: str):
        """Add query to search history."""
        # Remove if already exists
        if query in self._search_history:
            self._search_history.remove(query)

        # Add to front
        self._search_history.insert(0, query)

        # Limit size
        self._search_history = self._search_history[:self._max_history]

    def get_search_history(self) -> list:
        """Get search history."""
        return self._search_history.copy()

    def clear_history(self):
        """Clear search history."""
        self._search_history.clear()

    def load_history(self, history: list):
        """Load search history from external source."""
        self._search_history = history[:self._max_history]