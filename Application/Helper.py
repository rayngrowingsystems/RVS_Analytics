# Copyright 2024 ETC Inc d/b/a RAYN Growing Systems
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This Python file uses the following encoding: utf-8

from datetime import datetime

from PySide6.QtWidgets import QDialog, QGridLayout, QCheckBox, QLabel, QPushButton, QMessageBox, QComboBox, QFrame
from PySide6.QtCore import QTimer

from DoubleSlider import DoubleSlider

debug_file_name = None

def tprint(*args, **kwargs):
    timestamp = datetime.now().strftime("%Y-%d-%m %H:%M:%S")

    # print(timestamp + ":", *args, **kwargs)

    # Build string and add to log file
    s = timestamp + ": "
    for arg in args:
        s += str(arg) + " "
    for kwarg in kwargs.items():
        s += str(kwarg) + " "

    print(s)
    
    if debug_file_name:
        with open(debug_file_name, "a") as f:
           f.write(s + "\n")

def info_from_header_file(file_name):
    header_dict, wavelength_dict = _parse_envi(file_name)

    # tprint("Header wavelength info", header_dict, header_dict["wavelength"])

    date = ""
    time = ""
    camera = ""

    if "capturedate" in header_dict:
        date = header_dict["capturedate"]
    if "capturetime" in header_dict:
        time = header_dict["capturetime"]
    if "camera" in header_dict:
        camera = header_dict["camera"]

    if date == "" and time == "":
        now = datetime.now()

        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

    return date, time, camera, header_dict["wavelength"]

    # Old implementation - obsolete
    with open(file_name, 'r') as hdr:
        lines = hdr.readlines()

        date = ""
        time = ""
        camera = ""
        wavelengths = []

        for line in lines:
            if line.startswith('capture date = '):
                date = line.replace('capture date = ', '').replace('\n', '')
            elif line.startswith('capture time = '):
                time = line.replace('capture time = ', '').replace('\n', '')
            elif line.startswith('camera = '):
                camera = line.replace('camera = ', '').replace('\n', '')
            elif line.startswith('wavelength = '):
                wavelengths = line.replace('wavelength = ', '').replace('\n', '').replace('{', '').replace('}', '').replace(' ', '').split(",")

        return date, time, camera, wavelengths

# Copied from plantcv
def _parse_envi(headername):
    """Parse a header file and create dictionary of relevant metadata

    Keyword arguments:
    headername      = File path/name of a hyperspectral data file.

    Returns:
    header_dict     = Dictionary of hdr metadata
    wavelength_dict = Dictionary of wavelength metadata

    :param headername: str
    :return header_dict: dict
    :return wavelength_dict: dict

    """
    # Initialize dictionary
    header_dict = {}
    with open(headername, "r") as f:
        # Replace characters for easier parsing
        hdata = f.read()
        hdata = hdata.replace(",\n", ",")
        hdata = hdata.replace("\n,", ",")
        hdata = hdata.replace("{\n", "{")
        hdata = hdata.replace("\n}", "}")
        hdata = hdata.replace(" \n ", "")
        hdata = hdata.replace(" \n", "")
        hdata = hdata.replace(";", "")
    hdata = hdata.split("\n")

    # Loop through and create a dictionary from the header file
    # Try to reformat strings by replacing all " = " with '=' and " : "
    for string in hdata:
        # Remove white space for consistency across header file formats
        string = string.replace(' ', '')
        if '=' in string:
            header_data = string.split("=")
            header_data[0] = header_data[0].lower()
            header_dict.update({header_data[0].rstrip(): header_data[1].rstrip()})
        elif ':' in string:
            header_data = string.split(":")
            header_data[0] = header_data[0].lower()
            header_dict.update({header_data[0].rstrip(): header_data[1].rstrip()})

    # Reformat wavelengths
    header_dict["wavelength"] = header_dict["wavelength"].replace("{", "")
    header_dict["wavelength"] = header_dict["wavelength"].replace("}", "")
    header_dict["wavelength"] = header_dict["wavelength"].replace(" ", "")
    header_dict["wavelength"] = header_dict["wavelength"].split(",")

    # Create dictionary of wavelengths
    wavelength_dict = {}
    for j, wavelength in enumerate(header_dict["wavelength"]):
        wavelength_dict.update({float(wavelength): float(j)})

    # Replace datatype ID number with the numpy datatype
    # dtype_dict = {"1": np.uint8, "2": np.int16, "3": np.int32, "4": np.float32, "5": np.float64, "6": np.complex64,
    #               "9": np.complex128, "12": np.uint16, "13": np.uint32, "14": np.int64, "15": np.uint64}
    # header_dict["datatype"] = dtype_dict[header_dict["datatype"]]

    return header_dict, wavelength_dict

# Create grid of ui elements defined in a config file
def get_ui_elements_from_config(options, settings, execute_on_change, dropdown_changed, slider_value_changed, wavelength_changed, script_for_dropdown_values):
    # Lists to hold various UI elements
    option_checkboxes = []
    option_sliders = []
    option_wavelengths = []
    option_dropdowns = []

    # Store ranges for related sliders
    option_ranges = []

    # Lists to store wavelength settings
    wavelengths = []

    wavelength_value = {}

    # Create a grid layout to hold mask options
    grid = QGridLayout()

    row = 0
    column = 0

    # Iterate over each option
    for option in options:
        # Handle layout for new column
        if option["type"] == "newColumn":
            column += 1
            row = 0

        # Handle checkbox options
        if option["type"] == "checkBox":
            option_checkbox = QCheckBox(option["displayName"])
            if "hint" in option:
                option_checkbox.setToolTip(option["hint"])
            grid.addWidget(option_checkbox, row, column)
            row += 1

            # Check if the option is already set
            if option["name"] in settings:
                tprint("Found checkbox option:", option["name"], settings[option["name"]])
                option_checkbox.setChecked(settings[option["name"]])
            else:
                option_checkbox.setChecked(option["value"] == "true")

            option_checkboxes.append((option["name"], option_checkbox,))

            option_checkbox.toggled.connect(execute_on_change)

        # Handle slider options
        elif option["type"] == "slider":
            option_label = QLabel()
            if "hint" in option:
                option_label.setToolTip(option["hint"])
            grid.addWidget(option_label, row, column)
            row += 1

            start_value = 0
            option_slider = DoubleSlider()

            # Handle sliders dependent on dropdown values
            if "getRangesFor" in option:
                # Save optionSlider + related optionDropdown and update on currentIndexChange
                found = False
                for name, dropdown in option_dropdowns:  # Find referenced dropdown
                    if name == option["getRangesFor"]:
                        option_ranges.append((option_slider, dropdown, name,))

                        tprint("Force delayed refresh of related slider range", name)
                        # Force refresh of initial dropdown range. Needs a delay, otherwise, it won't activate the new range
                        QTimer.singleShot(200, lambda name=name, dropdown=dropdown: dropdown_changed(name, dropdown, True))
                        found = True
                        break

                if not found:
                    tprint("Slider is referring a non-existent dropdown", option["getRangesFor"])

                min = 0
                max = 1
                steps = 2
                step_size = 1
                default_value = 0
            else:
                # Set slider properties based on configuration
                min = int(option["minimum"])
                max = int(option["maximum"])
                if "steps" in option:
                    steps = int(option["steps"])
                else:
                    steps = max - min + 1
                step_size = (max - min) / (steps - 1)
                default_value = float(option["value"])

            # Check if the slider value is set
            if option["name"] in settings:
                tprint("Found slider option:", option["name"], settings[option["name"]])
                start_value = settings[option["name"]]  # Use last value
            elif "value" in option:
                start_value = default_value  # Use default value

            display_name = option["displayName"]
            name = option["name"]

            # Set slider properties
            option_slider.name = name
            option_slider.displayName = display_name
            option_slider.optionLabel = option_label
            option_slider.min = min
            option_slider.max = max
            option_slider.steps = steps
            option_slider.stepSize = step_size
            option_slider.defaultValue = default_value
            option_slider.startValue = start_value

            option_slider.setTracking(False)
            option_slider.setRange(min, max)
            option_slider.setSingleStep((max - min) / steps)

            # Connect slider value change to script execution
            option_slider.valueChanged.connect(lambda a, name=name, optionSlider=option_slider: slider_value_changed(name, optionSlider))
            option_slider.valueChanged.emit(0)  # Force refresh of label
            option_slider.setValue(start_value)
            if "hint" in option:
                option_slider.setToolTip(option["hint"])
            grid.addWidget(option_slider, row, column)
            row += 1

            option_sliders.append((option["name"], option_slider, min, step_size,))

            option_slider.valueChanged.connect(execute_on_change)

        # Handle wavelength options
        elif option["type"] == "wavelength":
            option_label = QLabel()
            option_label.setText(option["displayName"])
            if "hint" in option:
                option_label.setToolTip(option["hint"])
            grid.addWidget(option_label, row, column)
            row += 1

            option_wavelength = QComboBox()
            if "hint" in option:
                option_wavelength.setToolTip(option["hint"])
            grid.addWidget(option_wavelength, row, column)
            row += 1

            option_wavelength.addItem("")  # Dummy item until properly populated

            name = option["name"]
            display_name = option["displayName"]

            option_wavelengths.append((name, option_wavelength,))

            if option["name"] in settings:
                wavelength_value[name] = settings[name]
            else:
                wavelength_value[name] = option["value"]

            # Connect wavelength change to script execution
            option_wavelength.currentIndexChanged.connect(
            lambda a, name=name, option_wavelength=option_wavelength: wavelength_changed(name, option_wavelength))

            option_wavelength.currentIndexChanged.connect(execute_on_change)

        # Handle dropdown options
        elif option["type"] == "dropdown":
            # Create a label for the dropdown option
            option_label = QLabel()
            option_label.setText(option["displayName"])
            if "hint" in option:
                 option_label.setToolTip(option["hint"])
            grid.addWidget(option_label, row, column)
            row += 1

            # Create a dropdown menu
            option_dropdown = QComboBox()
            if "hint" in option:
                 option_dropdown.setToolTip(option["hint"])
            grid.addWidget(option_dropdown, row, column)
            row += 1

            # If the dropdown menu needs to be populated dynamically based on a script function
            if "getValuesFor" in option:
                # Get the values for the dropdown from the script function
                display_names, names = script_for_dropdown_values.dropdown_values(option["getValuesFor"], [])

                # Add the items to the dropdown menu
                for index, display_name in enumerate(display_names):
                    option_dropdown.addItem(display_name, names[index])
            # If the dropdown menu has predefined values in the configuration file
            else:
                # Add the predefined items to the dropdown menu
                for index, display_name in enumerate(option["displayNames"]):
                    option_dropdown.addItem(display_name, option["names"][index])

            # Restore the last used index for the dropdown menu
            if option["name"] in settings:
                value = settings[option["name"]]
                index = option_dropdown.findData(value)

                if index != -1:
                    option_dropdown.setCurrentIndex(index)
                else:
                    option_dropdown.currentIndexChanged.emit(0)
            else:
                option_dropdown.currentIndexChanged.emit(0)

            name = option["name"]
            display_name = option["displayName"]
            option_dropdowns.append((name, option_dropdown,))

            # Connect the signal of dropdown menu change to its handling function
            option_dropdown.currentIndexChanged.connect(
                lambda a, name=name, option_dropdown=option_dropdown: dropdown_changed(name, option_dropdown, False))

            # Connect the signal of dropdown menu change to the main function for updating the mask script
            option_dropdown.currentIndexChanged.connect(execute_on_change)
        
        # Handle divider
        elif option["type"] == "divider":
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setStyleSheet('color: rgb(100,100,100)')
            grid.addWidget(line, row, column)
            row += 1

        # Adjust row and column for grid layout
        if row > 5:
            column += 1
            row = 0

    grid.setRowStretch(grid.rowCount(), 1)

    return grid, option_checkboxes, option_sliders, option_wavelengths, wavelength_value, option_dropdowns, option_ranges

# Get a settings dict for the UI elements of the dialog
def get_settings_for_ui_elements(dialog):
    settings = {}

    for name, checkbox in dialog.option_checkboxes:
        settings[name] = checkbox.isChecked()

    for name, slider, min, step_size in dialog.option_sliders:
        if step_size == 1.0:
            settings[name] = int(slider.value())
        else:
            settings[name] = slider.value()

    for name, wavelength in dialog.option_wavelengths:
        settings[name] = wavelength.currentText()

    for name, dropdown in dialog.option_dropdowns:
        settings[name] = dropdown.currentData()

    return settings

