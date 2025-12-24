"""
Electron Cyclotron Frequency Calculator
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.plasma_formulas import calculate_cyclotron_frequency


class CyclotronFrequencyCalculator:
    """Calculator for electron cyclotron frequency."""

    def __init__(self):
        self.magnetic_field = None
        self.results = ResultGroup("Results")

    def calculate(self):
        if self.magnetic_field is None:
            ui.notify("Please enter magnetic field", type="warning")
            return

        try:
            result = calculate_cyclotron_frequency(self.magnetic_field)
            self.results.set_value("omega", f"{format_scientific(result['omega_ce'], 3)} rad/s (f = {format_scientific(result['f_ce'], 3)} Hz)")
        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        self.magnetic_field = None
        self.results.clear_all()

    def render(self):
        with calculator_card("Electron Cyclotron Frequency", "Ω_ce = eB/m_e c"):
            with ui.column().classes('gap-4 w-full'):
                ui.number(
                    label="Magnetic Field (Gauss)",
                    value=self.magnetic_field,
                    on_change=lambda e: setattr(self, 'magnetic_field', e.value),
                    format='%.6g',
                ).classes('w-48')

                action_buttons(self.calculate, self.reset)

                self.results.add_field("omega", "Cyclotron Frequency", "")
                self.results.render()
