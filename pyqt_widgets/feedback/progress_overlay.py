"""
Progress overlay widget for blocking interactions during loading.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QMovie
from ..base.theme_manager import theme_manager


class ProgressOverlayWidget(QWidget):
    """Semi-transparent overlay with progress indicator."""

    cancelled = pyqtSignal()

    def __init__(self, message="Loading...", progress_type="spinner",
                 cancellable=False, parent=None):
        super().__init__(parent)
        self._message = message
        self._progress_type = progress_type  # "spinner", "bar", "dots"
        self._cancellable = cancellable
        self._progress_value = 0
        self._setup_ui()

    def _setup_ui(self):
        """Setup the progress overlay UI."""
        # Make overlay cover entire parent
        if self.parent():
            self.resize(self.parent().size())

        # Semi-transparent background
        self.setStyleSheet(f"""
            ProgressOverlayWidget {{
                background-color: rgba(0, 0, 0, 0.5);
            }}
        """)

        # Center content layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Content container
        self.content_container = QWidget()
        self.content_container.setFixedSize(200, 120)
        self.content_container.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_manager.get_color('surface')};
                border-radius: {theme_manager.get_border_radius('lg')}px;
                border: 1px solid {theme_manager.get_color('border')};
            }}
        """)

        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(16)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Progress indicator
        self._setup_progress_indicator(content_layout)

        # Message label
        self.message_label = QLabel(self._message)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setFont(theme_manager.get_font('default'))
        self.message_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        self.message_label.setWordWrap(True)
        content_layout.addWidget(self.message_label)

        # Cancel button
        if self._cancellable:
            from ..base.base_button import BaseButton
            self.cancel_btn = BaseButton("Cancel", "secondary", "small")
            self.cancel_btn.clicked.connect(self.cancelled.emit)
            content_layout.addWidget(self.cancel_btn)

        main_layout.addWidget(self.content_container)

        # Initially hidden
        self.hide()

    def _setup_progress_indicator(self, layout):
        """Setup progress indicator based on type."""
        if self._progress_type == "spinner":
            self._setup_spinner(layout)
        elif self._progress_type == "bar":
            self._setup_progress_bar(layout)
        elif self._progress_type == "dots":
            self._setup_dots_animation(layout)

    def _setup_spinner(self, layout):
        """Setup spinning progress indicator."""
        self.spinner_label = QLabel("⟳")
        self.spinner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinner_label.setFixedSize(32, 32)

        spinner_font = theme_manager.get_font('default')
        spinner_font.setPointSize(24)
        self.spinner_label.setFont(spinner_font)
        self.spinner_label.setStyleSheet(f"color: {theme_manager.get_color('primary')};")

        layout.addWidget(self.spinner_label)

        # Rotation animation
        from PyQt6.QtCore import QPropertyAnimation
        self.spinner_animation = QPropertyAnimation(self.spinner_label, b"rotation")
        self.spinner_animation.setDuration(1000)
        self.spinner_animation.setStartValue(0)
        self.spinner_animation.setEndValue(360)
        self.spinner_animation.setLoopCount(-1)  # Infinite loop

    def _setup_progress_bar(self, layout):
        """Setup progress bar indicator."""
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 4px;
                background-color: {theme_manager.get_color('light')};
            }}
            QProgressBar::chunk {{
                border-radius: 4px;
                background-color: {theme_manager.get_color('primary')};
            }}
        """)

        layout.addWidget(self.progress_bar)

    def _setup_dots_animation(self, layout):
        """Setup animated dots indicator."""
        dots_container = QWidget()
        dots_layout = QHBoxLayout(dots_container)
        dots_layout.setContentsMargins(0, 0, 0, 0)
        dots_layout.setSpacing(8)
        dots_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.dots = []
        for i in range(3):
            dot = QLabel("●")
            dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dot.setFixedSize(12, 12)
            dot.setStyleSheet(f"color: {theme_manager.get_color('primary')};")
            dots_layout.addWidget(dot)
            self.dots.append(dot)

        layout.addWidget(dots_container)

        # Animate dots
        self._setup_dots_animation_timer()

    def _setup_dots_animation_timer(self):
        """Setup timer for dots animation."""
        self.dots_timer = QTimer()
        self.dots_timer.timeout.connect(self._animate_dots)
        self.dots_current_dot = 0

    def _animate_dots(self):
        """Animate dots sequence."""
        # Reset all dots
        for dot in self.dots:
            dot.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")

        # Highlight current dot
        if self.dots:
            self.dots[self.dots_current_dot].setStyleSheet(f"color: {theme_manager.get_color('primary')};")
            self.dots_current_dot = (self.dots_current_dot + 1) % len(self.dots)

    def show_overlay(self):
        """Show the overlay with fade-in animation."""
        if self.parent():
            self.resize(self.parent().size())

        self.show()

        # Start animations based on type
        if self._progress_type == "spinner" and hasattr(self, 'spinner_animation'):
            self.spinner_animation.start()
        elif self._progress_type == "dots" and hasattr(self, 'dots_timer'):
            self.dots_timer.start(500)  # 500ms interval

        # Fade in animation
        from ..base.animation_helpers import AnimationHelpers
        AnimationHelpers.fade_in(self, 200)

    def hide_overlay(self):
        """Hide the overlay with fade-out animation."""
        # Stop animations
        if hasattr(self, 'spinner_animation'):
            self.spinner_animation.stop()
        if hasattr(self, 'dots_timer'):
            self.dots_timer.stop()

        # Fade out animation
        from ..base.animation_helpers import AnimationHelpers
        AnimationHelpers.fade_out(self, 200, self.hide)

    def set_message(self, message: str):
        """Update progress message."""
        self._message = message
        self.message_label.setText(message)

    def set_progress(self, progress: int):
        """Update progress value (0-100)."""
        self._progress_value = max(0, min(100, progress))

        if self._progress_type == "bar" and hasattr(self, 'progress_bar'):
            self.progress_bar.setValue(self._progress_value)

        # Auto-hide when complete
        if self._progress_value >= 100:
            QTimer.singleShot(500, self.hide_overlay)

    def get_progress(self) -> int:
        """Get current progress value."""
        return self._progress_value

    def get_message(self) -> str:
        """Get current message."""
        return self._message

    def resizeEvent(self, event):
        """Handle resize to maintain overlay coverage."""
        super().resizeEvent(event)
        if self.parent():
            self.resize(self.parent().size())


class SimpleLoadingOverlay(ProgressOverlayWidget):
    """Simple loading overlay with just spinner and message."""

    def __init__(self, message="Loading...", parent=None):
        super().__init__(message, "spinner", False, parent)


class ProgressBarOverlay(ProgressOverlayWidget):
    """Progress overlay with progress bar."""

    def __init__(self, message="Processing...", parent=None):
        super().__init__(message, "bar", True, parent)


class CustomProgressOverlay(ProgressOverlayWidget):
    """Customizable progress overlay."""

    def __init__(self, message="", custom_widget=None, parent=None):
        self._custom_widget = custom_widget
        super().__init__(message, "spinner", False, parent)

        if custom_widget:
            self._add_custom_widget()

    def _add_custom_widget(self):
        """Add custom widget to overlay."""
        if self._custom_widget and hasattr(self, 'content_container'):
            # Insert custom widget before message
            layout = self.content_container.layout()
            layout.insertWidget(layout.count() - 1, self._custom_widget)


class BlockingProgressOverlay(ProgressOverlayWidget):
    """Progress overlay that blocks all interactions."""

    def __init__(self, message="Please wait...", parent=None):
        super().__init__(message, "spinner", False, parent)

    def show_overlay(self):
        """Show overlay and block interactions."""
        super().show_overlay()

        # Block interactions by capturing all events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.grabKeyboard()
        self.grabMouse()

    def hide_overlay(self):
        """Hide overlay and restore interactions."""
        # Release event capture
        self.releaseKeyboard()
        self.releaseMouse()

        super().hide_overlay()

    def keyPressEvent(self, event):
        """Block all key events."""
        event.accept()  # Consume the event

    def mousePressEvent(self, event):
        """Block mouse events outside content area."""
        # Only allow clicks on content container
        if not self.content_container.geometry().contains(event.pos()):
            event.accept()
        else:
            super().mousePressEvent(event)


class ProgressOverlayManager:
    """Manager for showing progress overlays on widgets."""

    def __init__(self):
        self._overlays = {}

    def show_progress(self, widget: QWidget, message: str = "Loading...",
                      progress_type: str = "spinner", cancellable: bool = False):
        """Show progress overlay on widget."""
        if widget in self._overlays:
            self.hide_progress(widget)

        overlay = ProgressOverlayWidget(message, progress_type, cancellable, widget)
        overlay.cancelled.connect(lambda: self.hide_progress(widget))

        self._overlays[widget] = overlay
        overlay.show_overlay()

        return overlay

    def update_progress(self, widget: QWidget, progress: int, message: str = None):
        """Update progress for widget overlay."""
        if widget in self._overlays:
            overlay = self._overlays[widget]
            overlay.set_progress(progress)
            if message:
                overlay.set_message(message)

    def hide_progress(self, widget: QWidget):
        """Hide progress overlay for widget."""
        if widget in self._overlays:
            overlay = self._overlays[widget]
            overlay.hide_overlay()
            del self._overlays[widget]

    def hide_all_progress(self):
        """Hide all active progress overlays."""
        for widget in list(self._overlays.keys()):
            self.hide_progress(widget)

    def is_showing_progress(self, widget: QWidget) -> bool:
        """Check if widget has active progress overlay."""
        return widget in self._overlays


# Global progress overlay manager
progress_manager = ProgressOverlayManager()


# Convenience functions
def show_loading(widget: QWidget, message: str = "Loading..."):
    """Show loading overlay on widget."""
    return progress_manager.show_progress(widget, message, "spinner", False)


def show_progress(widget: QWidget, message: str = "Processing..."):
    """Show progress bar overlay on widget."""
    return progress_manager.show_progress(widget, message, "bar", True)


def update_progress(widget: QWidget, progress: int, message: str = None):
    """Update progress for widget."""
    progress_manager.update_progress(widget, progress, message)


def hide_loading(widget: QWidget):
    """Hide loading overlay for widget."""
    progress_manager.hide_progress(widget)