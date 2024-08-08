import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyperclip

class UnitConverter:
    def __init__(self, master):
        self.master = master
        master.title("Multi-Unit Converter")

        # Create dictionaries to store units and their conversion factors
        self.units = {
            "Length": {
                "Kilometer (km)": 1000,
                "Meter (m)": 1,
                "Centimeter (cm)": 0.01,
                "Millimeter (mm)": 0.001,
                "Micrometer (µm)": 1e-6,
                "Nanometer (nm)": 1e-9,
                "Mile (mi)": 1609.34,
                "Yard (yd)": 0.9144,
                "Foot (ft)": 0.3048,
                "Inch (in)": 0.0254,
                "Nautical Mile (nmi)": 1852,
                "Astronomical Unit (AU)": 1.496e11,
                "Light-year (ly)": 9.461e15,
                "Picometer (pm)": 1e-12,
                "Femtometer (fm)": 1e-15,
                "Attometer (am)": 1e-18,
                "Zeptometer (zm)": 1e-21,
                "Yoctometer (ym)": 1e-24,
                "Decimeter (dm)": 0.1,
                "Dekameter (dam)": 10,
                "Hectometer (hm)": 100,
                "Megameter (Mm)": 1e6,
                "Gigameter (Gm)": 1e9,
                "Terameter (Tm)": 1e12,
                "Petameter (Pm)": 1e15
            },
            "Weight/Mass": {
                "Kilogram (kg)": 1,
                "Gram (g)": 0.001,
                "Milligram (mg)": 1e-6,
                "Microgram (µg)": 1e-9,
                "Metric Ton (t)": 1000,
                "Pound (lb)": 0.453592,
                "Ounce (oz)": 0.0283495,
                "Stone (st)": 6.35029,
                "Ton (short ton)": 907.185,
                "Long Ton (imperial ton)": 1016.05,
                "Carat (ct)": 0.0002,
                "Grain (gr)": 6.479891e-5,
                "Slug (slug)": 14.5939,
                "Atomic Mass Unit (amu)": 1.66054e-27,
                "Planck Mass (mP)": 2.17647e-8,
                "Electronvolt/c² (eV/c²)": 1.78266e-36,
                "Solar Mass (M☉)": 1.989e30,
                "Earth Mass (M⊕)": 5.972e24,
                "Jupiter Mass (MJ)": 1.898e27,
                "Kilogram-force (kgf)": 9.80665,
                "Pound-force (lbf)": 4.44822,
                "Dyne (dyn)": 1e-5,
                "Newton (N)": 1,
                "Poundal (pdl)": 0.138255,
                "Kip (kip)": 4448.22
            },
            "Temperature": {
                "Celsius (°C)": 1, 
                "Fahrenheit (°F)": 1, 
                "Kelvin (K)": 1, 
                "Rankine (°R)": 1, 
                "Réaumur (°Ré)": 1, 
                "Delisle (°De)": 1, 
                "Newton (°N)": 1, 
                "Rømer (°Rø)": 1
            },
            "Volume": {
                "Liter (L)": 1,
                "Milliliter (mL)": 0.001,
                "Cubic Meter (m³)": 1000,
                "Cubic Centimeter (cm³)": 1e-6,
                "Cubic Millimeter (mm³)": 1e-9,
                "Gallon (US)": 3.78541,
                "Gallon (Imperial)": 4.54609,
                "Quart (US)": 0.946353,
                "Quart (Imperial)": 1.13652,
                "Pint (US)": 0.473176,
                "Pint (Imperial)": 0.568261,
                "Cup (US)": 0.236588,
                "Cup (Imperial)": 0.284131,
                "Fluid Ounce (US)": 2.95735e-5,
                "Fluid Ounce (Imperial)": 2.84131e-5,
                "Tablespoon (US)": 1.47868e-5,
                "Tablespoon (Imperial)": 1.77582e-5,
                "Teaspoon (US)": 4.92892e-6,
                "Teaspoon (Imperial)": 5.91939e-6,
                "Cubic Yard (yd³)": 0.764555,
                "Cubic Foot (ft³)": 0.0283168,
                "Cubic Inch (in³)": 1.63871e-5,
                "Acre-foot (acre-ft)": 1233.48,
                "Barrel (oil)": 158.987,
                "Board Foot (FBM)": 2.35974e-3
            },
            "Area": {
                "Square Meter (m²)": 1,
                "Square Kilometer (km²)": 1e6,
                "Square Centimeter (cm²)": 1e-4,
                "Square Millimeter (mm²)": 1e-6,
                "Hectare (ha)": 1e4,
                "Square Mile (mi²)": 2.59e6,
                "Square Yard (yd²)": 0.836127,
                "Square Foot (ft²)": 9.2903e-4,
                "Square Inch (in²)": 6.4516e-4,
                "Acre (acre)": 4046.86,
                "Barn (b)": 1e-28
            },
            "Time": {
                "Second (s)": 1,
                "Minute (min)": 60,
                "Hour (h)": 3600,
                "Day (d)": 86400,
                "Week (wk)": 604800,
                "Month (mo)": 2.628e6,  # Approximate average month
                "Year (yr)": 3.1536e7,  # Approximate average year
                "Decade": 3.1536e8,
                "Century": 3.1536e9,
                "Millennium": 3.1536e12,
                "Millisecond (ms)": 0.001,
                "Microsecond (µs)": 1e-6,
                "Nanosecond (ns)": 1e-9,
                "Picosecond (ps)": 1e-12,
                "Femtosecond (fs)": 1e-15,
                "Attosecond (as)": 1e-18,
                "Zeptosecond (zs)": 1e-21,
                "Yoctosecond (ys)": 1e-24,
                "Sidereal Day": 86164.1,
                "Sidereal Year": 3.15581e7,
                "Planck Time (tP)": 5.391e-44
            },
            "Speed": {
                "Meter per Second (m/s)": 1,
                "Kilometer per Hour (km/h)": 0.277778,
                "Mile per Hour (mph)": 0.44704,
                "Knot (kn)": 0.514444,
                "Foot per Second (ft/s)": 0.3048,
                "Inch per Second (in/s)": 0.0254,
                "Speed of Light (c)": 299792458,
                "Mach Number (Ma)": 343  # Approximate at sea level
            },
            "Digital Storage": {
                "Bit (b)": 1,
                "Byte (B)": 8,
                "Kilobyte (KB)": 8192,
                "Megabyte (MB)": 8.38861e6,
                "Gigabyte (GB)": 8.58993e9,
                "Terabyte (TB)": 8.8e12,
                "Petabyte (PB)": 9.0072e15,
                "Exabyte (EB)": 9.22337e18,
                "Zettabyte (ZB)": 9.44473e21,
                "Yottabyte (YB)": 9.67141e24,
                "Kibibyte (KiB)": 1024,
                "Mebibyte (MiB)": 1.04858e6,
                "Gibibyte (GiB)": 1.07374e9,
                "Tebibyte (TiB)": 1.09951e12,
                "Pebibyte (PiB)": 1.1259e15,
                "Exbibyte (EiB)": 1.15292e18,
                "Zebibyte (ZiB)": 1.18059e21,
                "Yobibyte (YiB)": 1.20893e24
            },
            "Energy": {
                "Joule (J)": 1,
                "Kilojoule (kJ)": 1000,
                "Megajoule (MJ)": 1e6,
                "Gigajoule (GJ)": 1e9,
                "Terajoule (TJ)": 1e12,
                "Calorie (cal)": 4.184,
                "Kilocalorie (kcal)": 4184,
                "British Thermal Unit (BTU)": 1055.06,
                "Electronvolt (eV)": 1.60218e-19,
                "Kiloelectronvolt (keV)": 1.60218e-16,
                "Megaelectronvolt (MeV)": 1.60218e-13,
                "Gigaelectronvolt (GeV)": 1.60218e-10,
                "Teraelectronvolt (TeV)": 1.60218e-7,
                "Erg (erg)": 1e-7,
                "Foot-pound (ft·lb)": 1.35582,
                "Kilowatt-hour (kWh)": 3.6e6,
                "Therm": 1e5,
                "Quad (quadrillion BTU)": 1.055e18,
                "Ton of TNT equivalent": 4.184e9
            },
            "Pressure": {
                "Pascal (Pa)": 1,
                "Kilopascal (kPa)": 1000,
                "Megapascal (MPa)": 1e6,
                "Gigapascal (GPa)": 1e9,
                "Bar (bar)": 100000,
                "Millibar (mbar)": 100,
                "Atmosphere (atm)": 101325,
                "Torr (Torr)": 133.322,
                "Millimeter of Mercury (mmHg)": 133.322,
                "Inches of Mercury (inHg)": 3386.39,
                "Pounds per Square Inch (psi)": 6894.76,
                "Pounds per Square Foot (psf)": 47.8803,
                "Kilograms per Square Centimeter ( kg/cm ²)": 98066.5,
                "Dynes per Square Centimeter (dyn/cm²)": 0.1
            },
            "Power": {
                "Watt (W)": 1,
                "Kilowatt (kW)": 1000,
                "Megawatt (MW)": 1e6,
                "Gigawatt (GW)": 1e9,
                "Terawatt (TW)": 1e12,
                "Horsepower (hp)": 745.7,
                "Metric Horsepower (PS)": 735.499,
                "British Thermal Unit per Hour (BTU/h)": 0.293071,
                "Foot-pound per Second (ft·lb/s)": 1.35582,
                "Erg per Second (erg/s)": 1e-7
            },
            "Angle": {
                "Degree (°)": 1,
                "Radian (rad)": 57.2958,
                "Gradian (grad)": 0.9,
                "Minute of Arc (')": (1/60),
                "Second of Arc (\")": (1/3600),
                "Milliradian (mrad)": 17.4533,
                "Turn (revolution)": 360,
                "Quadrant": 90,
                "Sextant": 60
            },
            "Frequency": {
                "Hertz (Hz)": 1,
                "Kilohertz (kHz)": 1000,
                "Megahertz (MHz)": 1e6,
                "Gigahertz (GHz)": 1e9,
                "Terahertz (THz)": 1e12,
                "Cycles per Second (cps)": 1,
                "Revolutions per Minute (RPM)": 1/60,
                "Radians per Second (rad/s)": 2 * 3.141592653589793 # Approximation of pi
            }
        }

        # ... (GUI Elements)
        self.input_label = tk.Label(master, text="Enter value:")
        self.input_label.grid(row=1, column=0, padx=5, pady=5)

        self.input_entry = tk.Entry(master)
        self.input_entry.grid(row=1, column=1, padx=5, pady=5)

        self.output_label = tk.Label(master, text="Converted value:")
        self.output_label.grid(row=3, column=0, padx=5, pady=5)

        self.output_entry = tk.Entry(master, state="readonly")
        self.output_entry.grid(row=3, column=1, padx=5, pady=5)

        # ... (Dropdown Menus)
        self.category_label = tk.Label(master, text="Select category:")
        self.category_label.grid(row=0, column=0, padx=5, pady=5)

        self.category_var = tk.StringVar(master)
        self.category_dropdown = ttk.Combobox(
            master, textvariable=self.category_var, values=list(self.units.keys())
        )
        self.category_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.category_dropdown.current(0)
        self.category_dropdown.bind("<<ComboboxSelected>>", self.update_unit_dropdowns)

        self.from_unit_label = tk.Label(master, text="From unit:")
        self.from_unit_label.grid(row=2, column=0, padx=5, pady=5)

        self.from_unit_var = tk.StringVar(master)
        self.from_unit_dropdown = ttk.Combobox(master, textvariable=self.from_unit_var)
        self.from_unit_dropdown.grid(row=2, column=1, padx=5, pady=5)

        self.to_unit_label = tk.Label(master, text="To unit:")
        self.to_unit_label.grid(row=2, column=2, padx=5, pady=5)

        self.to_unit_var = tk.StringVar(master)
        self.to_unit_dropdown = ttk.Combobox(master, textvariable=self.to_unit_var)
        self.to_unit_dropdown.grid(row=2, column=3, padx=5, pady=5)

        self.update_unit_dropdowns()

        # ... (Buttons)
        self.convert_button = tk.Button(master, text="Convert", command=self.convert)
        self.convert_button.grid(row=3, column=3, padx=5, pady=5)

        self.clear_button = tk.Button(master, text="Clear", command=self.clear)
        self.clear_button.grid(row=1, column=3, padx=5, pady=5)

        self.copy_button = tk.Button(
            master, text="Copy", command=self.copy_to_clipboard
        )
        self.copy_button.grid(row=3, column=2, padx=5, pady=5)

    def update_unit_dropdowns(self, event=None):
        selected_category = self.category_var.get()
        units = list(self.units[selected_category].keys())
        self.from_unit_dropdown["values"] = units
        self.to_unit_dropdown["values"] = units
        self.from_unit_dropdown.current(0)
        self.to_unit_dropdown.current(1)

    # ... (Conversion Functions)
    def celsius_to_fahrenheit(self, celsius):
        return (celsius * 9 / 5) + 32

    def fahrenheit_to_celsius(self, fahrenheit):
        return (fahrenheit - 32) * 5 / 9

    def celsius_to_kelvin(self, celsius):
        return celsius + 273.15

    def kelvin_to_celsius(self, kelvin):
        return kelvin - 273.15

    def fahrenheit_to_kelvin(self, fahrenheit):
        return (fahrenheit + 459.67) * 5 / 9

    def kelvin_to_fahrenheit(self, kelvin):
        return kelvin * 9 / 5 - 459.67

    def celsius_to_reaumur(self, celsius):
        return celsius * 4 / 5

    def reaumur_to_celsius(self, reaumur):
        return reaumur * 5 / 4

    def fahrenheit_to_reaumur(self, fahrenheit):
        return (fahrenheit - 32) * 4 / 9

    def reaumur_to_fahrenheit(self, reaumur):
        return reaumur * 9 / 4 + 32

    def celsius_to_delisle(self, celsius):
        return (100 - celsius) * 3 / 2

    def delisle_to_celsius(self, delisle):
        return 100 - delisle * 2 / 3

    def fahrenheit_to_delisle(self, fahrenheit):
        return (212 - fahrenheit) * 5 / 6

    def delisle_to_fahrenheit(self, delisle):
        return 212 - delisle * 6 / 5

    def celsius_to_newton(self, celsius):
        return celsius * 33 / 100

    def newton_to_celsius(self, newton):
        return newton * 100 / 33

    def fahrenheit_to_newton(self, fahrenheit):
        return (fahrenheit - 32) * 11 / 60

    def newton_to_fahrenheit(self, newton):
        return newton * 60 / 11 + 32

    def celsius_to_romer(self, celsius):
        return celsius * 21 / 40 + 7.5

    def romer_to_celsius(self, romer):
        return (romer - 7.5) * 40 / 21

    def fahrenheit_to_romer(self, fahrenheit):
        return (fahrenheit - 32) * 7 / 24 + 7.5

    def romer_to_fahrenheit(self, romer):
        return (romer - 7.5) * 24 / 7 + 32


    def convert(self):
        try:
            value = float(self.input_entry.get())
            from_unit = self.from_unit_var.get()
            to_unit = self.to_unit_var.get()
            selected_category = self.category_var.get()

            if selected_category == "Temperature":
                if from_unit == "Celsius (°C)" and to_unit == "Fahrenheit (°F)":
                    converted_value = self.celsius_to_fahrenheit(value)
                elif from_unit == "Fahrenheit (°F)" and to_unit == "Celsius (°C)":
                    converted_value = self.fahrenheit_to_celsius(value)
                elif from_unit == "Celsius (°C)" and to_unit == "Kelvin (K)":
                    converted_value = self.celsius_to_kelvin(value)
                elif from_unit == "Kelvin (K)" and to_unit == "Celsius (°C)":
                    converted_value = self.kelvin_to_celsius(value)
                elif from_unit == "Fahrenheit (°F)" and to_unit == "Kelvin (K)":
                    converted_value = self.fahrenheit_to_kelvin(value)
                elif from_unit == "Kelvin (K)" and to_unit == "Fahrenheit (°F)":
                    converted_value = self.kelvin_to_fahrenheit(value)
                elif from_unit == "Celsius (°C)" and to_unit == "Réaumur (°Ré)":
                    converted_value = self.celsius_to_reaumur(value)
                elif from_unit == "Réaumur (°Ré)" and to_unit == "Celsius (°C)":
                    converted_value = self.reaumur_to_celsius(value)
                elif from_unit == "Fahrenheit (°F)" and to_unit == "Réaumur (°Ré)":
                    converted_value = self.fahrenheit_to_reaumur(value)
                elif from_unit == "Réaumur (°Ré)" and to_unit == "Fahrenheit (°F)":
                    converted_value = self.reaumur_to_fahrenheit(value)
                elif from_unit == "Celsius (°C)" and to_unit == "Delisle (°De)":
                    converted_value = self.celsius_to_delisle(value)
                elif from_unit == "Delisle (°De)" and to_unit == "Celsius (°C)":
                    converted_value = self.delisle_to_celsius(value)
                elif from_unit == "Fahrenheit (°F)" and to_unit == "Delisle (°De)":
                    converted_value = self.fahrenheit_to_delisle(value)
                elif from_unit == "Delisle (°De)" and to_unit == "Fahrenheit (°F)":
                    converted_value = self.delisle_to_fahrenheit(value)
                elif from_unit == "Celsius (°C)" and to_unit == "Newton (°N)":
                    converted_value = self.celsius_to_newton(value)
                elif from_unit == "Newton (°N)" and to_unit == "Celsius (°C)":
                    converted_value = self.newton_to_celsius(value)
                elif from_unit == "Fahrenheit (°F)" and to_unit == "Newton (°N)":
                    converted_value = self.fahrenheit_to_newton(value)
                elif from_unit == "Newton (°N)" and to_unit == "Fahrenheit (°F)":
                    converted_value = self.newton_to_fahrenheit(value)
                elif from_unit == "Celsius (°C)" and to_unit == "Rømer (°Rø)":
                    converted_value = self.celsius_to_romer(value)
                elif from_unit == "Rømer (°Rø)" and to_unit == "Celsius (°C)":
                    converted_value = self.romer_to_celsius(value)
                elif from_unit == "Fahrenheit (°F)" and to_unit == "Rømer (°Rø)":
                    converted_value = self.fahrenheit_to_romer(value)
                elif from_unit == "Rømer (°Rø)" and to_unit == "Fahrenheit (°F)":
                    converted_value = self.romer_to_fahrenheit(value)
                else:
                    converted_value = value  # Same unit, no conversion
            else:
                # Get conversion factors for other categories
                from_factor = self.units[selected_category][from_unit]
                to_factor = self.units[selected_category][to_unit]

                # Convert the value
                converted_value = value * from_factor / to_factor

            self.output_entry.config(state="normal")
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, str(converted_value))
            self.output_entry.config(state="readonly")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def clear(self):
        self.input_entry.delete(0, tk.END)
        self.output_entry.config(state="normal")
        self.output_entry.delete(0, tk.END)
        self.output_entry.config(state="readonly")

    def copy_to_clipboard(self):
        try:
            pyperclip.copy(self.output_entry.get())
        except:
            messagebox.showerror("Copy Error", "Unable to copy to clipboard.")


# Create the main window
root = tk.Tk()
root.geometry("600x200")  # Set window size

# Create an instance of the UnitConverter class
converter = UnitConverter(root)

# Run the main event loop
root.mainloop()