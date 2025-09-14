# PyQt6 Widgets Library - Installation and Usage Guide

## Overview

The PyQt6 Widgets Library is a comprehensive collection of **50+ polished, reusable PyQt6 widgets** designed for building modern desktop applications with consistent UI/UX. This guide covers installation, basic usage, and widget examples.

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- PyQt6 6.4.0 or higher

### Method 1: Install from PyPI (Recommended)

```bash
pip install pyqt6-widgets-library
```

### Method 2: Install from Wheel Package

If you have the wheel file:

```bash
pip install pyqt6_widgets_library-1.1.0-py3-none-any.whl
```

### Method 3: Install from Source

```bash
git clone https://github.com/madhusudanmewada/pyqt6-widgets-library.git
cd pyqt6-widgets-library
pip install -e .
```

### Development Installation

For contributors or advanced users:

```bash
pip install -e ".[dev]"
```

This includes additional tools:
- pytest (testing)
- black (code formatting)
- mypy (type checking)
- flake8 (linting)

---

## ✅ Verify Installation

Test your installation:

```python
import pyqt_widgets
print("PyQt6 Widgets Library installed successfully!")
```

Or run the demo:

```bash
pyqt6-widgets-demo
```

---

## 🚀 Quick Start

### Basic Application

```python
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
        
        # Add widgets
        card = InfoCardWidget(
            title="Welcome!",
            subtitle="Getting Started", 
            description="This is your first PyQt6 widget!"
        )
        layout.addWidget(card)
        
        button = BaseButton("Click Me!", "primary", "medium")
        layout.addWidget(button)
        
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(theme_manager.get_stylesheet())
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
```

---

## 📚 Widget Categories

### 🃏 Cards

Display information in structured, visually appealing formats.

#### InfoCardWidget
```python
from pyqt_widgets.cards import InfoCardWidget

card = InfoCardWidget(
    title="Total Users",
    subtitle="Active this month", 
    description="1,250 users (+15% from last month)"
)
```

#### ProfileCardWidget
```python
from pyqt_widgets.cards import ProfileCardWidget

profile = ProfileCardWidget(
    name="Alice Johnson",
    role="Senior Designer",
    avatar="path/to/avatar.png"
)
```

#### StatCardWidget
```python
from pyqt_widgets.cards import StatCardWidget

stat = StatCardWidget(
    number=45230,
    label="Revenue",
    trend="up",
    percentage=12.5
)
```

### 🧭 Navigation

Navigate through your application with style.

#### SidebarNavWidget
```python
from pyqt_widgets.navigation import SidebarNavWidget

sidebar = SidebarNavWidget(items=[
    {"text": "Dashboard", "icon": "dashboard"},
    {"text": "Users", "icon": "users"},
    {"text": "Settings", "icon": "settings"}
])
```

#### BreadcrumbBarWidget
```python
from pyqt_widgets.navigation import BreadcrumbBarWidget

breadcrumbs = BreadcrumbBarWidget(
    paths=["Home", "Projects", "Project Alpha"]
)
```

#### TabBarWidget
```python
from pyqt_widgets.navigation import TabBarWidget

tabs = TabBarWidget(tabs=[
    {"text": "Overview", "closeable": False},
    {"text": "Details", "closeable": True},
    {"text": "Settings", "closeable": True}
])
```

### 💬 Feedback & Information

Provide user feedback and display status information.

#### NotificationToastWidget
```python
from pyqt_widgets.feedback import NotificationToastWidget

toast = NotificationToastWidget(
    message="Settings saved successfully!",
    type="success",
    duration=3000
)
toast.show()
```

#### StatusChipWidget
```python
from pyqt_widgets.feedback import StatusChipWidget

status = StatusChipWidget(
    text="Active",
    color="green"
)
```

#### ProgressOverlayWidget
```python
from pyqt_widgets.feedback import ProgressOverlayWidget

overlay = ProgressOverlayWidget(
    message="Loading data...",
    progress=75
)
```

### 📊 Data & Visualization

Display and interact with data effectively.

#### DataTableWidget
```python
from pyqt_widgets.data import DataTableWidget

table = DataTableWidget(
    columns=["Name", "Email", "Role"],
    data=[
        ["Alice", "alice@example.com", "Designer"],
        ["Bob", "bob@example.com", "Developer"]
    ]
)
```

#### KanbanBoardWidget
```python
from pyqt_widgets.data import KanbanBoardWidget

kanban = KanbanBoardWidget(
    columns=["To Do", "In Progress", "Review", "Done"]
)
```

#### TimelineWidget
```python
from pyqt_widgets.data import TimelineWidget

timeline = TimelineWidget(events=[
    {"date": "2024-01-15", "title": "Project Started", "description": "Initial setup"},
    {"date": "2024-02-01", "title": "First Release", "description": "Beta version"}
])
```

### 👥 User & Social

User-focused widgets for social applications.

#### UserAvatarWidget
```python
from pyqt_widgets.user import UserAvatarWidget

avatar = UserAvatarWidget(
    image_path="user.png",
    initials="AJ",
    size=48
)
```

#### ChatBubbleWidget
```python
from pyqt_widgets.user import ChatBubbleWidget

bubble = ChatBubbleWidget(
    message="Hello! How are you today?",
    sender=True,
    timestamp="10:30 AM"
)
```

#### RatingStarWidget
```python
from pyqt_widgets.user import RatingStarWidget

rating = RatingStarWidget(
    max_stars=5,
    value=4,
    editable=True
)
```

### 📝 Forms & Input

Enhanced form controls and input widgets.

#### SearchBoxWithSuggestions
```python
from pyqt_widgets.forms import SearchBoxWithSuggestions

search = SearchBoxWithSuggestions(
    placeholder="Search users...",
    suggestions=["Alice", "Bob", "Charlie"]
)
```

#### TagInputWidget
```python
from pyqt_widgets.forms import TagInputWidget

tags = TagInputWidget(
    placeholder="Add tags...",
    suggestions=["Python", "PyQt6", "Desktop", "GUI"]
)
```

#### ToggleSwitchWidget
```python
from pyqt_widgets.forms import ToggleSwitchWidget

toggle = ToggleSwitchWidget(
    label="Enable notifications",
    state=True
)
```

### 🔧 Utility

Helpful utility widgets for enhanced UX.

#### FloatingActionButton
```python
from pyqt_widgets.utility import FloatingActionButton

fab = FloatingActionButton(
    icon="add",
    position="bottom-right"
)
```

#### QuickSettingsPanel
```python
from pyqt_widgets.utility import QuickSettingsPanel

settings = QuickSettingsPanel(toggles=[
    {"label": "Dark Mode", "key": "dark_mode"},
    {"label": "Notifications", "key": "notifications"}
])
```

---

## 🎨 Theming

The library includes a powerful theming system:

### Basic Theme Usage

```python
from pyqt_widgets import theme_manager

# Apply dark theme
theme_manager.set_theme("dark")
app.setStyleSheet(theme_manager.get_stylesheet())

# Apply light theme
theme_manager.set_theme("light")
app.setStyleSheet(theme_manager.get_stylesheet())
```

### Custom Colors

```python
# Get theme colors
primary_color = theme_manager.get_color("primary")
background_color = theme_manager.get_color("background")
text_color = theme_manager.get_color("text")

# Use in custom styling
widget.setStyleSheet(f"""
    background-color: {background_color};
    color: {text_color};
    border: 2px solid {primary_color};
""")
```

### Theme Customization

```python
# Define custom theme
custom_theme = {
    "primary": "#6366f1",
    "secondary": "#8b5cf6", 
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "background": "#ffffff",
    "surface": "#f8fafc",
    "text": "#1f2937"
}

theme_manager.register_theme("custom", custom_theme)
theme_manager.set_theme("custom")
```

---

## 🏗️ Building Complex Applications

### Dashboard Example

```python
from PyQt6.QtWidgets import QGridLayout, QWidget
from pyqt_widgets.cards import StatCardWidget, InfoCardWidget
from pyqt_widgets.data import MiniChartCard
from pyqt_widgets.navigation import SidebarNavWidget

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Main layout
        main_layout = QHBoxLayout(self)
        
        # Sidebar
        sidebar = SidebarNavWidget(items=[
            {"text": "Dashboard", "icon": "dashboard"},
            {"text": "Analytics", "icon": "chart"},
            {"text": "Users", "icon": "users"}
        ])
        main_layout.addWidget(sidebar)
        
        # Content area
        content = QWidget()
        content_layout = QGridLayout(content)
        
        # Stats cards
        users_card = StatCardWidget(1250, "Active Users", "up", 15.3)
        revenue_card = StatCardWidget(45230, "Revenue", "up", 8.2)
        orders_card = StatCardWidget(89, "Orders", "down", -2.1)
        
        content_layout.addWidget(users_card, 0, 0)
        content_layout.addWidget(revenue_card, 0, 1) 
        content_layout.addWidget(orders_card, 0, 2)
        
        # Chart
        chart_data = [10, 25, 15, 30, 20, 35, 25]
        chart = MiniChartCard(data=chart_data, title="Weekly Sales")
        content_layout.addWidget(chart, 1, 0, 1, 3)
        
        main_layout.addWidget(content)
```

### User Management Interface

```python
from pyqt_widgets.user import UserListItemWidget
from pyqt_widgets.forms import SearchBoxWithSuggestions
from pyqt_widgets.feedback import NotificationToastWidget

class UserManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Search
        search = SearchBoxWithSuggestions(
            placeholder="Search users...",
            suggestions=["Alice", "Bob", "Charlie"]
        )
        layout.addWidget(search)
        
        # User list
        users = [
            {"name": "Alice Johnson", "role": "Designer", "avatar": "alice.png"},
            {"name": "Bob Smith", "role": "Developer", "avatar": "bob.png"}
        ]
        
        for user in users:
            user_item = UserListItemWidget(
                name=user["name"],
                role=user["role"],
                avatar=user["avatar"],
                actions=[
                    {"text": "Edit", "callback": self.edit_user},
                    {"text": "Delete", "callback": self.delete_user}
                ]
            )
            layout.addWidget(user_item)
    
    def edit_user(self):
        toast = NotificationToastWidget("User edit dialog opened", "info")
        toast.show()
    
    def delete_user(self):
        toast = NotificationToastWidget("User deleted", "success")
        toast.show()
```

---

## 🎯 Best Practices

### 1. Theme Consistency
Always apply the global theme to your application:

```python
app = QApplication(sys.argv)
app.setStyleSheet(theme_manager.get_stylesheet())
```

### 2. Widget Organization
Organize widgets by category for better maintainability:

```python
from pyqt_widgets import cards, navigation, forms, feedback
```

### 3. Signal Connections
Connect widget signals for interactivity:

```python
button.clicked.connect(self.handle_click)
search.text_changed.connect(self.filter_results)
card.selection_changed.connect(self.update_selection)
```

### 4. Responsive Layouts
Use appropriate layouts for different screen sizes:

```python
# Use QGridLayout for dashboard-style layouts
grid = QGridLayout()

# Use QVBoxLayout for vertical lists
vbox = QVBoxLayout()

# Use QHBoxLayout for horizontal toolbars
hbox = QHBoxLayout()
```

### 5. Error Handling
Handle widget states appropriately:

```python
try:
    data = load_user_data()
    table.set_data(data)
except Exception as e:
    table.set_error(f"Failed to load data: {str(e)}")
```

---

## 🔧 Troubleshooting

### Common Issues

**ImportError: No module named 'PyQt6'**
```bash
pip install PyQt6
```

**Widget not displaying correctly**
- Ensure theme is applied: `app.setStyleSheet(theme_manager.get_stylesheet())`
- Check widget is added to layout: `layout.addWidget(widget)`

**Performance issues with many widgets**
- Use lazy loading for large datasets
- Implement virtual scrolling for long lists
- Consider widget pooling for dynamic content

**Styling not working**
- Verify theme is set before creating widgets
- Check CSS selector specificity
- Use `widget.update()` to force refresh

---

## 📞 Support

- **Documentation**: [Full API Documentation](https://pyqt6-widgets-library.readthedocs.io/)
- **GitHub**: [Issues and Discussions](https://github.com/madhusudanmewada/pyqt6-widgets-library)
- **Email**: madhusudanmewadamm@gmail.com

---

## 🎉 Demo Applications

Try the included demos:

```bash
# Basic widget showcase
pyqt6-widgets-demo

# Card widgets showcase  
pyqt6-cards-showcase
```

These provide interactive examples of all available widgets and their configurations.

---

*Made with ❤️ by Madhusudan Mewada*