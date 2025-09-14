"""
Form stepper widget for multi-step form navigation.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QStackedWidget, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPainter, QPen, QBrush, QFont
from ..base.theme_manager import theme_manager
from typing import List, Dict, Any


class FormStepperWidget(QWidget):
    """Multi-step form navigation widget with progress indicator."""

    step_changed = pyqtSignal(int)  # Emits current step index
    step_completed = pyqtSignal(int)  # Emits completed step index
    form_completed = pyqtSignal(dict)  # Emits all form data

    def __init__(self, parent=None):
        super().__init__(parent)
        self._steps = []
        self._current_step = 0
        self._completed_steps = set()
        self._step_data = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup the form stepper UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Progress indicator
        self.progress_widget = StepProgressIndicator()
        layout.addWidget(self.progress_widget)

        # Content area
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {theme_manager.get_color('background')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
                padding: 16px;
            }}
        """)
        layout.addWidget(self.content_stack)

        # Navigation buttons
        nav_layout = QHBoxLayout()

        self.prev_btn = QPushButton("Previous")
        self.prev_btn.setEnabled(False)
        self.prev_btn.clicked.connect(self.previous_step)

        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.next_step)

        self.finish_btn = QPushButton("Finish")
        self.finish_btn.hide()
        self.finish_btn.clicked.connect(self._finish_form)

        nav_layout.addStretch()
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)
        nav_layout.addWidget(self.finish_btn)

        layout.addLayout(nav_layout)

        # Style buttons
        button_style = f"""
            QPushButton {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: {theme_manager.get_border_radius('sm')}px;
                font-weight: bold;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
            QPushButton:disabled {{
                background-color: {theme_manager.get_color('border')};
                color: {theme_manager.get_color('text_secondary')};
            }}
        """

        self.prev_btn.setStyleSheet(button_style)
        self.next_btn.setStyleSheet(button_style)
        self.finish_btn.setStyleSheet(button_style)

    def add_step(self, title: str, widget: QWidget, description: str = "",
                 validation_func=None):
        """Add a step to the form."""
        step_info = {
            'title': title,
            'description': description,
            'widget': widget,
            'validation_func': validation_func
        }

        self._steps.append(step_info)
        self.content_stack.addWidget(widget)
        self.progress_widget.add_step(title, description)

        # Update navigation
        self._update_navigation()

    def remove_step(self, index: int):
        """Remove a step from the form."""
        if 0 <= index < len(self._steps):
            step = self._steps.pop(index)
            self.content_stack.removeWidget(step['widget'])
            self.progress_widget.remove_step(index)

            # Adjust current step if necessary
            if self._current_step >= len(self._steps):
                self._current_step = max(0, len(self._steps) - 1)

            self._update_navigation()

    def next_step(self):
        """Move to next step."""
        if self._current_step < len(self._steps) - 1:
            # Validate current step
            current_step_info = self._steps[self._current_step]
            if current_step_info['validation_func']:
                if not current_step_info['validation_func']():
                    return  # Validation failed

            # Mark current step as completed
            self._completed_steps.add(self._current_step)
            self.step_completed.emit(self._current_step)

            # Move to next step
            self._current_step += 1
            self._update_current_step()

    def previous_step(self):
        """Move to previous step."""
        if self._current_step > 0:
            self._current_step -= 1
            self._update_current_step()

    def go_to_step(self, step_index: int):
        """Go to specific step."""
        if 0 <= step_index < len(self._steps):
            self._current_step = step_index
            self._update_current_step()

    def _update_current_step(self):
        """Update UI for current step."""
        self.content_stack.setCurrentIndex(self._current_step)
        self.progress_widget.set_current_step(self._current_step)
        self._update_navigation()
        self.step_changed.emit(self._current_step)

    def _update_navigation(self):
        """Update navigation button states."""
        if not self._steps:
            return

        # Previous button
        self.prev_btn.setEnabled(self._current_step > 0)

        # Next/Finish buttons
        is_last_step = self._current_step == len(self._steps) - 1

        if is_last_step:
            self.next_btn.hide()
            self.finish_btn.show()
        else:
            self.next_btn.show()
            self.finish_btn.hide()

    def _finish_form(self):
        """Finish the form."""
        # Validate final step
        current_step_info = self._steps[self._current_step]
        if current_step_info['validation_func']:
            if not current_step_info['validation_func']():
                return

        # Mark final step as completed
        self._completed_steps.add(self._current_step)
        self.step_completed.emit(self._current_step)

        # Emit completion signal with all data
        self.form_completed.emit(self._step_data.copy())

    def set_step_data(self, step_index: int, data: dict):
        """Set data for a specific step."""
        self._step_data[step_index] = data

    def get_step_data(self, step_index: int) -> dict:
        """Get data for a specific step."""
        return self._step_data.get(step_index, {})

    def get_all_data(self) -> dict:
        """Get all form data."""
        return self._step_data.copy()

    def get_current_step(self) -> int:
        """Get current step index."""
        return self._current_step

    def get_step_count(self) -> int:
        """Get total number of steps."""
        return len(self._steps)

    def is_step_completed(self, step_index: int) -> bool:
        """Check if step is completed."""
        return step_index in self._completed_steps

    def reset_form(self):
        """Reset form to initial state."""
        self._current_step = 0
        self._completed_steps.clear()
        self._step_data.clear()
        self._update_current_step()


class StepProgressIndicator(QWidget):
    """Visual progress indicator for form steps."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._steps = []
        self._current_step = 0
        self._completed_steps = set()
        self.setFixedHeight(80)

    def add_step(self, title: str, description: str = ""):
        """Add a step to the indicator."""
        self._steps.append({'title': title, 'description': description})
        self.update()

    def remove_step(self, index: int):
        """Remove a step from the indicator."""
        if 0 <= index < len(self._steps):
            self._steps.pop(index)
            self.update()

    def set_current_step(self, step_index: int):
        """Set current active step."""
        self._current_step = step_index
        self.update()

    def set_completed_steps(self, completed_steps: set):
        """Set completed steps."""
        self._completed_steps = completed_steps
        self.update()

    def paintEvent(self, event):
        """Paint the progress indicator."""
        if not self._steps:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate positions
        width = self.width() - 40  # Margins
        step_width = width / len(self._steps) if len(self._steps) > 1 else width

        # Colors
        active_color = theme_manager.get_color('primary')
        completed_color = theme_manager.get_color('success')
        inactive_color = theme_manager.get_color('border')
        text_color = theme_manager.get_color('text')

        # Draw connecting lines
        if len(self._steps) > 1:
            line_y = 25
            painter.setPen(QPen(QBrush(inactive_color), 2))

            for i in range(len(self._steps) - 1):
                x1 = 20 + i * step_width + 15  # Circle center + radius
                x2 = 20 + (i + 1) * step_width - 15  # Next circle center - radius

                # Change color if step is completed
                if i in self._completed_steps:
                    painter.setPen(QPen(QBrush(completed_color), 2))
                else:
                    painter.setPen(QPen(QBrush(inactive_color), 2))

                painter.drawLine(x1, line_y, x2, line_y)

        # Draw step circles and labels
        for i, step in enumerate(self._steps):
            x = 20 + i * step_width
            circle_center_x = x
            circle_y = 25

            # Determine circle color
            if i in self._completed_steps:
                circle_color = completed_color
                text_color_circle = 'white'
                circle_text = "✓"
            elif i == self._current_step:
                circle_color = active_color
                text_color_circle = 'white'
                circle_text = str(i + 1)
            else:
                circle_color = inactive_color
                text_color_circle = theme_manager.get_color('text_secondary')
                circle_text = str(i + 1)

            # Draw circle
            painter.setBrush(QBrush(circle_color))
            painter.setPen(QPen(QBrush(circle_color), 1))
            painter.drawEllipse(circle_center_x - 15, circle_y - 15, 30, 30)

            # Draw circle text
            painter.setPen(QPen(QBrush(text_color_circle), 1))
            font = QFont(theme_manager.get_font('default'))
            font.setBold(True)
            painter.setFont(font)

            text_rect = painter.fontMetrics().boundingRect(circle_text)
            text_x = circle_center_x - text_rect.width() // 2
            text_y = circle_y + text_rect.height() // 2 - 2
            painter.drawText(text_x, text_y, circle_text)

            # Draw step title
            painter.setPen(QPen(QBrush(text_color), 1))
            title_font = QFont(theme_manager.get_font('default'))
            if i == self._current_step:
                title_font.setBold(True)
            painter.setFont(title_font)

            title_rect = painter.fontMetrics().boundingRect(step['title'])
            title_x = circle_center_x - title_rect.width() // 2
            title_y = circle_y + 25
            painter.drawText(title_x, title_y, step['title'])


class SimpleFormStepper(QWidget):
    """Simplified form stepper with basic navigation."""

    step_changed = pyqtSignal(int)

    def __init__(self, steps: List[str], parent=None):
        super().__init__(parent)
        self._step_titles = steps
        self._current_step = 0
        self._setup_ui()

    def _setup_ui(self):
        """Setup simple stepper."""
        layout = QVBoxLayout(self)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(len(self._step_titles) - 1)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Current step label
        self.step_label = QLabel(f"Step 1 of {len(self._step_titles)}: {self._step_titles[0]}")
        self.step_label.setFont(theme_manager.get_font('heading'))
        layout.addWidget(self.step_label)

        # Navigation
        nav_layout = QHBoxLayout()

        self.prev_btn = QPushButton("Previous")
        self.prev_btn.setEnabled(False)
        self.prev_btn.clicked.connect(self.previous_step)

        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.next_step)

        nav_layout.addWidget(self.prev_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_btn)

        layout.addLayout(nav_layout)

    def next_step(self):
        """Move to next step."""
        if self._current_step < len(self._step_titles) - 1:
            self._current_step += 1
            self._update_ui()

    def previous_step(self):
        """Move to previous step."""
        if self._current_step > 0:
            self._current_step -= 1
            self._update_ui()

    def _update_ui(self):
        """Update UI for current step."""
        self.progress_bar.setValue(self._current_step)
        self.step_label.setText(
            f"Step {self._current_step + 1} of {len(self._step_titles)}: "
            f"{self._step_titles[self._current_step]}"
        )

        self.prev_btn.setEnabled(self._current_step > 0)
        self.next_btn.setEnabled(self._current_step < len(self._step_titles) - 1)

        self.step_changed.emit(self._current_step)

    def get_current_step(self) -> int:
        """Get current step."""
        return self._current_step