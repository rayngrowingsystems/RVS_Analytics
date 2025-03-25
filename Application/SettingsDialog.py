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

from PySide6.QtWidgets import QDialog

import CameraApp_rc

from ui_SettingsDialog import Ui_SettingsDialog

from Helper import tprint

class SettingsDialog(QDialog):
    def __init__(self, main_window):
        self.main_window = main_window

        super(SettingsDialog, self).__init__()
        self.load_ui()

        self.ui.done_button.clicked.connect(self.accept)
        self.ui.cancel_button.clicked.connect(self.reject)

        if self.main_window.experiment.theme == "auto":
            self.ui.theme_combo_box.setCurrentIndex(0)
        elif self.main_window.experiment.theme == "light":
            self.ui.theme_combo_box.setCurrentIndex(1)
        elif self.main_window.experiment.theme == "dark":
            self.ui.theme_combo_box.setCurrentIndex(2)
            
        self.ui.theme_combo_box.currentIndexChanged.connect(self.on_theme_changed)

        self.ui.ip_lineedit.setText(self.main_window.experiment.mqtt_broker)
        self.ui.port_lineedit.setText(self.main_window.experiment.mqtt_port)
        self.ui.username_lineedit.setText(self.main_window.experiment.mqtt_username)
        self.ui.password_lineedit.setText(self.main_window.experiment.mqtt_password)

    def load_ui(self):
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

    def on_theme_changed(self):
        if self.ui.theme_combo_box.currentIndex() == 0:
            self.main_window.experiment.theme = "auto"
        elif self.ui.theme_combo_box.currentIndex() == 1:
            self.main_window.experiment.theme = "light"
        elif self.ui.theme_combo_box.currentIndex() == 2:
            self.main_window.experiment.theme = "dark"
        
        self.main_window.set_theme(self.main_window.experiment.theme)

        self.main_window.update_experiment_file(False)
