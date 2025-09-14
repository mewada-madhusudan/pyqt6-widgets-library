"""
Comprehensive showcase of all card widgets.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QGridLayout
from PyQt6.QtCore import Qt

from ..cards import (
    InfoCardWidget, ProfileCardWidget, StatCardWidget, ExpandableCardWidget,
    HoverActionCardWidget, ImageCardWidget, SelectableCardWidget
)
from ..base.theme_manager import theme_manager


class CardShowcaseWindow(QMainWindow):
    """Showcase window for all card widgets."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Widgets Library - Card Showcase")
        self.setGeometry(100, 100, 1200, 800)

        self._setup_ui()

    def _setup_ui(self):
        """Setup the showcase UI."""
        # Central widget with scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Main content widget
        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Add card sections
        self._add_info_cards(main_layout)
        self._add_profile_cards(main_layout)
        self._add_stat_cards(main_layout)
        self._add_interactive_cards(main_layout)

        scroll_area.setWidget(content_widget)
        self.setCentralWidget(scroll_area)

    def _add_info_cards(self, layout):
        """Add info card examples."""
        from PyQt6.QtWidgets import QLabel

        # Section title
        title = QLabel("Info Cards")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {theme_manager.get_color('text')};
                margin-bottom: 10px;
            }}
        """)
        layout.addWidget(title)

        # Cards grid
        cards_layout = QGridLayout()

        # Basic info card
        basic_card = InfoCardWidget(
            title="Project Overview",
            subtitle="Development Status",
            description="This project is currently in active development with 85% completion rate."
        )
        cards_layout.addWidget(basic_card, 0, 0)

        # Info card with icon
        icon_card = InfoCardWidget(
            title="System Health",
            subtitle="All systems operational",
            description="All services are running normally with no reported issues.",
            icon="✅"
        )
        cards_layout.addWidget(icon_card, 0, 1)

        # Metric info card
        from ..cards.info_card import MetricInfoCard
        metric_card = MetricInfoCard(
            title="Revenue",
            value="$45,231",
            unit="USD",
            change="+15.3%"
        )
        cards_layout.addWidget(metric_card, 0, 2)

        layout.addLayout(cards_layout)

    def _add_profile_cards(self, layout):
        """Add profile card examples."""
        from PyQt6.QtWidgets import QLabel

        # Section title
        title = QLabel("Profile Cards")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {theme_manager.get_color('text')};
                margin-bottom: 10px;
            }}
        """)
        layout.addWidget(title)

        # Cards grid
        cards_layout = QGridLayout()

        # Standard profile card
        profile_card = ProfileCardWidget(
            name="Alice Johnson",
            role="UX Designer",
            email="alice.johnson@company.com"
        )
        profile_card.add_action_button("View Profile", "view")
        profile_card.add_action_button("Message", "message", "secondary")
        cards_layout.addWidget(profile_card, 0, 0)

        # Compact profile card
        from ..cards.profile_card import CompactProfileCard
        compact_card = CompactProfileCard(
            name="Bob Smith",
            role="Developer"
        )
        cards_layout.addWidget(compact_card, 0, 1)

        # Team member card with status
        from ..cards.profile_card import TeamMemberCard
        team_card = TeamMemberCard(
            name="Carol Davis",
            role="Project Manager",
            status="online"
        )
        cards_layout.addWidget(team_card, 0, 2)

        layout.addLayout(cards_layout)

    def _add_stat_cards(self, layout):
        """Add statistics card examples."""
        from PyQt6.QtWidgets import QLabel

        # Section title
        title = QLabel("Statistics Cards")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {theme_manager.get_color('text')};
                margin-bottom: 10px;
            }}
        """)
        layout.addWidget(title)

        # Cards grid
        cards_layout = QGridLayout()

        # Basic stat card
        users_card = StatCardWidget(
            label="Total Users",
            value="12,345",
            trend="up",
            trend_value="+8.2%"
        )
        cards_layout.addWidget(users_card, 0, 0)

        # Revenue stat card
        revenue_card = StatCardWidget(
            label="Monthly Revenue",
            value="$54,321",
            unit="USD",
            trend="up",
            trend_value="+12.5%"
        )
        cards_layout.addWidget(revenue_card, 0, 1)

        # Progress stat card
        from ..cards.stat_card import ProgressStatCard
        progress_card = ProgressStatCard(
            label="Project Progress",
            value="75",
            max_value="100",
            unit="%"
        )
        cards_layout.addWidget(progress_card, 0, 2)

        layout.addLayout(cards_layout)

    def _add_interactive_cards(self, layout):
        """Add interactive card examples."""
        from PyQt6.QtWidgets import QLabel

        # Section title
        title = QLabel("Interactive Cards")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {theme_manager.get_color('text')};
                margin-bottom: 10px;
            }}
        """)
        layout.addWidget(title)

        # Cards grid
        cards_layout = QGridLayout()

        # Expandable card
        expandable_card = ExpandableCardWidget(
            title="Expandable Content",
            expanded=False
        )
        from PyQt6.QtWidgets import QLabel as ContentLabel
        content_label = ContentLabel("This is the expandable content that can be shown or hidden.")
        content_label.setWordWrap(True)
        expandable_card.set_content(content_label)
        cards_layout.addWidget(expandable_card, 0, 0)

        # Hover action card
        hover_card = HoverActionCardWidget(
            title="Hover for Actions",
            subtitle="Move your mouse over this card to see action buttons appear."
        )
        hover_card.add_action("Edit", "edit")
        hover_card.add_action("Delete", "delete", "destructive")
        hover_card.add_action("Share", "share", "secondary")
        cards_layout.addWidget(hover_card, 0, 1)

        # Selectable card
        selectable_card = SelectableCardWidget(
            title="Selectable Card",
            subtitle="Click to select this card",
            selectable=True
        )
        cards_layout.addWidget(selectable_card, 0, 2)

        layout.addLayout(cards_layout)


def run_card_showcase():
    """Run the card showcase application."""
    app = QApplication(sys.argv)

    # Apply theme
    app.setStyleSheet(theme_manager.get_stylesheet())

    window = CardShowcaseWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    run_card_showcase()