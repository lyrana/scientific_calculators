"""
External Links Reference Page
"""

from nicegui import ui
from ..components.calculator_card import calculator_card


class ExternalLinksReference:
    """Display external scientific resource links."""

    def render(self):
        with calculator_card("External Resources", "Links to scientific databases and tools"):
            with ui.column().classes('gap-6'):
                # Scientific Links
                ui.label("Scientific Links").classes('text-h6')
                with ui.column().classes('gap-2'):
                    ui.link(
                        "NRL Plasma Formulary",
                        "http://www.nrl.navy.mil/ppd/content/nrl-plasma-formulary",
                        new_tab=True,
                    )
                    ui.link(
                        "Pulse Power Formulary (PDF)",
                        "http://www.highvoltageprobes.com/_literature_89707/Pulsed_Power_Formulary",
                        new_tab=True,
                    )
                    ui.link(
                        "NIST ESTAR Database",
                        "http://physics.nist.gov/PhysRefData/Star/Text/ESTAR.html",
                        new_tab=True,
                    )
                    ui.link(
                        "Radiation Safety Information Computational Center (ORNL)",
                        "https://rsicc.ornl.gov/Default.aspx",
                        new_tab=True,
                    )

                ui.separator()

                # Solid-State Data
                ui.label("Solid-State Data").classes('text-h6')
                with ui.column().classes('gap-2'):
                    ui.link(
                        "Work functions for photoelectric effect",
                        "http://hyperphysics.phy-astr.gsu.edu/hbase/tables/photoelec.html",
                        new_tab=True,
                    )
                    ui.link(
                        "Fermi energies, temperatures, velocities",
                        "http://hyperphysics.phy-astr.gsu.edu/hbase/tables/fermi.html",
                        new_tab=True,
                    )

                ui.separator()

                # Related Software
                ui.label("Related Software").classes('text-h6')
                with ui.column().classes('gap-2'):
                    ui.link("Tcl/Tk", "https://www.tcl.tk", new_tab=True)
                    ui.link("Perl", "http://www.activestate.com/activeperl/downloads", new_tab=True)
                    ui.link("MPI Documentation", "http://www.mpi-forum.org/docs/docs.html", new_tab=True)
