"""
Breadcrumb navigation widget with clickable trail.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ..base.theme_manager import theme_manager


class BreadcrumbBarWidget(QWidget):
    """Breadcrumb navigation showing hierarchical path."""

    breadcrumb_clicked = pyqtSignal(int, str)  # Emits index and path segment

    def __init__(self, separator=" > ", max_items=5, parent=None):
        super().__init__(parent)
        self._separator = separator
        self._max_items = max_items
        self._paths = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup the breadcrumb UI."""
        self.setStyleSheet(f"""
            BreadcrumbBarWidget {{
                background-color: {theme_manager.get_color('background')};
                border-bottom: 1px solid {theme_manager.get_color('border')};
            }}
        """)

        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(12, 8, 12, 8)
        main_layout.setSpacing(0)

        # Scrollable area for long breadcrumbs
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(scroll_area.Shape.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        # Content widget
        self.content_widget = QWidget()
        self.content_layout = QHBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(4)
        self.content_layout.addStretch()

        scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(scroll_area)

    def set_paths(self, paths: list):
        """Set the breadcrumb paths."""
        self._paths = paths
        self._update_breadcrumbs()

    def add_path(self, path: str):
        """Add a new path segment."""
        self._paths.append(path)
        self._update_breadcrumbs()

    def remove_last_path(self):
        """Remove the last path segment."""
        if self._paths:
            self._paths.pop()
            self._update_breadcrumbs()

    def clear_paths(self):
        """Clear all paths."""
        self._paths.clear()
        self._update_breadcrumbs()

    def _update_breadcrumbs(self):
        """Update the breadcrumb display."""
        # Clear existing widgets
        for i in reversed(range(self.content_layout.count())):
            item = self.content_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        if not self._paths:
            return

        # Determine which paths to show
        display_paths = self._paths
        start_index = 0

        if len(self._paths) > self._max_items:
            # Show first, ellipsis, and last few items
            display_paths = [self._paths[0], "...", *self._paths[-(self._max_items - 2):]]
            start_index = 0

        # Create breadcrumb items
        for i, path in enumerate(display_paths):
            if path == "...":
                # Ellipsis indicator
                ellipsis_label = QLabel("...")
                ellipsis_label.setStyleSheet(f"""
                    QLabel {{
                        color: {theme_manager.get_color('text_secondary')};
                        padding: 4px 8px;
                    }}
                """)
                self.content_layout.insertWidget(self.content_layout.count() - 1, ellipsis_label)
            else:
                # Calculate actual index in original paths
                if len(self._paths) > self._max_items and i > 1:
                    actual_index = len(self._paths) - (len(display_paths) - i)
                else:
                    actual_index = i if i < len(self._paths) else len(self._paths) - 1

                # Create breadcrumb button
                is_last = (i == len(display_paths) - 1)
                breadcrumb_btn = self._create_breadcrumb_item(path, actual_index, is_last)
                self.content_layout.insertWidget(self.content_layout.count() - 1, breadcrumb_btn)

            # Add separator (except for last item)
            if i < len(display_paths) - 1:
                separator_label = QLabel(self._separator)
                separator_label.setStyleSheet(f"""
                    QLabel {{
                        color: {theme_manager.get_color('text_secondary')};
                        padding: 0px 4px;
                    }}
                """)
                self.content_layout.insertWidget(self.content_layout.count() - 1, separator_label)

    def _create_breadcrumb_item(self, text: str, index: int, is_last: bool):
        """Create a breadcrumb item widget."""
        if is_last:
            # Last item is not clickable
            label = QLabel(text)
            label.setFont(theme_manager.get_font('default'))
            label.setStyleSheet(f"""
                QLabel {{
                    color: {theme_manager.get_color('text')};
                    padding: 4px 8px;
                    font-weight: bold;
                }}
            """)
            return label
        else:
            # Clickable breadcrumb button
            button = QPushButton(text)
            button.setFlat(True)
            button.clicked.connect(lambda checked, idx=index, txt=text: self.breadcrumb_clicked.emit(idx, txt))
            button.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background-color: transparent;
                    color: {theme_manager.get_color('primary')};
                    padding: 4px 8px;
                    text-align: left;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: {theme_manager.get_color('hover')};
                    color: {theme_manager.get_color('text')};
                }}
            """)
            return button

    def navigate_to_index(self, index: int):
        """Navigate to a specific breadcrumb index."""
        if 0 <= index < len(self._paths):
            # Remove paths after the clicked index
            self._paths = self._paths[:index + 1]
            self._update_breadcrumbs()

    def get_current_path(self) -> str:
        """Get the current (last) path."""
        return self._paths[-1] if self._paths else ""

    def get_full_path(self, separator: str = "/") -> str:
        """Get the full path as a string."""
        return separator.join(self._paths)

    def get_paths(self) -> list:
        """Get all path segments."""
        return self._paths.copy()

    def set_separator(self, separator: str):
        """Change the separator character."""
        self._separator = separator
        self._update_breadcrumbs()

    def set_max_items(self, max_items: int):
        """Set maximum number of visible items."""
        self._max_items = max_items
        self._update_breadcrumbs()


class FileBreadcrumbBar(BreadcrumbBarWidget):
    """Breadcrumb bar specifically for file paths."""

    def __init__(self, parent=None):
        super().__init__(separator=" / ", parent=parent)

    def set_file_path(self, file_path: str):
        """Set breadcrumb from file path."""
        import os
        path_parts = []

        # Normalize path and split
        normalized_path = os.path.normpath(file_path)
        parts = normalized_path.split(os.sep)

        # Filter out empty parts
        parts = [part for part in parts if part]

        # Add drive letter on Windows
        if os.name == 'nt' and parts and ':' in parts[0]:
            parts[0] = parts[0] + os.sep

        self.set_paths(parts)

    def get_file_path(self) -> str:
        """Get the current path as a file path."""
        import os
        return os.sep.join(self._paths)


class WebBreadcrumbBar(BreadcrumbBarWidget):
    """Breadcrumb bar for web navigation."""

    def __init__(self, parent=None):
        super().__init__(separator=" › ", parent=parent)

    def set_url_path(self, url: str):
        """Set breadcrumb from URL path."""
        from urllib.parse import urlparse

        parsed_url = urlparse(url)
        path_parts = [part for part in parsed_url.path.split('/') if part]

        # Add domain as first item
        if parsed_url.netloc:
            path_parts.insert(0, parsed_url.netloc)

        self.set_paths(path_parts)

    def get_url_path(self) -> str:
        """Get the current path as URL."""
        if not self._paths:
            return ""

        domain = self._paths[0] if self._paths else ""
        path_parts = self._paths[1:] if len(self._paths) > 1 else []

        if path_parts:
            return f"https://{domain}/" + "/".join(path_parts)
        else:
            return f"https://{domain}"


class CustomizableBreadcrumb(BreadcrumbBarWidget):
    """Breadcrumb with customizable styling and icons."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._icons = {}

    def set_path_icon(self, path: str, icon):
        """Set icon for specific path."""
        self._icons[path] = icon
        self._update_breadcrumbs()

    def _create_breadcrumb_item(self, text: str, index: int, is_last: bool):
        """Override to add icons."""
        from PyQt6.QtWidgets import QHBoxLayout

        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # Add icon if available
        if text in self._icons:
            icon_label = QLabel()
            icon_label.setPixmap(self._icons[text].pixmap(16, 16))
            layout.addWidget(icon_label)

        # Add text
        if is_last:
            label = QLabel(text)
            label.setStyleSheet(f"""
                QLabel {{
                    color: {theme_manager.get_color('text')};
                    font-weight: bold;
                }}
            """)
            layout.addWidget(label)
        else:
            button = QPushButton(text)
            button.setFlat(True)
            button.clicked.connect(lambda checked, idx=index, txt=text: self.breadcrumb_clicked.emit(idx, txt))
            button.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background-color: transparent;
                    color: {theme_manager.get_color('primary')};
                    text-align: left;
                }}
                QPushButton:hover {{
                    color: {theme_manager.get_color('text')};
                }}
            """)
            layout.addWidget(button)

        return widget