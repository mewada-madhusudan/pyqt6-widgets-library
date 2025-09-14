"""
Toggle switch widget with smooth animations.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect, pyqtProperty
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QFont
from ..base.theme_manager import theme_manager


class ToggleSwitchWidget(QWidget):
    """Modern toggle switch with smooth animations."""

    toggled = pyqtSignal(bool)  # Emits new state

    def __init__(self, checked=False, text="", parent=None):
        super().__init__(parent)
        self._checked = checked
        self._text = text
        self._animation_duration = 200
        self._thumb_position = 0.0
        self._setup_ui()
        self._setup_animation()

    def _setup_ui(self):
        """Setup the toggle switch UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Switch dimensions
        self._switch_width = 50
        self._switch_height = 24
        self._thumb_size = 20
        self._thumb_margin = 2

        # Set widget size
        self.setFixedSize(
            self._switch_width + (100 if self._text else 0),
            max(self._switch_height, 20)
        )

        # Text label (optional)
        if self._text:
            self.label = QLabel(self._text)
            self.label.setFont(theme_manager.get_font('default'))
            self.label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
            layout.addWidget(self.label)

        # Set initial thumb position
        self._thumb_position = 1.0 if self._checked else 0.0

    def _setup_animation(self):
        """Setup thumb animation."""
        self._animation = QPropertyAnimation(self, b"thumbPosition")
        self._animation.setDuration(self._animation_duration)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    @pyqtProperty(float)
    def thumbPosition(self):
        """Get thumb position (0.0 to 1.0)."""
        return self._thumb_position

    @thumbPosition.setter
    def thumbPosition(self, position):
        """Set thumb position and trigger repaint."""
        self._thumb_position = position
        self.update()

    def mousePressEvent(self, event):
        """Handle mouse press to toggle switch."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle()

    def toggle(self):
        """Toggle the switch state."""
        self.setChecked(not self._checked)

    def setChecked(self, checked: bool):
        """Set switch state with animation."""
        if checked != self._checked:
            self._checked = checked

            # Animate thumb position
            target_position = 1.0 if checked else 0.0
            self._animation.setStartValue(self._thumb_position)
            self._animation.setEndValue(target_position)
            self._animation.start()

            self.toggled.emit(checked)

    def isChecked(self) -> bool:
        """Get current switch state."""
        return self._checked

    def setText(self, text: str):
        """Set label text."""
        self._text = text
        if hasattr(self, 'label'):
            self.label.setText(text)
        else:
            self._setup_ui()  # Recreate UI with label

    def getText(self) -> str:
        """Get label text."""
        return self._text

    def setAnimationDuration(self, duration: int):
        """Set animation duration in milliseconds."""
        self._animation_duration = duration
        self._animation.setDuration(duration)

    def paintEvent(self, event):
        """Paint the toggle switch."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate switch area (right side if there's text)
        switch_x = self.width() - self._switch_width if self._text else 0
        switch_y = (self.height() - self._switch_height) // 2

        # Colors based on state
        if self._checked:
            track_color = QColor(theme_manager.get_color('primary'))
            thumb_color = QColor('white')
        else:
            track_color = QColor(theme_manager.get_color('border'))
            thumb_color = QColor('white')

        # Draw track (background)
        track_rect = QRect(switch_x, switch_y, self._switch_width, self._switch_height)
        painter.setBrush(QBrush(track_color))
        painter.setPen(QPen(track_color))
        painter.drawRoundedRect(track_rect, self._switch_height // 2, self._switch_height // 2)

        # Calculate thumb position
        thumb_travel = self._switch_width - self._thumb_size - (2 * self._thumb_margin)
        thumb_x = switch_x + self._thumb_margin + (thumb_travel * self._thumb_position)
        thumb_y = switch_y + self._thumb_margin

        # Draw thumb
        thumb_rect = QRect(int(thumb_x), thumb_y, self._thumb_size, self._thumb_size)
        painter.setBrush(QBrush(thumb_color))
        painter.setPen(QPen(QColor(theme_manager.get_color('border')), 1))
        painter.drawEllipse(thumb_rect)

        # Add shadow effect to thumb
        shadow_color = QColor(0, 0, 0, 30)
        painter.setBrush(QBrush(shadow_color))
        painter.setPen(Qt.PenStyle.NoPen)
        shadow_rect = QRect(int(thumb_x + 1), thumb_y + 1, self._thumb_size, self._thumb_size)
        painter.drawEllipse(shadow_rect)

        # Redraw thumb on top
        painter.setBrush(QBrush(thumb_color))
        painter.setPen(QPen(QColor(theme_manager.get_color('border')), 1))
        painter.drawEllipse(thumb_rect)


class LabeledToggleSwitch(QWidget):
    """Toggle switch with customizable labels for on/off states."""

    toggled = pyqtSignal(bool)

    def __init__(self, on_text="ON", off_text="OFF", checked=False, parent=None):
        super().__init__(parent)
        self._on_text = on_text
        self._off_text = off_text
        self._checked = checked
        self._setup_ui()

    def _setup_ui(self):
        """Setup labeled toggle switch."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Off label
        self.off_label = QLabel(self._off_text)
        self.off_label.setFont(theme_manager.get_font('caption'))
        layout.addWidget(self.off_label)

        # Toggle switch
        self.switch = ToggleSwitchWidget(self._checked)
        self.switch.toggled.connect(self._on_toggled)
        layout.addWidget(self.switch)

        # On label
        self.on_label = QLabel(self._on_text)
        self.on_label.setFont(theme_manager.get_font('caption'))
        layout.addWidget(self.on_label)

        self._update_labels()

    def _on_toggled(self, checked):
        """Handle switch toggle."""
        self._checked = checked
        self._update_labels()
        self.toggled.emit(checked)

    def _update_labels(self):
        """Update label styles based on state."""
        active_color = theme_manager.get_color('primary')
        inactive_color = theme_manager.get_color('text_secondary')

        if self._checked:
            self.on_label.setStyleSheet(f"color: {active_color}; font-weight: bold;")
            self.off_label.setStyleSheet(f"color: {inactive_color};")
        else:
            self.off_label.setStyleSheet(f"color: {active_color}; font-weight: bold;")
            self.on_label.setStyleSheet(f"color: {inactive_color};")

    def setChecked(self, checked: bool):
        """Set switch state."""
        self.switch.setChecked(checked)

    def isChecked(self) -> bool:
        """Get switch state."""
        return self.switch.isChecked()

    def setLabels(self, on_text: str, off_text: str):
        """Set label texts."""
        self._on_text = on_text
        self._off_text = off_text
        self.on_label.setText(on_text)
        self.off_label.setText(off_text)


class IconToggleSwitch(ToggleSwitchWidget):
    """Toggle switch with icons instead of text."""

    def __init__(self, on_icon="✓", off_icon="✗", checked=False, parent=None):
        self._on_icon = on_icon
        self._off_icon = off_icon
        super().__init__(checked, "", parent)

    def paintEvent(self, event):
        """Paint toggle switch with icons."""
        # Call parent paint method for switch background
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw icon on thumb
        switch_x = self.width() - self._switch_width if self._text else 0
        switch_y = (self.height() - self._switch_height) // 2

        thumb_travel = self._switch_width - self._thumb_size - (2 * self._thumb_margin)
        thumb_x = switch_x + self._thumb_margin + (thumb_travel * self._thumb_position)
        thumb_y = switch_y + self._thumb_margin

        # Choose icon based on state
        icon = self._on_icon if self._checked else self._off_icon

        # Draw icon
        painter.setPen(QPen(QColor(theme_manager.get_color('text'))))
        font = QFont(theme_manager.get_font('default'))
        font.setPointSize(8)
        painter.setFont(font)

        icon_rect = QRect(int(thumb_x), thumb_y, self._thumb_size, self._thumb_size)
        painter.drawText(icon_rect, Qt.AlignmentFlag.AlignCenter, icon)


class ToggleSwitchGroup(QWidget):
    """Group of toggle switches with coordinated behavior."""

    switches_changed = pyqtSignal(dict)  # Emits all switch states

    def __init__(self, parent=None):
        super().__init__(parent)
        self._switches = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup switch group."""
        from PyQt6.QtWidgets import QVBoxLayout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)

    def add_switch(self, name: str, text: str, checked: bool = False):
        """Add a switch to the group."""
        switch = ToggleSwitchWidget(checked, text)
        switch.toggled.connect(lambda state, n=name: self._on_switch_toggled(n, state))

        self._switches[name] = switch
        self.layout.addWidget(switch)

    def _on_switch_toggled(self, name: str, state: bool):
        """Handle switch toggle."""
        states = {name: switch.isChecked() for name, switch in self._switches.items()}
        self.switches_changed.emit(states)

    def get_states(self) -> dict:
        """Get all switch states."""
        return {name: switch.isChecked() for name, switch in self._switches.items()}

    def set_states(self, states: dict):
        """Set switch states."""
        for name, state in states.items():
            if name in self._switches:
                self._switches[name].setChecked(state)

    def get_switch(self, name: str) -> ToggleSwitchWidget:
        """Get specific switch."""
        return self._switches.get(name)