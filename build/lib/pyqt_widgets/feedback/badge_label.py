"""
Badge label widget with count indicators.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ..base.theme_manager import theme_manager


class BadgeLabel(QWidget):
    """Label with count badge indicator."""

    def __init__(self, text="", count=0, badge_color="primary",
                 show_zero=False, max_count=99, parent=None):
        super().__init__(parent)
        self._text = text
        self._count = count
        self._badge_color = badge_color
        self._show_zero = show_zero
        self._max_count = max_count
        self._setup_ui()

    def _setup_ui(self):
        """Setup the badge label UI."""
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Main text label
        self.text_label = QLabel(self._text)
        self.text_label.setFont(theme_manager.get_font('default'))
        self.text_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        layout.addWidget(self.text_label)

        # Badge container (positioned relative to text)
        self.badge_container = QWidget()
        self.badge_container.setFixedSize(24, 20)

        # Badge label
        self.badge_label = QLabel()
        self.badge_label.setParent(self.badge_container)
        self.badge_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.badge_container)

        # Update badge display
        self._update_badge()

    def _update_badge(self):
        """Update badge appearance and visibility."""
        # Determine if badge should be visible
        show_badge = self._count > 0 or (self._count == 0 and self._show_zero)

        if not show_badge:
            self.badge_label.hide()
            return

        # Format count text
        if self._count > self._max_count:
            badge_text = f"{self._max_count}+"
        else:
            badge_text = str(self._count)

        self.badge_label.setText(badge_text)

        # Calculate badge size based on text length
        text_width = len(badge_text)
        if text_width == 1:
            badge_size = 18
        elif text_width == 2:
            badge_size = 22
        else:
            badge_size = max(22, text_width * 8)

        self.badge_label.setFixedSize(badge_size, 18)

        # Position badge (top-right of container)
        self.badge_label.move(
            self.badge_container.width() - badge_size,
            0
        )

        # Apply badge styling
        colors = self._get_badge_colors()

        self.badge_label.setStyleSheet(f"""
            QLabel {{
                background-color: {colors['bg']};
                color: {colors['text']};
                border-radius: 9px;
                font-size: 10px;
                font-weight: bold;
                padding: 2px 4px;
            }}
        """)

        self.badge_label.show()

    def _get_badge_colors(self):
        """Get colors for badge based on badge_color."""
        color_schemes = {
            'primary': {
                'bg': theme_manager.get_color('primary'),
                'text': 'white'
            },
            'success': {
                'bg': theme_manager.get_color('success'),
                'text': 'white'
            },
            'warning': {
                'bg': theme_manager.get_color('warning'),
                'text': 'white'
            },
            'error': {
                'bg': theme_manager.get_color('danger'),
                'text': 'white'
            },
            'info': {
                'bg': theme_manager.get_color('info'),
                'text': 'white'
            },
            'secondary': {
                'bg': theme_manager.get_color('text_secondary'),
                'text': 'white'
            }
        }

        return color_schemes.get(self._badge_color, color_schemes['primary'])

    def set_text(self, text: str):
        """Update main text."""
        self._text = text
        self.text_label.setText(text)

    def set_count(self, count: int):
        """Update badge count."""
        self._count = max(0, count)
        self._update_badge()

    def increment_count(self):
        """Increment badge count."""
        self.set_count(self._count + 1)

    def decrement_count(self):
        """Decrement badge count."""
        self.set_count(self._count - 1)

    def set_badge_color(self, color: str):
        """Update badge color."""
        self._badge_color = color
        self._update_badge()

    def set_show_zero(self, show_zero: bool):
        """Set whether to show badge when count is zero."""
        self._show_zero = show_zero
        self._update_badge()

    def set_max_count(self, max_count: int):
        """Set maximum count before showing '+'."""
        self._max_count = max_count
        self._update_badge()

    def get_text(self) -> str:
        """Get current text."""
        return self._text

    def get_count(self) -> int:
        """Get current count."""
        return self._count

    def get_badge_color(self) -> str:
        """Get current badge color."""
        return self._badge_color


class IconBadgeLabel(BadgeLabel):
    """Badge label with icon instead of text."""

    def __init__(self, icon=None, count=0, badge_color="primary", parent=None):
        self._icon = icon
        super().__init__("", count, badge_color, parent=parent)
        self._setup_icon()

    def _setup_icon(self):
        """Setup icon display."""
        if self._icon:
            if isinstance(self._icon, str):
                # Text icon (emoji or symbol)
                self.text_label.setText(self._icon)
                icon_font = theme_manager.get_font('default')
                icon_font.setPointSize(16)
                self.text_label.setFont(icon_font)
            else:
                # QIcon or QPixmap
                self.text_label.setPixmap(self._icon.pixmap(24, 24))

        self.text_label.setFixedSize(24, 24)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_icon(self, icon):
        """Update icon."""
        self._icon = icon
        self._setup_icon()


class NotificationBadge(QWidget):
    """Simple notification dot badge."""

    def __init__(self, color="primary", size=8, parent=None):
        super().__init__(parent)
        self._color = color
        self._size = size
        self._visible = True
        self._setup_ui()

    def _setup_ui(self):
        """Setup notification badge UI."""
        self.setFixedSize(self._size, self._size)

        colors = {
            'primary': theme_manager.get_color('primary'),
            'success': theme_manager.get_color('success'),
            'warning': theme_manager.get_color('warning'),
            'error': theme_manager.get_color('danger'),
            'info': theme_manager.get_color('info')
        }

        color = colors.get(self._color, colors['primary'])

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {color};
                border-radius: {self._size // 2}px;
                border: 2px solid white;
            }}
        """)

    def set_visible_badge(self, visible: bool):
        """Show/hide badge."""
        self._visible = visible
        self.setVisible(visible)

    def set_color(self, color: str):
        """Update badge color."""
        self._color = color
        self._setup_ui()

    def is_visible_badge(self) -> bool:
        """Check if badge is visible."""
        return self._visible


class MenuBadgeLabel(BadgeLabel):
    """Badge label specifically for menu items."""

    def __init__(self, text="", count=0, parent=None):
        super().__init__(text, count, "primary", False, 99, parent)
        self._setup_menu_styling()

    def _setup_menu_styling(self):
        """Apply menu-specific styling."""
        # Adjust layout for menu items
        self.layout().setSpacing(12)

        # Style text for menu
        menu_font = theme_manager.get_font('default')
        self.text_label.setFont(menu_font)

        # Position badge differently for menu
        self.badge_container.setFixedSize(20, 16)

    def _update_badge(self):
        """Override to position badge for menu layout."""
        super()._update_badge()

        if hasattr(self, 'badge_label') and self.badge_label.isVisible():
            # Position at right edge for menu items
            self.badge_label.move(0, 0)


class StatusBadgeLabel(BadgeLabel):
    """Badge label that shows status instead of count."""

    def __init__(self, text="", status="offline", parent=None):
        self._status = status
        super().__init__(text, 0, "secondary", True, parent=parent)
        self._update_status_badge()

    def _update_status_badge(self):
        """Update badge to show status."""
        status_config = {
            'online': {'color': 'success', 'text': '●'},
            'offline': {'color': 'secondary', 'text': '●'},
            'away': {'color': 'warning', 'text': '●'},
            'busy': {'color': 'error', 'text': '●'},
            'invisible': {'color': 'secondary', 'text': '○'}
        }

        config = status_config.get(self._status, status_config['offline'])

        self.badge_label.setText(config['text'])
        self.badge_label.setFixedSize(12, 12)

        # Position badge
        self.badge_label.move(
            self.badge_container.width() - 12,
            self.badge_container.height() - 12
        )

        # Apply status-specific styling
        colors = self._get_badge_colors()
        if config['color'] != self._badge_color:
            self._badge_color = config['color']
            colors = self._get_badge_colors()

        self.badge_label.setStyleSheet(f"""
            QLabel {{
                background-color: transparent;
                color: {colors['bg']};
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
            }}
        """)

        self.badge_label.show()

    def set_status(self, status: str):
        """Update status."""
        self._status = status
        self._update_status_badge()

    def get_status(self) -> str:
        """Get current status."""
        return self._status


class AnimatedBadgeLabel(BadgeLabel):
    """Badge label with animation effects."""

    def __init__(self, text="", count=0, parent=None):
        super().__init__(text, count, parent=parent)
        self._setup_animations()

    def _setup_animations(self):
        """Setup animation effects."""
        from PyQt6.QtCore import QPropertyAnimation, QSequentialAnimationGroup

        self._bounce_animation = QSequentialAnimationGroup()

        # Scale up
        scale_up = QPropertyAnimation(self.badge_label, b"geometry")
        scale_up.setDuration(150)

        # Scale down
        scale_down = QPropertyAnimation(self.badge_label, b"geometry")
        scale_down.setDuration(150)

        self._bounce_animation.addAnimation(scale_up)
        self._bounce_animation.addAnimation(scale_down)

    def set_count(self, count: int):
        """Override to add animation on count change."""
        old_count = self._count
        super().set_count(count)

        # Animate if count increased
        if count > old_count and hasattr(self, '_bounce_animation'):
            self._animate_badge_change()

    def _animate_badge_change(self):
        """Animate badge when count changes."""
        if not hasattr(self, 'badge_label') or not self.badge_label.isVisible():
            return

        original_rect = self.badge_label.geometry()
        expanded_rect = original_rect.adjusted(-2, -2, 2, 2)

        # Update animation values
        scale_up = self._bounce_animation.animationAt(0)
        scale_down = self._bounce_animation.animationAt(1)

        scale_up.setStartValue(original_rect)
        scale_up.setEndValue(expanded_rect)

        scale_down.setStartValue(expanded_rect)
        scale_down.setEndValue(original_rect)

        self._bounce_animation.start()