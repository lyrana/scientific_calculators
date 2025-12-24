"""
Electron Plasma Frequency Calculator
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.plasma_formulas import calculate_plasma_frequency


class PlasmaFrequencyCalculator:
    """Calculator for electron plasma frequency."""

    def __init__(self):
        self.electron_density = None
        self.results = ResultGroup("Results")
        self._density_input = None

    def calculate(self):
        if self.electron_density is None:
            ui.notify("Please enter electron density", type="warning")
            return

        try:
            result = calculate_plasma_frequency(self.electron_density)
            self.results.set_value("omega", f"{format_scientific(result['omega_pe'], 3)} rad/s (f = {format_scientific(result['f_pe'], 3)} Hz)")
            self.results.set_value("skin", f"{format_scientific(result['skin_depth'], 3)} cm")
        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        self.electron_density = None
        if self._density_input:
            self._density_input.set_value(None)
        self.results.clear_all()

    def render(self):
        with calculator_card("Electron Plasma Frequency", "ω_pe = 8978 × √n_e"):
            with ui.column().classes('gap-4 w-full'):
                self._density_input = ui.number(
                    label="Electron Density (cm⁻³)",
                    value=self.electron_density,
                    on_change=lambda e: setattr(self, 'electron_density', e.value),
                    format='%.6g',
                ).classes('w-48')

                action_buttons(self.calculate, self.reset)

                self.results.add_field("omega", "Plasma Frequency", "")
                self.results.add_field("skin", "Collisionless Skin Depth", "")
                self.results.render()
