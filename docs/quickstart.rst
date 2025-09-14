Quick Start Guide
=================

This guide will help you get started with the PyQt6 Widgets Library in just a few minutes.

Basic Example
-------------

Here's a simple example that demonstrates how to use the library:

.. code-block:: python

    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    from pyqt_widgets import InfoCardWidget, BaseButton, theme_manager

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("PyQt6 Widgets Demo")
            self.setGeometry(100, 100, 800, 600)

            # Central widget
            central_widget = QWidget()
            layout = QVBoxLayout(central_widget)

            # Add an info card
            card = InfoCardWidget(
                title="Welcome to PyQt6 Widgets!",
                subtitle="Getting Started",
                description="This library provides 50+ polished widgets for your desktop applications."
            )
            layout.addWidget(card)

            # Add a styled button
            button = BaseButton("Click Me!", "primary", "medium")
            button.clicked.connect(self.on_button_clicked)
            layout.addWidget(button)

            self.setCentralWidget(central_widget)

        def on_button_clicked(self):
            print("Button clicked!")

    if __name__ == "__main__":
        app = QApplication(sys.argv)

        # Apply the theme
        app.setStyleSheet(theme_manager.get_stylesheet())

        window = MainWindow()
        window.show()

        sys.exit(app.exec())

Key Concepts
------------

Theme Management
~~~~~~~~~~~~~~~~

The library includes a powerful theming system:

.. code-block:: python

    from pyqt_widgets import theme_manager

    # Switch to dark theme
    theme_manager.set_theme("dark")
    app.setStyleSheet(theme_manager.get_stylesheet())

    # Get theme colors
    primary_color = theme_manager.get_color("primary")
    background_color = theme_manager.get_color("background")

Widget Categories
~~~~~~~~~~~~~~~~~

Widgets are organized into logical categories:

.. code-block:: python

    # Cards
    from pyqt_widgets.cards import InfoCardWidget, ProfileCardWidget, StatCardWidget

    # Navigation
    from pyqt_widgets.navigation import SidebarNavWidget, TabBarWidget

    # Forms
    from pyqt_widgets.forms import SearchBoxWithSuggestions, TagInputWidget

    # Data visualization
    from pyqt_widgets.data import DataTableWidget, KanbanBoardWidget

Common Patterns
---------------

Creating a Dashboard
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from PyQt6.QtWidgets import QGridLayout
    from pyqt_widgets.cards import StatCardWidget
    from pyqt_widgets.data import MiniChartCard

    # Create a grid layout for dashboard
    grid_layout = QGridLayout()

    # Add stat cards
    users_card = StatCardWidget(number=1250, label="Active Users", trend="up")
    revenue_card = StatCardWidget(number=45000, label="Revenue", trend="up")
    orders_card = StatCardWidget(number=89, label="Orders", trend="down")

    grid_layout.addWidget(users_card, 0, 0)
    grid_layout.addWidget(revenue_card, 0, 1)
    grid_layout.addWidget(orders_card, 0, 2)

    # Add a chart
    chart_data = [10, 25, 15, 30, 20, 35, 25]
    chart_card = MiniChartCard(data=chart_data, title="Weekly Sales")
    grid_layout.addWidget(chart_card, 1, 0, 1, 3)

Building a User Interface
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pyqt_widgets.navigation import SidebarNavWidget
    from pyqt_widgets.user import UserAvatarWidget
    from pyqt_widgets.feedback import NotificationToastWidget

    # Create sidebar navigation
    sidebar = SidebarNavWidget(items=[
        {"text": "Dashboard", "icon": "dashboard"},
        {"text": "Users", "icon": "users"},
        {"text": "Settings", "icon": "settings"}
    ])

    # Add user avatar
    avatar = UserAvatarWidget(
        image_path="user.png",
        initials="JD",
        size=40
    )

    # Show notification
    toast = NotificationToastWidget(
        message="Settings saved successfully!",
        type="success",
        duration=3000
    )
    toast.show()

Form Creation
~~~~~~~~~~~~~

.. code-block:: python

    from pyqt_widgets.forms import TagInputWidget, DateRangePickerWidget, ToggleSwitchWidget

    # Multi-tag input
    tags = TagInputWidget(
        placeholder="Add tags...",
        suggestions=["Python", "PyQt6", "Desktop", "GUI"]
    )

    # Date range picker
    date_picker = DateRangePickerWidget()

    # Toggle switch
    notifications_toggle = ToggleSwitchWidget(
        label="Enable Notifications",
        state=True
    )

Next Steps
----------

1. Explore the :doc:`api/index` for detailed widget documentation
2. Check out :doc:`examples/index` for more complex examples
3. Learn about :doc:`theming` to customize the appearance
4. See :doc:`contributing` if you want to contribute to the project

Demo Applications
-----------------

Run the included demo applications to see widgets in action:

.. code-block:: bash

    # Basic widget showcase
    pyqt6-widgets-demo

    # Card widgets showcase
    pyqt6-cards-showcase

These demos provide interactive examples of all available widgets and their configurations.