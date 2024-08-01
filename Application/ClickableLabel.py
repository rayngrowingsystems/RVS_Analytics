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

import tempfile
import os

from plantcv import plantcv as pcv

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QRect, QPoint, QSize
from PySide6.QtGui import QPixmap

from PySide6 import QtCore

import rayn_utils


class ClickableLabel(QLabel):
    pressed = QtCore.Signal(QPoint)
    clicked = QtCore.Signal(QPoint)
    right_clicked = QtCore.Signal(QPoint)
    moved = QtCore.Signal(QPoint)
    rubberband_changed = QtCore.Signal(QRect)
    image_file_name_changed = QtCore.Signal()

    def __init__(self, parent):
        QLabel.__init__(self, parent)

        self.mouse_pressed = False
        self.mouse_moved = False

        self.rubberband_origin = QPoint()
        self.rubberband_rect = QRect()

        self.image_file_name = ""

        self.original_image_size = QSize(0, 0)
        self.original_image = QPixmap()

        self.roi_grid = None

    def set_image_file_name(self, file_name, lens_angle, normalize, light_correction):
        # print("Set preview file:", fileName)

        if file_name != "" and file_name != ".":
            self.image_file_name = file_name

            # Convert to something visible
            with tempfile.TemporaryDirectory() as tmp:
                temp_file_name = os.path.join(tmp, 'imageCubeConversion.png')

                print("Preview: Read imagecube and convert to visible image:", file_name)
                # print("Convert to a visible file through tempfile:", tempFileName)

                # Create preview image
                image_cube = os.path.splitext(file_name)[0]
                spectral_array = pcv.readimage(filename=image_cube, mode='envi')
                spectral_array.array_data = spectral_array.array_data.astype("float32")
                spectral_array.pseudo_rgb = spectral_array.pseudo_rgb.astype("float32")

                # Apply light correction
                if light_correction:
                    correction_matrix = rayn_utils.get_correction_matrix_from_file("calibration_data/120_correction_matrix.npy")
                    spectral_array = rayn_utils.light_intensity_correction(spectral_array, correction_matrix)

                # Apply undistort
                if lens_angle != 0:  # if a lens angle is selected, undistortion is applied.
                    cam_calibration_file = f"calibration_data/{lens_angle}_calibration_data.yml"
                    mtx, dist = rayn_utils.load_coefficients(cam_calibration_file)
                    spectral_array.array_data = rayn_utils.undistort_data_cube(spectral_array.array_data, mtx, dist)
                    spectral_array.pseudo_rgb = rayn_utils.undistort_data_cube(spectral_array.pseudo_rgb, mtx, dist)

                # Normalize the image cube
                if normalize:
                    spectral_array.array_data = rayn_utils.dark_normalize_array_data(spectral_array)

                pcv.print_image(spectral_array.pseudo_rgb, temp_file_name)

                # print("Load resulting image to preview box")

                pixmap = QPixmap(temp_file_name)
                self.setPixmap(pixmap.scaledToWidth(self.width()))

                self.set_original_image_size(pixmap.size())
                self.original_image = pixmap

            self.image_file_name_changed.emit()

    def set_original_image_size(self, size):
        print("Preview image: setOriginalImageSize:", size)
        self.original_image_size = size

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

    def resizeEvent(self, event):  # Note: Qt override
        if not self.roi_grid is None:
            self.roi_grid.setGeometry(0, 0, event.size().width(), event.size().height())
        # self.setPixmap(self.originalImage.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio))
