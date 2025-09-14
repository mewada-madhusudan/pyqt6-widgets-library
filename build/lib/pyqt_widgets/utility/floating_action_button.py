"""
Floating action button with expandable menu options.
"""

from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QFont, QIcon
from ..base.theme_manager import theme_manager


class FloatingActionButton(QPushButton):
    """Circular floating action button."""

    def __init__(self, icon_text="✚", size=56, parent=None):
        super().__init__(icon_text, parent)
        self._size = size
        self._expanded = False
        self._sub_buttons = []
        self._animations = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup the FAB UI."""
        self.setFixedSize(self._size, self._size)

        # Styling
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_manager.get_color('primary')};
                color: white;
                border: none;
                border-radius: {self._size // 2}px;
                font-size: {self._size // 3}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('dark')};
            }}
            QPushButton:pressed {{
                background-color: {theme_manager.get_color('dark')};
            }}
        """)

        # Position at bottom-right of parent
        if self.parent():
            self._position_fab()

        # Connect click
        self.clicked.connect(self._toggle_expansion)

        # Add shadow effect
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        from PyQt6.QtGui import QColor

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)

    def _position_fab(self):
        """Position FAB at bottom-right of parent."""
        if not self.parent():
            return

        parent_rect = self.parent().rect()
        x = parent_rect.width() - self._size - 20
        y = parent_rect.height() - self._size - 20
        self.move(x, y)

    def add_sub_action(self, icon_text: str, tooltip: str = "", callback=None):
        """Add sub-action button."""
        sub_button = QPushButton(icon_text, self.parent())
        sub_button.setFixedSize(40, 40)
        sub_button.setToolTip(tooltip)

        # Styling for sub-button
        sub_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_manager.get_color('surface')};
                color: {theme_manager.get_color('text')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: 20px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('hover')};
            }}
        """)

        # Connect callback
        if callback:
            sub_button.clicked.connect(callback)
            sub_button.clicked.connect(self._collapse)

        # Position initially hidden
        sub_button.move(self.pos())
        sub_button.hide()

        self._sub_buttons.append(sub_button)

    def _toggle_expansion(self):
        """Toggle expansion of sub-actions."""
        if self._expanded:
            self._collapse()
        else:
            self._expand()

    def _expand(self):
        """Expand sub-actions."""
        if not self._sub_buttons:
            return

        self._expanded = True

        # Update main button icon
        self.setText("✕")

        # Show and animate sub-buttons
        fab_pos = self.pos()
        spacing = 60

        for i, button in enumerate(self._sub_buttons):
            button.show()

            # Calculate target position
            target_y = fab_pos.y() - (i + 1) * spacing
            target_pos = QPoint(fab_pos.x() + 8, target_y)

            # Animate to position
            animation = QPropertyAnimation(button, b"pos")
            animation.setDuration(200 + i * 50)  # Stagger animations
            animation.setStartValue(fab_pos)
            animation.setEndValue(target_pos)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)

            self._animations.append(animation)
            animation.start()

    def _collapse(self):
        """Collapse sub-actions."""
        if not self._expanded:
            return

        self._expanded = False

        # Update main button icon
        self.setText("✚")

        # Animate sub-buttons back
        fab_pos = self.pos()

        for i, button in enumerate(self._sub_buttons):
            animation = QPropertyAnimation(button, b"pos")
            animation.setDuration(150)
            animation.setStartValue(button.pos())
            animation.setEndValue(fab_pos)
            animation.setEasingCurve(QEasingCurve.Type.InCubic)

            # Hide button when animation completes
            animation.finished.connect(button.hide)

            self._animations.append(animation)
            animation.start()

    def resizeEvent(self, event):
        """Handle parent resize to reposition FAB."""
        super().resizeEvent(event)
        if self.parent():
            self._position_fab()


class ExpandableFAB(FloatingActionButton):
    """FAB with expandable menu in different directions."""

    def __init__(self, icon_text="✚", size=56, direction="up", parent=None):
        self._direction = direction  # "up", "down", "left", "right", "radial"
        super().__init__(icon_text, size, parent)

    def _expand(self):
        """Override to support different expansion directions."""
        if not self._sub_buttons:
            return

        self._expanded = True
        self.setText("✕")

        fab_pos = self.pos()
        spacing = 60

        for i, button in enumerate(self._sub_buttons):
            button.show()

            # Calculate target position based on direction
            if self._direction == "up":
                target_pos = QPoint(fab_pos.x() + 8, fab_pos.y() - (i + 1) * spacing)
            elif self._direction == "down":
                target_pos = QPoint(fab_pos.x() + 8, fab_pos.y() + (i + 1) * spacing)
            elif self._direction == "left":
                target_pos = QPoint(fab_pos.x() - (i + 1) * spacing, fab_pos.y() + 8)
            elif self._direction == "right":
                target_pos = QPoint(fab_pos.x() + (i + 1) * spacing, fab_pos.y() + 8)
            elif self._direction == "radial":
                import math
                angle = (i * 45) * math.pi / 180  # 45 degrees apart
                offset_x = int(spacing * math.cos(angle))
                offset_y = int(spacing * math.sin(angle))
                target_pos = QPoint(fab_pos.x() + offset_x, fab_pos.y() - offset_y)
            else:
                target_pos = QPoint(fab_pos.x() + 8, fab_pos.y() - (i + 1) * spacing)

            # Animate to position
            animation = QPropertyAnimation(button, b"pos")
            animation.setDuration(200 + i * 50)
            animation.setStartValue(fab_pos)
            animation.setEndValue(target_pos)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)

            self._animations.append(animation)
            animation.start()


class SpeedDialFAB(FloatingActionButton):
    """FAB with speed dial functionality."""

    action_triggered = pyqtSignal(str)  # Emits action name

    def __init__(self, parent=None):
        super().__init__("⚡", 56, parent)
        self._actions = {}

    def add_speed_dial_action(self, name: str, icon: str, tooltip: str = ""):
        """Add speed dial action."""
        def action_callback():
            self.action_triggered.emit(name)

        self.add_sub_action(icon, tooltip or name, action_callback)
        self._actions[name] = {
            'icon': icon,
            'tooltip': tooltip
        }

    def get_actions(self) -> dict:
        """Get all speed dial actions."""
        return self._actions.copy()


class AnimatedFAB(FloatingActionButton):
    """FAB with rotation and scale animations."""

    def __init__(self, icon_text="✚", size=56, parent=None):
        super().__init__(icon_text, size, parent)
        self._setup_animations()

    def _setup_animations(self):
        """Setup rotation and scale animations."""
        from PyQt6.QtCore import QPropertyAnimation

        self._rotation_animation = QPropertyAnimation(self, b"rotation")
        self._rotation_animation.setDuration(300)

        self._scale_animation = QPropertyAnimation(self, b"geometry")
        self._scale_animation.setDuration(200)

    def _toggle_expansion(self):
        """Override with rotation animation."""
        # Rotate button
        if self._expanded:
            # Rotate back to normal
            self._rotation_animation.setStartValue(45)
            self._rotation_animation.setEndValue(0)
        else:
            # Rotate 45 degrees
            self._rotation_animation.setStartValue(0)
            self._rotation_animation.setEndValue(45)

        self._rotation_animation.start()

        # Call parent method
        super()._toggle_expansion()

    def enterEvent(self, event):
        """Scale up on hover."""
        super().enterEvent(event)

        current_rect = self.geometry()
        scaled_rect = current_rect.adjusted(-4, -4, 4, 4)

        self._scale_animation.setStartValue(current_rect)
        self._scale_animation.setEndValue(scaled_rect)
        self._scale_animation.start()

    def leaveEvent(self, event):
        """Scale back on leave."""
        super().leaveEvent(event)

        current_rect = self.geometry()
        normal_rect = current_rect.adjusted(4, 4, -4, -4)

        self._scale_animation.setStartValue(current_rect)
        self._scale_animation.setEndValue(normal_rect)
        self._scale_animation.start()


class ContextualFAB(FloatingActionButton):
    """FAB that changes based on context."""

    context_changed = pyqtSignal(str)  # Emits new context

    def __init__(self, parent=None):
        super().__init__("✚", 56, parent)
        self._contexts = {}
        self._current_context = "default"

    def add_context(self, context_name: str, icon: str, actions: list):
        """Add context configuration."""
        self._contexts[context_name] = {
            'icon': icon,
            'actions': actions
        }

    def set_context(self, context_name: str):
        """Switch to specific context."""
        if context_name not in self._contexts:
            return

        # Collapse if expanded
        if self._expanded:
            self._collapse()

        # Clear existing sub-buttons
        for button in self._sub_buttons:
            button.setParent(None)
        self._sub_buttons.clear()

        # Update context
        self._current_context = context_name
        context = self._contexts[context_name]

        # Update main button
        self.setText(context['icon'])

        # Add context actions
        for action in context['actions']:
            self.add_sub_action(
                action.get('icon', '•'),
                action.get('tooltip', ''),
                action.get('callback')
            )

        self.context_changed.emit(context_name)

    def get_current_context(self) -> str:
        """Get current context name."""
        return self._current_context


class MiniFAB(FloatingActionButton):
    """Smaller version of FAB for secondary actions."""

    def __init__(self, icon_text="✚", parent=None):
        super().__init__(icon_text, 40, parent)  # Smaller size

        # Update styling for mini size
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_manager.get_color('secondary')};
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('primary')};
            }}
        """)