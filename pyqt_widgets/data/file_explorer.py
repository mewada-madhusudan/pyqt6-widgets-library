"""
File explorer widget with styled folder/file tree and context menu support.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget,
                             QTreeWidgetItem, QLabel, QPushButton, QLineEdit,
                             QSplitter, QListWidget, QListWidgetItem, QMenu,
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QFileInfo, QDir, QFileSystemWatcher
from PyQt6.QtGui import QFont, QIcon, QAction, QPixmap
from ..base.theme_manager import theme_manager
import os


class FileExplorerWidget(QWidget):
    """File explorer with tree view and optional list view."""

    file_selected = pyqtSignal(str)  # Emits selected file path
    file_double_clicked = pyqtSignal(str)  # Emits double-clicked file path
    folder_changed = pyqtSignal(str)  # Emits current folder path

    def __init__(self, root_path: str = "", show_list_view: bool = True, parent=None):
        super().__init__(parent)
        self._root_path = root_path or os.path.expanduser("~")
        self._show_list_view = show_list_view
        self._current_path = self._root_path
        self._file_watcher = QFileSystemWatcher()
        self._file_watcher.directoryChanged.connect(self._on_directory_changed)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the file explorer UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        # Toolbar
        self._create_toolbar(main_layout)

        # Content area
        if self._show_list_view:
            # Splitter with tree and list
            splitter = QSplitter(Qt.Orientation.Horizontal)

            # Tree view (folders only)
            self.tree_widget = self._create_tree_view()
            splitter.addWidget(self.tree_widget)

            # List view (files in current folder)
            self.list_widget = self._create_list_view()
            splitter.addWidget(self.list_widget)

            # Set splitter proportions
            splitter.setSizes([200, 400])
            main_layout.addWidget(splitter)
        else:
            # Tree view only (folders and files)
            self.tree_widget = self._create_tree_view(show_files=True)
            main_layout.addWidget(self.tree_widget)

        # Load initial content
        self._load_root_directory()

    def _create_toolbar(self, layout):
        """Create toolbar with navigation and actions."""
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(8, 4, 8, 4)
        toolbar_layout.setSpacing(8)

        # Back button
        self.back_btn = QPushButton("←")
        self.back_btn.setFixedSize(32, 32)
        self.back_btn.setToolTip("Go back")
        self.back_btn.clicked.connect(self._go_back)
        toolbar_layout.addWidget(self.back_btn)

        # Forward button
        self.forward_btn = QPushButton("→")
        self.forward_btn.setFixedSize(32, 32)
        self.forward_btn.setToolTip("Go forward")
        self.forward_btn.clicked.connect(self._go_forward)
        toolbar_layout.addWidget(self.forward_btn)

        # Up button
        self.up_btn = QPushButton("↑")
        self.up_btn.setFixedSize(32, 32)
        self.up_btn.setToolTip("Go up")
        self.up_btn.clicked.connect(self._go_up)
        toolbar_layout.addWidget(self.up_btn)

        # Path display
        self.path_label = QLabel(self._current_path)
        self.path_label.setStyleSheet(f"""
            QLabel {{
                padding: 6px 12px;
                background-color: {theme_manager.get_color('light')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
            }}
        """)
        toolbar_layout.addWidget(self.path_label)

        # Refresh button
        refresh_btn = QPushButton("⟳")
        refresh_btn.setFixedSize(32, 32)
        refresh_btn.setToolTip("Refresh")
        refresh_btn.clicked.connect(self._refresh)
        toolbar_layout.addWidget(refresh_btn)

        layout.addWidget(toolbar)

    def _create_tree_view(self, show_files: bool = False) -> QTreeWidget:
        """Create tree view for folders (and optionally files)."""
        tree = QTreeWidget()
        tree.setHeaderHidden(True)
        tree.setAlternatingRowColors(True)

        # Connect signals
        tree.itemClicked.connect(self._on_tree_item_clicked)
        tree.itemDoubleClicked.connect(self._on_tree_item_double_clicked)
        tree.itemExpanded.connect(self._on_tree_item_expanded)

        # Context menu
        tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        tree.customContextMenuRequested.connect(self._show_tree_context_menu)

        # Styling
        tree.setStyleSheet(f"""
            QTreeWidget {{
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
                background-color: {theme_manager.get_color('surface')};
                alternate-background-color: {theme_manager.get_color('hover')};
            }}
            QTreeWidget::item {{
                padding: 4px;
                border-bottom: 1px solid transparent;
            }}
            QTreeWidget::item:selected {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
            }}
            QTreeWidget::item:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)

        return tree

    def _create_list_view(self) -> QListWidget:
        """Create list view for files in current directory."""
        list_widget = QListWidget()
        list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        list_widget.setGridSize(list_widget.gridSize())

        # Connect signals
        list_widget.itemClicked.connect(self._on_list_item_clicked)
        list_widget.itemDoubleClicked.connect(self._on_list_item_double_clicked)

        # Context menu
        list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        list_widget.customContextMenuRequested.connect(self._show_list_context_menu)

        # Styling
        list_widget.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
                background-color: {theme_manager.get_color('surface')};
            }}
            QListWidget::item {{
                padding: 8px;
                border-radius: {theme_manager.get_border_radius('sm')}px;
                margin: 2px;
            }}
            QListWidget::item:selected {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
            }}
            QListWidget::item:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)

        return list_widget

    def _load_root_directory(self):
        """Load root directory structure."""
        if not os.path.exists(self._root_path):
            return

        # Add root item
        root_item = QTreeWidgetItem(self.tree_widget)
        root_item.setText(0, os.path.basename(self._root_path) or self._root_path)
        root_item.setData(0, Qt.ItemDataRole.UserRole, self._root_path)

        # Add folder icon
        root_item.setIcon(0, self._get_folder_icon())

        # Load subdirectories
        self._load_directory_children(root_item, self._root_path)
        root_item.setExpanded(True)

        # Update list view if enabled
        if self._show_list_view:
            self._update_list_view(self._root_path)

        # Watch root directory
        self._file_watcher.addPath(self._root_path)

    def _load_directory_children(self, parent_item: QTreeWidgetItem, dir_path: str):
        """Load children of a directory."""
        try:
            entries = os.listdir(dir_path)
            entries.sort()

            for entry_name in entries:
                entry_path = os.path.join(dir_path, entry_name)

                if os.path.isdir(entry_path):
                    # Add folder
                    folder_item = QTreeWidgetItem(parent_item)
                    folder_item.setText(0, entry_name)
                    folder_item.setData(0, Qt.ItemDataRole.UserRole, entry_path)
                    folder_item.setIcon(0, self._get_folder_icon())

                    # Add placeholder for lazy loading
                    if self._has_subdirectories(entry_path):
                        placeholder = QTreeWidgetItem(folder_item)
                        placeholder.setText(0, "Loading...")

                elif not self._show_list_view:
                    # Add file (only if not using list view)
                    file_item = QTreeWidgetItem(parent_item)
                    file_item.setText(0, entry_name)
                    file_item.setData(0, Qt.ItemDataRole.UserRole, entry_path)
                    file_item.setIcon(0, self._get_file_icon(entry_name))

        except PermissionError:
            # Add "Access Denied" item
            denied_item = QTreeWidgetItem(parent_item)
            denied_item.setText(0, "Access Denied")
            denied_item.setDisabled(True)

    def _has_subdirectories(self, dir_path: str) -> bool:
        """Check if directory has subdirectories."""
        try:
            for entry in os.listdir(dir_path):
                entry_path = os.path.join(dir_path, entry)
                if os.path.isdir(entry_path):
                    return True
        except PermissionError:
            pass
        return False

    def _update_list_view(self, dir_path: str):
        """Update list view with files from directory."""
        if not hasattr(self, 'list_widget'):
            return

        self.list_widget.clear()

        try:
            entries = os.listdir(dir_path)
            entries.sort()

            for entry_name in entries:
                entry_path = os.path.join(dir_path, entry_name)

                if os.path.isfile(entry_path):
                    item = QListWidgetItem()
                    item.setText(entry_name)
                    item.setData(Qt.ItemDataRole.UserRole, entry_path)
                    item.setIcon(self._get_file_icon(entry_name))
                    self.list_widget.addItem(item)

        except PermissionError:
            pass

    def _get_folder_icon(self) -> QIcon:
        """Get folder icon."""
        # In a real implementation, you'd load actual icons
        return QIcon()  # Placeholder

    def _get_file_icon(self, filename: str) -> QIcon:
        """Get file icon based on extension."""
        # In a real implementation, you'd have different icons for different file types
        return QIcon()  # Placeholder

    def _on_tree_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle tree item click."""
        path = item.data(0, Qt.ItemDataRole.UserRole)
        if path and os.path.isdir(path):
            self._current_path = path
            self.path_label.setText(path)

            if self._show_list_view:
                self._update_list_view(path)

            self.folder_changed.emit(path)

    def _on_tree_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle tree item double click."""
        path = item.data(0, Qt.ItemDataRole.UserRole)
        if path:
            if os.path.isfile(path):
                self.file_double_clicked.emit(path)

    def _on_tree_item_expanded(self, item: QTreeWidgetItem):
        """Handle tree item expansion (lazy loading)."""
        # Remove placeholder and load actual children
        if item.childCount() == 1:
            child = item.child(0)
            if child.text(0) == "Loading...":
                item.removeChild(child)

                path = item.data(0, Qt.ItemDataRole.UserRole)
                if path:
                    self._load_directory_children(item, path)

    def _on_list_item_clicked(self, item: QListWidgetItem):
        """Handle list item click."""
        path = item.data(Qt.ItemDataRole.UserRole)
        if path:
            self.file_selected.emit(path)

    def _on_list_item_double_clicked(self, item: QListWidgetItem):
        """Handle list item double click."""
        path = item.data(Qt.ItemDataRole.UserRole)
        if path:
            self.file_double_clicked.emit(path)

    def _show_tree_context_menu(self, position):
        """Show context menu for tree items."""
        item = self.tree_widget.itemAt(position)
        if not item:
            return

        path = item.data(0, Qt.ItemDataRole.UserRole)
        if not path:
            return

        menu = QMenu(self)

        if os.path.isdir(path):
            # Folder actions
            open_action = QAction("Open in File Manager", self)
            open_action.triggered.connect(lambda: self._open_in_file_manager(path))
            menu.addAction(open_action)

            menu.addSeparator()

            new_folder_action = QAction("New Folder", self)
            new_folder_action.triggered.connect(lambda: self._create_new_folder(path))
            menu.addAction(new_folder_action)

        else:
            # File actions
            open_action = QAction("Open", self)
            open_action.triggered.connect(lambda: self.file_double_clicked.emit(path))
            menu.addAction(open_action)

        menu.addSeparator()

        # Common actions
        copy_path_action = QAction("Copy Path", self)
        copy_path_action.triggered.connect(lambda: self._copy_path_to_clipboard(path))
        menu.addAction(copy_path_action)

        properties_action = QAction("Properties", self)
        properties_action.triggered.connect(lambda: self._show_properties(path))
        menu.addAction(properties_action)

        menu.exec(self.tree_widget.mapToGlobal(position))

    def _show_list_context_menu(self, position):
        """Show context menu for list items."""
        item = self.list_widget.itemAt(position)
        if not item:
            return

        path = item.data(Qt.ItemDataRole.UserRole)
        if not path:
            return

        menu = QMenu(self)

        # File actions
        open_action = QAction("Open", self)
        open_action.triggered.connect(lambda: self.file_double_clicked.emit(path))
        menu.addAction(open_action)

        menu.addSeparator()

        copy_path_action = QAction("Copy Path", self)
        copy_path_action.triggered.connect(lambda: self._copy_path_to_clipboard(path))
        menu.addAction(copy_path_action)

        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self._delete_file(path))
        menu.addAction(delete_action)

        menu.exec(self.list_widget.mapToGlobal(position))

    def _go_back(self):
        """Navigate back in history."""
        # Implementation would maintain navigation history
        pass

    def _go_forward(self):
        """Navigate forward in history."""
        # Implementation would maintain navigation history
        pass

    def _go_up(self):
        """Navigate to parent directory."""
        parent_path = os.path.dirname(self._current_path)
        if parent_path != self._current_path:
            self.navigate_to(parent_path)

    def _refresh(self):
        """Refresh current view."""
        self.tree_widget.clear()
        self._load_root_directory()

    def _open_in_file_manager(self, path: str):
        """Open path in system file manager."""
        import subprocess
        import platform

        system = platform.system()
        try:
            if system == "Windows":
                subprocess.run(["explorer", path])
            elif system == "Darwin":  # macOS
                subprocess.run(["open", path])
            else:  # Linux
                subprocess.run(["xdg-open", path])
        except Exception:
            pass

    def _create_new_folder(self, parent_path: str):
        """Create new folder in parent directory."""
        folder_name = "New Folder"
        folder_path = os.path.join(parent_path, folder_name)

        counter = 1
        while os.path.exists(folder_path):
            folder_name = f"New Folder ({counter})"
            folder_path = os.path.join(parent_path, folder_name)
            counter += 1

        try:
            os.makedirs(folder_path)
            self._refresh()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not create folder: {e}")

    def _copy_path_to_clipboard(self, path: str):
        """Copy path to clipboard."""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(path)

    def _show_properties(self, path: str):
        """Show file/folder properties."""
        # Implementation would show a properties dialog
        pass

    def _delete_file(self, path: str):
        """Delete file with confirmation."""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete:\n{os.path.basename(path)}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(path)
                self._refresh()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not delete file: {e}")

    def _on_directory_changed(self, path: str):
        """Handle directory change notification."""
        if path == self._current_path and self._show_list_view:
            self._update_list_view(path)

    def navigate_to(self, path: str):
        """Navigate to specific path."""
        if os.path.exists(path):
            self._current_path = path
            self.path_label.setText(path)

            if self._show_list_view:
                self._update_list_view(path)

            self.folder_changed.emit(path)

    def get_current_path(self) -> str:
        """Get current directory path."""
        return self._current_path

    def get_selected_file(self) -> str:
        """Get currently selected file path."""
        if hasattr(self, 'list_widget'):
            current_item = self.list_widget.currentItem()
            if current_item:
                return current_item.data(Qt.ItemDataRole.UserRole)
        return ""