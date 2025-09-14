"""
Interactive star rating widget with hover preview.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QCursor
from ..base.theme_manager import theme_manager


class RatingStarWidget(QWidget):
    """Interactive star rating widget."""

    rating_changed = pyqtSignal(int)  # Emits new rating value

    def __init__(self, max_stars=5, current_rating=0, read_only=False,
                 size="medium", parent=None):
        super().__init__(parent)
        self._max_stars = max_stars
        self._current_rating = current_rating
        self._read_only = read_only
        self._size = size
        self._hover_rating = 0
        self._stars = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup the star rating UI."""
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # Create star labels
        for i in range(self._max_stars):
            star = StarLabel(i + 1, self._size)
            star.star_hovered.connect(self._on_star_hover)
            star.star_clicked.connect(self._on_star_click)

            if not self._read_only:
                star.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            self._stars.append(star)
            layout.addWidget(star)

        # Set initial rating
        self._update_stars_display()

        # Handle mouse leave
        if not self._read_only:
            self.setMouseTracking(True)

    def _get_star_size(self) -> int:
        """Get star size based on size setting."""
        sizes = {
            'small': 16,
            'medium': 20,
            'large': 24
        }
        return sizes.get(self._size, 20)

    def _on_star_hover(self, star_index: int):
        """Handle star hover."""
        if self._read_only:
            return

        self._hover_rating = star_index
        self._update_stars_display(preview=True)

    def _on_star_click(self, star_index: int):
        """Handle star click."""
        if self._read_only:
            return

        # Toggle rating: if clicking same star, set to 0
        if self._current_rating == star_index:
            self._current_rating = 0
        else:
            self._current_rating = star_index

        self._hover_rating = 0
        self._update_stars_display()
        self.rating_changed.emit(self._current_rating)

    def _update_stars_display(self, preview=False):
        """Update star display based on current/hover rating."""
        rating_to_show = self._hover_rating if preview and self._hover_rating > 0 else self._current_rating

        for i, star in enumerate(self._stars):
            star_index = i + 1

            if star_index <= rating_to_show:
                # Filled star
                star.set_filled(True)
                if preview and not self._read_only:
                    star.set_preview(True)
                else:
                    star.set_preview(False)
            else:
                # Empty star
                star.set_filled(False)
                star.set_preview(False)

    def leaveEvent(self, event):
        """Handle mouse leave."""
        if not self._read_only:
            self._hover_rating = 0
            self._update_stars_display()
        super().leaveEvent(event)

    def set_rating(self, rating: int):
        """Set current rating."""
        self._current_rating = max(0, min(rating, self._max_stars))
        self._update_stars_display()

    def get_rating(self) -> int:
        """Get current rating."""
        return self._current_rating

    def set_read_only(self, read_only: bool):
        """Set read-only mode."""
        self._read_only = read_only

        for star in self._stars:
            if read_only:
                star.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            else:
                star.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def set_max_stars(self, max_stars: int):
        """Change maximum number of stars."""
        if max_stars == self._max_stars:
            return

        # Clear existing stars
        for star in self._stars:
            star.setParent(None)
        self._stars.clear()

        # Update and recreate
        self._max_stars = max_stars
        self._current_rating = min(self._current_rating, max_stars)
        self._setup_ui()


class StarLabel(QLabel):
    """Individual star label with hover and click handling."""

    star_hovered = pyqtSignal(int)  # Emits star index (1-based)
    star_clicked = pyqtSignal(int)  # Emits star index (1-based)

    def __init__(self, star_index: int, size: str = "medium", parent=None):
        super().__init__(parent)
        self._star_index = star_index
        self._size = size
        self._filled = False
        self._preview = False
        self._setup_star()

    def _setup_star(self):
        """Setup star appearance."""
        # Get size
        star_size = self._get_star_size()
        self.setFixedSize(star_size, star_size)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set font
        font = QFont()
        font.setPointSize(star_size - 4)
        self.setFont(font)

        # Initial display
        self._update_display()

    def _get_star_size(self) -> int:
        """Get star size based on size setting."""
        sizes = {
            'small': 16,
            'medium': 20,
            'large': 24
        }
        return sizes.get(self._size, 20)

    def _update_display(self):
        """Update star visual appearance."""
        if self._filled:
            star_char = "★"  # Filled star
            if self._preview:
                color = theme_manager.get_color('warning')  # Preview color
            else:
                color = theme_manager.get_color('primary')  # Normal filled color
        else:
            star_char = "☆"  # Empty star
            color = theme_manager.get_color('text_secondary')

        self.setText(star_char)
        self.setStyleSheet(f"color: {color};")

    def set_filled(self, filled: bool):
        """Set filled state."""
        self._filled = filled
        self._update_display()

    def set_preview(self, preview: bool):
        """Set preview state."""
        self._preview = preview
        self._update_display()

    def enterEvent(self, event):
        """Handle mouse enter."""
        self.star_hovered.emit(self._star_index)
        super().enterEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse press."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.star_clicked.emit(self._star_index)
        super().mousePressEvent(event)


class RatingDisplay(QWidget):
    """Read-only rating display with average and count."""

    def __init__(self, average_rating=0.0, total_ratings=0, max_stars=5, parent=None):
        super().__init__(parent)
        self._average_rating = average_rating
        self._total_ratings = total_ratings
        self._max_stars = max_stars
        self._setup_ui()

    def _setup_ui(self):
        """Setup rating display UI."""
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Star rating
        self.star_widget = RatingStarWidget(
            max_stars=self._max_stars,
            current_rating=round(self._average_rating),
            read_only=True,
            size="small"
        )
        layout.addWidget(self.star_widget)

        # Average rating text
        self.rating_label = QLabel(f"{self._average_rating:.1f}")
        self.rating_label.setFont(theme_manager.get_font('default'))
        self.rating_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        layout.addWidget(self.rating_label)

        # Total ratings count
        self.count_label = QLabel(f"({self._total_ratings})")
        self.count_label.setFont(theme_manager.get_font('caption'))
        self.count_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        layout.addWidget(self.count_label)

    def update_rating(self, average_rating: float, total_ratings: int):
        """Update rating display."""
        self._average_rating = average_rating
        self._total_ratings = total_ratings

        self.star_widget.set_rating(round(average_rating))
        self.rating_label.setText(f"{average_rating:.1f}")
        self.count_label.setText(f"({total_ratings})")


class DetailedRatingWidget(QWidget):
    """Detailed rating widget with breakdown by star level."""

    def __init__(self, ratings_breakdown=None, parent=None):
        super().__init__(parent)
        # ratings_breakdown: {5: 10, 4: 5, 3: 2, 2: 1, 1: 0}
        self._ratings_breakdown = ratings_breakdown or {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        self._setup_ui()

    def _setup_ui(self):
        """Setup detailed rating UI."""
        from PyQt6.QtWidgets import QProgressBar

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(4)

        # Calculate totals
        total_ratings = sum(self._ratings_breakdown.values())
        average_rating = self._calculate_average()

        # Summary
        summary_layout = QHBoxLayout()

        # Large average rating
        avg_label = QLabel(f"{average_rating:.1f}")
        avg_font = theme_manager.get_font('heading')
        avg_font.setPointSize(24)
        avg_label.setFont(avg_font)
        avg_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        summary_layout.addWidget(avg_label)

        # Stars and count
        details_layout = QVBoxLayout()

        star_widget = RatingStarWidget(
            max_stars=5,
            current_rating=round(average_rating),
            read_only=True,
            size="small"
        )
        details_layout.addWidget(star_widget)

        count_label = QLabel(f"{total_ratings} ratings")
        count_label.setFont(theme_manager.get_font('caption'))
        count_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        details_layout.addWidget(count_label)

        summary_layout.addLayout(details_layout)
        summary_layout.addStretch()

        main_layout.addLayout(summary_layout)

        # Breakdown bars
        for stars in range(5, 0, -1):
            bar_layout = QHBoxLayout()
            bar_layout.setSpacing(8)

            # Star label
            star_label = QLabel(f"{stars} ★")
            star_label.setFixedWidth(30)
            star_label.setFont(theme_manager.get_font('caption'))
            bar_layout.addWidget(star_label)

            # Progress bar
            progress_bar = QProgressBar()
            progress_bar.setFixedHeight(8)
            progress_bar.setTextVisible(False)

            count = self._ratings_breakdown.get(stars, 0)
            percentage = (count / total_ratings * 100) if total_ratings > 0 else 0
            progress_bar.setValue(int(percentage))

            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: none;
                    border-radius: 4px;
                    background-color: {theme_manager.get_color('light')};
                }}
                QProgressBar::chunk {{
                    border-radius: 4px;
                    background-color: {theme_manager.get_color('primary')};
                }}
            """)

            bar_layout.addWidget(progress_bar)

            # Count label
            count_label = QLabel(str(count))
            count_label.setFixedWidth(30)
            count_label.setFont(theme_manager.get_font('caption'))
            count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            bar_layout.addWidget(count_label)

            main_layout.addLayout(bar_layout)

    def _calculate_average(self) -> float:
        """Calculate average rating."""
        total_points = sum(stars * count for stars, count in self._ratings_breakdown.items())
        total_ratings = sum(self._ratings_breakdown.values())

        return total_points / total_ratings if total_ratings > 0 else 0.0

    def update_breakdown(self, ratings_breakdown: dict):
        """Update ratings breakdown."""
        self._ratings_breakdown = ratings_breakdown

        # Clear and recreate UI
        for i in reversed(range(self.layout().count())):
            item = self.layout().itemAt(i)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                # Clear nested layouts
                pass

        self._setup_ui()


class CompactRatingWidget(RatingStarWidget):
    """Compact rating widget for small spaces."""

    def __init__(self, current_rating=0, read_only=True, parent=None):
        super().__init__(
            max_stars=5,
            current_rating=current_rating,
            read_only=read_only,
            size="small",
            parent=parent
        )

    def _setup_ui(self):
        """Override for compact layout."""
        super()._setup_ui()

        # Add rating number
        rating_label = QLabel(f"({self._current_rating})")
        rating_label.setFont(theme_manager.get_font('caption'))
        rating_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        self.layout().addWidget(rating_label)

        self._rating_label = rating_label

    def set_rating(self, rating: int):
        """Override to update label."""
        super().set_rating(rating)
        if hasattr(self, '_rating_label'):
            self._rating_label.setText(f"({rating})")