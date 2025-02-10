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

from PySide6.QtWidgets import QDialog, QVBoxLayout
from PySide6 import QtCore
from PySide6.QtCore import QUrl, QDir
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage

import CameraApp_rc

from ui_HelpDialog import Ui_HelpDialog


class HelpDialog(QDialog):
    def __init__(self):
        super(HelpDialog, self).__init__()

        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint)  # Get rid of What's this icon in title bar

        self.load_ui()

        self.setModal(False)

        layout = QVBoxLayout(self.ui.help_widget)
        self.help_view = QWebEngineView()
        layout.addWidget(self.help_view)

        self.url = QUrl.fromLocalFile(path.join(path.dirname(__file__), 'Help', 'Default.htm'));
        self.help_view.load(self.url)

        self.ui.home_button.clicked.connect(self.home)
        self.ui.back_button.clicked.connect(self.backward)

        self.ui.done_button.clicked.connect(self.accept)

    def home(self):
        self.help_view.load(self.url)

    def backward(self):
        self.help_view.page().triggerAction(QWebEnginePage.Back)

    def load_ui(self):
        self.ui = Ui_HelpDialog()
        self.ui.setupUi(self)
