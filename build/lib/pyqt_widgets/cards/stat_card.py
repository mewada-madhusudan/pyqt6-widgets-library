"""
Statistics card widget for displaying metrics and KPIs.
"""

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPen
from ..base.base_card import BaseCardWidget
from ..base.theme_manager import theme_manager


class StatCardWidget(BaseCardWidget):
    """Card widget for displaying statistics and metrics."""

    value_changed = pyqtSignal(str)  # Emits new value

    def __init__(self, label="", value="0", unit="", trend=None, trend_value="", parent=None):
        super().__init__(parent)
        self._label = label
        self._value = value
        self._unit = unit
        self._trend = trend  # "up", "down", "neutral", None
        self._trend_value = trend_value
        self._setup_stat_ui()

    def _setup_stat_ui(self):
        """Setup the statistics card UI."""
        # Main content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)

        # Label
        if self._label:
            self.label_widget = QLabel(self._label)
            self.label_widget.setFont(theme_manager.get_font('default'))
            self.label_widget.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            content_layout.addWidget(self.label_widget)

        # Value section
        value_section = QWidget()
        value_layout = QHBoxLayout(value_section)
        value_layout.setContentsMargins(0, 0, 0, 0)
        value_layout.setSpacing(8)

        # Main value
        self.value_label = QLabel(self._value)
        value_font = theme_manager.get_font('heading')
        value_font.setPointSize(24)
        value_font.setWeight(QFont.Weight.Bold)
        self.value_label.setFont(value_font)
        self.value_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        value_layout.addWidget(self.value_label)

        # Unit
        if self._unit:
            self.unit_label = QLabel(self._unit)
            unit_font = theme_manager.get_font('default')
            unit_font.setPointSize(12)
            self.unit_label.setFont(unit_font)
            self.unit_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            self.unit_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
            value_layout.addWidget(self.unit_label)

        value_layout.addStretch()
        content_layout.addWidget(value_section)

        # Trend section
        if self._trend or self._trend_value:
            trend_section = QWidget()
            trend_layout = QHBoxLayout(trend_section)
            trend_layout.setContentsMargins(0, 0, 0, 0)
            trend_layout.setSpacing(4)

            # Trend arrow
            if self._trend:
                self.trend_arrow = QLabel()
                self.trend_arrow.setFixedSize(16, 16)
                self._update_trend_arrow()
                trend_layout.addWidget(self.trend_arrow)

            # Trend value
            if self._trend_value:
                self.trend_label = QLabel(self._trend_value)
                self.trend_label.setFont(theme_manager.get_font('caption'))
                self._update_trend_color()
                trend_layout.addWidget(self.trend_label)

            trend_layout.addStretch()
            content_layout.addWidget(trend_section)

        content_layout.addStretch()

        # Set the content as body
        self.set_body(content_widget)

    def _update_trend_arrow(self):
        """Update trend arrow based on trend direction."""
        if not hasattr(self, 'trend_arrow'):
            return

        # Create arrow pixmap
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set color based on trend
        if self._trend == "up":
            color = theme_manager.get_color('success')
            # Draw up arrow
            painter.setPen(QPen(color, 2))
            painter.drawLine(8, 12, 8, 4)  # Vertical line
            painter.drawLine(8, 4, 5, 7)  # Left diagonal
            painter.drawLine(8, 4, 11, 7)  # Right diagonal
        elif self._trend == "down":
            color = theme_manager.get_color('danger')
            # Draw down arrow
            painter.setPen(QPen(color, 2))
            painter.drawLine(8, 4, 8, 12)  # Vertical line
            painter.drawLine(8, 12, 5, 9)  # Left diagonal
            painter.drawLine(8, 12, 11, 9)  # Right diagonal
        else:  # neutral
            color = theme_manager.get_color('text_secondary')
            # Draw horizontal line
            painter.setPen(QPen(color, 2))
            painter.drawLine(4, 8, 12, 8)

        painter.end()
        self.trend_arrow.setPixmap(pixmap)

    def _update_trend_color(self):
        """Update trend label color based on trend direction."""
        if not hasattr(self, 'trend_label'):
            return

        if self._trend == "up":
            color = theme_manager.get_color('success')
        elif self._trend == "down":
            color = theme_manager.get_color('danger')
        else:
            color = theme_manager.get_color('text_secondary')

        self.trend_label.setStyleSheet(f"color: {color};")

    def set_value(self, value: str):
        """Update the main value."""
        old_value = self._value
        self._value = value
        if hasattr(self, 'value_label'):
            self.value_label.setText(value)
        self.value_changed.emit(value)

    def set_label(self, label: str):
        """Update the label."""
        self._label = label
        if hasattr(self, 'label_widget'):
            self.label_widget.setText(label)

    def set_unit(self, unit: str):
        """Update the unit."""
        self._unit = unit
        if hasattr(self, 'unit_label'):
            self.unit_label.setText(unit)

    def set_trend(self, trend: str, trend_value: str = ""):
        """Update trend information."""
        self._trend = trend
        self._trend_value = trend_value

        if hasattr(self, 'trend_arrow'):
            self._update_trend_arrow()
        if hasattr(self, 'trend_label'):
            if trend_value:
                self.trend_label.setText(trend_value)
            self._update_trend_color()
        else:
            # Recreate UI to add trend section
            self._setup_stat_ui()

    def get_value(self) -> str:
        """Get current value."""
        return self._value

    def get_label(self) -> str:
        """Get current label."""
        return self._label

    def get_trend(self) -> tuple:
        """Get current trend as (direction, value)."""
        return (self._trend, self._trend_value)


class ProgressStatCard(StatCardWidget):
    """Statistics card with progress bar."""

    def __init__(self, label="", value="0", max_value="100", unit="", parent=None):
        self._max_value = max_value
        self._progress_percentage = 0
        super().__init__(label, value, unit, parent=parent)
        self._add_progress_bar()
        self._update_progress()

    def _add_progress_bar(self):
        """Add progress bar to the card."""
        from PyQt6.QtWidgets import QProgressBar

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 3px;
                background-color: {theme_manager.get_color('light')};
            }}
            QProgressBar::chunk {{
                border-radius: 3px;
                background-color: {theme_manager.get_color('primary')};
            }}
        """)

        # Add to body layout
        if hasattr(self, 'body_layout'):
            self.body_layout.addWidget(self.progress_bar)

    def _update_progress(self):
        """Update progress bar based on current value."""
        try:
            current = float(self._value.replace(',', ''))
            maximum = float(self._max_value.replace(',', ''))
            self._progress_percentage = int((current / maximum) * 100) if maximum > 0 else 0

            if hasattr(self, 'progress_bar'):
                self.progress_bar.setValue(self._progress_percentage)
        except (ValueError, AttributeError):
            self._progress_percentage = 0

    def set_value(self, value: str):
        """Override to update progress bar."""
        super().set_value(value)
        self._update_progress()

    def set_max_value(self, max_value: str):
        """Update maximum value."""
        self._max_value = max_value
        self._update_progress()

    def get_progress_percentage(self) -> int:
        """Get current progress percentage."""
        return self._progress_percentage


class ComparisonStatCard(StatCardWidget):
    """Statistics card comparing two values."""

    def __init__(self, label="", current_value="0", previous_value="0", unit="", parent=None):
        self._previous_value = previous_value

        # Calculate trend automatically
        try:
            current = float(current_value.replace(',', ''))
            previous = float(previous_value.replace(',', ''))

            if current > previous:
                trend = "up"
                change = ((current - previous) / previous) * 100 if previous != 0 else 0
                trend_value = f"+{change:.1f}%"
            elif current < previous:
                trend = "down"
                change = ((previous - current) / previous) * 100 if previous != 0 else 0
                trend_value = f"-{change:.1f}%"
            else:
                trend = "neutral"
                trend_value = "0%"
        except (ValueError, ZeroDivisionError):
            trend = "neutral"
            trend_value = "N/A"

        super().__init__(label, current_value, unit, trend, trend_value, parent)

    def set_comparison_values(self, current_value: str, previous_value: str):
        """Update both current and previous values."""
        self._previous_value = previous_value
        self.set_value(current_value)

        # Recalculate trend
        try:
            current = float(current_value.replace(',', ''))
            previous = float(previous_value.replace(',', ''))

            if current > previous:
                trend = "up"
                change = ((current - previous) / previous) * 100 if previous != 0 else 0
                trend_value = f"+{change:.1f}%"
            elif current < previous:
                trend = "down"
                change = ((previous - current) / previous) * 100 if previous != 0 else 0
                trend_value = f"-{change:.1f}%"
            else:
                trend = "neutral"
                trend_value = "0%"
        except (ValueError, ZeroDivisionError):
            trend = "neutral"
            trend_value = "N/A"

        self.set_trend(trend, trend_value)

    def get_previous_value(self) -> str:
        """Get previous value."""
        return self._previous_value


class IconStatCard(StatCardWidget):
    """Statistics card with icon."""

    def __init__(self, label="", value="0", unit="", icon=None, icon_color=None, parent=None):
        self._icon = icon
        self._icon_color = icon_color or theme_manager.get_color('primary')
        super().__init__(label, value, unit, parent=parent)
        self._add_icon()

    def _add_icon(self):
        """Add icon to the card."""
        if not self._icon:
            return

        # Create header with icon
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Icon
        icon_label = QLabel()
        icon_label.setFixedSize(32, 32)

        if isinstance(self._icon, str):
            # Load from file path
            pixmap = QPixmap(self._icon)
            if not pixmap.isNull():
                icon_label.setPixmap(pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio,
                                                   Qt.TransformationMode.SmoothTransformation))

        icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: {self._icon_color};
                border-radius: 16px;
                padding: 8px;
            }}
        """)

        header_layout.addWidget(icon_label)
        header_layout.addStretch()

        self.set_header(header_widget)

    def set_icon(self, icon, color=None):
        """Update icon."""
        self._icon = icon
        if color:
            self._icon_color = color
        self._add_icon()