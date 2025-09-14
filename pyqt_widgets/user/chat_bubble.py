"""
Chat bubble widget for left/right aligned messages.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QDateTime
from PyQt6.QtGui import QFont, QPainter, QPainterPath, QColor, QBrush
from ..base.theme_manager import theme_manager
from .user_avatar import UserAvatarWidget


class ChatBubbleWidget(QWidget):
    """Message bubble with left/right alignment for chat interfaces."""

    bubble_clicked = pyqtSignal()

    def __init__(self, message="", sender_name="", is_own_message=False,
                 timestamp=None, avatar_path="", parent=None):
        super().__init__(parent)
        self._message = message
        self._sender_name = sender_name
        self._is_own_message = is_own_message
        self._timestamp = timestamp or QDateTime.currentDateTime()
        self._avatar_path = avatar_path
        self._show_avatar = True
        self._show_timestamp = True
        self._setup_ui()

    def _setup_ui(self):
        """Setup the chat bubble UI."""
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(8, 4, 8, 4)
        main_layout.setSpacing(8)

        if self._is_own_message:
            # Own message: avatar on right, bubble on left
            main_layout.addStretch()
            self._create_bubble_content(main_layout)
            if self._show_avatar:
                self._create_avatar(main_layout)
        else:
            # Other's message: avatar on left, bubble on right
            if self._show_avatar:
                self._create_avatar(main_layout)
            self._create_bubble_content(main_layout)
            main_layout.addStretch()

    def _create_avatar(self, layout):
        """Create avatar widget."""
        self.avatar = UserAvatarWidget(self._sender_name, self._avatar_path, 32)
        self.avatar.setFixedSize(32, 32)
        layout.addWidget(self.avatar)

    def _create_bubble_content(self, layout):
        """Create bubble content."""
        bubble_container = QWidget()
        bubble_container.setMaximumWidth(300)
        bubble_layout = QVBoxLayout(bubble_container)
        bubble_layout.setContentsMargins(0, 0, 0, 0)
        bubble_layout.setSpacing(2)

        # Sender name (for other's messages)
        if not self._is_own_message and self._sender_name:
            sender_label = QLabel(self._sender_name)
            sender_label.setFont(theme_manager.get_font('caption'))
            sender_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            bubble_layout.addWidget(sender_label)

        # Message bubble
        self.bubble_widget = MessageBubble(self._message, self._is_own_message)
        self.bubble_widget.clicked.connect(self.bubble_clicked.emit)
        bubble_layout.addWidget(self.bubble_widget)

        # Timestamp
        if self._show_timestamp:
            time_label = QLabel(self._timestamp.toString("hh:mm"))
            time_label.setFont(theme_manager.get_font('caption'))
            time_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")

            if self._is_own_message:
                time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            else:
                time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

            bubble_layout.addWidget(time_label)

        layout.addWidget(bubble_container)

    def set_message(self, message: str):
        """Update message text."""
        self._message = message
        self.bubble_widget.set_message(message)

    def set_timestamp(self, timestamp: QDateTime):
        """Update timestamp."""
        self._timestamp = timestamp

    def set_show_avatar(self, show: bool):
        """Show/hide avatar."""
        self._show_avatar = show

    def set_show_timestamp(self, show: bool):
        """Show/hide timestamp."""
        self._show_timestamp = show

    def get_message(self) -> str:
        """Get message text."""
        return self._message

    def is_own_message(self) -> bool:
        """Check if this is user's own message."""
        return self._is_own_message


class MessageBubble(QWidget):
    """Individual message bubble with custom painting."""

    clicked = pyqtSignal()

    def __init__(self, message="", is_own_message=False, parent=None):
        super().__init__(parent)
        self._message = message
        self._is_own_message = is_own_message
        self._setup_ui()

    def _setup_ui(self):
        """Setup bubble UI."""
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        # Message label
        self.message_label = QLabel(self._message)
        self.message_label.setFont(theme_manager.get_font('default'))
        self.message_label.setWordWrap(True)

        # Color based on message type
        if self._is_own_message:
            bg_color = theme_manager.get_color('primary')
            text_color = 'white'
        else:
            bg_color = theme_manager.get_color('light')
            text_color = theme_manager.get_color('text')

        self.message_label.setStyleSheet(f"color: {text_color}; background: transparent;")
        layout.addWidget(self.message_label)

        # Apply bubble styling
        self.setStyleSheet(f"""
            MessageBubble {{
                background-color: {bg_color};
                border-radius: 12px;
            }}
            MessageBubble:hover {{
                background-color: {self._get_hover_color(bg_color)};
            }}
        """)

    def _get_hover_color(self, base_color: str) -> str:
        """Get hover color variation."""
        # Simple darkening - in real implementation you'd use QColor
        return base_color

    def mousePressEvent(self, event):
        """Handle click events."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def set_message(self, message: str):
        """Update message text."""
        self._message = message
        self.message_label.setText(message)


class GroupedChatBubbles(QWidget):
    """Container for grouping consecutive messages from same sender."""

    def __init__(self, sender_name="", is_own_message=False, parent=None):
        super().__init__(parent)
        self._sender_name = sender_name
        self._is_own_message = is_own_message
        self._messages = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup grouped bubbles UI."""
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(8, 4, 8, 4)
        main_layout.setSpacing(8)

        # Messages container
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setContentsMargins(0, 0, 0, 0)
        self.messages_layout.setSpacing(2)

        if self._is_own_message:
            # Own messages: right aligned
            main_layout.addStretch()
            main_layout.addWidget(self.messages_container)
            # Avatar at bottom
            self.avatar = UserAvatarWidget(self._sender_name, "", 32)
            main_layout.addWidget(self.avatar)
        else:
            # Other's messages: left aligned
            # Avatar at bottom
            self.avatar = UserAvatarWidget(self._sender_name, "", 32)
            main_layout.addWidget(self.avatar)
            main_layout.addWidget(self.messages_container)
            main_layout.addStretch()

        # Sender name
        if not self._is_own_message:
            sender_label = QLabel(self._sender_name)
            sender_label.setFont(theme_manager.get_font('caption'))
            sender_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            self.messages_layout.addWidget(sender_label)

    def add_message(self, message: str, timestamp: QDateTime = None):
        """Add message to group."""
        bubble = MessageBubble(message, self._is_own_message)
        self._messages.append((message, timestamp or QDateTime.currentDateTime()))
        self.messages_layout.addWidget(bubble)

    def get_messages(self) -> list:
        """Get all messages in group."""
        return self._messages.copy()


class TypingIndicator(QWidget):
    """Typing indicator bubble."""

    def __init__(self, sender_name="", parent=None):
        super().__init__(parent)
        self._sender_name = sender_name
        self._setup_ui()
        self._start_animation()

    def _setup_ui(self):
        """Setup typing indicator UI."""
        # Layout similar to chat bubble
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(8, 4, 8, 4)
        main_layout.setSpacing(8)

        # Avatar
        avatar = UserAvatarWidget(self._sender_name, "", 32)
        main_layout.addWidget(avatar)

        # Typing bubble
        typing_bubble = QWidget()
        typing_bubble.setFixedSize(60, 30)
        typing_bubble.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_manager.get_color('light')};
                border-radius: 12px;
            }}
        """)

        # Dots container
        dots_layout = QHBoxLayout(typing_bubble)
        dots_layout.setContentsMargins(12, 8, 12, 8)
        dots_layout.setSpacing(4)

        # Animated dots
        self.dots = []
        for i in range(3):
            dot = QLabel("●")
            dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dot.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            dots_layout.addWidget(dot)
            self.dots.append(dot)

        main_layout.addWidget(typing_bubble)
        main_layout.addStretch()

    def _start_animation(self):
        """Start typing animation."""
        from PyQt6.QtCore import QTimer

        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._animate_dots)
        self.animation_timer.start(500)  # 500ms interval
        self.current_dot = 0

    def _animate_dots(self):
        """Animate typing dots."""
        # Reset all dots
        for dot in self.dots:
            dot.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")

        # Highlight current dot
        self.dots[self.current_dot].setStyleSheet(f"color: {theme_manager.get_color('primary')};")
        self.current_dot = (self.current_dot + 1) % len(self.dots)

    def stop_animation(self):
        """Stop typing animation."""
        if hasattr(self, 'animation_timer'):
            self.animation_timer.stop()


class ChatContainer(QWidget):
    """Container for managing multiple chat bubbles."""

    message_sent = pyqtSignal(str)  # Emits sent message

    def __init__(self, parent=None):
        super().__init__(parent)
        self._messages = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup chat container UI."""
        from PyQt6.QtWidgets import QScrollArea

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scrollable messages area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Messages container
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setContentsMargins(0, 0, 0, 0)
        self.messages_layout.setSpacing(4)
        self.messages_layout.addStretch()

        scroll_area.setWidget(self.messages_container)
        main_layout.addWidget(scroll_area)

        # Input area
        self._create_input_area(main_layout)

    def _create_input_area(self):
        """Create message input area."""
        from PyQt6.QtWidgets import QLineEdit, QPushButton

        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(8, 8, 8, 8)
        input_layout.setSpacing(8)

        # Message input
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.returnPressed.connect(self._send_message)
        input_layout.addWidget(self.message_input)

        # Send button
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self._send_message)
        input_layout.addWidget(send_btn)

        return input_container

    def add_message(self, message: str, sender_name: str = "", is_own_message: bool = False,
                    timestamp: QDateTime = None, avatar_path: str = ""):
        """Add message to chat."""
        bubble = ChatBubbleWidget(
            message, sender_name, is_own_message,
            timestamp, avatar_path
        )

        self._messages.append(bubble)
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, bubble)

        # Auto-scroll to bottom
        self._scroll_to_bottom()

    def _send_message(self):
        """Send message from input."""
        message = self.message_input.text().strip()
        if message:
            self.add_message(message, "You", True)
            self.message_input.clear()
            self.message_sent.emit(message)

    def _scroll_to_bottom(self):
        """Scroll to bottom of messages."""
        # Implementation would scroll the scroll area to bottom
        pass

    def clear_messages(self):
        """Clear all messages."""
        for message in self._messages:
            message.setParent(None)
        self._messages.clear()

    def get_messages(self) -> list:
        """Get all messages."""
        return self._messages.copy()