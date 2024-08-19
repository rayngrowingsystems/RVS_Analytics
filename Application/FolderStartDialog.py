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

from PySide6.QtWidgets import QDialog

import CameraApp_rc

from ui_FolderStartDialog import Ui_FolderStartDialog


class FolderStartDialog(QDialog):
    def __init__(self, parent):
        self.main_window = parent

        super(FolderStartDialog, self).__init__()
        self.load_ui()

        self.ui.done_button.clicked.connect(self.accept)
        self.ui.cancel_button.clicked.connect(self.reject)

    def load_ui(self):
        self.ui = Ui_FolderStartDialog()
        self.ui.setupUi(self)
