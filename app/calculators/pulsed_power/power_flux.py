"""
Power Flux Calculator

Calculate Poynting flux and electric field relationships.
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.pulsed_power_formulas import calculate_power_flux


class PowerFluxCalculator:
    """Calculator for power flux (Poynting vector)."""

    def __init__(self):
        self.input_value = None
        self.input_type = "electric_field"
        self.results = ResultGroup("Results")

    def calculate(self):
        """Perform the calculation."""
        if self.input_value is None:
            ui.notify("Please enter an input value", type="warning")
            return

        try:
            result = calculate_power_flux(
                input_value=self.input_value,
                input_type=self.input_type,
            )

            if self.input_type == "electric_field":
                self.results.set_value("output1", f"{format_scientific(result['poynting_flux'])} watts/m²")
                self.results.set_value("output2", "")
            else:
                self.results.set_value("output1", f"{format_scientific(result['electric_field'])} V/m")
                self.results.set_value("output2", f"{format_scientific(result['magnetic_field'])} T")

        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        """Reset all inputs and outputs."""
        self.input_value = None
        self.results.clear_all()

    def render(self):
        """Render the calculator UI."""
        with calculator_card("Power Flux", "Calculate Poynting flux and field relationships"):
            with ui.column().classes('gap-4 w-full'):
                # Input type selection
                ui.select(
                    options={
                        "electric_field": "Electric Field Amplitude (V/m)",
                        "poynting_flux": "Poynting Flux (W/m²)",
                    },
                    value=self.input_type,
                    label="Input Type",
                    on_change=lambda e: setattr(self, 'input_type', e.value),
                ).classes('w-64')

                # Input value
                ui.number(
                    label="Value",
                    value=self.input_value,
                    on_change=lambda e: setattr(self, 'input_value', e.value),
                    format='%.6g',
                ).classes('w-64')

                action_buttons(self.calculate, self.reset)

                # Results
                self.results.add_field("output1", "Result 1", "")
                self.results.add_field("output2", "Magnetic Field", "")
                self.results.render()
