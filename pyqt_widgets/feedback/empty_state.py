"""
Empty state widget for displaying friendly placeholders.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from ..base.base_button import BaseButton
from ..base.theme_manager import theme_manager


class EmptyStateWidget(QWidget):
    """Friendly placeholder for empty data states."""

    action_clicked = pyqtSignal(str)  # Emits action name

    def __init__(self, title="No items found", message="", icon=None, parent=None):
        super().__init__(parent)
        self._title = title
        self._message = message
        self._icon = icon
        self._actions = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup the empty state UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(16)

        # Icon
        if self._icon:
            self.icon_label = QLabel()
            self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if isinstance(self._icon, str):
                # Text icon (emoji or symbol)
                self.icon_label.setText(self._icon)
                icon_font = theme_manager.get_font('default')
                icon_font.setPointSize(48)
                self.icon_label.setFont(icon_font)
            else:
                # QIcon or QPixmap
                self.icon_label.setPixmap(self._icon.pixmap(64, 64))

            self.icon_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            main_layout.addWidget(self.icon_label)

        # Title
        self.title_label = QLabel(self._title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_font = theme_manager.get_font('heading')
        title_font.setPointSize(18)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")

        main_layout.addWidget(self.title_label)

        # Message
        if self._message:
            self.message_label = QLabel(self._message)
            self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.message_label.setFont(theme_manager.get_font('default'))
            self.message_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            self.message_label.setWordWrap(True)
            self.message_label.setMaximumWidth(400)
            main_layout.addWidget(self.message_label)

        # Actions container
        self.actions_widget = QWidget()
        self.actions_layout = QHBoxLayout(self.actions_widget)
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        self.actions_layout.setSpacing(12)
        self.actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.actions_widget.hide()

        main_layout.addWidget(self.actions_widget)

        # Apply styling
        self.setStyleSheet(f"""
            EmptyStateWidget {{
                background-color: {theme_manager.get_color('background')};
                padding: 32px;
            }}
        """)

    def add_action(self, text: str, action_name: str = None, variant: str = "primary"):
        """Add action button to empty state."""
        if action_name is None:
            action_name = text.lower().replace(" ", "_")

        action_btn = BaseButton(text, variant, "medium")
        action_btn.clicked.connect(lambda: self.action_clicked.emit(action_name))

        self.actions_layout.addWidget(action_btn)
        self._actions.append((action_btn, action_name))

        # Show actions container
        self.actions_widget.show()

    def remove_action(self, action_name: str):
        """Remove action by name."""
        for i, (button, name) in enumerate(self._actions):
            if name == action_name:
                button.setParent(None)
                del self._actions[i]
                break

        # Hide container if no actions left
        if not self._actions:
            self.actions_widget.hide()

    def clear_actions(self):
        """Remove all actions."""
        for button, _ in self._actions:
            button.setParent(None)
        self._actions.clear()
        self.actions_widget.hide()

    def set_title(self, title: str):
        """Update title."""
        self._title = title
        self.title_label.setText(title)

    def set_message(self, message: str):
        """Update message."""
        self._message = message
        if hasattr(self, 'message_label'):
            self.message_label.setText(message)
        elif message:
            # Create message label if it doesn't exist
            self._setup_ui()

    def set_icon(self, icon):
        """Update icon."""
        self._icon = icon
        if hasattr(self, 'icon_label'):
            if isinstance(icon, str):
                self.icon_label.setText(icon)
                icon_font = theme_manager.get_font('default')
                icon_font.setPointSize(48)
                self.icon_label.setFont(icon_font)
            else:
                self.icon_label.setPixmap(icon.pixmap(64, 64))
        elif icon:
            # Recreate UI to add icon
            self._setup_ui()

    def get_title(self) -> str:
        """Get current title."""
        return self._title

    def get_message(self) -> str:
        """Get current message."""
        return self._message


class NoDataEmptyState(EmptyStateWidget):
    """Empty state for no data scenarios."""

    def __init__(self, data_type: str = "items", parent=None):
        title = f"No {data_type} found"
        message = f"There are no {data_type} to display right now."
        icon = "📭"  # Empty mailbox emoji

        super().__init__(title, message, icon, parent)

        # Add common action
        self.add_action(f"Add {data_type.rstrip('s')}", "add_item", "primary")


class SearchEmptyState(EmptyStateWidget):
    """Empty state for search results."""

    def __init__(self, query: str = "", parent=None):
        if query:
            title = f"No results for '{query}'"
            message = "Try adjusting your search terms or filters."
        else:
            title = "No search results"
            message = "Enter a search term to find items."

        icon = "🔍"  # Magnifying glass emoji

        super().__init__(title, message, icon, parent)

        # Add search actions
        self.add_action("Clear search", "clear_search", "secondary")
        self.add_action("Browse all", "browse_all", "primary")


class ErrorEmptyState(EmptyStateWidget):
    """Empty state for error scenarios."""

    def __init__(self, error_message: str = "", parent=None):
        title = "Something went wrong"
        message = error_message or "We encountered an error while loading the data."
        icon = "⚠️"  # Warning emoji

        super().__init__(title, message, icon, parent)

        # Add error actions
        self.add_action("Retry", "retry", "primary")
        self.add_action("Report issue", "report", "secondary")


class LoadingEmptyState(EmptyStateWidget):
    """Empty state for loading scenarios."""

    def __init__(self, parent=None):
        title = "Loading..."
        message = "Please wait while we fetch your data."
        icon = "⟳"  # Refresh emoji

        super().__init__(title, message, icon, parent)

        # Add loading animation
        self._setup_loading_animation()

    def _setup_loading_animation(self):
        """Setup loading animation for icon."""
        if hasattr(self, 'icon_label'):
            from PyQt6.QtCore import QPropertyAnimation, QTimer

            # Simple text rotation animation
            self._animation_timer = QTimer()
            self._animation_timer.timeout.connect(self._rotate_icon)
            self._animation_timer.start(500)  # Rotate every 500ms
            self._rotation_state = 0

    def _rotate_icon(self):
        """Rotate loading icon."""
        rotation_chars = ["⟳", "⟲", "⟳", "⟲"]
        self._rotation_state = (self._rotation_state + 1) % len(rotation_chars)
        if hasattr(self, 'icon_label'):
            self.icon_label.setText(rotation_chars[self._rotation_state])


class PermissionEmptyState(EmptyStateWidget):
    """Empty state for permission denied scenarios."""

    def __init__(self, resource: str = "this content", parent=None):
        title = "Access denied"
        message = f"You don't have permission to view {resource}."
        icon = "🔒"  # Lock emoji

        super().__init__(title, message, icon, parent)

        # Add permission actions
        self.add_action("Request access", "request_access", "primary")
        self.add_action("Go back", "go_back", "secondary")


class MaintenanceEmptyState(EmptyStateWidget):
    """Empty state for maintenance scenarios."""

    def __init__(self, parent=None):
        title = "Under maintenance"
        message = "This feature is temporarily unavailable while we make improvements."
        icon = "🔧"  # Wrench emoji

        super().__init__(title, message, icon, parent)

        # Add maintenance actions
        self.add_action("Check status", "check_status", "secondary")


class FirstTimeEmptyState(EmptyStateWidget):
    """Empty state for first-time users."""

    def __init__(self, feature_name: str = "feature", parent=None):
        title = f"Welcome to {feature_name}!"
        message = f"Get started by creating your first item or exploring the {feature_name}."
        icon = "🎉"  # Party emoji

        super().__init__(title, message, icon, parent)

        # Add onboarding actions
        self.add_action("Get started", "get_started", "primary")
        self.add_action("Take tour", "take_tour", "secondary")


class CustomEmptyState(EmptyStateWidget):
    """Customizable empty state with flexible content."""

    def __init__(self, parent=None):
        super().__init__("", "", None, parent)

    def set_content(self, title: str, message: str = "", icon=None,
                    actions: list = None):
        """Set all content at once."""
        self.set_title(title)
        self.set_message(message)
        if icon:
            self.set_icon(icon)

        # Clear existing actions
        self.clear_actions()

        # Add new actions
        if actions:
            for action in actions:
                if isinstance(action, dict):
                    self.add_action(
                        action.get('text', ''),
                        action.get('name'),
                        action.get('variant', 'primary')
                    )
                elif isinstance(action, (list, tuple)) and len(action) >= 2:
                    self.add_action(action[0], action[1],
                                    action[2] if len(action) > 2 else 'primary')


class AnimatedEmptyState(EmptyStateWidget):
    """Empty state with subtle animations."""

    def __init__(self, title="", message="", icon=None, parent=None):
        super().__init__(title, message, icon, parent)
        self._setup_animations()

    def _setup_animations(self):
        """Setup entrance animations."""
        from ..base.animation_helpers import AnimationHelpers

        # Fade in animation on show
        self.showEvent = self._animated_show_event

    def _animated_show_event(self, event):
        """Override show event to add animation."""
        QWidget.showEvent(self, event)

        # Animate fade in
        from ..base.animation_helpers import AnimationHelpers
        AnimationHelpers.fade_in(self, 500)

        # Animate icon bounce
        if hasattr(self, 'icon_label'):
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(200, self._bounce_icon)

    def _bounce_icon(self):
        """Add bounce effect to icon."""
        if hasattr(self, 'icon_label'):
            from ..base.animation_helpers import AnimationHelpers
            AnimationHelpers.bounce_effect(self.icon_label)