"""
Cross Sections Image Gallery
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...physics.materials import CROSS_SECTION_IMAGES


class CrossSectionsDisplay:
    """Display cross-section plots from Magboltz data."""

    def render(self):
        with calculator_card("Cross Sections", "Electron scattering cross-sections from Magboltz data"):
            ui.link(
                "Source: Magboltz data at CERN",
                "http://rjd.web.cern.ch/rjd/cgi-bin/cross/",
                new_tab=True,
            ).classes('text-caption')

            ui.separator().classes('q-my-md')

            # Create expansion panels for each species
            with ui.column().classes('w-full gap-2'):
                for item in CROSS_SECTION_IMAGES:
                    with ui.expansion(item["name"], icon="show_chart").classes('w-full'):
                        ui.image(f"/static/pngs/{item['file']}").classes('w-full max-w-2xl')
