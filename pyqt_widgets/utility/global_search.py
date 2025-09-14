"""
Global search widget with autocomplete and filtering.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QListWidget, QListWidgetItem, QPushButton, QLabel,
                             QFrame, QComboBox, QCheckBox, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QThread, pyqtSlot
from PyQt6.QtGui import QFont, QKeyEvent
from ..base.theme_manager import theme_manager
from typing import List, Dict, Any, Callable
import re


class GlobalSearchWidget(QWidget):
    """Global search interface with autocomplete and filtering."""

    search_performed = pyqtSignal(str, dict)  # query, filters
    result_selected = pyqtSignal(dict)  # selected result
    search_cleared = pyqtSignal()

    def __init__(self, placeholder="Search everything...", parent=None):
        super().__init__(parent)
        self._placeholder = placeholder
        self._search_providers = {}  # name -> search function
        self._results = []
        self._current_query = ""
        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._perform_search)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the global search UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Search input area
        search_frame = QFrame()
        search_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {theme_manager.get_color('surface')};
                border: 2px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}
            QFrame:focus-within {{
                border-color: {theme_manager.get_color('primary')};
            }}
        """)

        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(12, 8, 12, 8)
        search_layout.setSpacing(8)

        # Search icon/button
        self.search_icon = QLabel("🔍")
        self.search_icon.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        search_layout.addWidget(self.search_icon)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self._placeholder)
        self.search_input.setFrame(False)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                border: none;
                background: transparent;
                color: {theme_manager.get_color('text')};
                font-size: 12pt;
            }}
        """)
        self.search_input.textChanged.connect(self._on_search_text_changed)
        self.search_input.returnPressed.connect(self._perform_immediate_search)
        search_layout.addWidget(self.search_input)

        # Clear button
        self.clear_btn = QPushButton("×")
        self.clear_btn.setFixedSize(24, 24)
        self.clear_btn.clicked.connect(self.clear_search)
        self.clear_btn.hide()
        self.clear_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                border-radius: 12px;
                background-color: {theme_manager.get_color('text_secondary')};
                color: white;
                font-weight: bold;
                font-size: 14pt;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('danger')};
            }}
        """)
        search_layout.addWidget(self.clear_btn)

        layout.addWidget(search_frame)

        # Filters area
        self.filters_frame = self._create_filters_area()
        layout.addWidget(self.filters_frame)

        # Results area
        self.results_frame = self._create_results_area()
        layout.addWidget(self.results_frame)

        # Status bar
        self.status_label = QLabel("Type to search...")
        self.status_label.setFont(theme_manager.get_font('caption'))
        self.status_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        layout.addWidget(self.status_label)

    def _create_filters_area(self):
        """Create search filters area."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {theme_manager.get_color('background')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
            }}
        """)
        frame.hide()  # Hidden by default

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(8, 4, 8, 4)

        # Filter by type
        layout.addWidget(QLabel("Type:"))
        self.type_filter = QComboBox()
        self.type_filter.addItem("All", None)
        self.type_filter.currentDataChanged.connect(self._on_filter_changed)
        layout.addWidget(self.type_filter)

        # Case sensitive
        self.case_sensitive = QCheckBox("Case sensitive")
        self.case_sensitive.toggled.connect(self._on_filter_changed)
        layout.addWidget(self.case_sensitive)

        # Whole words
        self.whole_words = QCheckBox("Whole words")
        self.whole_words.toggled.connect(self._on_filter_changed)
        layout.addWidget(self.whole_words)

        # Regex
        self.regex_mode = QCheckBox("Regex")
        self.regex_mode.toggled.connect(self._on_filter_changed)
        layout.addWidget(self.regex_mode)

        layout.addStretch()

        # Toggle filters button
        self.toggle_filters_btn = QPushButton("Filters")
        self.toggle_filters_btn.setCheckable(True)
        self.toggle_filters_btn.toggled.connect(self._toggle_filters)
        self.toggle_filters_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_manager.get_color('secondary')};
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: {theme_manager.get_border_radius('sm')}px;
                font-size: 8pt;
            }}
            QPushButton:checked {{
                background-color: {theme_manager.get_color('primary')};
            }}
        """)

        # Add toggle button before the frame
        return frame

    def _create_results_area(self):
        """Create search results area."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {theme_manager.get_color('background')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
            }}
        """)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)

        # Results header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(8, 4, 8, 4)

        self.results_label = QLabel("Results")
        self.results_label.setFont(theme_manager.get_font('heading'))
        header_layout.addWidget(self.results_label)

        header_layout.addStretch()

        # Add filters toggle here
        self.toggle_filters_btn = QPushButton("Filters")
        self.toggle_filters_btn.setCheckable(True)
        self.toggle_filters_btn.toggled.connect(self._toggle_filters)
        self.toggle_filters_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_manager.get_color('secondary')};
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: {theme_manager.get_border_radius('sm')}px;
                font-size: 8pt;
            }}
            QPushButton:checked {{
                background-color: {theme_manager.get_color('primary')};
            }}
        """)
        header_layout.addWidget(self.toggle_filters_btn)

        layout.addLayout(header_layout)

        # Results list
        self.results_list = QListWidget()
        self.results_list.itemClicked.connect(self._on_result_selected)
        self.results_list.setStyleSheet(f"""
            QListWidget {{
                border: none;
                background-color: transparent;
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
        layout.addWidget(self.results_list)

        return frame

    def _toggle_filters(self, show):
        """Toggle filters visibility."""
        if show:
            self.filters_frame.show()
        else:
            self.filters_frame.hide()

    def _on_search_text_changed(self, text):
        """Handle search text change."""
        self._current_query = text

        if text:
            self.clear_btn.show()
            self._search_timer.start(300)  # Debounce search
        else:
            self.clear_btn.hide()
            self.clear_search()

    def _on_filter_changed(self):
        """Handle filter change."""
        if self._current_query:
            self._perform_search()

    def _perform_immediate_search(self):
        """Perform search immediately."""
        self._search_timer.stop()
        self._perform_search()

    def _perform_search(self):
        """Perform the actual search."""
        query = self._current_query.strip()
        if not query:
            return

        # Get current filters
        filters = self._get_current_filters()

        # Clear previous results
        self.results_list.clear()
        self._results.clear()

        # Update status
        self.status_label.setText("Searching...")

        # Search through all providers
        total_results = 0
        for provider_name, search_func in self._search_providers.items():
            try:
                results = search_func(query, filters)
                if results:
                    for result in results:
                        result['provider'] = provider_name
                        self._results.append(result)
                        total_results += 1
            except Exception as e:
                print(f"Search error in {provider_name}: {e}")

        # Update results display
        self._update_results_display()

        # Update status
        self.status_label.setText(f"Found {total_results} results")

        # Emit search signal
        self.search_performed.emit(query, filters)

    def _get_current_filters(self) -> dict:
        """Get current filter settings."""
        return {
            'type': self.type_filter.currentData(),
            'case_sensitive': self.case_sensitive.isChecked(),
            'whole_words': self.whole_words.isChecked(),
            'regex': self.regex_mode.isChecked()
        }

    def _update_results_display(self):
        """Update results list display."""
        for result in self._results:
            item_widget = SearchResultItem(result)
            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())

            self.results_list.addItem(list_item)
            self.results_list.setItemWidget(list_item, item_widget)

    def _on_result_selected(self, item):
        """Handle result selection."""
        widget = self.results_list.itemWidget(item)
        if widget:
            result = widget.get_result()
            self.result_selected.emit(result)

    def clear_search(self):
        """Clear search and results."""
        self.search_input.clear()
        self.results_list.clear()
        self._results.clear()
        self._current_query = ""
        self.clear_btn.hide()
        self.status_label.setText("Type to search...")
        self.search_cleared.emit()

    def add_search_provider(self, name: str, search_func: Callable):
        """Add a search provider function."""
        self._search_providers[name] = search_func

        # Add to type filter
        self.type_filter.addItem(name.title(), name)

    def remove_search_provider(self, name: str):
        """Remove a search provider."""
        if name in self._search_providers:
            del self._search_providers[name]

            # Remove from type filter
            for i in range(self.type_filter.count()):
                if self.type_filter.itemData(i) == name:
                    self.type_filter.removeItem(i)
                    break

    def set_placeholder(self, placeholder: str):
        """Set search placeholder text."""
        self._placeholder = placeholder
        self.search_input.setPlaceholderText(placeholder)

    def focus_search(self):
        """Focus the search input."""
        self.search_input.setFocus()

    def get_results(self) -> List[Dict]:
        """Get current search results."""
        return self._results.copy()


class SearchResultItem(QWidget):
    """Individual search result item widget."""

    def __init__(self, result: dict, parent=None):
        super().__init__(parent)
        self._result = result
        self._setup_ui()

    def _setup_ui(self):
        """Setup result item UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        # Title
        title = self._result.get('title', 'Untitled')
        title_label = QLabel(title)
        title_label.setFont(theme_manager.get_font('default'))
        title_label.setStyleSheet(f"color: {theme_manager.get_color('text')}; font-weight: bold;")
        layout.addWidget(title_label)

        # Description/Content
        description = self._result.get('description', '')
        if description:
            desc_label = QLabel(description)
            desc_label.setFont(theme_manager.get_font('caption'))
            desc_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        # Metadata
        meta_layout = QHBoxLayout()

        # Type/Provider
        provider = self._result.get('provider', '')
        if provider:
            provider_label = QLabel(provider.upper())
            provider_label.setFont(theme_manager.get_font('caption'))
            provider_label.setStyleSheet(f"""
                color: {theme_manager.get_color('primary')};
                font-weight: bold;
                font-size: 7pt;
            """)
            meta_layout.addWidget(provider_label)

        meta_layout.addStretch()

        # Score/Relevance
        score = self._result.get('score', 0)
        if score > 0:
            score_label = QLabel(f"{score:.1f}%")
            score_label.setFont(theme_manager.get_font('caption'))
            score_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')}; font-size: 7pt;")
            meta_layout.addWidget(score_label)

        layout.addLayout(meta_layout)

    def get_result(self) -> dict:
        """Get result data."""
        return self._result


class SimpleGlobalSearch(QWidget):
    """Simplified global search widget."""

    search_performed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Setup simple search."""
        layout = QHBoxLayout(self)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.returnPressed.connect(self._perform_search)
        layout.addWidget(self.search_input)

        # Search button
        search_btn = QPushButton("🔍")
        search_btn.clicked.connect(self._perform_search)
        search_btn.setFixedSize(32, 32)
        layout.addWidget(search_btn)

    def _perform_search(self):
        """Perform search."""
        query = self.search_input.text().strip()
        if query:
            self.search_performed.emit(query)


# Example search providers
def file_search_provider(query: str, filters: dict) -> List[Dict]:
    """Example file search provider."""
    # This would typically search through files
    results = []

    # Mock results
    if 'file' in query.lower():
        results.append({
            'title': 'example.txt',
            'description': 'Text file containing example data',
            'type': 'file',
            'path': '/path/to/example.txt',
            'score': 95.0
        })

    return results


def content_search_provider(query: str, filters: dict) -> List[Dict]:
    """Example content search provider."""
    # This would typically search through content/documents
    results = []

    # Mock results
    if len(query) > 2:
        results.append({
            'title': f'Content matching "{query}"',
            'description': f'Found {len(query)} matches in various documents',
            'type': 'content',
            'matches': len(query),
            'score': 80.0
        })

    return results