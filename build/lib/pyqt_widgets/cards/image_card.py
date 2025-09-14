"""
Image card widget for displaying images with descriptions.
"""

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QBrush, QColor
from ..base.base_card import BaseCardWidget
from ..base.theme_manager import theme_manager


class ImageCardWidget(BaseCardWidget):
    """Card widget for displaying images with overlay descriptions."""

    image_clicked = pyqtSignal()

    def __init__(self, image_path="", title="", description="", parent=None):
        super().__init__(parent)
        self._image_path = image_path
        self._title = title
        self._description = description
        self._image_label = None
        self._overlay_widget = None
        self._setup_image_card_ui()

    def _setup_image_card_ui(self):
        """Setup the image card UI."""
        # Main container
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Image container with overlay
        image_container = QWidget()
        image_container.setFixedHeight(200)
        image_container.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_manager.get_color('light')};
                border-radius: {theme_manager.get_border_radius('sm')}px;
            }}
        """)

        # Image label
        self._image_label = QLabel()
        self._image_label.setParent(image_container)
        self._image_label.setGeometry(0, 0, image_container.width(), image_container.height())
        self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_label.setStyleSheet("border-radius: 8px;")

        if self._image_path:
            self._load_image()
        else:
            self._image_label.setText("No Image")
            self._image_label.setStyleSheet(f"""
                QLabel {{
                    color: {theme_manager.get_color('text_secondary')};
                    background-color: {theme_manager.get_color('light')};
                    border-radius: {theme_manager.get_border_radius('sm')}px;
                }}
            """)

        # Overlay for title and description
        if self._title or self._description:
            self._overlay_widget = QWidget()
            self._overlay_widget.setParent(image_container)
            self._overlay_widget.setStyleSheet(f"""
                QWidget {{
                    background-color: rgba(0, 0, 0, 0.7);
                    border-radius: 0px 0px {theme_manager.get_border_radius('sm')}px {theme_manager.get_border_radius('sm')}px;
                }}
            """)

            overlay_layout = QVBoxLayout(self._overlay_widget)
            overlay_layout.setContentsMargins(16, 12, 16, 12)
            overlay_layout.setSpacing(4)

            # Title
            if self._title:
                title_label = QLabel(self._title)
                title_font = theme_manager.get_font('heading')
                title_font.setPointSize(12)
                title_label.setFont(title_font)
                title_label.setStyleSheet("color: white;")
                overlay_layout.addWidget(title_label)

            # Description
            if self._description:
                desc_label = QLabel(self._description)
                desc_label.setFont(theme_manager.get_font('caption'))
                desc_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
                desc_label.setWordWrap(True)
                overlay_layout.addWidget(desc_label)

            # Position overlay at bottom
            self._overlay_widget.move(0, image_container.height() - self._overlay_widget.sizeHint().height())

        container_layout.addWidget(image_container)
        self.set_body(container)

        # Make image clickable
        self._image_label.mousePressEvent = self._on_image_click

    def _load_image(self):
        """Load and display image."""
        if not self._image_path:
            return

        pixmap = QPixmap(self._image_path)
        if not pixmap.isNull():
            # Scale image to fit container while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                self._image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self._image_label.setPixmap(scaled_pixmap)
        else:
            self._image_label.setText("Invalid Image")
            self._image_label.setStyleSheet(f"""
                QLabel {{
                    color: {theme_manager.get_color('danger')};
                    background-color: {theme_manager.get_color('light')};
                }}
            """)

    def _on_image_click(self, event):
        """Handle image click."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.image_clicked.emit()

    def set_image(self, image_path: str):
        """Update image."""
        self._image_path = image_path
        self._load_image()

    def set_title(self, title: str):
        """Update title."""
        self._title = title
        self._setup_image_card_ui()

    def set_description(self, description: str):
        """Update description."""
        self._description = description
        self._setup_image_card_ui()

    def get_image_path(self) -> str:
        """Get current image path."""
        return self._image_path

    def get_title(self) -> str:
        """Get current title."""
        return self._title

    def get_description(self) -> str:
        """Get current description."""
        return self._description

    def resizeEvent(self, event):
        """Handle resize to reposition overlay."""
        super().resizeEvent(event)
        if self._overlay_widget and self._image_label:
            # Reposition overlay
            overlay_height = self._overlay_widget.sizeHint().height()
            container_height = self._image_label.parent().height()
            self._overlay_widget.move(0, container_height - overlay_height)
            self._overlay_widget.resize(self._image_label.parent().width(), overlay_height)


class GalleryCard(ImageCardWidget):
    """Image card with gallery functionality."""

    def __init__(self, images=None, current_index=0, parent=None):
        self._images = images or []
        self._current_index = current_index

        # Initialize with first image
        image_path = self._images[current_index] if self._images else ""
        super().__init__(image_path, parent=parent)

        if len(self._images) > 1:
            self._add_navigation_controls()

    def _add_navigation_controls(self):
        """Add previous/next navigation controls."""
        from ..base.base_button import BaseButton

        # Navigation controls
        nav_widget = QWidget()
        nav_layout = QHBoxLayout(nav_widget)
        nav_layout.setContentsMargins(0, 0, 0, 0)

        # Previous button
        prev_btn = BaseButton("‹", "ghost", "small")
        prev_btn.setFixedSize(32, 32)
        prev_btn.clicked.connect(self._previous_image)
        nav_layout.addWidget(prev_btn)

        # Image counter
        self._counter_label = QLabel(f"{self._current_index + 1} / {len(self._images)}")
        self._counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._counter_label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
        nav_layout.addWidget(self._counter_label)

        # Next button
        next_btn = BaseButton("›", "ghost", "small")
        next_btn.setFixedSize(32, 32)
        next_btn.clicked.connect(self._next_image)
        nav_layout.addWidget(next_btn)

        self.set_footer(nav_widget)

    def _previous_image(self):
        """Show previous image."""
        if self._images and self._current_index > 0:
            self._current_index -= 1
            self.set_image(self._images[self._current_index])
            self._update_counter()

    def _next_image(self):
        """Show next image."""
        if self._images and self._current_index < len(self._images) - 1:
            self._current_index += 1
            self.set_image(self._images[self._current_index])
            self._update_counter()

    def _update_counter(self):
        """Update image counter display."""
        if hasattr(self, '_counter_label'):
            self._counter_label.setText(f"{self._current_index + 1} / {len(self._images)}")

    def add_image(self, image_path: str):
        """Add image to gallery."""
        self._images.append(image_path)
        if len(self._images) == 1:
            self.set_image(image_path)
        self._update_counter()

    def remove_image(self, index: int):
        """Remove image from gallery."""
        if 0 <= index < len(self._images):
            del self._images[index]
            if self._current_index >= len(self._images):
                self._current_index = len(self._images) - 1
            if self._images:
                self.set_image(self._images[self._current_index])
            self._update_counter()

    def set_images(self, images: list):
        """Set all images."""
        self._images = images
        self._current_index = 0
        if self._images:
            self.set_image(self._images[0])
        self._update_counter()


class ProductCard(ImageCardWidget):
    """Product card with price and rating."""

    def __init__(self, image_path="", name="", price="", rating=0, parent=None):
        self._name = name
        self._price = price
        self._rating = rating
        super().__init__(image_path, name, parent=parent)
        self._setup_product_ui()

    def _setup_product_ui(self):
        """Setup product-specific UI."""
        # Product info section
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 8, 0, 0)
        info_layout.setSpacing(4)

        # Name
        if self._name:
            name_label = QLabel(self._name)
            name_font = theme_manager.get_font('default')
            name_font.setWeight(QFont.Weight.Bold)
            name_label.setFont(name_font)
            name_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
            info_layout.addWidget(name_label)

        # Price and rating row
        price_rating_widget = QWidget()
        price_rating_layout = QHBoxLayout(price_rating_widget)
        price_rating_layout.setContentsMargins(0, 0, 0, 0)

        # Price
        if self._price:
            price_label = QLabel(self._price)
            price_font = theme_manager.get_font('heading')
            price_font.setPointSize(14)
            price_label.setFont(price_font)
            price_label.setStyleSheet(f"color: {theme_manager.get_color('primary')};")
            price_rating_layout.addWidget(price_label)

        price_rating_layout.addStretch()

        # Rating stars
        if self._rating > 0:
            rating_label = QLabel("★" * int(self._rating) + "☆" * (5 - int(self._rating)))
            rating_label.setStyleSheet(f"color: {theme_manager.get_color('warning')};")
            price_rating_layout.addWidget(rating_label)

        info_layout.addWidget(price_rating_widget)

        # Add to body layout
        if hasattr(self, 'body_layout'):
            self.body_layout.addWidget(info_widget)

    def set_name(self, name: str):
        """Update product name."""
        self._name = name
        self.set_title(name)

    def set_price(self, price: str):
        """Update product price."""
        self._price = price
        self._setup_product_ui()

    def set_rating(self, rating: float):
        """Update product rating."""
        self._rating = rating
        self._setup_product_ui()

    def get_name(self) -> str:
        """Get product name."""
        return self._name

    def get_price(self) -> str:
        """Get product price."""
        return self._price

    def get_rating(self) -> float:
        """Get product rating."""
        return self._rating