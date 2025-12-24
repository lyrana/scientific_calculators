"""
Electron Thermal Speed Calculator
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.plasma_formulas import calculate_thermal_speed


class ThermalSpeedCalculator:
    """Calculator for electron thermal speed."""

    def __init__(self):
        self.temperature = None
        self.results = ResultGroup("Results")

    def calculate(self):
        if self.temperature is None:
            ui.notify("Please enter temperature", type="warning")
            return

        try:
            result = calculate_thermal_speed(self.temperature)
            self.results.set_value("speed", f"{format_scientific(result['thermal_speed'], 3)} cm/s")
        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        self.temperature = None
        self.results.clear_all()

    def render(self):
        with calculator_card("Electron Thermal Speed", "v_th = √(T_eV/511000) × c"):
            with ui.column().classes('gap-4 w-full'):
                ui.number(
                    label="Electron Temperature (eV)",
                    value=self.temperature,
                    on_change=lambda e: setattr(self, 'temperature', e.value),
                    format='%.6g',
                ).classes('w-48')

                action_buttons(self.calculate, self.reset)

                self.results.add_field("speed", "Thermal Speed", "")
                self.results.render()
