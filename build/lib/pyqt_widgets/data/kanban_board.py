"""
Kanban board widget with draggable cards and columns.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
                             QLabel, QFrame, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData, QPoint
from PyQt6.QtGui import QDrag, QFont, QPainter
from ..base.theme_manager import theme_manager
from ..base.base_card import BaseCardWidget
from ..base.base_button import BaseButton


class KanbanCard(BaseCardWidget):
    """Draggable card for Kanban board."""

    def __init__(self, title="", description="", card_id=None, parent=None):
        super().__init__(parent)
        self._title = title
        self._description = description
        self._card_id = card_id or id(self)
        self._drag_start_position = None
        self._setup_card_ui()

    def _setup_card_ui(self):
        """Setup the kanban card UI."""
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)

        # Title
        if self._title:
            self.title_label = QLabel(self._title)
            title_font = theme_manager.get_font('default')
            title_font.setWeight(QFont.Weight.Bold)
            self.title_label.setFont(title_font)
            self.title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
            content_layout.addWidget(self.title_label)

        # Description
        if self._description:
            self.desc_label = QLabel(self._description)
            self.desc_label.setFont(theme_manager.get_font('default'))
            self.desc_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            self.desc_label.setWordWrap(True)
            content_layout.addWidget(self.desc_label)

        self.set_body(content_widget)

        # Enable dragging
        self.setAcceptDrops(False)  # Cards don't accept drops

        # Styling
        self.setStyleSheet(f"""
            KanbanCard {{
                background-color: {theme_manager.get_color('surface')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('md')}px;
                margin: 4px;
            }}
            KanbanCard:hover {{
                border-color: {theme_manager.get_color('primary')};
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
        """)

    def mousePressEvent(self, event):
        """Handle mouse press for drag start."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_position = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging."""
        if (event.buttons() == Qt.MouseButton.LeftButton and
                self._drag_start_position is not None):

            # Check if drag distance is sufficient
            drag_distance = (event.position().toPoint() - self._drag_start_position).manhattanLength()

            if drag_distance >= 10:  # Minimum drag distance
                self._start_drag()

        super().mouseMoveEvent(event)

    def _start_drag(self):
        """Start drag operation."""
        drag = QDrag(self)
        mime_data = QMimeData()

        # Set drag data
        mime_data.setText(f"kanban_card:{self._card_id}")
        drag.setMimeData(mime_data)

        # Create drag pixmap
        pixmap = self.grab()
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))

        # Execute drag
        drag.exec(Qt.DropAction.MoveAction)

    def get_card_id(self):
        """Get card ID."""
        return self._card_id

    def set_title(self, title: str):
        """Update card title."""
        self._title = title
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)

    def set_description(self, description: str):
        """Update card description."""
        self._description = description
        if hasattr(self, 'desc_label'):
            self.desc_label.setText(description)

    def get_data(self) -> dict:
        """Get card data."""
        return {
            'id': self._card_id,
            'title': self._title,
            'description': self._description
        }


class KanbanColumn(QWidget):
    """Column for Kanban board that accepts card drops."""

    card_dropped = pyqtSignal(str, str)  # card_id, column_id
    card_added = pyqtSignal(dict)  # card_data

    def __init__(self, title="", column_id=None, parent=None):
        super().__init__(parent)
        self._title = title
        self._column_id = column_id or id(self)
        self._cards = []
        self._setup_column_ui()

    def _setup_column_ui(self):
        """Setup the kanban column UI."""
        self.setAcceptDrops(True)
        self.setMinimumWidth(250)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        # Header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(12, 8, 12, 8)

        # Title
        self.title_label = QLabel(self._title)
        title_font = theme_manager.get_font('heading')
        title_font.setPointSize(14)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        # Card count
        self.count_label = QLabel("0")
        self.count_label.setStyleSheet(f"""
            QLabel {{
                background-color: {theme_manager.get_color('light')};
                color: {theme_manager.get_color('text_secondary')};
                padding: 2px 8px;
                border-radius: 10px;
                font-size: 10px;
            }}
        """)
        header_layout.addWidget(self.count_label)

        # Add card button
        add_btn = QPushButton("+")
        add_btn.setFixedSize(24, 24)
        add_btn.setFlat(True)
        add_btn.clicked.connect(self._add_new_card)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-color: transparent;
                color: {theme_manager.get_color('text_secondary')};
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
                border-radius: 12px;
            }}
        """)
        header_layout.addWidget(add_btn)

        main_layout.addWidget(header_widget)

        # Cards scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        # Cards container
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(8)
        self.cards_layout.addStretch()

        scroll_area.setWidget(self.cards_container)
        main_layout.addWidget(scroll_area)

        # Column styling
        self.setStyleSheet(f"""
            KanbanColumn {{
                background-color: {theme_manager.get_color('light')};
                border-radius: {theme_manager.get_border_radius('lg')}px;
                border: 1px solid {theme_manager.get_color('border')};
            }}
        """)

        self._update_count()

    def dragEnterEvent(self, event):
        """Handle drag enter."""
        if event.mimeData().hasText() and event.mimeData().text().startswith("kanban_card:"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """Handle drag move."""
        if event.mimeData().hasText() and event.mimeData().text().startswith("kanban_card:"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handle card drop."""
        if event.mimeData().hasText() and event.mimeData().text().startswith("kanban_card:"):
            card_id = event.mimeData().text().split(":")[1]
            self.card_dropped.emit(card_id, str(self._column_id))
            event.acceptProposedAction()
        else:
            event.ignore()

    def add_card(self, card: KanbanCard):
        """Add card to column."""
        self._cards.append(card)
        self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)
        self._update_count()

    def remove_card(self, card_id: str):
        """Remove card from column."""
        for i, card in enumerate(self._cards):
            if card.get_card_id() == card_id:
                card.setParent(None)
                del self._cards[i]
                break
        self._update_count()

    def get_card(self, card_id: str) -> KanbanCard:
        """Get card by ID."""
        for card in self._cards:
            if card.get_card_id() == card_id:
                return card
        return None

    def _add_new_card(self):
        """Add new card (placeholder)."""
        card_data = {
            'title': 'New Card',
            'description': 'Click to edit...'
        }
        self.card_added.emit(card_data)

    def _update_count(self):
        """Update card count display."""
        self.count_label.setText(str(len(self._cards)))

    def get_column_id(self):
        """Get column ID."""
        return self._column_id

    def get_cards(self) -> list:
        """Get all cards in column."""
        return self._cards.copy()

    def set_title(self, title: str):
        """Update column title."""
        self._title = title
        self.title_label.setText(title)


class KanbanBoardWidget(QWidget):
    """Main Kanban board widget."""

    card_moved = pyqtSignal(str, str, str)  # card_id, from_column, to_column
    card_created = pyqtSignal(str, dict)  # column_id, card_data
    column_added = pyqtSignal(str)  # column_title

    def __init__(self, parent=None):
        super().__init__(parent)
        self._columns = []
        self._cards = {}  # card_id -> card mapping
        self._setup_ui()

    def _setup_ui(self):
        """Setup the kanban board UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = self._create_header()
        main_layout.addWidget(header)

        # Board scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Board container
        self.board_container = QWidget()
        self.board_layout = QHBoxLayout(self.board_container)
        self.board_layout.setContentsMargins(16, 16, 16, 16)
        self.board_layout.setSpacing(16)
        self.board_layout.addStretch()

        scroll_area.setWidget(self.board_container)
        main_layout.addWidget(scroll_area)

        # Board styling
        self.setStyleSheet(f"""
            KanbanBoardWidget {{
                background-color: {theme_manager.get_color('background')};
            }}
        """)

    def _create_header(self) -> QWidget:
        """Create board header."""
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 12, 16, 12)

        # Title
        title_label = QLabel("Kanban Board")
        title_font = theme_manager.get_font('heading')
        title_font.setPointSize(18)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Add column button
        add_column_btn = BaseButton("Add Column", "primary", "small")
        add_column_btn.clicked.connect(self._add_new_column)
        header_layout.addWidget(add_column_btn)

        # Header styling
        header.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_manager.get_color('surface')};
                border-bottom: 1px solid {theme_manager.get_color('border')};
            }}
        """)

        return header

    def add_column(self, title: str, column_id: str = None) -> KanbanColumn:
        """Add column to board."""
        column = KanbanColumn(title, column_id)
        column.card_dropped.connect(self._handle_card_drop)
        column.card_added.connect(lambda data: self._handle_card_creation(column.get_column_id(), data))

        self._columns.append(column)
        self.board_layout.insertWidget(self.board_layout.count() - 1, column)

        return column

    def add_card(self, column_id: str, title: str, description: str = "", card_id: str = None) -> KanbanCard:
        """Add card to specific column."""
        # Find column
        column = self._find_column(column_id)
        if not column:
            return None

        # Create card
        card = KanbanCard(title, description, card_id)
        self._cards[card.get_card_id()] = card

        # Add to column
        column.add_card(card)

        return card

    def _handle_card_drop(self, card_id: str, to_column_id: str):
        """Handle card drop between columns."""
        # Find card and current column
        card = self._cards.get(card_id)
        if not card:
            return

        from_column = None
        for column in self._columns:
            if column.get_card(card_id):
                from_column = column
                break

        if not from_column:
            return

        # Find target column
        to_column = self._find_column(to_column_id)
        if not to_column or to_column == from_column:
            return

        # Move card
        from_column.remove_card(card_id)
        to_column.add_card(card)

        self.card_moved.emit(card_id, str(from_column.get_column_id()), to_column_id)

    def _handle_card_creation(self, column_id: str, card_data: dict):
        """Handle new card creation."""
        self.card_created.emit(column_id, card_data)

    def _add_new_column(self):
        """Add new column (placeholder)."""
        column_title = f"Column {len(self._columns) + 1}"
        self.add_column(column_title)
        self.column_added.emit(column_title)

    def _find_column(self, column_id: str) -> KanbanColumn:
        """Find column by ID."""
        for column in self._columns:
            if str(column.get_column_id()) == str(column_id):
                return column
        return None

    def remove_column(self, column_id: str):
        """Remove column from board."""
        column = self._find_column(column_id)
        if column:
            # Remove all cards from tracking
            for card in column.get_cards():
                if card.get_card_id() in self._cards:
                    del self._cards[card.get_card_id()]

            # Remove column
            column.setParent(None)
            self._columns.remove(column)

    def get_board_data(self) -> dict:
        """Get complete board data."""
        board_data = {
            'columns': []
        }

        for column in self._columns:
            column_data = {
                'id': column.get_column_id(),
                'title': column._title,
                'cards': []
            }

            for card in column.get_cards():
                column_data['cards'].append(card.get_data())

            board_data['columns'].append(column_data)

        return board_data

    def load_board_data(self, board_data: dict):
        """Load board from data."""
        # Clear existing board
        for column in self._columns.copy():
            self.remove_column(column.get_column_id())

        # Load columns and cards
        for column_data in board_data.get('columns', []):
            column = self.add_column(column_data['title'], column_data['id'])

            for card_data in column_data.get('cards', []):
                self.add_card(
                    column.get_column_id(),
                    card_data['title'],
                    card_data.get('description', ''),
                    card_data.get('id')
                )