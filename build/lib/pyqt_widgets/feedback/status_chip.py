"""
Status chip widget for displaying colored status indicators.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ..base.theme_manager import theme_manager


class StatusChipWidget(QWidget):
    """Colored pill widget for status display."""

    clicked = pyqtSignal()

    def __init__(self, text="", status="default", size="medium",
                 clickable=False, icon=None, parent=None):
        super().__init__(parent)
        self._text = text
        self._status = status
        self._size = size
        self._clickable = clickable
        self._icon = icon
        self._setup_ui()

    def _setup_ui(self):
        """Setup the status chip UI."""
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Get size properties
        size_props = self._get_size_properties()

        # Set fixed height based on size
        self.setFixedHeight(size_props['height'])

        # Inner container for proper padding and styling
        self.container = QWidget()
        container_layout = QHBoxLayout(self.container)
        container_layout.setContentsMargins(
            size_props['padding_h'],
            size_props['padding_v'],
            size_props['padding_h'],
            size_props['padding_v']
        )
        container_layout.setSpacing(size_props['spacing'])

        # Icon
        if self._icon:
            self.icon_label = QLabel()
            if isinstance(self._icon, str):
                # Text icon (emoji or symbol)
                self.icon_label.setText(self._icon)
            else:
                # QIcon or QPixmap
                self.icon_label.setPixmap(self._icon.pixmap(size_props['icon_size'], size_props['icon_size']))

            self.icon_label.setFixedSize(size_props['icon_size'], size_props['icon_size'])
            self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            container_layout.addWidget(self.icon_label)

        # Text label
        self.text_label = QLabel(self._text)
        self.text_label.setFont(self._get_font())
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.text_label)

        layout.addWidget(self.container)

        # Apply styling
        self._apply_styling()

        # Make clickable if needed
        if self._clickable:
            self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _get_size_properties(self):
        """Get size-specific properties."""
        sizes = {
            'small': {
                'height': 20,
                'padding_h': 8,
                'padding_v': 2,
                'spacing': 4,
                'icon_size': 12,
                'font_size': 10,
                'border_radius': 10
            },
            'medium': {
                'height': 24,
                'padding_h': 12,
                'padding_v': 4,
                'spacing': 6,
                'icon_size': 14,
                'font_size': 11,
                'border_radius': 12
            },
            'large': {
                'height': 32,
                'padding_h': 16,
                'padding_v': 6,
                'spacing': 8,
                'icon_size': 16,
                'font_size': 12,
                'border_radius': 16
            }
        }

        return sizes.get(self._size, sizes['medium'])

    def _get_font(self):
        """Get font for current size."""
        font = theme_manager.get_font('default')
        size_props = self._get_size_properties()
        font.setPointSize(size_props['font_size'])
        font.setWeight(QFont.Weight.Medium)
        return font

    def _apply_styling(self):
        """Apply status-specific styling."""
        status_colors = {
            'default': {
                'bg': theme_manager.get_color('light'),
                'text': theme_manager.get_color('text'),
                'border': theme_manager.get_color('border')
            },
            'primary': {
                'bg': theme_manager.get_color('primary'),
                'text': 'white',
                'border': theme_manager.get_color('primary')
            },
            'success': {
                'bg': theme_manager.get_color('success'),
                'text': 'white',
                'border': theme_manager.get_color('success')
            },
            'warning': {
                'bg': theme_manager.get_color('warning'),
                'text': 'white',
                'border': theme_manager.get_color('warning')
            },
            'error': {
                'bg': theme_manager.get_color('danger'),
                'text': 'white',
                'border': theme_manager.get_color('danger')
            },
            'info': {
                'bg': theme_manager.get_color('info'),
                'text': 'white',
                'border': theme_manager.get_color('info')
            },
            'active': {
                'bg': '#10B981',  # Green
                'text': 'white',
                'border': '#10B981'
            },
            'inactive': {
                'bg': theme_manager.get_color('text_secondary'),
                'text': 'white',
                'border': theme_manager.get_color('text_secondary')
            },
            'pending': {
                'bg': '#F59E0B',  # Amber
                'text': 'white',
                'border': '#F59E0B'
            },
            'draft': {
                'bg': '#6B7280',  # Gray
                'text': 'white',
                'border': '#6B7280'
            }
        }

        colors = status_colors.get(self._status, status_colors['default'])
        size_props = self._get_size_properties()

        hover_style = ""
        if self._clickable:
            hover_style = f"""
                QWidget:hover {{
                    background-color: {self._darken_color(colors['bg'])};
                }}
            """

        self.container.setStyleSheet(f"""
            QWidget {{
                background-color: {colors['bg']};
                border: 1px solid {colors['border']};
                border-radius: {size_props['border_radius']}px;
                color: {colors['text']};
            }}
            {hover_style}
        """)

        # Update text and icon colors
        self.text_label.setStyleSheet(f"color: {colors['text']}; background: transparent; border: none;")

        if hasattr(self, 'icon_label'):
            self.icon_label.setStyleSheet(f"color: {colors['text']}; background: transparent; border: none;")

    def _darken_color(self, color: str) -> str:
        """Darken a color for hover effect."""
        # Simple darkening - in real implementation, you'd use QColor
        if color.startswith('#'):
            return color  # Return same for now
        return color

    def mousePressEvent(self, event):
        """Handle mouse press for clickable chips."""
        if self._clickable and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def set_text(self, text: str):
        """Update chip text."""
        self._text = text
        self.text_label.setText(text)

    def set_status(self, status: str):
        """Update chip status."""
        self._status = status
        self._apply_styling()

    def set_icon(self, icon):
        """Update chip icon."""
        self._icon = icon
        if hasattr(self, 'icon_label'):
            if isinstance(icon, str):
                self.icon_label.setText(icon)
            else:
                size_props = self._get_size_properties()
                self.icon_label.setPixmap(icon.pixmap(size_props['icon_size'], size_props['icon_size']))
        else:
            # Recreate UI to add icon
            self._setup_ui()

    def set_clickable(self, clickable: bool):
        """Set whether chip is clickable."""
        self._clickable = clickable
        if clickable:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        self._apply_styling()

    def get_text(self) -> str:
        """Get current text."""
        return self._text

    def get_status(self) -> str:
        """Get current status."""
        return self._status

    def is_clickable(self) -> bool:
        """Check if chip is clickable."""
        return self._clickable


class StatusChipGroup(QWidget):
    """Group of status chips."""

    chip_clicked = pyqtSignal(str, str)  # Emits chip text and status

    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(parent)
        self._chips = []
        self._orientation = orientation
        self._setup_ui()

    def _setup_ui(self):
        """Setup the chip group UI."""
        if self._orientation == Qt.Orientation.Horizontal:
            self.layout = QHBoxLayout(self)
        else:
            from PyQt6.QtWidgets import QVBoxLayout
            self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)
        self.layout.addStretch()

    def add_chip(self, text: str, status: str = "default", clickable: bool = False):
        """Add chip to group."""
        chip = StatusChipWidget(text, status, "medium", clickable)
        if clickable:
            chip.clicked.connect(lambda: self.chip_clicked.emit(text, status))

        self._chips.append(chip)
        self.layout.insertWidget(self.layout.count() - 1, chip)

        return chip

    def remove_chip(self, text: str):
        """Remove chip by text."""
        for i, chip in enumerate(self._chips):
            if chip.get_text() == text:
                chip.setParent(None)
                del self._chips[i]
                break

    def clear_chips(self):
        """Remove all chips."""
        for chip in self._chips:
            chip.setParent(None)
        self._chips.clear()

    def get_chips(self) -> list:
        """Get list of chip texts."""
        return [chip.get_text() for chip in self._chips]


class InteractiveStatusChip(StatusChipWidget):
    """Status chip that can be toggled or changed interactively."""

    status_changed = pyqtSignal(str)  # Emits new status

    def __init__(self, text="", statuses=None, current_status=0, parent=None):
        self._statuses = statuses or ['default', 'active', 'inactive']
        self._current_status_index = current_status

        super().__init__(text, self._statuses[self._current_status_index], "medium", True, parent=parent)
        self.clicked.connect(self._cycle_status)

    def _cycle_status(self):
        """Cycle to next status."""
        self._current_status_index = (self._current_status_index + 1) % len(self._statuses)
        new_status = self._statuses[self._current_status_index]
        self.set_status(new_status)
        self.status_changed.emit(new_status)

    def set_statuses(self, statuses: list):
        """Set available statuses."""
        self._statuses = statuses
        self._current_status_index = 0
        self.set_status(self._statuses[0])

    def get_current_status_index(self) -> int:
        """Get current status index."""
        return self._current_status_index


class AnimatedStatusChip(StatusChipWidget):
    """Status chip with animation effects."""

    def __init__(self, text="", status="default", parent=None):
        super().__init__(text, status, "medium", parent=parent)
        self._setup_animations()

    def _setup_animations(self):
        """Setup animation effects."""
        from PyQt6.QtCore import QPropertyAnimation

        self._pulse_animation = QPropertyAnimation(self, b"geometry")
        self._pulse_animation.setDuration(200)

    def pulse_effect(self):
        """Trigger pulse animation."""
        original_rect = self.geometry()
        expanded_rect = original_rect.adjusted(-2, -1, 2, 1)

        self._pulse_animation.setStartValue(original_rect)
        self._pulse_animation.setEndValue(expanded_rect)

        # Return to original size
        def return_to_normal():
            self._pulse_animation.setStartValue(expanded_rect)
            self._pulse_animation.setEndValue(original_rect)
            self._pulse_animation.start()

        self._pulse_animation.finished.connect(return_to_normal)
        self._pulse_animation.start()

    def set_status(self, status: str):
        """Override to add pulse effect on status change."""
        if status != self._status:
            super().set_status(status)
            self.pulse_effect()


class CounterChip(StatusChipWidget):
    """Status chip that displays a counter."""

    def __init__(self, label="", count=0, status="default", parent=None):
        self._label = label
        self._count = count
        text = f"{label} ({count})" if label else str(count)

        super().__init__(text, status, "medium", parent=parent)

    def set_count(self, count: int):
        """Update counter value."""
        self._count = count
        text = f"{self._label} ({count})" if self._label else str(count)
        self.set_text(text)

    def increment(self):
        """Increment counter."""
        self.set_count(self._count + 1)

    def decrement(self):
        """Decrement counter."""
        self.set_count(max(0, self._count - 1))

    def get_count(self) -> int:
        """Get current count."""
        return self._count