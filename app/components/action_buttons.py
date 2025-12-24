"""
Action Button Components

Reusable button components for calculator actions.
"""

from nicegui import ui
from typing import Callable


def action_buttons(
    on_calculate: Callable,
    on_reset: Callable,
    calculate_label: str = "Calculate",
    reset_label: str = "Reset Form",
):
    """
    Create a standard Calculate/Reset button pair.

    Args:
        on_calculate: Callback for calculate button
        on_reset: Callback for reset button
        calculate_label: Label for calculate button
        reset_label: Label for reset button
    """
    with ui.row().classes('gap-2 q-mt-md'):
        ui.button(calculate_label, on_click=on_calculate).props('color=primary')
        ui.button(reset_label, on_click=on_reset).props('color=secondary outline')


def single_button(
    label: str,
    on_click: Callable,
    color: str = "primary",
    outline: bool = False,
    icon: str = None,
) -> ui.button:
    """
    Create a single action button.

    Args:
        label: Button label
        on_click: Click callback
        color: Button color
        outline: Whether to use outline style
        icon: Optional icon name

    Returns:
        The button element
    """
    btn = ui.button(label, on_click=on_click, icon=icon)
    props = f'color={color}'
    if outline:
        props += ' outline'
    btn.props(props)
    return btn
