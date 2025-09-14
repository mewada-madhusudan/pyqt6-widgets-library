"""
Notification toast widget for auto-dismissing messages.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QIcon
from ..base.base_popup import BasePopupWidget
from ..base.theme_manager import theme_manager


class NotificationToastWidget(BasePopupWidget):
    """Auto-dismissing notification toast."""

    action_clicked = pyqtSignal(str)  # Emits action name

    def __init__(self, message="", toast_type="info", duration=3000,
                 position="top-right", parent=None):
        super().__init__(parent, modal=False)
        self._message = message
        self._toast_type = toast_type  # "info", "success", "warning", "error"
        self._duration = duration
        self._position = position
        self._action_buttons = []
        self._setup_toast_ui()

    def _setup_toast_ui(self):
        """Setup the toast notification UI."""
        self.setFixedWidth(350)

        # Main content layout
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(16, 12, 16, 12)
        content_layout.setSpacing(12)

        # Type icon
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(24, 24)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._set_type_icon()
        content_layout.addWidget(self.icon_label)

        # Message content
        message_layout = QVBoxLayout()
        message_layout.setContentsMargins(0, 0, 0, 0)
        message_layout.setSpacing(4)

        # Message text
        self.message_label = QLabel(self._message)
        self.message_label.setWordWrap(True)
        self.message_label.setFont(theme_manager.get_font('default'))
        message_layout.addWidget(self.message_label)

        # Action buttons container
        self.actions_widget = QWidget()
        self.actions_layout = QHBoxLayout(self.actions_widget)
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        self.actions_layout.setSpacing(8)
        self.actions_widget.hide()
        message_layout.addWidget(self.actions_widget)

        content_layout.addLayout(message_layout)

        # Close button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setFlat(True)
        self.close_btn.clicked.connect(self.close_animated)
        self.close_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-color: transparent;
                color: {theme_manager.get_color('text_secondary')};
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }}
        """)
        content_layout.addWidget(self.close_btn)

        # Apply type-specific styling
        self._apply_type_styling()

        # Set layout
        self.layout.addLayout(content_layout)

        # Auto-dismiss timer
        if self._duration > 0:
            QTimer.singleShot(self._duration, self.close_animated)

    def _set_type_icon(self):
        """Set icon based on toast type."""
        icons = {
            'info': 'ℹ',
            'success': '✓',
            'warning': '⚠',
            'error': '✕'
        }

        icon_text = icons.get(self._toast_type, 'ℹ')
        self.icon_label.setText(icon_text)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Icon styling
        icon_font = theme_manager.get_font('default')
        icon_font.setPointSize(16)
        icon_font.setWeight(QFont.Weight.Bold)
        self.icon_label.setFont(icon_font)

    def _apply_type_styling(self):
        """Apply styling based on toast type."""
        type_colors = {
            'info': {
                'bg': theme_manager.get_color('info'),
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
            }
        }

        colors = type_colors.get(self._toast_type, type_colors['info'])

        self.setStyleSheet(f"""
            NotificationToastWidget {{
                background-color: {colors['bg']};
                border: none;
                border-radius: {theme_manager.get_border_radius('lg')}px;
                color: {colors['text']};
            }}
        """)

        # Update text colors
        self.message_label.setStyleSheet(f"color: {colors['text']};")
        self.icon_label.setStyleSheet(f"color: {colors['text']};")

    def add_action(self, text: str, action_name: str = None):
        """Add action button to toast."""
        if action_name is None:
            action_name = text.lower().replace(" ", "_")

        action_btn = QPushButton(text)
        action_btn.setFlat(True)
        action_btn.clicked.connect(lambda: self._on_action_clicked(action_name))
        action_btn.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid rgba(255, 255, 255, 0.5);
                background-color: transparent;
                color: white;
                padding: 4px 12px;
                border-radius: 4px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.2);
            }}
        """)

        self.actions_layout.addWidget(action_btn)
        self._action_buttons.append((action_btn, action_name))

        # Show actions container
        self.actions_widget.show()

    def _on_action_clicked(self, action_name: str):
        """Handle action button click."""
        self.action_clicked.emit(action_name)
        self.close_animated()

    def show_toast(self):
        """Show the toast at specified position."""
        screen = QApplication.instance().primaryScreen().availableGeometry()

        # Calculate position
        if self._position == "top-right":
            x = screen.width() - self.width() - 20
            y = 20
        elif self._position == "top-left":
            x = 20
            y = 20
        elif self._position == "bottom-right":
            x = screen.width() - self.width() - 20
            y = screen.height() - self.height() - 20
        elif self._position == "bottom-left":
            x = 20
            y = screen.height() - self.height() - 20
        elif self._position == "top-center":
            x = (screen.width() - self.width()) // 2
            y = 20
        elif self._position == "bottom-center":
            x = (screen.width() - self.width()) // 2
            y = screen.height() - self.height() - 20
        else:  # center
            x = (screen.width() - self.width()) // 2
            y = (screen.height() - self.height()) // 2

        # Slide in animation
        self.move(x, y - 50)  # Start above final position
        self.show()

        # Animate slide down
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(QRect(x, y - 50, self.width(), self.height()))
        animation.setEndValue(QRect(x, y, self.width(), self.height()))
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()

    def set_message(self, message: str):
        """Update toast message."""
        self._message = message
        self.message_label.setText(message)

    def set_type(self, toast_type: str):
        """Update toast type."""
        self._toast_type = toast_type
        self._set_type_icon()
        self._apply_type_styling()

    def get_message(self) -> str:
        """Get current message."""
        return self._message

    def get_type(self) -> str:
        """Get current type."""
        return self._toast_type


class ToastManager:
    """Manager for displaying multiple toasts."""

    def __init__(self):
        self._active_toasts = []
        self._max_toasts = 5
        self._spacing = 10

    def show_toast(self, message: str, toast_type: str = "info",
                   duration: int = 3000, position: str = "top-right"):
        """Show a new toast notification."""
        # Remove oldest toast if at max capacity
        if len(self._active_toasts) >= self._max_toasts:
            oldest_toast = self._active_toasts.pop(0)
            oldest_toast.close_animated()

        # Create new toast
        toast = NotificationToastWidget(message, toast_type, duration, position)
        toast.closed.connect(lambda: self._remove_toast(toast))

        # Position toast considering existing toasts
        self._position_toast(toast, position)

        self._active_toasts.append(toast)
        toast.show_toast()

        return toast

    def _position_toast(self, toast: NotificationToastWidget, position: str):
        """Position toast considering existing toasts."""
        if not self._active_toasts:
            return

        # Calculate offset based on existing toasts
        offset = 0
        for existing_toast in self._active_toasts:
            if existing_toast._position == position:
                offset += existing_toast.height() + self._spacing

        # Adjust toast position
        if "top" in position:
            toast._position_offset = offset
        elif "bottom" in position:
            toast._position_offset = -offset

    def _remove_toast(self, toast: NotificationToastWidget):
        """Remove toast from active list."""
        if toast in self._active_toasts:
            self._active_toasts.remove(toast)

    def clear_all_toasts(self):
        """Close all active toasts."""
        for toast in self._active_toasts.copy():
            toast.close_animated()

    def get_active_count(self) -> int:
        """Get number of active toasts."""
        return len(self._active_toasts)


# Global toast manager instance
toast_manager = ToastManager()


# Convenience functions
def show_info_toast(message: str, duration: int = 3000, position: str = "top-right"):
    """Show info toast."""
    return toast_manager.show_toast(message, "info", duration, position)


def show_success_toast(message: str, duration: int = 3000, position: str = "top-right"):
    """Show success toast."""
    return toast_manager.show_toast(message, "success", duration, position)


def show_warning_toast(message: str, duration: int = 3000, position: str = "top-right"):
    """Show warning toast."""
    return toast_manager.show_toast(message, "warning", duration, position)


def show_error_toast(message: str, duration: int = 5000, position: str = "top-right"):
    """Show error toast."""
    return toast_manager.show_toast(message, "error", duration, position)


class PersistentToast(NotificationToastWidget):
    """Toast that doesn't auto-dismiss."""

    def __init__(self, message="", toast_type="info", position="top-right", parent=None):
        super().__init__(message, toast_type, 0, position, parent)  # duration = 0

    def _setup_toast_ui(self):
        """Override to remove auto-dismiss."""
        super()._setup_toast_ui()
        # No auto-dismiss timer


class ActionToast(NotificationToastWidget):
    """Toast with prominent action buttons."""

    def __init__(self, message="", primary_action="", secondary_action="",
                 toast_type="info", parent=None):
        super().__init__(message, toast_type, 0, parent=parent)  # No auto-dismiss

        if primary_action:
            self.add_action(primary_action, "primary")

        if secondary_action:
            self.add_action(secondary_action, "secondary")


class ProgressToast(NotificationToastWidget):
    """Toast with progress indicator."""

    def __init__(self, message="", toast_type="info", parent=None):
        super().__init__(message, toast_type, 0, parent=parent)  # No auto-dismiss
        self._progress = 0
        self._add_progress_bar()

    def _add_progress_bar(self):
        """Add progress bar to toast."""
        from PyQt6.QtWidgets import QProgressBar

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 2px;
                background-color: rgba(255, 255, 255, 0.3);
            }}
            QProgressBar::chunk {{
                border-radius: 2px;
                background-color: white;
            }}
        """)

        # Add to message layout
        if hasattr(self, 'message_layout'):
            self.message_layout.addWidget(self.progress_bar)

    def set_progress(self, progress: int):
        """Update progress (0-100)."""
        self._progress = progress
        self.progress_bar.setValue(progress)

        # Auto-close when complete
        if progress >= 100:
            QTimer.singleShot(1000, self.close_animated)

    def get_progress(self) -> int:
        """Get current progress."""
        return self._progress