Navigation API
==============

Navigation widgets help users move through your application efficiently. All navigation widgets support theming, keyboard navigation, and accessibility features.

.. currentmodule:: pyqt_widgets.navigation

SidebarNavWidget
----------------

.. autoclass:: SidebarNavWidget
   :members:
   :inherited-members:

A collapsible sidebar navigation with icons, grouping, and hierarchical menus.

**Parameters:**
    * ``items`` (list) - Navigation items configuration
    * ``collapsible`` (bool) - Whether sidebar can be collapsed
    * ``width`` (int) - Sidebar width in pixels
    * ``theme`` (str) - Theme variant

**Example:**

.. code-block:: python

    from pyqt_widgets.navigation import SidebarNavWidget

    sidebar = SidebarNavWidget(
        items=[
            {"text": "Dashboard", "icon": "dashboard", "callback": self.show_dashboard},
            {"text": "Users", "icon": "users", "callback": self.show_users},
            {"separator": True},
            {"text": "Settings", "icon": "settings", "callback": self.show_settings}
        ],
        collapsible=True,
        width=250
    )

**Signals:**
    * ``item_clicked(item_id)`` - Emitted when navigation item is clicked
    * ``collapsed_changed(collapsed)`` - Emitted when sidebar is collapsed/expanded

BreadcrumbBarWidget
-------------------

.. autoclass:: BreadcrumbBarWidget
   :members:
   :inherited-members:

Displays hierarchical navigation path with clickable segments.

**Parameters:**
    * ``paths`` (list) - List of path segments
    * ``separator`` (str) - Path separator character
    * ``max_items`` (int) - Maximum visible items before truncation

**Example:**

.. code-block:: python

    from pyqt_widgets.navigation import BreadcrumbBarWidget

    breadcrumbs = BreadcrumbBarWidget(
        paths=["Home", "Projects", "Web App", "Components"],
        separator=" › ",
        max_items=4
    )

    breadcrumbs.path_clicked.connect(self.navigate_to_path)

TabBarWidget
------------

.. autoclass:: TabBarWidget
   :members:
   :inherited-members:

Modern tab bar with closeable tabs, overflow handling, and drag reordering.

**Parameters:**
    * ``tabs`` (list) - Tab configurations
    * ``closeable`` (bool) - Whether tabs can be closed
    * ``reorderable`` (bool) - Whether tabs can be reordered
    * ``overflow_mode`` (str) - "scroll" or "dropdown"

**Example:**

.. code-block:: python

    from pyqt_widgets.navigation import TabBarWidget

    tabs = TabBarWidget(
        tabs=[
            {"text": "Overview", "closeable": False, "icon": "home"},
            {"text": "Details", "closeable": True, "icon": "info"},
            {"text": "Settings", "closeable": True, "icon": "settings"}
        ],
        reorderable=True,
        overflow_mode="scroll"
    )

**Signals:**
    * ``tab_clicked(index)`` - Emitted when tab is clicked
    * ``tab_closed(index)`` - Emitted when tab is closed
    * ``tab_reordered(old_index, new_index)`` - Emitted when tab is moved

AccordionMenuWidget
-------------------

.. autoclass:: AccordionMenuWidget
   :members:
   :inherited-members:

Collapsible menu sections with smooth animations.

**Parameters:**
    * ``sections`` (dict) - Menu sections and items
    * ``allow_multiple`` (bool) - Allow multiple sections open
    * ``animate`` (bool) - Enable expand/collapse animations

**Example:**

.. code-block:: python

    from pyqt_widgets.navigation import AccordionMenuWidget

    accordion = AccordionMenuWidget(
        sections={
            "File Operations": [
                {"text": "New File", "icon": "file-plus", "callback": self.new_file},
                {"text": "Open File", "icon": "folder-open", "callback": self.open_file}
            ],
            "Edit Operations": [
                {"text": "Cut", "icon": "scissors", "callback": self.cut},
                {"text": "Copy", "icon": "copy", "callback": self.copy}
            ]
        },
        allow_multiple=False
    )

CommandPaletteWidget
--------------------

.. autoclass:: CommandPaletteWidget
   :members:
   :inherited-members:

Searchable command interface similar to VS Code's command palette.

**Parameters:**
    * ``actions`` (list) - Available actions/commands
    * ``placeholder`` (str) - Search input placeholder
    * ``max_results`` (int) - Maximum results to display

**Example:**

.. code-block:: python

    from pyqt_widgets.navigation import CommandPaletteWidget

    palette = CommandPaletteWidget(
        actions=[
            {"text": "Open File", "description": "Open a file", "callback": self.open_file},
            {"text": "Save File", "description": "Save current file", "callback": self.save_file},
            {"text": "Toggle Theme", "description": "Switch between light/dark", "callback": self.toggle_theme}
        ],
        placeholder="Type a command...",
        max_results=10
    )

    # Show palette with keyboard shortcut
    palette.show_palette()

PaginationWidget
----------------

.. autoclass:: PaginationWidget
   :members:
   :inherited-members:

Flexible pagination with multiple display modes.

**Parameters:**
    * ``total_pages`` (int) - Total number of pages
    * ``current_page`` (int) - Current active page
    * ``mode`` (str) - "numeric", "simple", or "load_more"
    * ``page_size`` (int) - Items per page

**Example:**

.. code-block:: python

    from pyqt_widgets.navigation import PaginationWidget

    # Numeric pagination
    pagination = PaginationWidget(
        total_pages=25,
        current_page=1,
        mode="numeric",
        page_size=20
    )

    pagination.page_changed.connect(self.load_page)

**Signals:**
    * ``page_changed(page)`` - Emitted when page is changed
    * ``page_size_changed(size)`` - Emitted when page size changes

DockablePanelWidget
-------------------

.. autoclass:: DockablePanelWidget
   :members:
   :inherited-members:

Detachable, draggable panel that can float or dock.

**Parameters:**
    * ``title`` (str) - Panel title
    * ``dockable`` (bool) - Whether panel can be docked
    * ``closeable`` (bool) - Whether panel can be closed
    * ``resizable`` (bool) - Whether panel can be resized

**Example:**

.. code-block:: python

    from pyqt_widgets.navigation import DockablePanelWidget
    from PyQt6.QtWidgets import QTextEdit

    # Create dockable console panel
    console_panel = DockablePanelWidget(
        title="Console Output",
        dockable=True,
        closeable=True
    )

    # Add content to panel
    console_text = QTextEdit()
    console_panel.set_content(console_text)

**Signals:**
    * ``docked_changed(docked)`` - Emitted when dock state changes
    * ``panel_closed()`` - Emitted when panel is closed

Navigation Patterns
-------------------

Multi-Level Navigation
~~~~~~~~~~~~~~~~~~~~~~

Combine navigation widgets for complex hierarchies:

.. code-block:: python

    class NavigationManager:
        def __init__(self):
            # Main sidebar
            self.sidebar = SidebarNavWidget(items=self.get_main_nav())

            # Breadcrumbs for current location
            self.breadcrumbs = BreadcrumbBarWidget()

            # Tabs for sub-sections
            self.tabs = TabBarWidget()

            # Connect navigation events
            self.sidebar.item_clicked.connect(self.on_nav_item_clicked)
            self.breadcrumbs.path_clicked.connect(self.on_breadcrumb_clicked)

        def navigate_to(self, path_segments):
            # Update breadcrumbs
            self.breadcrumbs.set_paths(path_segments)

            # Update tabs based on current section
            section_tabs = self.get_tabs_for_section(path_segments[-1])
            self.tabs.set_tabs(section_tabs)

Responsive Navigation
~~~~~~~~~~~~~~~~~~~~

Adapt navigation to different screen sizes:

.. code-block:: python

    class ResponsiveNavigation(QWidget):
        def __init__(self):
            super().__init__()
            self.setup_ui()

        def setup_ui(self):
            # Desktop: full sidebar
            self.sidebar = SidebarNavWidget(width=250)

            # Mobile: collapsible hamburger menu
            self.mobile_menu = AccordionMenuWidget()

            # Responsive switching
            self.update_navigation_mode()

        def resizeEvent(self, event):
            super().resizeEvent(event)
            self.update_navigation_mode()

        def update_navigation_mode(self):
            if self.width() < 768:  # Mobile breakpoint
                self.sidebar.hide()
                self.mobile_menu.show()
            else:  # Desktop
                self.sidebar.show()
                self.mobile_menu.hide()

Keyboard Navigation
~~~~~~~~~~~~~~~~~~

All navigation widgets support keyboard shortcuts:

.. code-block:: python

    # Enable keyboard navigation
    sidebar.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    # Custom keyboard shortcuts
    def setup_shortcuts(self):
        # Ctrl+K for command palette
        palette_shortcut = QShortcut(QKeySequence("Ctrl+K"), self)
        palette_shortcut.activated.connect(self.show_command_palette)

        # Ctrl+Tab for tab switching
        next_tab_shortcut = QShortcut(QKeySequence("Ctrl+Tab"), self)
        next_tab_shortcut.activated.connect(self.next_tab)

Accessibility Features
---------------------

Navigation widgets include comprehensive accessibility support:

**Screen Reader Support:**
    * ARIA labels for all interactive elements
    * Proper focus management
    * Semantic HTML structure

**Keyboard Navigation:**
    * Tab order follows logical flow
    * Arrow keys for menu navigation
    * Enter/Space for activation
    * Escape for closing/canceling

**High Contrast Support:**
    * Respects system high contrast settings
    * Sufficient color contrast ratios
    * Focus indicators clearly visible

**Example Accessibility Setup:**

.. code-block:: python

    # Enable accessibility features
    sidebar.setAccessibleName("Main Navigation")
    sidebar.setAccessibleDescription("Navigate between application sections")

    # Set ARIA roles
    for item in sidebar.get_items():
        item.setAccessibleRole(QAccessible.Role.MenuItem)
        item.setAccessibleName(item.text())