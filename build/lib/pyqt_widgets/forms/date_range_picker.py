"""
Date range picker widget with calendar popup.
"""

from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLineEdit,
                             QPushButton, QCalendarWidget, QLabel, QFrame,
                             QApplication)
from PyQt6.QtCore import Qt, pyqtSignal, QDate, QPoint, QTimer
from PyQt6.QtGui import QIcon, QPainter, QPixmap
from ..base.theme_manager import theme_manager
from ..base.base_popup import BasePopupWidget
from datetime import datetime, date
from typing import Optional, Tuple


class DateRangePickerWidget(QWidget):
    """Date range picker with calendar popup."""

    date_range_changed = pyqtSignal(object, object)  # start_date, end_date
    start_date_changed = pyqtSignal(object)  # QDate
    end_date_changed = pyqtSignal(object)  # QDate

    def __init__(self, parent=None):
        super().__init__(parent)
        self._start_date = None
        self._end_date = None
        self._selecting_start = True
        self._popup = None
        self._setup_ui()

    def _setup_ui(self):
        """Setup the date range picker UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Start date input
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("Start date")
        self.start_input.setReadOnly(True)
        self.start_input.mousePressEvent = lambda e: self._show_calendar(True)
        layout.addWidget(self.start_input)

        # Separator
        separator = QLabel("to")
        separator.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        layout.addWidget(separator)

        # End date input
        self.end_input = QLineEdit()
        self.end_input.setPlaceholderText("End date")
        self.end_input.setReadOnly(True)
        self.end_input.mousePressEvent = lambda e: self._show_calendar(False)
        layout.addWidget(self.end_input)

        # Calendar button
        self.calendar_btn = QPushButton("📅")
        self.calendar_btn.setFixedSize(32, 32)
        self.calendar_btn.clicked.connect(lambda: self._show_calendar(True))
        layout.addWidget(self.calendar_btn)

        # Style inputs
        input_style = f"""
            QLineEdit {{
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                padding: 6px 8px;
                background-color: {theme_manager.get_color('background')};
                color: {theme_manager.get_color('text')};
                min-width: 100px;
            }}
            QLineEdit:focus {{
                border-color: {theme_manager.get_color('primary')};
            }}
            QLineEdit:hover {{
                border-color: {theme_manager.get_color('hover')};
            }}
        """

        self.start_input.setStyleSheet(input_style)
        self.end_input.setStyleSheet(input_style)

        # Style button
        self.calendar_btn.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
                background-color: {theme_manager.get_color('surface')};
                color: {theme_manager.get_color('text')};
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
            QPushButton:pressed {{
                background-color: {theme_manager.get_color('primary')};
            }}
        """)

    def _show_calendar(self, selecting_start: bool):
        """Show calendar popup."""
        self._selecting_start = selecting_start

        if self._popup:
            self._popup.close()

        self._popup = DateRangeCalendarPopup(self._start_date, self._end_date, self)
        self._popup.date_selected.connect(self._on_date_selected)
        self._popup.range_selected.connect(self._on_range_selected)

        # Position popup below the widget
        global_pos = self.mapToGlobal(QPoint(0, self.height()))
        self._popup.move(global_pos)
        self._popup.show()

    def _on_date_selected(self, date):
        """Handle single date selection."""
        if self._selecting_start:
            self.set_start_date(date)
        else:
            self.set_end_date(date)

    def _on_range_selected(self, start_date, end_date):
        """Handle date range selection."""
        self.set_date_range(start_date, end_date)
        if self._popup:
            self._popup.close()

    def set_start_date(self, date: QDate):
        """Set start date."""
        if date != self._start_date:
            self._start_date = date
            self.start_input.setText(date.toString("yyyy-MM-dd") if date else "")
            self.start_date_changed.emit(date)

            if self._start_date and self._end_date:
                self.date_range_changed.emit(self._start_date, self._end_date)

    def set_end_date(self, date: QDate):
        """Set end date."""
        if date != self._end_date:
            self._end_date = date
            self.end_input.setText(date.toString("yyyy-MM-dd") if date else "")
            self.end_date_changed.emit(date)

            if self._start_date and self._end_date:
                self.date_range_changed.emit(self._start_date, self._end_date)

    def set_date_range(self, start_date: QDate, end_date: QDate):
        """Set both start and end dates."""
        self._start_date = start_date
        self._end_date = end_date

        self.start_input.setText(start_date.toString("yyyy-MM-dd") if start_date else "")
        self.end_input.setText(end_date.toString("yyyy-MM-dd") if end_date else "")

        if start_date:
            self.start_date_changed.emit(start_date)
        if end_date:
            self.end_date_changed.emit(end_date)

        if start_date and end_date:
            self.date_range_changed.emit(start_date, end_date)

    def get_start_date(self) -> Optional[QDate]:
        """Get start date."""
        return self._start_date

    def get_end_date(self) -> Optional[QDate]:
        """Get end date."""
        return self._end_date

    def get_date_range(self) -> Tuple[Optional[QDate], Optional[QDate]]:
        """Get date range as tuple."""
        return (self._start_date, self._end_date)

    def clear(self):
        """Clear both dates."""
        self._start_date = None
        self._end_date = None
        self.start_input.clear()
        self.end_input.clear()


class DateRangeCalendarPopup(BasePopupWidget):
    """Calendar popup for date range selection."""

    date_selected = pyqtSignal(object)  # QDate
    range_selected = pyqtSignal(object, object)  # start_date, end_date

    def __init__(self, start_date=None, end_date=None, parent=None):
        super().__init__(parent)
        self._start_date = start_date
        self._end_date = end_date
        self._temp_start = None
        self._temp_end = None
        self._setup_calendar_ui()

    def _setup_calendar_ui(self):
        """Setup calendar popup UI."""
        layout = QVBoxLayout(self.content_widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Header with preset ranges
        header_layout = QHBoxLayout()

        presets = [
            ("Today", 0, 0),
            ("Yesterday", -1, -1),
            ("Last 7 days", -6, 0),
            ("Last 30 days", -29, 0),
            ("This month", "month_start", "month_end")
        ]

        for label, start_offset, end_offset in presets:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, s=start_offset, e=end_offset:
                                self._select_preset(s, e))
            btn.setStyleSheet(f"""
                QPushButton {{
                    border: 1px solid {theme_manager.get_color('border')};
                    border-radius: {theme_manager.get_border_radius('sm')}px;
                    padding: 4px 8px;
                    background-color: {theme_manager.get_color('surface')};
                    color: {theme_manager.get_color('text')};
                    font-size: 8pt;
                }}
                QPushButton:hover {{
                    background-color: {theme_manager.get_color('hover')};
                }}
            """)
            header_layout.addWidget(btn)

        layout.addLayout(header_layout)

        # Calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self._on_calendar_clicked)

        # Style calendar
        self.calendar.setStyleSheet(f"""
            QCalendarWidget {{
                background-color: {theme_manager.get_color('background')};
                color: {theme_manager.get_color('text')};
            }}
            QCalendarWidget QTableView {{
                selection-background-color: {theme_manager.get_color('primary')};
            }}
        """)

        layout.addWidget(self.calendar)

        # Action buttons
        button_layout = QHBoxLayout()

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self._clear_selection)

        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self._apply_selection)

        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.apply_btn)

        layout.addLayout(button_layout)

        # Set initial selection
        if self._start_date:
            self.calendar.setSelectedDate(self._start_date)

    def _select_preset(self, start_offset, end_offset):
        """Select a preset date range."""
        today = QDate.currentDate()

        if start_offset == "month_start":
            start_date = QDate(today.year(), today.month(), 1)
            end_date = today
        else:
            start_date = today.addDays(start_offset)
            end_date = today.addDays(end_offset)

        self._temp_start = start_date
        self._temp_end = end_date
        self.range_selected.emit(start_date, end_date)

    def _on_calendar_clicked(self, date):
        """Handle calendar date click."""
        if not self._temp_start or (self._temp_start and self._temp_end):
            # Start new selection
            self._temp_start = date
            self._temp_end = None
        else:
            # Complete selection
            if date < self._temp_start:
                self._temp_end = self._temp_start
                self._temp_start = date
            else:
                self._temp_end = date

        self.date_selected.emit(date)

    def _clear_selection(self):
        """Clear current selection."""
        self._temp_start = None
        self._temp_end = None
        self.range_selected.emit(None, None)

    def _apply_selection(self):
        """Apply current selection."""
        if self._temp_start and self._temp_end:
            self.range_selected.emit(self._temp_start, self._temp_end)
        elif self._temp_start:
            self.date_selected.emit(self._temp_start)

        self.close()


class SimpleDateRangePicker(QWidget):
    """Simplified date range picker with text inputs."""

    date_range_changed = pyqtSignal(object, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Setup simple date range picker."""
        layout = QHBoxLayout(self)

        # Start date
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("YYYY-MM-DD")
        self.start_input.textChanged.connect(self._validate_dates)
        layout.addWidget(QLabel("From:"))
        layout.addWidget(self.start_input)

        # End date
        self.end_input = QLineEdit()
        self.end_input.setPlaceholderText("YYYY-MM-DD")
        self.end_input.textChanged.connect(self._validate_dates)
        layout.addWidget(QLabel("To:"))
        layout.addWidget(self.end_input)

    def _validate_dates(self):
        """Validate and emit date range."""
        try:
            start_text = self.start_input.text()
            end_text = self.end_input.text()

            if start_text and end_text:
                start_date = QDate.fromString(start_text, "yyyy-MM-dd")
                end_date = QDate.fromString(end_text, "yyyy-MM-dd")

                if start_date.isValid() and end_date.isValid():
                    self.date_range_changed.emit(start_date, end_date)
        except:
            pass

    def get_date_range(self):
        """Get current date range."""
        try:
            start_date = QDate.fromString(self.start_input.text(), "yyyy-MM-dd")
            end_date = QDate.fromString(self.end_input.text(), "yyyy-MM-dd")

            if start_date.isValid() and end_date.isValid():
                return (start_date, end_date)
        except:
            pass
        return (None, None)