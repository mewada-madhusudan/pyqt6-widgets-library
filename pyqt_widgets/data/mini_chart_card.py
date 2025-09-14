"""
Mini chart card widget for inline data visualization.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from ..base.base_card import BaseCardWidget
from ..base.theme_manager import theme_manager


class MiniChartCard(BaseCardWidget):
    """Card widget with inline chart visualization."""

    chart_clicked = pyqtSignal(int)  # Emits clicked data point index

    def __init__(self, title="", data=None, chart_type="line", parent=None):
        super().__init__(parent)
        self._title = title
        self._data = data or []
        self._chart_type = chart_type  # "line", "bar", "sparkline"
        self._max_value = None
        self._min_value = None
        self._setup_ui()

    def _setup_ui(self):
        """Setup the mini chart card UI."""
        # Main container
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Title
        if self._title:
            title_label = QLabel(self._title)
            title_font = theme_manager.get_font('heading')
            title_font.setPointSize(12)
            title_label.setFont(title_font)
            title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
            layout.addWidget(title_label)

        # Chart area
        self.chart_widget = ChartWidget(self._data, self._chart_type)
        self.chart_widget.setMinimumHeight(60)
        self.chart_widget.point_clicked.connect(self.chart_clicked.emit)
        layout.addWidget(self.chart_widget)

        # Stats row
        if self._data:
            stats_layout = QHBoxLayout()

            # Min value
            min_val = min(self._data) if self._data else 0
            min_label = QLabel(f"Min: {min_val}")
            min_label.setFont(theme_manager.get_font('caption'))
            min_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            stats_layout.addWidget(min_label)

            stats_layout.addStretch()

            # Max value
            max_val = max(self._data) if self._data else 0
            max_label = QLabel(f"Max: {max_val}")
            max_label.setFont(theme_manager.get_font('caption'))
            max_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            stats_layout.addWidget(max_label)

            layout.addLayout(stats_layout)

        self.set_body(container)

    def set_data(self, data: list):
        """Update chart data."""
        self._data = data
        self.chart_widget.set_data(data)
        self._setup_ui()  # Refresh UI with new data

    def set_chart_type(self, chart_type: str):
        """Change chart type."""
        self._chart_type = chart_type
        self.chart_widget.set_chart_type(chart_type)

    def get_data(self) -> list:
        """Get current data."""
        return self._data.copy()


class ChartWidget(QWidget):
    """Widget for rendering mini charts."""

    point_clicked = pyqtSignal(int)  # Emits clicked point index

    def __init__(self, data=None, chart_type="line", parent=None):
        super().__init__(parent)
        self._data = data or []
        self._chart_type = chart_type
        self._hover_index = -1
        self.setMouseTracking(True)

    def set_data(self, data: list):
        """Update chart data."""
        self._data = data
        self.update()

    def set_chart_type(self, chart_type: str):
        """Change chart type."""
        self._chart_type = chart_type
        self.update()

    def paintEvent(self, event):
        """Paint the chart."""
        if not self._data:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Get drawing area
        rect = self.rect()
        margin = 10
        chart_rect = rect.adjusted(margin, margin, -margin, -margin)

        if self._chart_type == "line":
            self._draw_line_chart(painter, chart_rect)
        elif self._chart_type == "bar":
            self._draw_bar_chart(painter, chart_rect)
        elif self._chart_type == "sparkline":
            self._draw_sparkline(painter, chart_rect)

        painter.end()

    def _draw_line_chart(self, painter: QPainter, rect):
        """Draw line chart."""
        if len(self._data) < 2:
            return

        # Calculate scaling
        min_val = min(self._data)
        max_val = max(self._data)
        val_range = max_val - min_val if max_val != min_val else 1

        width = rect.width()
        height = rect.height()

        # Draw grid lines
        painter.setPen(QPen(QColor(theme_manager.get_color('border')), 1))
        for i in range(5):
            y = rect.top() + (i * height / 4)
            painter.drawLine(rect.left(), y, rect.right(), y)

        # Draw line
        painter.setPen(QPen(QColor(theme_manager.get_color('primary')), 2))

        points = []
        for i, value in enumerate(self._data):
            x = rect.left() + (i * width / (len(self._data) - 1))
            y = rect.bottom() - ((value - min_val) / val_range * height)
            points.append((x, y))

        # Draw line segments
        for i in range(len(points) - 1):
            painter.drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])

        # Draw points
        painter.setBrush(QBrush(QColor(theme_manager.get_color('primary'))))
        for i, (x, y) in enumerate(points):
            radius = 4 if i == self._hover_index else 2
            painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

    def _draw_bar_chart(self, painter: QPainter, rect):
        """Draw bar chart."""
        if not self._data:
            return

        # Calculate scaling
        max_val = max(self._data) if self._data else 1

        width = rect.width()
        height = rect.height()
        bar_width = width / len(self._data) * 0.8
        spacing = width / len(self._data) * 0.2

        # Draw bars
        for i, value in enumerate(self._data):
            bar_height = (value / max_val) * height
            x = rect.left() + i * (bar_width + spacing)
            y = rect.bottom() - bar_height

            # Color based on hover
            if i == self._hover_index:
                color = theme_manager.get_color('primary')
            else:
                color = theme_manager.get_color('secondary')

            painter.setBrush(QBrush(QColor(color)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(x, y, bar_width, bar_height)

    def _draw_sparkline(self, painter: QPainter, rect):
        """Draw minimal sparkline."""
        if len(self._data) < 2:
            return

        # Calculate scaling
        min_val = min(self._data)
        max_val = max(self._data)
        val_range = max_val - min_val if max_val != min_val else 1

        width = rect.width()
        height = rect.height()

        # Draw line only
        painter.setPen(QPen(QColor(theme_manager.get_color('primary')), 1))

        points = []
        for i, value in enumerate(self._data):
            x = rect.left() + (i * width / (len(self._data) - 1))
            y = rect.bottom() - ((value - min_val) / val_range * height)
            points.append((x, y))

        # Draw line segments
        for i in range(len(points) - 1):
            painter.drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])

    def mouseMoveEvent(self, event):
        """Handle mouse move for hover effects."""
        if not self._data:
            return

        # Find closest data point
        pos = event.position()
        rect = self.rect()
        margin = 10
        chart_rect = rect.adjusted(margin, margin, -margin, -margin)

        closest_index = -1
        min_distance = float('inf')

        for i in range(len(self._data)):
            x = chart_rect.left() + (i * chart_rect.width() / (len(self._data) - 1))
            distance = abs(pos.x() - x)

            if distance < min_distance and distance < 20:  # 20px threshold
                min_distance = distance
                closest_index = i

        if closest_index != self._hover_index:
            self._hover_index = closest_index
            self.update()

        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse click."""
        if event.button() == Qt.MouseButton.LeftButton and self._hover_index >= 0:
            self.point_clicked.emit(self._hover_index)
        super().mousePressEvent(event)

    def leaveEvent(self, event):
        """Clear hover state when mouse leaves."""
        self._hover_index = -1
        self.update()
        super().leaveEvent(event)


class SparklineCard(MiniChartCard):
    """Simplified sparkline card."""

    def __init__(self, title="", data=None, parent=None):
        super().__init__(title, data, "sparkline", parent)

    def _setup_ui(self):
        """Override for minimal UI."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Title and value in same row
        if self._title:
            header_layout = QHBoxLayout()

            title_label = QLabel(self._title)
            title_label.setFont(theme_manager.get_font('caption'))
            title_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            header_layout.addWidget(title_label)

            header_layout.addStretch()

            # Current value
            if self._data:
                current_value = self._data[-1] if self._data else 0
                value_label = QLabel(str(current_value))
                value_font = theme_manager.get_font('default')
                value_font.setWeight(QFont.Weight.Bold)
                value_label.setFont(value_font)
                value_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
                header_layout.addWidget(value_label)

            layout.addLayout(header_layout)

        # Compact chart
        self.chart_widget = ChartWidget(self._data, "sparkline")
        self.chart_widget.setFixedHeight(30)
        layout.addWidget(self.chart_widget)

        self.set_body(container)


class TrendCard(MiniChartCard):
    """Card showing trend with percentage change."""

    def __init__(self, title="", data=None, parent=None):
        super().__init__(title, data, "line", parent)

    def _setup_ui(self):
        """Override to show trend information."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Header with title and trend
        header_layout = QHBoxLayout()

        if self._title:
            title_label = QLabel(self._title)
            title_font = theme_manager.get_font('heading')
            title_font.setPointSize(12)
            title_label.setFont(title_font)
            title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
            header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Trend indicator
        if len(self._data) >= 2:
            change = self._data[-1] - self._data[-2]
            percent_change = (change / self._data[-2] * 100) if self._data[-2] != 0 else 0

            trend_text = f"{percent_change:+.1f}%"
            trend_color = theme_manager.get_color('success') if change >= 0 else theme_manager.get_color('danger')
            trend_icon = "↗" if change >= 0 else "↘"

            trend_label = QLabel(f"{trend_icon} {trend_text}")
            trend_label.setStyleSheet(f"color: {trend_color}; font-weight: bold;")
            header_layout.addWidget(trend_label)

        layout.addLayout(header_layout)

        # Chart
        self.chart_widget = ChartWidget(self._data, "line")
        self.chart_widget.setMinimumHeight(50)
        layout.addWidget(self.chart_widget)

        self.set_body(container)