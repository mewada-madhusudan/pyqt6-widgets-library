"""
Info card widget for displaying title, subtitle, and description.
"""

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIcon
from ..base.base_card import BaseCardWidget
from ..base.theme_manager import theme_manager


class InfoCardWidget(BaseCardWidget):
    """Card widget for displaying information with title, subtitle, and description."""

    def __init__(self, title="", subtitle="", description="", icon=None, parent=None):
        super().__init__(parent)
        self._title = title
        self._subtitle = subtitle
        self._description = description
        self._icon = icon
        self._setup_info_ui()

    def _setup_info_ui(self):
        """Setup the info card UI."""
        # Main content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)

        # Header with icon and title
        if self._icon or self._title:
            header_widget = QWidget()
            header_layout = QHBoxLayout(header_widget)
            header_layout.setContentsMargins(0, 0, 0, 0)
            header_layout.setSpacing(12)

            # Icon
            if self._icon:
                self.icon_label = QLabel()
                if isinstance(self._icon, str):
                    # Load from file path
                    pixmap = QPixmap(self._icon)
                    if not pixmap.isNull():
                        self.icon_label.setPixmap(pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio,
                                                                Qt.TransformationMode.SmoothTransformation))
                elif isinstance(self._icon, QIcon):
                    self.icon_label.setPixmap(self._icon.pixmap(24, 24))
                elif isinstance(self._icon, QPixmap):
                    self.icon_label.setPixmap(self._icon.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio,
                                                                Qt.TransformationMode.SmoothTransformation))

                self.icon_label.setFixedSize(24, 24)
                header_layout.addWidget(self.icon_label)

            # Title
            if self._title:
                self.title_label = QLabel(self._title)
                self.title_label.setFont(theme_manager.get_font('heading'))
                self.title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
                header_layout.addWidget(self.title_label)

            header_layout.addStretch()
            content_layout.addWidget(header_widget)

        # Subtitle
        if self._subtitle:
            self.subtitle_label = QLabel(self._subtitle)
            subtitle_font = theme_manager.get_font('default')
            subtitle_font.setWeight(QFont.Weight.Medium)
            self.subtitle_label.setFont(subtitle_font)
            self.subtitle_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            content_layout.addWidget(self.subtitle_label)

        # Description
        if self._description:
            self.description_label = QLabel(self._description)
            self.description_label.setFont(theme_manager.get_font('default'))
            self.description_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
            self.description_label.setWordWrap(True)
            content_layout.addWidget(self.description_label)

        # Set the content as body
        self.set_body(content_widget)

    def set_title(self, title: str):
        """Update the title."""
        self._title = title
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)
        else:
            self._setup_info_ui()

    def set_subtitle(self, subtitle: str):
        """Update the subtitle."""
        self._subtitle = subtitle
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setText(subtitle)
        else:
            self._setup_info_ui()

    def set_description(self, description: str):
        """Update the description."""
        self._description = description
        if hasattr(self, 'description_label'):
            self.description_label.setText(description)
        else:
            self._setup_info_ui()

    def set_icon(self, icon):
        """Update the icon."""
        self._icon = icon
        self._setup_info_ui()

    def get_title(self) -> str:
        """Get current title."""
        return self._title

    def get_subtitle(self) -> str:
        """Get current subtitle."""
        return self._subtitle

    def get_description(self) -> str:
        """Get current description."""
        return self._description


class MetricInfoCard(InfoCardWidget):
    """Specialized info card for displaying metrics."""

    def __init__(self, title="", value="", unit="", change="", parent=None):
        self._value = value
        self._unit = unit
        self._change = change

        # Create description from value and change
        description = f"{value} {unit}"
        if change:
            description += f" ({change})"

        super().__init__(title=title, description=description, parent=parent)
        self._setup_metric_styling()

    def _setup_metric_styling(self):
        """Apply metric-specific styling."""
        if hasattr(self, 'description_label'):
            # Make value larger and bold
            font = theme_manager.get_font('heading')
            font.setPointSize(16)
            self.description_label.setFont(font)

            # Color code the change
            if self._change:
                if self._change.startswith('+'):
                    color = theme_manager.get_color('success')
                elif self._change.startswith('-'):
                    color = theme_manager.get_color('danger')
                else:
                    color = theme_manager.get_color('text')

                self.description_label.setStyleSheet(f"color: {color};")

    def update_metric(self, value: str, unit: str = "", change: str = ""):
        """Update metric values."""
        self._value = value
        self._unit = unit
        self._change = change

        description = f"{value} {unit}"
        if change:
            description += f" ({change})"

        self.set_description(description)
        self._setup_metric_styling()


class StatusInfoCard(InfoCardWidget):
    """Info card with status indicator."""

    def __init__(self, title="", subtitle="", description="", status="active", parent=None):
        super().__init__(title, subtitle, description, parent=parent)
        self._status = status
        self._add_status_indicator()

    def _add_status_indicator(self):
        """Add status indicator to the card."""
        from PyQt6.QtWidgets import QFrame

        # Status indicator (colored dot)
        status_indicator = QFrame()
        status_indicator.setFixedSize(12, 12)

        status_colors = {
            'active': theme_manager.get_color('success'),
            'inactive': theme_manager.get_color('text_secondary'),
            'warning': theme_manager.get_color('warning'),
            'error': theme_manager.get_color('danger'),
            'pending': theme_manager.get_color('info')
        }

        color = status_colors.get(self._status, theme_manager.get_color('text_secondary'))

        status_indicator.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 6px;
                border: none;
            }}
        """)

        # Add to header
        if hasattr(self, 'header_widget') and self.header_widget.isVisible():
            self.header_layout.addWidget(status_indicator)
        else:
            # Create header if it doesn't exist
            header_widget = QWidget()
            header_layout = QHBoxLayout(header_widget)
            header_layout.addStretch()
            header_layout.addWidget(status_indicator)
            self.set_header(header_widget)

    def set_status(self, status: str):
        """Update status."""
        self._status = status
        self._add_status_indicator()

    def get_status(self) -> str:
        """Get current status."""
        return self._status