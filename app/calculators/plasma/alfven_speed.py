"""
Alfven Speed Calculator
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.plasma_formulas import calculate_alfven_speed


class AlfvenSpeedCalculator:
    """Calculator for Alfven speed."""

    def __init__(self):
        self.magnetic_field = None
        self.electron_density = None
        self.atomic_weight = None
        self.results = ResultGroup("Results")

    def calculate(self):
        if any(v is None for v in [self.magnetic_field, self.electron_density, self.atomic_weight]):
            ui.notify("Please enter all values", type="warning")
            return

        try:
            result = calculate_alfven_speed(
                self.magnetic_field,
                self.electron_density,
                self.atomic_weight
            )
            self.results.set_value("speed", f"{format_scientific(result['alfven_speed'], 3)} cm/s")
        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        self.magnetic_field = None
        self.electron_density = None
        self.atomic_weight = None
        self.results.clear_all()

    def render(self):
        with calculator_card("Alfven Speed", "v_A = 2.2×10¹¹ × B / √(n × A)"):
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
                    label="Atomic Weight (amu)",
                    value=self.atomic_weight,
                    on_change=lambda e: setattr(self, 'atomic_weight', e.value),
                    format='%.6g',
                ).classes('w-48')

                action_buttons(self.calculate, self.reset)

                self.results.add_field("speed", "Alfven Speed", "")
                self.results.render()
