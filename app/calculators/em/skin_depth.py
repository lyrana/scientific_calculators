"""
Skin Depth Calculator

Calculate skin depth for electromagnetic waves in conductors.
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.em_formulas import calculate_skin_depth


class SkinDepthCalculator:
    """Calculator for skin depth in conductors."""

    def __init__(self):
        self.input_value = None
        self.input_type = "depth_m"
        self.permeability = 1.0
        self.conductivity = None
        self.results = ResultGroup("Results")
        self._input_field = None
        self._permea_field = None
        self._conduct_field = None

    def calculate(self):
        """Perform the calculation."""
        if self.input_value is None:
            ui.notify("Please enter an input value", type="warning")
            return
        if self.conductivity is None or self.conductivity <= 0:
            ui.notify("Please enter a valid conductivity", type="warning")
            return

        try:
            result = calculate_skin_depth(
                input_value=self.input_value,
                input_type=self.input_type,
                relative_permeability=self.permeability or 1.0,
                conductivity=self.conductivity,
            )

            if self.input_type in ["depth_m", "depth_cm"]:
                self.results.set_value("output", f"{format_scientific(result['frequency'])} Hz ({format_scientific(result['omega'])} rad/s)")
            else:
                self.results.set_value("output", f"{format_scientific(result['depth_m'])} m ({format_scientific(result['depth_cm'])} cm)")

        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        """Reset all inputs and outputs."""
        self.input_value = None
        self.permeability = 1.0
        self.conductivity = None
        if self._input_field:
            self._input_field.set_value(None)
        if self._permea_field:
            self._permea_field.set_value(1.0)
        if self._conduct_field:
            self._conduct_field.set_value(None)
        self.results.clear_all()

    def render(self):
        """Render the calculator UI."""
        with calculator_card("Skin Depth", "Calculate skin depth: δ = √(2/μσω)"):
            with ui.column().classes('gap-4 w-full'):
                # Input type selection
                ui.select(
                    options={
                        "depth_m": "Skin Depth (m)",
                        "depth_cm": "Skin Depth (cm)",
                        "frequency": "Frequency (Hz)",
                    },
                    value=self.input_type,
                    label="Input Type",
                    on_change=lambda e: setattr(self, 'input_type', e.value),
                ).classes('w-64')

                # Input value
                self._input_field = ui.number(
                    label="Value",
                    value=self.input_value,
                    on_change=lambda e: setattr(self, 'input_value', e.value),
                    format='%.6g',
                ).classes('w-64')

                # Material properties
                with ui.row().classes('gap-4'):
                    self._permea_field = ui.number(
                        label="Relative Permeability (μ_r)",
                        value=self.permeability,
                        on_change=lambda e: setattr(self, 'permeability', e.value),
                    ).classes('w-48')

                    self._conduct_field = ui.number(
                        label="Conductivity (S/m)",
                        value=self.conductivity,
                        on_change=lambda e: setattr(self, 'conductivity', e.value),
                        format='%.6g',
                    ).classes('w-48')

                action_buttons(self.calculate, self.reset)

                # Results
                self.results.add_field("output", "Result", "")
                self.results.render()
