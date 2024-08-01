# Copyright 2024 RAYN Growing Systems
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

from PySide6.QtWidgets import QDialog, QCheckBox, QSlider, QLabel, QVBoxLayout, QComboBox
from PySide6 import QtCore

import CameraApp_rc

from ui_ScriptOptionsDialog import Ui_ScriptOptionsDialog

class ScriptOptionsDialog(QDialog):
    def __init__(self, main_window):
        self.main_window = main_window

        self.option_checkboxes = []
        self.option_sliders = []
        self.option_dropdowns = []

        super(ScriptOptionsDialog, self).__init__()
        self.load_ui()

        self.script_description = ''

        if self.main_window.experiment.selected_script != "":
            # configFileName = path.join(self.mainWindow.scriptFolder, self.mainWindow.experiment.selectedScript.replace(".py", ".config"))
            config_file_name = self.main_window.script_paths[self.main_window.experiment.selected_script].replace(".py", ".config")

            print("Script options config:", config_file_name)

            vbox = QVBoxLayout()
            with open(config_file_name) as config_file:
                data = json.load(config_file)
                print(data)

                self.script_description = data['script']['info']['description']

                for option in data['script']['options']:
                    if option["type"] == "checkBox":
                        option_checkbox = QCheckBox(option["displayName"])
                        option_checkbox.toggled.connect(self.refresh_values)
                        if option["name"] in self.main_window.experiment.script_options:
                            option_checkbox.setChecked(self.main_window.experiment.script_options[option["name"]])
                        else:
                            option_checkbox.setChecked(option["value"] == "true")
                        vbox.addWidget(option_checkbox)

                        self.option_checkboxes.append((option["name"], option_checkbox,))
                    elif option["type"] == "slider":
                        option_label = QLabel()
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
                        vbox.addWidget(option_slider)

                        self.option_sliders.append((option["name"], option_slider,))
                    elif option["type"] == "dropdown":
                        option_label = QLabel()
                        option_label.setText(option["displayName"])
                        vbox.addWidget(option_label)

                        option_dropdown = QComboBox()
                        # optionDropdown.setFixedWidth(150)
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

            vbox.addStretch(1)
            self.ui.script_options_box.setLayout(vbox)

        self.ui.script_label.setText("Script: " + self.main_window.ui.script_selection_combobox.currentText())
        self.ui.script_description.setText(self.script_description)

    def load_ui(self):
        self.ui = Ui_ScriptOptionsDialog()
        self.ui.setupUi(self)

    def dropdown_changed(self, name, option_dropdown):
        print("Dropdown changed", name, option_dropdown, option_dropdown.currentIndex())

    def select_reference_image1(self):
        print("selectReferenceImage1")

    def select_reference_image2(self):
        print("selectReferenceImage2")

    def refresh_values(self):
        for name, checkbox in self.option_checkboxes:
            self.main_window.experiment.script_options[name] = checkbox.isChecked()

        for name, slider in self.option_sliders:
            self.main_window.experiment.script_options[name] = slider.value()

        for name, dropdown in self.option_dropdowns:
            self.main_window.experiment.script_options[name] = dropdown.currentData()

        print("Refresh", self.main_window.experiment.script_options)

        self.main_window.experiment.to_json()

