"""
Main Application Layout

Defines the sidebar navigation and content area for the application.
"""

from nicegui import ui

# Import all calculators
from .calculators.em.light_waves import LightWavesCalculator
from .calculators.em.skin_depth import SkinDepthCalculator
from .calculators.pulsed_power.transmission_line import TransmissionLineCalculator
from .calculators.pulsed_power.power_flux import PowerFluxCalculator
from .calculators.beams.moliere_scattering import MoliereScatteringCalculator
from .calculators.beams.emittance import EmittanceCalculator
from .calculators.beams.beam_breakup import BeamBreakupCalculator
from .calculators.plasma.plasma_frequency import PlasmaFrequencyCalculator
from .calculators.plasma.cyclotron_frequency import CyclotronFrequencyCalculator
from .calculators.plasma.thermal_speed import ThermalSpeedCalculator
from .calculators.plasma.debye_length import DebyeLengthCalculator
from .calculators.plasma.alfven_speed import AlfvenSpeedCalculator
from .calculators.plasma.plasma_beta import PlasmaBetaCalculator
from .calculators.plasma.coulomb_rates import CoulombRatesCalculator
from .calculators.plasma.neutral_density import NeutralDensityCalculator
from .calculators.atomic.mass_conversion import MassConversionCalculator
from .calculators.atomic.ionization_table import IonizationTableDisplay
from .calculators.atomic.cross_sections import CrossSectionsDisplay
from .reference.integrals import IntegralsReference
from .reference.external_links import ExternalLinksReference


# Calculator registry
CALCULATORS = {
    # EM
    "light_waves": LightWavesCalculator,
    "skin_depth": SkinDepthCalculator,
    # Pulsed Power
    "transmission_line": TransmissionLineCalculator,
    "power_flux": PowerFluxCalculator,
    # Beams
    "moliere_scattering": MoliereScatteringCalculator,
    "emittance": EmittanceCalculator,
    "beam_breakup": BeamBreakupCalculator,
    # Plasma
    "plasma_frequency": PlasmaFrequencyCalculator,
    "cyclotron_frequency": CyclotronFrequencyCalculator,
    "thermal_speed": ThermalSpeedCalculator,
    "debye_length": DebyeLengthCalculator,
    "alfven_speed": AlfvenSpeedCalculator,
    "plasma_beta": PlasmaBetaCalculator,
    "coulomb_rates": CoulombRatesCalculator,
    "neutral_density": NeutralDensityCalculator,
    # Atomic
    "mass_conversion": MassConversionCalculator,
    "ionization_table": IonizationTableDisplay,
    "cross_sections": CrossSectionsDisplay,
    # Reference
    "integrals": IntegralsReference,
    "external_links": ExternalLinksReference,
}


class AppLayout:
    """Main application layout with sidebar navigation."""

    def __init__(self):
        self.current_calculator = None
        self.content_container = None
        self.calculator_instances = {}

    def show_calculator(self, name: str):
        """Display the selected calculator in the content area."""
        if self.content_container is None:
            return

        self.content_container.clear()

        # Get or create calculator instance
        if name not in self.calculator_instances:
            if name in CALCULATORS:
                self.calculator_instances[name] = CALCULATORS[name]()

        if name in self.calculator_instances:
            with self.content_container:
                self.calculator_instances[name].render()
            self.current_calculator = name

    def show_home(self):
        """Display the home/welcome page."""
        if self.content_container is None:
            return

        self.content_container.clear()
        with self.content_container:
            with ui.card().classes('w-full max-w-3xl q-pa-lg'):
                ui.label("Scientific Calculators").classes('text-h4 text-weight-medium')
                ui.separator().classes('q-my-md')

                ui.markdown('''
                Welcome to the Scientific Calculators application. This tool provides
                interactive calculators for various physics calculations including:

                - **Electromagnetic**: Light waves, skin depth
                - **Pulsed Power**: Transmission line impedance, power flux
                - **Beam Physics**: Moliere scattering, emittance, beam breakup
                - **Plasma Physics**: Plasma frequency, cyclotron frequency, thermal speed,
                  Debye length, Alfven speed, plasma beta, collision rates
                - **Atomic Physics**: Mass conversion, ionization energies, cross-sections

                Use the sidebar menu to navigate to different calculators.

                ---

                *Originally created by Thomas Hughes and Fiona Hughes.*
                ''')

    def create_layout(self):
        """Create the main application layout."""
        # Enable dark mode
        ui.dark_mode().enable()

        # Header
        with ui.header().classes('bg-primary items-center'):
            ui.button(on_click=lambda: drawer.toggle(), icon='menu').props('flat color=white')
            ui.label('Scientific Calculators').classes('text-h6 text-white')
            ui.space()
            ui.label('Physics Tools').classes('text-caption text-white')

        # Left drawer (sidebar)
        with ui.left_drawer(value=True, bordered=True).classes('bg-dark') as drawer:
            ui.label('Navigation').classes('text-subtitle1 q-pa-md text-grey-5')

            # Home link
            ui.item('Home', on_click=self.show_home).props('clickable').classes('text-white')

            ui.separator().classes('q-my-sm')

            # Electromagnetic
            with ui.expansion('Electromagnetic', icon='waves').classes('text-white'):
                ui.item('Light Waves', on_click=lambda: self.show_calculator('light_waves')).props('clickable dense')
                ui.item('Skin Depth', on_click=lambda: self.show_calculator('skin_depth')).props('clickable dense')

            # Pulsed Power
            with ui.expansion('Pulsed Power', icon='bolt').classes('text-white'):
                ui.item('Transmission Line', on_click=lambda: self.show_calculator('transmission_line')).props('clickable dense')
                ui.item('Power Flux', on_click=lambda: self.show_calculator('power_flux')).props('clickable dense')

            # Beams
            with ui.expansion('Beams', icon='scatter_plot').classes('text-white'):
                ui.item('Moliere Scattering', on_click=lambda: self.show_calculator('moliere_scattering')).props('clickable dense')
                ui.item('Emittance', on_click=lambda: self.show_calculator('emittance')).props('clickable dense')
                ui.item('Beam Breakup', on_click=lambda: self.show_calculator('beam_breakup')).props('clickable dense')

            # Plasma Physics
            with ui.expansion('Plasma Physics', icon='blur_on').classes('text-white'):
                ui.item('Plasma Frequency', on_click=lambda: self.show_calculator('plasma_frequency')).props('clickable dense')
                ui.item('Cyclotron Frequency', on_click=lambda: self.show_calculator('cyclotron_frequency')).props('clickable dense')
                ui.item('Thermal Speed', on_click=lambda: self.show_calculator('thermal_speed')).props('clickable dense')
                ui.item('Debye Length', on_click=lambda: self.show_calculator('debye_length')).props('clickable dense')
                ui.item('Alfven Speed', on_click=lambda: self.show_calculator('alfven_speed')).props('clickable dense')
                ui.item('Plasma Beta', on_click=lambda: self.show_calculator('plasma_beta')).props('clickable dense')
                ui.item('Coulomb Rates', on_click=lambda: self.show_calculator('coulomb_rates')).props('clickable dense')
                ui.item('Neutral Density', on_click=lambda: self.show_calculator('neutral_density')).props('clickable dense')

            # Atomic Physics
            with ui.expansion('Atomic Physics', icon='science').classes('text-white'):
                ui.item('Mass Conversion', on_click=lambda: self.show_calculator('mass_conversion')).props('clickable dense')
                ui.item('Ionization Energies', on_click=lambda: self.show_calculator('ionization_table')).props('clickable dense')
                ui.item('Cross Sections', on_click=lambda: self.show_calculator('cross_sections')).props('clickable dense')

            # Reference
            with ui.expansion('Reference', icon='menu_book').classes('text-white'):
                ui.item('Useful Integrals', on_click=lambda: self.show_calculator('integrals')).props('clickable dense')
                ui.item('External Links', on_click=lambda: self.show_calculator('external_links')).props('clickable dense')

        # Main content area
        with ui.column().classes('w-full items-center q-pa-md'):
            self.content_container = ui.column().classes('w-full max-w-4xl')

        # Show home page initially
        self.show_home()
