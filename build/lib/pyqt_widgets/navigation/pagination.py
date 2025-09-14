"""
Pagination widget with numeric, infinite scroll, and load-more modes.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ..base.theme_manager import theme_manager
from ..base.base_button import BaseButton


class PaginationWidget(QWidget):
    """Pagination widget with multiple display modes."""

    page_changed = pyqtSignal(int)  # Emits new page number
    load_more_requested = pyqtSignal()  # For load-more mode

    def __init__(self, mode="numeric", total_pages=1, current_page=1,
                 max_visible_pages=7, parent=None):
        super().__init__(parent)
        self._mode = mode  # "numeric", "simple", "load_more"
        self._total_pages = total_pages
        self._current_page = current_page
        self._max_visible_pages = max_visible_pages
        self._page_buttons = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup the pagination UI."""
        self.setStyleSheet(f"""
            PaginationWidget {{
                background-color: {theme_manager.get_color('background')};
            }}
        """)

        # Main layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(4)

        if self._mode == "numeric":
            self._setup_numeric_pagination()
        elif self._mode == "simple":
            self._setup_simple_pagination()
        elif self._mode == "load_more":
            self._setup_load_more_pagination()

    def _setup_numeric_pagination(self):
        """Setup numeric pagination with page numbers."""
        # Previous button
        self.prev_btn = BaseButton("‹", "ghost", "small")
        self.prev_btn.setFixedSize(32, 32)
        self.prev_btn.clicked.connect(self._go_to_previous_page)
        self.main_layout.addWidget(self.prev_btn)

        # Page numbers container
        self.pages_container = QWidget()
        self.pages_layout = QHBoxLayout(self.pages_container)
        self.pages_layout.setContentsMargins(0, 0, 0, 0)
        self.pages_layout.setSpacing(2)
        self.main_layout.addWidget(self.pages_container)

        # Next button
        self.next_btn = BaseButton("›", "ghost", "small")
        self.next_btn.setFixedSize(32, 32)
        self.next_btn.clicked.connect(self._go_to_next_page)
        self.main_layout.addWidget(self.next_btn)

        # Page info label
        self.main_layout.addStretch()
        self.page_info_label = QLabel()
        self.page_info_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        self.page_info_label.setFont(theme_manager.get_font('caption'))
        self.main_layout.addWidget(self.page_info_label)

        self._update_numeric_pagination()

    def _setup_simple_pagination(self):
        """Setup simple pagination with just prev/next."""
        # Previous button with text
        self.prev_btn = BaseButton("← Previous", "secondary", "medium")
        self.prev_btn.clicked.connect(self._go_to_previous_page)
        self.main_layout.addWidget(self.prev_btn)

        self.main_layout.addStretch()

        # Page info
        self.page_info_label = QLabel()
        self.page_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_info_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        self.page_info_label.setFont(theme_manager.get_font('default'))
        self.main_layout.addWidget(self.page_info_label)

        self.main_layout.addStretch()

        # Next button with text
        self.next_btn = BaseButton("Next →", "secondary", "medium")
        self.next_btn.clicked.connect(self._go_to_next_page)
        self.main_layout.addWidget(self.next_btn)

        self._update_simple_pagination()

    def _setup_load_more_pagination(self):
        """Setup load-more pagination."""
        self.main_layout.addStretch()

        # Load more button
        self.load_more_btn = BaseButton("Load More", "primary", "medium")
        self.load_more_btn.clicked.connect(self._on_load_more)
        self.main_layout.addWidget(self.load_more_btn)

        self.main_layout.addStretch()

        # Items info
        self.items_info_label = QLabel("Showing items 1-20")
        self.items_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.items_info_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        self.items_info_label.setFont(theme_manager.get_font('caption'))

        # Add to vertical layout for centering
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.addWidget(self.load_more_btn)
        container_layout.addWidget(self.items_info_label)

        self.main_layout.addWidget(container)

    def _update_numeric_pagination(self):
        """Update numeric pagination display."""
        # Clear existing page buttons
        for button in self._page_buttons:
            button.setParent(None)
        self._page_buttons.clear()

        if self._total_pages <= 1:
            return

        # Calculate visible page range
        start_page, end_page = self._calculate_visible_range()

        # First page and ellipsis
        if start_page > 1:
            first_btn = self._create_page_button(1)
            self.pages_layout.addWidget(first_btn)
            self._page_buttons.append(first_btn)

            if start_page > 2:
                ellipsis_label = QLabel("...")
                ellipsis_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                ellipsis_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
                self.pages_layout.addWidget(ellipsis_label)
                self._page_buttons.append(ellipsis_label)

        # Visible page range
        for page in range(start_page, end_page + 1):
            page_btn = self._create_page_button(page)
            self.pages_layout.addWidget(page_btn)
            self._page_buttons.append(page_btn)

        # Last page and ellipsis
        if end_page < self._total_pages:
            if end_page < self._total_pages - 1:
                ellipsis_label = QLabel("...")
                ellipsis_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                ellipsis_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
                self.pages_layout.addWidget(ellipsis_label)
                self._page_buttons.append(ellipsis_label)

            last_btn = self._create_page_button(self._total_pages)
            self.pages_layout.addWidget(last_btn)
            self._page_buttons.append(last_btn)

        # Update navigation buttons
        self.prev_btn.setEnabled(self._current_page > 1)
        self.next_btn.setEnabled(self._current_page < self._total_pages)

        # Update page info
        self.page_info_label.setText(f"Page {self._current_page} of {self._total_pages}")

    def _calculate_visible_range(self):
        """Calculate the range of visible page numbers."""
        half_visible = self._max_visible_pages // 2

        start_page = max(1, self._current_page - half_visible)
        end_page = min(self._total_pages, self._current_page + half_visible)

        # Adjust if we're near the beginning or end
        if end_page - start_page + 1 < self._max_visible_pages:
            if start_page == 1:
                end_page = min(self._total_pages, start_page + self._max_visible_pages - 1)
            elif end_page == self._total_pages:
                start_page = max(1, end_page - self._max_visible_pages + 1)

        return start_page, end_page

    def _create_page_button(self, page_number: int) -> BaseButton:
        """Create a page number button."""
        is_current = (page_number == self._current_page)
        variant = "primary" if is_current else "ghost"

        btn = BaseButton(str(page_number), variant, "small")
        btn.setFixedSize(32, 32)

        if not is_current:
            btn.clicked.connect(lambda checked, page=page_number: self.set_current_page(page))
        else:
            btn.setEnabled(False)

        return btn

    def _update_simple_pagination(self):
        """Update simple pagination display."""
        self.prev_btn.setEnabled(self._current_page > 1)
        self.next_btn.setEnabled(self._current_page < self._total_pages)
        self.page_info_label.setText(f"Page {self._current_page} of {self._total_pages}")

    def _go_to_previous_page(self):
        """Go to previous page."""
        if self._current_page > 1:
            self.set_current_page(self._current_page - 1)

    def _go_to_next_page(self):
        """Go to next page."""
        if self._current_page < self._total_pages:
            self.set_current_page(self._current_page + 1)

    def _on_load_more(self):
        """Handle load more button click."""
        self.load_more_requested.emit()

    def set_current_page(self, page: int):
        """Set current page."""
        if 1 <= page <= self._total_pages and page != self._current_page:
            self._current_page = page

            if self._mode == "numeric":
                self._update_numeric_pagination()
            elif self._mode == "simple":
                self._update_simple_pagination()

            self.page_changed.emit(page)

    def set_total_pages(self, total_pages: int):
        """Set total number of pages."""
        self._total_pages = max(1, total_pages)

        # Adjust current page if necessary
        if self._current_page > self._total_pages:
            self._current_page = self._total_pages

        if self._mode == "numeric":
            self._update_numeric_pagination()
        elif self._mode == "simple":
            self._update_simple_pagination()

    def get_current_page(self) -> int:
        """Get current page number."""
        return self._current_page

    def get_total_pages(self) -> int:
        """Get total number of pages."""
        return self._total_pages

    def set_mode(self, mode: str):
        """Change pagination mode."""
        if mode != self._mode:
            self._mode = mode

            # Clear current layout
            for i in reversed(range(self.main_layout.count())):
                item = self.main_layout.itemAt(i)
                if item.widget():
                    item.widget().setParent(None)

            # Setup new mode
            self._setup_ui()

    def set_loading_state(self, loading: bool):
        """Set loading state for load-more mode."""
        if self._mode == "load_more" and hasattr(self, 'load_more_btn'):
            if loading:
                self.load_more_btn.set_loading(True)
                self.load_more_btn.setText("Loading...")
            else:
                self.load_more_btn.set_loading(False)
                self.load_more_btn.setText("Load More")

    def update_items_info(self, current_items: int, total_items: int = None):
        """Update items information for load-more mode."""
        if self._mode == "load_more" and hasattr(self, 'items_info_label'):
            if total_items:
                text = f"Showing {current_items} of {total_items} items"
            else:
                text = f"Showing {current_items} items"
            self.items_info_label.setText(text)


class InfiniteScrollPagination(PaginationWidget):
    """Pagination for infinite scroll scenarios."""

    def __init__(self, parent=None):
        super().__init__("load_more", parent=parent)
        self._items_per_page = 20
        self._current_items = 0
        self._total_items = None

    def add_items(self, count: int):
        """Add items to the current count."""
        self._current_items += count
        self.update_items_info(self._current_items, self._total_items)

    def set_total_items(self, total: int):
        """Set total number of items."""
        self._total_items = total
        self.update_items_info(self._current_items, self._total_items)

        # Hide load more button if all items are loaded
        if hasattr(self, 'load_more_btn'):
            if self._current_items >= self._total_items:
                self.load_more_btn.hide()
            else:
                self.load_more_btn.show()

    def reset(self):
        """Reset pagination state."""
        self._current_items = 0
        self._total_items = None
        self.update_items_info(0)
        if hasattr(self, 'load_more_btn'):
            self.load_more_btn.show()


class CompactPagination(PaginationWidget):
    """Compact pagination for small spaces."""

    def __init__(self, total_pages=1, current_page=1, parent=None):
        super().__init__("simple", total_pages, current_page, parent=parent)
        self._setup_compact_styling()

    def _setup_compact_styling(self):
        """Apply compact styling."""
        # Make buttons smaller
        if hasattr(self, 'prev_btn'):
            self.prev_btn.set_size("small")
            self.prev_btn.setText("‹")

        if hasattr(self, 'next_btn'):
            self.next_btn.set_size("small")
            self.next_btn.setText("›")

        # Smaller font for page info
        if hasattr(self, 'page_info_label'):
            self.page_info_label.setFont(theme_manager.get_font('caption'))