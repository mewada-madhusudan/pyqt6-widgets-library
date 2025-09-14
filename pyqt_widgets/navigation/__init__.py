"""Navigation widgets for PyQt6 library."""

from .sidebar_nav import SidebarNavWidget
from .breadcrumb_bar import BreadcrumbBarWidget
from .tab_bar import TabBarWidget
from .accordion_menu import AccordionMenuWidget
from .command_palette import CommandPaletteWidget
from .pagination import PaginationWidget
from .dockable_panel import DockablePanelWidget

__all__ = [
    'SidebarNavWidget',
    'BreadcrumbBarWidget',
    'TabBarWidget',
    'AccordionMenuWidget',
    'CommandPaletteWidget',
    'PaginationWidget',
    'DockablePanelWidget'
]