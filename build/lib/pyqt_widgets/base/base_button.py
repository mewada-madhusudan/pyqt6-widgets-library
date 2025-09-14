"""
Enhanced button widget with variants and states.
"""

from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QIcon, QFont
from .theme_manager import theme_manager
from .animation_helpers import AnimationHelpers


class BaseButton(QPushButton):
    """Enhanced button with variants and hover effects."""

    def __init__(self, text="", variant="primary", size="medium", parent=None):
        super().__init__(text, parent)
        self._variant = variant
        self._size = size
        self._loading = False
        self._icon_widget = None
        self._setup_styling()

    def _setup_styling(self):
        """Apply variant-specific styling."""
        colors = self._get_variant_colors()
        sizes = self._get_size_properties()

        self.setStyleSheet(f"""
            BaseButton {{
                background-color: {colors['bg']};
                color: {colors['text']};
                border: {colors['border']};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                padding: {sizes['padding']};
                font-size: {sizes['font_size']}pt;
                font-weight: bold;
                min-width: {sizes['min_width']}px;
                min-height: {sizes['min_height']}px;
            }}

            BaseButton:hover {{
                background-color: {colors['hover_bg']};
                border-color: {colors['hover_border']};
            }}

            BaseButton:pressed {{
                background-color: {colors['pressed_bg']};
            }}

            BaseButton:disabled {{
                background-color: {theme_manager.get_color('light')};
                color: {theme_manager.get_color('text_secondary')};
                border-color: {theme_manager.get_color('border')};
            }}
        """)

    def _get_variant_colors(self):
        """Get colors for current variant."""
        if self._variant == "primary":
            return {
                'bg': theme_manager.get_color('primary'),
                'text': 'white',
                'border': f"1px solid {theme_manager.get_color('primary')}",
                'hover_bg': theme_manager.get_color('dark'),
                'hover_border': theme_manager.get_color('dark'),
                'pressed_bg': theme_manager.get_color('dark')
            }
        elif self._variant == "secondary":
            return {
                'bg': 'transparent',
                'text': theme_manager.get_color('primary'),
                'border': f"1px solid {theme_manager.get_color('primary')}",
                'hover_bg': theme_manager.get_color('primary'),
                'hover_border': theme_manager.get_color('primary'),
                'pressed_bg': theme_manager.get_color('dark')
            }
        elif self._variant == "destructive":
            return {
                'bg': theme_manager.get_color('danger'),
                'text': 'white',
                'border': f"1px solid {theme_manager.get_color('danger')}",
                'hover_bg': '#c82333',
                'hover_border': '#c82333',
                'pressed_bg': '#bd2130'
            }
        elif self._variant == "ghost":
            return {
                'bg': 'transparent',
                'text': theme_manager.get_color('text'),
                'border': 'none',
                'hover_bg': theme_manager.get_color('hover'),
                'hover_border': 'none',
                'pressed_bg': theme_manager.get_color('light')
            }
        else:  # default
            return {
                'bg': theme_manager.get_color('surface'),
                'text': theme_manager.get_color('text'),
                'border': f"1px solid {theme_manager.get_color('border')}",
                'hover_bg': theme_manager.get_color('hover'),
                'hover_border': theme_manager.get_color('border'),
                'pressed_bg': theme_manager.get_color('light')
            }

    def _get_size_properties(self):
        """Get size properties for current size."""
        if self._size == "small":
            return {
                'padding': '4px 8px',
                'font_size': 8,
                'min_width': 60,
                'min_height': 24
            }
        elif self._size == "large":
            return {
                'padding': '12px 24px',
                'font_size': 11,
                'min_width': 120,
                'min_height': 44
            }
        else:  # medium
            return {
                'padding': '8px 16px',
                'font_size': 9,
                'min_width': 80,
                'min_height': 32
            }

    def set_variant(self, variant: str):
        """Change button variant."""
        self._variant = variant
        self._setup_styling()

    def set_size(self, size: str):
        """Change button size."""
        self._size = size
        self._setup_styling()

    def set_loading(self, loading: bool):
        """Set loading state."""
        self._loading = loading
        if loading:
            self.setText("Loading...")
            self.setEnabled(False)
        else:
            self.setEnabled(True)

    def set_icon(self, icon: QIcon, position="left"):
        """Set button icon."""
        self.setIcon(icon)
        if position == "right":
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

    def animate_click(self):
        """Animate button click effect."""
        # Scale down and back up
        original_size = self.size()
        smaller_size = QSize(
            int(original_size.width() * 0.95),
            int(original_size.height() * 0.95)
        )

        # Scale down animation
        scale_down = QPropertyAnimation(self, b"size")
        scale_down.setDuration(100)
        scale_down.setStartValue(original_size)
        scale_down.setEndValue(smaller_size)
        scale_down.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Scale back up animation
        scale_up = QPropertyAnimation(self, b"size")
        scale_up.setDuration(100)
        scale_up.setStartValue(smaller_size)
        scale_up.setEndValue(original_size)
        scale_up.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Chain animations
        scale_down.finished.connect(scale_up.start)
        scale_down.start()

    def mousePressEvent(self, event):
        """Handle mouse press with animation."""
        self.animate_click()
        super().mousePressEvent(event)


class IconButton(BaseButton):
    """Button with icon only."""

    def __init__(self, icon: QIcon, size="medium", parent=None):
        super().__init__("", "ghost", size, parent)
        self.setIcon(icon)
        self._make_circular()

    def _make_circular(self):
        """Make button circular."""
        size_props = self._get_size_properties()
        min_size = size_props['min_height']

        self.setFixedSize(min_size, min_size)
        self.setStyleSheet(self.styleSheet() + f"""
            BaseButton {{
                border-radius: {min_size // 2}px;
            }}
        """)


class ToggleButton(BaseButton):
    """Toggle button that can be checked/unchecked."""

    toggled = pyqtSignal(bool)

    def __init__(self, text="", parent=None):
        super().__init__(text, "secondary", "medium", parent)
        self._checked = False
        self.clicked.connect(self._handle_toggle)

    def _handle_toggle(self):
        """Handle toggle action."""
        self._checked = not self._checked
        self._update_appearance()
        self.toggled.emit(self._checked)

    def set_checked(self, checked: bool):
        """Set checked state."""
        self._checked = checked
        self._update_appearance()

    def is_checked(self) -> bool:
        """Get checked state."""
        return self._checked

    def _update_appearance(self):
        """Update appearance based on checked state."""
        if self._checked:
            self.set_variant("primary")
        else:
            self.set_variant("secondary")


class ButtonGroup:
    """Group of mutually exclusive toggle buttons."""

    def __init__(self):
        self._buttons = []
        self._active_button = None

    def add_button(self, button: ToggleButton):
        """Add button to group."""
        self._buttons.append(button)
        button.toggled.connect(lambda checked, btn=button: self._handle_button_toggle(btn, checked))

    def _handle_button_toggle(self, button: ToggleButton, checked: bool):
        """Handle button toggle in group."""
        if checked:
            # Uncheck all other buttons
            for btn in self._buttons:
                if btn != button and btn.is_checked():
                    btn.set_checked(False)
            self._active_button = button
        else:
            if button == self._active_button:
                self._active_button = None

    def get_active_button(self) -> ToggleButton:
        """Get currently active button."""
        return self._active_button