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

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QSize, QPoint, QRect
from PySide6.QtGui import QPainter, QPixmap

from PySide6 import QtCore

class Label(QLabel):

    def __init__(self, parent):
        QLabel.__init__(self, parent)

        self.magnifier_mode = False
        self.magnifier_size = 100
        self.magnifier_pos = QPoint()
        self.magnifier_zoom_factor = 1.0

    def set_magnifier_mode(self, mode, pos, zoom_factor):
        self.magnifier_mode = mode
        self.magnifier_pos = pos
        self.magnifier_zoom_factor = zoom_factor
        self.update()

    def minimumSizeHint(self):  # Qt override, keep casing
        return QSize(400, 300)

    def paintEvent(self, e):  # Qt override, keep casing
        super().paintEvent(e)

        painter = QPainter(self)

        if self.magnifier_mode and not self.pixmap().isNull():
            
            # Scale the pixmap to the same size as the original image. scale_factor is delivered through the magnifier_zoom_factor
            full_original_size = QSize(self.pixmap().width() / self.magnifier_zoom_factor, self.pixmap().height() / self.magnifier_zoom_factor)
            magnified_full_pixmap = self.pixmap().scaled(full_original_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            
            # Set up and copy the zoomed area from the full image
            scaled_center_point = self.magnifier_pos / self.magnifier_zoom_factor

            magnifier_size = QSize(self.magnifier_size, self.magnifier_size)

            source_rect = QRect(scaled_center_point.x() - self.magnifier_size / 2, scaled_center_point.y() - self.magnifier_size / 2, self.magnifier_size, self.magnifier_size) # QRect(top_left_point, magnifier_size)

            magnified_zoom_pixmap = magnified_full_pixmap.copy(source_rect)
 
            # Paint it
            painter_half_magnifier_size = self.magnifier_size / 2
            painter_top_left_point = self.magnifier_pos - QPoint(painter_half_magnifier_size, painter_half_magnifier_size)

            painter.drawPixmap(QRect(painter_top_left_point, magnifier_size), magnified_zoom_pixmap)
            painter.drawRect(QRect(painter_top_left_point, magnifier_size))

