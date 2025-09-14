"""
Timeline widget for displaying chronological events.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
                             QLabel, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QDateTime
from PyQt6.QtGui import QFont, QPainter, QPen, QColor
from ..base.theme_manager import theme_manager
from ..base.base_card import BaseCardWidget


class TimelineWidget(QWidget):
    """Timeline widget for displaying chronological events."""

    event_clicked = pyqtSignal(dict)  # Emits event data

    def __init__(self, orientation=Qt.Orientation.Vertical, parent=None):
        super().__init__(parent)
        self._orientation = orientation
        self._events = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup the timeline UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scrollable area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        # Timeline container
        self.timeline_container = QWidget()
        if self._orientation == Qt.Orientation.Vertical:
            self.timeline_layout = QVBoxLayout(self.timeline_container)
        else:
            self.timeline_layout = QHBoxLayout(self.timeline_container)

        self.timeline_layout.setContentsMargins(20, 20, 20, 20)
        self.timeline_layout.setSpacing(0)
        self.timeline_layout.addStretch()

        scroll_area.setWidget(self.timeline_container)
        main_layout.addWidget(scroll_area)

        # Apply styling
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_manager.get_color('background')};
            }}
        """)

    def add_event(self, title: str, description: str = "", timestamp=None,
                  event_type: str = "default", icon: str = None, data: dict = None):
        """Add event to timeline."""
        if timestamp is None:
            timestamp = QDateTime.currentDateTime()

        event_data = {
            'title': title,
            'description': description,
            'timestamp': timestamp,
            'type': event_type,
            'icon': icon,
            'data': data or {}
        }

        self._events.append(event_data)
        self._sort_events()
        self._rebuild_timeline()

    def _sort_events(self):
        """Sort events by timestamp."""
        self._events.sort(key=lambda x: x['timestamp'])

    def _rebuild_timeline(self):
        """Rebuild the entire timeline."""
        # Clear existing items
        for i in reversed(range(self.timeline_layout.count())):
            item = self.timeline_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        # Add events
        for i, event in enumerate(self._events):
            event_widget = self._create_event_widget(event, i)
            self.timeline_layout.insertWidget(self.timeline_layout.count() - 1, event_widget)

    def _create_event_widget(self, event: dict, index: int) -> QWidget:
        """Create widget for timeline event."""
        container = QWidget()

        if self._orientation == Qt.Orientation.Vertical:
            layout = QHBoxLayout(container)
        else:
            layout = QVBoxLayout(container)

        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(16)

        # Timeline line and dot
        timeline_visual = self._create_timeline_visual(event, index)

        # Event content
        event_content = self._create_event_content(event)

        if self._orientation == Qt.Orientation.Vertical:
            layout.addWidget(timeline_visual)
            layout.addWidget(event_content)
        else:
            layout.addWidget(event_content)
            layout.addWidget(timeline_visual)

        return container

    def _create_timeline_visual(self, event: dict, index: int) -> QWidget:
        """Create timeline visual (dot and line)."""
        visual_widget = QWidget()

        if self._orientation == Qt.Orientation.Vertical:
            visual_widget.setFixedWidth(40)
            visual_widget.setMinimumHeight(60)
        else:
            visual_widget.setFixedHeight(40)
            visual_widget.setMinimumWidth(60)

        # Custom paint for timeline visual
        visual_widget.paintEvent = lambda event: self._paint_timeline_visual(
            event, visual_widget, index
        )

        return visual_widget

    def _paint_timeline_visual(self, paint_event, widget, index):
        """Paint timeline dot and line."""
        painter = QPainter(widget)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Get colors based on event type
        event = self._events[index]
        dot_color = self._get_event_color(event['type'])
        line_color = theme_manager.get_color('border')

        if self._orientation == Qt.Orientation.Vertical:
            # Vertical timeline
            center_x = widget.width() // 2
            dot_y = 20

            # Draw line (except for last item)
            if index < len(self._events) - 1:
                painter.setPen(QPen(QColor(line_color), 2))
                painter.drawLine(center_x, dot_y + 8, center_x, widget.height())

            # Draw line from top (except for first item)
            if index > 0:
                painter.setPen(QPen(QColor(line_color), 2))
                painter.drawLine(center_x, 0, center_x, dot_y - 8)

            # Draw dot
            painter.setBrush(QColor(dot_color))
            painter.setPen(QPen(QColor(dot_color), 2))
            painter.drawEllipse(center_x - 8, dot_y - 8, 16, 16)

        else:
            # Horizontal timeline
            center_y = widget.height() // 2
            dot_x = 20

            # Draw line (except for last item)
            if index < len(self._events) - 1:
                painter.setPen(QPen(QColor(line_color), 2))
                painter.drawLine(dot_x + 8, center_y, widget.width(), center_y)

            # Draw line from left (except for first item)
            if index > 0:
                painter.setPen(QPen(QColor(line_color), 2))
                painter.drawLine(0, center_y, dot_x - 8, center_y)

            # Draw dot
            painter.setBrush(QColor(dot_color))
            painter.setPen(QPen(QColor(dot_color), 2))
            painter.drawEllipse(dot_x - 8, center_y - 8, 16, 16)

        painter.end()

    def _get_event_color(self, event_type: str) -> str:
        """Get color for event type."""
        colors = {
            'success': theme_manager.get_color('success'),
            'warning': theme_manager.get_color('warning'),
            'error': theme_manager.get_color('danger'),
            'info': theme_manager.get_color('info'),
            'default': theme_manager.get_color('primary')
        }
        return colors.get(event_type, colors['default'])

    def _create_event_content(self, event: dict) -> QWidget:
        """Create event content widget."""
        content_card = BaseCardWidget()
        content_card.set_hoverable(True)

        # Content layout
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)

        # Header with timestamp
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Title
        title_label = QLabel(event['title'])
        title_font = theme_manager.get_font('heading')
        title_font.setPointSize(12)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Timestamp
        timestamp_label = QLabel(event['timestamp'].toString("MMM dd, yyyy hh:mm"))
        timestamp_label.setFont(theme_manager.get_font('caption'))
        timestamp_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        header_layout.addWidget(timestamp_label)

        content_layout.addLayout(header_layout)

        # Description
        if event['description']:
            desc_label = QLabel(event['description'])
            desc_label.setFont(theme_manager.get_font('default'))
            desc_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
            desc_label.setWordWrap(True)
            content_layout.addWidget(desc_label)

        # Icon
        if event['icon']:
            icon_label = QLabel(event['icon'])
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_font = theme_manager.get_font('default')
            icon_font.setPointSize(16)
            icon_label.setFont(icon_font)
            content_layout.addWidget(icon_label)

        content_card.set_body(content_widget)

        # Make clickable
        content_card.clicked.connect(lambda: self.event_clicked.emit(event))

        return content_card

    def clear_events(self):
        """Clear all events from timeline."""
        self._events.clear()
        self._rebuild_timeline()

    def remove_event(self, index: int):
        """Remove event at index."""
        if 0 <= index < len(self._events):
            del self._events[index]
            self._rebuild_timeline()

    def get_events(self) -> list:
        """Get all events."""
        return self._events.copy()

    def set_orientation(self, orientation: Qt.Orientation):
        """Change timeline orientation."""
        self._orientation = orientation
        self._setup_ui()
        self._rebuild_timeline()


class CompactTimeline(TimelineWidget):
    """Compact timeline for smaller spaces."""

    def __init__(self, parent=None):
        super().__init__(Qt.Orientation.Vertical, parent)

    def _create_event_content(self, event: dict) -> QWidget:
        """Create compact event content."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        # Icon or type indicator
        if event['icon']:
            icon_label = QLabel(event['icon'])
            icon_label.setFixedSize(16, 16)
            layout.addWidget(icon_label)
        else:
            # Color indicator
            indicator = QFrame()
            indicator.setFixedSize(4, 16)
            indicator.setStyleSheet(f"""
                QFrame {{
                    background-color: {self._get_event_color(event['type'])};
                    border-radius: 2px;
                }}
            """)
            layout.addWidget(indicator)

        # Title
        title_label = QLabel(event['title'])
        title_label.setFont(theme_manager.get_font('default'))
        title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        layout.addWidget(title_label)

        layout.addStretch()

        # Time
        time_label = QLabel(event['timestamp'].toString("hh:mm"))
        time_label.setFont(theme_manager.get_font('caption'))
        time_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        layout.addWidget(time_label)

        # Apply styling
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_manager.get_color('surface')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                border: 1px solid {theme_manager.get_color('border')};
            }}
            QWidget:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)

        # Make clickable
        container.mousePressEvent = lambda event: self.event_clicked.emit(event)

        return container


class InteractiveTimeline(TimelineWidget):
    """Timeline with interactive features."""

    event_edited = pyqtSignal(int, dict)  # index, new_data
    event_deleted = pyqtSignal(int)  # index

    def __init__(self, parent=None):
        super().__init__(Qt.Orientation.Vertical, parent)

    def _create_event_content(self, event: dict) -> QWidget:
        """Create interactive event content."""
        content_card = super()._create_event_content(event)

        # Add action buttons
        from ..base.base_button import BaseButton

        edit_btn = BaseButton("Edit", "ghost", "small")
        edit_btn.clicked.connect(lambda: self._edit_event(event))
        content_card.add_footer_action(edit_btn)

        delete_btn = BaseButton("Delete", "destructive", "small")
        delete_btn.clicked.connect(lambda: self._delete_event(event))
        content_card.add_footer_action(delete_btn)

        return content_card

    def _edit_event(self, event: dict):
        """Edit event (placeholder - would open edit dialog)."""
        index = self._events.index(event)
        self.event_edited.emit(index, event)

    def _delete_event(self, event: dict):
        """Delete event."""
        index = self._events.index(event)
        self.remove_event(index)
        self.event_deleted.emit(index)