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

from os import path

from PySide6 import QtCore
from PySide6.QtWidgets import QDialog

from ui_EulaDialog import Ui_EulaDialog


class EulaDialog(QDialog):
    def __init__(self):
        super(EulaDialog, self).__init__()

        # Get rid of What's this icon in title bar
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint)

        self.load_ui()

        with open(path.join(path.dirname(__file__), 'RAYN_Vision_System_Eula.txt'), 'rt', encoding='utf-8') as file:
            text = file.read()
            self.ui.eula_plain_text_edit.setPlainText(text)
            file.close()

        self.ui.done_button.clicked.connect(self.accept)

    def load_ui(self):
        self.ui = Ui_EulaDialog()
        self.ui.setupUi(self)
