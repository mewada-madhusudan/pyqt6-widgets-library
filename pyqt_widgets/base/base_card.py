"""
Base card widget with optional header, body, and footer sections.
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPalette
from .theme_manager import theme_manager
from .animation_helpers import AnimatedWidget


class BaseCardWidget(AnimatedWidget):
    """Base card widget with header, body, and footer sections."""

    clicked = pyqtSignal()
    hover_entered = pyqtSignal()
    hover_left = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("BaseCardWidget")
        self._setup_ui()
        self._setup_styling()
        self._hoverable = True
        self._selectable = False
        self._selected = False

    def _setup_ui(self):
        """Setup the UI layout."""
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(1)

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Header section
        self.header_widget = QWidget()
        self.header_layout = QHBoxLayout(self.header_widget)
        self.header_layout.setContentsMargins(16, 12, 16, 12)
        self.main_layout.addWidget(self.header_widget)
        self.header_widget.hide()

        # Body section
        self.body_widget = QWidget()
        self.body_layout = QVBoxLayout(self.body_widget)
        self.body_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.addWidget(self.body_widget)

        # Footer section
        self.footer_widget = QWidget()
        self.footer_layout = QHBoxLayout(self.footer_widget)
        self.footer_layout.setContentsMargins(16, 12, 16, 12)
        self.main_layout.addWidget(self.footer_widget)
        self.footer_widget.hide()

    def _setup_styling(self):
        """Apply theme styling."""
        self.setStyleSheet(f"""
            BaseCardWidget {{
                background-color: {theme_manager.get_color('surface')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}

            BaseCardWidget:hover {{
                border-color: {theme_manager.get_color('primary')};
                background-color: {theme_manager.get_color('hover')};
            }}
        """)

    def set_header(self, widget: QWidget):
        """Set header widget."""
        # Clear existing header
        for i in reversed(range(self.header_layout.count())):
            self.header_layout.itemAt(i).widget().setParent(None)

        self.header_layout.addWidget(widget)
        self.header_widget.show()

    def set_body(self, widget: QWidget):
        """Set body widget."""
        # Clear existing body
        for i in reversed(range(self.body_layout.count())):
            self.body_layout.itemAt(i).widget().setParent(None)

        self.body_layout.addWidget(widget)

    def set_footer(self, widget: QWidget):
        """Set footer widget."""
        # Clear existing footer
        for i in reversed(range(self.footer_layout.count())):
            self.footer_layout.itemAt(i).widget().setParent(None)

        self.footer_layout.addWidget(widget)
        self.footer_widget.show()

    def add_header_action(self, button: QPushButton):
        """Add action button to header."""
        if not self.header_widget.isVisible():
            self.header_widget.show()
        self.header_layout.addWidget(button)

    def add_footer_action(self, button: QPushButton):
        """Add action button to footer."""
        if not self.footer_widget.isVisible():
            self.footer_widget.show()
        self.footer_layout.addWidget(button)

    def set_hoverable(self, hoverable: bool):
        """Enable/disable hover effects."""
        self._hoverable = hoverable

    def set_selectable(self, selectable: bool):
        """Enable/disable selection."""
        self._selectable = selectable

    def set_selected(self, selected: bool):
        """Set selection state."""
        if self._selectable:
            self._selected = selected
            self._update_selection_style()

    def is_selected(self) -> bool:
        """Check if card is selected."""
        return self._selected

    def _update_selection_style(self):
        """Update styling based on selection state."""
        if self._selected:
            self.setStyleSheet(f"""
                BaseCardWidget {{
                    background-color: {theme_manager.get_color('primary')};
                    border: 2px solid {theme_manager.get_color('primary')};
                    border-radius: {theme_manager.get_border_radius('md')}px;
                    color: white;
                }}
            """)
        else:
            self._setup_styling()

    def enterEvent(self, event):
        """Handle mouse enter event."""
        if self._hoverable:
            self.hover_entered.emit()
            # Add subtle animation
            self.animate_bounce_effect()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave event."""
        if self._hoverable:
            self.hover_left.emit()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse press event."""
        if event.button() == Qt.MouseButton.LeftButton:
            if self._selectable:
                self.set_selected(not self._selected)
            self.clicked.emit()
        super().mousePressEvent(event)

    def animate_bounce_effect(self):
        """Add subtle bounce animation on hover."""
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(150)

        current_rect = self.geometry()
        bounce_rect = current_rect.adjusted(-2, -2, 2, 2)

        animation.setStartValue(current_rect)
        animation.setEndValue(bounce_rect)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Return to original size
        return_animation = QPropertyAnimation(self, b"geometry")
        return_animation.setDuration(150)
        return_animation.setStartValue(bounce_rect)
        return_animation.setEndValue(current_rect)
        return_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        animation.finished.connect(return_animation.start)
        animation.start()