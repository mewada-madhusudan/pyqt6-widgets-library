API Reference
=============

This section provides detailed documentation for all widgets and components in the PyQt6 Widgets Library.

.. toctree::
   :maxdepth: 2

   base
   cards
   navigation
   feedback
   data
   user
   forms
   utility

Base Components
---------------

The library is built on a foundation of reusable base components that provide common functionality:

* :class:`~pyqt_widgets.base.BaseCardWidget` - Foundation for all card widgets
* :class:`~pyqt_widgets.base.BasePopupWidget` - Base for overlays and popups
* :class:`~pyqt_widgets.base.BaseButton` - Enhanced button with variants and states
* :class:`~pyqt_widgets.base.ThemeManager` - Centralized styling management
* :class:`~pyqt_widgets.base.AnimationHelpers` - Smooth transitions and effects

Widget Categories
-----------------

Cards (:doc:`cards`)
    Information display, profile cards, statistics, expandable content

Navigation (:doc:`navigation`)
    Sidebar, breadcrumbs, tabs, command palette, pagination

Feedback & Information (:doc:`feedback`)
    Notifications, status indicators, progress, tooltips

Data & Visualization (:doc:`data`)
    Tables, timelines, kanban boards, charts, file explorers

User & Social (:doc:`user`)
    Avatars, chat bubbles, ratings, profiles, comments

Forms & Input (:doc:`forms`)
    Search, inline editing, tags, rich text, form wizards

Utility (:doc:`utility`)
    Floating actions, settings panels, notes, shortcuts

Common Parameters
-----------------

Many widgets share common parameters:

**Styling Parameters:**
    * ``theme`` - Theme variant ("light", "dark", or custom)
    * ``size`` - Size variant ("small", "medium", "large")
    * ``variant`` - Style variant (e.g., "primary", "secondary", "success")

**Behavioral Parameters:**
    * ``enabled`` - Whether the widget is interactive
    * ``visible`` - Whether the widget is visible
    * ``tooltip`` - Tooltip text to display on hover

**Animation Parameters:**
    * ``animated`` - Whether to use animations
    * ``duration`` - Animation duration in milliseconds
    * ``easing`` - Animation easing curve

Usage Patterns
--------------

**Importing Widgets:**

.. code-block:: python

    # Import specific widgets
    from pyqt_widgets.cards import InfoCardWidget
    from pyqt_widgets.navigation import SidebarNavWidget

    # Import entire categories
    from pyqt_widgets import cards, navigation

    # Import commonly used components
    from pyqt_widgets import theme_manager, BaseButton

**Widget Lifecycle:**

.. code-block:: python

    # Create widget
    widget = InfoCardWidget(title="Example", description="Description")

    # Configure widget
    widget.set_theme("dark")
    widget.set_size("large")

    # Connect signals
    widget.clicked.connect(self.on_widget_clicked)

    # Add to layout
    layout.addWidget(widget)

**Theme Integration:**

.. code-block:: python

    # Apply global theme
    app.setStyleSheet(theme_manager.get_stylesheet())

    # Get theme colors for custom styling
    primary = theme_manager.get_color("primary")
    widget.setStyleSheet(f"background-color: {primary};")