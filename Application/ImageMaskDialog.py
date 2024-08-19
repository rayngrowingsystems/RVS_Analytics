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

import json
import tempfile
import os

from PySide6.QtWidgets import QDialog, QGridLayout, QCheckBox, QLabel, QPushButton, QMessageBox, QComboBox
from PySide6.QtGui import QPixmap, QGuiApplication, QCursor
from PySide6.QtCore import QTimer
from PySide6 import QtCore

import CameraApp_rc

from ui_ImageMaskDialog import Ui_ImageMaskDialog

from SelectImageDialog import SelectImageDialog

from DoubleSlider import DoubleSlider

import Config
import Helper

class ImageMaskDialog(QDialog):
    # MASK_FILE_PREFIX = "mask_"

    def __init__(self, main_window):
        # Initialize the dialog
        self.main_window = main_window

        # Lists to hold various UI elements
        self.option_checkboxes = []
        self.option_sliders = []
        self.option_wavelengths = []
        self.option_dropdowns = []

        # Store ranges for related sliders
        self.option_ranges = []

        # Lists to store wavelength settings
        self.wavelengths = []

        self.wavelength_value = {}

        # Flag to track setup completion
        self.setup_completed = False

        # Call parent class's constructor
        super(ImageMaskDialog, self).__init__()

        # Set window flags to customize window behavior
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint)  # Get rid of What's this icon in title bar

        # Load the UI from the ui file
        self.load_ui()

        # Connect signals of reference images to the slot for running mask script
        self.ui.reference_image1.image_file_name_changed.connect(self.run_mask_script)
        self.ui.reference_image2.image_file_name_changed.connect(self.run_mask_script)

        # Initialize variables to hold original preview images
        self.original_preview_image1 = None
        self.original_preview_image2 = None

        # Connect image buttons to slot for selecting reference images
        image_button = QPushButton("Image...", self.ui.reference_image1)
        image_button.setMaximumWidth(55)
        image_button.setDefault(False)
        image_button.setAutoDefault(False)
        image_button.clicked.connect(self.select_reference_image1)

        image_button = QPushButton("Image...", self.ui.reference_image2)
        image_button.setMaximumWidth(55)
        image_button.setDefault(False)
        image_button.setAutoDefault(False)
        image_button.clicked.connect(self.select_reference_image2)

        # Connect cancel button to close the dialog
        self.ui.cancel_button.clicked.connect(self.reject)

        # Initialize script description
        self.script_description = ''

        # Determine the configuration file for the mask
        if self.main_window.experiment.selected_mask == "" or self.main_window.experiment.selected_mask == "Default":
            self.mask_script = self.main_window.experiment.selected_script
            config_file_name = self.main_window.script_paths[self.mask_script].replace(".py", ".config")
        else:
            self.mask_script = self.main_window.experiment.selected_mask
            config_file_name = self.main_window.mask_paths[self.mask_script].replace(".py", ".config")

        print("Mask/Config:", self.mask_script, config_file_name)

        # Create a grid layout to hold mask options
        grid = QGridLayout()
        with open(config_file_name) as config_file:
            data = json.load(config_file)
            if Config.verbose_mode:
                print("Read config file:", data)

            # Extract script and mask descriptions
            if "script" in data:
                self.script_description = data['script']['info']['description']

            if "mask" in data:
                self.mask_description = data['mask']['info']['description']

            row = 0
            column = 0

            # Iterate over each mask option
            for option in data['mask']['options']:
                # Handle layout for new column
                if option["type"] == "newColumn":
                    column += 1
                    row = 0

                # Handle checkbox options
                if option["type"] == "checkBox":
                    option_checkbox = QCheckBox(option["displayName"])
                    grid.addWidget(option_checkbox, row, column)
                    row += 1

                    # Check if the option is already set
                    if option["name"] in self.main_window.experiment.mask:
                        print("Mask: Found checkbox option:", option["name"], self.main_window.experiment.mask[option["name"]])
                        option_checkbox.setChecked(self.main_window.experiment.mask[option["name"]])
                    else:
                        option_checkbox.setChecked(option["value"] == "true")

                    # Connect checkbox toggling to mask script execution
                    self.option_checkboxes.append((option["name"], option_checkbox,))

                    option_checkbox.toggled.connect(self.run_mask_script)

                # Handle slider options
                elif option["type"] == "slider":
                    option_label = QLabel()
                    grid.addWidget(option_label, row, column)
                    row += 1

                    start_value = 0
                    option_slider = DoubleSlider()

                    # Handle sliders dependent on dropdown values
                    if "getRangesFor" in option:
                        # Save optionSlider + related optionDropdown and update on currentIndexChange
                        found = False
                        for name, dropdown in self.option_dropdowns:  # Find referenced dropdown
                            if name == option["getRangesFor"]:
                                self.option_ranges.append((option_slider, dropdown, name,))

                                print("Force delayed refresh of related slider range", name)
                                # Force refresh of initial dropdown range. Needs a delay, otherwise, it won't activate the new range
                                QTimer.singleShot(200, lambda name=name, dropdown=dropdown: self.dropdown_changed(name, dropdown, True))
                                found = True
                                break

                        if not found:
                            print("Slider is referring a non-existent dropdown", option["getRangesFor"])

                        min = 0
                        max = 1
                        steps = 2
                        step_size = 1
                        default_value = 0
                    else:
                        # Set slider properties based on configuration
                        min = int(option["minimum"])
                        max = int(option["maximum"])
                        steps = int(option["steps"])
                        step_size = (max - min) / steps
                        default_value = float(option["value"])

                    # Check if the slider value is set
                    if option["name"] in self.main_window.experiment.mask:
                        print("Mask: Found slider option:", option["name"], self.main_window.experiment.mask[option["name"]])
                        start_value = self.main_window.experiment.mask[option["name"]]  # Use last value
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
                    option_slider.valueChanged.connect(lambda a, name=name, optionSlider=option_slider: self.slider_value_changed(name, optionSlider))
                    option_slider.valueChanged.emit(0)  # Force refresh of label
                    option_slider.setValue(start_value)
                    grid.addWidget(option_slider, row, column)
                    row += 1

                    self.option_sliders.append((option["name"], option_slider, min, step_size,))

                    option_slider.valueChanged.connect(self.run_mask_script)

                # Handle wavelength options
                elif option["type"] == "wavelength":
                    option_label = QLabel()
                    option_label.setText(option["displayName"])
                    grid.addWidget(option_label, row, column)
                    row += 1

                    option_wavelength = QComboBox()
                    grid.addWidget(option_wavelength, row, column)
                    row += 1

                    option_wavelength.addItem("")  # Dummy item until properly populated

                    name = option["name"]
                    display_name = option["displayName"]

                    self.option_wavelengths.append((name, option_wavelength,))

                    if option["name"] in self.main_window.experiment.mask:
                        self.wavelength_value[name] = self.main_window.experiment.mask[name]
                    else:
                        self.wavelength_value[name] = option["value"]

                    # Connect wavelength change to script execution
                    option_wavelength.currentIndexChanged.connect(
                    lambda a, name=name, option_wavelength=option_wavelength: self.wavelength_changed(name, option_wavelength))

                    option_wavelength.currentIndexChanged.connect(self.run_mask_script)

                # Handle dropdown options
                elif option["type"] == "dropdown":
                    # Create a label for the dropdown option
                    option_label = QLabel()
                    option_label.setText(option["displayName"])
                    grid.addWidget(option_label, row, column)
                    row += 1

                    # Create a dropdown menu
                    option_dropdown = QComboBox()
                    grid.addWidget(option_dropdown, row, column)
                    row += 1

                    # If the dropdown menu needs to be populated dynamically based on a script function
                    if "getValuesFor" in option:
                        mask_script = self.main_window.current_mask_script()

                        # Get the values for the dropdown from the script function
                        display_names, names = mask_script.dropdown_values(option["getValuesFor"], [])

                        # Add the items to the dropdown menu
                        for index, display_name in enumerate(display_names):
                            option_dropdown.addItem(display_name, names[index])
                    # If the dropdown menu has predefined values in the configuration file
                    else:
                        # Add the predefined items to the dropdown menu
                        for index, display_name in enumerate(option["displayNames"]):
                            option_dropdown.addItem(display_name, option["names"][index])

                    # Restore the last used index for the dropdown menu
                    if option["name"] in self.main_window.experiment.mask:
                        value = self.main_window.experiment.mask[option["name"]]
                        index = option_dropdown.findData(value)

                        if index != -1:
                            option_dropdown.setCurrentIndex(index)
                        else:
                            option_dropdown.currentIndexChanged.emit(0)
                    else:
                        option_dropdown.currentIndexChanged.emit(0)

                    name = option["name"]
                    display_name = option["displayName"]
                    self.option_dropdowns.append((name, option_dropdown,))

                    # Connect the signal of dropdown menu change to its handling function
                    option_dropdown.currentIndexChanged.connect(
                        lambda a, name=name, option_dropdown=option_dropdown: self.dropdown_changed(name, option_dropdown, False))

                    # Connect the signal of dropdown menu change to the main function for updating the mask script
                    option_dropdown.currentIndexChanged.connect(self.run_mask_script)

                # Adjust row and column for grid layout
                if row > 5:
                    column += 1
                    row = 0

            # Set the layout for mask options
            self.ui.mask_options_box.setLayout(grid)

            print(self.option_wavelengths, self.option_dropdowns)

        # Set label and description based on selected mask or script
        if self.main_window.experiment.selected_mask == "" or self.main_window.experiment.selected_mask == "Default":
            self.ui.script_label.setText("Script: " + self.main_window.ui.script_selection_combobox.currentText())
            self.ui.script_description.setText(self.script_description)
        else:
            self.ui.script_label.setText("Mask: " + self.main_window.ui.mask_selection_combobox.currentText().replace(".py", ""))
            self.ui.script_description.setText(self.mask_description)

        # For some reason, geometry won't work unless we move the update outside the constructor
        QTimer.singleShot(300, lambda: self.load_reference_images())

    def load_ui(self):
        self.ui = Ui_ImageMaskDialog()
        self.ui.setupUi(self)

    def slider_value_changed(self, name, option_slider):
        print("Slider value changed", name, option_slider, option_slider.value(), option_slider.min, option_slider.max, option_slider.steps, option_slider.stepSize)
        option_slider.optionLabel.setText(str(option_slider.displayName + ": " + str(option_slider.value())))

    def wavelength_changed(self, name, option_wavelength):
        print("Wavelength changed", name, option_wavelength, option_wavelength.currentIndex())
        # No action needed, runMaskScript will pull the current values

    def populate_wavelengths(self):
        if self.ui.reference_image1.image_file_name != "":
            date, time, camera, image_wavelengths = Helper.info_from_header_file(self.ui.reference_image1.image_file_name)

            print("Wavelengths from image:", image_wavelengths)

            self.wavelengths = ['None']
            self.wavelengths.extend(image_wavelengths)

            # Add the wavelengths from the image to all wavelength dropdowns
            for name, option_wavelength in self.option_wavelengths:
                option_wavelength.clear()
                option_wavelength.addItems(self.wavelengths)

                if name in self.wavelength_value and self.wavelength_value[name] != "":
                    print("Restore wavelength", name, self.wavelength_value[name], self.wavelengths)
                    index = option_wavelength.findText(str(self.wavelength_value[name]))
                    option_wavelength.setCurrentIndex(index)

    def dropdown_changed(self, name, option_dropdown, initial_update):
        print("Dropdown changed", name, option_dropdown, option_dropdown.currentIndex(), initial_update)
        # runMaskScript will pull the current values

        # If dropdown is referenced by a slider, get related slider ranges from the mask script for the new index
        for slider, dropdown, name in self.option_ranges:
            if dropdown == option_dropdown:
                print("Update related slider range", name)

                mask_script = self.main_window.current_mask_script()

                slider.min, slider.max, slider.steps, slider.defaultValue = mask_script.range_values(name, dropdown.currentData(), dropdown.currentIndex())

                slider.stepSize = (slider.max - slider.min) / slider.steps

                slider.setRange(slider.min, slider.max)
                slider.setSingleStep(slider.stepSize)

                if initial_update:
                    start_value = slider.startValue
                else:
                    start_value = slider.defaultValue

                slider.setValue(start_value)

                slider.valueChanged.emit(slider.value())  # Force refresh of label

                print("New range:", slider.min, slider.max, slider.steps, slider.defaultValue, slider.stepSize)

                # Find corresponding optionSlider and update the min and stepsize in the tuplet
                for index, item in enumerate(self.option_sliders):
                    itemlist = list(item)  # tuplet is (name, slider, min, stepSize)
                    print(itemlist)
                    if itemlist[1] == slider:
                        itemlist[2] = slider.min
                        itemlist[3] = slider.stepSize
                        item = tuple(itemlist)

                        self.option_sliders[index] = item

    def select_reference_image1(self):
        select_image_dialog = SelectImageDialog(self, self.ui.reference_image1)

        select_image_dialog.exec()

        self.populate_wavelengths()

    def select_reference_image2(self):
        if self.ui.reference_image1.image_file_name != "":
            select_image_dialog = SelectImageDialog(self, self.ui.reference_image2)

            select_image_dialog.exec()
        else:
            QMessageBox.warning(self, "Image selection", "You must select the left image first")

    def load_reference_images(self):
        if self.main_window.experiment.mask_reference_image1 is not None:
            self.ui.reference_image1.set_image_file_name(self.main_window.experiment.mask_reference_image1, self.main_window.experiment.lens_angle, self.main_window.experiment.normalize, self.main_window.experiment.light_correction)
            print("Mask: Load left preview image:", self.main_window.experiment.mask_reference_image1)

        if self.main_window.experiment.mask_reference_image2 is not None:
            self.ui.reference_image2.set_image_file_name(self.main_window.experiment.mask_reference_image2, self.main_window.experiment.lens_angle, self.main_window.experiment.normalize, self.main_window.experiment.light_correction)
            print("Mask: Load right preview image:", self.main_window.experiment.mask_reference_image2)

        self.populate_wavelengths()

        self.setup_completed = True
        self.run_mask_script()

        self.refresh_image_sizes()

    def run_mask_script(self):
        # Ensure the function is only executed after the dialog is fully populated
        if self.setup_completed is False:
            return

        # Set the cursor to a wait cursor during script execution
        QGuiApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))

        # Set up temporary file for mask preview
        with tempfile.TemporaryDirectory() as tmp:
            temp_file_name = os.path.join(tmp, 'maskPreview.png')

            # Initialize settings dictionary for the script
            settings = {}

            settings["outputImage"] = temp_file_name

            settings['experimentSettings'] = {}
            settings['experimentSettings']['analysis'] = {}
            settings['experimentSettings']['analysis']['maskOptions'] = {}
            settings['experimentSettings']['imageOptions'] = {}

            # Populate mask options from UI elements
            # Note: If you change ui elements here, you are likely to have to update openImageMaskDialog when dialog is closed
            for name, checkbox in self.option_checkboxes:
                settings['experimentSettings']['analysis']['maskOptions'][name] = checkbox.isChecked()

            for name, slider, min, step_size in self.option_sliders:
                settings['experimentSettings']['analysis']['maskOptions'][name] = slider.value()

            for name, wavelength in self.option_wavelengths:
                settings['experimentSettings']['analysis']['maskOptions'][name] = wavelength.currentText()

            for name, dropdown in self.option_dropdowns:
                settings['experimentSettings']['analysis']['maskOptions'][name] = dropdown.currentData()

            # Populate image options
            settings["experimentSettings"]["imageOptions"]["lensAngle"] = self.main_window.experiment.lens_angle
            settings["experimentSettings"]["imageOptions"]["normalize"] = self.main_window.experiment.normalize
            settings["experimentSettings"]["imageOptions"]["lightCorrection"] = self.main_window.experiment.light_correction

            # Get the current mask script
            mask_script = self.main_window.current_mask_script()

            # Process preview image 1 if available
            if self.ui.reference_image1.image_file_name != "":
                settings["inputImage"] = self.ui.reference_image1.image_file_name

                print("Mask", settings)

                # Execute the mask script
                mask_script.create_mask(settings)

                # Load the generated mask preview image
                self.original_preview_image1 = QPixmap(temp_file_name)

                # Refresh the preview image on the UI
                self.refresh_preview_image1()

            # Process preview image 2 if available
            if self.ui.reference_image2.image_file_name != "":
                settings["inputImage"] = self.ui.reference_image2.image_file_name

                # Execute the mask script
                mask_script.create_mask(settings)

                # Load the generated mask preview image
                self.original_preview_image2 = QPixmap(temp_file_name)

                # Refresh the preview image on the UI
                self.refresh_preview_image2()

        # Set a flag to indicate that the mask has been defined
        self.main_window.experiment.mask_defined = True

        # Restore the cursor to its original state
        QGuiApplication.restoreOverrideCursor()

    def refresh_preview_image1(self):
        if self.original_preview_image1 is not None:
            width = self.ui.preview_image1.width()
            height = self.ui.preview_image1.height()

            # Scale pixmap to follow available space
            self.ui.preview_image1.setPixmap(self.original_preview_image1.scaled(width, height, QtCore.Qt.KeepAspectRatio))

    def refresh_preview_image2(self):
        if self.original_preview_image2 is not None:
            width = self.ui.preview_image2.width()
            height = self.ui.preview_image2.height()

            # Scale pixmap to follow available space
            self.ui.preview_image2.setPixmap(self.original_preview_image2.scaled(width, height, QtCore.Qt.KeepAspectRatio))

    def refresh_reference_image1(self):
        if self.ui.reference_image1 is not None:
            width = self.ui.reference_image1.width()
            height = self.ui.reference_image1.height()

            # Scale pixmap to follow available space
            self.ui.reference_image1.setPixmap(self.ui.reference_image1.original_image.scaled(width, height, QtCore.Qt.KeepAspectRatio))

    def refresh_reference_image2(self):
        if self.ui.reference_image2 is not None:
            width = self.ui.reference_image2.width()
            height = self.ui.reference_image2.height()

            # Scale pixmap to follow available space
            self.ui.reference_image2.setPixmap(self.ui.reference_image2.original_image.scaled(width, height, QtCore.Qt.KeepAspectRatio))

    def refresh_image_sizes(self):
        self.refresh_reference_image1()
        self.refresh_reference_image2()

        self.refresh_preview_image1()
        self.refresh_preview_image2()

    def resizeEvent(self, event):  # Qt override
        self.refresh_image_sizes()

