"""
Atomic Mass Conversion Calculator
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.atomic_formulas import calculate_mass_conversion
from ...physics.constants import PROTON_MASS_KG, ELECTRON_MASS_KG


class MassConversionCalculator:
    """Calculator for atomic mass unit conversion."""

    def __init__(self):
        self.amu = None
        self.results = ResultGroup("Results")

    def calculate(self):
        if self.amu is None:
            ui.notify("Please enter a mass value", type="warning")
            return

        try:
            result = calculate_mass_conversion(self.amu)
            self.results.set_value("mass", f"{format_scientific(result['mass_kg'], 6)} kg")
        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        self.amu = None
        self.results.clear_all()

    def render(self):
        with calculator_card("Atomic Mass Conversion", "Convert atomic mass units to kilograms"):
            with ui.column().classes('gap-4 w-full'):
                ui.number(
                    label="Atomic Mass (amu)",
                    value=self.amu,
                    on_change=lambda e: setattr(self, 'amu', e.value),
                    format='%.6g',
                ).classes('w-48')

                action_buttons(self.calculate, self.reset)

                self.results.add_field("mass", "Mass", "")
                self.results.render()

                ui.separator().classes('q-my-md')
                ui.label("Reference Values").classes('text-subtitle2')
                ui.label(f"Proton mass = {format_scientific(PROTON_MASS_KG, 8)} kg").classes('font-mono text-caption')
                ui.label(f"Electron mass = {format_scientific(ELECTRON_MASS_KG, 8)} kg").classes('font-mono text-caption')
