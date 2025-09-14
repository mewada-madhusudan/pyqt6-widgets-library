Changelog
=========

All notable changes to the PyQt6 Widgets Library will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------

Added
~~~~~
- Comprehensive documentation with Sphinx
- API reference documentation
- Confluence-style installation guide
- Contributing guidelines
- Code of conduct

Changed
~~~~~~~
- Improved theme management system
- Enhanced widget base classes
- Better error handling across widgets

[1.1.0] - 2024-09-14
---------------------

Added
~~~~~
- **New Widget Categories:**
  - Cards: InfoCardWidget, ProfileCardWidget, StatCardWidget, ExpandableCardWidget, HoverActionCardWidget, ImageCardWidget, SelectableCardWidget
  - Navigation: SidebarNavWidget, BreadcrumbBarWidget, TabBarWidget, AccordionMenuWidget, CommandPaletteWidget, PaginationWidget, DockablePanelWidget
  - Feedback: NotificationToastWidget, SnackbarWidget, StatusChipWidget, BadgeLabel, ProgressOverlayWidget, TooltipWidget, EmptyStateWidget
  - Data: DataTableWidget, TimelineWidget, KanbanBoardWidget, PropertyGridWidget, MiniChartCard, TreeViewWidget, FileExplorerWidget
  - User: UserAvatarWidget, UserListItemWidget, ChatBubbleWidget, CommentThreadWidget, RatingStarWidget, ReactionBarWidget, ProfileHeaderWidget
  - Forms: SearchBoxWithSuggestions, InlineEditLabel, TagInputWidget, RichTextEditorWidget, FormStepperWidget, DateRangePickerWidget, ToggleSwitchWidget, SliderWithInputWidget
  - Utility: FloatingActionButton, QuickSettingsPanel, PinnedNoteWidget, ClipboardHistoryWidget, GlobalSearchWidget, ShortcutHelperWidget

- **Base Components:**
  - BaseCardWidget with theming and animation support
  - BasePopupWidget for overlays and modals
  - BaseButton with multiple variants and states
  - ThemeManager for centralized styling
  - AnimationHelpers for smooth transitions

- **Theme System:**
  - Built-in light and dark themes
  - Custom theme support
  - Dynamic theme switching
  - CSS-like styling system

- **Examples and Demos:**
  - Basic widget showcase application
  - Card widgets demonstration
  - Interactive examples for all categories

- **Development Tools:**
  - pytest configuration for testing
  - black for code formatting
  - mypy for type checking
  - flake8 for linting
  - pre-commit hooks

Changed
~~~~~~~
- Improved package structure with logical categorization
- Enhanced widget APIs with consistent parameter naming
- Better signal handling across all widgets
- Optimized performance for large datasets

Fixed
~~~~~
- Memory leaks in animation system
- Theme switching edge cases
- Widget sizing issues on different platforms

[1.0.0] - 2024-08-15
---------------------

Added
~~~~~
- Initial release of PyQt6 Widgets Library
- Basic widget implementations
- Core theming system
- Package configuration and setup

Features
~~~~~~~~
- 20+ initial widgets across 4 categories
- Basic light/dark theme support
- Simple animation system
- Cross-platform compatibility

[0.9.0-beta] - 2024-07-20
--------------------------

Added
~~~~~
- Beta release for testing
- Core widget framework
- Basic documentation
- Example applications

[0.1.0-alpha] - 2024-06-01
---------------------------

Added
~~~~~
- Project initialization
- Basic project structure
- Initial widget prototypes
- Development environment setup

Migration Guide
---------------

From 1.0.x to 1.1.x
~~~~~~~~~~~~~~~~~~~

**Breaking Changes:**
- Widget import paths have changed to use category-based structure
- Theme API has been redesigned for better flexibility

**Before (1.0.x):**

.. code-block:: python

    from pyqt_widgets import InfoCard, BaseTheme

    card = InfoCard("Title", "Description")
    theme = BaseTheme("dark")

**After (1.1.x):**

.. code-block:: python

    from pyqt_widgets.cards import InfoCardWidget
    from pyqt_widgets import theme_manager

    card = InfoCardWidget("Title", description="Description")
    theme_manager.set_theme("dark")

**New Features:**
- All widgets now support consistent theming
- Enhanced animation system
- Improved signal handling
- Better documentation and examples

**Deprecated:**
- Old theme classes (use ThemeManager instead)
- Direct widget imports from root package (use category imports)

Upgrade Instructions
~~~~~~~~~~~~~~~~~~~

1. Update import statements to use category-based imports
2. Replace old theme initialization with ThemeManager
3. Update widget instantiation to use new parameter names
4. Test your application with the new theme system

**Automatic Migration:**

We provide a migration script to help update your code:

.. code-block:: bash

    python -m pyqt_widgets.migrate --input your_app.py --output your_app_updated.py

Support for Legacy Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **1.0.x**: Security fixes only until 2025-01-01
- **0.9.x**: No longer supported
- **0.1.x**: No longer supported

For critical applications, we recommend upgrading to 1.1.x as soon as possible.

Future Roadmap
--------------

[1.2.0] - Planned for 2024-12-01
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **New Widgets:**
  - Advanced chart widgets with plotting capabilities
  - Video player widget with controls
  - Code editor widget with syntax highlighting
  - Calendar and scheduler widgets

- **Enhanced Features:**
  - Improved accessibility support (ARIA labels, keyboard navigation)
  - Better high-DPI display support
  - Performance optimizations for large datasets
  - Mobile-responsive design patterns

- **Developer Experience:**
  - Widget designer tool for visual development
  - Better debugging tools and logging
  - Enhanced documentation with interactive examples
  - Plugin system for third-party widgets

[1.3.0] - Planned for 2025-03-01
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Advanced Features:**
  - 3D visualization widgets
  - Advanced animation and transition system
  - Internationalization (i18n) support
  - Advanced theming with CSS-in-Python

- **Integration:**
  - Better integration with popular Python frameworks
  - Export to web components
  - Integration with design systems (Material Design, Fluent UI)

[2.0.0] - Planned for 2025-06-01
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Major Overhaul:**
  - PyQt6.5+ support with latest features
  - Redesigned API for better consistency
  - Performance improvements and memory optimization
  - Modern Python features (3.10+ type hints, pattern matching)

- **Breaking Changes:**
  - Simplified widget hierarchy
  - New theming system architecture
  - Updated signal/slot patterns
  - Modern packaging and distribution

Contributing to Roadmap
~~~~~~~~~~~~~~~~~~~~~~~

We welcome community input on our roadmap! Please:

1. Open GitHub issues for feature requests
2. Participate in roadmap discussions
3. Vote on proposed features
4. Contribute implementations for planned features

Stay updated with our progress by:

- Following our GitHub repository
- Joining our community discussions
- Subscribing to release notifications
- Reading our development blog posts