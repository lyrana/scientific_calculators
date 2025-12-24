"""
Light Waves Calculator

Calculate light wave properties in different media.
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.em_formulas import calculate_light_waves


class LightWavesCalculator:
    """Calculator for light wave properties."""

    def __init__(self):
        self.input_value = None
        self.input_type = "wavelength_m"
        self.permittivity = 1.0
        self.permeability = 1.0
        self.results = ResultGroup("Results")

    def calculate(self):
        """Perform the calculation."""
        if self.input_value is None:
            ui.notify("Please enter an input value", type="warning")
            return

        try:
            result = calculate_light_waves(
                input_value=self.input_value,
                input_type=self.input_type,
                relative_permittivity=self.permittivity or 1.0,
                relative_permeability=self.permeability or 1.0,
            )

            # Update results
            self.results.set_value("light_speed", f"{format_scientific(result['light_speed_m'])} m/s ({format_scientific(result['light_speed_cm'])} cm/s)")

            if self.input_type in ["wavelength_m", "wavelength_cm"]:
                self.results.set_value("output", f"{format_scientific(result['frequency'])} Hz ({format_scientific(result['omega'])} rad/s)")
            else:
                self.results.set_value("output", f"{format_scientific(result['wavelength'])} m ({format_scientific(result['wavenumber'])} /m)")

        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        """Reset all inputs and outputs."""
        self.input_value = None
        self.permittivity = 1.0
        self.permeability = 1.0
        self.results.clear_all()
        if hasattr(self, '_input_field'):
            self._input_field.value = None
        if hasattr(self, '_permit_field'):
            self._permit_field.value = 1.0
        if hasattr(self, '_permea_field'):
            self._permea_field.value = 1.0

    def render(self):
        """Render the calculator UI."""
        with calculator_card("Light Waves", "Calculate light wave properties in a medium"):
            with ui.column().classes('gap-4 w-full'):
                # Input type selection
                ui.select(
                    options={
                        "wavelength_m": "Wavelength (m)",
                        "wavelength_cm": "Wavelength (cm)",
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
                    self._permit_field = ui.number(
                        label="Relative Permittivity (ε_r)",
                        value=self.permittivity,
                        on_change=lambda e: setattr(self, 'permittivity', e.value),
                    ).classes('w-48')

                    self._permea_field = ui.number(
                        label="Relative Permeability (μ_r)",
                        value=self.permeability,
                        on_change=lambda e: setattr(self, 'permeability', e.value),
                    ).classes('w-48')

                action_buttons(self.calculate, self.reset)

                # Results
                self.results.add_field("light_speed", "Light Speed", "")
                self.results.add_field("output", "Result", "")
                self.results.render()
