"""
Quick settings panel widget - collapsible settings with common options.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QScrollArea, QCheckBox,
                             QComboBox, QSpinBox, QSlider, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QFont, QIcon
from ..base.theme_manager import theme_manager
from ..forms.toggle_switch import ToggleSwitchWidget
from typing import Dict, Any


class QuickSettingsPanel(QWidget):
    """Collapsible settings panel with common options."""

    setting_changed = pyqtSignal(str, object)  # setting_name, value
    settings_applied = pyqtSignal(dict)  # all settings
    panel_toggled = pyqtSignal(bool)  # expanded state

    def __init__(self, title="Settings", collapsible=True, parent=None):
        super().__init__(parent)
        self._title = title
        self._collapsible = collapsible
        self._expanded = True
        self._settings = {}
        self._setting_widgets = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup the settings panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        self.header = self._create_header()
        layout.addWidget(self.header)

        # Content area (scrollable)
        self.content_scroll = QScrollArea()
        self.content_scroll.setWidgetResizable(True)
        self.content_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarNever)
        self.content_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(12, 8, 12, 8)
        self.content_layout.setSpacing(12)

        self.content_scroll.setWidget(self.content_widget)
        layout.addWidget(self.content_scroll)

        # Apply/Reset buttons
        self.button_frame = self._create_buttons()
        layout.addWidget(self.button_frame)

        # Style the panel
        self.setStyleSheet(f"""
            QuickSettingsPanel {{
                background-color: {theme_manager.get_color('surface')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}
        """)

        # Animation for collapse/expand
        if self._collapsible:
            self._setup_animation()

    def _create_header(self):
        """Create panel header."""
        header = QFrame()
        header.setFrameShape(QFrame.Shape.Box)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
                border-radius: {theme_manager.get_border_radius('md')}px {theme_manager.get_border_radius('md')}px 0 0;
                padding: 8px 12px;
            }}
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(8, 8, 8, 8)

        # Title
        title_label = QLabel(self._title)
        title_font = theme_manager.get_font('heading')
        title_font.setPointSize(10)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(title_label)

        layout.addStretch()

        # Collapse/Expand button
        if self._collapsible:
            self.toggle_btn = QPushButton("▼")
            self.toggle_btn.setFixedSize(24, 24)
            self.toggle_btn.clicked.connect(self.toggle_panel)
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                    color: white;
                    font-weight: bold;
                    font-size: 12pt;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 12px;
                }
            """)
            layout.addWidget(self.toggle_btn)

        return header

    def _create_buttons(self):
        """Create action buttons."""
        button_frame = QFrame()
        button_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {theme_manager.get_color('background')};
                border-top: 1px solid {theme_manager.get_color('border')};
                border-radius: 0 0 {theme_manager.get_border_radius('md')}px {theme_manager.get_border_radius('md')}px;
            }}
        """)

        layout = QHBoxLayout(button_frame)
        layout.setContentsMargins(12, 8, 12, 8)

        # Reset button
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_settings)

        # Apply button
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.apply_settings)

        layout.addWidget(self.reset_btn)
        layout.addStretch()
        layout.addWidget(self.apply_btn)

        # Style buttons
        button_style = f"""
            QPushButton {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
                border: none;
                padding: 6px 16px;
                border-radius: {theme_manager.get_border_radius('sm')}px;
                font-weight: bold;
                min-width: 60px;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
            QPushButton:pressed {{
                background-color: {theme_manager.get_color('dark')};
            }}
        """

        self.reset_btn.setStyleSheet(button_style.replace(
            theme_manager.get_color('primary'),
            theme_manager.get_color('secondary')
        ))
        self.apply_btn.setStyleSheet(button_style)

        return button_frame

    def _setup_animation(self):
        """Setup collapse/expand animation."""
        self._animation = QPropertyAnimation(self, b"maximumHeight")
        self._animation.setDuration(300)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def toggle_panel(self):
        """Toggle panel expanded/collapsed state."""
        if not self._collapsible:
            return

        self._expanded = not self._expanded

        if self._expanded:
            self.toggle_btn.setText("▼")
            target_height = self.sizeHint().height()
            self.content_scroll.show()
            self.button_frame.show()
        else:
            self.toggle_btn.setText("▶")
            target_height = self.header.sizeHint().height()
            self.content_scroll.hide()
            self.button_frame.hide()

        if hasattr(self, '_animation'):
            self._animation.setStartValue(self.height())
            self._animation.setEndValue(target_height)
            self._animation.start()

        self.panel_toggled.emit(self._expanded)

    def add_toggle_setting(self, name: str, label: str, default_value: bool = False,
                           description: str = ""):
        """Add a toggle switch setting."""
        group = self._create_setting_group(label, description)

        toggle = ToggleSwitchWidget(default_value)
        toggle.toggled.connect(lambda value, n=name: self._on_setting_changed(n, value))

        group.layout().addWidget(toggle)
        self.content_layout.addWidget(group)

        self._settings[name] = default_value
        self._setting_widgets[name] = toggle

    def add_choice_setting(self, name: str, label: str, choices: list,
                           default_index: int = 0, description: str = ""):
        """Add a dropdown choice setting."""
        group = self._create_setting_group(label, description)

        combo = QComboBox()
        combo.addItems([str(choice) for choice in choices])
        combo.setCurrentIndex(default_index)
        combo.currentTextChanged.connect(lambda value, n=name: self._on_setting_changed(n, value))

        combo.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                padding: 4px 8px;
                background-color: {theme_manager.get_color('background')};
                color: {theme_manager.get_color('text')};
                min-width: 120px;
            }}
            QComboBox:focus {{
                border-color: {theme_manager.get_color('primary')};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                border: 2px solid {theme_manager.get_color('text')};
                border-width: 0 2px 2px 0;
                width: 4px;
                height: 4px;
                transform: rotate(45deg);
            }}
        """)

        group.layout().addWidget(combo)
        self.content_layout.addWidget(group)

        self._settings[name] = choices[default_index] if choices else None
        self._setting_widgets[name] = combo

    def add_number_setting(self, name: str, label: str, default_value: int = 0,
                           minimum: int = 0, maximum: int = 100, description: str = ""):
        """Add a numeric setting with spinbox."""
        group = self._create_setting_group(label, description)

        spinbox = QSpinBox()
        spinbox.setRange(minimum, maximum)
        spinbox.setValue(default_value)
        spinbox.valueChanged.connect(lambda value, n=name: self._on_setting_changed(n, value))

        spinbox.setStyleSheet(f"""
            QSpinBox {{
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                padding: 4px 8px;
                background-color: {theme_manager.get_color('background')};
                color: {theme_manager.get_color('text')};
                min-width: 80px;
            }}
            QSpinBox:focus {{
                border-color: {theme_manager.get_color('primary')};
            }}
        """)

        group.layout().addWidget(spinbox)
        self.content_layout.addWidget(group)

        self._settings[name] = default_value
        self._setting_widgets[name] = spinbox

    def add_slider_setting(self, name: str, label: str, default_value: int = 50,
                           minimum: int = 0, maximum: int = 100, description: str = ""):
        """Add a slider setting."""
        group = self._create_setting_group(label, description)

        slider_layout = QHBoxLayout()

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(minimum, maximum)
        slider.setValue(default_value)

        value_label = QLabel(str(default_value))
        value_label.setMinimumWidth(30)
        value_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")

        def on_slider_changed(value):
            value_label.setText(str(value))
            self._on_setting_changed(name, value)

        slider.valueChanged.connect(on_slider_changed)

        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)

        group.layout().addLayout(slider_layout)
        self.content_layout.addWidget(group)

        self._settings[name] = default_value
        self._setting_widgets[name] = slider

    def _create_setting_group(self, label: str, description: str = ""):
        """Create a setting group container."""
        group = QGroupBox()
        group.setStyleSheet(f"""
            QGroupBox {{
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                margin-top: 8px;
                padding-top: 8px;
                background-color: {theme_manager.get_color('background')};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
                color: {theme_manager.get_color('text')};
                font-weight: bold;
            }}
        """)

        layout = QVBoxLayout(group)
        layout.setContentsMargins(8, 8, 8, 8)

        # Label
        label_widget = QLabel(label)
        label_widget.setFont(theme_manager.get_font('default'))
        label_widget.setStyleSheet(f"color: {theme_manager.get_color('text')}; font-weight: bold;")
        layout.addWidget(label_widget)

        # Description (optional)
        if description:
            desc_label = QLabel(description)
            desc_label.setFont(theme_manager.get_font('caption'))
            desc_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        return group

    def _on_setting_changed(self, name: str, value):
        """Handle setting value change."""
        self._settings[name] = value
        self.setting_changed.emit(name, value)

    def apply_settings(self):
        """Apply all current settings."""
        self.settings_applied.emit(self._settings.copy())

    def reset_settings(self):
        """Reset all settings to defaults."""
        for name, widget in self._setting_widgets.items():
            if isinstance(widget, ToggleSwitchWidget):
                widget.setChecked(False)
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            elif isinstance(widget, (QSpinBox, QSlider)):
                widget.setValue(0)

    def get_settings(self) -> dict:
        """Get all current settings."""
        return self._settings.copy()

    def set_settings(self, settings: dict):
        """Set multiple settings."""
        for name, value in settings.items():
            if name in self._setting_widgets:
                widget = self._setting_widgets[name]

                if isinstance(widget, ToggleSwitchWidget):
                    widget.setChecked(bool(value))
                elif isinstance(widget, QComboBox):
                    index = widget.findText(str(value))
                    if index >= 0:
                        widget.setCurrentIndex(index)
                elif isinstance(widget, (QSpinBox, QSlider)):
                    widget.setValue(int(value))

                self._settings[name] = value

    def get_setting(self, name: str):
        """Get specific setting value."""
        return self._settings.get(name)

    def set_setting(self, name: str, value):
        """Set specific setting value."""
        if name in self._setting_widgets:
            widget = self._setting_widgets[name]

            if isinstance(widget, ToggleSwitchWidget):
                widget.setChecked(bool(value))
            elif isinstance(widget, QComboBox):
                index = widget.findText(str(value))
                if index >= 0:
                    widget.setCurrentIndex(index)
            elif isinstance(widget, (QSpinBox, QSlider)):
                widget.setValue(int(value))

            self._settings[name] = value


class CompactSettingsPanel(QWidget):
    """Compact version of settings panel."""

    setting_changed = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup compact settings."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        self.setStyleSheet(f"""
            CompactSettingsPanel {{
                background-color: {theme_manager.get_color('surface')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
            }}
        """)

    def add_setting(self, name: str, widget: QWidget):
        """Add a setting widget."""
        self.layout().addWidget(widget)
        self._settings[name] = widget

    def get_settings(self) -> dict:
        """Get all settings."""
        return self._settings