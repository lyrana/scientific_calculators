"""
Result Display Components

Components for displaying calculation results with proper formatting.
"""

from nicegui import ui
from typing import Optional


def format_scientific(value: float, precision: int = 5) -> str:
    """
    Format a number in scientific notation similar to JavaScript's toPrecision.

    Args:
        value: The number to format
        precision: Number of significant digits

    Returns:
        Formatted string
    """
    if value is None:
        return "--"
    if value == 0:
        return "0"
    try:
        return f"{value:.{precision}g}"
    except (ValueError, TypeError):
        return str(value)


class ResultField:
    """A read-only result display field with label and optional unit."""

    def __init__(self, label: str, unit: str = ""):
        """
        Create a result field.

        Args:
            label: Field label
            unit: Unit label to display after the value
        """
        self.label = label
        self.unit = unit
        self._value = "--"
        self._label_element = None
        self._value_element = None

    def render(self) -> 'ResultField':
        """Render the result field UI."""
        with ui.row().classes('items-center gap-2'):
            self._label_element = ui.label(f"{self.label}:").classes('text-weight-medium w-48')
            self._value_element = ui.label(self._value).classes('font-mono text-primary')
            if self.unit:
                ui.label(self.unit).classes('text-grey-6')
        return self

    def set_value(self, value: float | str, precision: int = 5):
        """
        Set the displayed value.

        Args:
            value: The value to display
            precision: Number of significant digits for formatting
        """
        if isinstance(value, (int, float)):
            self._value = format_scientific(value, precision)
        else:
            self._value = str(value) if value else "--"

        if self._value_element:
            self._value_element.set_text(self._value)

    def clear(self):
        """Clear the displayed value."""
        self._value = "--"
        if self._value_element:
            self._value_element.set_text("--")


class ResultGroup:
    """A group of result fields displayed together."""

    def __init__(self, title: str = "Results"):
        """
        Create a result group.

        Args:
            title: Optional title for the group
        """
        self.title = title
        self.fields: dict[str, ResultField] = {}

    def add_field(self, key: str, label: str, unit: str = "") -> ResultField:
        """
        Add a result field to the group.

        Args:
            key: Unique key for accessing the field
            label: Display label
            unit: Unit label

        Returns:
            The created ResultField
        """
        field = ResultField(label, unit)
        self.fields[key] = field
        return field

    def render(self):
        """Render all result fields."""
        with ui.column().classes('gap-2 q-mt-md'):
            if self.title:
                ui.label(self.title).classes('text-subtitle1 text-weight-medium')
            ui.separator().classes('q-my-xs')
            for field in self.fields.values():
                field.render()

    def set_value(self, key: str, value: float | str, precision: int = 5):
        """Set a specific field's value."""
        if key in self.fields:
            self.fields[key].set_value(value, precision)

    def clear_all(self):
        """Clear all field values."""
        for field in self.fields.values():
            field.clear()
