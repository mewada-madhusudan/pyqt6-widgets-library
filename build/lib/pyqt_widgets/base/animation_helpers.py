"""
Animation helpers for smooth transitions and effects.
"""

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect, QSize, pyqtProperty
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt6.QtGui import QColor
from typing import Optional, Callable


class AnimationHelpers:
    """Helper class for creating smooth animations."""

    @staticmethod
    def fade_in(widget: QWidget, duration: int = 300, finished_callback: Optional[Callable] = None):
        """Fade in animation for a widget."""
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)

        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        if finished_callback:
            animation.finished.connect(finished_callback)

        animation.start()
        return animation

    @staticmethod
    def fade_out(widget: QWidget, duration: int = 300, finished_callback: Optional[Callable] = None):
        """Fade out animation for a widget."""
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)

        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        if finished_callback:
            animation.finished.connect(finished_callback)

        animation.start()
        return animation

    @staticmethod
    def slide_in_from_left(widget: QWidget, duration: int = 300):
        """Slide in from left animation."""
        start_rect = widget.geometry()
        start_rect.moveLeft(-start_rect.width())
        end_rect = widget.geometry()

        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        animation.start()
        return animation

    @staticmethod
    def slide_in_from_right(widget: QWidget, duration: int = 300):
        """Slide in from right animation."""
        parent_width = widget.parent().width() if widget.parent() else 800
        start_rect = widget.geometry()
        start_rect.moveLeft(parent_width)
        end_rect = widget.geometry()

        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        animation.start()
        return animation

    @staticmethod
    def expand_height(widget: QWidget, target_height: int, duration: int = 300):
        """Expand widget height animation."""
        start_size = widget.size()
        end_size = QSize(start_size.width(), target_height)

        animation = QPropertyAnimation(widget, b"size")
        animation.setDuration(duration)
        animation.setStartValue(start_size)
        animation.setEndValue(end_size)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        animation.start()
        return animation

    @staticmethod
    def collapse_height(widget: QWidget, duration: int = 300):
        """Collapse widget height animation."""
        start_size = widget.size()
        end_size = QSize(start_size.width(), 0)

        animation = QPropertyAnimation(widget, b"size")
        animation.setDuration(duration)
        animation.setStartValue(start_size)
        animation.setEndValue(end_size)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        animation.start()
        return animation

    @staticmethod
    def bounce_effect(widget: QWidget, scale_factor: float = 1.1, duration: int = 200):
        """Bounce effect animation."""
        original_size = widget.size()
        scaled_size = QSize(
            int(original_size.width() * scale_factor),
            int(original_size.height() * scale_factor)
        )

        # Scale up
        scale_up = QPropertyAnimation(widget, b"size")
        scale_up.setDuration(duration // 2)
        scale_up.setStartValue(original_size)
        scale_up.setEndValue(scaled_size)
        scale_up.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Scale back down
        scale_down = QPropertyAnimation(widget, b"size")
        scale_down.setDuration(duration // 2)
        scale_down.setStartValue(scaled_size)
        scale_down.setEndValue(original_size)
        scale_down.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Chain animations
        scale_up.finished.connect(scale_down.start)
        scale_up.start()

        return scale_up, scale_down


class AnimatedWidget(QWidget):
    """Base widget with animation support."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._animations = []

    def animate_fade_in(self, duration: int = 300):
        """Animate fade in effect."""
        animation = AnimationHelpers.fade_in(self, duration)
        self._animations.append(animation)
        return animation

    def animate_fade_out(self, duration: int = 300):
        """Animate fade out effect."""
        animation = AnimationHelpers.fade_out(self, duration)
        self._animations.append(animation)
        return animation

    def animate_slide_in_left(self, duration: int = 300):
        """Animate slide in from left."""
        animation = AnimationHelpers.slide_in_from_left(self, duration)
        self._animations.append(animation)
        return animation

    def animate_slide_in_right(self, duration: int = 300):
        """Animate slide in from right."""
        animation = AnimationHelpers.slide_in_from_right(self, duration)
        self._animations.append(animation)
        return animation

    def stop_all_animations(self):
        """Stop all running animations."""
        for animation in self._animations:
            if animation.state() == QPropertyAnimation.State.Running:
                animation.stop()
        self._animations.clear()