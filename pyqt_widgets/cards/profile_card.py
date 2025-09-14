"""
Profile card widget for displaying user information.
"""

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPainterPath
from ..base.base_card import BaseCardWidget
from ..base.base_button import BaseButton
from ..base.theme_manager import theme_manager


class ProfileCardWidget(BaseCardWidget):
    """Card widget for displaying user profile information."""

    action_clicked = pyqtSignal(str)  # Emits action name

    def __init__(self, name="", role="", avatar=None, email="", parent=None):
        super().__init__(parent)
        self._name = name
        self._role = role
        self._avatar = avatar
        self._email = email
        self._action_buttons = []
        self._setup_profile_ui()

    def _setup_profile_ui(self):
        """Setup the profile card UI."""
        # Main content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        # Avatar and basic info section
        profile_section = QWidget()
        profile_layout = QHBoxLayout(profile_section)
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.setSpacing(16)

        # Avatar
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(64, 64)
        self.avatar_label.setStyleSheet(f"""
            QLabel {{
                border: 2px solid {theme_manager.get_color('border')};
                border-radius: 32px;
                background-color: {theme_manager.get_color('light')};
            }}
        """)

        if self._avatar:
            self._set_avatar_image(self._avatar)
        else:
            # Show initials if no avatar
            self._set_avatar_initials()

        profile_layout.addWidget(self.avatar_label)

        # Name and role info
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(4)

        # Name
        if self._name:
            self.name_label = QLabel(self._name)
            name_font = theme_manager.get_font('heading')
            name_font.setPointSize(14)
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
            email_font = theme_manager.get_font('caption')
            self.email_label.setFont(email_font)
            self.email_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            info_layout.addWidget(self.email_label)

        info_layout.addStretch()
        profile_layout.addWidget(info_widget)
        profile_layout.addStretch()

        content_layout.addWidget(profile_section)

        # Set the content as body
        self.set_body(content_widget)

    def _set_avatar_image(self, avatar_path: str):
        """Set avatar from image path."""
        pixmap = QPixmap(avatar_path)
        if not pixmap.isNull():
            # Create circular avatar
            circular_pixmap = self._create_circular_pixmap(pixmap, 64)
            self.avatar_label.setPixmap(circular_pixmap)
        else:
            self._set_avatar_initials()

    def _set_avatar_initials(self):
        """Set avatar to show initials."""
        initials = ""
        if self._name:
            name_parts = self._name.split()
            for part in name_parts[:2]:  # First two names
                if part:
                    initials += part[0].upper()

        if not initials:
            initials = "?"

        self.avatar_label.setText(initials)
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Style for initials
        font = theme_manager.get_font('heading')
        font.setPointSize(18)
        self.avatar_label.setFont(font)
        self.avatar_label.setStyleSheet(f"""
            QLabel {{
                border: 2px solid {theme_manager.get_color('primary')};
                border-radius: 32px;
                background-color: {theme_manager.get_color('primary')};
                color: white;
            }}
        """)

    def _create_circular_pixmap(self, pixmap: QPixmap, size: int) -> QPixmap:
        """Create circular pixmap from square pixmap."""
        # Scale pixmap to size
        scaled_pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                      Qt.TransformationMode.SmoothTransformation)

        # Create circular mask
        circular_pixmap = QPixmap(size, size)
        circular_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(circular_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create circular path
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)

        # Draw the scaled pixmap
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()

        return circular_pixmap

    def add_action_button(self, text: str, action_name: str = None, variant: str = "secondary"):
        """Add action button to the profile card."""
        if action_name is None:
            action_name = text.lower().replace(" ", "_")

        button = BaseButton(text, variant, "small")
        button.clicked.connect(lambda: self.action_clicked.emit(action_name))

        self._action_buttons.append((button, action_name))

        # Add to footer
        if not self.footer_widget.isVisible():
            self.footer_widget.show()

        self.footer_layout.addWidget(button)

    def remove_action_button(self, action_name: str):
        """Remove action button by name."""
        for i, (button, name) in enumerate(self._action_buttons):
            if name == action_name:
                button.setParent(None)
                del self._action_buttons[i]
                break

        # Hide footer if no buttons left
        if not self._action_buttons:
            self.footer_widget.hide()

    def set_name(self, name: str):
        """Update name."""
        self._name = name
        if hasattr(self, 'name_label'):
            self.name_label.setText(name)
        self._set_avatar_initials()  # Update initials if no avatar

    def set_role(self, role: str):
        """Update role."""
        self._role = role
        if hasattr(self, 'role_label'):
            self.role_label.setText(role)

    def set_email(self, email: str):
        """Update email."""
        self._email = email
        if hasattr(self, 'email_label'):
            self.email_label.setText(email)

    def set_avatar(self, avatar_path: str):
        """Update avatar."""
        self._avatar = avatar_path
        self._set_avatar_image(avatar_path)

    def get_name(self) -> str:
        """Get current name."""
        return self._name

    def get_role(self) -> str:
        """Get current role."""
        return self._role

    def get_email(self) -> str:
        """Get current email."""
        return self._email


class CompactProfileCard(ProfileCardWidget):
    """Compact version of profile card."""

    def __init__(self, name="", role="", avatar=None, parent=None):
        super().__init__(name, role, avatar, parent=parent)
        self._setup_compact_ui()

    def _setup_compact_ui(self):
        """Setup compact profile UI."""
        # Override the default UI with a more compact layout
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        # Smaller avatar
        self.avatar_label.setFixedSize(40, 40)
        self.avatar_label.setStyleSheet(f"""
            QLabel {{
                border: 2px solid {theme_manager.get_color('border')};
                border-radius: 20px;
                background-color: {theme_manager.get_color('light')};
            }}
        """)

        if self._avatar:
            self._set_avatar_image(self._avatar)
        else:
            self._set_avatar_initials()

        content_layout.addWidget(self.avatar_label)

        # Info section
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2)

        # Name (smaller font)
        if self._name:
            self.name_label = QLabel(self._name)
            name_font = theme_manager.get_font('default')
            name_font.setWeight(QFont.Weight.Bold)
            self.name_label.setFont(name_font)
            self.name_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
            info_layout.addWidget(self.name_label)

        # Role (smaller font)
        if self._role:
            self.role_label = QLabel(self._role)
            self.role_label.setFont(theme_manager.get_font('caption'))
            self.role_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            info_layout.addWidget(self.role_label)

        content_layout.addWidget(info_widget)
        content_layout.addStretch()

        # Replace body content
        self.set_body(content_widget)


class TeamMemberCard(ProfileCardWidget):
    """Profile card specifically for team members with status."""

    def __init__(self, name="", role="", avatar=None, status="online", parent=None):
        self._status = status
        super().__init__(name, role, avatar, parent=parent)
        self._add_status_indicator()

    def _add_status_indicator(self):
        """Add online status indicator."""
        from PyQt6.QtWidgets import QFrame

        # Status dot
        status_dot = QFrame()
        status_dot.setFixedSize(12, 12)

        status_colors = {
            'online': theme_manager.get_color('success'),
            'away': theme_manager.get_color('warning'),
            'busy': theme_manager.get_color('danger'),
            'offline': theme_manager.get_color('text_secondary')
        }

        color = status_colors.get(self._status, theme_manager.get_color('text_secondary'))

        status_dot.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 6px;
                border: 2px solid white;
            }}
        """)

        # Position status dot on avatar (overlay)
        status_dot.setParent(self.avatar_label)
        status_dot.move(48, 48)  # Bottom right of avatar

    def set_status(self, status: str):
        """Update online status."""
        self._status = status
        self._add_status_indicator()

    def get_status(self) -> str:
        """Get current status."""
        return self._status