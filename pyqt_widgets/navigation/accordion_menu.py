"""
Accordion menu widget with collapsible sections.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon
from ..base.theme_manager import theme_manager
from ..base.animation_helpers import AnimationHelpers


class AccordionMenuWidget(QWidget):
    """Accordion menu with collapsible sections."""

    section_toggled = pyqtSignal(str, bool)  # Emits section name and expanded state
    item_clicked = pyqtSignal(str, str)  # Emits section name and item name

    def __init__(self, allow_multiple=False, parent=None):
        super().__init__(parent)
        self._allow_multiple = allow_multiple
        self._sections = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup the accordion menu UI."""
        self.setStyleSheet(f"""
            AccordionMenuWidget {{
                background-color: {theme_manager.get_color('surface')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}
        """)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scrollable content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.content_layout.addStretch()

        scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(scroll_area)

    def add_section(self, section_name: str, expanded: bool = False, icon: QIcon = None):
        """Add a new accordion section."""
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(0)

        # Section header
        header_btn = QPushButton()
        header_btn.setFlat(True)
        header_btn.clicked.connect(lambda: self._toggle_section(section_name))

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(16, 12, 16, 12)
        header_layout.setSpacing(12)

        # Expand/collapse arrow
        arrow_label = QLabel("▼" if expanded else "▶")
        arrow_label.setFixedSize(12, 12)
        arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        arrow_label.setStyleSheet(f"""
            QLabel {{
                color: {theme_manager.get_color('text_secondary')};
                font-size: 10px;
            }}
        """)
        header_layout.addWidget(arrow_label)

        # Section icon
        if icon:
            icon_label = QLabel()
            icon_label.setPixmap(icon.pixmap(20, 20))
            icon_label.setFixedSize(20, 20)
            header_layout.addWidget(icon_label)

        # Section name
        name_label = QLabel(section_name)
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
                border-bottom: 1px solid {theme_manager.get_color('border')};
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)

        section_layout.addWidget(header_btn)

        # Section content container
        content_container = QWidget()
        content_container_layout = QVBoxLayout(content_container)
        content_container_layout.setContentsMargins(0, 0, 0, 0)
        content_container_layout.setSpacing(0)

        if not expanded:
            content_container.hide()

        section_layout.addWidget(content_container)

        # Store section info
        self._sections[section_name] = {
            'widget': section_widget,
            'header_btn': header_btn,
            'arrow_label': arrow_label,
            'content_container': content_container,
            'content_layout': content_container_layout,
            'expanded': expanded,
            'items': []
        }

        # Add to main layout
        self.content_layout.insertWidget(self.content_layout.count() - 1, section_widget)

    def add_item(self, section_name: str, item_name: str, icon: QIcon = None):
        """Add item to a section."""
        if section_name not in self._sections:
            return

        section = self._sections[section_name]

        # Create item button
        item_btn = QPushButton()
        item_btn.setFlat(True)
        item_btn.clicked.connect(lambda: self.item_clicked.emit(section_name, item_name))

        item_layout = QHBoxLayout()
        item_layout.setContentsMargins(32, 8, 16, 8)
        item_layout.setSpacing(12)

        # Item icon
        if icon:
            icon_label = QLabel()
            icon_label.setPixmap(icon.pixmap(16, 16))
            icon_label.setFixedSize(16, 16)
            item_layout.addWidget(icon_label)
        else:
            # Spacer for alignment
            spacer = QLabel()
            spacer.setFixedSize(16, 16)
            item_layout.addWidget(spacer)

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
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)

        # Add to section
        section['content_layout'].addWidget(item_btn)
        section['items'].append({
            'name': item_name,
            'button': item_btn,
            'icon': icon
        })

    def _toggle_section(self, section_name: str):
        """Toggle section expansion."""
        if section_name not in self._sections:
            return

        section = self._sections[section_name]
        expanded = not section['expanded']

        # Close other sections if not allowing multiple
        if expanded and not self._allow_multiple:
            for name, sec in self._sections.items():
                if name != section_name and sec['expanded']:
                    self._collapse_section(name)

        # Toggle current section
        if expanded:
            self._expand_section(section_name)
        else:
            self._collapse_section(section_name)

    def _expand_section(self, section_name: str):
        """Expand a section with animation."""
        if section_name not in self._sections:
            return

        section = self._sections[section_name]
        section['expanded'] = True

        # Update arrow
        section['arrow_label'].setText("▼")

        # Show content and animate
        content_container = section['content_container']
        content_container.show()

        # Measure target height
        content_container.adjustSize()
        target_height = content_container.sizeHint().height()

        # Animate expansion
        content_container.setFixedHeight(0)
        animation = QPropertyAnimation(content_container, b"maximumHeight")
        animation.setDuration(300)
        animation.setStartValue(0)
        animation.setEndValue(target_height)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        def on_expand_finished():
            content_container.setMaximumHeight(16777215)

        animation.finished.connect(on_expand_finished)
        animation.start()

        self.section_toggled.emit(section_name, True)

    def _collapse_section(self, section_name: str):
        """Collapse a section with animation."""
        if section_name not in self._sections:
            return

        section = self._sections[section_name]
        section['expanded'] = False

        # Update arrow
        section['arrow_label'].setText("▶")

        # Animate collapse
        content_container = section['content_container']
        current_height = content_container.height()

        animation = QPropertyAnimation(content_container, b"maximumHeight")
        animation.setDuration(300)
        animation.setStartValue(current_height)
        animation.setEndValue(0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        def on_collapse_finished():
            content_container.hide()

        animation.finished.connect(on_collapse_finished)
        animation.start()

        self.section_toggled.emit(section_name, False)

    def expand_section(self, section_name: str):
        """Expand section programmatically."""
        if section_name in self._sections and not self._sections[section_name]['expanded']:
            self._expand_section(section_name)

    def collapse_section(self, section_name: str):
        """Collapse section programmatically."""
        if section_name in self._sections and self._sections[section_name]['expanded']:
            self._collapse_section(section_name)

    def is_section_expanded(self, section_name: str) -> bool:
        """Check if section is expanded."""
        return self._sections.get(section_name, {}).get('expanded', False)

    def remove_section(self, section_name: str):
        """Remove a section."""
        if section_name in self._sections:
            section = self._sections[section_name]
            section['widget'].setParent(None)
            del self._sections[section_name]

    def remove_item(self, section_name: str, item_name: str):
        """Remove an item from a section."""
        if section_name not in self._sections:
            return

        section = self._sections[section_name]
        for i, item in enumerate(section['items']):
            if item['name'] == item_name:
                item['button'].setParent(None)
                del section['items'][i]
                break

    def clear_section(self, section_name: str):
        """Clear all items from a section."""
        if section_name not in self._sections:
            return

        section = self._sections[section_name]
        for item in section['items']:
            item['button'].setParent(None)
        section['items'].clear()

    def get_sections(self) -> list:
        """Get list of section names."""
        return list(self._sections.keys())

    def get_section_items(self, section_name: str) -> list:
        """Get list of items in a section."""
        if section_name in self._sections:
            return [item['name'] for item in self._sections[section_name]['items']]
        return []


class SimpleAccordion(AccordionMenuWidget):
    """Simplified accordion for basic use cases."""

    def __init__(self, parent=None):
        super().__init__(allow_multiple=False, parent=parent)

    def add_section_with_items(self, section_name: str, items: list, expanded: bool = False):
        """Add section with list of items."""
        self.add_section(section_name, expanded)
        for item in items:
            if isinstance(item, str):
                self.add_item(section_name, item)
            elif isinstance(item, dict):
                self.add_item(section_name, item.get('name', ''), item.get('icon'))


class SettingsAccordion(AccordionMenuWidget):
    """Accordion specifically for settings organization."""

    def __init__(self, parent=None):
        super().__init__(allow_multiple=True, parent=parent)

    def add_settings_group(self, group_name: str, settings: dict):
        """Add settings group with key-value pairs."""
        self.add_section(group_name, False)

        for setting_key, setting_value in settings.items():
            # Create setting item with current value display
            display_text = f"{setting_key}: {setting_value}"
            self.add_item(group_name, display_text)


class NavigationAccordion(AccordionMenuWidget):
    """Accordion for navigation menus."""

    def __init__(self, parent=None):
        super().__init__(allow_multiple=False, parent=parent)
        self._active_item = None

    def set_active_item(self, section_name: str, item_name: str):
        """Set active navigation item."""
        # Remove previous active styling
        if self._active_item:
            prev_section, prev_item = self._active_item
            if prev_section in self._sections:
                for item in self._sections[prev_section]['items']:
                    if item['name'] == prev_item:
                        item['button'].setStyleSheet(f"""
                            QPushButton {{
                                border: none;
                                background-color: transparent;
                                text-align: left;
                            }}
                            QPushButton:hover {{
                                background-color: {theme_manager.get_color('hover')};
                            }}
                        """)
                        break

        # Apply active styling to new item
        if section_name in self._sections:
            for item in self._sections[section_name]['items']:
                if item['name'] == item_name:
                    item['button'].setStyleSheet(f"""
                        QPushButton {{
                            border: none;
                            background-color: {theme_manager.get_color('primary')};
                            color: white;
                            text-align: left;
                        }}
                        QPushButton:hover {{
                            background-color: {theme_manager.get_color('primary')};
                        }}
                    """)
                    self._active_item = (section_name, item_name)
                    break