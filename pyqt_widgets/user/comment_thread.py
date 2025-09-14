"""
Comment thread widget for nested threaded comments.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QTextEdit, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QDateTime
from PyQt6.QtGui import QFont
from ..base.theme_manager import theme_manager
from ..base.base_button import BaseButton
from .user_avatar import UserAvatarWidget


class CommentWidget(QWidget):
    """Individual comment widget."""

    reply_clicked = pyqtSignal()
    like_clicked = pyqtSignal()
    edit_clicked = pyqtSignal()
    delete_clicked = pyqtSignal()

    def __init__(self, author="", content="", timestamp=None,
                 avatar_path="", likes=0, comment_id=None, parent=None):
        super().__init__(parent)
        self._author = author
        self._content = content
        self._timestamp = timestamp or QDateTime.currentDateTime()
        self._avatar_path = avatar_path
        self._likes = likes
        self._comment_id = comment_id or id(self)
        self._is_liked = False
        self._is_editing = False
        self._setup_ui()

    def _setup_ui(self):
        """Setup comment UI."""
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(12, 8, 12, 8)
        main_layout.setSpacing(12)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Avatar
        self.avatar = UserAvatarWidget(self._author, self._avatar_path, 32)
        main_layout.addWidget(self.avatar)

        # Content area
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(4)

        # Header (author and timestamp)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        # Author name
        author_label = QLabel(self._author)
        author_font = theme_manager.get_font('default')
        author_font.setWeight(QFont.Weight.Bold)
        author_label.setFont(author_font)
        author_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        header_layout.addWidget(author_label)

        # Timestamp
        time_label = QLabel(self._format_timestamp())
        time_label.setFont(theme_manager.get_font('caption'))
        time_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        header_layout.addWidget(time_label)

        header_layout.addStretch()
        content_layout.addLayout(header_layout)

        # Comment content
        self.content_label = QLabel(self._content)
        self.content_label.setFont(theme_manager.get_font('default'))
        self.content_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        self.content_label.setWordWrap(True)
        content_layout.addWidget(self.content_label)

        # Edit text area (hidden by default)
        self.edit_text = QTextEdit()
        self.edit_text.setPlainText(self._content)
        self.edit_text.setMaximumHeight(100)
        self.edit_text.hide()
        content_layout.addWidget(self.edit_text)

        # Actions
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(0, 4, 0, 0)
        actions_layout.setSpacing(12)

        # Like button
        self.like_btn = QPushButton(f"👍 {self._likes}")
        self.like_btn.setFlat(True)
        self.like_btn.clicked.connect(self._on_like_clicked)
        self.like_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                color: {theme_manager.get_color('text_secondary')};
                padding: 4px 8px;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
                border-radius: 4px;
            }}
        """)
        actions_layout.addWidget(self.like_btn)

        # Reply button
        reply_btn = QPushButton("Reply")
        reply_btn.setFlat(True)
        reply_btn.clicked.connect(self.reply_clicked.emit)
        reply_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                color: {theme_manager.get_color('text_secondary')};
                padding: 4px 8px;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
                border-radius: 4px;
            }}
        """)
        actions_layout.addWidget(reply_btn)

        # Edit button
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setFlat(True)
        self.edit_btn.clicked.connect(self._toggle_edit)
        self.edit_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                color: {theme_manager.get_color('text_secondary')};
                padding: 4px 8px;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
                border-radius: 4px;
            }}
        """)
        actions_layout.addWidget(self.edit_btn)

        # Delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setFlat(True)
        delete_btn.clicked.connect(self.delete_clicked.emit)
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                color: {theme_manager.get_color('danger')};
                padding: 4px 8px;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
                border-radius: 4px;
            }}
        """)
        actions_layout.addWidget(delete_btn)

        actions_layout.addStretch()
        content_layout.addLayout(actions_layout)

        # Save/Cancel buttons for editing (hidden by default)
        self.edit_actions = QWidget()
        edit_actions_layout = QHBoxLayout(self.edit_actions)
        edit_actions_layout.setContentsMargins(0, 4, 0, 0)
        edit_actions_layout.setSpacing(8)

        save_btn = BaseButton("Save", "primary", "small")
        save_btn.clicked.connect(self._save_edit)
        edit_actions_layout.addWidget(save_btn)

        cancel_btn = BaseButton("Cancel", "ghost", "small")
        cancel_btn.clicked.connect(self._cancel_edit)
        edit_actions_layout.addWidget(cancel_btn)

        edit_actions_layout.addStretch()
        self.edit_actions.hide()
        content_layout.addWidget(self.edit_actions)

        main_layout.addLayout(content_layout)

        # Apply styling
        self.setStyleSheet(f"""
            CommentWidget {{
                background-color: {theme_manager.get_color('surface')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}
            CommentWidget:hover {{
                border-color: {theme_manager.get_color('primary')};
            }}
        """)

    def _format_timestamp(self) -> str:
        """Format timestamp for display."""
        now = QDateTime.currentDateTime()
        seconds_ago = self._timestamp.secsTo(now)

        if seconds_ago < 60:
            return "just now"
        elif seconds_ago < 3600:
            minutes = seconds_ago // 60
            return f"{minutes}m ago"
        elif seconds_ago < 86400:
            hours = seconds_ago // 3600
            return f"{hours}h ago"
        else:
            days = seconds_ago // 86400
            return f"{days}d ago"

    def _on_like_clicked(self):
        """Handle like button click."""
        self._is_liked = not self._is_liked
        if self._is_liked:
            self._likes += 1
            self.like_btn.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background: transparent;
                    color: {theme_manager.get_color('primary')};
                    padding: 4px 8px;
                }}
                QPushButton:hover {{
                    background-color: {theme_manager.get_color('hover')};
                    border-radius: 4px;
                }}
            """)
        else:
            self._likes -= 1
            self.like_btn.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background: transparent;
                    color: {theme_manager.get_color('text_secondary')};
                    padding: 4px 8px;
                }}
                QPushButton:hover {{
                    background-color: {theme_manager.get_color('hover')};
                    border-radius: 4px;
                }}
            """)

        self.like_btn.setText(f"👍 {self._likes}")
        self.like_clicked.emit()

    def _toggle_edit(self):
        """Toggle edit mode."""
        if self._is_editing:
            self._cancel_edit()
        else:
            self._start_edit()

    def _start_edit(self):
        """Start editing mode."""
        self._is_editing = True
        self.content_label.hide()
        self.edit_text.show()
        self.edit_actions.show()
        self.edit_btn.setText("Cancel")

    def _save_edit(self):
        """Save edited content."""
        new_content = self.edit_text.toPlainText().strip()
        if new_content:
            self._content = new_content
            self.content_label.setText(new_content)
            self.edit_clicked.emit()

        self._end_edit()

    def _cancel_edit(self):
        """Cancel editing."""
        self.edit_text.setPlainText(self._content)  # Reset to original
        self._end_edit()

    def _end_edit(self):
        """End editing mode."""
        self._is_editing = False
        self.edit_text.hide()
        self.edit_actions.hide()
        self.content_label.show()
        self.edit_btn.setText("Edit")

    def get_comment_id(self):
        """Get comment ID."""
        return self._comment_id

    def get_content(self) -> str:
        """Get comment content."""
        return self._content

    def get_author(self) -> str:
        """Get comment author."""
        return self._author

    def get_likes(self) -> int:
        """Get number of likes."""
        return self._likes


class CommentThreadWidget(QWidget):
    """Widget for displaying nested comment threads."""

    comment_added = pyqtSignal(str, str)  # parent_id, content
    comment_edited = pyqtSignal(str, str)  # comment_id, new_content
    comment_deleted = pyqtSignal(str)  # comment_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self._comments = {}  # comment_id -> comment_widget
        self._comment_tree = {}  # parent_id -> [child_ids]
        self._setup_ui()

    def _setup_ui(self):
        """Setup comment thread UI."""
        from PyQt6.QtWidgets import QScrollArea

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 8, 12, 8)

        title_label = QLabel("Comments")
        title_font = theme_manager.get_font('heading')
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Comment count
        self.count_label = QLabel("0 comments")
        self.count_label.setFont(theme_manager.get_font('caption'))
        self.count_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        header_layout.addWidget(self.count_label)

        main_layout.addWidget(header)

        # Add comment form
        self.add_comment_form = self._create_comment_form()
        main_layout.addWidget(self.add_comment_form)

        # Comments scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Comments container
        self.comments_container = QWidget()
        self.comments_layout = QVBoxLayout(self.comments_container)
        self.comments_layout.setContentsMargins(0, 0, 0, 0)
        self.comments_layout.setSpacing(8)
        self.comments_layout.addStretch()

        scroll_area.setWidget(self.comments_container)
        main_layout.addWidget(scroll_area)

    def _create_comment_form(self, parent_id: str = None) -> QWidget:
        """Create comment input form."""
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(12, 8, 12, 8)
        form_layout.setSpacing(8)

        # Text input
        text_edit = QTextEdit()
        text_edit.setPlaceholderText("Write a comment...")
        text_edit.setMaximumHeight(80)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                background-color: {theme_manager.get_color('surface')};
                padding: 8px;
            }}
        """)
        form_layout.addWidget(text_edit)

        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.addStretch()

        cancel_btn = BaseButton("Cancel", "ghost", "small")
        cancel_btn.clicked.connect(lambda: self._cancel_comment(form_container))
        buttons_layout.addWidget(cancel_btn)

        post_btn = BaseButton("Post Comment", "primary", "small")
        post_btn.clicked.connect(lambda: self._post_comment(text_edit, parent_id, form_container))
        buttons_layout.addWidget(post_btn)

        form_layout.addLayout(buttons_layout)

        # Initially hide if it's a reply form
        if parent_id:
            form_container.hide()

        return form_container

    def _post_comment(self, text_edit: QTextEdit, parent_id: str, form_container: QWidget):
        """Post new comment."""
        content = text_edit.toPlainText().strip()
        if not content:
            return

        # Create comment
        comment_id = str(len(self._comments))
        comment = CommentWidget(
            author="Current User",  # In real app, get from auth
            content=content,
            comment_id=comment_id
        )

        # Connect signals
        comment.reply_clicked.connect(lambda: self._show_reply_form(comment_id))
        comment.edit_clicked.connect(lambda: self.comment_edited.emit(comment_id, comment.get_content()))
        comment.delete_clicked.connect(lambda: self._delete_comment(comment_id))

        # Add to data structures
        self._comments[comment_id] = comment
        if parent_id:
            if parent_id not in self._comment_tree:
                self._comment_tree[parent_id] = []
            self._comment_tree[parent_id].append(comment_id)
        else:
            if "root" not in self._comment_tree:
                self._comment_tree["root"] = []
            self._comment_tree["root"].append(comment_id)

        # Add to UI
        self._rebuild_comments_ui()

        # Clear form
        text_edit.clear()
        if parent_id:  # Hide reply form
            form_container.hide()

        # Update count
        self._update_comment_count()

        # Emit signal
        self.comment_added.emit(parent_id or "root", content)

    def _cancel_comment(self, form_container: QWidget):
        """Cancel comment input."""
        form_container.hide()

    def _show_reply_form(self, parent_id: str):
        """Show reply form for comment."""
        # Implementation would show reply form below the comment
        pass

    def _delete_comment(self, comment_id: str):
        """Delete comment and its replies."""
        if comment_id in self._comments:
            # Remove from UI
            self._comments[comment_id].setParent(None)

            # Remove from data structures
            del self._comments[comment_id]

            # Remove from tree and remove children
            self._remove_from_tree(comment_id)

            # Rebuild UI
            self._rebuild_comments_ui()

            # Update count
            self._update_comment_count()

            # Emit signal
            self.comment_deleted.emit(comment_id)

    def _remove_from_tree(self, comment_id: str):
        """Remove comment from tree structure."""
        # Remove from parent's children list
        for parent_id, children in self._comment_tree.items():
            if comment_id in children:
                children.remove(comment_id)
                break

        # Remove children recursively
        if comment_id in self._comment_tree:
            for child_id in self._comment_tree[comment_id][:]:
                self._delete_comment(child_id)
            del self._comment_tree[comment_id]

    def _rebuild_comments_ui(self):
        """Rebuild the comments UI."""
        # Clear existing comments from layout
        for i in reversed(range(self.comments_layout.count() - 1)):  # Keep stretch
            item = self.comments_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        # Add comments in tree order
        self._add_comments_recursive("root", 0)

    def _add_comments_recursive(self, parent_id: str, depth: int):
        """Recursively add comments to UI."""
        if parent_id not in self._comment_tree:
            return

        for comment_id in self._comment_tree[parent_id]:
            if comment_id in self._comments:
                comment_widget = self._comments[comment_id]

                # Create container with indentation
                if depth > 0:
                    container = QWidget()
                    container_layout = QHBoxLayout(container)
                    container_layout.setContentsMargins(depth * 30, 0, 0, 0)
                    container_layout.addWidget(comment_widget)
                    self.comments_layout.insertWidget(self.comments_layout.count() - 1, container)
                else:
                    self.comments_layout.insertWidget(self.comments_layout.count() - 1, comment_widget)

                # Add children
                self._add_comments_recursive(comment_id, depth + 1)

    def _update_comment_count(self):
        """Update comment count display."""
        count = len(self._comments)
        self.count_label.setText(f"{count} comment{'s' if count != 1 else ''}")

    def add_comment(self, author: str, content: str, parent_id: str = None,
                   timestamp: QDateTime = None, avatar_path: str = ""):
        """Add comment programmatically."""
        comment_id = str(len(self._comments))
        comment = CommentWidget(
            author=author,
            content=content,
            timestamp=timestamp,
            avatar_path=avatar_path,
            comment_id=comment_id
        )

        # Connect signals
        comment.reply_clicked.connect(lambda: self._show_reply_form(comment_id))
        comment.edit_clicked.connect(lambda: self.comment_edited.emit(comment_id, comment.get_content()))
        comment.delete_clicked.connect(lambda: self._delete_comment(comment_id))

        # Add to data structures
        self._comments[comment_id] = comment
        parent_key = parent_id or "root"
        if parent_key not in self._comment_tree:
            self._comment_tree[parent_key] = []
        self._comment_tree[parent_key].append(comment_id)

        # Rebuild UI
        self._rebuild_comments_ui()
        self._update_comment_count()

        return comment_id

    def clear_comments(self):
        """Clear all comments."""
        self._comments.clear()
        self._comment_tree.clear()
        self._rebuild_comments_ui()
        self._update_comment_count()

    def get_comments_count(self) -> int:
        """Get total number of comments."""
        return len(self._comments)