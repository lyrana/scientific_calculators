"""
Transmission Line Impedance Calculator

Calculate characteristic impedance for coaxial and radial transmission lines.
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.pulsed_power_formulas import calculate_transmission_line_impedance


class TransmissionLineCalculator:
    """Calculator for transmission line impedance."""

    def __init__(self):
        self.line_type = "coaxial"
        self.dimension1 = None
        self.dimension2 = None
        self.permittivity = 1.0
        self.permeability = 1.0
        self.results = ResultGroup("Results")
        self._dim1_label = None
        self._dim2_label = None
        self._dim1_input = None
        self._dim2_input = None
        self._permit_field = None
        self._permea_field = None

    def _update_labels(self):
        """Update dimension labels based on line type."""
        if self.line_type == "coaxial":
            if self._dim1_label:
                self._dim1_label.set_text("Inner Radius (cm)")
            if self._dim2_label:
                self._dim2_label.set_text("Outer Radius (cm)")
        else:
            if self._dim1_label:
                self._dim1_label.set_text("Radius (cm)")
            if self._dim2_label:
                self._dim2_label.set_text("Width (cm)")

    def calculate(self):
        """Perform the calculation."""
        if self.dimension1 is None or self.dimension2 is None:
            ui.notify("Please enter both dimensions", type="warning")
            return

        try:
            result = calculate_transmission_line_impedance(
                line_type=self.line_type,
                dimension1=self.dimension1,
                dimension2=self.dimension2,
                relative_permittivity=self.permittivity or 1.0,
                relative_permeability=self.permeability or 1.0,
            )

            self.results.set_value("impedance", f"{format_scientific(result['impedance'])} ohms")

        except ValueError as e:
            ui.notify(str(e), type="warning")
        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        """Reset all inputs and outputs."""
        self.dimension1 = None
        self.dimension2 = None
        self.permittivity = 1.0
        self.permeability = 1.0
        if self._dim1_input:
            self._dim1_input.set_value(None)
        if self._dim2_input:
            self._dim2_input.set_value(None)
        if self._permit_field:
            self._permit_field.set_value(1.0)
        if self._permea_field:
            self._permea_field.set_value(1.0)
        self.results.clear_all()

    def render(self):
        """Render the calculator UI."""
        with calculator_card("Transmission Line Impedance", "Calculate characteristic impedance"):
            with ui.column().classes('gap-4 w-full'):
                # Line type selection
                def on_type_change(e):
                    self.line_type = e.value
                    self._update_labels()

                ui.radio(
                    options={"coaxial": "Coaxial", "radial": "Radial"},
                    value=self.line_type,
                    on_change=on_type_change,
                ).props('inline')

                # Dimensions
                with ui.row().classes('gap-4'):
                    with ui.column():
                        self._dim1_label = ui.label("Inner Radius (cm)").classes('text-caption')
                        ui.number(
                            value=self.dimension1,
                            on_change=lambda e: setattr(self, 'dimension1', e.value),
                            format='%.6g',
                        ).classes('w-40')

                    with ui.column():
                        self._dim2_label = ui.label("Outer Radius (cm)").classes('text-caption')
                        ui.number(
                            value=self.dimension2,
                            on_change=lambda e: setattr(self, 'dimension2', e.value),
                            format='%.6g',
                        ).classes('w-40')

                # Material properties
                with ui.row().classes('gap-4'):
                    ui.number(
                        label="Relative Permittivity (ε_r)",
                        value=self.permittivity,
                        on_change=lambda e: setattr(self, 'permittivity', e.value),
                    ).classes('w-48')

                    ui.number(
                        label="Relative Permeability (μ_r)",
                        value=self.permeability,
                        on_change=lambda e: setattr(self, 'permeability', e.value),
                    ).classes('w-48')

                action_buttons(self.calculate, self.reset)

                # Results
                self.results.add_field("impedance", "Impedance", "")
                self.results.render()
