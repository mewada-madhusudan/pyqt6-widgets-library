"""
Theme Manager for centralized styling management.
"""

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPalette
from typing import Dict, Any


class ThemeManager(QObject):
    """Centralized theme and styling management."""

    theme_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._current_theme = "light"
        self._themes = {
            "light": {
                "colors": {
                    "primary": "#007ACC",
                    "secondary": "#6C757D",
                    "success": "#28A745",
                    "warning": "#FFC107",
                    "danger": "#DC3545",
                    "info": "#17A2B8",
                    "light": "#F8F9FA",
                    "dark": "#343A40",
                    "background": "#FFFFFF",
                    "surface": "#F5F5F5",
                    "text": "#212529",
                    "text_secondary": "#6C757D",
                    "border": "#DEE2E6",
                    "hover": "#E9ECEF"
                },
                "fonts": {
                    "default": QFont("Segoe UI", 9),
                    "heading": QFont("Segoe UI", 12, QFont.Weight.Bold),
                    "caption": QFont("Segoe UI", 8),
                    "code": QFont("Consolas", 9)
                },
                "spacing": {
                    "xs": 4,
                    "sm": 8,
                    "md": 16,
                    "lg": 24,
                    "xl": 32
                },
                "border_radius": {
                    "sm": 4,
                    "md": 8,
                    "lg": 12,
                    "xl": 16
                }
            },
            "dark": {
                "colors": {
                    "primary": "#0D7377",
                    "secondary": "#495057",
                    "success": "#198754",
                    "warning": "#FD7E14",
                    "danger": "#DC3545",
                    "info": "#0DCAF0",
                    "light": "#F8F9FA",
                    "dark": "#212529",
                    "background": "#1E1E1E",
                    "surface": "#2D2D2D",
                    "text": "#FFFFFF",
                    "text_secondary": "#B0B0B0",
                    "border": "#404040",
                    "hover": "#3A3A3A"
                },
                "fonts": {
                    "default": QFont("Segoe UI", 9),
                    "heading": QFont("Segoe UI", 12, QFont.Weight.Bold),
                    "caption": QFont("Segoe UI", 8),
                    "code": QFont("Consolas", 9)
                },
                "spacing": {
                    "xs": 4,
                    "sm": 8,
                    "md": 16,
                    "lg": 24,
                    "xl": 32
                },
                "border_radius": {
                    "sm": 4,
                    "md": 8,
                    "lg": 12,
                    "xl": 16
                }
            }
        }

    def set_theme(self, theme_name: str):
        """Set the current theme."""
        if theme_name in self._themes:
            self._current_theme = theme_name
            self.theme_changed.emit()

    def get_current_theme(self) -> str:
        """Get the current theme name."""
        return self._current_theme

    def get_color(self, color_name: str) -> str:
        """Get a color value from the current theme."""
        return self._themes[self._current_theme]["colors"].get(color_name, "#000000")

    def get_font(self, font_name: str) -> QFont:
        """Get a font from the current theme."""
        return self._themes[self._current_theme]["fonts"].get(font_name, QFont())

    def get_spacing(self, size: str) -> int:
        """Get spacing value from the current theme."""
        return self._themes[self._current_theme]["spacing"].get(size, 8)

    def get_border_radius(self, size: str) -> int:
        """Get border radius value from the current theme."""
        return self._themes[self._current_theme]["border_radius"].get(size, 4)

    def get_stylesheet(self, widget_type: str = "default") -> str:
        """Generate stylesheet for a widget type."""
        colors = self._themes[self._current_theme]["colors"]

        base_style = f"""
            QWidget {{
                background-color: {colors['background']};
                color: {colors['text']};
                font-family: 'Segoe UI';
                font-size: 9pt;
            }}

            QPushButton {{
                background-color: {colors['primary']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: {colors['hover']};
            }}

            QPushButton:pressed {{
                background-color: {colors['dark']};
            }}

            QFrame {{
                background-color: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}

            QLabel {{
                color: {colors['text']};
                background-color: transparent;
            }}
        """

        return base_style


# Global theme manager instance
theme_manager = ThemeManager()