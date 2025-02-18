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

from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QHBoxLayout
from PySide6.QtCore import QRect, QPoint, QSize, QTimer
from PySide6.QtGui import QPixmap, QTransform, QPainter, QPen, QColor

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

        self.zoom_mode = False
        self.zoom_origin = QPoint()
        self.zoom_rect = QRect()

        self.select_image_button = QPushButton("Image...", self)
        self.select_image_button.setMaximumWidth(55)
        self.select_image_button.setDefault(False)
        self.select_image_button.setAutoDefault(False)

        self.zoom_button = QPushButton("Zoom", self)
        self.zoom_button.setFixedWidth(55)
        self.zoom_button.setDefault(False)
        self.zoom_button.setAutoDefault(False)
        self.zoom_button.clicked.connect(self.on_zoom)
     
        self.zoom_accept_button = QPushButton("Accept", self)
        self.zoom_accept_button.setFixedWidth(55)
        self.zoom_accept_button.setDefault(False)
        self.zoom_accept_button.setAutoDefault(False)
        self.zoom_accept_button.clicked.connect(self.on_zoom_accept)
        self.zoom_accept_button.hide()

        self.zoom_cancel_button = QPushButton("Cancel", self)
        self.zoom_cancel_button.setFixedWidth(55)
        self.zoom_cancel_button.setDefault(False)
        self.zoom_cancel_button.setAutoDefault(False)
        self.zoom_cancel_button.clicked.connect(self.on_zoom_cancel)
        self.zoom_cancel_button.hide()

        self.zoom_reset_button = QPushButton("Reset", self)
        self.zoom_reset_button.setFixedWidth(55)
        self.zoom_reset_button.setDefault(False)
        self.zoom_reset_button.setAutoDefault(False)
        self.zoom_reset_button.clicked.connect(self.on_zoom_reset)
        self.zoom_reset_button.hide()

        QTimer.singleShot(300, lambda: self.refresh())  # Delayed initial refresh to make sure sizes are established

    def paintEvent(self, e):  # Qt override, keep casing
        super().paintEvent(e)

        if not self.zoom_mode and self.zoom_rect.isEmpty():
            return
        
        painter = QPainter(self)
        pen = QPen()
        pen.setColor(QColor('#888'))
        pen.setWidth(3)
        painter.setPen(pen)

        if not self.zoom_rect.isEmpty():
             painter.drawRect(self.zoom_rect)

    def refresh(self):
        self.refresh_zoom_buttons(self.width())

    def on_zoom(self):
        self.zoom_mode = True
        self.zoom_rect = QRect()

        self.refresh_zoom_buttons(self.width())
    
    def on_zoom_accept(self):
        if self.zoom_mode:
            self.zoom_mode = False
            self.update()

            self.refresh_zoom_buttons(self.width())

    def on_zoom_cancel(self):
        if self.zoom_mode:
            self.zoom_mode = False
            self.zoom_rect = QRect()
            self.update()

            self.refresh_zoom_buttons(self.width())

    def on_zoom_reset(self):
        if not self.zoom_rect.isEmpty():
            self.zoom_rect = QRect()
            self.update()

            self.zoom_reset_button.hide()
            self.zoom_button.show()

            self.refresh_zoom_buttons(self.width())

    def set_image_file_name(self, file_name, image_options):
        # tprint("Set preview file:", fileName)

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
            if self.zoom_mode:
                self.zoom_origin = event.pos()

                self.zoom_rect = QRect(self.zoom_origin, QSize())
            else:
                self.rubberband_origin = event.pos()

                self.rubberband_rect = QRect(self.rubberband_origin, QSize())

                self.rubberband_changed.emit(self.rubberband_rect)

                self.pressed.emit(event.pos())

            self.mouse_pressed = True

        self.mouse_moved = False

    def mouseMoveEvent(self, event):  # Note: Qt override
        if self.mouse_pressed:
            if self.zoom_mode:
                self.zoom_rect = QRect(self.zoom_origin, event.pos()).normalized()

                self.update()
            else:
                self.rubberband_rect = QRect(self.rubberband_origin, event.pos()).normalized()

                diff = event.pos() - self.rubberband_origin
                if diff.manhattanLength() > 3:
                    self.rubberband_changed.emit(self.rubberband_rect)

                    self.moved.emit(event.pos())

                    self.mouse_moved = True

    def mouseReleaseEvent(self, event):  # Note: Qt override
        if not self.zoom_mode:
            if not self.mouse_moved:
                if event.button() == QtCore.Qt.LeftButton:
                    self.clicked.emit(event.pos())
                elif event.button() == QtCore.Qt.RightButton:
                    self.right_clicked.emit(event.pos())

        self.mouse_pressed = False

    def mouseDoubleClickEvent(self, event):  # Note: Qt override
        if not self.zoom_mode:
            self.double_clicked.emit(event.pos())

    def refresh_zoom_buttons(self, width):
        self.zoom_button.setVisible(not self.zoom_mode)
        self.zoom_accept_button.setVisible(self.zoom_mode)
        self.zoom_cancel_button.setVisible(self.zoom_mode)
        self.zoom_reset_button.setVisible(not self.zoom_mode and not self.zoom_rect.isEmpty())

        x = 0
        offset = self.zoom_button.height() + 4

        if self.zoom_button.isVisible():
            self.zoom_button.move(width - self.zoom_button.width(), x)
            x += offset
        if self.zoom_accept_button.isVisible():
            self.zoom_accept_button.move(width - self.zoom_accept_button.width(), x)
            x += offset
        if self.zoom_cancel_button.isVisible():
            self.zoom_cancel_button.move(width - self.zoom_cancel_button.width(), x)
            x += offset
        if self.zoom_reset_button.isVisible():
            self.zoom_reset_button.move(width - self.zoom_reset_button.width(), x)
            x += offset

    def resizeEvent(self, event):  # Note: Qt override
        if not self.roi_grid is None:
            self.roi_grid.setGeometry(0, 0, event.size().width(), event.size().height())
 
        self.refresh_zoom_buttons(event.size().width())

