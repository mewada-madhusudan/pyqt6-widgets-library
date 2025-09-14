"""
Expandable card widget with collapsible content.
"""

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QTransform
from ..base.base_card import BaseCardWidget
from ..base.theme_manager import theme_manager
from ..base.animation_helpers import AnimationHelpers


class ExpandableCardWidget(BaseCardWidget):
    """Card widget with expandable/collapsible content."""

    expanded = pyqtSignal(bool)  # Emits expansion state

    def __init__(self, title="", expanded=False, parent=None):
        super().__init__(parent)
        self._title = title
        self._expanded = expanded
        self._content_widget = None
        self._animation = None
        self._setup_expandable_ui()

    def _setup_expandable_ui(self):
        """Setup the expandable card UI."""
        # Header with title and expand button
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        # Title
        self.title_label = QLabel(self._title)
        title_font = theme_manager.get_font('heading')
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        # Expand/collapse button
        self.expand_button = QPushButton()
        self.expand_button.setFixedSize(24, 24)
        self.expand_button.setFlat(True)
        self.expand_button.clicked.connect(self._toggle_expansion)
        self._update_expand_button()
        header_layout.addWidget(self.expand_button)

        self.set_header(header_widget)

        # Content container
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Set initial state
        if not self._expanded:
            self.content_container.hide()

        self.set_body(self.content_container)

    def _update_expand_button(self):
        """Update expand button appearance."""
        if self._expanded:
            # Down arrow (expanded state)
            arrow_text = "▼"
        else:
            # Right arrow (collapsed state)
            arrow_text = "▶"

        self.expand_button.setText(arrow_text)
        self.expand_button.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-color: transparent;
                color: {theme_manager.get_color('text_secondary')};
                font-size: 12px;
            }}
            QPushButton:hover {{
                color: {theme_manager.get_color('primary')};
            }}
        """)

    def _toggle_expansion(self):
        """Toggle expansion state with animation."""
        self._expanded = not self._expanded
        self._update_expand_button()

        if self._expanded:
            self._expand_content()
        else:
            self._collapse_content()

        self.expanded.emit(self._expanded)

    def _expand_content(self):
        """Expand content with animation."""
        if self.content_container.isVisible():
            return

        # Show content first to measure size
        self.content_container.show()
        self.content_container.adjustSize()

        # Get target height
        target_height = self.content_container.sizeHint().height()

        # Start from height 0
        self.content_container.setFixedHeight(0)

        # Animate to target height
        self._animation = QPropertyAnimation(self.content_container, b"maximumHeight")
        self._animation.setDuration(300)
        self._animation.setStartValue(0)
        self._animation.setEndValue(target_height)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        def on_expand_finished():
            self.content_container.setMaximumHeight(16777215)  # Remove height constraint

        self._animation.finished.connect(on_expand_finished)
        self._animation.start()

    def _collapse_content(self):
        """Collapse content with animation."""
        if not self.content_container.isVisible():
            return

        # Get current height
        current_height = self.content_container.height()

        # Animate to height 0
        self._animation = QPropertyAnimation(self.content_container, b"maximumHeight")
        self._animation.setDuration(300)
        self._animation.setStartValue(current_height)
        self._animation.setEndValue(0)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        def on_collapse_finished():
            self.content_container.hide()

        self._animation.finished.connect(on_collapse_finished)
        self._animation.start()

    def set_content(self, widget: QWidget):
        """Set the expandable content."""
        # Clear existing content
        for i in reversed(range(self.content_layout.count())):
            item = self.content_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        self.content_layout.addWidget(widget)
        self._content_widget = widget

        # Adjust visibility based on current state
        if self._expanded:
            self.content_container.show()
        else:
            self.content_container.hide()

    def add_content_widget(self, widget: QWidget):
        """Add widget to content area."""
        self.content_layout.addWidget(widget)

    def set_title(self, title: str):
        """Update title."""
        self._title = title
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)

    def set_expanded(self, expanded: bool, animate: bool = True):
        """Set expansion state programmatically."""
        if self._expanded == expanded:
            return

        self._expanded = expanded
        self._update_expand_button()

        if animate:
            if expanded:
                self._expand_content()
            else:
                self._collapse_content()
        else:
            # Immediate change without animation
            if expanded:
                self.content_container.show()
                self.content_container.setMaximumHeight(16777215)
            else:
                self.content_container.hide()

        self.expanded.emit(self._expanded)

    def is_expanded(self) -> bool:
        """Check if card is expanded."""
        return self._expanded

    def get_title(self) -> str:
        """Get current title."""
        return self._title


class AccordionCard(ExpandableCardWidget):
    """Expandable card designed for accordion layouts."""

    def __init__(self, title="", content_text="", parent=None):
        super().__init__(title, False, parent)

        if content_text:
            content_label = QLabel(content_text)
            content_label.setWordWrap(True)
            content_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
            self.set_content(content_label)

    def set_content_text(self, text: str):
        """Set content as text."""
        content_label = QLabel(text)
        content_label.setWordWrap(True)
        content_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        self.set_content(content_label)


class CollapsibleSection(ExpandableCardWidget):
    """Collapsible section for organizing content."""

    def __init__(self, title="", parent=None):
        super().__init__(title, True, parent)  # Start expanded
        self._setup_section_styling()

    def _setup_section_styling(self):
        """Apply section-specific styling."""
        # Remove card border for seamless integration
        self.setStyleSheet(f"""
            CollapsibleSection {{
                background-color: transparent;
                border: none;
                border-bottom: 1px solid {theme_manager.get_color('border')};
                border-radius: 0px;
            }}
        """)

        # Style header differently
        if hasattr(self, 'title_label'):
            section_font = theme_manager.get_font('heading')
            section_font.setPointSize(12)
            self.title_label.setFont(section_font)


class StepCard(ExpandableCardWidget):
    """Expandable card for step-by-step processes."""

    def __init__(self, step_number: int, title="", completed=False, parent=None):
        self._step_number = step_number
        self._completed = completed
        super().__init__(title, False, parent)
        self._setup_step_ui()

    def _setup_step_ui(self):
        """Setup step-specific UI elements."""
        # Add step number and completion indicator to header
        if hasattr(self, 'header_layout'):
            # Step number circle
            step_label = QLabel(str(self._step_number))
            step_label.setFixedSize(24, 24)
            step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if self._completed:
                step_label.setText("✓")
                bg_color = theme_manager.get_color('success')
            else:
                bg_color = theme_manager.get_color('primary')

            step_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {bg_color};
                    color: white;
                    border-radius: 12px;
                    font-weight: bold;
                    font-size: 10px;
                }}
            """)

            # Insert at beginning of header
            self.header_layout.insertWidget(0, step_label)

    def set_completed(self, completed: bool):
        """Mark step as completed."""
        self._completed = completed
        self._setup_step_ui()

    def is_completed(self) -> bool:
        """Check if step is completed."""
        return self._completed

    def get_step_number(self) -> int:
        """Get step number."""
        return self._step_number