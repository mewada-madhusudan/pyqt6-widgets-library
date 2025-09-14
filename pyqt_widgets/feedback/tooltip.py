"""
Enhanced tooltip widget with icons and actions.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPoint
from PyQt6.QtGui import QFont, QIcon
from ..base.base_popup import BasePopupWidget
from ..base.theme_manager import theme_manager


class TooltipWidget(BasePopupWidget):
    """Enhanced tooltip with icons, actions, and rich content."""

    action_clicked = pyqtSignal(str)

    def __init__(self, text="", icon=None, delay=500, parent=None):
        super().__init__(parent, modal=False)
        self._text = text
        self._icon = icon
        self._delay = delay
        self._actions = []
        self._setup_tooltip_ui()

    def _setup_tooltip_ui(self):
        """Setup the tooltip UI."""
        self.setMaximumWidth(300)

        # Main content layout
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(12, 8, 12, 8)
        content_layout.setSpacing(8)

        # Header with icon and text
        if self._icon or self._text:
            header_layout = QHBoxLayout()
            header_layout.setContentsMargins(0, 0, 0, 0)
            header_layout.setSpacing(8)

            # Icon
            if self._icon:
                self.icon_label = QLabel()
                if isinstance(self._icon, str):
                    self.icon_label.setText(self._icon)
                    icon_font = theme_manager.get_font('default')
                    icon_font.setPointSize(14)
                    self.icon_label.setFont(icon_font)
                else:
                    self.icon_label.setPixmap(self._icon.pixmap(16, 16))

                self.icon_label.setFixedSize(16, 16)
                self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                header_layout.addWidget(self.icon_label)

            # Text
            if self._text:
                self.text_label = QLabel(self._text)
                self.text_label.setFont(theme_manager.get_font('default'))
                self.text_label.setWordWrap(True)
                header_layout.addWidget(self.text_label)

            content_layout.addLayout(header_layout)

        # Actions container
        self.actions_widget = QWidget()
        self.actions_layout = QHBoxLayout(self.actions_widget)
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        self.actions_layout.setSpacing(4)
        self.actions_widget.hide()

        content_layout.addWidget(self.actions_widget)

        # Apply tooltip styling
        self.setStyleSheet(f"""
            TooltipWidget {{
                background-color: {theme_manager.get_color('dark')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                color: white;
            }}
        """)

        if hasattr(self, 'text_label'):
            self.text_label.setStyleSheet("color: white; background: transparent;")
        if hasattr(self, 'icon_label'):
            self.icon_label.setStyleSheet("color: white; background: transparent;")

        # Set layout
        self.layout.addLayout(content_layout)

    def add_action(self, text: str, action_name: str = None):
        """Add action button to tooltip."""
        if action_name is None:
            action_name = text.lower().replace(" ", "_")

        action_btn = QPushButton(text)
        action_btn.setFlat(True)
        action_btn.clicked.connect(lambda: self._on_action_clicked(action_name))
        action_btn.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid rgba(255, 255, 255, 0.3);
                background-color: transparent;
                color: white;
                padding: 2px 8px;
                border-radius: 3px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.2);
            }}
        """)

        self.actions_layout.addWidget(action_btn)
        self._actions.append((action_btn, action_name))

        # Show actions container
        self.actions_widget.show()

    def _on_action_clicked(self, action_name: str):
        """Handle action button click."""
        self.action_clicked.emit(action_name)
        self.close_animated()

    def show_tooltip_at(self, position: QPoint):
        """Show tooltip at specific position."""
        # Adjust position to keep tooltip on screen
        screen = QApplication.instance().primaryScreen().availableGeometry()

        x = position.x()
        y = position.y() - self.height() - 10  # Show above cursor

        # Adjust if tooltip would go off screen
        if x + self.width() > screen.right():
            x = screen.right() - self.width()
        if x < screen.left():
            x = screen.left()

        if y < screen.top():
            y = position.y() + 20  # Show below cursor instead

        self.show_at_position(x, y)

    def show_for_widget(self, widget: QWidget, position: str = "top"):
        """Show tooltip for a specific widget."""
        widget_rect = widget.geometry()
        widget_global_pos = widget.mapToGlobal(QPoint(0, 0))

        if position == "top":
            x = widget_global_pos.x() + widget_rect.width() // 2 - self.width() // 2
            y = widget_global_pos.y() - self.height() - 5
        elif position == "bottom":
            x = widget_global_pos.x() + widget_rect.width() // 2 - self.width() // 2
            y = widget_global_pos.y() + widget_rect.height() + 5
        elif position == "left":
            x = widget_global_pos.x() - self.width() - 5
            y = widget_global_pos.y() + widget_rect.height() // 2 - self.height() // 2
        elif position == "right":
            x = widget_global_pos.x() + widget_rect.width() + 5
            y = widget_global_pos.y() + widget_rect.height() // 2 - self.height() // 2
        else:  # center
            x = widget_global_pos.x() + widget_rect.width() // 2 - self.width() // 2
            y = widget_global_pos.y() + widget_rect.height() // 2 - self.height() // 2

        self.show_at_position(x, y)

    def set_text(self, text: str):
        """Update tooltip text."""
        self._text = text
        if hasattr(self, 'text_label'):
            self.text_label.setText(text)

    def set_icon(self, icon):
        """Update tooltip icon."""
        self._icon = icon
        if hasattr(self, 'icon_label'):
            if isinstance(icon, str):
                self.icon_label.setText(icon)
            else:
                self.icon_label.setPixmap(icon.pixmap(16, 16))

    def get_text(self) -> str:
        """Get current text."""
        return self._text


class TooltipManager:
    """Manager for showing tooltips on widgets."""

    def __init__(self):
        self._tooltips = {}
        self._hover_timers = {}
        self._current_tooltip = None

    def set_tooltip(self, widget: QWidget, text: str, icon=None, delay: int = 500):
        """Set tooltip for a widget."""
        # Remove existing tooltip
        self.remove_tooltip(widget)

        # Create new tooltip
        tooltip = TooltipWidget(text, icon, delay)
        self._tooltips[widget] = tooltip

        # Install event filter for hover detection
        widget.installEventFilter(self)

    def remove_tooltip(self, widget: QWidget):
        """Remove tooltip from widget."""
        if widget in self._tooltips:
            widget.removeEventFilter(self)
            del self._tooltips[widget]

        if widget in self._hover_timers:
            self._hover_timers[widget].stop()
            del self._hover_timers[widget]

    def eventFilter(self, obj, event):
        """Handle widget events for tooltip display."""
        if obj in self._tooltips:
            if event.type() == event.Type.Enter:
                self._start_hover_timer(obj)
            elif event.type() == event.Type.Leave:
                self._stop_hover_timer(obj)
                self._hide_current_tooltip()

        return False

    def _start_hover_timer(self, widget: QWidget):
        """Start timer for showing tooltip."""
        if widget in self._tooltips:
            tooltip = self._tooltips[widget]

            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(lambda: self._show_tooltip(widget))
            timer.start(tooltip._delay)

            self._hover_timers[widget] = timer

    def _stop_hover_timer(self, widget: QWidget):
        """Stop hover timer."""
        if widget in self._hover_timers:
            self._hover_timers[widget].stop()
            del self._hover_timers[widget]

    def _show_tooltip(self, widget: QWidget):
        """Show tooltip for widget."""
        if widget in self._tooltips:
            # Hide current tooltip
            self._hide_current_tooltip()

            # Show new tooltip
            tooltip = self._tooltips[widget]
            tooltip.show_for_widget(widget)
            self._current_tooltip = tooltip

    def _hide_current_tooltip(self):
        """Hide currently visible tooltip."""
        if self._current_tooltip:
            self._current_tooltip.close_animated()
            self._current_tooltip = None


# Global tooltip manager
tooltip_manager = TooltipManager()


# Convenience functions
def set_tooltip(widget: QWidget, text: str, icon=None, delay: int = 500):
    """Set tooltip for widget."""
    tooltip_manager.set_tooltip(widget, text, icon, delay)


def remove_tooltip(widget: QWidget):
    """Remove tooltip from widget."""
    tooltip_manager.remove_tooltip(widget)


class RichTooltip(TooltipWidget):
    """Tooltip with rich content support."""

    def __init__(self, parent=None):
        super().__init__("", None, 500, parent)
        self._setup_rich_content()

    def _setup_rich_content(self):
        """Setup rich content container."""
        # Clear existing content
        self.layout.itemAt(0).layout().setParent(None)

        # Rich content layout
        self.rich_layout = QVBoxLayout()
        self.rich_layout.setContentsMargins(12, 8, 12, 8)
        self.rich_layout.setSpacing(8)

        self.layout.addLayout(self.rich_layout)

    def add_title(self, title: str):
        """Add title to tooltip."""
        title_label = QLabel(title)
        title_font = theme_manager.get_font('heading')
        title_font.setPointSize(12)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; font-weight: bold;")
        self.rich_layout.addWidget(title_label)

    def add_description(self, description: str):
        """Add description text."""
        desc_label = QLabel(description)
        desc_label.setFont(theme_manager.get_font('default'))
        desc_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        desc_label.setWordWrap(True)
        self.rich_layout.addWidget(desc_label)

    def add_shortcut(self, shortcut: str):
        """Add keyboard shortcut display."""
        shortcut_label = QLabel(f"Shortcut: {shortcut}")
        shortcut_label.setFont(theme_manager.get_font('caption'))
        shortcut_label.setStyleSheet(f"""
            QLabel {{
                color: {theme_manager.get_color('primary')};
                background-color: rgba(255, 255, 255, 0.1);
                padding: 2px 6px;
                border-radius: 3px;
            }}
        """)
        self.rich_layout.addWidget(shortcut_label)

    def add_separator(self):
        """Add visual separator."""
        from PyQt6.QtWidgets import QFrame
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("color: rgba(255, 255, 255, 0.3);")
        self.rich_layout.addWidget(separator)


class HelpTooltip(RichTooltip):
    """Tooltip specifically for help content."""

    def __init__(self, title: str, description: str, shortcut: str = "", parent=None):
        super().__init__(parent)

        if title:
            self.add_title(title)

        if description:
            self.add_description(description)

        if shortcut:
            self.add_separator()
            self.add_shortcut(shortcut)


class StatusTooltip(TooltipWidget):
    """Tooltip for showing status information."""

    def __init__(self, status: str, details: str = "", parent=None):
        # Choose icon based on status
        status_icons = {
            'success': '✓',
            'error': '✗',
            'warning': '⚠',
            'info': 'ℹ',
            'loading': '⟳'
        }

        icon = status_icons.get(status, 'ℹ')
        super().__init__(details, icon, 200, parent)

        # Apply status-specific styling
        self._apply_status_styling(status)

    def _apply_status_styling(self, status: str):
        """Apply styling based on status."""
        status_colors = {
            'success': theme_manager.get_color('success'),
            'error': theme_manager.get_color('danger'),
            'warning': theme_manager.get_color('warning'),
            'info': theme_manager.get_color('info'),
            'loading': theme_manager.get_color('primary')
        }

        bg_color = status_colors.get(status, theme_manager.get_color('dark'))

        self.setStyleSheet(f"""
            StatusTooltip {{
                background-color: {bg_color};
                border: 1px solid {bg_color};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                color: white;
            }}
        """)


class InteractiveTooltip(TooltipWidget):
    """Tooltip that stays open for interaction."""

    def __init__(self, text="", parent=None):
        super().__init__(text, None, 0, parent)  # No auto-close
        self._setup_interactive_features()

    def _setup_interactive_features(self):
        """Setup interactive features."""
        # Add close button
        if hasattr(self, 'layout'):
            close_btn = QPushButton("×")
            close_btn.setFixedSize(16, 16)
            close_btn.setFlat(True)
            close_btn.clicked.connect(self.close_animated)
            close_btn.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background-color: transparent;
                    color: white;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 8px;
                }}
            """)

            # Add to top-right corner
            header_layout = self.layout.itemAt(0).layout().itemAt(0).layout()
            if header_layout:
                header_layout.addStretch()
                header_layout.addWidget(close_btn)

    def enterEvent(self, event):
        """Keep tooltip open on mouse enter."""
        # Don't auto-close on hover
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave."""
        # Could add delayed close here if desired
        super().leaveEvent(event)