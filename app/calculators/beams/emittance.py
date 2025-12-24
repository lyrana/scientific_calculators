"""
Transverse Emittance Calculator

Calculate transverse beam emittance from beam parameters.
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.beam_formulas import calculate_emittance


class EmittanceCalculator:
    """Calculator for transverse beam emittance."""

    def __init__(self):
        self.radius = None
        self.value = None
        self.value_type = "ev"
        self.results = ResultGroup("Results")

    def calculate(self):
        """Perform the calculation."""
        if self.radius is None or self.value is None:
            ui.notify("Please enter radius and temperature/angle", type="warning")
            return

        try:
            result = calculate_emittance(
                radius=self.radius,
                value=self.value,
                value_type=self.value_type,
            )

            if self.value_type == "ev":
                self.results.set_value("convert", f"{format_scientific(result['angle'])} rad")
            else:
                self.results.set_value("convert", f"{format_scientific(result['temperature'])} eV")

            self.results.set_value("emittance", f"{format_scientific(result['emittance'])} cm-rad")

        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        """Reset all inputs and outputs."""
        self.radius = None
        self.value = None
        self.results.clear_all()

    def render(self):
        """Render the calculator UI."""
        with calculator_card("Transverse Emittance", "Calculate beam emittance from thermal properties"):
            with ui.column().classes('gap-4 w-full'):
                # Radius input
                ui.number(
                    label="Beam Radius (cm)",
                    value=self.radius,
                    on_change=lambda e: setattr(self, 'radius', e.value),
                    format='%.6g',
                ).classes('w-48')

                # Value type selection
                with ui.row().classes('gap-4 items-end'):
                    ui.number(
                        label="Value",
                        value=self.value,
                        on_change=lambda e: setattr(self, 'value', e.value),
                        format='%.6g',
                    ).classes('w-40')

                    ui.select(
                        options={"ev": "Temperature (eV)", "radians": "Angle (rad)"},
                        value=self.value_type,
                        label="Type",
                        on_change=lambda e: setattr(self, 'value_type', e.value),
                    ).classes('w-40')

                action_buttons(self.calculate, self.reset)

                # Results
                self.results.add_field("convert", "Converted Value", "")
                self.results.add_field("emittance", "Emittance", "")
                self.results.render()
