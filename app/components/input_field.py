"""
Input Field Components

Reusable input field components with labels and units.
"""

from nicegui import ui
from typing import Optional, Callable, List, Tuple


def number_input(
    label: str,
    value: float = None,
    unit: str = None,
    on_change: Callable = None,
    placeholder: str = "",
    min_val: float = None,
    max_val: float = None,
) -> ui.number:
    """
    Create a labeled number input field with optional unit suffix.

    Args:
        label: Field label
        value: Initial value
        unit: Unit label to display after the input
        on_change: Callback function when value changes
        placeholder: Placeholder text
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        The ui.number element for binding
    """
    with ui.row().classes('items-center gap-2'):
        inp = ui.number(
            label=label,
            value=value,
            on_change=on_change,
            format='%.6g',
        ).classes('w-48')

        if placeholder:
            inp.props(f'placeholder="{placeholder}"')
        if min_val is not None:
            inp.props(f'min={min_val}')
        if max_val is not None:
            inp.props(f'max={max_val}')

        if unit:
            ui.label(unit).classes('text-grey-6')

    return inp


def select_input(
    label: str,
    options: List[str] | dict,
    value: str = None,
    on_change: Callable = None,
) -> ui.select:
    """
    Create a labeled select/dropdown field.

    Args:
        label: Field label
        options: List of options or dict of {value: label}
        value: Initial selected value
        on_change: Callback function when selection changes

    Returns:
        The ui.select element for binding
    """
    return ui.select(
        options=options,
        value=value,
        label=label,
        on_change=on_change,
    ).classes('w-48')


def radio_input(
    label: str,
    options: List[str] | dict,
    value: str = None,
    on_change: Callable = None,
) -> ui.radio:
    """
    Create a labeled radio button group.

    Args:
        label: Group label
        options: List of options or dict of {value: label}
        value: Initial selected value
        on_change: Callback function when selection changes

    Returns:
        The ui.radio element for binding
    """
    with ui.column().classes('gap-1'):
        if label:
            ui.label(label).classes('text-caption text-grey-6')
        return ui.radio(
            options=options,
            value=value,
            on_change=on_change,
        )
