"""
Snackbar widget for bottom-floating action messages.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QApplication
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont
from ..base.base_popup import BasePopupWidget
from ..base.theme_manager import theme_manager


class SnackbarWidget(BasePopupWidget):
    """Bottom-floating snackbar with optional action."""

    action_clicked = pyqtSignal()

    def __init__(self, message="", action_text="", duration=4000, parent=None):
        super().__init__(parent, modal=False)
        self._message = message
        self._action_text = action_text
        self._duration = duration
        self._setup_snackbar_ui()

    def _setup_snackbar_ui(self):
        """Setup the snackbar UI."""
        self.setFixedHeight(48)
        self.setMinimumWidth(300)
        self.setMaximumWidth(600)

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(16, 0, 8, 0)
        main_layout.setSpacing(16)

        # Message
        self.message_label = QLabel(self._message)
        self.message_label.setFont(theme_manager.get_font('default'))
        self.message_label.setStyleSheet("color: white;")
        self.message_label.setWordWrap(True)
        main_layout.addWidget(self.message_label)

        main_layout.addStretch()

        # Action button
        if self._action_text:
            self.action_btn = QPushButton(self._action_text)
            self.action_btn.setFlat(True)
            self.action_btn.clicked.connect(self._on_action_clicked)
            self.action_btn.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background-color: transparent;
                    color: {theme_manager.get_color('primary')};
                    font-weight: bold;
                    padding: 8px 12px;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 4px;
                }}
            """)
            main_layout.addWidget(self.action_btn)

        # Close button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.setFlat(True)
        self.close_btn.clicked.connect(self.close_animated)
        self.close_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-color: transparent;
                color: white;
                font-size: 18px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 16px;
            }}
        """)
        main_layout.addWidget(self.close_btn)

        # Apply snackbar styling
        self.setStyleSheet(f"""
            SnackbarWidget {{
                background-color: {theme_manager.get_color('dark')};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}
        """)

        # Set layout
        self.layout.addLayout(main_layout)

        # Auto-dismiss timer
        if self._duration > 0:
            QTimer.singleShot(self._duration, self.close_animated)

    def _on_action_clicked(self):
        """Handle action button click."""
        self.action_clicked.emit()
        self.close_animated()

    def show_snackbar(self):
        """Show snackbar with slide-up animation."""
        screen = QApplication.instance().primaryScreen().availableGeometry()

        # Position at bottom center
        x = (screen.width() - self.width()) // 2
        y = screen.height() - 80  # 80px from bottom

        # Start below screen
        start_y = screen.height()
        self.move(x, start_y)
        self.show()

        # Animate slide up
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(QRect(x, start_y, self.width(), self.height()))
        animation.setEndValue(QRect(x, y, self.width(), self.height()))
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()

    def close_animated(self):
        """Close with slide-down animation."""
        screen = QApplication.instance().primaryScreen().availableGeometry()
        current_rect = self.geometry()
        end_y = screen.height()

        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(250)
        animation.setStartValue(current_rect)
        animation.setEndValue(QRect(current_rect.x(), end_y, current_rect.width(), current_rect.height()))
        animation.setEasingCurve(QEasingCurve.Type.InCubic)

        def on_animation_finished():
            self.close()
            self.closed.emit()

        animation.finished.connect(on_animation_finished)
        animation.start()

    def set_message(self, message: str):
        """Update snackbar message."""
        self._message = message
        self.message_label.setText(message)

    def set_action_text(self, action_text: str):
        """Update action button text."""
        self._action_text = action_text
        if hasattr(self, 'action_btn'):
            self.action_btn.setText(action_text)

    def get_message(self) -> str:
        """Get current message."""
        return self._message

    def get_action_text(self) -> str:
        """Get current action text."""
        return self._action_text


class SnackbarManager:
    """Manager for displaying snackbars sequentially."""

    def __init__(self):
        self._queue = []
        self._current_snackbar = None

    def show_snackbar(self, message: str, action_text: str = "", duration: int = 4000):
        """Show snackbar, queuing if another is active."""
        snackbar_info = {
            'message': message,
            'action_text': action_text,
            'duration': duration
        }

        if self._current_snackbar is None:
            self._show_next_snackbar(snackbar_info)
        else:
            self._queue.append(snackbar_info)

    def _show_next_snackbar(self, snackbar_info: dict):
        """Show the next snackbar."""
        self._current_snackbar = SnackbarWidget(
            snackbar_info['message'],
            snackbar_info['action_text'],
            snackbar_info['duration']
        )

        self._current_snackbar.closed.connect(self._on_snackbar_closed)
        self._current_snackbar.show_snackbar()

    def _on_snackbar_closed(self):
        """Handle snackbar close and show next in queue."""
        self._current_snackbar = None

        if self._queue:
            next_snackbar = self._queue.pop(0)
            self._show_next_snackbar(next_snackbar)

    def clear_queue(self):
        """Clear pending snackbars."""
        self._queue.clear()

    def close_current(self):
        """Close current snackbar."""
        if self._current_snackbar:
            self._current_snackbar.close_animated()

    def get_queue_length(self) -> int:
        """Get number of queued snackbars."""
        return len(self._queue)


# Global snackbar manager
snackbar_manager = SnackbarManager()


# Convenience functions
def show_snackbar(message: str, action_text: str = "", duration: int = 4000):
    """Show a snackbar message."""
    return snackbar_manager.show_snackbar(message, action_text, duration)


def show_undo_snackbar(message: str, duration: int = 4000):
    """Show snackbar with undo action."""
    return snackbar_manager.show_snackbar(message, "UNDO", duration)


def show_retry_snackbar(message: str, duration: int = 6000):
    """Show snackbar with retry action."""
    return snackbar_manager.show_snackbar(message, "RETRY", duration)


class CustomSnackbar(SnackbarWidget):
    """Customizable snackbar with different styles."""

    def __init__(self, message="", action_text="", duration=4000,
                 style="default", parent=None):
        self._style = style
        super().__init__(message, action_text, duration, parent)
        self._apply_custom_styling()

    def _apply_custom_styling(self):
        """Apply custom styling based on style type."""
        styles = {
            'success': {
                'bg': theme_manager.get_color('success'),
                'text': 'white',
                'action': 'white'
            },
            'warning': {
                'bg': theme_manager.get_color('warning'),
                'text': 'white',
                'action': 'white'
            },
            'error': {
                'bg': theme_manager.get_color('danger'),
                'text': 'white',
                'action': 'white'
            },
            'info': {
                'bg': theme_manager.get_color('info'),
                'text': 'white',
                'action': 'white'
            },
            'default': {
                'bg': theme_manager.get_color('dark'),
                'text': 'white',
                'action': theme_manager.get_color('primary')
            }
        }

        style_config = styles.get(self._style, styles['default'])

        self.setStyleSheet(f"""
            CustomSnackbar {{
                background-color: {style_config['bg']};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}
        """)

        if hasattr(self, 'message_label'):
            self.message_label.setStyleSheet(f"color: {style_config['text']};")

        if hasattr(self, 'action_btn'):
            self.action_btn.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background-color: transparent;
                    color: {style_config['action']};
                    font-weight: bold;
                    padding: 8px 12px;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 4px;
                }}
            """)


class PersistentSnackbar(SnackbarWidget):
    """Snackbar that doesn't auto-dismiss."""

    def __init__(self, message="", action_text="", parent=None):
        super().__init__(message, action_text, 0, parent)  # duration = 0


class ProgressSnackbar(SnackbarWidget):
    """Snackbar with progress indicator."""

    def __init__(self, message="", parent=None):
        super().__init__(message, "", 0, parent)  # No action, no auto-dismiss
        self._progress = 0
        self._add_progress_indicator()

    def _add_progress_indicator(self):
        """Add progress bar to snackbar."""
        from PyQt6.QtWidgets import QProgressBar

        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                background-color: rgba(255, 255, 255, 0.3);
                border-radius: 1px;
            }}
            QProgressBar::chunk {{
                background-color: {theme_manager.get_color('primary')};
                border-radius: 1px;
            }}
        """)

        # Add to bottom of snackbar
        if hasattr(self, 'layout'):
            progress_container = QWidget()
            progress_layout = QHBoxLayout(progress_container)
            progress_layout.setContentsMargins(0, 0, 0, 4)
            progress_layout.addWidget(self.progress_bar)

            self.layout.addWidget(progress_container)

    def set_progress(self, progress: int):
        """Update progress (0-100)."""
        self._progress = progress
        if hasattr(self, 'progress_bar'):
            self.progress_bar.setValue(progress)

        # Auto-close when complete
        if progress >= 100:
            QTimer.singleShot(1000, self.close_animated)

    def get_progress(self) -> int:
        """Get current progress."""
        return self._progress


class MultiActionSnackbar(SnackbarWidget):
    """Snackbar with multiple action buttons."""

    def __init__(self, message="", actions=None, duration=4000, parent=None):
        self._actions = actions or []  # List of (text, callback) tuples
        super().__init__(message, "", duration, parent)
        self._add_multiple_actions()

    def _add_multiple_actions(self):
        """Add multiple action buttons."""
        if not self._actions:
            return

        # Remove single action button if it exists
        if hasattr(self, 'action_btn'):
            self.action_btn.setParent(None)

        # Add multiple action buttons
        for action_text, callback in self._actions:
            action_btn = QPushButton(action_text)
            action_btn.setFlat(True)
            action_btn.clicked.connect(lambda checked, cb=callback: self._on_multi_action_clicked(cb))
            action_btn.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background-color: transparent;
                    color: {theme_manager.get_color('primary')};
                    font-weight: bold;
                    padding: 8px 12px;
                    margin-left: 4px;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 4px;
                }}
            """)

            # Add to main layout (before close button)
            if hasattr(self, 'layout') and self.layout.count() > 0:
                main_layout = self.layout.itemAt(0).layout()
                if main_layout:
                    # Insert before close button (last item)
                    main_layout.insertWidget(main_layout.count() - 1, action_btn)

    def _on_multi_action_clicked(self, callback):
        """Handle multi-action button click."""
        if callable(callback):
            callback()
        self.close_animated()