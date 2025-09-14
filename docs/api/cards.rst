Cards API
=========

Card widgets are used to display information in a structured, visually appealing format. All card widgets inherit from :class:`BaseCardWidget` and support theming, animations, and common styling options.

.. currentmodule:: pyqt_widgets.cards

InfoCardWidget
--------------

.. autoclass:: InfoCardWidget
   :members:
   :inherited-members:

A versatile card widget for displaying information with a title, subtitle, and description.

**Parameters:**
    * ``title`` (str) - Main heading text
    * ``subtitle`` (str, optional) - Secondary heading text
    * ``description`` (str, optional) - Body text content
    * ``icon`` (str, optional) - Icon name or path
    * ``theme`` (str) - Theme variant ("light", "dark")

**Example:**

.. code-block:: python

    from pyqt_widgets.cards import InfoCardWidget

    card = InfoCardWidget(
        title="Total Revenue",
        subtitle="This Month",
        description="$45,230 (+12% from last month)",
        icon="dollar-sign"
    )

**Signals:**
    * ``clicked()`` - Emitted when card is clicked
    * ``double_clicked()`` - Emitted when card is double-clicked

ProfileCardWidget
-----------------

.. autoclass:: ProfileCardWidget
   :members:
   :inherited-members:

Displays user profile information with avatar, name, role, and action buttons.

**Parameters:**
    * ``name`` (str) - User's display name
    * ``role`` (str, optional) - User's role or title
    * ``avatar`` (str, optional) - Path to avatar image
    * ``initials`` (str, optional) - Fallback initials if no avatar
    * ``actions`` (list, optional) - List of action button configurations

**Example:**

.. code-block:: python

    from pyqt_widgets.cards import ProfileCardWidget

    profile = ProfileCardWidget(
        name="Alice Johnson",
        role="Senior Designer",
        avatar="avatars/alice.png",
        actions=[
            {"text": "Message", "icon": "message"},
            {"text": "Call", "icon": "phone"}
        ]
    )

StatCardWidget
--------------

.. autoclass:: StatCardWidget
   :members:
   :inherited-members:

Displays statistical information with large numbers, labels, and trend indicators.

**Parameters:**
    * ``number`` (int/float) - The main statistic to display
    * ``label`` (str) - Description of the statistic
    * ``trend`` (str, optional) - Trend direction ("up", "down", "neutral")
    * ``percentage`` (float, optional) - Percentage change
    * ``format`` (str, optional) - Number formatting ("currency", "percentage", "number")

**Example:**

.. code-block:: python

    from pyqt_widgets.cards import StatCardWidget

    stat = StatCardWidget(
        number=1250,
        label="Active Users",
        trend="up",
        percentage=15.3,
        format="number"
    )

ExpandableCardWidget
--------------------

.. autoclass:: ExpandableCardWidget
   :members:
   :inherited-members:

A collapsible card that can show/hide content sections.

**Parameters:**
    * ``title`` (str) - Card header title
    * ``expanded`` (bool) - Initial expansion state
    * ``animate`` (bool) - Whether to animate expansion

**Methods:**
    * ``add_content(widget)`` - Add widget to expandable content area
    * ``set_expanded(expanded)`` - Programmatically expand/collapse
    * ``toggle()`` - Toggle expansion state

**Example:**

.. code-block:: python

    from pyqt_widgets.cards import ExpandableCardWidget
    from PyQt6.QtWidgets import QLabel

    card = ExpandableCardWidget(title="Order Details")

    # Add content to the expandable section
    details = QLabel("Order #12345\nStatus: Shipped\nTotal: $99.99")
    card.add_content(details)

HoverActionCardWidget
---------------------

.. autoclass:: HoverActionCardWidget
   :members:
   :inherited-members:

Displays action buttons when hovered, useful for item lists and dashboards.

**Parameters:**
    * ``title`` (str) - Card title
    * ``description`` (str, optional) - Card description
    * ``actions`` (list) - List of action configurations

**Example:**

.. code-block:: python

    from pyqt_widgets.cards import HoverActionCardWidget

    card = HoverActionCardWidget(
        title="Project Alpha",
        description="Web application development",
        actions=[
            {"text": "Edit", "icon": "edit", "callback": self.edit_project},
            {"text": "Delete", "icon": "trash", "callback": self.delete_project}
        ]
    )

ImageCardWidget
---------------

.. autoclass:: ImageCardWidget
   :members:
   :inherited-members:

Card with image preview and overlay text.

**Parameters:**
    * ``image_path`` (str) - Path to image file
    * ``title`` (str, optional) - Overlay title
    * ``description`` (str, optional) - Overlay description
    * ``aspect_ratio`` (str) - Image aspect ratio ("16:9", "4:3", "1:1")

**Example:**

.. code-block:: python

    from pyqt_widgets.cards import ImageCardWidget

    card = ImageCardWidget(
        image_path="products/laptop.jpg",
        title="Gaming Laptop",
        description="High-performance laptop for gaming",
        aspect_ratio="16:9"
    )

SelectableCardWidget
--------------------

.. autoclass:: SelectableCardWidget
   :members:
   :inherited-members:

Card that can be selected/deselected, useful for multi-selection interfaces.

**Parameters:**
    * ``title`` (str) - Card title
    * ``description`` (str, optional) - Card description
    * ``selected`` (bool) - Initial selection state
    * ``selection_mode`` (str) - "single" or "multiple"

**Signals:**
    * ``selection_changed(selected)`` - Emitted when selection state changes

**Example:**

.. code-block:: python

    from pyqt_widgets.cards import SelectableCardWidget

    card = SelectableCardWidget(
        title="Option A",
        description="Choose this option for...",
        selection_mode="multiple"
    )

    card.selection_changed.connect(self.on_selection_changed)

Common Card Methods
-------------------

All card widgets inherit these methods from :class:`BaseCardWidget`:

**Styling Methods:**
    * ``set_theme(theme)`` - Set theme variant
    * ``set_size(size)`` - Set size variant
    * ``set_border_radius(radius)`` - Set corner radius
    * ``set_shadow(enabled)`` - Enable/disable drop shadow

**Animation Methods:**
    * ``fade_in(duration=300)`` - Fade in animation
    * ``fade_out(duration=300)`` - Fade out animation
    * ``slide_in(direction="up", duration=300)`` - Slide in animation

**State Methods:**
    * ``set_loading(loading)`` - Show/hide loading state
    * ``set_error(error_message)`` - Show error state
    * ``reset_state()`` - Reset to normal state

Card Theming
------------

Cards support extensive theming through CSS-like properties:

.. code-block:: python

    # Apply custom styling
    card.setStyleSheet("""
        InfoCardWidget {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
        }

        InfoCardWidget:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
    """)

    # Use theme manager colors
    primary_color = theme_manager.get_color("primary")
    card.set_accent_color(primary_color)