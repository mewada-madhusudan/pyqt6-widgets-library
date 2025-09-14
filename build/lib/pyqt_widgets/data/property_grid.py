"""
Property grid widget for editing key-value pairs.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget,
                             QTreeWidgetItem, QLineEdit, QComboBox, QCheckBox,
                             QSpinBox, QDoubleSpinBox, QPushButton, QColorDialog,
                             QFileDialog, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal, QVariant
from PyQt6.QtGui import QFont, QColor
from ..base.theme_manager import theme_manager
from ..base.base_button import BaseButton


class PropertyGridWidget(QWidget):
    """Property grid for editing object properties."""

    property_changed = pyqtSignal(str, object)  # property_name, new_value

    def __init__(self, parent=None):
        super().__init__(parent)
        self._properties = {}
        self._property_types = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup the property grid UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 8, 12, 8)

        title_label = QLabel("Properties")
        title_font = theme_manager.get_font('heading')
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {theme_manager.get_color('text')};")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Reset button
        reset_btn = BaseButton("Reset", "ghost", "small")
        reset_btn.clicked.connect(self._reset_properties)
        header_layout.addWidget(reset_btn)

        main_layout.addWidget(header)

        # Property tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Property", "Value"])
        self.tree.setAlternatingRowColors(True)
        self.tree.setRootIsDecorated(False)
        self.tree.header().setStretchLastSection(True)

        # Styling
        self.tree.setStyleSheet(f"""
            QTreeWidget {{
                border: 1px solid {theme_manager.get_color('border')};
                background-color: {theme_manager.get_color('surface')};
                alternate-background-color: {theme_manager.get_color('hover')};
            }}
            QTreeWidget::item {{
                padding: 4px;
                border-bottom: 1px solid {theme_manager.get_color('border')};
            }}
            QHeaderView::section {{
                background-color: {theme_manager.get_color('light')};
                padding: 8px;
                border: none;
                border-bottom: 2px solid {theme_manager.get_color('border')};
                font-weight: bold;
            }}
        """)

        main_layout.addWidget(self.tree)

    def add_property(self, name: str, value, property_type: str = "auto",
                     options: list = None, readonly: bool = False):
        """Add property to grid."""
        # Auto-detect type if not specified
        if property_type == "auto":
            property_type = self._detect_type(value)

        self._properties[name] = value
        self._property_types[name] = {
            'type': property_type,
            'options': options,
            'readonly': readonly
        }

        # Create tree item
        item = QTreeWidgetItem([name, ""])
        self.tree.addTopLevelItem(item)

        # Create editor widget
        editor = self._create_editor(name, value, property_type, options, readonly)
        self.tree.setItemWidget(item, 1, editor)

    def _detect_type(self, value) -> str:
        """Auto-detect property type from value."""
        if isinstance(value, bool):
            return "bool"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, QColor):
            return "color"
        else:
            return "string"

    def _create_editor(self, name: str, value, prop_type: str,
                       options: list = None, readonly: bool = False) -> QWidget:
        """Create appropriate editor widget for property type."""
        if readonly:
            # Read-only label
            label = QLabel(str(value))
            label.setStyleSheet(f"color: {theme_manager.get_color('text_secondary')};")
            return label

        if prop_type == "bool":
            return self._create_bool_editor(name, value)
        elif prop_type == "int":
            return self._create_int_editor(name, value)
        elif prop_type == "float":
            return self._create_float_editor(name, value)
        elif prop_type == "string":
            return self._create_string_editor(name, value)
        elif prop_type == "choice" and options:
            return self._create_choice_editor(name, value, options)
        elif prop_type == "color":
            return self._create_color_editor(name, value)
        elif prop_type == "file":
            return self._create_file_editor(name, value)
        else:
            return self._create_string_editor(name, value)

    def _create_bool_editor(self, name: str, value: bool) -> QWidget:
        """Create boolean checkbox editor."""
        checkbox = QCheckBox()
        checkbox.setChecked(value)
        checkbox.toggled.connect(lambda checked: self._update_property(name, checked))
        return checkbox

    def _create_int_editor(self, name: str, value: int) -> QWidget:
        """Create integer spinbox editor."""
        spinbox = QSpinBox()
        spinbox.setRange(-999999, 999999)
        spinbox.setValue(value)
        spinbox.valueChanged.connect(lambda val: self._update_property(name, val))
        return spinbox

    def _create_float_editor(self, name: str, value: float) -> QWidget:
        """Create float spinbox editor."""
        spinbox = QDoubleSpinBox()
        spinbox.setRange(-999999.0, 999999.0)
        spinbox.setDecimals(3)
        spinbox.setValue(value)
        spinbox.valueChanged.connect(lambda val: self._update_property(name, val))
        return spinbox

    def _create_string_editor(self, name: str, value: str) -> QWidget:
        """Create string line edit editor."""
        line_edit = QLineEdit(str(value))
        line_edit.textChanged.connect(lambda text: self._update_property(name, text))
        return line_edit

    def _create_choice_editor(self, name: str, value, options: list) -> QWidget:
        """Create choice combobox editor."""
        combo = QComboBox()
        combo.addItems([str(opt) for opt in options])

        # Set current value
        try:
            index = options.index(value)
            combo.setCurrentIndex(index)
        except ValueError:
            pass

        combo.currentTextChanged.connect(lambda text: self._update_property(name, text))
        return combo

    def _create_color_editor(self, name: str, value) -> QWidget:
        """Create color picker editor."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Color preview
        color_preview = QLabel()
        color_preview.setFixedSize(20, 20)
        color_preview.setStyleSheet(f"""
            QLabel {{
                background-color: {value.name() if isinstance(value, QColor) else str(value)};
                border: 1px solid {theme_manager.get_color('border')};
            }}
        """)
        layout.addWidget(color_preview)

        # Color button
        color_btn = QPushButton("Choose...")
        color_btn.clicked.connect(lambda: self._choose_color(name, color_preview))
        layout.addWidget(color_btn)

        return container

    def _create_file_editor(self, name: str, value: str) -> QWidget:
        """Create file picker editor."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # File path display
        path_edit = QLineEdit(str(value))
        path_edit.setReadOnly(True)
        layout.addWidget(path_edit)

        # Browse button
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(lambda: self._browse_file(name, path_edit))
        layout.addWidget(browse_btn)

        return container

    def _choose_color(self, name: str, preview_label: QLabel):
        """Open color chooser dialog."""
        current_color = self._properties.get(name, QColor(255, 255, 255))
        if isinstance(current_color, str):
            current_color = QColor(current_color)

        color = QColorDialog.getColor(current_color, self)
        if color.isValid():
            self._update_property(name, color)
            preview_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {color.name()};
                    border: 1px solid {theme_manager.get_color('border')};
                }}
            """)

    def _browse_file(self, name: str, path_edit: QLineEdit):
        """Open file browser dialog."""
        filename, _ = QFileDialog.getOpenFileName(self, "Choose File")
        if filename:
            self._update_property(name, filename)
            path_edit.setText(filename)

    def _update_property(self, name: str, value):
        """Update property value."""
        self._properties[name] = value
        self.property_changed.emit(name, value)

    def get_property(self, name: str):
        """Get property value."""
        return self._properties.get(name)

    def set_property(self, name: str, value):
        """Set property value programmatically."""
        if name in self._properties:
            self._properties[name] = value
            # Update UI widget
            for i in range(self.tree.topLevelItemCount()):
                item = self.tree.topLevelItem(i)
                if item.text(0) == name:
                    widget = self.tree.itemWidget(item, 1)
                    self._update_widget_value(widget, value)
                    break

    def _update_widget_value(self, widget: QWidget, value):
        """Update widget to show new value."""
        if isinstance(widget, QCheckBox):
            widget.setChecked(value)
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            widget.setValue(value)
        elif isinstance(widget, QLineEdit):
            widget.setText(str(value))
        elif isinstance(widget, QComboBox):
            widget.setCurrentText(str(value))

    def remove_property(self, name: str):
        """Remove property from grid."""
        if name in self._properties:
            del self._properties[name]
            del self._property_types[name]

            # Remove from tree
            for i in range(self.tree.topLevelItemCount()):
                item = self.tree.topLevelItem(i)
                if item.text(0) == name:
                    self.tree.takeTopLevelItem(i)
                    break

    def clear_properties(self):
        """Clear all properties."""
        self._properties.clear()
        self._property_types.clear()
        self.tree.clear()

    def _reset_properties(self):
        """Reset all properties to default values."""
        # This would need default values to be stored
        pass

    def get_all_properties(self) -> dict:
        """Get all property values."""
        return self._properties.copy()

    def set_properties(self, properties: dict):
        """Set multiple properties at once."""
        self.clear_properties()
        for name, value in properties.items():
            self.add_property(name, value)


class GroupedPropertyGrid(PropertyGridWidget):
    """Property grid with grouped properties."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._groups = {}

    def add_group(self, group_name: str):
        """Add property group."""
        group_item = QTreeWidgetItem([group_name, ""])
        group_font = theme_manager.get_font('default')
        group_font.setWeight(QFont.Weight.Bold)
        group_item.setFont(0, group_font)

        self.tree.addTopLevelItem(group_item)
        self._groups[group_name] = group_item

    def add_property_to_group(self, group_name: str, name: str, value,
                              property_type: str = "auto", options: list = None,
                              readonly: bool = False):
        """Add property to specific group."""
        if group_name not in self._groups:
            self.add_group(group_name)

        # Auto-detect type if not specified
        if property_type == "auto":
            property_type = self._detect_type(value)

        self._properties[name] = value
        self._property_types[name] = {
            'type': property_type,
            'options': options,
            'readonly': readonly
        }

        # Create tree item under group
        group_item = self._groups[group_name]
        item = QTreeWidgetItem([name, ""])
        group_item.addChild(item)

        # Create editor widget
        editor = self._create_editor(name, value, property_type, options, readonly)
        self.tree.setItemWidget(item, 1, editor)

        # Expand group
        group_item.setExpanded(True)


class ObjectPropertyGrid(PropertyGridWidget):
    """Property grid that automatically reflects object properties."""

    def __init__(self, target_object=None, parent=None):
        super().__init__(parent)
        self._target_object = target_object
        if target_object:
            self._reflect_object()

    def set_target_object(self, obj):
        """Set target object to reflect."""
        self._target_object = obj
        self._reflect_object()

    def _reflect_object(self):
        """Reflect object properties into grid."""
        if not self._target_object:
            return

        self.clear_properties()

        # Get object attributes
        for attr_name in dir(self._target_object):
            if not attr_name.startswith('_'):  # Skip private attributes
                try:
                    value = getattr(self._target_object, attr_name)
                    if not callable(value):  # Skip methods
                        self.add_property(attr_name, value)
                except:
                    pass  # Skip attributes that can't be accessed

    def _update_property(self, name: str, value):
        """Override to update target object."""
        super()._update_property(name, value)

        # Update target object if it exists
        if self._target_object and hasattr(self._target_object, name):
            try:
                setattr(self._target_object, name, value)
            except:
                pass  # Skip read-only attributes