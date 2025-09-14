"""
Base popup widget with configurable alignment and animation.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QColor
from .theme_manager import theme_manager
from .animation_helpers import AnimationHelpers


class BasePopupWidget(QFrame):
    """Base popup widget with backdrop and animations."""

    closed = pyqtSignal()

    def __init__(self, parent=None, modal=True):
        super().__init__(parent)
        self._modal = modal
        self._auto_close_timer = None
        self._setup_ui()
        self._setup_styling()

    def _setup_ui(self):
        """Setup the UI."""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        if self._modal:
            self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

    def _setup_styling(self):
        """Apply styling."""
        self.setStyleSheet(f"""
            BasePopupWidget {{
                background-color: {theme_manager.get_color('surface')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('lg')}px;
            }}
        """)

    def show_at_position(self, x: int, y: int):
        """Show popup at specific position."""
        self.move(x, y)
        self.show()
        AnimationHelpers.fade_in(self, 200)

    def show_centered(self, parent_widget: QWidget = None):
        """Show popup centered on parent or screen."""
        if parent_widget:
            parent_rect = parent_widget.geometry()
            x = parent_rect.x() + (parent_rect.width() - self.width()) // 2
            y = parent_rect.y() + (parent_rect.height() - self.height()) // 2
        else:
            # Center on screen
            screen = self.screen().geometry()
            x = (screen.width() - self.width()) // 2
            y = (screen.height() - self.height()) // 2

        self.show_at_position(x, y)

    def show_at_cursor(self):
        """Show popup at current cursor position."""
        from PyQt6.QtGui import QCursor
        cursor_pos = QCursor.pos()
        self.show_at_position(cursor_pos.x(), cursor_pos.y())

    def auto_close(self, delay_ms: int):
        """Auto close popup after delay."""
        if self._auto_close_timer:
            self._auto_close_timer.stop()

        self._auto_close_timer = QTimer()
        self._auto_close_timer.timeout.connect(self.close_animated)
        self._auto_close_timer.setSingleShot(True)
        self._auto_close_timer.start(delay_ms)

    def close_animated(self):
        """Close with fade out animation."""

        def on_fade_complete():
            self.close()
            self.closed.emit()

        AnimationHelpers.fade_out(self, 200, on_fade_complete)

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Escape:
            self.close_animated()
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse press for backdrop clicks."""
        # Close on backdrop click if modal
        if self._modal and event.button() == Qt.MouseButton.LeftButton:
            # Check if click is outside the content area
            content_rect = self.rect()
            if not content_rect.contains(event.pos()):
                self.close_animated()
        super().mousePressEvent(event)


class ToastPopup(BasePopupWidget):
    """Toast notification popup."""

    def __init__(self, message: str, duration: int = 3000, parent=None):
        super().__init__(parent, modal=False)
        self._message = message
        self._duration = duration
        self._setup_toast_ui()

    def _setup_toast_ui(self):
        """Setup toast-specific UI."""
        from PyQt6.QtWidgets import QLabel

        self.setFixedSize(300, 60)

        # Message label
        self.message_label = QLabel(self._message)
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.message_label)

        # Auto close
        self.auto_close(self._duration)

    def show_toast(self, position="top-right"):
        """Show toast at specified position."""
        screen = self.screen().geometry()

        if position == "top-right":
            x = screen.width() - self.width() - 20
            y = 20
        elif position == "top-left":
            x = 20
            y = 20
        elif position == "bottom-right":
            x = screen.width() - self.width() - 20
            y = screen.height() - self.height() - 20
        elif position == "bottom-left":
            x = 20
            y = screen.height() - self.height() - 20
        else:  # center
            x = (screen.width() - self.width()) // 2
            y = (screen.height() - self.height()) // 2

        self.show_at_position(x, y)


class ContextMenuPopup(BasePopupWidget):
    """Context menu popup."""

    def __init__(self, parent=None):
        super().__init__(parent, modal=False)
        self._actions = []
        self._setup_menu_ui()

    def _setup_menu_ui(self):
        """Setup context menu UI."""
        from PyQt6.QtWidgets import QVBoxLayout

        self.menu_layout = QVBoxLayout()
        self.menu_layout.setContentsMargins(4, 4, 4, 4)
        self.menu_layout.setSpacing(2)
        self.layout.addLayout(self.menu_layout)

    def add_action(self, text: str, callback=None, icon=None):
        """Add menu action."""
        from PyQt6.QtWidgets import QPushButton

        action_btn = QPushButton(text)
        action_btn.setFlat(True)
        action_btn.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 8px 12px;
                border: none;
                background-color: transparent;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)

        if callback:
            action_btn.clicked.connect(callback)
            action_btn.clicked.connect(self.close_animated)

        self.menu_layout.addWidget(action_btn)
        self._actions.append(action_btn)

        # Adjust size
        self.adjustSize()

    def add_separator(self):
        """Add menu separator."""
        from PyQt6.QtWidgets import QFrame

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"color: {theme_manager.get_color('border')};")
        self.menu_layout.addWidget(separator)