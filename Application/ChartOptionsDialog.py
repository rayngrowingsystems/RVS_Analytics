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

from ui_ChartOptionsDialog import Ui_ChartOptionsDialog


class ChartOptionsDialog(QDialog):
    def __init__(self, main_window):
        self.main_window = main_window

        self.option_checkboxes = []
        self.option_sliders = []
        self.option_dropdowns = []

        super(ChartOptionsDialog, self).__init__()
        self.load_ui()

        if self.main_window.experiment.selected_script != "":
            config_file_name = self.main_window.script_paths[self.main_window.experiment.selected_script].replace(".py", ".config")

            print("Chart options config:", config_file_name)

            vbox = QVBoxLayout()
            with open(config_file_name) as config_file:
                data = json.load(config_file)
                print(data)

                # TODO Can we break this out and make a module that handle UI controls for all views?

                for option in data['chart']['options']:
                    if option["type"] == "checkBox":
                        option_checkbox = QCheckBox(option["displayName"])
                        option_checkbox.toggled.connect(self.refresh_values)
                        if option["name"] in self.main_window.experiment.chart_options:
                            option_checkbox.setChecked(self.main_window.experiment.chart_options[option["name"]])
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
                        if option["name"] in self.main_window.experiment.chart_options:
                            option_slider.setValue(self.main_window.experiment.chart_options[option["name"]])
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

                        if option["name"] in self.main_window.experiment.chart_options:
                            value = self.main_window.experiment.chart_options[option["name"]]
                            index = option_dropdown.findData(value)

                            if index != -1:
                                option_dropdown.setCurrentIndex(index)
                            else:
                                option_dropdown.currentIndexChanged.emit(0)
                        else:
                            option_dropdown.currentIndexChanged.emit(option["value"])

                        name = option["name"]
                        display_name = option["displayName"]

                        self.option_dropdowns.append((name, option_dropdown,))

                        option_dropdown.currentIndexChanged.connect(self.refresh_values)

                        # optionDropdown.currentIndexChanged.connect(
                        # lambda a, name=name, optionDropdown=optionDropdown : self.dropdownChanged(name, optionDropdown))

            vbox.addStretch(1)
            self.ui.chart_options_box.setLayout(vbox)

    def load_ui(self):
        self.ui = Ui_ChartOptionsDialog()
        self.ui.setupUi(self)

    def dropdown_changed(self, name, option_dropdown):
        print("Dropdown changed", name, option_dropdown, option_dropdown.currentIndex())

    def refresh_values(self):
        for name, check_box in self.option_checkboxes:
            self.main_window.experiment.chart_options[name] = check_box.isChecked()

        for name, slider in self.option_sliders:
            self.main_window.experiment.chart_options[name] = slider.value()

        for name, dropdown in self.option_dropdowns:
            self.main_window.experiment.chart_options[name] = dropdown.currentData()

        print("Refresh", self.main_window.experiment.chart_options)

        self.main_window.experiment.to_json()
