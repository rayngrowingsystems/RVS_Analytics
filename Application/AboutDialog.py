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
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QDialog

from ui_AboutDialog import Ui_AboutDialog


class AboutDialog(QDialog):
    def __init__(self):
        super(AboutDialog, self).__init__()

        # Get rid of What's this icon in title bar
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint)

        self.load_ui()

        with open(path.join(path.dirname(__file__), 'RAYN_Vision_System_Eula.txt'), 'rt', encoding='utf-8') as file:
            text = file.read()
            self.ui.eula_plain_text_edit.setPlainText(text)
            file.close()

        self.ui.license_link.setText('<a href="http://etcconnect.com/Licenses">etcconnect.com/Licenses</a>')
        self.ui.privacy_link.setText('<a href="http://etcconnect.com/Privacy-Policy-Terms-of-Use-and-Acceptable-Use.aspx">etcconnect.com/Privacy-Policy-Terms-of-Use-and-Acceptable-Use</a>')

        self.ui.license_link.linkActivated.connect(self.license)
        self.ui.privacy_link.linkActivated.connect(self.privacy)

        self.ui.version_label.setText("Version: " + AboutDialog.version_number())

        self.ui.done_button.clicked.connect(self.accept)

    def load_ui(self):
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)

    def license(self, str):
        QDesktopServices.openUrl(QUrl(str))

    def privacy(self, str):
        QDesktopServices.openUrl(QUrl(str))

    def version_number():
        file = open(path.join(path.dirname(__file__), 'VersionNumber.txt'), 'r')
        version_number = file.readline()
        file.close()

        return version_number
