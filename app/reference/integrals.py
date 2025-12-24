"""
Useful Integrals Reference Page
"""

from nicegui import ui
from ..components.calculator_card import calculator_card


class IntegralsReference:
    """Display useful Gaussian integrals."""

    def render(self):
        with calculator_card("Useful Integrals", "Gaussian function integrals"):
            with ui.column().classes('gap-4'):
                # Function definition
                ui.html('''
                    <div style="font-family: 'Times New Roman', serif; font-size: 1.2em; line-height: 2;">
                        <p>Let f(x) = e<sup>-x²/a²</sup></p>
                        <p>Standard Deviation = a/√2</p>
                    </div>
                ''')

                ui.separator()

                # Integrals
                ui.html('''
                    <div style="font-family: 'Times New Roman', serif; font-size: 1.2em; line-height: 2.5;">
                        <p>∫<sub>-∞</sub><sup>∞</sup> f(x)dx = a√π</p>

                        <p>∫<sub>0</sub><sup>∞</sup> f(r)r dr = a²/2</p>

                        <table style="border-collapse: collapse;">
                            <tr>
                                <td rowspan="3" style="vertical-align: middle; padding-right: 10px;">⟨r²⟩ = </td>
                                <td style="text-align: center;">∫<sub>0</sub><sup>∞</sup> f(r)r³ dr</td>
                                <td rowspan="3" style="vertical-align: middle; padding-left: 10px;">= a²</td>
                            </tr>
                            <tr>
                                <td style="border-bottom: 1px solid currentColor; text-align: center;">―――――――</td>
                            </tr>
                            <tr>
                                <td style="text-align: center;">∫<sub>0</sub><sup>∞</sup> f(r)r dr</td>
                            </tr>
                        </table>
                    </div>
                ''')
