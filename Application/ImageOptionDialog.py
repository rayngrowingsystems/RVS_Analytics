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

from PySide6 import QtCore
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QDialog

from ui_ImageOptionDialog import Ui_ImageOptionDialog


class ImageOptionDialog(QDialog):
    def __init__(self, main_window):
        self.main_window = main_window

        super(ImageOptionDialog, self).__init__()

        # Get rid of What's this icon in title bar
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint)

        self.load_ui()

        if self.main_window.experiment.lens_angle == 60:
            self.ui.lens_angle_combobox.setCurrentIndex(1)
        elif self.main_window.experiment.lens_angle == 120:
            self.ui.lens_angle_combobox.setCurrentIndex(2)
        else:
            self.ui.lens_angle_combobox.setCurrentIndex(0)
        self.ui.lens_angle_combobox.currentIndexChanged.connect(self.on_lens_angle)

        self.ui.normalize_checkbox.setChecked(self.main_window.experiment.normalize)
        self.ui.normalize_checkbox.toggled.connect(self.on_normalize)

        self.ui.rotation_spinbox.setValue(self.main_window.experiment.rotation)
        self.ui.rotation_spinbox.valueChanged.connect(self.on_rotation)

        self.ui.done_button.clicked.connect(self.accept)

        if self.main_window.test_mode:
            QTimer.singleShot(self.main_window.test_dialog_timeout, lambda:self.accept())

    def load_ui(self):
        self.ui = Ui_ImageOptionDialog()
        self.ui.setupUi(self)

    def on_lens_angle(self, index):
        if index == 0:
            self.main_window.experiment.lens_angle = 0
        elif index == 1:
            self.main_window.experiment.lens_angle = 60
        else:
            self.main_window.experiment.lens_angle = 120

        self.main_window.update_experiment_file(False)

    def on_normalize(self):
        self.main_window.experiment.normalize = self.ui.normalize_checkbox.isChecked()
        self.main_window.update_experiment_file(False)

    def on_rotation(self):
        self.main_window.experiment.rotation = self.ui.rotation_spinbox.value()
        self.main_window.update_experiment_file(False)
