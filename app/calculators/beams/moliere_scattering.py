"""
Moliere Scattering Calculator

Calculate multiple scattering parameters for particle beams through foils.
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.beam_formulas import calculate_moliere_scattering
from ...physics.materials import MATERIALS


class MoliereScatteringCalculator:
    """Calculator for Moliere multiple scattering."""

    def __init__(self):
        self.thickness = None
        self.thickness_units = "mil"
        self.element = "aluminum"
        self.energy = None
        self.results = ResultGroup("Results")

    def calculate(self):
        """Perform the calculation."""
        if self.thickness is None or self.energy is None:
            ui.notify("Please enter thickness and energy", type="warning")
            return

        try:
            result = calculate_moliere_scattering(
                thickness=self.thickness,
                thickness_units=self.thickness_units,
                element=self.element,
                energy_mev=self.energy,
            )

            self.results.set_value("element", result['element_name'])
            self.results.set_value("thermal", format_scientific(result['thermal_momentum']))
            self.results.set_value("collisions", format_scientific(result['n_collisions']))
            self.results.set_value("theta", format_scientific(result['theta_rms']))

        except ValueError as e:
            ui.notify(str(e), type="warning")
        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        """Reset all inputs and outputs."""
        self.thickness = None
        self.energy = None
        self.results.clear_all()

    def render(self):
        """Render the calculator UI."""
        with calculator_card("Moliere Scattering", "Calculate multiple scattering through foils"):
            with ui.column().classes('gap-4 w-full'):
                # Thickness input
                with ui.row().classes('gap-4 items-end'):
                    ui.number(
                        label="Foil Thickness",
                        value=self.thickness,
                        on_change=lambda e: setattr(self, 'thickness', e.value),
                        format='%.6g',
                    ).classes('w-40')

                    ui.select(
                        options={"mil": "mil", "mm": "mm"},
                        value=self.thickness_units,
                        label="Units",
                        on_change=lambda e: setattr(self, 'thickness_units', e.value),
                    ).classes('w-24')

                # Element selection
                element_options = {key: mat["name"] for key, mat in MATERIALS.items()}
                ui.select(
                    options=element_options,
                    value=self.element,
                    label="Element",
                    on_change=lambda e: setattr(self, 'element', e.value),
                ).classes('w-48')

                # Energy input
                ui.number(
                    label="Beam Energy (MeV)",
                    value=self.energy,
                    on_change=lambda e: setattr(self, 'energy', e.value),
                    format='%.6g',
                ).classes('w-48')

                action_buttons(self.calculate, self.reset)

                # Results
                self.results.add_field("element", "Element", "")
                self.results.add_field("thermal", "Thermal Momentum (γβθ)", "")
                self.results.add_field("collisions", "Number of Collisions", "")
                self.results.add_field("theta", "Moliere 2D θ_rms", "rad")
                self.results.render()
