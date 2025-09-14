"""
Inline edit label widget - editable text label on double-click.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ..base.theme_manager import theme_manager


class InlineEditLabel(QWidget):
    """Label that becomes editable on double-click."""

    text_changed = pyqtSignal(str)  # Emits new text
    editing_started = pyqtSignal()
    editing_finished = pyqtSignal(str)  # Emits final text

    def __init__(self, text="", placeholder="Click to edit",
                 validation_func=None, parent=None):
        super().__init__(parent)
        self._text = text
        self._placeholder = placeholder
        self._validation_func = validation_func
        self._is_editing = False
        self._setup_ui()

    def _setup_ui(self):
        """Setup the inline edit label UI."""
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Display label
        self.display_label = QLabel(self._text or self._placeholder)
        self.display_label.setFont(theme_manager.get_font('default'))

        if self._text:
            self.display_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        else:
            self.display_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")

        layout.addWidget(self.display_label)

        # Edit input (hidden by default)
        self.edit_input = QLineEdit()
        self.edit_input.setText(self._text)
        self.edit_input.hide()
        self.edit_input.returnPressed.connect(self._finish_editing)
        self.edit_input.editingFinished.connect(self._finish_editing)

        self.edit_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {theme_manager.get_color('primary')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                padding: 2px 4px;
                background-color: {theme_manager.get_color('surface')};
            }}
        """)

        layout.addWidget(self.edit_input)

        # Make label clickable
        self.display_label.mouseDoubleClickEvent = self._start_editing

        # Add hover effect
        self.setStyleSheet(f"""
            InlineEditLabel:hover {{
                background-color: {theme_manager.get_color('hover')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
            }}
        """)

    def _start_editing(self, event=None):
        """Start editing mode."""
        if self._is_editing:
            return

        self._is_editing = True
        self.display_label.hide()
        self.edit_input.show()
        self.edit_input.setFocus()
        self.edit_input.selectAll()

        self.editing_started.emit()

    def _finish_editing(self):
        """Finish editing and save changes."""
        if not self._is_editing:
            return

        new_text = self.edit_input.text().strip()

        # Validate if validation function provided
        if self._validation_func and not self._validation_func(new_text):
            # Invalid input - revert to original text
            self.edit_input.setText(self._text)
            return

        # Update text
        old_text = self._text
        self._text = new_text

        # Update display
        self._update_display()

        # Switch back to display mode
        self._is_editing = False
        self.edit_input.hide()
        self.display_label.show()

        # Emit signals
        if new_text != old_text:
            self.text_changed.emit(new_text)
        self.editing_finished.emit(new_text)

    def _update_display(self):
        """Update display label."""
        if self._text:
            self.display_label.setText(self._text)
            self.display_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        else:
            self.display_label.setText(self._placeholder)
            self.display_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")

    def set_text(self, text: str):
        """Set text programmatically."""
        self._text = text
        self.edit_input.setText(text)
        self._update_display()

    def get_text(self) -> str:
        """Get current text."""
        return self._text

    def set_placeholder(self, placeholder: str):
        """Set placeholder text."""
        self._placeholder = placeholder
        if not self._text:
            self._update_display()

    def set_validation(self, validation_func):
        """Set validation function."""
        self._validation_func = validation_func

    def is_editing(self) -> bool:
        """Check if currently editing."""
        return self._is_editing

    def start_editing(self):
        """Programmatically start editing."""
        self._start_editing()

    def cancel_editing(self):
        """Cancel editing without saving."""
        if self._is_editing:
            self.edit_input.setText(self._text)  # Revert to original
            self._finish_editing()


class MultilineInlineEdit(InlineEditLabel):
    """Inline edit for multiline text."""

    def __init__(self, text="", placeholder="Click to edit", parent=None):
        super().__init__(text, placeholder, None, parent)
        self._setup_multiline()

    def _setup_multiline(self):
        """Setup multiline editing."""
        from PyQt6.QtWidgets import QTextEdit

        # Replace line edit with text edit
        self.edit_input.setParent(None)

        self.edit_input = QTextEdit()
        self.edit_input.setPlainText(self._text)
        self.edit_input.setMaximumHeight(100)
        self.edit_input.hide()

        # Connect signals differently for QTextEdit
        self.edit_input.focusOutEvent = self._on_focus_out

        self.layout().addWidget(self.edit_input)

        # Update display label for multiline
        self.display_label.setWordWrap(True)

    def _on_focus_out(self, event):
        """Handle focus out for text edit."""
        from PyQt6.QtWidgets import QTextEdit
        QTextEdit.focusOutEvent(self.edit_input, event)
        self._finish_editing()

    def _finish_editing(self):
        """Override for multiline text."""
        if not self._is_editing:
            return

        new_text = self.edit_input.toPlainText().strip()

        # Update text
        old_text = self._text
        self._text = new_text

        # Update display
        self._update_display()

        # Switch back to display mode
        self._is_editing = False
        self.edit_input.hide()
        self.display_label.show()

        # Emit signals
        if new_text != old_text:
            self.text_changed.emit(new_text)
        self.editing_finished.emit(new_text)

    def set_text(self, text: str):
        """Override for multiline."""
        self._text = text
        self.edit_input.setPlainText(text)
        self._update_display()


class ValidatedInlineEdit(InlineEditLabel):
    """Inline edit with built-in validation patterns."""

    def __init__(self, text="", validation_type="text", parent=None):
        self._validation_type = validation_type
        validation_func = self._get_validation_func(validation_type)

        super().__init__(text, self._get_placeholder(validation_type), validation_func, parent)

    def _get_validation_func(self, validation_type: str):
        """Get validation function for type."""
        if validation_type == "email":
            return self._validate_email
        elif validation_type == "number":
            return self._validate_number
        elif validation_type == "phone":
            return self._validate_phone
        elif validation_type == "url":
            return self._validate_url
        else:
            return None

    def _get_placeholder(self, validation_type: str) -> str:
        """Get placeholder for validation type."""
        placeholders = {
            "email": "Enter email address",
            "number": "Enter number",
            "phone": "Enter phone number",
            "url": "Enter URL",
            "text": "Click to edit"
        }
        return placeholders.get(validation_type, "Click to edit")

    def _validate_email(self, text: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, text))

    def _validate_number(self, text: str) -> bool:
        """Validate number format."""
        try:
            float(text)
            return True
        except ValueError:
            return False

    def _validate_phone(self, text: str) -> bool:
        """Validate phone number format."""
        import re
        # Simple phone validation - digits, spaces, dashes, parentheses
        pattern = r'^[\d\s\-\(\)\+]+$'
        return bool(re.match(pattern, text)) and len(
            text.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')) >= 10

    def _validate_url(self, text: str) -> bool:
        """Validate URL format."""
        import re
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, text))


class InlineEditGroup(QWidget):
    """Group of inline edit labels with coordinated editing."""

    group_changed = pyqtSignal(dict)  # Emits all values as dict

    def __init__(self, parent=None):
        super().__init__(parent)
        self._editors = {}  # name -> editor mapping
        self._setup_ui()

    def _setup_ui(self):
        """Setup group UI."""
        from PyQt6.QtWidgets import QVBoxLayout

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)

    def add_editor(self, name: str, label: str, initial_value: str = "",
                   validation_type: str = "text"):
        """Add editor to group."""
        # Create container with label
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(8)

        # Label
        label_widget = QLabel(f"{label}:")
        label_widget.setFont(theme_manager.get_font('default'))
        label_widget.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        label_widget.setFixedWidth(100)
        container_layout.addWidget(label_widget)

        # Editor
        if validation_type != "text":
            editor = ValidatedInlineEdit(initial_value, validation_type)
        else:
            editor = InlineEditLabel(initial_value)

        editor.text_changed.connect(lambda text, n=name: self._on_editor_changed(n, text))
        container_layout.addWidget(editor)

        self._editors[name] = editor
        self.layout.addWidget(container)

    def _on_editor_changed(self, name: str, text: str):
        """Handle editor change."""
        # Emit all current values
        values = {name: editor.get_text() for name, editor in self._editors.items()}
        self.group_changed.emit(values)

    def get_values(self) -> dict:
        """Get all editor values."""
        return {name: editor.get_text() for name, editor in self._editors.items()}

    def set_values(self, values: dict):
        """Set values for all editors."""
        for name, value in values.items():
            if name in self._editors:
                self._editors[name].set_text(str(value))

    def get_editor(self, name: str) -> InlineEditLabel:
        """Get specific editor."""
        return self._editors.get(name)


class QuickEditLabel(InlineEditLabel):
    """Quick edit label with single-click editing."""

    def __init__(self, text="", parent=None):
        super().__init__(text, "Click to edit", None, parent)

        # Override to use single click instead of double click
        self.display_label.mouseDoubleClickEvent = None
        self.display_label.mousePressEvent = self._on_single_click

    def _on_single_click(self, event):
        """Handle single click to start editing."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._start_editing()