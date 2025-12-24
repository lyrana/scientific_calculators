"""
Neutral Density Calculator
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.plasma_formulas import calculate_neutral_density


class NeutralDensityCalculator:
    """Calculator for neutral gas density from ideal gas law."""

    def __init__(self):
        self.pressure = None
        self.pressure_units = "torr"
        self.temperature = None
        self.results = ResultGroup("Results")

    def calculate(self):
        if self.pressure is None or self.temperature is None:
            ui.notify("Please enter pressure and temperature", type="warning")
            return

        try:
            result = calculate_neutral_density(
                pressure=self.pressure,
                pressure_units=self.pressure_units,
                temperature=self.temperature,
            )
            self.results.set_value("density", f"{format_scientific(result['neutral_density'], 3)} /cm³")
        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        self.pressure = None
        self.temperature = None
        self.results.clear_all()

    def render(self):
        with calculator_card("Neutral Density", "Ideal gas law: n = 2.687×10¹⁹ × (P/760) × (273/T)"):
            with ui.column().classes('gap-4 w-full'):
                with ui.row().classes('gap-4 items-end'):
                    ui.number(
                        label="Pressure",
                        value=self.pressure,
                        on_change=lambda e: setattr(self, 'pressure', e.value),
                        format='%.6g',
                    ).classes('w-40')

                    ui.select(
                        options={"torr": "torr", "Pa": "Pa"},
                        value=self.pressure_units,
                        label="Units",
                        on_change=lambda e: setattr(self, 'pressure_units', e.value),
                    ).classes('w-24')

                ui.number(
                    label="Temperature (K)",
                    value=self.temperature,
                    on_change=lambda e: setattr(self, 'temperature', e.value),
                    format='%.6g',
                ).classes('w-48')

                action_buttons(self.calculate, self.reset)

                self.results.add_field("density", "Neutral Density", "")
                self.results.render()
