"""
Example usage of RichTextEditorWidget.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

# Add the parent directory to the path to import the widgets
sys.path.append('..')

from forms.rich_text_editor import RichTextEditorWidget, SimpleRichTextEditor


class RichTextEditorExample(QMainWindow):
    """Example application for RichTextEditorWidget."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rich Text Editor Example")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Rich text editor
        self.editor = RichTextEditorWidget()
        self.editor.content_changed.connect(self.on_content_changed)
        layout.addWidget(self.editor)

        # Control buttons
        button_layout = QHBoxLayout()

        load_btn = QPushButton("Load Sample")
        load_btn.clicked.connect(self.load_sample_content)
        button_layout.addWidget(load_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.editor.clear)
        button_layout.addWidget(clear_btn)

        get_html_btn = QPushButton("Get HTML")
        get_html_btn.clicked.connect(self.show_html)
        button_layout.addWidget(get_html_btn)

        readonly_btn = QPushButton("Toggle Read-Only")
        readonly_btn.clicked.connect(self.toggle_readonly)
        button_layout.addWidget(readonly_btn)

        layout.addLayout(button_layout)

        # Simple editor
        layout.addWidget(QWidget())  # Spacer
        simple_label = QWidget()
        layout.addWidget(simple_label)

        self.simple_editor = SimpleRichTextEditor()
        layout.addWidget(self.simple_editor)

    def on_content_changed(self, html_content):
        """Handle content change."""
        print(f"Content changed: {len(html_content)} characters")

    def load_sample_content(self):
        """Load sample content."""
        sample_html = """
        <h1>Sample Rich Text Content</h1>
        <p>This is a <b>bold</b> paragraph with <i>italic</i> and <u>underlined</u> text.</p>
        <p style="color: red;">This text is red.</p>
        <ul>
            <li>First bullet point</li>
            <li>Second bullet point</li>
        </ul>
        <ol>
            <li>First numbered item</li>
            <li>Second numbered item</li>
        </ol>
        """
        self.editor.set_html(sample_html)

    def show_html(self):
        """Show HTML content."""
        html = self.editor.get_html()
        print("HTML Content:")
        print(html)

    def toggle_readonly(self):
        """Toggle read-only mode."""
        current_readonly = self.editor.text_editor.isReadOnly()
        self.editor.set_read_only(not current_readonly)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = RichTextEditorExample()
    window.show()

    sys.exit(app.exec())