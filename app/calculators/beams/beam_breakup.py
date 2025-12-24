"""
Beam Breakup (BBU) Instability Calculator

Calculate beam breakup instability parameters.
"""

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.beam_formulas import calculate_beam_breakup


class BeamBreakupCalculator:
    """Calculator for beam breakup instability."""

    def __init__(self):
        self.pulse_width = None  # ns
        self.frequency = None    # MHz
        self.b_field = None
        self.current = None
        self.n_gaps = None
        self.impedance = None
        self.q_factor = None
        self.results = ResultGroup("Results")

    def calculate(self):
        """Perform the calculation."""
        # Validate inputs
        required = [self.pulse_width, self.frequency, self.b_field,
                    self.current, self.n_gaps, self.impedance, self.q_factor]
        if any(v is None for v in required):
            ui.notify("Please enter all required values", type="warning")
            return

        try:
            result = calculate_beam_breakup(
                pulse_width_ns=self.pulse_width,
                frequency_mhz=self.frequency,
                b_field=self.b_field,
                current=self.current,
                n_gaps=self.n_gaps,
                impedance=self.impedance,
                q_factor=self.q_factor,
            )

            self.results.set_value("time", f"{format_scientific(result['time_max_growth'])} ns")
            self.results.set_value("damped", format_scientific(result.get('damped_response', 0)))
            self.results.set_value("delta", format_scientific(result.get('delta', 0)))

            if 'resonant_response' in result:
                self.results.set_value("resonant", format_scientific(result['resonant_response']))
            else:
                self.results.set_value("resonant", "--")

        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        """Reset all inputs and outputs."""
        self.pulse_width = None
        self.frequency = None
        self.b_field = None
        self.current = None
        self.n_gaps = None
        self.impedance = None
        self.q_factor = None
        self.results.clear_all()

    def render(self):
        """Render the calculator UI."""
        with calculator_card("Beam Breakup Instability", "Calculate BBU growth parameters"):
            with ui.column().classes('gap-4 w-full'):
                # Input grid
                with ui.row().classes('gap-4'):
                    ui.number(
                        label="Pulse Width (ns)",
                        value=self.pulse_width,
                        on_change=lambda e: setattr(self, 'pulse_width', e.value),
                        format='%.6g',
                    ).classes('w-40')

                    ui.number(
                        label="Frequency (MHz)",
                        value=self.frequency,
                        on_change=lambda e: setattr(self, 'frequency', e.value),
                        format='%.6g',
                    ).classes('w-40')

                with ui.row().classes('gap-4'):
                    ui.number(
                        label="B Field",
                        value=self.b_field,
                        on_change=lambda e: setattr(self, 'b_field', e.value),
                        format='%.6g',
                    ).classes('w-40')

                    ui.number(
                        label="Current",
                        value=self.current,
                        on_change=lambda e: setattr(self, 'current', e.value),
                        format='%.6g',
                    ).classes('w-40')

                with ui.row().classes('gap-4'):
                    ui.number(
                        label="Number of Gaps",
                        value=self.n_gaps,
                        on_change=lambda e: setattr(self, 'n_gaps', e.value),
                        format='%.6g',
                    ).classes('w-40')

                    ui.number(
                        label="Impedance (Z)",
                        value=self.impedance,
                        on_change=lambda e: setattr(self, 'impedance', e.value),
                        format='%.6g',
                    ).classes('w-40')

                ui.number(
                    label="Q Factor",
                    value=self.q_factor,
                    on_change=lambda e: setattr(self, 'q_factor', e.value),
                    format='%.6g',
                ).classes('w-40')

                action_buttons(self.calculate, self.reset)

                # Results
                self.results.add_field("time", "Time to Max Growth", "")
                self.results.add_field("damped", "Damped Response", "")
                self.results.add_field("delta", "Delta", "")
                self.results.add_field("resonant", "Resonant Response", "")
                self.results.render()
