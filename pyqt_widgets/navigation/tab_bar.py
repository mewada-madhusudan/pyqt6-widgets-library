"""
Tab bar widget with close buttons and overflow handling.
"""

from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
                             QLabel, QScrollArea, QFrame, QMenu)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon
from ..base.theme_manager import theme_manager
from ..base.base_button import BaseButton


class TabBarWidget(QWidget):
    """Tab bar with closeable tabs and overflow handling."""

    tab_clicked = pyqtSignal(int, str)  # Emits index and tab name
    tab_closed = pyqtSignal(int, str)  # Emits index and tab name
    tab_added = pyqtSignal(int, str)  # Emits index and tab name

    def __init__(self, closeable=True, scrollable=True, parent=None):
        super().__init__(parent)
        self._closeable = closeable
        self._scrollable = scrollable
        self._tabs = []
        self._active_tab = -1
        self._setup_ui()

    def _setup_ui(self):
        """Setup the tab bar UI."""
        self.setStyleSheet(f"""
            TabBarWidget {{
                background-color: {theme_manager.get_color('background')};
                border-bottom: 1px solid {theme_manager.get_color('border')};
            }}
        """)

        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        if self._scrollable:
            # Scrollable tab container
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            scroll_area.setFrameShape(QFrame.Shape.NoFrame)
            scroll_area.setStyleSheet("QScrollArea { border: none; }")

            # Tab container widget
            self.tab_container = QWidget()
            self.tab_layout = QHBoxLayout(self.tab_container)
            self.tab_layout.setContentsMargins(0, 0, 0, 0)
            self.tab_layout.setSpacing(0)
            self.tab_layout.addStretch()

            scroll_area.setWidget(self.tab_container)
            main_layout.addWidget(scroll_area)
        else:
            # Direct tab layout
            self.tab_layout = QHBoxLayout()
            self.tab_layout.setContentsMargins(0, 0, 0, 0)
            self.tab_layout.setSpacing(0)
            main_layout.addLayout(self.tab_layout)

        # Add new tab button
        self.add_tab_btn = QPushButton("+")
        self.add_tab_btn.setFixedSize(32, 32)
        self.add_tab_btn.setFlat(True)
        self.add_tab_btn.clicked.connect(self._on_add_tab)
        self.add_tab_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-color: transparent;
                color: {theme_manager.get_color('text_secondary')};
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
                color: {theme_manager.get_color('text')};
            }}
        """)
        main_layout.addWidget(self.add_tab_btn)

    def add_tab(self, name: str, icon: QIcon = None, closeable: bool = None):
        """Add a new tab."""
        if closeable is None:
            closeable = self._closeable

        tab_index = len(self._tabs)

        # Create tab widget
        tab_widget = QWidget()
        tab_layout = QHBoxLayout(tab_widget)
        tab_layout.setContentsMargins(12, 8, 8 if closeable else 12, 8)
        tab_layout.setSpacing(8)

        # Icon
        if icon:
            icon_label = QLabel()
            icon_label.setPixmap(icon.pixmap(16, 16))
            icon_label.setFixedSize(16, 16)
            tab_layout.addWidget(icon_label)

        # Tab name button
        name_btn = QPushButton(name)
        name_btn.setFlat(True)
        name_btn.clicked.connect(lambda checked, idx=tab_index: self._on_tab_clicked(idx))
        name_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-color: transparent;
                color: {theme_manager.get_color('text')};
                text-align: left;
                padding: 0px;
            }}
            QPushButton:hover {{
                color: {theme_manager.get_color('primary')};
            }}
        """)
        tab_layout.addWidget(name_btn)

        # Close button
        close_btn = None
        if closeable:
            close_btn = QPushButton("×")
            close_btn.setFixedSize(16, 16)
            close_btn.setFlat(True)
            close_btn.clicked.connect(lambda checked, idx=tab_index: self._on_tab_closed(idx))
            close_btn.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background-color: transparent;
                    color: {theme_manager.get_color('text_secondary')};
                    font-size: 12px;
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    background-color: {theme_manager.get_color('danger')};
                    color: white;
                }}
            """)
            tab_layout.addWidget(close_btn)

        # Tab styling
        tab_widget.setStyleSheet(f"""
            QWidget {{
                border: none;
                border-bottom: 2px solid transparent;
                background-color: transparent;
            }}
            QWidget:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)

        # Store tab info
        tab_info = {
            'widget': tab_widget,
            'name': name,
            'name_btn': name_btn,
            'close_btn': close_btn,
            'icon': icon,
            'closeable': closeable
        }
        self._tabs.append(tab_info)

        # Add to layout
        if self._scrollable:
            self.tab_layout.insertWidget(self.tab_layout.count() - 1, tab_widget)
        else:
            self.tab_layout.addWidget(tab_widget)

        # Set as active if first tab
        if len(self._tabs) == 1:
            self.set_active_tab(0)

        self.tab_added.emit(tab_index, name)
        return tab_index

    def _on_tab_clicked(self, index: int):
        """Handle tab click."""
        self.set_active_tab(index)

    def _on_tab_closed(self, index: int):
        """Handle tab close."""
        self.close_tab(index)

    def _on_add_tab(self):
        """Handle add tab button click."""
        # Default new tab
        tab_count = len(self._tabs)
        self.add_tab(f"Tab {tab_count + 1}")

    def close_tab(self, index: int):
        """Close a tab by index."""
        if 0 <= index < len(self._tabs):
            tab_info = self._tabs[index]
            tab_name = tab_info['name']

            # Remove widget
            tab_info['widget'].setParent(None)

            # Remove from list
            del self._tabs[index]

            # Update active tab
            if self._active_tab == index:
                if self._tabs:
                    # Set previous tab as active, or first if closing first tab
                    new_active = max(0, index - 1)
                    self.set_active_tab(new_active)
                else:
                    self._active_tab = -1
            elif self._active_tab > index:
                self._active_tab -= 1

            # Update tab indices in click handlers
            self._update_tab_indices()

            self.tab_closed.emit(index, tab_name)

    def _update_tab_indices(self):
        """Update tab click handler indices after tab removal."""
        for i, tab_info in enumerate(self._tabs):
            # Reconnect with correct index
            tab_info['name_btn'].clicked.disconnect()
            tab_info['name_btn'].clicked.connect(lambda checked, idx=i: self._on_tab_clicked(idx))

            if tab_info['close_btn']:
                tab_info['close_btn'].clicked.disconnect()
                tab_info['close_btn'].clicked.connect(lambda checked, idx=i: self._on_tab_closed(idx))

    def set_active_tab(self, index: int):
        """Set active tab by index."""
        if not (0 <= index < len(self._tabs)):
            return

        # Remove active styling from previous tab
        if 0 <= self._active_tab < len(self._tabs):
            self._tabs[self._active_tab]['widget'].setStyleSheet(f"""
                QWidget {{
                    border: none;
                    border-bottom: 2px solid transparent;
                    background-color: transparent;
                }}
                QWidget:hover {{
                    background-color: {theme_manager.get_color('hover')};
                }}
            """)

        # Apply active styling to new tab
        self._active_tab = index
        self._tabs[index]['widget'].setStyleSheet(f"""
            QWidget {{
                border: none;
                border-bottom: 2px solid {theme_manager.get_color('primary')};
                background-color: {theme_manager.get_color('surface')};
            }}
        """)

        self.tab_clicked.emit(index, self._tabs[index]['name'])

    def get_active_tab(self) -> int:
        """Get active tab index."""
        return self._active_tab

    def get_tab_count(self) -> int:
        """Get number of tabs."""
        return len(self._tabs)

    def get_tab_name(self, index: int) -> str:
        """Get tab name by index."""
        if 0 <= index < len(self._tabs):
            return self._tabs[index]['name']
        return ""

    def set_tab_name(self, index: int, name: str):
        """Set tab name by index."""
        if 0 <= index < len(self._tabs):
            self._tabs[index]['name'] = name
            self._tabs[index]['name_btn'].setText(name)

    def set_tab_icon(self, index: int, icon: QIcon):
        """Set tab icon by index."""
        if 0 <= index < len(self._tabs):
            self._tabs[index]['icon'] = icon
            # Update icon in layout - would need to rebuild tab

    def clear_tabs(self):
        """Remove all tabs."""
        for i in reversed(range(len(self._tabs))):
            self.close_tab(i)


class VerticalTabBar(TabBarWidget):
    """Vertical tab bar widget."""

    def __init__(self, closeable=True, parent=None):
        super().__init__(closeable, False, parent)  # No horizontal scrolling for vertical
        self._setup_vertical_ui()

    def _setup_vertical_ui(self):
        """Setup vertical tab bar UI."""
        # Clear horizontal layout and create vertical
        self.setParent(None)

        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Tab container
        self.tab_container = QWidget()
        self.tab_layout = QVBoxLayout(self.tab_container)
        self.tab_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_layout.setSpacing(2)
        self.tab_layout.addStretch()

        main_layout.addWidget(self.tab_container)

        # Add tab button at bottom
        self.add_tab_btn.setParent(None)
        main_layout.addWidget(self.add_tab_btn)


class TabbedContainer(QWidget):
    """Container widget with integrated tab bar and content area."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._content_widgets = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup tabbed container UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Tab bar
        self.tab_bar = TabBarWidget()
        self.tab_bar.tab_clicked.connect(self._on_tab_changed)
        self.tab_bar.tab_closed.connect(self._on_tab_closed)
        layout.addWidget(self.tab_bar)

        # Content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.content_area)

    def add_tab(self, name: str, widget: QWidget, icon: QIcon = None):
        """Add tab with associated widget."""
        tab_index = self.tab_bar.add_tab(name, icon)
        self._content_widgets[tab_index] = widget

        # Hide widget initially
        widget.hide()
        self.content_layout.addWidget(widget)

        return tab_index

    def _on_tab_changed(self, index: int, name: str):
        """Handle tab change."""
        # Hide all content widgets
        for widget in self._content_widgets.values():
            widget.hide()

        # Show selected widget
        if index in self._content_widgets:
            self._content_widgets[index].show()

    def _on_tab_closed(self, index: int, name: str):
        """Handle tab close."""
        if index in self._content_widgets:
            widget = self._content_widgets[index]
            widget.setParent(None)
            del self._content_widgets[index]

        # Update indices
        new_content_widgets = {}
        for old_index, widget in self._content_widgets.items():
            new_index = old_index if old_index < index else old_index - 1
            new_content_widgets[new_index] = widget
        self._content_widgets = new_content_widgets