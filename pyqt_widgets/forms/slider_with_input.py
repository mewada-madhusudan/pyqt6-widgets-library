"""
Slider with numeric input field widget.
"""

from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QSlider,
                           QSpinBox, QDoubleSpinBox, QLabel, QLineEdit)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QValidator, QDoubleValidator, QIntValidator
from ..base.theme_manager import theme_manager
from typing import Union


class SliderWithInputWidget(QWidget):
    """Slider combined with numeric input field."""

    value_changed = pyqtSignal(float)  # Emits current value

    def __init__(self, minimum=0, maximum=100, value=0, decimals=0,
                 label="", suffix="", parent=None):
        super().__init__(parent)
        self._minimum = minimum
        self._maximum = maximum
        self._value = value
        self._decimals = decimals
        self._label = label
        self._suffix = suffix
        self._updating = False
        self._setup_ui()

    def _setup_ui(self):
        """Setup the slider with input UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Label (optional)
        if self._label:
            label_widget = QLabel(self._label)
            label_widget.setFont(theme_manager.get_font('default'))
            label_widget.setStyleSheet(f"color: {theme_manager.get_color('text')};")
            layout.addWidget(label_widget)

        # Main control layout
        control_layout = QHBoxLayout()
        control_layout.setSpacing(12)

        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(int(self._minimum * (10 ** self._decimals)))
        self.slider.setMaximum(int(self._maximum * (10 ** self._decimals)))
        self.slider.setValue(int(self._value * (10 ** self._decimals)))
        self.slider.valueChanged.connect(self._on_slider_changed)

        # Style slider
        self.slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                border: 1px solid {theme_manager.get_color('border')};
                height: 6px;
                background: {theme_manager.get_color('surface')};
                border-radius: 3px;
            }}
            
            QSlider::handle:horizontal {{
                background: {theme_manager.get_color('primary')};
                border: 2px solid {theme_manager.get_color('primary')};
                width: 16px;
                height: 16px;
                border-radius: 8px;
                margin: -6px 0;
            }}
            
            QSlider::handle:horizontal:hover {{
                background: {theme_manager.get_color('hover')};
                border-color: {theme_manager.get_color('hover')};
            }}
            
            QSlider::sub-page:horizontal {{
                background: {theme_manager.get_color('primary')};
                border-radius: 3px;
            }}
            
            QSlider::add-page:horizontal {{
                background: {theme_manager.get_color('surface')};
                border-radius: 3px;
            }}
        """)

        control_layout.addWidget(self.slider, 1)

        # Input field
        if self._decimals > 0:
            self.input_field = QDoubleSpinBox()
            self.input_field.setDecimals(self._decimals)
        else:
            self.input_field = QSpinBox()

        self.input_field.setMinimum(self._minimum)
        self.input_field.setMaximum(self._maximum)
        self.input_field.setValue(self._value)

        if self._suffix:
            self.input_field.setSuffix(f" {self._suffix}")

        self.input_field.valueChanged.connect(self._on_input_changed)

        # Style input field
        self.input_field.setStyleSheet(f"""
            QSpinBox, QDoubleSpinBox {{
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                padding: 4px 8px;
                background-color: {theme_manager.get_color('background')};
                color: {theme_manager.get_color('text')};
                min-width: 80px;
            }}
            QSpinBox:focus, QDoubleSpinBox:focus {{
                border-color: {theme_manager.get_color('primary')};
            }}
            QSpinBox::up-button, QDoubleSpinBox::up-button {{
                border: none;
                background: {theme_manager.get_color('surface')};
                width: 16px;
            }}
            QSpinBox::down-button, QDoubleSpinBox::down-button {{
                border: none;
                background: {theme_manager.get_color('surface')};
                width: 16px;
            }}
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
                border: 2px solid {theme_manager.get_color('text')};
                border-width: 0 2px 2px 0;
                width: 4px;
                height: 4px;
                transform: rotate(-45deg);
            }}
            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
                border: 2px solid {theme_manager.get_color('text')};
                border-width: 2px 2px 0 0;
                width: 4px;
                height: 4px;
                transform: rotate(45deg);
            }}
        """)

        control_layout.addWidget(self.input_field)

        layout.addLayout(control_layout)

        # Value display (optional)
        value_layout = QHBoxLayout()

        self.min_label = QLabel(str(self._minimum))
        self.min_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')}; font-size: 8pt;")
        value_layout.addWidget(self.min_label)

        value_layout.addStretch()

        self.max_label = QLabel(str(self._maximum))
        self.max_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')}; font-size: 8pt;")
        value_layout.addWidget(self.max_label)

        layout.addLayout(value_layout)

    def _on_slider_changed(self, value):
        """Handle slider value change."""
        if self._updating:
            return

        self._updating = True

        # Convert slider value back to actual value
        actual_value = value / (10 ** self._decimals)
        self._value = actual_value

        # Update input field
        self.input_field.setValue(actual_value)

        self._updating = False
        self.value_changed.emit(actual_value)

    def _on_input_changed(self, value):
        """Handle input field value change."""
        if self._updating:
            return

        self._updating = True

        self._value = value

        # Update slider
        slider_value = int(value * (10 ** self._decimals))
        self.slider.setValue(slider_value)

        self._updating = False
        self.value_changed.emit(value)

    def set_value(self, value: float):
        """Set current value."""
        if self._minimum <= value <= self._maximum:
            self._value = value

            self._updating = True
            self.slider.setValue(int(value * (10 ** self._decimals)))
            self.input_field.setValue(value)
            self._updating = False

    def get_value(self) -> float:
        """Get current value."""
        return self._value

    def set_range(self, minimum: float, maximum: float):
        """Set value range."""
        self._minimum = minimum
        self._maximum = maximum

        # Update controls
        self.slider.setMinimum(int(minimum * (10 ** self._decimals)))
        self.slider.setMaximum(int(maximum * (10 ** self._decimals)))

        self.input_field.setMinimum(minimum)
        self.input_field.setMaximum(maximum)

        # Update labels
        self.min_label.setText(str(minimum))
        self.max_label.setText(str(maximum))

        # Ensure current value is within range
        if self._value < minimum:
            self.set_value(minimum)
        elif self._value > maximum:
            self.set_value(maximum)

    def get_range(self) -> tuple:
        """Get value range."""
        return (self._minimum, self._maximum)

    def set_label(self, label: str):
        """Set label text."""
        self._label = label
        # Note: Would need to rebuild UI to add/remove label

    def set_suffix(self, suffix: str):
        """Set value suffix."""
        self._suffix = suffix
        if self._suffix:
            self.input_field.setSuffix(f" {self._suffix}")
        else:
            self.input_field.setSuffix("")


class RangeSliderWidget(QWidget):
    """Dual slider for selecting value ranges."""

    range_changed = pyqtSignal(float, float)  # min_value, max_value

    def __init__(self, minimum=0, maximum=100, min_value=20, max_value=80,
                 decimals=0, parent=None):
        super().__init__(parent)
        self._minimum = minimum
        self._maximum = maximum
        self._min_value = min_value
        self._max_value = max_value
        self._decimals = decimals
        self._setup_ui()

    def _setup_ui(self):
        """Setup range slider UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Min value slider
        min_layout = QHBoxLayout()
        min_layout.addWidget(QLabel("Min:"))

        self.min_slider = SliderWithInputWidget(
            self._minimum, self._maximum, self._min_value, self._decimals
        )
        self.min_slider.value_changed.connect(self._on_min_changed)
        min_layout.addWidget(self.min_slider)

        layout.addLayout(min_layout)

        # Max value slider
        max_layout = QHBoxLayout()
        max_layout.addWidget(QLabel("Max:"))

        self.max_slider = SliderWithInputWidget(
            self._minimum, self._maximum, self._max_value, self._decimals
        )
        self.max_slider.value_changed.connect(self._on_max_changed)
        max_layout.addWidget(self.max_slider)

        layout.addLayout(max_layout)

    def _on_min_changed(self, value):
        """Handle min value change."""
        if value > self._max_value:
            self._max_value = value
            self.max_slider.set_value(value)

        self._min_value = value
        self.range_changed.emit(self._min_value, self._max_value)

    def _on_max_changed(self, value):
        """Handle max value change."""
        if value < self._min_value:
            self._min_value = value
            self.min_slider.set_value(value)

        self._max_value = value
        self.range_changed.emit(self._min_value, self._max_value)

    def set_range(self, min_value: float, max_value: float):
        """Set selected range."""
        self._min_value = min_value
        self._max_value = max_value

        self.min_slider.set_value(min_value)
        self.max_slider.set_value(max_value)

    def get_range(self) -> tuple:
        """Get selected range."""
        return (self._min_value, self._max_value)


class SimpleSliderInput(QWidget):
    """Simplified slider with input."""

    value_changed = pyqtSignal(int)

    def __init__(self, minimum=0, maximum=100, value=50, parent=None):
        super().__init__(parent)
        self._setup_ui(minimum, maximum, value)

    def _setup_ui(self, minimum, maximum, value):
        """Setup simple slider input."""
        layout = QHBoxLayout(self)

        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(minimum, maximum)
        self.slider.setValue(value)
        self.slider.valueChanged.connect(self._on_value_changed)
        layout.addWidget(self.slider)

        # Value display
        self.value_label = QLabel(str(value))
        self.value_label.setMinimumWidth(40)
        self.value_label.setStyleSheet(f"""
            QLabel {{
                border: 1px solid {theme_manager.get_color('border')};
                padding: 4px 8px;
                background-color: {theme_manager.get_color('surface')};
                color: {theme_manager.get_color('text')};
            }}
        """)
        layout.addWidget(self.value_label)

    def _on_value_changed(self, value):
        """Handle value change."""
        self.value_label.setText(str(value))
        self.value_changed.emit(value)

    def get_value(self) -> int:
        """Get current value."""
        return self.slider.value()

    def set_value(self, value: int):
        """Set current value."""
        self.slider.setValue(value)