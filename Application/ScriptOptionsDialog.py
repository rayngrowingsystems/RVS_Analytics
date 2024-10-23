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

import sys
import os
import json
import tempfile
import importlib

from multiprocessing import Queue

from PySide6.QtWidgets import QDialog, QCheckBox, QSlider, QLabel, QVBoxLayout, QComboBox, QFrame, QPushButton, QMessageBox
from PySide6.QtGui import QPixmap, QGuiApplication, QCursor
from PySide6.QtCore import QTimer, QCoreApplication
from PySide6 import QtCore

import Helper
from Helper import tprint

import CameraApp_rc

from SelectImageDialog import SelectImageDialog

from ui_ScriptOptionsDialog import Ui_ScriptOptionsDialog

class ScriptOptionsDialog(QDialog):
    def __init__(self, main_window):
        self.main_window = main_window

        self.option_checkboxes = []
        self.option_sliders = []
        self.option_dropdowns = []

        super(ScriptOptionsDialog, self).__init__()
        self.load_ui()

        # Connect signals of reference images to the slot for running preview script
        self.ui.reference_image1.image_file_name_changed.connect(self.run_preview_script)
        self.ui.reference_image2.image_file_name_changed.connect(self.run_preview_script)

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

        self.ui.preview_button.clicked.connect(self.run_preview_script)
        
        self.script_description = ''

        if self.main_window.experiment.selected_script != "":
            # configFileName = path.join(self.mainWindow.scriptFolder, self.mainWindow.experiment.selectedScript.replace(".py", ".config"))
            config_file_name = self.main_window.script_paths[self.main_window.experiment.selected_script].replace(".py", ".config")

            tprint("Script options config:", config_file_name)

            with open(config_file_name) as config_file:
                data = json.load(config_file)
                tprint(data)

                self.script_description = data['script']['info']['description']

                grid, self.option_checkboxes, self.option_sliders, self.option_wavelengths, self.wavelength_value, self.option_dropdowns, self.option_ranges = \
                    Helper.get_ui_elements_from_config(options=data['script']['options'], settings=self.main_window.experiment.script_options, \
                                                    execute_on_change=self.refresh_values, dropdown_changed=self.dropdown_changed, \
                                                    slider_value_changed=self.slider_value_changed, wavelength_changed=self.wavelength_changed, \
                                                    script_for_dropdown_values=self.main_window.current_analysis_script())

                '''for option in data['script']['options']:
                    if option["type"] == "checkBox":
                        option_checkbox = QCheckBox(option["displayName"])
                        option_checkbox.toggled.connect(self.refresh_values)
                        if option["name"] in self.main_window.experiment.script_options:
                            option_checkbox.setChecked(self.main_window.experiment.script_options[option["name"]])
                        else:
                            option_checkbox.setChecked(option["value"] == "true")
                        option_checkbox.setToolTip(option["hint"])
                        vbox.addWidget(option_checkbox)

                        self.option_checkboxes.append((option["name"], option_checkbox,))
                    elif option["type"] == "slider":
                        option_label = QLabel()
                        option_label.setToolTip(option["hint"])
                        vbox.addWidget(option_label)

                        display_name = option["displayName"]

                        option_slider = QSlider(QtCore.Qt.Orientation.Horizontal)
                        option_slider.setRange(int(option["minimum"]), int(option["maximum"]))
                        option_slider.valueChanged.connect(lambda a, displayName=display_name, optionLabel=option_label, optionSlider=option_slider: optionLabel.setText(displayName + ": " + str(optionSlider.value())))
                        option_slider.valueChanged.connect(self.refresh_values)
                        option_slider.valueChanged.emit(0) # Force refresh of label
                        if option["name"] in self.main_window.experiment.script_options:
                            option_slider.setValue(self.main_window.experiment.script_options[option["name"]])
                        else:
                            option_slider.setValue(int(option["value"]))
                        option_slider.setToolTip(option["hint"])
                        vbox.addWidget(option_slider)

                        self.option_sliders.append((option["name"], option_slider,))
                    elif option["type"] == "dropdown":
                        option_label = QLabel()
                        option_label.setText(option["displayName"])
                        option_label.setToolTip(option["hint"])
                        vbox.addWidget(option_label)

                        option_dropdown = QComboBox()
                        # optionDropdown.setFixedWidth(150)
                        option_dropdown.setToolTip(option["hint"])
                        vbox.addWidget(option_dropdown)

                        if "getValuesFor" in option:
                            analytics_script_name = self.main_window.experiment.selected_script
                            sys.path.append(os.path.dirname(self.main_window.script_paths[analytics_script_name]))
                            analytics_script = importlib.import_module(analytics_script_name.replace(".py", ""))

                            display_names, names = analytics_script.dropdown_values(option["getValuesFor"], [])

                            for index, display_name in enumerate(display_names):
                                option_dropdown.addItem(display_name, names[index])
                        else:
                            for index, display_name in enumerate(option["displayNames"]):
                                option_dropdown.addItem(display_name, option["names"][index])

                        if option["name"] in self.main_window.experiment.script_options:
                            value = self.main_window.experiment.script_options[option["name"]]
                            index = option_dropdown.findData(value)

                            if index != -1:
                                option_dropdown.setCurrentIndex(index)
                            else:
                                option_dropdown.currentIndexChanged.emit(0)
                        else:
                            option_dropdown.currentIndexChanged.emit(option["value"])

                        name = option["name"];
                        display_name = option["displayName"]

                        self.option_dropdowns.append((name, option_dropdown,))

                        option_dropdown.currentIndexChanged.connect(self.refresh_values)

                        # optionDropdown.currentIndexChanged.connect(
                        # lambda a, name=name, optionDropdown=optionDropdown : self.dropdownChanged(name, optionDropdown))
                    elif option["type"] == "divider":
                        line = QFrame()
                        line.setFrameShape(QFrame.HLine)
                        line.setStyleSheet('color: rgb(100,100,100)')
                        vbox.addWidget(line)'''

                self.ui.script_options_box.setLayout(grid)

        self.ui.script_label.setText("Script: " + self.main_window.ui.script_selection_combobox.currentText())
        self.ui.script_description.setText(self.script_description)

        # For some reason, geometry won't work unless we move the update outside the constructor
        QTimer.singleShot(300, lambda: self.load_reference_images())

    def load_ui(self):
        self.ui = Ui_ScriptOptionsDialog()
        self.ui.setupUi(self)

    def slider_value_changed(self, name, option_slider):
        tprint("Slider value changed", name, option_slider, option_slider.value(), option_slider.min, option_slider.max, option_slider.steps, option_slider.stepSize)
        if option_slider.stepSize == 1.0:
            option_slider.optionLabel.setText(str(option_slider.displayName + ": " + str(int(option_slider.value()))))
        else:
            option_slider.optionLabel.setText(str(option_slider.displayName + ": " + str(option_slider.value())))

    def wavelength_changed(self, name, option_wavelength):
        tprint("Wavelength changed", name, option_wavelength, option_wavelength.currentIndex())

    def dropdown_changed(self, name, option_dropdown, initial_update):
        tprint("Dropdown changed", name, option_dropdown, option_dropdown.currentIndex(), initial_update)

    def refresh_values(self):
        for name, checkbox in self.option_checkboxes:
            self.main_window.experiment.script_options[name] = checkbox.isChecked()

        for name, slider, min, step_size in self.option_sliders:
            self.main_window.experiment.script_options[name] = slider.value()

        for name, dropdown in self.option_dropdowns:
            self.main_window.experiment.script_options[name] = dropdown.currentData()

        tprint("Refresh", self.main_window.experiment.script_options)

        self.main_window.update_experiment_file(True)

        # self.run_preview_script()

    def refresh_preview_image1(self):
        if self.original_preview_image1 is not None:
            width = self.ui.preview_image1.width()
            height = self.ui.preview_image1.height()

            if self.original_preview_image1:
                # Scale pixmap to follow available space
                self.ui.preview_image1.setPixmap(self.original_preview_image1.scaled(width, height, QtCore.Qt.KeepAspectRatio))
            
    def refresh_preview_image2(self):
        if self.original_preview_image2 is not None:
            width = self.ui.preview_image2.width()
            height = self.ui.preview_image2.height()

            if self.original_preview_image2:
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

    def select_reference_image1(self):
        select_image_dialog = SelectImageDialog(self, self.ui.reference_image1)

        select_image_dialog.exec()

        # self.populate_wavelengths()

    def select_reference_image2(self):
        if self.ui.reference_image1.image_file_name != "":
            select_image_dialog = SelectImageDialog(self, self.ui.reference_image2)

            select_image_dialog.exec()
        else:
            QMessageBox.warning(self, "Image selection", "You must select the left image first")

    def load_reference_images(self):
        if self.main_window.experiment.script_reference_image1 is not None:
            self.ui.reference_image1.set_image_file_name(self.main_window.experiment.script_reference_image1, self.main_window.experiment.image_options_to_dict())
            tprint("Script: Load left preview image:", self.main_window.experiment.script_reference_image1)

        if self.main_window.experiment.script_reference_image2 is not None:
            self.ui.reference_image2.set_image_file_name(self.main_window.experiment.script_reference_image2, self.main_window.experiment.image_options_to_dict())
            tprint("Script: Load right preview image:", self.main_window.experiment.script_reference_image2)

        self.run_preview_script()

        self.refresh_image_sizes()

    def run_preview_script(self):
        if self.ui.reference_image1.image_file_name != "":
            # Set the cursor to a wait cursor during script execution
            QGuiApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))

            if self.ui.reference_image1.image_file_name != "":
                self.ui.preview_image1.setText("Processing preview...")
            if self.ui.reference_image2.image_file_name != "":
                self.ui.preview_image2.setText("Processing preview...")

            QCoreApplication.processEvents()  # Make sure GUI is updated before executing the preview script

            # Set up temporary file for preview
            with tempfile.TemporaryDirectory() as temp_path:
                # temp_file_name = os.path.join(temp_path, "ProcessedImages", 'scriptPreview.png')

                # Initialize settings dictionary for the script
                settings = {}
                settings["experimentSettings"] = self.main_window.experiment.to_dict()

                settings["scriptName"] = self.main_window.experiment.selected_script
                settings["outputFolder"] = temp_path
                # settings["outputImage"] = temp_file_name
                # TODO Why can't we use the outputImage in this case? Seems like it is hardcoded in the script to ProcessedImages and the input file name

                # Populate script options from UI elements
                # Note: If you change ui elements here, you are likely to have to update openImageMaskDialog when dialog is closed
                for name, checkbox in self.option_checkboxes:
                    settings['experimentSettings']['analysis']['scriptOptions']['general'][name] = checkbox.isChecked()

                for name, slider, min, step_size in self.option_sliders:
                    settings['experimentSettings']['analysis']['scriptOptions']['general'][name] = int(slider.value())

                for name, wavelength in self.option_wavelengths:
                    settings['experimentSettings']['analysis']['scriptOptions']['general'][name] = wavelength.currentText()

                for name, dropdown in self.option_dropdowns:
                    settings['experimentSettings']['analysis']['scriptOptions']['general'][name] = dropdown.currentData()

                analytics_script_name = self.main_window.experiment.selected_script
                sys.path.append(os.path.dirname(self.main_window.script_paths[analytics_script_name]))
                analytics_script = importlib.import_module(analytics_script_name.replace(".py", ""))

                # Find selected mask
                mask_path, mask_file = self.main_window.mask_info()

                if mask_file != self.main_window.experiment.selected_script:
                    mask_file_name = os.path.join(mask_path, mask_file)
                else:
                    mask_file_name = ''

                analysis_script_queue = Queue()

                # Process preview image 1 if available
                if self.ui.reference_image1.image_file_name != "":
                    settings["inputImage"] = self.ui.reference_image1.image_file_name

                    tprint("Script preview", settings)

                    analytics_script.execute(analysis_script_queue, analytics_script_name, settings, mask_file_name)
                    # TODO: We should clean this up and be able to specify an output file, like we can when processing the mask
                    temp_file_name = os.path.join(temp_path, "ProcessedImages", os.path.splitext(os.path.basename(self.ui.reference_image1.image_file_name))[0]) + ".png"
                    self.original_preview_image1 = QPixmap(temp_file_name)
                    self.refresh_preview_image1()

                    tprint("Reading preview from", temp_file_name)

                # Process preview image 2 if available
                if self.ui.reference_image2.image_file_name != "":
                    settings["inputImage"] = self.ui.reference_image2.image_file_name

                    analytics_script.execute(analysis_script_queue, analytics_script_name, settings, mask_file_name)
                    # TODO: We should clean this up and be able to specify an output file, like we can when processing the mask
                    temp_file_name = os.path.join(temp_path, "ProcessedImages", os.path.splitext(os.path.basename(self.ui.reference_image2.image_file_name))[0]) + ".png"
                    self.original_preview_image2 = QPixmap(temp_file_name)
                    self.refresh_preview_image2()

            # Restore the cursor to its original state
            QGuiApplication.restoreOverrideCursor()

