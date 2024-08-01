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

import os
from os import path

from PySide6.QtWidgets import QDialog
from PySide6 import QtCore

import CameraApp_rc

from ui_HelpDialog import Ui_HelpDialog


class HelpDialog(QDialog):
    def __init__(self):
        super(HelpDialog, self).__init__()

        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint)  # Get rid of What's this icon in title bar

        self.load_ui()

        self.ui.help_browser.setSearchPaths([ 'Help' ])
        self.ui.help_browser.setSource(os.path.join('.', 'Help', 'Help.htm'))

        self.ui.home_button.clicked.connect(self.ui.help_browser.home)
        self.ui.back_button.clicked.connect(self.ui.help_browser.backward)

        self.ui.done_button.clicked.connect(self.accept)

    def load_ui(self):
        self.ui = Ui_HelpDialog()
        self.ui.setupUi(self)
