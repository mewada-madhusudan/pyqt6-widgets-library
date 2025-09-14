"""
User list item widget with avatar, name, and action buttons.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ..base.theme_manager import theme_manager
from ..base.base_button import BaseButton
from .user_avatar import UserAvatarWidget


class UserListItemWidget(QWidget):
    """List item displaying user information with optional actions."""

    clicked = pyqtSignal()
    action_clicked = pyqtSignal(str)  # Emits action name

    def __init__(self, name="", role="", email="", avatar_path="",
                 status=None, parent=None):
        super().__init__(parent)
        self._name = name
        self._role = role
        self._email = email
        self._avatar_path = avatar_path
        self._status = status
        self._actions = []
        self._clickable = False
        self._setup_ui()

    def _setup_ui(self):
        """Setup the user list item UI."""
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(12, 8, 12, 8)
        main_layout.setSpacing(12)

        # Avatar
        self.avatar = UserAvatarWidget(self._name, self._avatar_path, 40, self._status)
        main_layout.addWidget(self.avatar)

        # User info
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2)

        # Name
        self.name_label = QLabel(self._name)
        name_font = theme_manager.get_font('default')
        name_font.setWeight(QFont.Weight.Bold)
        self.name_label.setFont(name_font)
        self.name_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        info_layout.addWidget(self.name_label)

        # Role
        if self._role:
            self.role_label = QLabel(self._role)
            self.role_label.setFont(theme_manager.get_font('default'))
            self.role_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            info_layout.addWidget(self.role_label)

        # Email
        if self._email:
            self.email_label = QLabel(self._email)
            self.email_label.setFont(theme_manager.get_font('caption'))
            self.email_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            info_layout.addWidget(self.email_label)

        main_layout.addLayout(info_layout)
        main_layout.addStretch()

        # Actions container
        self.actions_widget = QWidget()
        self.actions_layout = QHBoxLayout(self.actions_widget)
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        self.actions_layout.setSpacing(8)
        self.actions_widget.hide()

        main_layout.addWidget(self.actions_widget)

        # Apply styling
        self.setStyleSheet(f"""
            UserListItemWidget {{
                background-color: {theme_manager.get_color('surface')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}
            UserListItemWidget:hover {{
                background-color: {theme_manager.get_color('hover')};
                border-color: {theme_manager.get_color('primary')};
            }}
        """)

    def add_action(self, text: str, action_name: str = None, variant: str = "secondary"):
        """Add action button."""
        if action_name is None:
            action_name = text.lower().replace(" ", "_")

        action_btn = BaseButton(text, variant, "small")
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

    def set_clickable(self, clickable: bool):
        """Enable/disable click interaction."""
        self._clickable = clickable
        if clickable:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, event):
        """Handle mouse press for clicks."""
        if self._clickable and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def set_name(self, name: str):
        """Update user name."""
        self._name = name
        self.name_label.setText(name)
        self.avatar.set_name(name)

    def set_role(self, role: str):
        """Update user role."""
        self._role = role
        if hasattr(self, 'role_label'):
            self.role_label.setText(role)

    def set_email(self, email: str):
        """Update user email."""
        self._email = email
        if hasattr(self, 'email_label'):
            self.email_label.setText(email)

    def set_status(self, status: str):
        """Update user status."""
        self._status = status
        self.avatar.set_status(status)

    def set_avatar(self, avatar_path: str):
        """Update avatar image."""
        self._avatar_path = avatar_path
        self.avatar.set_image(avatar_path)

    def get_name(self) -> str:
        """Get user name."""
        return self._name

    def get_role(self) -> str:
        """Get user role."""
        return self._role

    def get_email(self) -> str:
        """Get user email."""
        return self._email


class CompactUserListItem(UserListItemWidget):
    """Compact version of user list item."""

    def __init__(self, name="", role="", avatar_path="", parent=None):
        super().__init__(name, role, "", avatar_path, None, parent)
        self._setup_compact_ui()

    def _setup_compact_ui(self):
        """Override for compact layout."""
        # Clear existing layout
        self.layout().setParent(None)

        # Compact layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(8, 4, 8, 4)
        main_layout.setSpacing(8)

        # Smaller avatar
        self.avatar.set_size(24)
        main_layout.addWidget(self.avatar)

        # Name only
        self.name_label.setParent(None)
        main_layout.addWidget(self.name_label)

        main_layout.addStretch()


class TeamMemberItem(UserListItemWidget):
    """Team member list item with additional team info."""

    def __init__(self, name="", role="", team="", avatar_path="",
                 status=None, parent=None):
        self._team = team
        super().__init__(name, role, "", avatar_path, status, parent)
        self._add_team_info()

    def _add_team_info(self):
        """Add team information."""
        if self._team:
            team_label = QLabel(f"Team: {self._team}")
            team_label.setFont(theme_manager.get_font('caption'))
            team_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")

            # Insert after role
            info_layout = self.layout().itemAt(1).layout()
            info_layout.addWidget(team_label)

    def set_team(self, team: str):
        """Update team name."""
        self._team = team
        # Would need to update team label

    def get_team(self) -> str:
        """Get team name."""
        return self._team


class ContactListItem(UserListItemWidget):
    """Contact list item with phone and additional info."""

    def __init__(self, name="", role="", email="", phone="",
                 avatar_path="", parent=None):
        self._phone = phone
        super().__init__(name, role, email, avatar_path, None, parent)
        self._add_contact_info()

    def _add_contact_info(self):
        """Add contact information."""
        if self._phone:
            phone_label = QLabel(self._phone)
            phone_label.setFont(theme_manager.get_font('caption'))
            phone_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")

            # Insert after email
            info_layout = self.layout().itemAt(1).layout()
            info_layout.addWidget(phone_label)

        # Add default contact actions
        self.add_action("Call", "call", "primary")
        self.add_action("Message", "message", "secondary")

    def set_phone(self, phone: str):
        """Update phone number."""
        self._phone = phone

    def get_phone(self) -> str:
        """Get phone number."""
        return self._phone


class SelectableUserListItem(UserListItemWidget):
    """User list item with selection checkbox."""

    selection_changed = pyqtSignal(bool)  # Emits selection state

    def __init__(self, name="", role="", email="", avatar_path="", parent=None):
        super().__init__(name, role, email, avatar_path, None, parent)
        self._selected = False
        self._add_selection_checkbox()

    def _add_selection_checkbox(self):
        """Add selection checkbox."""
        from PyQt6.QtWidgets import QCheckBox

        self.checkbox = QCheckBox()
        self.checkbox.toggled.connect(self._on_selection_changed)

        # Insert at beginning of layout
        self.layout().insertWidget(0, self.checkbox)

    def _on_selection_changed(self, checked: bool):
        """Handle selection change."""
        self._selected = checked
        self.selection_changed.emit(checked)

        # Update styling based on selection
        if checked:
            self.setStyleSheet(f"""
                SelectableUserListItem {{
                    background-color: {theme_manager.get_color('primary')};
                    border: 1px solid {theme_manager.get_color('primary')};
                    border-radius: {theme_manager.get_border_radius('md')}px;
                    color: white;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                SelectableUserListItem {{
                    background-color: {theme_manager.get_color('surface')};
                    border: 1px solid {theme_manager.get_color('border')};
                    border-radius: {theme_manager.get_border_radius('md')}px;
                }}
                SelectableUserListItem:hover {{
                    background-color: {theme_manager.get_color('hover')};
                    border-color: {theme_manager.get_color('primary')};
                }}
            """)

    def set_selected(self, selected: bool):
        """Set selection state."""
        self.checkbox.setChecked(selected)

    def is_selected(self) -> bool:
        """Check if item is selected."""
        return self._selected


class UserListWidget(QWidget):
    """Container for multiple user list items."""

    user_selected = pyqtSignal(str)  # Emits user name
    user_action = pyqtSignal(str, str)  # Emits user name and action

    def __init__(self, parent=None):
        super().__init__(parent)
        self._users = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup user list UI."""
        from PyQt6.QtWidgets import QScrollArea, QVBoxLayout

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scrollable area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Users container
        self.users_container = QWidget()
        self.users_layout = QVBoxLayout(self.users_container)
        self.users_layout.setContentsMargins(0, 0, 0, 0)
        self.users_layout.setSpacing(4)
        self.users_layout.addStretch()

        scroll_area.setWidget(self.users_container)
        main_layout.addWidget(scroll_area)

    def add_user(self, user_item: UserListItemWidget):
        """Add user item to list."""
        self._users.append(user_item)
        self.users_layout.insertWidget(self.users_layout.count() - 1, user_item)

        # Connect signals
        user_item.clicked.connect(lambda: self.user_selected.emit(user_item.get_name()))
        user_item.action_clicked.connect(lambda action: self.user_action.emit(user_item.get_name(), action))

    def remove_user(self, name: str):
        """Remove user by name."""
        for i, user_item in enumerate(self._users):
            if user_item.get_name() == name:
                user_item.setParent(None)
                del self._users[i]
                break

    def clear_users(self):
        """Remove all users."""
        for user_item in self._users:
            user_item.setParent(None)
        self._users.clear()

    def get_users(self) -> list:
        """Get list of user names."""
        return [user.get_name() for user in self._users]

    def find_user(self, name: str) -> UserListItemWidget:
        """Find user item by name."""
        for user_item in self._users:
            if user_item.get_name() == name:
                return user_item
        return None