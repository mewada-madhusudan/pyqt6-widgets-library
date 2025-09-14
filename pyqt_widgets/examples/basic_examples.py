"""
Basic examples demonstrating core widget usage.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Import widgets from the library
from ..cards import InfoCardWidget, ProfileCardWidget, StatCardWidget
from ..base import BaseButton, ThemeManager
from ..feedback import show_success_toast, StatusChipWidget, BadgeLabel


class BasicExamplesWindow(QMainWindow):
    """Main window showcasing basic widget examples."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Widgets Library - Basic Examples")
        self.setGeometry(100, 100, 1000, 700)

        # Setup UI
        self._setup_ui()

    def _setup_ui(self):
        """Setup the main UI."""
        # Central widget with scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Main content widget
        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Add example sections
        self._add_button_examples(main_layout)
        self._add_card_examples(main_layout)
        self._add_feedback_examples(main_layout)

        scroll_area.setWidget(content_widget)
        self.setCentralWidget(scroll_area)

    def _add_button_examples(self, layout):
        """Add button examples."""
        from PyQt6.QtWidgets import QLabel, QGroupBox

        group = QGroupBox("Button Examples")
        group_layout = QVBoxLayout(group)

        # Button variants
        buttons_layout = QHBoxLayout()

        primary_btn = BaseButton("Primary", "primary", "medium")
        primary_btn.clicked.connect(lambda: show_success_toast("Primary button clicked!"))
        buttons_layout.addWidget(primary_btn)

        secondary_btn = BaseButton("Secondary", "secondary", "medium")
        secondary_btn.clicked.connect(lambda: show_success_toast("Secondary button clicked!"))
        buttons_layout.addWidget(secondary_btn)

        destructive_btn = BaseButton("Destructive", "destructive", "medium")
        destructive_btn.clicked.connect(lambda: show_success_toast("Destructive button clicked!"))
        buttons_layout.addWidget(destructive_btn)

        ghost_btn = BaseButton("Ghost", "ghost", "medium")
        ghost_btn.clicked.connect(lambda: show_success_toast("Ghost button clicked!"))
        buttons_layout.addWidget(ghost_btn)

        buttons_layout.addStretch()
        group_layout.addLayout(buttons_layout)

        # Button sizes
        sizes_layout = QHBoxLayout()

        small_btn = BaseButton("Small", "primary", "small")
        sizes_layout.addWidget(small_btn)

        medium_btn = BaseButton("Medium", "primary", "medium")
        sizes_layout.addWidget(medium_btn)

        large_btn = BaseButton("Large", "primary", "large")
        sizes_layout.addWidget(large_btn)

        sizes_layout.addStretch()
        group_layout.addLayout(sizes_layout)

        layout.addWidget(group)

    def _add_card_examples(self, layout):
        """Add card examples."""
        from PyQt6.QtWidgets import QGroupBox

        group = QGroupBox("Card Examples")
        group_layout = QHBoxLayout(group)

        # Info card
        info_card = InfoCardWidget(
            title="Welcome",
            subtitle="Getting Started",
            description="This is an example of an info card widget with title, subtitle, and description."
        )
        group_layout.addWidget(info_card)

        # Profile card
        profile_card = ProfileCardWidget(
            name="John Doe",
            role="Software Engineer",
            email="john.doe@example.com"
        )
        profile_card.add_action_button("View Profile", "view_profile")
        profile_card.add_action_button("Send Message", "send_message", "secondary")
        group_layout.addWidget(profile_card)

        # Stat card
        stat_card = StatCardWidget(
            label="Total Users",
            value="1,234",
            unit="users",
            trend="up",
            trend_value="+12%"
        )
        group_layout.addWidget(stat_card)

        group_layout.addStretch()
        layout.addWidget(group)

    def _add_feedback_examples(self, layout):
        """Add feedback widget examples."""
        from PyQt6.QtWidgets import QGroupBox

        group = QGroupBox("Feedback Examples")
        group_layout = QVBoxLayout(group)

        # Status chips
        chips_layout = QHBoxLayout()

        active_chip = StatusChipWidget("Active", "success", "medium")
        chips_layout.addWidget(active_chip)

        pending_chip = StatusChipWidget("Pending", "warning", "medium")
        chips_layout.addWidget(pending_chip)

        error_chip = StatusChipWidget("Error", "error", "medium")
        chips_layout.addWidget(error_chip)

        chips_layout.addStretch()
        group_layout.addLayout(chips_layout)

        # Badge labels
        badges_layout = QHBoxLayout()

        messages_badge = BadgeLabel("Messages", 5, "primary")
        badges_layout.addWidget(messages_badge)

        notifications_badge = BadgeLabel("Notifications", 12, "error")
        badges_layout.addWidget(notifications_badge)

        tasks_badge = BadgeLabel("Tasks", 0, "secondary", show_zero=True)
        badges_layout.addWidget(tasks_badge)

        badges_layout.addStretch()
        group_layout.addLayout(badges_layout)

        layout.addWidget(group)


def run_basic_examples():
    """Run the basic examples application."""
    app = QApplication(sys.argv)

    # Apply theme
    from ..base.theme_manager import theme_manager
    app.setStyleSheet(theme_manager.get_stylesheet())

    window = BasicExamplesWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    run_basic_examples()