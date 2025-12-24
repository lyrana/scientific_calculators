"""
Coulomb Collision Rates Calculator
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.plasma_formulas import calculate_coulomb_rates


class CoulombRatesCalculator:
    """Calculator for Coulomb collision rates and transport coefficients."""

    def __init__(self):
        self.electron_density = None
        self.electron_temp = None
        self.ion_temp = None
        self.atomic_weight = None
        self.z = None
        self.results = ResultGroup("Results")

    def calculate(self):
        required = [self.electron_density, self.electron_temp, self.ion_temp,
                    self.atomic_weight, self.z]
        if any(v is None for v in required):
            ui.notify("Please enter all values", type="warning")
            return

        try:
            result = calculate_coulomb_rates(
                electron_density=self.electron_density,
                electron_temp=self.electron_temp,
                ion_temp=self.ion_temp,
                atomic_weight=self.atomic_weight,
                z=self.z,
            )

            self.results.set_value("lambda_ei", format_scientific(result['lambda_ei'], 3))
            self.results.set_value("lambda_ii", format_scientific(result['lambda_ii'], 3))
            self.results.set_value("nu_e", f"{format_scientific(result['nu_e'], 3)} /s")
            self.results.set_value("nu_i", f"{format_scientific(result['nu_i'], 3)} /s")
            self.results.set_value("sigma", f"{format_scientific(result['conductivity'], 3)} (Ω-cm)⁻¹")
            self.results.set_value("eta", f"{format_scientific(result['resistivity'], 3)} Ω-cm")

        except ValueError as e:
            ui.notify(str(e), type="warning")
        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        self.electron_density = None
        self.electron_temp = None
        self.ion_temp = None
        self.atomic_weight = None
        self.z = None
        self.results.clear_all()

    def render(self):
        with calculator_card("Coulomb Collision Rates", "Calculate collision frequencies and transport coefficients"):
            with ui.column().classes('gap-4 w-full'):
                with ui.row().classes('gap-4'):
                    ui.number(
                        label="Electron Density (cm⁻³)",
                        value=self.electron_density,
                        on_change=lambda e: setattr(self, 'electron_density', e.value),
                        format='%.6g',
                    ).classes('w-48')

                    ui.number(
                        label="Electron Temperature (eV)",
                        value=self.electron_temp,
                        on_change=lambda e: setattr(self, 'electron_temp', e.value),
                        format='%.6g',
                    ).classes('w-48')

                with ui.row().classes('gap-4'):
                    ui.number(
                        label="Ion Temperature (eV)",
                        value=self.ion_temp,
                        on_change=lambda e: setattr(self, 'ion_temp', e.value),
                        format='%.6g',
                    ).classes('w-48')

                    ui.number(
                        label="Atomic Weight (amu)",
                        value=self.atomic_weight,
                        on_change=lambda e: setattr(self, 'atomic_weight', e.value),
                        format='%.6g',
                    ).classes('w-48')

                ui.number(
                    label="Ion Charge State (Z)",
                    value=self.z,
                    on_change=lambda e: setattr(self, 'z', e.value),
                    format='%.6g',
                ).classes('w-40')

                action_buttons(self.calculate, self.reset)

                self.results.add_field("lambda_ei", "Coulomb Log (e-i)", "")
                self.results.add_field("lambda_ii", "Coulomb Log (i-i)", "")
                self.results.add_field("nu_e", "ν_e (e-i collision freq)", "")
                self.results.add_field("nu_i", "ν_i (i-i collision freq)", "")
                self.results.add_field("sigma", "Conductivity σ", "")
                self.results.add_field("eta", "Resistivity η", "")
                self.results.render()
