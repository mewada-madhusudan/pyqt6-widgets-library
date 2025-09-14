"""
Profile header widget with banner, avatar, and metadata.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QBrush, QColor
from ..base.theme_manager import theme_manager
from ..base.base_button import BaseButton
from .user_avatar import UserAvatarWidget


class ProfileHeaderWidget(QWidget):
    """Profile header with banner image, avatar, and user information."""

    action_clicked = pyqtSignal(str)  # Emits action name
    avatar_clicked = pyqtSignal()
    banner_clicked = pyqtSignal()

    def __init__(self, name="", title="", bio="", location="",
                 avatar_path="", banner_path="", parent=None):
        super().__init__(parent)
        self._name = name
        self._title = title
        self._bio = bio
        self._location = location
        self._avatar_path = avatar_path
        self._banner_path = banner_path
        self._actions = []
        self._stats = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup the profile header UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Banner section
        self.banner_section = self._create_banner_section()
        main_layout.addWidget(self.banner_section)

        # Profile info section
        self.info_section = self._create_info_section()
        main_layout.addWidget(self.info_section)

    def _create_banner_section(self) -> QWidget:
        """Create banner section with background image."""
        banner_container = QWidget()
        banner_container.setFixedHeight(200)

        # Banner background
        if self._banner_path:
            # In real implementation, load and display banner image
            banner_container.setStyleSheet(f"""
                QWidget {{
                    background-color: {theme_manager.get_color('primary')};
                    background-image: url({self._banner_path});
                    background-repeat: no-repeat;
                    background-position: center;
                    background-size: cover;
                }}
            """)
        else:
            # Default gradient background
            banner_container.setStyleSheet(f"""
                QWidget {{
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 {theme_manager.get_color('primary')},
                        stop: 1 {theme_manager.get_color('secondary')}
                    );
                }}
            """)

        # Make banner clickable
        banner_container.mousePressEvent = lambda \
            event: self.banner_clicked.emit() if event.button() == Qt.MouseButton.LeftButton else None

        return banner_container

    def _create_info_section(self) -> QWidget:
        """Create profile information section."""
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(20, 0, 20, 20)
        info_layout.setSpacing(16)

        # Avatar and basic info row
        header_row = self._create_header_row()
        info_layout.addWidget(header_row)

        # Bio section
        if self._bio:
            bio_section = self._create_bio_section()
            info_layout.addWidget(bio_section)

        # Stats section
        if self._stats:
            stats_section = self._create_stats_section()
            info_layout.addWidget(stats_section)

        # Apply styling
        info_container.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_manager.get_color('surface')};
                border: 1px solid {theme_manager.get_color('border')};
                border-top: none;
            }}
        """)

        return info_container

    def _create_header_row(self) -> QWidget:
        """Create header row with avatar, name, and actions."""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(16)

        # Avatar (positioned to overlap banner)
        self.avatar = UserAvatarWidget(self._name, self._avatar_path, 80)
        self.avatar.set_clickable(True)
        self.avatar.clicked.connect(self.avatar_clicked.emit)

        # Position avatar to overlap banner
        avatar_container = QWidget()
        avatar_container.setFixedSize(80, 80)
        avatar_layout = QVBoxLayout(avatar_container)
        avatar_layout.setContentsMargins(0, -40, 0, 0)  # Negative margin to overlap
        avatar_layout.addWidget(self.avatar)

        header_layout.addWidget(avatar_container)

        # Name and title
        name_section = QVBoxLayout()
        name_section.setContentsMargins(0, 0, 0, 0)
        name_section.setSpacing(4)

        # Name
        self.name_label = QLabel(self._name)
        name_font = theme_manager.get_font('heading')
        name_font.setPointSize(20)
        name_font.setWeight(QFont.Weight.Bold)
        self.name_label.setFont(name_font)
        self.name_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        name_section.addWidget(self.name_label)

        # Title
        if self._title:
            self.title_label = QLabel(self._title)
            title_font = theme_manager.get_font('default')
            title_font.setPointSize(14)
            self.title_label.setFont(title_font)
            self.title_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            name_section.addWidget(self.title_label)

        # Location
        if self._location:
            location_label = QLabel(f"📍 {self._location}")
            location_label.setFont(theme_manager.get_font('caption'))
            location_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            name_section.addWidget(location_label)

        header_layout.addLayout(name_section)
        header_layout.addStretch()

        # Action buttons
        self.actions_container = QWidget()
        self.actions_layout = QHBoxLayout(self.actions_container)
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        self.actions_layout.setSpacing(8)

        header_layout.addWidget(self.actions_container)

        return header_widget

    def _create_bio_section(self) -> QWidget:
        """Create bio section."""
        bio_container = QWidget()
        bio_layout = QVBoxLayout(bio_container)
        bio_layout.setContentsMargins(0, 0, 0, 0)

        self.bio_label = QLabel(self._bio)
        self.bio_label.setFont(theme_manager.get_font('default'))
        self.bio_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        self.bio_label.setWordWrap(True)
        bio_layout.addWidget(self.bio_label)

        return bio_container

    def _create_stats_section(self) -> QWidget:
        """Create statistics section."""
        stats_container = QWidget()
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(24)

        for stat_name, stat_value in self._stats.items():
            stat_widget = self._create_stat_widget(stat_name, stat_value)
            stats_layout.addWidget(stat_widget)

        stats_layout.addStretch()
        return stats_container

    def _create_stat_widget(self, name: str, value) -> QWidget:
        """Create individual stat widget."""
        stat_container = QWidget()
        stat_layout = QVBoxLayout(stat_container)
        stat_layout.setContentsMargins(0, 0, 0, 0)
        stat_layout.setSpacing(2)
        stat_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Value
        value_label = QLabel(str(value))
        value_font = theme_manager.get_font('heading')
        value_font.setPointSize(16)
        value_font.setWeight(QFont.Weight.Bold)
        value_label.setFont(value_font)
        value_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stat_layout.addWidget(value_label)

        # Name
        name_label = QLabel(name)
        name_label.setFont(theme_manager.get_font('caption'))
        name_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stat_layout.addWidget(name_label)

        return stat_container

    def add_action(self, text: str, action_name: str = None, variant: str = "primary"):
        """Add action button to profile header."""
        if action_name is None:
            action_name = text.lower().replace(" ", "_")

        action_btn = BaseButton(text, variant, "medium")
        action_btn.clicked.connect(lambda: self.action_clicked.emit(action_name))

        self.actions_layout.addWidget(action_btn)
        self._actions.append((action_btn, action_name))

    def remove_action(self, action_name: str):
        """Remove action by name."""
        for i, (button, name) in enumerate(self._actions):
            if name == action_name:
                button.setParent(None)
                del self._actions[i]
                break

    def add_stat(self, name: str, value):
        """Add statistic to profile."""
        self._stats[name] = value

        # Recreate stats section
        if hasattr(self, 'info_section'):
            # Would need to rebuild the stats section
            pass

    def set_name(self, name: str):
        """Update profile name."""
        self._name = name
        self.name_label.setText(name)
        self.avatar.set_name(name)

    def set_title(self, title: str):
        """Update profile title."""
        self._title = title
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)

    def set_bio(self, bio: str):
        """Update profile bio."""
        self._bio = bio
        if hasattr(self, 'bio_label'):
            self.bio_label.setText(bio)

    def set_location(self, location: str):
        """Update location."""
        self._location = location

    def set_avatar(self, avatar_path: str):
        """Update avatar image."""
        self._avatar_path = avatar_path
        self.avatar.set_image(avatar_path)

    def set_banner(self, banner_path: str):
        """Update banner image."""
        self._banner_path = banner_path
        # Would need to update banner styling

    def get_name(self) -> str:
        """Get profile name."""
        return self._name

    def get_stats(self) -> dict:
        """Get profile statistics."""
        return self._stats.copy()


class CompactProfileHeader(ProfileHeaderWidget):
    """Compact version of profile header."""

    def __init__(self, name="", title="", avatar_path="", parent=None):
        super().__init__(name, title, "", "", avatar_path, "", parent)

    def _create_banner_section(self) -> QWidget:
        """Override to create smaller banner."""
        banner_container = QWidget()
        banner_container.setFixedHeight(100)  # Smaller height

        banner_container.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {theme_manager.get_color('primary')},
                    stop: 1 {theme_manager.get_color('secondary')}
                );
            }}
        """)

        return banner_container

    def _create_header_row(self) -> QWidget:
        """Override for compact layout."""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        # Smaller avatar
        self.avatar = UserAvatarWidget(self._name, self._avatar_path, 60)
        self.avatar.set_clickable(True)
        self.avatar.clicked.connect(self.avatar_clicked.emit)

        # Position avatar
        avatar_container = QWidget()
        avatar_container.setFixedSize(60, 60)
        avatar_layout = QVBoxLayout(avatar_container)
        avatar_layout.setContentsMargins(0, -30, 0, 0)  # Less overlap
        avatar_layout.addWidget(self.avatar)

        header_layout.addWidget(avatar_container)

        # Name and title (more compact)
        name_section = QVBoxLayout()
        name_section.setContentsMargins(0, 0, 0, 0)
        name_section.setSpacing(2)

        # Name
        self.name_label = QLabel(self._name)
        name_font = theme_manager.get_font('heading')
        name_font.setPointSize(16)  # Smaller font
        name_font.setWeight(QFont.Weight.Bold)
        self.name_label.setFont(name_font)
        self.name_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        name_section.addWidget(self.name_label)

        # Title
        if self._title:
            self.title_label = QLabel(self._title)
            self.title_label.setFont(theme_manager.get_font('default'))
            self.title_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            name_section.addWidget(self.title_label)

        header_layout.addLayout(name_section)
        header_layout.addStretch()

        # Single action button
        self.actions_container = QWidget()
        self.actions_layout = QHBoxLayout(self.actions_container)
        self.actions_layout.setContentsMargins(0, 0, 0, 0)

        header_layout.addWidget(self.actions_container)

        return header_widget


class BusinessProfileHeader(ProfileHeaderWidget):
    """Profile header for business/organization profiles."""

    def __init__(self, name="", industry="", website="", founded="",
                 avatar_path="", banner_path="", parent=None):
        self._industry = industry
        self._website = website
        self._founded = founded

        super().__init__(name, industry, "", "", avatar_path, banner_path, parent)
        self._add_business_info()

    def _add_business_info(self):
        """Add business-specific information."""
        # Add industry as title
        if self._industry:
            self.set_title(self._industry)

        # Add business stats
        if self._founded:
            self.add_stat("Founded", self._founded)

        # Add business actions
        self.add_action("Visit Website", "website", "secondary")
        self.add_action("Contact", "contact", "primary")

    def set_industry(self, industry: str):
        """Set business industry."""
        self._industry = industry
        self.set_title(industry)

    def set_website(self, website: str):
        """Set business website."""
        self._website = website

    def set_founded(self, founded: str):
        """Set founding date."""
        self._founded = founded


class SocialProfileHeader(ProfileHeaderWidget):
    """Profile header with social media features."""

    def __init__(self, name="", username="", bio="", avatar_path="",
                 banner_path="", parent=None):
        self._username = username

        # Add @ to username if not present
        if username and not username.startswith('@'):
            username = f"@{username}"

        super().__init__(name, username, bio, "", avatar_path, banner_path, parent)
        self._add_social_features()

    def _add_social_features(self):
        """Add social media features."""
        # Add social stats
        self.add_stat("Posts", 0)
        self.add_stat("Followers", 0)
        self.add_stat("Following", 0)

        # Add social actions
        self.add_action("Follow", "follow", "primary")
        self.add_action("Message", "message", "secondary")

    def set_username(self, username: str):
        """Set username."""
        self._username = username
        if username and not username.startswith('@'):
            username = f"@{username}"
        self.set_title(username)

    def set_social_stats(self, posts: int, followers: int, following: int):
        """Update social statistics."""
        self._stats["Posts"] = posts
        self._stats["Followers"] = followers
        self._stats["Following"] = following

        # Would need to update stats display

    def get_username(self) -> str:
        """Get username."""
        return self._username