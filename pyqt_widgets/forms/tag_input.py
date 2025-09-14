"""
Tag input widget with multi-select chips and autocomplete.
"""

from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLineEdit,
                             QLabel, QPushButton, QListWidget, QListWidgetItem,
                             QFrame, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QKeyEvent
from ..base.theme_manager import theme_manager


class TagChip(QWidget):
    """Individual tag chip widget."""

    removed = pyqtSignal(str)  # Emits tag text

    def __init__(self, text: str, removable: bool = True, parent=None):
        super().__init__(parent)
        self._text = text
        self._removable = removable
        self._setup_ui()

    def _setup_ui(self):
        """Setup tag chip UI."""
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 4 if self._removable else 8, 4)
        layout.setSpacing(4)

        # Tag text
        self.text_label = QLabel(self._text)
        self.text_label.setFont(theme_manager.get_font('caption'))
        layout.addWidget(self.text_label)

        # Remove button
        if self._removable:
            self.remove_btn = QPushButton("×")
            self.remove_btn.setFixedSize(16, 16)
            self.remove_btn.clicked.connect(lambda: self.removed.emit(self._text))
            self.remove_btn.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background: transparent;
                    color: {theme_manager.get_color('text_secondary')};
                    font-size: 12px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    color: {theme_manager.get_color('danger')};
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 8px;
                }}
            """)
            layout.addWidget(self.remove_btn)

        # Apply chip styling
        self.setStyleSheet(f"""
            TagChip {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
                border-radius: 12px;
                max-width: 200px;
            }}
        """)

        self.text_label.setStyleSheet("color: white; background: transparent;")

    def get_text(self) -> str:
        """Get tag text."""
        return self._text


class TagInputWidget(QWidget):
    """Multi-tag input with autocomplete and chips."""

    tag_added = pyqtSignal(str)  # Emits added tag
    tag_removed = pyqtSignal(str)  # Emits removed tag
    tags_changed = pyqtSignal(list)  # Emits current tag list

    def __init__(self, placeholder="Add tags...", suggestions=None,
                 max_tags=None, parent=None):
        super().__init__(parent)
        self._placeholder = placeholder
        self._suggestions = suggestions or []
        self._max_tags = max_tags
        self._tags = []
        self._tag_chips = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup tag input UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(4)

        # Input container
        self.input_container = QWidget()
        self.input_container.setStyleSheet(f"""
            QWidget {{
                border: 2px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
                background-color: {theme_manager.get_color('surface')};
            }}
            QWidget:focus-within {{
                border-color: {theme_manager.get_color('primary')};
            }}
        """)

        # Input layout (tags + input field)
        self.input_layout = QHBoxLayout(self.input_container)
        self.input_layout.setContentsMargins(8, 4, 8, 4)
        self.input_layout.setSpacing(4)

        # Tags scroll area
        self.tags_scroll = QScrollArea()
        self.tags_scroll.setWidgetResizable(True)
        self.tags_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tags_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tags_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.tags_scroll.setMaximumHeight(32)

        # Tags container
        self.tags_container = QWidget()
        self.tags_layout = QHBoxLayout(self.tags_container)
        self.tags_layout.setContentsMargins(0, 0, 0, 0)
        self.tags_layout.setSpacing(4)
        self.tags_layout.addStretch()

        self.tags_scroll.setWidget(self.tags_container)
        self.input_layout.addWidget(self.tags_scroll)

        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(self._placeholder)
        self.input_field.setFrame(False)
        self.input_field.setStyleSheet("QLineEdit { border: none; background: transparent; }")
        self.input_field.returnPressed.connect(self._add_tag_from_input)
        self.input_field.textChanged.connect(self._on_text_changed)
        self.input_field.keyPressEvent = self._handle_key_press

        self.input_layout.addWidget(self.input_field)
        main_layout.addWidget(self.input_container)

        # Suggestions dropdown
        self.suggestions_list = QListWidget()
        self.suggestions_list.setMaximumHeight(150)
        self.suggestions_list.hide()
        self.suggestions_list.itemClicked.connect(self._add_tag_from_suggestion)
        self.suggestions_list.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid {theme_manager.get_color('border')};
                border-top: none;
                border-radius: 0px 0px {theme_manager.get_border_radius('md')}px {theme_manager.get_border_radius('md')}px;
                background-color: {theme_manager.get_color('surface')};
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {theme_manager.get_color('border')};
            }}
            QListWidget::item:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
            QListWidget::item:selected {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
            }}
        """)

        main_layout.addWidget(self.suggestions_list)

    def _handle_key_press(self, event: QKeyEvent):
        """Handle special key presses."""
        if event.key() == Qt.Key.Key_Backspace and not self.input_field.text():
            # Remove last tag on backspace when input is empty
            if self._tags:
                self.remove_tag(self._tags[-1])
        elif event.key() == Qt.Key.Key_Down and self.suggestions_list.isVisible():
            # Navigate suggestions
            self.suggestions_list.setFocus()
        elif event.key() in (Qt.Key.Key_Comma, Qt.Key.Key_Semicolon):
            # Add tag on comma or semicolon
            self._add_tag_from_input()
            event.accept()
            return
        elif event.key() == Qt.Key.Key_Escape:
            # Hide suggestions
            self.suggestions_list.hide()

        # Call original key press handler
        QLineEdit.keyPressEvent(self.input_field, event)

    def _on_text_changed(self, text: str):
        """Handle input text change."""
        if text and self._suggestions:
            self._show_suggestions(text)
        else:
            self.suggestions_list.hide()

    def _show_suggestions(self, query: str):
        """Show filtered suggestions."""
        query_lower = query.lower()

        # Filter suggestions
        filtered = [
            suggestion for suggestion in self._suggestions
            if query_lower in suggestion.lower() and suggestion not in self._tags
        ]

        if filtered:
            self.suggestions_list.clear()
            for suggestion in filtered[:10]:  # Limit to 10 suggestions
                item = QListWidgetItem(suggestion)
                self.suggestions_list.addItem(item)
            self.suggestions_list.show()
        else:
            self.suggestions_list.hide()

    def _add_tag_from_input(self):
        """Add tag from input field."""
        text = self.input_field.text().strip()
        if text:
            self.add_tag(text)
            self.input_field.clear()
            self.suggestions_list.hide()

    def _add_tag_from_suggestion(self, item: QListWidgetItem):
        """Add tag from suggestion click."""
        self.add_tag(item.text())
        self.input_field.clear()
        self.suggestions_list.hide()

    def add_tag(self, tag: str):
        """Add tag to the input."""
        # Validate tag
        if not tag or tag in self._tags:
            return

        # Check max tags limit
        if self._max_tags and len(self._tags) >= self._max_tags:
            return

        # Add to tags list
        self._tags.append(tag)

        # Create chip widget
        chip = TagChip(tag)
        chip.removed.connect(self.remove_tag)
        self._tag_chips[tag] = chip

        # Add to layout (before stretch)
        self.tags_layout.insertWidget(self.tags_layout.count() - 1, chip)

        # Update placeholder
        self._update_placeholder()

        # Emit signals
        self.tag_added.emit(tag)
        self.tags_changed.emit(self._tags.copy())

    def remove_tag(self, tag: str):
        """Remove tag from input."""
        if tag in self._tags:
            # Remove from list
            self._tags.remove(tag)

            # Remove chip widget
            chip = self._tag_chips.pop(tag)
            chip.setParent(None)

            # Update placeholder
            self._update_placeholder()

            # Emit signals
            self.tag_removed.emit(tag)
            self.tags_changed.emit(self._tags.copy())

    def _update_placeholder(self):
        """Update placeholder text based on tags."""
        if self._tags:
            self.input_field.setPlaceholderText("Add more tags...")
        else:
            self.input_field.setPlaceholderText(self._placeholder)

    def set_tags(self, tags: list):
        """Set tags programmatically."""
        # Clear existing tags
        self.clear_tags()

        # Add new tags
        for tag in tags:
            self.add_tag(tag)

    def get_tags(self) -> list:
        """Get current tags."""
        return self._tags.copy()

    def clear_tags(self):
        """Clear all tags."""
        for tag in self._tags.copy():
            self.remove_tag(tag)

    def set_suggestions(self, suggestions: list):
        """Set autocomplete suggestions."""
        self._suggestions = suggestions

    def set_max_tags(self, max_tags: int):
        """Set maximum number of tags."""
        self._max_tags = max_tags

        # Remove excess tags if needed
        if max_tags and len(self._tags) > max_tags:
            excess_tags = self._tags[max_tags:]
            for tag in excess_tags:
                self.remove_tag(tag)


class CategoryTagInput(TagInputWidget):
    """Tag input with category-based suggestions."""

    def __init__(self, categories=None, parent=None):
        super().__init__("Add tags...", [], None, parent)
        self._categories = categories or {}  # category -> [tags]
        self._current_category = None
        self._setup_category_ui()

    def _setup_category_ui(self):
        """Add category selection."""
        from PyQt6.QtWidgets import QComboBox

        # Category selector
        category_layout = QHBoxLayout()
        category_layout.setContentsMargins(0, 0, 0, 4)

        category_label = QLabel("Category:")
        category_label.setFont(theme_manager.get_font('caption'))
        category_layout.addWidget(category_label)

        self.category_combo = QComboBox()
        self.category_combo.addItem("All Categories", None)
        for category in self._categories.keys():
            self.category_combo.addItem(category, category)
        self.category_combo.currentDataChanged.connect(self._on_category_changed)
        category_layout.addWidget(self.category_combo)

        category_layout.addStretch()

        # Insert at top
        self.layout().insertLayout(0, category_layout)

    def _on_category_changed(self, category):
        """Handle category change."""
        self._current_category = category

        # Update suggestions based on category
        if category:
            self.set_suggestions(self._categories.get(category, []))
        else:
            # All suggestions
            all_suggestions = []
            for tags in self._categories.values():
                all_suggestions.extend(tags)
            self.set_suggestions(all_suggestions)


class ColoredTagInput(TagInputWidget):
    """Tag input with colored tags."""

    def __init__(self, tag_colors=None, parent=None):
        super().__init__("Add tags...", [], None, parent)
        self._tag_colors = tag_colors or {}  # tag -> color

    def add_tag(self, tag: str):
        """Override to add colored tags."""
        # Call parent method
        super().add_tag(tag)

        # Apply color if available
        if tag in self._tag_chips and tag in self._tag_colors:
            chip = self._tag_chips[tag]
            color = self._tag_colors[tag]
            chip.setStyleSheet(f"""
                TagChip {{
                    background-color: {color};
                    color: white;
                    border-radius: 12px;
                }}
            """)

    def set_tag_color(self, tag: str, color: str):
        """Set color for specific tag."""
        self._tag_colors[tag] = color

        # Update existing chip if present
        if tag in self._tag_chips:
            chip = self._tag_chips[tag]
            chip.setStyleSheet(f"""
                TagChip {{
                    background-color: {color};
                    color: white;
                    border-radius: 12px;
                }}
            """)


class ReadOnlyTagDisplay(QWidget):
    """Read-only display of tags."""

    tag_clicked = pyqtSignal(str)  # Emits clicked tag

    def __init__(self, tags=None, parent=None):
        super().__init__(parent)
        self._tags = tags or []
        self._setup_ui()

    def _setup_ui(self):
        """Setup read-only display."""
        # Layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(4)
        self.layout.addStretch()

        # Add tag chips
        self._update_display()

    def _update_display(self):
        """Update tag display."""
        # Clear existing chips
        for i in reversed(range(self.layout.count() - 1)):  # Keep stretch
            item = self.layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        # Add tag chips
        for tag in self._tags:
            chip = TagChip(tag, removable=False)
            chip.mousePressEvent = lambda event, t=tag: self.tag_clicked.emit(
                t) if event.button() == Qt.MouseButton.LeftButton else None
            chip.setCursor(Qt.CursorShape.PointingHandCursor)

            # Insert before stretch
            self.layout.insertWidget(self.layout.count() - 1, chip)

    def set_tags(self, tags: list):
        """Set tags to display."""
        self._tags = tags
        self._update_display()

    def get_tags(self) -> list:
        """Get current tags."""
        return self._tags.copy()


class CompactTagInput(TagInputWidget):
    """Compact version of tag input."""

    def __init__(self, parent=None):
        super().__init__("Tags...", [], 5, parent)  # Max 5 tags
        self._setup_compact_ui()

    def _setup_compact_ui(self):
        """Override for compact layout."""
        # Smaller container
        self.input_container.setMaximumHeight(32)

        # Smaller chips
        self.tags_scroll.setMaximumHeight(24)

        # Smaller input
        self.input_field.setMaximumHeight(24)

        # Adjust layout margins
        self.input_layout.setContentsMargins(4, 2, 4, 2)
        self.input_layout.setSpacing(2)