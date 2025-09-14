"""
User avatar widget with fallback initials and status indicators.
"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPainterPath, QColor, QBrush
from ..base.theme_manager import theme_manager


class UserAvatarWidget(QWidget):
    """Circular user avatar with initials fallback and status indicator."""

    clicked = pyqtSignal()

    def __init__(self, name="", image_path="", size=48, status=None, parent=None):
        super().__init__(parent)
        self._name = name
        self._image_path = image_path
        self._size = size
        self._status = status  # "online", "away", "busy", "offline"
        self._clickable = False
        self._setup_ui()

    def _setup_ui(self):
        """Setup the avatar UI."""
        self.setFixedSize(self._size, self._size)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Avatar label
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(self._size, self._size)
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.avatar_label)

        # Load avatar
        self._update_avatar()

    def _update_avatar(self):
        """Update avatar display."""
        if self._image_path:
            self._load_image_avatar()
        else:
            self._create_initials_avatar()

        # Add status indicator if specified
        if self._status:
            self._add_status_indicator()

    def _load_image_avatar(self):
        """Load avatar from image file."""
        pixmap = QPixmap(self._image_path)
        if not pixmap.isNull():
            # Create circular avatar
            circular_pixmap = self._create_circular_pixmap(pixmap)
            self.avatar_label.setPixmap(circular_pixmap)
        else:
            # Fallback to initials
            self._create_initials_avatar()

    def _create_initials_avatar(self):
        """Create avatar with initials."""
        # Get initials
        initials = self._get_initials()

        # Create circular background
        pixmap = QPixmap(self._size, self._size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw background circle
        bg_color = self._get_background_color()
        painter.setBrush(QBrush(QColor(bg_color)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self._size, self._size)

        # Draw initials
        painter.setPen(QColor("white"))
        font = theme_manager.get_font('default')
        font.setPointSize(self._size // 3)
        font.setWeight(QFont.Weight.Bold)
        painter.setFont(font)

        painter.drawText(
            0, 0, self._size, self._size,
            Qt.AlignmentFlag.AlignCenter,
            initials
        )

        painter.end()
        self.avatar_label.setPixmap(pixmap)

    def _create_circular_pixmap(self, pixmap: QPixmap) -> QPixmap:
        """Create circular pixmap from square image."""
        # Scale to avatar size
        scaled = pixmap.scaled(
            self._size, self._size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        # Create circular mask
        circular = QPixmap(self._size, self._size)
        circular.fill(Qt.GlobalColor.transparent)

        painter = QPainter(circular)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create circular path
        path = QPainterPath()
        path.addEllipse(0, 0, self._size, self._size)
        painter.setClipPath(path)

        # Draw scaled image
        painter.drawPixmap(0, 0, scaled)
        painter.end()

        return circular

    def _get_initials(self) -> str:
        """Get initials from name."""
        if not self._name:
            return "?"

        parts = self._name.strip().split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        elif len(parts) == 1 and parts[0]:
            return parts[0][0].upper()
        else:
            return "?"

    def _get_background_color(self) -> str:
        """Get background color based on name hash."""
        if not self._name:
            return theme_manager.get_color('primary')

        # Generate consistent color from name
        colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
            "#FECA57", "#FF9FF3", "#54A0FF", "#5F27CD",
            "#00D2D3", "#FF9F43", "#EE5A24", "#0984E3"
        ]

        hash_value = hash(self._name) % len(colors)
        return colors[hash_value]

    def _add_status_indicator(self):
        """Add status indicator dot."""
        if not self._status:
            return

        # Status colors
        status_colors = {
            'online': '#10B981',  # Green
            'away': '#F59E0B',  # Amber
            'busy': '#EF4444',  # Red
            'offline': '#6B7280'  # Gray
        }

        color = status_colors.get(self._status, status_colors['offline'])

        # Create status dot
        dot_size = max(8, self._size // 6)
        status_dot = QLabel(self)
        status_dot.setFixedSize(dot_size, dot_size)
        status_dot.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                border: 2px solid white;
                border-radius: {dot_size // 2}px;
            }}
        """)

        # Position at bottom-right
        x = self._size - dot_size
        y = self._size - dot_size
        status_dot.move(x, y)
        status_dot.show()

    def set_name(self, name: str):
        """Update user name."""
        self._name = name
        self._update_avatar()

    def set_image(self, image_path: str):
        """Update avatar image."""
        self._image_path = image_path
        self._update_avatar()

    def set_status(self, status: str):
        """Update status indicator."""
        self._status = status
        self._update_avatar()

    def set_size(self, size: int):
        """Update avatar size."""
        self._size = size
        self.setFixedSize(size, size)
        self.avatar_label.setFixedSize(size, size)
        self._update_avatar()

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

    def get_name(self) -> str:
        """Get current name."""
        return self._name

    def get_status(self) -> str:
        """Get current status."""
        return self._status


class AvatarGroup(QWidget):
    """Group of overlapping avatars."""

    def __init__(self, max_visible=4, size=32, parent=None):
        super().__init__(parent)
        self._max_visible = max_visible
        self._size = size
        self._avatars = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup avatar group UI."""
        # Calculate width based on overlap
        overlap = self._size // 3
        width = self._size + (self._max_visible - 1) * (self._size - overlap)
        self.setFixedSize(width, self._size)

    def add_avatar(self, name: str, image_path: str = "", status: str = None):
        """Add avatar to group."""
        avatar = UserAvatarWidget(name, image_path, self._size, status, self)
        self._avatars.append(avatar)
        self._update_positions()

    def _update_positions(self):
        """Update avatar positions with overlap."""
        overlap = self._size // 3

        visible_count = min(len(self._avatars), self._max_visible)

        for i in range(visible_count):
            avatar = self._avatars[i]
            x = i * (self._size - overlap)
            avatar.move(x, 0)
            avatar.show()

        # Hide excess avatars
        for i in range(visible_count, len(self._avatars)):
            self._avatars[i].hide()

        # Show count indicator if there are more avatars
        if len(self._avatars) > self._max_visible:
            self._show_count_indicator()

    def _show_count_indicator(self):
        """Show count of additional avatars."""
        extra_count = len(self._avatars) - self._max_visible

        # Create count avatar
        count_avatar = UserAvatarWidget(f"+{extra_count}", "", self._size, None, self)

        # Position at the end
        overlap = self._size // 3
        x = self._max_visible * (self._size - overlap)
        count_avatar.move(x, 0)
        count_avatar.show()

        # Style as count indicator
        count_avatar.avatar_label.setStyleSheet(f"""
            QLabel {{
                background-color: {theme_manager.get_color('light')};
                border: 2px solid {theme_manager.get_color('border')};
                border-radius: {self._size // 2}px;
                color: {theme_manager.get_color('text')};
            }}
        """)

    def clear_avatars(self):
        """Remove all avatars."""
        for avatar in self._avatars:
            avatar.setParent(None)
        self._avatars.clear()

    def get_avatar_count(self) -> int:
        """Get total number of avatars."""
        return len(self._avatars)


class EditableAvatar(UserAvatarWidget):
    """Avatar with edit functionality."""

    image_changed = pyqtSignal(str)  # Emits new image path

    def __init__(self, name="", image_path="", size=48, parent=None):
        super().__init__(name, image_path, size, None, parent)
        self._editable = True
        self.set_clickable(True)
        self.clicked.connect(self._edit_avatar)

    def _edit_avatar(self):
        """Open image selection dialog."""
        if not self._editable:
            return

        from PyQt6.QtWidgets import QFileDialog

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Avatar Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )

        if filename:
            self.set_image(filename)
            self.image_changed.emit(filename)

    def set_editable(self, editable: bool):
        """Enable/disable editing."""
        self._editable = editable
        self.set_clickable(editable)

        # Add edit indicator
        if editable:
            self._add_edit_indicator()

    def _add_edit_indicator(self):
        """Add visual edit indicator."""
        edit_icon = QLabel("✏", self)
        edit_icon.setFixedSize(16, 16)
        edit_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        edit_icon.setStyleSheet(f"""
            QLabel {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
                border-radius: 8px;
                font-size: 10px;
            }}
        """)

        # Position at top-right
        edit_icon.move(self._size - 16, 0)
        edit_icon.show()


class AnimatedAvatar(UserAvatarWidget):
    """Avatar with hover animations."""

    def __init__(self, name="", image_path="", size=48, parent=None):
        super().__init__(name, image_path, size, None, parent)
        self._setup_animations()

    def _setup_animations(self):
        """Setup hover animations."""
        from PyQt6.QtCore import QPropertyAnimation

        self._scale_animation = QPropertyAnimation(self, b"geometry")
        self._scale_animation.setDuration(150)

    def enterEvent(self, event):
        """Handle mouse enter with scale animation."""
        super().enterEvent(event)

        # Scale up slightly
        current_rect = self.geometry()
        scaled_rect = current_rect.adjusted(-2, -2, 2, 2)

        self._scale_animation.setStartValue(current_rect)
        self._scale_animation.setEndValue(scaled_rect)
        self._scale_animation.start()

    def leaveEvent(self, event):
        """Handle mouse leave with scale animation."""
        super().leaveEvent(event)

        # Scale back to normal
        current_rect = self.geometry()
        normal_rect = current_rect.adjusted(2, 2, -2, -2)

        self._scale_animation.setStartValue(current_rect)
        self._scale_animation.setEndValue(normal_rect)
        self._scale_animation.start()