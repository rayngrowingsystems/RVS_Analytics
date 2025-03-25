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
import os
import json

from PySide6.QtWidgets import QGridLayout, QCheckBox, QLabel, QComboBox, QFrame, QStyledItemDelegate, QSlider, QGroupBox, QVBoxLayout, QHBoxLayout, QSpinBox
from PySide6.QtCore import QTimer, QEvent
from PySide6 import QtCore
from PySide6.QtGui import QPalette, QFontMetrics, QStandardItem

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

class CheckableComboBox(QComboBox):

    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # Make the lineedit the same color as QPushButton
        palette = qApp.palette()
        palette.setBrush(QPalette.Base, palette.button())
        self.lineEdit().setPalette(palette)

        # Use custom delegate
        self.setItemDelegate(CheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)
        self.model().dataChanged.connect(self.signalChange)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):

        if object == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == QtCore.Qt.Checked:
                    item.setCheckState(QtCore.Qt.Unchecked)
                else:
                    item.setCheckState(QtCore.Qt.Checked)

                return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == QtCore.Qt.Checked:
                texts.append(self.model().item(i).text())
        text = ", ".join(texts)

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, QtCore.Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elidedText)

    def signalChange(self):
        self.currentIndexChanged.emit(0)

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == QtCore.Qt.Checked:
                res.append(self.model().item(i).data())
        return res
    
    def setCurrentData(self, data):
        for i in range(self.model().rowCount()):
            if self.model().item(i).data() in data:
                self.model().item(i).setCheckState(QtCore.Qt.Checked)
            else:
                self.model().item(i).setCheckState(QtCore.Qt.Unchecked)
        
        QTimer.singleShot(300, lambda:self.updateText())  # Delayed update to get size established
    
def expand_presets(preset_folder, preset_list):
    settings_list = []

    for file_name in preset_list:
        with open(os.path.join(preset_folder, file_name), 'r') as f:
            j = f.read()
            d = json.loads(j)

            if "settings" in d:
                for setting in d["settings"]:
                    settings_list.append(setting)
        
    return settings_list

# Create grid of ui elements defined in a config file
def get_ui_elements_from_config(options, settings, execute_on_change, dropdown_changed, slider_value_changed, wavelength_changed, script_for_dropdown_values, preset_folder):
    # Lists to hold various UI elements
    option_checkboxes = []
    option_sliders = []
    option_wavelengths = []
    option_dropdowns = []
    option_spinboxes = []

    # Store ranges for related sliders
    option_ranges = []

    # Lists to store wavelength settings
    wavelengths = []

    wavelength_value = {}

    default_values = {}  # Keep a list of default values for each element

    top_layout = QVBoxLayout()

    for section in options["sections"]:
        display_name = section["displayName"]
        name = section["name"]

        settings_list = []
        if "settings" in section:
            settings_list = section["settings"]
        
        preset_list = []
        if "presets" in section:
            preset_list = section["presets"]

        if len(preset_list) > 0:
            settings_list.extend(expand_presets(preset_folder, preset_list))

        section_groupbox = QGroupBox(display_name) 
        section_grid = QGridLayout()

        row = 0
        column = 0

        # Iterate over each option
        for option in settings_list:
            # Handle layout for new column
            if option["type"] == "newColumn":
                column += 1
                row = 0

            # Handle checkbox options
            if option["type"] == "checkBox":
                option_checkbox = QCheckBox(option["displayName"])
                option_checkbox.setObjectName(option["name"])
                if "chartOptionType" in option:
                    option_checkbox.setProperty("chartOptionType", option["chartOptionType"])
                else:
                    option_checkbox.setProperty("chartOptionType", "")
                if "hint" in option:
                    option_checkbox.setToolTip(option["hint"])
                section_grid.addWidget(option_checkbox, row, column)
                row += 1

                # Check if the option is already set
                if option["name"] in settings:
                    tprint("Found checkbox option:", option["name"], settings[option["name"]])
                    option_checkbox.setChecked(settings[option["name"]])
                else:
                    option_checkbox.setChecked(option["value"] == "true")

                default_values[option_checkbox] = (option["value"] == "true")

                option_checkboxes.append((option["name"], option_checkbox,))

                option_checkbox.toggled.connect(execute_on_change)

            # Handle slider options
            elif option["type"] == "slider":
                option_label = QLabel()
                if "hint" in option:
                    option_label.setToolTip(option["hint"])
                section_grid.addWidget(option_label, row, column)
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

                default_values[option_slider] = default_value

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
                section_grid.addWidget(option_slider, row, column)
                row += 1

                option_sliders.append((option["name"], option_slider, min, step_size,))

                option_slider.valueChanged.connect(execute_on_change)

            # Handle wavelength options
            elif option["type"] == "wavelength":
                option_label = QLabel()
                option_label.setText(option["displayName"])
                if "hint" in option:
                    option_label.setToolTip(option["hint"])
                section_grid.addWidget(option_label, row, column)
                row += 1

                option_wavelength = QComboBox()
                if "hint" in option:
                    option_wavelength.setToolTip(option["hint"])
                section_grid.addWidget(option_wavelength, row, column)
                row += 1

                option_wavelength.addItem("")  # Dummy item until properly populated

                name = option["name"]
                display_name = option["displayName"]

                option_wavelengths.append((name, option_wavelength,))

                if option["name"] in settings:
                    wavelength_value[name] = settings[name]
                else:
                    wavelength_value[name] = option["value"]

                default_values[option_wavelength] = option["value"]

                # Connect wavelength change to script execution
                option_wavelength.currentIndexChanged.connect(
                lambda a, name=name, option_wavelength=option_wavelength: wavelength_changed(name, option_wavelength))

                option_wavelength.currentIndexChanged.connect(execute_on_change)

            # Handle dropdown options
            elif option["type"] == "dropdown" or option["type"] == "dropdownMultiSelect":
                # Create a label for the dropdown option
                option_label = QLabel()
                option_label.setText(option["displayName"])
                if "hint" in option:
                    option_label.setToolTip(option["hint"])
                section_grid.addWidget(option_label, row, column)
                row += 1

                # Create a dropdown menu
                if option["type"] == "dropdown":
                    option_dropdown = QComboBox()
                else:
                    option_dropdown = CheckableComboBox()

                if "hint" in option:
                    option_dropdown.setToolTip(option["hint"])
                section_grid.addWidget(option_dropdown, row, column)
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

                    if option["type"] == "dropdownMultiSelect":
                        option_dropdown.setCurrentData(value)
                    else:
                        index = option_dropdown.findData(value)

                        if index != -1:
                            option_dropdown.setCurrentIndex(index)
                        else:
                            option_dropdown.currentIndexChanged.emit(0)
                else:
                    option_dropdown.currentIndexChanged.emit(0)

                if "value" in option:
                    default_values[option_dropdown] = option["value"]

                name = option["name"]
                display_name = option["displayName"]
                option_dropdowns.append((name, option_dropdown,))

                # Connect the signal of dropdown menu change to its handling function
                option_dropdown.currentIndexChanged.connect(
                    lambda a, name=name, option_dropdown=option_dropdown: dropdown_changed(name, option_dropdown, False))

                # Connect the signal of dropdown menu change to the main function for updating the mask script
                option_dropdown.currentIndexChanged.connect(execute_on_change)
            
            # Handle spinbox options
            elif option["type"] == "spinBox":
                option_label = QLabel()
                option_label.setText(option["displayName"])
                if "hint" in option:
                    option_label.setToolTip(option["hint"])

                start_value = 0
                option_spinbox = QSpinBox()

                min = int(option["minimum"])
                max = int(option["maximum"])

                default_value = 0  # TODO?

                # Check if the spinbox value is set
                if option["name"] in settings:
                    tprint("Found spinbox option:", option["name"], settings[option["name"]])
                    start_value = settings[option["name"]]  # Use last value
                elif "value" in option:
                    start_value = default_value  # Use default value

                default_values[option_spinbox] = default_value

                display_name = option["displayName"]
                name = option["name"]

                # Set spinbox properties
                option_spinbox.name = name
                option_spinbox.displayName = display_name
                option_spinbox.optionLabel = option_label
                option_spinbox.min = min
                option_spinbox.max = max
                option_spinbox.defaultValue = default_value
                option_spinbox.startValue = start_value

                option_spinbox.setRange(min, max)

                # TODO? Connect spinbox value change to script execution
                #option_spinbox.valueChanged.connect(lambda a, name=name, optionSpinBox=option_spinbox: spinbox_value_changed(name, optionSpinbox))
                #option_spinbox.valueChanged.emit(0)  # Force refresh of label
                option_spinbox.setValue(start_value)
                if "hint" in option:
                    option_spinbox.setToolTip(option["hint"])

                layout = QHBoxLayout()
                layout.addWidget(option_label)
                layout.addWidget(option_spinbox)
                layout.addStretch(1)
                
                section_grid.addLayout(layout, row, column)
                row += 1

                option_spinboxes.append((option["name"], option_spinbox,))

                option_spinbox.valueChanged.connect(execute_on_change)

            # Handle divider
            elif option["type"] == "divider":
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setStyleSheet('color: rgb(100,100,100)')
                section_grid.addWidget(line, row, column)
                row += 1

            # Adjust row and column for grid layout
            if row > 5:
                column += 1
                row = 0

        section_groupbox.setLayout(section_grid)
        top_layout.addWidget(section_groupbox)

    # section_grid.setRowStretch(section_grid.rowCount(), 1)

    return top_layout, option_checkboxes, option_sliders, option_wavelengths, wavelength_value, option_dropdowns, option_ranges, option_spinboxes, default_values

def set_ui_elements_default_values(values):
    for option, value in values.items():
        if isinstance(option, QSlider):
            option.setValue(value)
        elif isinstance(option, QCheckBox):
            option.setChecked(bool(value))
        elif isinstance(option, QComboBox):
            option.setCurrentIndex(int(value))

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

    for name, spinbox in dialog.option_spinboxes:
        settings[name] = spinbox.value()

    return settings

