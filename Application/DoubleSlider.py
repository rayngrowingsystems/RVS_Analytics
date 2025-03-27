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
from PySide6.QtWidgets import QSlider


# Special slider that can handle the necessary negative and decimal ranges
class DoubleSlider(QSlider):
    double_value_changed = QtCore.Signal(float)

    def __init__(self, decimals=3, parent=None):
        QSlider.__init__(self, QtCore.Qt.Horizontal, parent)

        self._multi = 10 ** decimals

        self.valueChanged.connect(self.emit_double_value_changed)

    def emit_double_value_changed(self):
        value = float(super(DoubleSlider, self).value()) / self._multi
        self.double_value_changed.emit(value)

    def setValue(self, value):  # Note: Qt override
        super(DoubleSlider, self).setValue(int(value * self._multi))

    def value(self):  # Note: Qt override
        return float(super(DoubleSlider, self).value()) / self._multi

    def setRange(self, min, max):  # Note: Qt override
        # super(DoubleSlider, self).setPageStep((max - min) * self._multi / 20)  # Use 5% steps
        super(DoubleSlider, self).setRange(min * self._multi, max * self._multi)

    def setMinimum(self, value):  # Note: Qt override
        super(DoubleSlider, self).setMinimum(value * self._multi)

    def setMaximum(self, value):  # Note: Qt override
        super(DoubleSlider, self).setMaximum(value * self._multi)

    def setSingleStep(self, value):  # Note: Qt override
        super(DoubleSlider, self).setSingleStep(value * self._multi)
        super(DoubleSlider, self).setPageStep(value * self._multi)

    def singleStep(self):  # Note: Qt override
        return float(super(DoubleSlider, self).singleStep()) / self._multi
