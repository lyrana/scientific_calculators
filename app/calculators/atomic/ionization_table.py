"""
Ionization Energies Table
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...physics.materials import IONIZATION_ENERGIES


class IonizationTableDisplay:
    """Display ionization energies reference table."""

    def render(self):
        with calculator_card("Ionization Energies", "Reference table of first ionization energies"):
            # Build table data
            rows = []
            for key, data in IONIZATION_ENERGIES.items():
                display = data.get("display", key)
                energy = data["energy"]
                energy_str = str(energy) if isinstance(energy, str) else f"{energy:.1f}"
                rows.append({
                    "molecule": display,
                    "name": data["name"],
                    "energy": energy_str,
                })

            columns = [
                {"name": "molecule", "label": "Species", "field": "molecule", "align": "left"},
                {"name": "name", "label": "Name", "field": "name", "align": "left"},
                {"name": "energy", "label": "Ionization Energy (eV)", "field": "energy", "align": "right"},
            ]

            ui.table(columns=columns, rows=rows, row_key="molecule").classes('w-full')

            ui.separator().classes('q-my-md')
            ui.label("[TMAE = Tetrakis Dimethylamine Ethylene]").classes('text-caption text-grey-6')
