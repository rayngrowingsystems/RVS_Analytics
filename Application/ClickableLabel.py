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

import tempfile
import os

from plantcv import plantcv as pcv

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QRect, QPoint, QSize
from PySide6.QtGui import QPixmap, QTransform

from PySide6 import QtCore

import rayn_utils

from Helper import tprint

class ClickableLabel(QLabel):
    pressed = QtCore.Signal(QPoint)
    clicked = QtCore.Signal(QPoint)
    right_clicked = QtCore.Signal(QPoint)
    moved = QtCore.Signal(QPoint)
    double_clicked = QtCore.Signal(QPoint)
    rubberband_changed = QtCore.Signal(QRect)
    image_file_name_changed = QtCore.Signal()

    def __init__(self, parent):
        QLabel.__init__(self, parent)

        self.mouse_pressed = False
        self.mouse_moved = False

        self.rubberband_origin = QPoint()
        self.rubberband_rect = QRect()

        self.image_file_name = ""

        self.original_image = QPixmap()

        self.roi_grid = None

    def set_image_file_name(self, file_name, image_options):
        # tprint("Set preview file:", fileName)

        lens_angle = image_options["lensAngle"]
        normalize = image_options["normalize"]
        light_correction = image_options["lightCorrection"]
        rotation = image_options["rotation"]
        crop = image_options["crop"]

        if file_name != "" and file_name != ".":
            self.image_file_name = file_name

            # Convert to something visible
            with tempfile.TemporaryDirectory() as tmp:
                temp_file_name = os.path.join(tmp, 'imageCubeConversion.png')

                tprint("Preview: Read imagecube and convert to visible image:", file_name)
                # tprint("Convert to a visible file through tempfile:", tempFileName)

                # Create preview image
                spectral_array, rvs_metadata = rayn_utils.prepare_spectral_data(image_options, file_name, preview=True)
                pcv.print_image(spectral_array.pseudo_rgb, temp_file_name)

                # tprint("Load resulting image to preview box")

                pixmap = QPixmap(temp_file_name)

                self.setPixmap(pixmap.scaledToWidth(self.width()))                   

                self.original_image = pixmap

            self.image_file_name_changed.emit()

    def set_roi_grid(self, roi_grid):
        self.roi_grid = roi_grid

    def mousePressEvent(self, event):  # Note: Qt override
        if event.button() == QtCore.Qt.LeftButton:
            self.rubberband_origin = event.pos()

            self.rubberband_rect = QRect(self.rubberband_origin, QSize())

            self.rubberband_changed.emit(self.rubberband_rect)

            self.pressed.emit(event.pos())

            self.mouse_pressed = True

        self.mouse_moved = False

    def mouseMoveEvent(self, event):  # Note: Qt override
        if self.mouse_pressed:
            self.rubberband_rect = QRect(self.rubberband_origin, event.pos()).normalized()

            diff = event.pos() - self.rubberband_origin
            if diff.manhattanLength() > 3:
                self.rubberband_changed.emit(self.rubberband_rect)

                self.moved.emit(event.pos())

                self.mouse_moved = True

    def mouseReleaseEvent(self, event):  # Note: Qt override
        if not self.mouse_moved:
            if event.button() == QtCore.Qt.LeftButton:
                self.clicked.emit(event.pos())
            elif event.button() == QtCore.Qt.RightButton:
                self.right_clicked.emit(event.pos())

        self.mouse_pressed = False

    def mouseDoubleClickEvent(self, event):  # Note: Qt override
        self.double_clicked.emit(event.pos())

    def resizeEvent(self, event):  # Note: Qt override
        if not self.roi_grid is None:
            self.roi_grid.setGeometry(0, 0, event.size().width(), event.size().height())
        # self.setPixmap(self.originalImage.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio))
