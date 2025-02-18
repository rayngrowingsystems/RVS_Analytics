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
import importlib

from PySide6.QtWidgets import QDialog, QCheckBox, QSlider, QLabel, QVBoxLayout, QComboBox, QFrame
from PySide6 import QtCore
from PySide6.QtCore import QTimer

import Helper
from Helper import tprint

import CameraApp_rc

from ui_AnalysisOptionsDialog import Ui_AnalysisOptionsDialog

class AnalysisOptionsDialog(QDialog):
    def __init__(self, main_window):
        self.main_window = main_window

        self.option_checkboxes = []
        self.option_sliders = []
        self.option_dropdowns = []

        self.default_values = {}

        super(AnalysisOptionsDialog, self).__init__()
        self.load_ui()

        if self.main_window.experiment.selected_script != "":
            config_file_name = self.main_window.script_paths[self.main_window.experiment.selected_script].replace(".py", ".config")

            tprint("Analysis options config:", config_file_name)

            with open(config_file_name) as config_file:
                data = json.load(config_file)
                tprint(data)

                # Script options
                grid, self.option_checkboxes, self.option_sliders, self.option_wavelengths, self.wavelength_value, self.option_dropdowns, self.option_ranges, self.default_values = \
                    Helper.get_ui_elements_from_config(options=data['script']['options'], settings=self.main_window.experiment.script_options, \
                                                    execute_on_change=self.refresh_values, dropdown_changed=self.dropdown_changed, \
                                                    slider_value_changed=self.slider_value_changed, wavelength_changed=self.wavelength_changed, \
                                                    script_for_dropdown_values=self.main_window.current_analysis_script(), preset_folder=self.main_window.preset_folder)
                
            self.ui.main_groupbox.setLayout(grid)   
            
            # Set active checkboxes
            chart_checkboxes = self.ui.main_groupbox.findChildren(QCheckBox)
            for child_checkbox in chart_checkboxes:
                if child_checkbox.objectName() in self.main_window.experiment.script_options:
                    child_checkbox.setChecked(self.main_window.experiment.script_options[child_checkbox.objectName()])

        self.ui.default_button.clicked.connect(self.set_default_values)

        # Connect cancel button to close the dialog
        self.ui.cancel_button.clicked.connect(self.reject)

        if self.main_window.test_mode:
            QTimer.singleShot(self.main_window.test_dialog_timeout, lambda:self.accept())

    def load_ui(self):
        self.ui = Ui_AnalysisOptionsDialog()
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
        pass

    def set_default_values(self):
        self.blockSignals(True)
        Helper.set_ui_elements_default_values(self.default_values)
        self.blockSignals(False)
 