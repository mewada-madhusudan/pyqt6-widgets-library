"""
Card widget with hidden actions that appear on hover.
"""

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont
from ..base.base_card import BaseCardWidget
from ..base.base_button import BaseButton
from ..base.theme_manager import theme_manager
from ..base.animation_helpers import AnimationHelpers


class HoverActionCardWidget(BaseCardWidget):
    """Card with actions that appear on hover."""

    action_triggered = pyqtSignal(str)  # Emits action name

    def __init__(self, title="", subtitle="", parent=None):
        super().__init__(parent)
        self._title = title
        self._subtitle = subtitle
        self._actions = []
        self._actions_widget = None
        self._hover_animation = None
        self._setup_hover_card_ui()

    def _setup_hover_card_ui(self):
        """Setup the hover action card UI."""
        # Main content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)

        # Title
        if self._title:
            self.title_label = QLabel(self._title)
            title_font = theme_manager.get_font('heading')
            self.title_label.setFont(title_font)
            self.title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
            content_layout.addWidget(self.title_label)

        # Subtitle
        if self._subtitle:
            self.subtitle_label = QLabel(self._subtitle)
            self.subtitle_label.setFont(theme_manager.get_font('default'))
            self.subtitle_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            self.subtitle_label.setWordWrap(True)
            content_layout.addWidget(self.subtitle_label)

        content_layout.addStretch()
        self.set_body(content_widget)

        # Actions widget (initially hidden)
        self._actions_widget = QWidget()
        self._actions_layout = QHBoxLayout(self._actions_widget)
        self._actions_layout.setContentsMargins(0, 0, 0, 0)
        self._actions_layout.setSpacing(8)
        self._actions_widget.hide()

        # Add actions to footer
        self.set_footer(self._actions_widget)

    def add_action(self, text: str, action_name: str = None, variant: str = "secondary", icon=None):
        """Add hover action button."""
        if action_name is None:
            action_name = text.lower().replace(" ", "_")

        button = BaseButton(text, variant, "small")
        if icon:
            button.set_icon(icon)

        button.clicked.connect(lambda: self.action_triggered.emit(action_name))

        self._actions.append((button, action_name))
        self._actions_layout.addWidget(button)

    def remove_action(self, action_name: str):
        """Remove action by name."""
        for i, (button, name) in enumerate(self._actions):
            if name == action_name:
                button.setParent(None)
                del self._actions[i]
                break

    def clear_actions(self):
        """Remove all actions."""
        for button, _ in self._actions:
            button.setParent(None)
        self._actions.clear()

    def set_title(self, title: str):
        """Update title."""
        self._title = title
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)

    def set_subtitle(self, subtitle: str):
        """Update subtitle."""
        self._subtitle = subtitle
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setText(subtitle)

    def enterEvent(self, event):
        """Show actions on mouse enter."""
        super().enterEvent(event)
        self._show_actions()

    def leaveEvent(self, event):
        """Hide actions on mouse leave."""
        super().leaveEvent(event)
        self._hide_actions()

    def _show_actions(self):
        """Animate actions into view."""
        if not self._actions or self._actions_widget.isVisible():
            return

        self._actions_widget.show()

        # Fade in animation
        AnimationHelpers.fade_in(self._actions_widget, 200)

        # Slide up animation
        self._hover_animation = QPropertyAnimation(self._actions_widget, b"geometry")
        self._hover_animation.setDuration(200)

        start_rect = self._actions_widget.geometry()
        start_rect.moveTop(start_rect.top() + 10)  # Start slightly below
        end_rect = self._actions_widget.geometry()

        self._hover_animation.setStartValue(start_rect)
        self._hover_animation.setEndValue(end_rect)
        self._hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._hover_animation.start()

    def _hide_actions(self):
        """Animate actions out of view."""
        if not self._actions or not self._actions_widget.isVisible():
            return

        # Fade out animation
        def on_fade_complete():
            self._actions_widget.hide()

        AnimationHelpers.fade_out(self._actions_widget, 150, on_fade_complete)

    def get_actions(self) -> list:
        """Get list of action names."""
        return [name for _, name in self._actions]


class QuickActionCard(HoverActionCardWidget):
    """Card optimized for quick actions."""

    def __init__(self, title="", icon=None, parent=None):
        super().__init__(title, "", parent)
        self._icon = icon
        self._setup_quick_action_ui()

    def _setup_quick_action_ui(self):
        """Setup quick action specific UI."""
        # Add icon to the card
        if self._icon:
            # Create new content with icon
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setSpacing(12)
            content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Icon
            icon_label = QLabel()
            icon_label.setFixedSize(48, 48)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {theme_manager.get_color('primary')};
                    border-radius: 24px;
                    color: white;
                    font-size: 24px;
                }}
            """)

            if isinstance(self._icon, str):
                # Treat as text icon (emoji or symbol)
                icon_label.setText(self._icon)

            content_layout.addWidget(icon_label)

            # Title
            if self._title:
                title_label = QLabel(self._title)
                title_font = theme_manager.get_font('default')
                title_font.setWeight(QFont.Weight.Bold)
                title_label.setFont(title_font)
                title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
                title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                content_layout.addWidget(title_label)

            self.set_body(content_widget)

        # Make card smaller for quick actions
        self.setFixedSize(120, 100)


class MediaCard(HoverActionCardWidget):
    """Card for media items with hover actions."""

    def __init__(self, title="", description="", thumbnail=None, parent=None):
        self._thumbnail = thumbnail
        super().__init__(title, description, parent)
        self._setup_media_ui()

    def _setup_media_ui(self):
        """Setup media-specific UI."""
        if self._thumbnail:
            # Add thumbnail to header
            header_widget = QWidget()
            header_layout = QVBoxLayout(header_widget)
            header_layout.setContentsMargins(0, 0, 0, 0)

            # Thumbnail
            thumbnail_label = QLabel()
            thumbnail_label.setFixedSize(200, 120)
            thumbnail_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {theme_manager.get_color('light')};
                    border-radius: {theme_manager.get_border_radius('sm')}px;
                }}
            """)

            if isinstance(self._thumbnail, str):
                from PyQt6.QtGui import QPixmap
                pixmap = QPixmap(self._thumbnail)
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(
                        200, 120,
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    thumbnail_label.setPixmap(scaled_pixmap)

            header_layout.addWidget(thumbnail_label)
            self.set_header(header_widget)

        # Add common media actions
        self.add_action("Play", "play", "primary")
        self.add_action("Share", "share", "secondary")
        self.add_action("More", "more", "ghost")

    def set_thumbnail(self, thumbnail_path: str):
        """Update thumbnail."""
        self._thumbnail = thumbnail_path
        self._setup_media_ui()


class ProjectCard(HoverActionCardWidget):
    """Card for project items with status and actions."""

    def __init__(self, title="", description="", status="active", progress=0, parent=None):
        self._status = status
        self._progress = progress
        super().__init__(title, description, parent)
        self._setup_project_ui()

    def _setup_project_ui(self):
        """Setup project-specific UI."""
        # Add status indicator
        status_colors = {
            'active': theme_manager.get_color('success'),
            'paused': theme_manager.get_color('warning'),
            'completed': theme_manager.get_color('info'),
            'cancelled': theme_manager.get_color('danger')
        }

        # Status chip in header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)

        status_chip = QLabel(self._status.title())
        status_chip.setStyleSheet(f"""
            QLabel {{
                background-color: {status_colors.get(self._status, theme_manager.get_color('light'))};
                color: white;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 10px;
                font-weight: bold;
            }}
        """)

        header_layout.addStretch()
        header_layout.addWidget(status_chip)
        self.set_header(header_widget)

        # Add progress bar if progress > 0
        if self._progress > 0:
            from PyQt6.QtWidgets import QProgressBar

            progress_bar = QProgressBar()
            progress_bar.setValue(self._progress)
            progress_bar.setTextVisible(False)
            progress_bar.setFixedHeight(4)
            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: none;
                    border-radius: 2px;
                    background-color: {theme_manager.get_color('light')};
                }}
                QProgressBar::chunk {{
                    border-radius: 2px;
                    background-color: {theme_manager.get_color('primary')};
                }}
            """)

            # Add to body
            if hasattr(self, 'body_layout'):
                self.body_layout.addWidget(progress_bar)

        # Add project actions
        self.add_action("Open", "open", "primary")
        self.add_action("Edit", "edit", "secondary")
        self.add_action("Settings", "settings", "ghost")

    def set_status(self, status: str):
        """Update project status."""
        self._status = status
        self._setup_project_ui()

    def set_progress(self, progress: int):
        """Update project progress."""
        self._progress = progress
        self._setup_project_ui()

    def get_status(self) -> str:
        """Get current status."""
        return self._status

    def get_progress(self) -> int:
        """Get current progress."""
        return self._progress