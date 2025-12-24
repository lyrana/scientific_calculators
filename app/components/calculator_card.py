"""
Calculator Card Component

A reusable card wrapper for calculator sections with consistent styling.
"""

from contextlib import contextmanager
from nicegui import ui


@contextmanager
def calculator_card(title: str, description: str = None):
    """
    Context manager for creating a styled calculator card.

    Args:
        title: The title displayed at the top of the card
        description: Optional description text below the title

    Usage:
        with calculator_card("My Calculator", "Calculate something"):
            ui.number("Input 1")
            ui.button("Calculate")
    """
    with ui.card().classes('w-full max-w-3xl q-pa-md'):
        ui.label(title).classes('text-h5 text-weight-medium')
        if description:
            ui.label(description).classes('text-caption text-grey-6 q-mb-sm')
        ui.separator().classes('q-my-sm')
        yield


def calculator_section(title: str):
    """
    Create a section header within a calculator.

    Args:
        title: Section title
    """
    ui.label(title).classes('text-subtitle1 text-weight-medium q-mt-md')
