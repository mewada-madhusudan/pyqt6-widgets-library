"""
Sidebar navigation widget with icons and grouping.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon
from ..base.theme_manager import theme_manager
from ..base.base_button import BaseButton


class SidebarNavWidget(QWidget):
    """Vertical sidebar navigation with icons and collapsible groups."""

    item_clicked = pyqtSignal(str)  # Emits item name
    group_toggled = pyqtSignal(str, bool)  # Emits group name and expanded state

    def __init__(self, collapsible=True, parent=None):
        super().__init__(parent)
        self._collapsible = collapsible
        self._collapsed = False
        self._groups = {}
        self._items = {}
        self._active_item = None
        self._setup_ui()

    def _setup_ui(self):
        """Setup the sidebar UI."""
        self.setFixedWidth(250)
        self.setStyleSheet(f"""
            SidebarNavWidget {{
                background-color: {theme_manager.get_color('surface')};
                border-right: 1px solid {theme_manager.get_color('border')};
            }}
        """)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header with collapse button
        if self._collapsible:
            header = QWidget()
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(12, 12, 12, 12)

            self.collapse_btn = QPushButton("☰")
            self.collapse_btn.setFixedSize(32, 32)
            self.collapse_btn.setFlat(True)
            self.collapse_btn.clicked.connect(self._toggle_collapse)
            self.collapse_btn.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background-color: transparent;
                    color: {theme_manager.get_color('text')};
                    font-size: 16px;
                }}
                QPushButton:hover {{
                    background-color: {theme_manager.get_color('hover')};
                    border-radius: 4px;
                }}
            """)
            header_layout.addWidget(self.collapse_btn)
            header_layout.addStretch()

            main_layout.addWidget(header)

        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(4)
        self.content_layout.addStretch()

        scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(scroll_area)

    def add_group(self, group_name: str, expanded: bool = True):
        """Add a collapsible group."""
        group_widget = QWidget()
        group_layout = QVBoxLayout(group_widget)
        group_layout.setContentsMargins(0, 0, 0, 0)
        group_layout.setSpacing(2)

        # Group header
        header_btn = QPushButton()
        header_btn.setFlat(True)
        header_btn.clicked.connect(lambda: self._toggle_group(group_name))

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(12, 8, 12, 8)

        # Expand/collapse arrow
        arrow_label = QLabel("▼" if expanded else "▶")
        arrow_label.setFixedSize(16, 16)
        arrow_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        header_layout.addWidget(arrow_label)

        # Group name
        name_label = QLabel(group_name)
        name_font = theme_manager.get_font('default')
        name_font.setWeight(QFont.Weight.Bold)
        name_label.setFont(name_font)
        name_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        header_layout.addWidget(name_label)

        header_layout.addStretch()
        header_btn.setLayout(header_layout)

        header_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-color: transparent;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)

        group_layout.addWidget(header_btn)

        # Group items container
        items_container = QWidget()
        items_layout = QVBoxLayout(items_container)
        items_layout.setContentsMargins(0, 0, 0, 0)
        items_layout.setSpacing(2)

        if not expanded:
            items_container.hide()

        group_layout.addWidget(items_container)

        # Store group info
        self._groups[group_name] = {
            'widget': group_widget,
            'header_btn': header_btn,
            'arrow_label': arrow_label,
            'items_container': items_container,
            'items_layout': items_layout,
            'expanded': expanded
        }

        # Insert before stretch
        self.content_layout.insertWidget(self.content_layout.count() - 1, group_widget)

    def add_item(self, item_name: str, icon: QIcon = None, group: str = None):
        """Add navigation item."""
        item_btn = QPushButton()
        item_btn.setFlat(True)
        item_btn.clicked.connect(lambda: self._on_item_clicked(item_name))

        item_layout = QHBoxLayout()
        item_layout.setContentsMargins(24 if group else 12, 8, 12, 8)
        item_layout.setSpacing(12)

        # Icon
        if icon:
            icon_label = QLabel()
            icon_label.setPixmap(icon.pixmap(20, 20))
            icon_label.setFixedSize(20, 20)
            item_layout.addWidget(icon_label)
        else:
            # Placeholder for alignment
            placeholder = QLabel()
            placeholder.setFixedSize(20, 20)
            item_layout.addWidget(placeholder)

        # Item name
        name_label = QLabel(item_name)
        name_label.setFont(theme_manager.get_font('default'))
        name_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        item_layout.addWidget(name_label)

        item_layout.addStretch()
        item_btn.setLayout(item_layout)

        item_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-color: transparent;
                text-align: left;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)

        # Store item info
        self._items[item_name] = {
            'button': item_btn,
            'group': group,
            'icon': icon
        }

        # Add to appropriate container
        if group and group in self._groups:
            self._groups[group]['items_layout'].addWidget(item_btn)
        else:
            # Add to main content
            self.content_layout.insertWidget(self.content_layout.count() - 1, item_btn)

    def _toggle_group(self, group_name: str):
        """Toggle group expansion."""
        if group_name not in self._groups:
            return

        group = self._groups[group_name]
        expanded = not group['expanded']
        group['expanded'] = expanded

        # Update arrow
        group['arrow_label'].setText("▼" if expanded else "▶")

        # Animate expansion/collapse
        if expanded:
            group['items_container'].show()
        else:
            group['items_container'].hide()

        self.group_toggled.emit(group_name, expanded)

    def _on_item_clicked(self, item_name: str):
        """Handle item click."""
        # Update active item styling
        if self._active_item and self._active_item in self._items:
            self._items[self._active_item]['button'].setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background-color: transparent;
                    text-align: left;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: {theme_manager.get_color('hover')};
                }}
            """)

        self._active_item = item_name
        if item_name in self._items:
            self._items[item_name]['button'].setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background-color: {theme_manager.get_color('primary')};
                    color: white;
                    text-align: left;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: {theme_manager.get_color('primary')};
                }}
            """)

        self.item_clicked.emit(item_name)

    def _toggle_collapse(self):
        """Toggle sidebar collapse state."""
        self._collapsed = not self._collapsed

        if self._collapsed:
            self.setFixedWidth(60)
            # Hide text labels, show only icons
            for item_info in self._items.values():
                # Hide text in buttons
                pass
        else:
            self.setFixedWidth(250)
            # Show full content

    def set_active_item(self, item_name: str):
        """Set active item programmatically."""
        self._on_item_clicked(item_name)

    def get_active_item(self) -> str:
        """Get currently active item."""
        return self._active_item

    def remove_item(self, item_name: str):
        """Remove navigation item."""
        if item_name in self._items:
            item_info = self._items[item_name]
            item_info['button'].setParent(None)
            del self._items[item_name]

            if self._active_item == item_name:
                self._active_item = None

    def remove_group(self, group_name: str):
        """Remove entire group and its items."""
        if group_name in self._groups:
            # Remove all items in group
            items_to_remove = [name for name, info in self._items.items() if info['group'] == group_name]
            for item_name in items_to_remove:
                self.remove_item(item_name)

            # Remove group widget
            group_info = self._groups[group_name]
            group_info['widget'].setParent(None)
            del self._groups[group_name]

    def clear(self):
        """Clear all items and groups."""
        for item_name in list(self._items.keys()):
            self.remove_item(item_name)

        for group_name in list(self._groups.keys()):
            self.remove_group(group_name)


class CompactSidebarNav(SidebarNavWidget):
    """Compact version of sidebar navigation."""

    def __init__(self, parent=None):
        super().__init__(False, parent)
        self.setFixedWidth(60)
        self._setup_compact_styling()

    def _setup_compact_styling(self):
        """Setup compact-specific styling."""
        # Override item layout to show only icons
        pass

    def add_item(self, item_name: str, icon: QIcon = None, tooltip: str = None):
        """Add item with tooltip for compact mode."""
        super().add_item(item_name, icon)

        if tooltip and item_name in self._items:
            self._items[item_name]['button'].setToolTip(tooltip or item_name)