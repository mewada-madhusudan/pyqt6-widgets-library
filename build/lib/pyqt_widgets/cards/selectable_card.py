"""
Selectable card widget with highlight and toggle states.
"""

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ..base.base_card import BaseCardWidget
from ..base.theme_manager import theme_manager


class SelectableCardWidget(BaseCardWidget):
    """Card widget that can be selected with visual feedback."""

    selection_changed = pyqtSignal(bool)  # Emits selection state

    def __init__(self, title="", subtitle="", selectable=True, multi_select=False, parent=None):
        super().__init__(parent)
        self._title = title
        self._subtitle = subtitle
        self._multi_select = multi_select
        self._checkbox = None
        self.set_selectable(selectable)
        self._setup_selectable_ui()

    def _setup_selectable_ui(self):
        """Setup the selectable card UI."""
        # Main content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)

        # Header with selection indicator
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        # Multi-select checkbox
        if self._multi_select:
            self._checkbox = QCheckBox()
            self._checkbox.stateChanged.connect(self._on_checkbox_changed)
            header_layout.addWidget(self._checkbox)

        # Title and subtitle
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(4)

        # Title
        if self._title:
            self.title_label = QLabel(self._title)
            title_font = theme_manager.get_font('heading')
            self.title_label.setFont(title_font)
            self.title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
            text_layout.addWidget(self.title_label)

        # Subtitle
        if self._subtitle:
            self.subtitle_label = QLabel(self._subtitle)
            self.subtitle_label.setFont(theme_manager.get_font('default'))
            self.subtitle_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            self.subtitle_label.setWordWrap(True)
            text_layout.addWidget(self.subtitle_label)

        header_layout.addWidget(text_widget)
        header_layout.addStretch()

        # Selection indicator (for single select)
        if not self._multi_select:
            self.selection_indicator = QLabel()
            self.selection_indicator.setFixedSize(20, 20)
            self.selection_indicator.setStyleSheet(f"""
                QLabel {{
                    border: 2px solid {theme_manager.get_color('border')};
                    border-radius: 10px;
                    background-color: transparent;
                }}
            """)
            header_layout.addWidget(self.selection_indicator)

        content_layout.addWidget(header_widget)
        content_layout.addStretch()

        self.set_body(content_widget)

        # Update initial styling
        self._update_selection_styling()

    def _on_checkbox_changed(self, state):
        """Handle checkbox state change."""
        selected = state == Qt.CheckState.Checked.value
        self.set_selected(selected)

    def _update_selection_styling(self):
        """Update styling based on selection state."""
        if self.is_selected():
            # Selected state styling
            self.setStyleSheet(f"""
                SelectableCardWidget {{
                    background-color: {theme_manager.get_color('primary')};
                    border: 2px solid {theme_manager.get_color('primary')};
                    border-radius: {theme_manager.get_border_radius('md')}px;
                }}
            """)

            # Update text colors for selected state
            if hasattr(self, 'title_label'):
                self.title_label.setStyleSheet("color: white;")
            if hasattr(self, 'subtitle_label'):
                self.subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")

            # Update selection indicator
            if hasattr(self, 'selection_indicator'):
                self.selection_indicator.setStyleSheet(f"""
                    QLabel {{
                        border: 2px solid white;
                        border-radius: 10px;
                        background-color: white;
                        color: {theme_manager.get_color('primary')};
                        font-weight: bold;
                    }}
                """)
                self.selection_indicator.setText("✓")
                self.selection_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            # Unselected state styling
            self.setStyleSheet(f"""
                SelectableCardWidget {{
                    background-color: {theme_manager.get_color('surface')};
                    border: 1px solid {theme_manager.get_color('border')};
                    border-radius: {theme_manager.get_border_radius('md')}px;
                }}

                SelectableCardWidget:hover {{
                    border-color: {theme_manager.get_color('primary')};
                    background-color: {theme_manager.get_color('hover')};
                }}
            """)

            # Reset text colors
            if hasattr(self, 'title_label'):
                self.title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
            if hasattr(self, 'subtitle_label'):
                self.subtitle_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")

            # Reset selection indicator
            if hasattr(self, 'selection_indicator'):
                self.selection_indicator.setText("")
                self.selection_indicator.setStyleSheet(f"""
                    QLabel {{
                        border: 2px solid {theme_manager.get_color('border')};
                        border-radius: 10px;
                        background-color: transparent;
                    }}
                """)

    def set_selected(self, selected: bool):
        """Override parent method to update styling."""
        super().set_selected(selected)
        self._update_selection_styling()

        # Update checkbox if in multi-select mode
        if self._multi_select and self._checkbox:
            self._checkbox.blockSignals(True)
            self._checkbox.setChecked(selected)
            self._checkbox.blockSignals(False)

        self.selection_changed.emit(selected)

    def set_title(self, title: str):
        """Update title."""
        self._title = title
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)

    def set_subtitle(self, subtitle: str):
        """Update subtitle."""
        self._subtitle = subtitle
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setText(subtitle)

    def get_title(self) -> str:
        """Get current title."""
        return self._title

    def get_subtitle(self) -> str:
        """Get current subtitle."""
        return self._subtitle


class OptionCard(SelectableCardWidget):
    """Card for selecting options with description."""

    def __init__(self, title="", description="", value=None, parent=None):
        self._value = value
        super().__init__(title, description, True, False, parent)

    def get_value(self):
        """Get option value."""
        return self._value

    def set_value(self, value):
        """Set option value."""
        self._value = value


class MultiSelectCard(SelectableCardWidget):
    """Card for multi-selection scenarios."""

    def __init__(self, title="", subtitle="", parent=None):
        super().__init__(title, subtitle, True, True, parent)


class FilterCard(SelectableCardWidget):
    """Card for filter options."""

    def __init__(self, filter_name="", count=0, parent=None):
        self._filter_name = filter_name
        self._count = count

        # Format subtitle with count
        subtitle = f"{count} items" if count > 0 else "No items"
        super().__init__(filter_name, subtitle, True, True, parent)

    def set_count(self, count: int):
        """Update item count."""
        self._count = count
        subtitle = f"{count} items" if count > 0 else "No items"
        self.set_subtitle(subtitle)

    def get_count(self) -> int:
        """Get current count."""
        return self._count

    def get_filter_name(self) -> str:
        """Get filter name."""
        return self._filter_name