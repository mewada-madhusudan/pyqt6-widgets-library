"""
Dockable panel widget with detaching and floating behavior.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QApplication)
from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QRect
from PyQt6.QtGui import QFont, QIcon, QMouseEvent, QDragEnterEvent, QDropEvent
from ..base.theme_manager import theme_manager
from ..base.base_button import BaseButton


class DockablePanelWidget(QWidget):
    """Detachable, draggable panel widget."""

    panel_detached = pyqtSignal()
    panel_attached = pyqtSignal()
    panel_closed = pyqtSignal()

    def __init__(self, title="Panel", closeable=True, detachable=True, parent=None):
        super().__init__(parent)
        self._title = title
        self._closeable = closeable
        self._detachable = detachable
        self._is_floating = False
        self._drag_start_position = None
        self._original_parent = parent
        self._setup_ui()

    def _setup_ui(self):
        """Setup the dockable panel UI."""
        self.setStyleSheet(f"""
            DockablePanelWidget {{
                background-color: {theme_manager.get_color('surface')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}
        """)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Title bar
        self.title_bar = QWidget()
        self.title_bar.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_manager.get_color('light')};
                border-bottom: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px {theme_manager.get_border_radius('md')}px 0px 0px;
            }}
        """)

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(12, 8, 8, 8)
        title_layout.setSpacing(8)

        # Title label
        self.title_label = QLabel(self._title)
        title_font = theme_manager.get_font('default')
        title_font.setWeight(QFont.Weight.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        title_layout.addWidget(self.title_label)

        title_layout.addStretch()

        # Control buttons
        if self._detachable:
            self.detach_btn = QPushButton("⧉")
            self.detach_btn.setFixedSize(20, 20)
            self.detach_btn.setFlat(True)
            self.detach_btn.setToolTip("Detach panel")
            self.detach_btn.clicked.connect(self._toggle_detach)
            self.detach_btn.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background-color: transparent;
                    color: {theme_manager.get_color('text_secondary')};
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {theme_manager.get_color('hover')};
                    color: {theme_manager.get_color('text')};
                }}
            """)
            title_layout.addWidget(self.detach_btn)

        if self._closeable:
            self.close_btn = QPushButton("×")
            self.close_btn.setFixedSize(20, 20)
            self.close_btn.setFlat(True)
            self.close_btn.setToolTip("Close panel")
            self.close_btn.clicked.connect(self._close_panel)
            self.close_btn.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background-color: transparent;
                    color: {theme_manager.get_color('text_secondary')};
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {theme_manager.get_color('danger')};
                    color: white;
                }}
            """)
            title_layout.addWidget(self.close_btn)

        main_layout.addWidget(self.title_bar)

        # Content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.addWidget(self.content_area)

        # Enable dragging on title bar
        self.title_bar.mousePressEvent = self._title_mouse_press
        self.title_bar.mouseMoveEvent = self._title_mouse_move
        self.title_bar.mouseReleaseEvent = self._title_mouse_release

    def _title_mouse_press(self, event: QMouseEvent):
        """Handle title bar mouse press for dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_position = event.globalPosition().toPoint()

    def _title_mouse_move(self, event: QMouseEvent):
        """Handle title bar mouse move for dragging."""
        if (event.buttons() == Qt.MouseButton.LeftButton and
                self._drag_start_position is not None):

            # Calculate drag distance
            drag_distance = (event.globalPosition().toPoint() - self._drag_start_position).manhattanLength()

            if drag_distance > QApplication.startDragDistance():
                if not self._is_floating and self._detachable:
                    # Auto-detach when dragging
                    self._detach_panel()

                if self._is_floating:
                    # Move floating window
                    new_pos = event.globalPosition().toPoint() - self._drag_start_position
                    self.move(self.pos() + new_pos)
                    self._drag_start_position = event.globalPosition().toPoint()

    def _title_mouse_release(self, event: QMouseEvent):
        """Handle title bar mouse release."""
        self._drag_start_position = None

        # Check for snap-back to dock
        if self._is_floating and self._original_parent:
            parent_rect = self._original_parent.geometry()
            panel_rect = self.geometry()

            # If panel is near original position, snap back
            if (abs(panel_rect.x() - parent_rect.x()) < 50 and
                    abs(panel_rect.y() - parent_rect.y()) < 50):
                self._attach_panel()

    def _toggle_detach(self):
        """Toggle panel detach state."""
        if self._is_floating:
            self._attach_panel()
        else:
            self._detach_panel()

    def _detach_panel(self):
        """Detach panel to floating window."""
        if self._is_floating:
            return

        # Store original parent and position
        self._original_parent = self.parent()
        self._original_geometry = self.geometry()

        # Convert to floating window
        self.setParent(None)
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)

        # Position near cursor
        cursor_pos = QApplication.instance().primaryScreen().availableGeometry().center()
        self.move(cursor_pos.x() - self.width() // 2, cursor_pos.y() - self.height() // 2)

        # Update styling for floating state
        self.setStyleSheet(f"""
            DockablePanelWidget {{
                background-color: {theme_manager.get_color('surface')};
                border: 2px solid {theme_manager.get_color('primary')};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}
        """)

        # Update detach button
        if hasattr(self, 'detach_btn'):
            self.detach_btn.setText("⧈")
            self.detach_btn.setToolTip("Attach panel")

        self._is_floating = True
        self.show()
        self.panel_detached.emit()

    def _attach_panel(self):
        """Attach panel back to original parent."""
        if not self._is_floating or not self._original_parent:
            return

        # Hide floating window
        self.hide()

        # Restore to original parent
        self.setParent(self._original_parent)
        self.setWindowFlags(Qt.WindowType.Widget)

        # Restore original styling
        self.setStyleSheet(f"""
            DockablePanelWidget {{
                background-color: {theme_manager.get_color('surface')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}
        """)

        # Update detach button
        if hasattr(self, 'detach_btn'):
            self.detach_btn.setText("⧉")
            self.detach_btn.setToolTip("Detach panel")

        self._is_floating = False
        self.show()
        self.panel_attached.emit()

    def _close_panel(self):
        """Close the panel."""
        self.panel_closed.emit()
        self.close()

    def set_content(self, widget: QWidget):
        """Set the panel content."""
        # Clear existing content
        for i in reversed(range(self.content_layout.count())):
            item = self.content_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        self.content_layout.addWidget(widget)

    def add_content_widget(self, widget: QWidget):
        """Add widget to content area."""
        self.content_layout.addWidget(widget)

    def set_title(self, title: str):
        """Update panel title."""
        self._title = title
        self.title_label.setText(title)

    def get_title(self) -> str:
        """Get panel title."""
        return self._title

    def is_floating(self) -> bool:
        """Check if panel is floating."""
        return self._is_floating

    def set_closeable(self, closeable: bool):
        """Set whether panel can be closed."""
        self._closeable = closeable
        if hasattr(self, 'close_btn'):
            self.close_btn.setVisible(closeable)

    def set_detachable(self, detachable: bool):
        """Set whether panel can be detached."""
        self._detachable = detachable
        if hasattr(self, 'detach_btn'):
            self.detach_btn.setVisible(detachable)


class DockingArea(QWidget):
    """Area that can accept docked panels."""

    panel_docked = pyqtSignal(DockablePanelWidget)
    panel_undocked = pyqtSignal(DockablePanelWidget)

    def __init__(self, orientation=Qt.Orientation.Vertical, parent=None):
        super().__init__(parent)
        self._orientation = orientation
        self._panels = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup docking area UI."""
        self.setAcceptDrops(True)
        self.setStyleSheet(f"""
            DockingArea {{
                background-color: {theme_manager.get_color('background')};
                border: 2px dashed {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
            }}
        """)

        if self._orientation == Qt.Orientation.Vertical:
            self.layout = QVBoxLayout(self)
        else:
            self.layout = QHBoxLayout(self)

        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(8)

    def add_panel(self, panel: DockablePanelWidget):
        """Add panel to docking area."""
        if panel not in self._panels:
            self._panels.append(panel)
            self.layout.addWidget(panel)
            panel.panel_closed.connect(lambda: self._remove_panel(panel))
            self.panel_docked.emit(panel)

    def _remove_panel(self, panel: DockablePanelWidget):
        """Remove panel from docking area."""
        if panel in self._panels:
            self._panels.remove(panel)
            self.panel_undocked.emit(panel)

    def remove_panel(self, panel: DockablePanelWidget):
        """Remove panel programmatically."""
        if panel in self._panels:
            panel.setParent(None)
            self._remove_panel(panel)

    def get_panels(self) -> list:
        """Get list of docked panels."""
        return self._panels.copy()

    def clear_panels(self):
        """Remove all panels."""
        for panel in self._panels.copy():
            self.remove_panel(panel)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter for panel docking."""
        # Accept drag if it's a dockable panel
        if event.mimeData().hasFormat("application/x-dockable-panel"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """Handle drop for panel docking."""
        # Handle panel docking
        if event.mimeData().hasFormat("application/x-dockable-panel"):
            # Get panel from drag data (would need custom implementation)
            event.acceptProposedAction()


class TabbedDockingArea(DockingArea):
    """Docking area that organizes panels in tabs."""

    def __init__(self, parent=None):
        super().__init__(Qt.Orientation.Vertical, parent)
        self._setup_tabbed_ui()

    def _setup_tabbed_ui(self):
        """Setup tabbed docking area."""
        from .tab_bar import TabbedContainer

        # Replace layout with tabbed container
        self.layout.setParent(None)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.tabbed_container = TabbedContainer()
        main_layout.addWidget(self.tabbed_container)

    def add_panel(self, panel: DockablePanelWidget):
        """Add panel as new tab."""
        if panel not in self._panels:
            self._panels.append(panel)

            # Create content widget for the panel
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.addWidget(panel)

            # Add as tab
            self.tabbed_container.add_tab(panel.get_title(), content_widget)

            panel.panel_closed.connect(lambda: self._remove_panel(panel))
            self.panel_docked.emit(panel)


class SplitterDockingArea(DockingArea):
    """Docking area with splitter for resizable panels."""

    def __init__(self, orientation=Qt.Orientation.Vertical, parent=None):
        super().__init__(orientation, parent)
        self._setup_splitter_ui()

    def _setup_splitter_ui(self):
        """Setup splitter docking area."""
        from PyQt6.QtWidgets import QSplitter

        # Replace layout with splitter
        self.layout.setParent(None)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.splitter = QSplitter(self._orientation)
        main_layout.addWidget(self.splitter)

    def add_panel(self, panel: DockablePanelWidget):
        """Add panel to splitter."""
        if panel not in self._panels:
            self._panels.append(panel)
            self.splitter.addWidget(panel)
            panel.panel_closed.connect(lambda: self._remove_panel(panel))
            self.panel_docked.emit(panel)

    def set_panel_sizes(self, sizes: list):
        """Set relative sizes of panels."""
        self.splitter.setSizes(sizes)

    def get_panel_sizes(self) -> list:
        """Get current panel sizes."""
        return self.splitter.sizes()