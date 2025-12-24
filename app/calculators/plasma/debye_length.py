"""
Debye Length Calculator
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.plasma_formulas import calculate_debye_length


class DebyeLengthCalculator:
    """Calculator for Debye length."""

    def __init__(self):
        self.electron_density = None
        self.temperature = None
        self.results = ResultGroup("Results")
        self._density_input = None
        self._temp_input = None

    def calculate(self):
        if self.electron_density is None or self.temperature is None:
            ui.notify("Please enter density and temperature", type="warning")
            return

        try:
            result = calculate_debye_length(self.electron_density, self.temperature)
            self.results.set_value("debye", f"{format_scientific(result['debye_length'], 3)} cm")
        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        self.electron_density = None
        self.temperature = None
        if self._density_input:
            self._density_input.set_value(None)
        if self._temp_input:
            self._temp_input.set_value(None)
        self.results.clear_all()


    def render(self):
        with calculator_card("Debye Length", "λ_D = 743.5 × √(T/n)"):
            with ui.column().classes('gap-4 w-full'):
                self._density_input = ui.number(
                    label="Electron Density (cm⁻³)",
                    value=self.electron_density,
                    on_change=lambda e: setattr(self, 'electron_density', e.value),
                    format='%.6g',
                ).classes('w-48')

                self._temp_input = ui.number(
                    label="Plasma Temperature (eV)",
                    value=self.temperature,
                    on_change=lambda e: setattr(self, 'temperature', e.value),
                    format='%.6g',
                ).classes('w-48')

                action_buttons(self.calculate, self.reset)

                self.results.add_field("debye", "Debye Length", "")
                self.results.render()
