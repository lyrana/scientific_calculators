"""
Plasma Beta Calculator
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.plasma_formulas import calculate_plasma_beta


class PlasmaBetaCalculator:
    """Calculator for plasma beta."""

    def __init__(self):
        self.magnetic_field = None
        self.electron_density = None
        self.temperature = None
        self.results = ResultGroup("Results")

    def calculate(self):
        if any(v is None for v in [self.magnetic_field, self.electron_density, self.temperature]):
            ui.notify("Please enter all values", type="warning")
            return

        try:
            result = calculate_plasma_beta(
                self.magnetic_field,
                self.electron_density,
                self.temperature
            )
            self.results.set_value("beta", format_scientific(result['beta'], 3))
        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        self.magnetic_field = None
        self.electron_density = None
        self.temperature = None
        self.results.clear_all()

    def render(self):
        with calculator_card("Plasma Beta", "β = nkT / (B²/8π) [electron pressure only]"):
            with ui.column().classes('gap-4 w-full'):
                ui.number(
                    label="Magnetic Field (Gauss)",
                    value=self.magnetic_field,
                    on_change=lambda e: setattr(self, 'magnetic_field', e.value),
                    format='%.6g',
                ).classes('w-48')

                ui.number(
                    label="Electron Density (cm⁻³)",
                    value=self.electron_density,
                    on_change=lambda e: setattr(self, 'electron_density', e.value),
                    format='%.6g',
                ).classes('w-48')

                ui.number(
                    label="Plasma Temperature (eV)",
                    value=self.temperature,
                    on_change=lambda e: setattr(self, 'temperature', e.value),
                    format='%.6g',
                ).classes('w-48')

                action_buttons(self.calculate, self.reset)

                self.results.add_field("beta", "Plasma β", "")
                self.results.render()
