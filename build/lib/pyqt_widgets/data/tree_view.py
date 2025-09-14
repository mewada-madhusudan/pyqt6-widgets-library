"""
Enhanced tree view widget with icons and animations.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget,
                             QTreeWidgetItem, QLabel, QPushButton, QLineEdit,
                             QCheckBox, QMenu)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon, QAction
from ..base.theme_manager import theme_manager


class TreeViewWidget(QWidget):
    """Enhanced tree view with search, icons, and animations."""

    item_clicked = pyqtSignal(QTreeWidgetItem)
    item_double_clicked = pyqtSignal(QTreeWidgetItem)
    item_expanded = pyqtSignal(QTreeWidgetItem)
    item_collapsed = pyqtSignal(QTreeWidgetItem)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._checkable = False
        self._searchable = True
        self._animated = True
        self._setup_ui()

    def _setup_ui(self):
        """Setup the tree view UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        # Search bar
        if self._searchable:
            self._create_search_bar(main_layout)

        # Tree widget
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setAlternatingRowColors(True)
        self.tree.setAnimated(self._animated)

        # Connect signals
        self.tree.itemClicked.connect(self.item_clicked.emit)
        self.tree.itemDoubleClicked.connect(self.item_double_clicked.emit)
        self.tree.itemExpanded.connect(self.item_expanded.emit)
        self.tree.itemCollapsed.connect(self.item_collapsed.emit)

        # Styling
        self.tree.setStyleSheet(f"""
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
            QTreeWidget::branch {{
                background: transparent;
            }}
            QTreeWidget::branch:has-children:closed {{
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTYgNEwxMCA4TDYgMTJWNFoiIGZpbGw9IiM2QjcyODAiLz4KPHN2Zz4K);
            }}
            QTreeWidget::branch:has-children:open {{
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQgNkw4IDEwTDEyIDZINFoiIGZpbGw9IiM2QjcyODAiLz4KPHN2Zz4K);
            }}
        """)

        main_layout.addWidget(self.tree)

        # Context menu
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)

    def _create_search_bar(self, layout):
        """Create search functionality."""
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(8)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.textChanged.connect(self._filter_items)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 6px 12px;
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                background-color: {theme_manager.get_color('surface')};
            }}
        """)
        search_layout.addWidget(self.search_input)

        # Clear button
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self._clear_search)
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                padding: 6px 12px;
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                background-color: {theme_manager.get_color('light')};
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)
        search_layout.addWidget(clear_btn)

        layout.addWidget(search_container)

    def add_item(self, text: str, parent=None, icon=None, data=None) -> QTreeWidgetItem:
        """Add item to tree."""
        if parent is None:
            item = QTreeWidgetItem(self.tree, [text])
        else:
            item = QTreeWidgetItem(parent, [text])

        # Set icon if provided
        if icon:
            item.setIcon(0, icon)

        # Store custom data
        if data:
            item.setData(0, Qt.ItemDataRole.UserRole, data)

        # Add checkbox if checkable
        if self._checkable:
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(0, Qt.CheckState.Unchecked)

        return item

    def add_folder(self, text: str, parent=None) -> QTreeWidgetItem:
        """Add folder item with folder icon."""
        folder_icon = self._get_folder_icon()
        return self.add_item(text, parent, folder_icon)

    def add_file(self, text: str, parent=None, file_type: str = "default") -> QTreeWidgetItem:
        """Add file item with file type icon."""
        file_icon = self._get_file_icon(file_type)
        return self.add_item(text, parent, file_icon)

    def _get_folder_icon(self) -> QIcon:
        """Get folder icon."""
        # In a real implementation, you'd load actual icons
        # For now, return None and use text indicators
        return None

    def _get_file_icon(self, file_type: str) -> QIcon:
        """Get file icon based on type."""
        # In a real implementation, you'd have different icons for different file types
        return None

    def _filter_items(self, search_text: str):
        """Filter tree items based on search text."""
        search_text = search_text.lower()

        def filter_recursive(item: QTreeWidgetItem):
            """Recursively filter items."""
            item_text = item.text(0).lower()
            match = search_text in item_text

            # Check children
            child_match = False
            for i in range(item.childCount()):
                child = item.child(i)
                if filter_recursive(child):
                    child_match = True

            # Show item if it matches or has matching children
            show_item = match or child_match or not search_text
            item.setHidden(not show_item)

            # Expand if has matching children
            if child_match and search_text:
                item.setExpanded(True)

            return show_item

        # Filter all top-level items
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            filter_recursive(item)

    def _clear_search(self):
        """Clear search and show all items."""
        self.search_input.clear()

    def _show_context_menu(self, position):
        """Show context menu for tree items."""
        item = self.tree.itemAt(position)
        if not item:
            return

        menu = QMenu(self)

        # Common actions
        expand_action = QAction("Expand All", self)
        expand_action.triggered.connect(lambda: self._expand_all(item))
        menu.addAction(expand_action)

        collapse_action = QAction("Collapse All", self)
        collapse_action.triggered.connect(lambda: self._collapse_all(item))
        menu.addAction(collapse_action)

        menu.addSeparator()

        # Custom actions based on item type
        if item.childCount() > 0:  # Folder
            add_folder_action = QAction("Add Folder", self)
            add_folder_action.triggered.connect(lambda: self._add_new_folder(item))
            menu.addAction(add_folder_action)

            add_file_action = QAction("Add File", self)
            add_file_action.triggered.connect(lambda: self._add_new_file(item))
            menu.addAction(add_file_action)
        else:  # File
            rename_action = QAction("Rename", self)
            rename_action.triggered.connect(lambda: self._rename_item(item))
            menu.addAction(rename_action)

        menu.addSeparator()

        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self._delete_item(item))
        menu.addAction(delete_action)

        menu.exec(self.tree.mapToGlobal(position))

    def _expand_all(self, item: QTreeWidgetItem):
        """Expand item and all children."""
        item.setExpanded(True)
        for i in range(item.childCount()):
            self._expand_all(item.child(i))

    def _collapse_all(self, item: QTreeWidgetItem):
        """Collapse item and all children."""
        item.setExpanded(False)
        for i in range(item.childCount()):
            self._collapse_all(item.child(i))

    def _add_new_folder(self, parent: QTreeWidgetItem):
        """Add new folder to parent."""
        folder_name = f"New Folder {parent.childCount() + 1}"
        self.add_folder(folder_name, parent)
        parent.setExpanded(True)

    def _add_new_file(self, parent: QTreeWidgetItem):
        """Add new file to parent."""
        file_name = f"New File {parent.childCount() + 1}.txt"
        self.add_file(file_name, parent, "text")
        parent.setExpanded(True)

    def _rename_item(self, item: QTreeWidgetItem):
        """Rename tree item."""
        # In a real implementation, you'd show an inline editor
        pass

    def _delete_item(self, item: QTreeWidgetItem):
        """Delete tree item."""
        parent = item.parent()
        if parent:
            parent.removeChild(item)
        else:
            index = self.tree.indexOfTopLevelItem(item)
            self.tree.takeTopLevelItem(index)

    def set_checkable(self, checkable: bool):
        """Enable/disable checkboxes for items."""
        self._checkable = checkable

    def get_checked_items(self) -> list:
        """Get list of checked items."""
        checked_items = []

        def collect_checked(item: QTreeWidgetItem):
            if item.checkState(0) == Qt.CheckState.Checked:
                checked_items.append(item)
            for i in range(item.childCount()):
                collect_checked(item.child(i))

        for i in range(self.tree.topLevelItemCount()):
            collect_checked(self.tree.topLevelItem(i))

        return checked_items

    def clear_tree(self):
        """Clear all items from tree."""
        self.tree.clear()

    def expand_all(self):
        """Expand all items."""
        self.tree.expandAll()

    def collapse_all(self):
        """Collapse all items."""
        self.tree.collapseAll()


class FileTreeView(TreeViewWidget):
    """Tree view specifically for file system navigation."""

    def __init__(self, root_path: str = "", parent=None):
        super().__init__(parent)
        self._root_path = root_path
        if root_path:
            self._load_file_system()

    def _load_file_system(self):
        """Load file system structure."""
        import os

        if not os.path.exists(self._root_path):
            return

        def add_path(path: str, parent_item=None):
            """Recursively add paths to tree."""
            try:
                items = os.listdir(path)
                items.sort()

                for item_name in items:
                    item_path = os.path.join(path, item_name)

                    if os.path.isdir(item_path):
                        folder_item = self.add_folder(item_name, parent_item)
                        folder_item.setData(0, Qt.ItemDataRole.UserRole, item_path)
                        # Lazy load - add placeholder
                        placeholder = QTreeWidgetItem(folder_item, ["Loading..."])

                    else:
                        file_ext = os.path.splitext(item_name)[1].lower()
                        file_type = self._get_file_type(file_ext)
                        file_item = self.add_file(item_name, parent_item, file_type)
                        file_item.setData(0, Qt.ItemDataRole.UserRole, item_path)

            except PermissionError:
                pass  # Skip directories we can't access

        # Add root
        root_name = os.path.basename(self._root_path) or self._root_path
        root_item = self.add_folder(root_name)
        root_item.setData(0, Qt.ItemDataRole.UserRole, self._root_path)
        add_path(self._root_path, root_item)
        root_item.setExpanded(True)

    def _get_file_type(self, extension: str) -> str:
        """Determine file type from extension."""
        type_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.html': 'html',
            '.css': 'css',
            '.txt': 'text',
            '.md': 'markdown',
            '.json': 'json',
            '.xml': 'xml',
            '.png': 'image',
            '.jpg': 'image',
            '.jpeg': 'image',
            '.gif': 'image',
            '.pdf': 'pdf',
            '.doc': 'document',
            '.docx': 'document'
        }
        return type_map.get(extension, 'default')


class CheckableTreeView(TreeViewWidget):
    """Tree view with checkbox functionality."""

    items_checked = pyqtSignal(list)  # Emits list of checked items

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_checkable(True)
        self.tree.itemChanged.connect(self._on_item_changed)

    def _on_item_changed(self, item: QTreeWidgetItem, column: int):
        """Handle item check state change."""
        if column == 0:  # Only handle first column
            self._update_children_check_state(item)
            self._update_parent_check_state(item)
            self.items_checked.emit(self.get_checked_items())

    def _update_children_check_state(self, item: QTreeWidgetItem):
        """Update children to match parent check state."""
        check_state = item.checkState(0)
        for i in range(item.childCount()):
            child = item.child(i)
            child.setCheckState(0, check_state)
            self._update_children_check_state(child)

    def _update_parent_check_state(self, item: QTreeWidgetItem):
        """Update parent check state based on children."""
        parent = item.parent()
        if not parent:
            return

        # Count checked children
        checked_count = 0
        total_count = parent.childCount()

        for i in range(total_count):
            child = parent.child(i)
            if child.checkState(0) == Qt.CheckState.Checked:
                checked_count += 1

        # Set parent state
        if checked_count == 0:
            parent.setCheckState(0, Qt.CheckState.Unchecked)
        elif checked_count == total_count:
            parent.setCheckState(0, Qt.CheckState.Checked)
        else:
            parent.setCheckState(0, Qt.CheckState.PartiallyChecked)

        # Recursively update grandparent
        self._update_parent_check_state(parent)