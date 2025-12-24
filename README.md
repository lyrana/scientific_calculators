# Scientific Calculators

A modern NiceGUI-based web application for physics calculations. This application provides interactive calculators for electromagnetic, plasma physics, beam physics, and atomic physics formulas.

Originally created by Thomas Hughes and Fiona Hughes, refactored to Python/NiceGUI.

## Features

- **15+ Interactive Calculators** across 5 physics domains
- **Dark Theme** with modern Quasar UI components
- **Sidebar Navigation** for easy access to all calculators
- **Real-time Calculations** with input validation
- **Cross-section Image Gallery** with electron scattering data
- **Reference Tables** for ionization energies and useful integrals

## Requirements

- Python 3.10 or higher
- nicegui >= 2.0.0

## Installation

```bash
# Clone the repository (if applicable)
cd scientific_calculators

# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

- **Default Port:** 8080
- **Access URL:** http://localhost:8080
- **Auto-reload:** Enabled in development mode

The application will start and you can access it in your web browser.

## Project Structure

```
scientific_calculators/
├── main.py                      # Entry point - run this to start the app
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
└── app/
    ├── __init__.py
    ├── layout.py                # Main layout with sidebar navigation
    │
    ├── components/              # Reusable UI components
    │   ├── calculator_card.py   # Card wrapper for calculators
    │   ├── input_field.py       # Input field helpers
    │   ├── result_display.py    # Result formatting and display
    │   └── action_buttons.py    # Calculate/Reset button pair
    │
    ├── calculators/             # Calculator UI modules
    │   ├── em/                  # Electromagnetic calculators
    │   │   ├── light_waves.py
    │   │   └── skin_depth.py
    │   ├── pulsed_power/        # Pulsed power calculators
    │   │   ├── transmission_line.py
    │   │   └── power_flux.py
    │   ├── beams/               # Beam physics calculators
    │   │   ├── moliere_scattering.py
    │   │   ├── emittance.py
    │   │   └── beam_breakup.py
    │   ├── plasma/              # Plasma physics calculators
    │   │   ├── plasma_frequency.py
    │   │   ├── cyclotron_frequency.py
    │   │   ├── thermal_speed.py
    │   │   ├── debye_length.py
    │   │   ├── alfven_speed.py
    │   │   ├── plasma_beta.py
    │   │   ├── coulomb_rates.py
    │   │   └── neutral_density.py
    │   └── atomic/              # Atomic physics calculators
    │       ├── mass_conversion.py
    │       ├── ionization_table.py
    │       └── cross_sections.py
    │
    ├── physics/                 # Calculation logic (pure Python)
    │   ├── constants.py         # Physical constants
    │   ├── materials.py         # Material properties database
    │   └── formulas/            # Physics formulas
    │       ├── em_formulas.py
    │       ├── pulsed_power_formulas.py
    │       ├── beam_formulas.py
    │       ├── plasma_formulas.py
    │       └── atomic_formulas.py
    │
    ├── reference/               # Static content pages
    │   ├── integrals.py
    │   └── external_links.py
    │
    └── static/
        └── pngs/                # Cross-section images
            ├── ar2002.png
            ├── cesium.png
            ├── h2_2001.png
            ├── h2o2004.png
            ├── he2002.png
            ├── hg2003.png
            ├── n22003.png
            └── ox2004.png
```

## Available Calculators

### Electromagnetic
| Calculator | Description |
|------------|-------------|
| Light Waves | Calculate light speed, frequency, and wavelength in a medium |
| Skin Depth | Calculate skin depth for EM waves in conductors |

### Pulsed Power
| Calculator | Description |
|------------|-------------|
| Transmission Line | Calculate impedance for coaxial and radial lines |
| Power Flux | Convert between E-field and Poynting flux |

### Beam Physics
| Calculator | Description |
|------------|-------------|
| Moliere Scattering | Multiple scattering through foils |
| Emittance | Transverse beam emittance from thermal properties |
| Beam Breakup | BBU instability growth parameters |

### Plasma Physics
| Calculator | Description |
|------------|-------------|
| Plasma Frequency | Electron plasma frequency and skin depth |
| Cyclotron Frequency | Electron cyclotron frequency |
| Thermal Speed | Electron thermal speed |
| Debye Length | Plasma Debye length |
| Alfven Speed | Alfven wave speed |
| Plasma Beta | Plasma pressure to magnetic pressure ratio |
| Coulomb Rates | Collision frequencies and transport coefficients |
| Neutral Density | Neutral gas density from ideal gas law |

### Atomic Physics
| Calculator | Description |
|------------|-------------|
| Mass Conversion | Convert atomic mass units to kg |
| Ionization Energies | Reference table of ionization energies |
| Cross Sections | Electron scattering cross-section plots |

## How to Add New Calculators

### Step 1: Add the formula (physics layer)

Create or edit a file in `app/physics/formulas/`:

```python
# In app/physics/formulas/my_formulas.py

def my_new_formula(input1: float, input2: float) -> dict:
    """
    Calculate something useful.

    Args:
        input1: Description with units (e.g., "Pressure in Pa")
        input2: Description with units

    Returns:
        dict with result keys and values
    """
    result = input1 * input2  # Your formula here
    return {'result': result}
```

### Step 2: Create the calculator UI

Create a new file in `app/calculators/<category>/`:

```python
# In app/calculators/<category>/my_calculator.py

from nicegui import ui
from ...components.calculator_card import calculator_card
from ...components.action_buttons import action_buttons
from ...components.result_display import ResultGroup, format_scientific
from ...physics.formulas.my_formulas import my_new_formula


class MyCalculator:
    def __init__(self):
        self.input1 = None
        self.input2 = None
        self.results = ResultGroup("Results")

    def calculate(self):
        if self.input1 is None or self.input2 is None:
            ui.notify("Please enter all values", type="warning")
            return

        try:
            result = my_new_formula(self.input1, self.input2)
            self.results.set_value("result", f"{format_scientific(result['result'])} units")
        except Exception as e:
            ui.notify(f"Calculation error: {e}", type="negative")

    def reset(self):
        self.input1 = None
        self.input2 = None
        self.results.clear_all()

    def render(self):
        with calculator_card("My Calculator", "Description of what it calculates"):
            with ui.column().classes('gap-4 w-full'):
                ui.number(
                    label="Input 1 (units)",
                    value=self.input1,
                    on_change=lambda e: setattr(self, 'input1', e.value),
                ).classes('w-48')

                ui.number(
                    label="Input 2 (units)",
                    value=self.input2,
                    on_change=lambda e: setattr(self, 'input2', e.value),
                ).classes('w-48')

                action_buttons(self.calculate, self.reset)

                self.results.add_field("result", "Result Label", "units")
                self.results.render()
```

### Step 3: Register in the layout

Edit `app/layout.py`:

```python
# Add import at the top
from .calculators.<category>.my_calculator import MyCalculator

# Add to CALCULATORS dict
CALCULATORS = {
    ...
    "my_calculator": MyCalculator,
}

# Add to sidebar in create_layout() method
with ui.expansion('<Category>', icon='icon_name').classes('text-white'):
    ...
    ui.item('My Calculator', on_click=lambda: self.show_calculator('my_calculator')).props('clickable dense')
```

## Adding Physical Constants

Edit `app/physics/constants.py`:

```python
# Add your constant with units documented
MY_CONSTANT = 1.234e-5  # units (system: CGS or MKS)
```

## Adding Materials

Edit `app/physics/materials.py`:

```python
MATERIALS = {
    ...
    'new_material': {
        'density': 1.0,      # g/cm³
        'g_mole': 12.0,      # g/mol
        'z': 6,              # atomic number
        'name': 'Display Name',
    },
}
```

## Code Style Guidelines

- Use type hints for all function parameters and returns
- Document formulas with docstrings including units
- Keep UI (calculators/) separate from logic (physics/formulas/)
- Use scientific notation formatting: `format_scientific(value, precision)`
- CGS units for beam/plasma calculations (as in original)
- MKS units for EM calculations (as in original)

## Unit Systems

The application uses two unit systems, matching the original implementation:

| Domain | Unit System | Examples |
|--------|-------------|----------|
| Electromagnetic | MKS (SI) | meters, Hz, ohms |
| Plasma Physics | CGS | cm, Gauss, eV |
| Beam Physics | CGS | cm, MeV, g/cm³ |

## Testing

To verify calculations:
1. Compare results against known physics values
2. Test edge cases (zero, negative, very large values)
3. Cross-reference with the original JavaScript implementation

## License

Original work Copyright 2005-2007 by Thomas Hughes and Fiona Hughes.

## External Resources

- [NRL Plasma Formulary](http://www.nrl.navy.mil/ppd/content/nrl-plasma-formulary)
- [NIST ESTAR Database](http://physics.nist.gov/PhysRefData/Star/Text/ESTAR.html)
- [Magboltz Cross-section Data (CERN)](http://rjd.web.cern.ch/rjd/cgi-bin/cross/)
