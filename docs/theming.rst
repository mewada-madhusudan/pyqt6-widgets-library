Theming Guide
=============

The PyQt6 Widgets Library includes a comprehensive theming system that allows you to customize the appearance of all widgets consistently across your application.

Theme Manager
-------------

The :class:`ThemeManager` is the central component for managing themes in your application.

.. code-block:: python

    from pyqt_widgets import theme_manager

Basic Theme Usage
-----------------

Applying Themes
~~~~~~~~~~~~~~~

The library comes with built-in light and dark themes:

.. code-block:: python

    # Apply dark theme
    theme_manager.set_theme("dark")
    app.setStyleSheet(theme_manager.get_stylesheet())

    # Apply light theme
    theme_manager.set_theme("light")
    app.setStyleSheet(theme_manager.get_stylesheet())

Getting Theme Colors
~~~~~~~~~~~~~~~~~~~~

Access theme colors programmatically:

.. code-block:: python

    # Get primary colors
    primary = theme_manager.get_color("primary")
    secondary = theme_manager.get_color("secondary")

    # Get semantic colors
    success = theme_manager.get_color("success")
    warning = theme_manager.get_color("warning")
    error = theme_manager.get_color("error")

    # Get surface colors
    background = theme_manager.get_color("background")
    surface = theme_manager.get_color("surface")
    text = theme_manager.get_color("text")

Built-in Themes
---------------

Light Theme
~~~~~~~~~~~

The default light theme uses a clean, modern color palette:

* **Primary**: #3b82f6 (Blue)
* **Secondary**: #6b7280 (Gray)
* **Success**: #10b981 (Green)
* **Warning**: #f59e0b (Amber)
* **Error**: #ef4444 (Red)
* **Background**: #ffffff (White)
* **Surface**: #f8fafc (Light Gray)
* **Text**: #1f2937 (Dark Gray)

Dark Theme
~~~~~~~~~~

The dark theme provides a comfortable low-light experience:

* **Primary**: #60a5fa (Light Blue)
* **Secondary**: #9ca3af (Light Gray)
* **Success**: #34d399 (Light Green)
* **Warning**: #fbbf24 (Light Amber)
* **Error**: #f87171 (Light Red)
* **Background**: #111827 (Dark Blue-Gray)
* **Surface**: #1f2937 (Medium Gray)
* **Text**: #f9fafb (Off-White)

Custom Themes
-------------

Creating Custom Themes
~~~~~~~~~~~~~~~~~~~~~~

Define your own theme with custom colors:

.. code-block:: python

    # Define custom theme colors
    custom_theme = {
        "primary": "#6366f1",      # Indigo
        "secondary": "#8b5cf6",    # Violet
        "success": "#10b981",      # Emerald
        "warning": "#f59e0b",      # Amber
        "error": "#ef4444",        # Red
        "background": "#ffffff",   # White
        "surface": "#f8fafc",      # Slate 50
        "text": "#1f2937",         # Gray 800
        "text_secondary": "#6b7280", # Gray 500
        "border": "#e5e7eb",       # Gray 200
        "shadow": "rgba(0,0,0,0.1)" # Subtle shadow
    }

    # Register the custom theme
    theme_manager.register_theme("custom", custom_theme)

    # Apply the custom theme
    theme_manager.set_theme("custom")
    app.setStyleSheet(theme_manager.get_stylesheet())

Theme Variants
~~~~~~~~~~~~~~

Create theme variants for different contexts:

.. code-block:: python

    # High contrast theme for accessibility
    high_contrast_theme = {
        "primary": "#000000",
        "secondary": "#333333",
        "success": "#008000",
        "warning": "#ff8c00",
        "error": "#ff0000",
        "background": "#ffffff",
        "surface": "#f0f0f0",
        "text": "#000000"
    }

    # Corporate theme
    corporate_theme = {
        "primary": "#1e40af",      # Corporate blue
        "secondary": "#64748b",    # Slate
        "success": "#059669",      # Emerald
        "warning": "#d97706",      # Amber
        "error": "#dc2626",        # Red
        "background": "#ffffff",
        "surface": "#f1f5f9",      # Slate 100
        "text": "#0f172a"          # Slate 900
    }

    theme_manager.register_theme("high_contrast", high_contrast_theme)
    theme_manager.register_theme("corporate", corporate_theme)

Widget-Specific Styling
-----------------------

Custom Widget Styles
~~~~~~~~~~~~~~~~~~~~

Apply custom styles to specific widgets:

.. code-block:: python

    # Style a specific card widget
    card = InfoCardWidget("Title", "Subtitle", "Description")
    card.setStyleSheet(f"""
        InfoCardWidget {{
            background-color: {theme_manager.get_color("surface")};
            border: 2px solid {theme_manager.get_color("primary")};
            border-radius: 12px;
            padding: 16px;
        }}

        InfoCardWidget:hover {{
            background-color: {theme_manager.get_color("primary")};
            color: white;
        }}
    """)

Theme-Aware Custom Styles
~~~~~~~~~~~~~~~~~~~~~~~~~

Create styles that adapt to theme changes:

.. code-block:: python

    def apply_custom_button_style(button):
        primary = theme_manager.get_color("primary")
        text = theme_manager.get_color("text")
        surface = theme_manager.get_color("surface")

        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: {primary}dd;
            }}

            QPushButton:pressed {{
                background-color: {primary}bb;
            }}

            QPushButton:disabled {{
                background-color: {surface};
                color: {text}80;
            }}
        """)

Dynamic Theme Switching
-----------------------

Runtime Theme Changes
~~~~~~~~~~~~~~~~~~~~

Allow users to switch themes at runtime:

.. code-block:: python

    class ThemeSelector(QWidget):
        def __init__(self):
            super().__init__()
            layout = QHBoxLayout(self)

            # Theme selection buttons
            light_btn = QPushButton("Light")
            dark_btn = QPushButton("Dark")
            custom_btn = QPushButton("Custom")

            light_btn.clicked.connect(lambda: self.switch_theme("light"))
            dark_btn.clicked.connect(lambda: self.switch_theme("dark"))
            custom_btn.clicked.connect(lambda: self.switch_theme("custom"))

            layout.addWidget(light_btn)
            layout.addWidget(dark_btn)
            layout.addWidget(custom_btn)

        def switch_theme(self, theme_name):
            theme_manager.set_theme(theme_name)

            # Get the main application window
            app = QApplication.instance()
            app.setStyleSheet(theme_manager.get_stylesheet())

            # Refresh all widgets
            for widget in app.allWidgets():
                widget.update()

Theme Persistence
~~~~~~~~~~~~~~~~

Save and restore user theme preferences:

.. code-block:: python

    import json
    from pathlib import Path

    class ThemeSettings:
        def __init__(self):
            self.settings_file = Path.home() / ".myapp" / "theme_settings.json"
            self.settings_file.parent.mkdir(exist_ok=True)

        def save_theme(self, theme_name):
            settings = {"theme": theme_name}
            with open(self.settings_file, "w") as f:
                json.dump(settings, f)

        def load_theme(self):
            try:
                with open(self.settings_file, "r") as f:
                    settings = json.load(f)
                    return settings.get("theme", "light")
            except FileNotFoundError:
                return "light"

    # Usage
    theme_settings = ThemeSettings()
    saved_theme = theme_settings.load_theme()
    theme_manager.set_theme(saved_theme)

Advanced Theming
----------------

CSS Variables
~~~~~~~~~~~~~

Use CSS custom properties for dynamic styling:

.. code-block:: python

    def generate_css_variables():
        variables = []
        for key, value in theme_manager.current_theme.items():
            variables.append(f"--{key}: {value};")

        return f"""
        :root {{
            {chr(10).join(variables)}
        }}

        .themed-widget {{
            background-color: var(--surface);
            color: var(--text);
            border: 1px solid var(--border);
        }}
        """

Animation Integration
~~~~~~~~~~~~~~~~~~~~

Animate theme transitions:

.. code-block:: python

    from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
    from PyQt6.QtWidgets import QGraphicsOpacityEffect

    def animate_theme_change(widget, duration=300):
        # Create opacity effect
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)

        # Create animation
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        def on_fade_out_finished():
            # Apply new theme
            theme_manager.set_theme("dark")
            widget.setStyleSheet(theme_manager.get_stylesheet())

            # Fade back in
            fade_in = QPropertyAnimation(effect, b"opacity")
            fade_in.setDuration(duration)
            fade_in.setStartValue(0.0)
            fade_in.setEndValue(1.0)
            fade_in.start()

        animation.finished.connect(on_fade_out_finished)
        animation.start()

Best Practices
--------------

1. **Consistency**: Always use theme colors instead of hardcoded values
2. **Accessibility**: Ensure sufficient contrast ratios in custom themes
3. **Performance**: Cache theme stylesheets for better performance
4. **Responsiveness**: Test themes with different widget states and sizes
5. **User Choice**: Provide theme selection options in your application settings

Theme Testing
-------------

Test your themes across different widgets:

.. code-block:: python

    def test_theme_with_widgets():
        """Test current theme with various widgets"""
        test_window = QWidget()
        layout = QVBoxLayout(test_window)

        # Test different widget types
        widgets = [
            InfoCardWidget("Test Card", "Subtitle", "Description"),
            BaseButton("Test Button", "primary", "medium"),
            StatusChipWidget("Active", "success"),
            SearchBoxWithSuggestions(placeholder="Search..."),
            ToggleSwitchWidget("Test Toggle", True)
        ]

        for widget in widgets:
            layout.addWidget(widget)

        test_window.show()
        return test_window

This comprehensive theming system ensures your application maintains a consistent, professional appearance while providing flexibility for customization and branding.