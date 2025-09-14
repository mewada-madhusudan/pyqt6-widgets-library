"""
Enhanced data table widget with sorting, filtering, and pagination.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView, QLineEdit, QPushButton,
                             QComboBox, QLabel, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal, QSortFilterProxyModel, QAbstractTableModel
from PyQt6.QtGui import QFont, QIcon
from ..base.theme_manager import theme_manager
from ..base.base_button import BaseButton


class DataTableWidget(QWidget):
    """Enhanced table widget with filtering, sorting, and selection."""

    row_selected = pyqtSignal(int)  # Emits selected row index
    row_double_clicked = pyqtSignal(int, dict)  # Emits row index and data
    data_changed = pyqtSignal()

    def __init__(self, columns=None, data=None, parent=None):
        super().__init__(parent)
        self._columns = columns or []
        self._data = data or []
        self._filtered_data = []
        self._sortable = True
        self._filterable = True
        self._selectable = True
        self._checkable = False
        self._setup_ui()

    def _setup_ui(self):
        """Setup the data table UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        # Toolbar
        if self._filterable:
            self._create_toolbar(main_layout)

        # Table widget
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)

        # Connect signals
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.itemDoubleClicked.connect(self._on_double_click)

        # Apply styling
        self.table.setStyleSheet(f"""
            QTableWidget {{
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
                background-color: {theme_manager.get_color('surface')};
                gridline-color: {theme_manager.get_color('border')};
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {theme_manager.get_color('border')};
            }}
            QTableWidget::item:selected {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {theme_manager.get_color('light')};
                padding: 8px;
                border: none;
                border-bottom: 2px solid {theme_manager.get_color('border')};
                font-weight: bold;
            }}
        """)

        main_layout.addWidget(self.table)

        # Load initial data
        self._load_data()

    def _create_toolbar(self, layout):
        """Create toolbar with search and filters."""
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(12)

        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.textChanged.connect(self._filter_data)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 6px 12px;
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                background-color: {theme_manager.get_color('surface')};
            }}
        """)
        toolbar_layout.addWidget(self.search_input)

        # Column filter
        self.column_filter = QComboBox()
        self.column_filter.addItem("All Columns")
        self.column_filter.addItems(self._columns)
        self.column_filter.currentTextChanged.connect(self._filter_data)
        toolbar_layout.addWidget(self.column_filter)

        # Clear filters button
        clear_btn = BaseButton("Clear", "ghost", "small")
        clear_btn.clicked.connect(self._clear_filters)
        toolbar_layout.addWidget(clear_btn)

        toolbar_layout.addStretch()

        # Export button
        export_btn = BaseButton("Export", "secondary", "small")
        export_btn.clicked.connect(self._export_data)
        toolbar_layout.addWidget(export_btn)

        layout.addWidget(toolbar)

    def _load_data(self):
        """Load data into table."""
        if not self._columns or not self._data:
            return

        # Set up table structure
        self.table.setRowCount(len(self._data))
        self.table.setColumnCount(len(self._columns))
        self.table.setHorizontalHeaderLabels(self._columns)

        # Add checkboxes if checkable
        if self._checkable:
            self.table.insertColumn(0)
            self.table.setHorizontalHeaderItem(0, QTableWidgetItem(""))

        # Populate data
        for row_idx, row_data in enumerate(self._data):
            col_offset = 1 if self._checkable else 0

            # Add checkbox
            if self._checkable:
                checkbox = QCheckBox()
                self.table.setCellWidget(row_idx, 0, checkbox)

            # Add data cells
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row_idx, col_idx + col_offset, item)

        # Auto-resize columns
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Enable sorting
        if self._sortable:
            self.table.setSortingEnabled(True)

    def _filter_data(self):
        """Filter table data based on search and column filter."""
        search_text = self.search_input.text().lower()
        column_filter = self.column_filter.currentText()

        for row in range(self.table.rowCount()):
            show_row = False

            if not search_text:
                show_row = True
            else:
                # Search in specified column or all columns
                if column_filter == "All Columns":
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        if item and search_text in item.text().lower():
                            show_row = True
                            break
                else:
                    col_idx = self._columns.index(column_filter)
                    col_idx += 1 if self._checkable else 0
                    item = self.table.item(row, col_idx)
                    if item and search_text in item.text().lower():
                        show_row = True

            self.table.setRowHidden(row, not show_row)

    def _clear_filters(self):
        """Clear all filters."""
        self.search_input.clear()
        self.column_filter.setCurrentIndex(0)

    def _export_data(self):
        """Export table data to CSV."""
        from PyQt6.QtWidgets import QFileDialog
        import csv

        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Data", "", "CSV Files (*.csv)"
        )

        if filename:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Write headers
                headers = []
                for col in range(self.table.columnCount()):
                    header_item = self.table.horizontalHeaderItem(col)
                    if header_item:
                        headers.append(header_item.text())
                writer.writerow(headers)

                # Write data
                for row in range(self.table.rowCount()):
                    if not self.table.isRowHidden(row):
                        row_data = []
                        for col in range(self.table.columnCount()):
                            item = self.table.item(row, col)
                            if item:
                                row_data.append(item.text())
                            else:
                                row_data.append("")
                        writer.writerow(row_data)

    def _on_selection_changed(self):
        """Handle row selection."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.row_selected.emit(current_row)

    def _on_double_click(self, item):
        """Handle double click on row."""
        row = item.row()
        row_data = {}

        col_offset = 1 if self._checkable else 0
        for col_idx, column_name in enumerate(self._columns):
            table_item = self.table.item(row, col_idx + col_offset)
            if table_item:
                row_data[column_name] = table_item.text()

        self.row_double_clicked.emit(row, row_data)

    def set_data(self, columns: list, data: list):
        """Set table data."""
        self._columns = columns
        self._data = data
        self._load_data()

    def add_row(self, row_data: list):
        """Add new row to table."""
        self._data.append(row_data)
        self._load_data()
        self.data_changed.emit()

    def remove_row(self, row_index: int):
        """Remove row from table."""
        if 0 <= row_index < len(self._data):
            del self._data[row_index]
            self._load_data()
            self.data_changed.emit()

    def get_selected_rows(self) -> list:
        """Get indices of selected rows."""
        selected_rows = []
        if self._checkable:
            for row in range(self.table.rowCount()):
                checkbox = self.table.cellWidget(row, 0)
                if checkbox and checkbox.isChecked():
                    selected_rows.append(row)
        else:
            current_row = self.table.currentRow()
            if current_row >= 0:
                selected_rows.append(current_row)

        return selected_rows

    def get_row_data(self, row_index: int) -> dict:
        """Get data for specific row."""
        if 0 <= row_index < len(self._data):
            return dict(zip(self._columns, self._data[row_index]))
        return {}

    def set_checkable(self, checkable: bool):
        """Enable/disable row checkboxes."""
        self._checkable = checkable
        self._load_data()

    def set_sortable(self, sortable: bool):
        """Enable/disable column sorting."""
        self._sortable = sortable
        self.table.setSortingEnabled(sortable)

    def set_filterable(self, filterable: bool):
        """Enable/disable filtering toolbar."""
        self._filterable = filterable
        # Would need to recreate UI to add/remove toolbar


class EditableDataTable(DataTableWidget):
    """Data table with inline editing capabilities."""

    cell_changed = pyqtSignal(int, int, str)  # row, col, new_value

    def __init__(self, columns=None, data=None, parent=None):
        super().__init__(columns, data, parent)
        self._setup_editing()

    def _setup_editing(self):
        """Setup editing capabilities."""
        # Make items editable
        self.table.itemChanged.connect(self._on_item_changed)

    def _load_data(self):
        """Override to make items editable."""
        super()._load_data()

        # Make all items editable
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)

    def _on_item_changed(self, item):
        """Handle cell value change."""
        row = item.row()
        col = item.column()
        new_value = item.text()

        # Update internal data
        col_offset = 1 if self._checkable else 0
        data_col = col - col_offset

        if 0 <= data_col < len(self._columns) and row < len(self._data):
            self._data[row][data_col] = new_value

        self.cell_changed.emit(row, col, new_value)
        self.data_changed.emit()


class PaginatedDataTable(DataTableWidget):
    """Data table with pagination support."""

    page_changed = pyqtSignal(int)  # Emits current page

    def __init__(self, columns=None, data=None, page_size=50, parent=None):
        self._page_size = page_size
        self._current_page = 1
        self._total_pages = 1
        super().__init__(columns, data, parent)
        self._setup_pagination()

    def _setup_pagination(self):
        """Setup pagination controls."""
        from ..navigation.pagination import PaginationWidget

        # Add pagination widget
        self.pagination = PaginationWidget("numeric", self._total_pages, self._current_page)
        self.pagination.page_changed.connect(self._on_page_changed)

        # Add to layout
        self.layout().addWidget(self.pagination)

    def _load_data(self):
        """Override to load paginated data."""
        if not self._columns or not self._data:
            return

        # Calculate pagination
        self._total_pages = max(1, (len(self._data) + self._page_size - 1) // self._page_size)
        self.pagination.set_total_pages(self._total_pages)

        # Get current page data
        start_idx = (self._current_page - 1) * self._page_size
        end_idx = start_idx + self._page_size
        page_data = self._data[start_idx:end_idx]

        # Set up table structure
        self.table.setRowCount(len(page_data))
        self.table.setColumnCount(len(self._columns))
        self.table.setHorizontalHeaderLabels(self._columns)

        # Populate page data
        for row_idx, row_data in enumerate(page_data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row_idx, col_idx, item)

        # Auto-resize columns
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _on_page_changed(self, page: int):
        """Handle page change."""
        self._current_page = page
        self._load_data()
        self.page_changed.emit(page)

    def set_page_size(self, page_size: int):
        """Set number of rows per page."""
        self._page_size = page_size
        self._current_page = 1
        self._load_data()