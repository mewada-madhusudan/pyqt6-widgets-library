"""
Rich text editor widget with formatting toolbar.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QToolBar, QToolButton, QColorDialog, QFontComboBox,
                             QSpinBox, QComboBox, QSeparator, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import (QFont, QTextCharFormat, QColor, QIcon, QPixmap,
                         QPainter, QTextCursor, QAction)
from ..base.theme_manager import theme_manager


class RichTextEditorWidget(QWidget):
    """Rich text editor with formatting toolbar."""

    content_changed = pyqtSignal(str)  # Emits HTML content
    text_changed = pyqtSignal(str)  # Emits plain text

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """Setup the rich text editor UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create toolbar
        self.toolbar = self._create_toolbar()
        layout.addWidget(self.toolbar)

        # Create text editor
        self.text_editor = QTextEdit()
        self.text_editor.setMinimumHeight(200)

        # Style the editor
        self.text_editor.setStyleSheet(f"""
            QTextEdit {{
                border: 1px solid {theme_manager.get_color('border')};
                border-top: none;
                background-color: {theme_manager.get_color('background')};
                color: {theme_manager.get_color('text')};
                font-family: 'Segoe UI';
                font-size: 10pt;
                padding: 8px;
            }}
            QTextEdit:focus {{
                border-color: {theme_manager.get_color('primary')};
            }}
        """)

        layout.addWidget(self.text_editor)

    def _create_toolbar(self):
        """Create formatting toolbar."""
        toolbar = QFrame()
        toolbar.setFrameStyle(QFrame.Shape.Box)
        toolbar.setStyleSheet(f"""
            QFrame {{
                background-color: {theme_manager.get_color('surface')};
                border: 1px solid {theme_manager.get_color('border')};
                border-bottom: none;
            }}
        """)

        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        # Font family
        self.font_combo = QFontComboBox()
        self.font_combo.setMaximumWidth(150)
        layout.addWidget(self.font_combo)

        # Font size
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 72)
        self.font_size.setValue(10)
        self.font_size.setMaximumWidth(60)
        layout.addWidget(self.font_size)

        # Separator
        layout.addWidget(self._create_separator())

        # Bold, Italic, Underline
        self.bold_btn = self._create_tool_button("B", "Bold", checkable=True)
        self.bold_btn.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.bold_btn)

        self.italic_btn = self._create_tool_button("I", "Italic", checkable=True)
        self.italic_btn.setStyleSheet("font-style: italic;")
        layout.addWidget(self.italic_btn)

        self.underline_btn = self._create_tool_button("U", "Underline", checkable=True)
        self.underline_btn.setStyleSheet("text-decoration: underline;")
        layout.addWidget(self.underline_btn)

        # Separator
        layout.addWidget(self._create_separator())

        # Text color
        self.text_color_btn = self._create_tool_button("A", "Text Color")
        self.text_color_btn.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        layout.addWidget(self.text_color_btn)

        # Background color
        self.bg_color_btn = self._create_tool_button("H", "Highlight")
        layout.addWidget(self.bg_color_btn)

        # Separator
        layout.addWidget(self._create_separator())

        # Alignment
        self.align_left_btn = self._create_tool_button("⬅", "Align Left", checkable=True)
        layout.addWidget(self.align_left_btn)

        self.align_center_btn = self._create_tool_button("⬌", "Align Center", checkable=True)
        layout.addWidget(self.align_center_btn)

        self.align_right_btn = self._create_tool_button("➡", "Align Right", checkable=True)
        layout.addWidget(self.align_right_btn)

        # Separator
        layout.addWidget(self._create_separator())

        # Lists
        self.bullet_btn = self._create_tool_button("•", "Bullet List")
        layout.addWidget(self.bullet_btn)

        self.number_btn = self._create_tool_button("1.", "Numbered List")
        layout.addWidget(self.number_btn)

        # Stretch to push everything to the left
        layout.addStretch()

        return toolbar

    def _create_tool_button(self, text: str, tooltip: str, checkable: bool = False):
        """Create a toolbar button."""
        btn = QToolButton()
        btn.setText(text)
        btn.setToolTip(tooltip)
        btn.setCheckable(checkable)
        btn.setFixedSize(28, 28)

        btn.setStyleSheet(f"""
            QToolButton {{
                border: 1px solid transparent;
                border-radius: 3px;
                background-color: transparent;
                color: {theme_manager.get_color('text')};
                font-weight: bold;
            }}
            QToolButton:hover {{
                background-color: {theme_manager.get_color('hover')};
                border-color: {theme_manager.get_color('border')};
            }}
            QToolButton:pressed, QToolButton:checked {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
            }}
        """)

        return btn

    def _create_separator(self):
        """Create a toolbar separator."""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet(f"color: {theme_manager.get_color('border')};")
        return separator

    def _setup_connections(self):
        """Setup signal connections."""
        # Font changes
        self.font_combo.currentFontChanged.connect(self._on_font_changed)
        self.font_size.valueChanged.connect(self._on_font_size_changed)

        # Format buttons
        self.bold_btn.toggled.connect(self._on_bold_toggled)
        self.italic_btn.toggled.connect(self._on_italic_toggled)
        self.underline_btn.toggled.connect(self._on_underline_toggled)

        # Colors
        self.text_color_btn.clicked.connect(self._on_text_color_clicked)
        self.bg_color_btn.clicked.connect(self._on_bg_color_clicked)

        # Alignment
        self.align_left_btn.toggled.connect(lambda: self._on_alignment_changed(Qt.AlignmentFlag.AlignLeft))
        self.align_center_btn.toggled.connect(lambda: self._on_alignment_changed(Qt.AlignmentFlag.AlignCenter))
        self.align_right_btn.toggled.connect(lambda: self._on_alignment_changed(Qt.AlignmentFlag.AlignRight))

        # Lists
        self.bullet_btn.clicked.connect(self._on_bullet_list)
        self.number_btn.clicked.connect(self._on_number_list)

        # Text changes
        self.text_editor.textChanged.connect(self._on_text_changed)
        self.text_editor.cursorPositionChanged.connect(self._update_format_buttons)

    def _on_font_changed(self, font):
        """Handle font family change."""
        cursor = self.text_editor.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            format.setFontFamily(font.family())
            cursor.mergeCharFormat(format)
        else:
            self.text_editor.setCurrentFont(font)

    def _on_font_size_changed(self, size):
        """Handle font size change."""
        cursor = self.text_editor.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            format.setFontPointSize(size)
            cursor.mergeCharFormat(format)
        else:
            font = self.text_editor.currentFont()
            font.setPointSize(size)
            self.text_editor.setCurrentFont(font)

    def _on_bold_toggled(self, checked):
        """Handle bold toggle."""
        weight = QFont.Weight.Bold if checked else QFont.Weight.Normal
        self.text_editor.setFontWeight(weight)

    def _on_italic_toggled(self, checked):
        """Handle italic toggle."""
        self.text_editor.setFontItalic(checked)

    def _on_underline_toggled(self, checked):
        """Handle underline toggle."""
        self.text_editor.setFontUnderline(checked)

    def _on_text_color_clicked(self):
        """Handle text color change."""
        color = QColorDialog.getColor(Qt.GlobalColor.black, self)
        if color.isValid():
            self.text_editor.setTextColor(color)

    def _on_bg_color_clicked(self):
        """Handle background color change."""
        color = QColorDialog.getColor(Qt.GlobalColor.yellow, self)
        if color.isValid():
            cursor = self.text_editor.textCursor()
            format = QTextCharFormat()
            format.setBackground(color)
            cursor.mergeCharFormat(format)

    def _on_alignment_changed(self, alignment):
        """Handle text alignment change."""
        self.text_editor.setAlignment(alignment)

        # Update button states
        self.align_left_btn.setChecked(alignment == Qt.AlignmentFlag.AlignLeft)
        self.align_center_btn.setChecked(alignment == Qt.AlignmentFlag.AlignCenter)
        self.align_right_btn.setChecked(alignment == Qt.AlignmentFlag.AlignRight)

    def _on_bullet_list(self):
        """Insert bullet list."""
        cursor = self.text_editor.textCursor()
        cursor.insertList(QTextCursor.MoveOperation.BulletList)

    def _on_number_list(self):
        """Insert numbered list."""
        cursor = self.text_editor.textCursor()
        cursor.insertList(QTextCursor.MoveOperation.NumberedList)

    def _on_text_changed(self):
        """Handle text content change."""
        html_content = self.text_editor.toHtml()
        plain_content = self.text_editor.toPlainText()

        self.content_changed.emit(html_content)
        self.text_changed.emit(plain_content)

    def _update_format_buttons(self):
        """Update format button states based on current cursor position."""
        cursor = self.text_editor.textCursor()
        format = cursor.charFormat()

        # Update font info
        font = format.font()
        self.font_combo.setCurrentFont(font)
        self.font_size.setValue(int(font.pointSize()) if font.pointSize() > 0 else 10)

        # Update format buttons
        self.bold_btn.setChecked(font.bold())
        self.italic_btn.setChecked(font.italic())
        self.underline_btn.setChecked(font.underline())

        # Update alignment
        alignment = self.text_editor.alignment()
        self.align_left_btn.setChecked(alignment == Qt.AlignmentFlag.AlignLeft)
        self.align_center_btn.setChecked(alignment == Qt.AlignmentFlag.AlignCenter)
        self.align_right_btn.setChecked(alignment == Qt.AlignmentFlag.AlignRight)

    def get_html(self) -> str:
        """Get HTML content."""
        return self.text_editor.toHtml()

    def get_text(self) -> str:
        """Get plain text content."""
        return self.text_editor.toPlainText()

    def set_html(self, html: str):
        """Set HTML content."""
        self.text_editor.setHtml(html)

    def set_text(self, text: str):
        """Set plain text content."""
        self.text_editor.setPlainText(text)

    def clear(self):
        """Clear all content."""
        self.text_editor.clear()

    def set_read_only(self, read_only: bool):
        """Set read-only mode."""
        self.text_editor.setReadOnly(read_only)
        self.toolbar.setEnabled(not read_only)


class SimpleRichTextEditor(QWidget):
    """Simplified rich text editor with basic formatting."""

    content_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Setup simplified editor."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Simple toolbar
        toolbar_layout = QHBoxLayout()

        self.bold_btn = QToolButton()
        self.bold_btn.setText("B")
        self.bold_btn.setCheckable(True)
        self.bold_btn.setStyleSheet("font-weight: bold;")

        self.italic_btn = QToolButton()
        self.italic_btn.setText("I")
        self.italic_btn.setCheckable(True)
        self.italic_btn.setStyleSheet("font-style: italic;")

        self.underline_btn = QToolButton()
        self.underline_btn.setText("U")
        self.underline_btn.setCheckable(True)
        self.underline_btn.setStyleSheet("text-decoration: underline;")

        toolbar_layout.addWidget(self.bold_btn)
        toolbar_layout.addWidget(self.italic_btn)
        toolbar_layout.addWidget(self.underline_btn)
        toolbar_layout.addStretch()

        layout.addLayout(toolbar_layout)

        # Text editor
        self.text_editor = QTextEdit()
        self.text_editor.setMaximumHeight(150)
        layout.addWidget(self.text_editor)

        # Connections
        self.bold_btn.toggled.connect(lambda checked: self.text_editor.setFontWeight(
            QFont.Weight.Bold if checked else QFont.Weight.Normal))
        self.italic_btn.toggled.connect(self.text_editor.setFontItalic)
        self.underline_btn.toggled.connect(self.text_editor.setFontUnderline)
        self.text_editor.textChanged.connect(
            lambda: self.content_changed.emit(self.text_editor.toHtml()))

    def get_html(self) -> str:
        """Get HTML content."""
        return self.text_editor.toHtml()

    def set_html(self, html: str):
        """Set HTML content."""
        self.text_editor.setHtml(html)