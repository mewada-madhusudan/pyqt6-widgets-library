"""
Reaction bar widget for emoji/like reactions under content.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ..base.theme_manager import theme_manager


class ReactionBarWidget(QWidget):
    """Bar displaying emoji reactions with counts and interaction."""

    reaction_clicked = pyqtSignal(str)  # Emits reaction emoji
    reaction_added = pyqtSignal(str)  # Emits new reaction emoji
    reaction_removed = pyqtSignal(str)  # Emits removed reaction emoji

    def __init__(self, reactions=None, user_reactions=None, parent=None):
        super().__init__(parent)
        # reactions: {"👍": 5, "❤️": 3, "😂": 2}
        self._reactions = reactions or {}
        # user_reactions: ["👍", "❤️"] - reactions by current user
        self._user_reactions = set(user_reactions or [])
        self._reaction_buttons = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup the reaction bar UI."""
        # Main layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(4)

        # Update display
        self._update_reactions_display()

        # Add reaction button
        self._create_add_button()

        # Stretch to push add button to right
        self.main_layout.addStretch()

    def _update_reactions_display(self):
        """Update the display of all reactions."""
        # Clear existing reaction buttons
        for button in self._reaction_buttons.values():
            button.setParent(None)
        self._reaction_buttons.clear()

        # Add reaction buttons
        for emoji, count in self._reactions.items():
            if count > 0:  # Only show reactions with count > 0
                self._create_reaction_button(emoji, count)

    def _create_reaction_button(self, emoji: str, count: int):
        """Create button for a specific reaction."""
        button = QPushButton(f"{emoji} {count}")
        button.setFlat(True)
        button.clicked.connect(lambda: self._toggle_reaction(emoji))

        # Style based on whether user has reacted
        is_user_reaction = emoji in self._user_reactions

        if is_user_reaction:
            # User has reacted - highlighted style
            button.setStyleSheet(f"""
                QPushButton {{
                    border: 1px solid {theme_manager.get_color('primary')};
                    background-color: {theme_manager.get_color('primary')};
                    color: white;
                    padding: 4px 8px;
                    border-radius: {theme_manager.get_border_radius('sm')}px;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {theme_manager.get_color('dark')};
                }}
            """)
        else:
            # User hasn't reacted - normal style
            button.setStyleSheet(f"""
                QPushButton {{
                    border: 1px solid {theme_manager.get_color('border')};
                    background-color: {theme_manager.get_color('surface')};
                    color: {theme_manager.get_color('text')};
                    padding: 4px 8px;
                    border-radius: {theme_manager.get_border_radius('sm')}px;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {theme_manager.get_color('hover')};
                    border-color: {theme_manager.get_color('primary')};
                }}
            """)

        self._reaction_buttons[emoji] = button

        # Insert before the stretch and add button
        insert_index = self.main_layout.count() - 2  # Before stretch and add button
        if insert_index < 0:
            insert_index = 0
        self.main_layout.insertWidget(insert_index, button)

    def _create_add_button(self):
        """Create add reaction button."""
        self.add_button = QPushButton("😊+")
        self.add_button.setFlat(True)
        self.add_button.clicked.connect(self._show_reaction_picker)

        self.add_button.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid {theme_manager.get_color('border')};
                background-color: {theme_manager.get_color('light')};
                color: {theme_manager.get_color('text_secondary')};
                padding: 4px 8px;
                border-radius: {theme_manager.get_border_radius('sm')}px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
                border-color: {theme_manager.get_color('primary')};
            }}
        """)

        self.main_layout.addWidget(self.add_button)

    def _toggle_reaction(self, emoji: str):
        """Toggle user's reaction to specific emoji."""
        if emoji in self._user_reactions:
            # Remove reaction
            self._user_reactions.remove(emoji)
            self._reactions[emoji] = max(0, self._reactions.get(emoji, 0) - 1)
            self.reaction_removed.emit(emoji)
        else:
            # Add reaction
            self._user_reactions.add(emoji)
            self._reactions[emoji] = self._reactions.get(emoji, 0) + 1
            self.reaction_added.emit(emoji)

        # Update display
        self._update_reactions_display()
        self.reaction_clicked.emit(emoji)

    def _show_reaction_picker(self):
        """Show reaction picker popup."""
        picker = ReactionPicker(self)
        picker.reaction_selected.connect(self._add_new_reaction)

        # Position picker above the add button
        button_pos = self.add_button.mapToGlobal(self.add_button.rect().bottomLeft())
        picker_pos = button_pos - picker.rect().bottomLeft()
        picker.move(picker_pos)
        picker.show()

    def _add_new_reaction(self, emoji: str):
        """Add new reaction from picker."""
        if emoji not in self._user_reactions:
            self._user_reactions.add(emoji)
            self._reactions[emoji] = self._reactions.get(emoji, 0) + 1
            self._update_reactions_display()
            self.reaction_added.emit(emoji)

    def add_reaction(self, emoji: str, count: int = 1):
        """Add reaction programmatically."""
        self._reactions[emoji] = self._reactions.get(emoji, 0) + count
        self._update_reactions_display()

    def remove_reaction(self, emoji: str, count: int = 1):
        """Remove reaction programmatically."""
        if emoji in self._reactions:
            self._reactions[emoji] = max(0, self._reactions[emoji] - count)
            if self._reactions[emoji] == 0:
                del self._reactions[emoji]
            self._update_reactions_display()

    def set_user_reaction(self, emoji: str, reacted: bool):
        """Set whether current user has reacted with emoji."""
        if reacted:
            self._user_reactions.add(emoji)
        else:
            self._user_reactions.discard(emoji)
        self._update_reactions_display()

    def get_reactions(self) -> dict:
        """Get current reactions."""
        return self._reactions.copy()

    def get_user_reactions(self) -> set:
        """Get current user's reactions."""
        return self._user_reactions.copy()

    def clear_reactions(self):
        """Clear all reactions."""
        self._reactions.clear()
        self._user_reactions.clear()
        self._update_reactions_display()


class ReactionPicker(QWidget):
    """Popup widget for selecting reactions."""

    reaction_selected = pyqtSignal(str)  # Emits selected emoji

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup)
        self._setup_ui()

    def _setup_ui(self):
        """Setup reaction picker UI."""
        # Common reactions
        self._reactions = [
            "👍", "👎", "❤️", "😂", "😮", "😢", "😡", "🎉", "👏", "🔥"
        ]

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # Create reaction buttons
        for emoji in self._reactions:
            button = QPushButton(emoji)
            button.setFixedSize(32, 32)
            button.setFlat(True)
            button.clicked.connect(lambda checked, e=emoji: self._select_reaction(e))

            button.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background-color: transparent;
                    border-radius: {theme_manager.get_border_radius('sm')}px;
                    font-size: 16px;
                }}
                QPushButton:hover {{
                    background-color: {theme_manager.get_color('hover')};
                }}
            """)

            layout.addWidget(button)

        # Apply picker styling
        self.setStyleSheet(f"""
            ReactionPicker {{
                background-color: {theme_manager.get_color('surface')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}
        """)

    def _select_reaction(self, emoji: str):
        """Handle reaction selection."""
        self.reaction_selected.emit(emoji)
        self.close()


class SimpleReactionBar(ReactionBarWidget):
    """Simplified reaction bar with just like/dislike."""

    def __init__(self, likes=0, dislikes=0, user_liked=False, user_disliked=False, parent=None):
        reactions = {}
        user_reactions = set()

        if likes > 0:
            reactions["👍"] = likes
        if dislikes > 0:
            reactions["👎"] = dislikes

        if user_liked:
            user_reactions.add("👍")
        if user_disliked:
            user_reactions.add("👎")

        super().__init__(reactions, user_reactions, parent)

    def _create_add_button(self):
        """Override to not show add button for simple version."""
        pass

    def set_likes(self, likes: int, user_liked: bool = False):
        """Set like count and user state."""
        if likes > 0:
            self._reactions["👍"] = likes
        else:
            self._reactions.pop("👍", None)

        if user_liked:
            self._user_reactions.add("👍")
        else:
            self._user_reactions.discard("👍")

        self._update_reactions_display()

    def set_dislikes(self, dislikes: int, user_disliked: bool = False):
        """Set dislike count and user state."""
        if dislikes > 0:
            self._reactions["👎"] = dislikes
        else:
            self._reactions.pop("👎", None)

        if user_disliked:
            self._user_reactions.add("👎")
        else:
            self._user_reactions.discard("👎")

        self._update_reactions_display()

    def get_likes(self) -> int:
        """Get like count."""
        return self._reactions.get("👍", 0)

    def get_dislikes(self) -> int:
        """Get dislike count."""
        return self._reactions.get("👎", 0)

    def is_liked(self) -> bool:
        """Check if user has liked."""
        return "👍" in self._user_reactions

    def is_disliked(self) -> bool:
        """Check if user has disliked."""
        return "👎" in self._user_reactions


class AnimatedReactionBar(ReactionBarWidget):
    """Reaction bar with animation effects."""

    def __init__(self, reactions=None, user_reactions=None, parent=None):
        super().__init__(reactions, user_reactions, parent)

    def _toggle_reaction(self, emoji: str):
        """Override to add animation effects."""
        # Store old count for animation
        old_count = self._reactions.get(emoji, 0)

        # Call parent method
        super()._toggle_reaction(emoji)

        # Animate the button if count changed
        new_count = self._reactions.get(emoji, 0)
        if new_count != old_count and emoji in self._reaction_buttons:
            self._animate_button(self._reaction_buttons[emoji])

    def _animate_button(self, button: QPushButton):
        """Animate button on reaction change."""
        from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

        # Scale animation
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(200)

        original_rect = button.geometry()
        scaled_rect = original_rect.adjusted(-2, -2, 2, 2)

        animation.setStartValue(original_rect)
        animation.setEndValue(scaled_rect)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Return to original size
        def return_to_normal():
            return_animation = QPropertyAnimation(button, b"geometry")
            return_animation.setDuration(200)
            return_animation.setStartValue(scaled_rect)
            return_animation.setEndValue(original_rect)
            return_animation.setEasingCurve(QEasingCurve.Type.InCubic)
            return_animation.start()

        animation.finished.connect(return_to_normal)
        animation.start()


class CompactReactionBar(ReactionBarWidget):
    """Compact reaction bar for smaller spaces."""

    def __init__(self, reactions=None, user_reactions=None, parent=None):
        super().__init__(reactions, user_reactions, parent)

    def _create_reaction_button(self, emoji: str, count: int):
        """Override for compact button style."""
        button = QPushButton(f"{emoji}{count}")  # No space between emoji and count
        button.setFlat(True)
        button.clicked.connect(lambda: self._toggle_reaction(emoji))

        # Compact styling
        is_user_reaction = emoji in self._user_reactions

        button.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid {theme_manager.get_color('border') if not is_user_reaction else theme_manager.get_color('primary')};
                background-color: {theme_manager.get_color('surface') if not is_user_reaction else theme_manager.get_color('primary')};
                color: {theme_manager.get_color('text') if not is_user_reaction else 'white'};
                padding: 2px 4px;
                border-radius: {theme_manager.get_border_radius('sm')}px;
                font-size: 10px;
                min-width: 20px;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover') if not is_user_reaction else theme_manager.get_color('dark')};
            }}
        """)

        self._reaction_buttons[emoji] = button

        # Insert before stretch and add button
        insert_index = self.main_layout.count() - 2
        if insert_index < 0:
            insert_index = 0
        self.main_layout.insertWidget(insert_index, button)

    def _create_add_button(self):
        """Override for compact add button."""
        self.add_button = QPushButton("+")
        self.add_button.setFlat(True)
        self.add_button.clicked.connect(self._show_reaction_picker)

        self.add_button.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid {theme_manager.get_color('border')};
                background-color: {theme_manager.get_color('light')};
                color: {theme_manager.get_color('text_secondary')};
                padding: 2px 4px;
                border-radius: {theme_manager.get_border_radius('sm')}px;
                font-size: 10px;
                min-width: 16px;
                max-width: 16px;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)

        self.main_layout.addWidget(self.add_button)