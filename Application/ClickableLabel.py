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

import os
import tempfile

from plantcv import plantcv as pcv
from PySide6 import QtCore
from PySide6.QtCore import QPoint, QRect, QSize, QTimer
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QLabel, QPushButton

import rayn_utils
from Helper import tprint


class ClickableLabel(QLabel):
    pressed = QtCore.Signal(QPoint)
    clicked = QtCore.Signal(QPoint)
    right_clicked = QtCore.Signal(QPoint)
    moved = QtCore.Signal(QPoint)
    double_clicked = QtCore.Signal(QPoint)
    rubberband_changed = QtCore.Signal(QRect)
    crop_rect_changed = QtCore.Signal(QRect)
    crop_state_changed = QtCore.Signal()
    crop_accepted = QtCore.Signal()
    crop_reset = QtCore.Signal()
    image_file_name_changed = QtCore.Signal()
    magnify_state_changed = QtCore.Signal(bool, QPoint, float)

    def __init__(self, parent):
        QLabel.__init__(self, parent)

        self.mouse_pressed = False
        self.mouse_moved = False

        self.rubberband_origin = QPoint()
        self.rubberband_rect = QRect()

        self.image_file_name = ""

        self.original_image = QPixmap()

        self.roi_grid = None

        self.crop_mode = False
        self.crop_origin = QPoint()
        self.crop_edit_rect = QRect()
        self.crop_rect = QRect()
        self.crop_pixmap = QPixmap()

        self.show_crop_buttons = False

        self.magnifier_mode = False
        self.magnifier_size = 100
        self.setMouseTracking(True)
        self.mouse_pos = QPoint()

        button_stylesheet = "background-color: #444; color: white;"

        self.select_image_button = QPushButton("Image...", self)
        self.select_image_button.setMaximumWidth(70)
        self.select_image_button.setDefault(False)
        self.select_image_button.setAutoDefault(False)
        self.select_image_button.setStyleSheet(button_stylesheet)

        self.crop_button = QPushButton("Crop", self)
        self.crop_button.setFixedWidth(55)
        self.crop_button.setDefault(False)
        self.crop_button.setAutoDefault(False)
        self.crop_button.setStyleSheet(button_stylesheet)
        self.crop_button.clicked.connect(self.on_crop)
        self.crop_button.hide()

        self.crop_accept_button = QPushButton("Accept", self)
        self.crop_accept_button.setFixedWidth(55)
        self.crop_accept_button.setDefault(False)
        self.crop_accept_button.setAutoDefault(False)
        self.crop_accept_button.setStyleSheet(button_stylesheet)
        self.crop_accept_button.clicked.connect(self.on_crop_accept)
        self.crop_accept_button.hide()

        self.crop_cancel_button = QPushButton("Cancel", self)
        self.crop_cancel_button.setFixedWidth(55)
        self.crop_cancel_button.setDefault(False)
        self.crop_cancel_button.setAutoDefault(False)
        self.crop_cancel_button.setStyleSheet(button_stylesheet)
        self.crop_cancel_button.clicked.connect(self.on_crop_cancel)
        self.crop_cancel_button.hide()

        self.crop_reset_button = QPushButton("Reset", self)
        self.crop_reset_button.setFixedWidth(55)
        self.crop_reset_button.setDefault(False)
        self.crop_reset_button.setAutoDefault(False)
        self.crop_reset_button.setStyleSheet(button_stylesheet)
        self.crop_reset_button.clicked.connect(self.on_crop_reset)
        self.crop_reset_button.hide()

        self.magnify_button = QPushButton(QIcon(":/images/Magnify.png"), "", self)
        self.magnify_button.setFixedWidth(40)
        self.magnify_button.setDefault(False)
        self.magnify_button.setAutoDefault(False)
        self.magnify_button.setStyleSheet(button_stylesheet)
        self.magnify_button.clicked.connect(self.on_magnify)
        self.magnify_button.hide()

        self.show_magnify_button = True

        QTimer.singleShot(300, lambda: self.refresh())  # Delayed initial refresh to make sure sizes are established

    def paintEvent(self, e):  # Qt override, keep casing
        super().paintEvent(e)

        painter = QPainter(self)

        if self.magnifier_mode:
            if self.mouse_pressed and not self.original_image.isNull():
                scaling_factor = self.pixmap().width() / self.original_image.width()
                half_size = self.magnifier_size / 2
                image_pos = QPoint(self.mouse_pos.x() / scaling_factor, self.mouse_pos.y() / scaling_factor)
                source_rect = self.original_image.copy(image_pos.x() - half_size, image_pos.y() - half_size,
                                                       self.magnifier_size, self.magnifier_size)
                magnified_pixmap = source_rect.scaled(self.magnifier_size, self.magnifier_size,
                                                      QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

                rect = QRect(self.mouse_pos.x() - half_size, self.mouse_pos.y() - half_size,
                             magnified_pixmap.width(), magnified_pixmap.height())

                painter.drawPixmap(rect, magnified_pixmap)
                painter.drawRect(rect)

        if not self.crop_mode and self.crop_edit_rect.isEmpty():
            return

        pen = QPen()
        pen.setColor(QColor('#888'))
        pen.setWidth(3)
        painter.setPen(pen)

        if not self.crop_edit_rect.isEmpty():
            painter.drawRect(self.crop_edit_rect)

    def refresh(self):
        self.refresh_crop_buttons(self.width())

        if self.show_magnify_button:
            self.magnify_button.show()
            self.magnify_button.move(self.width() - self.magnify_button.width(),
                                     self.height() - self.magnify_button.height())

    def set_crop_parent(self, parent):
        self.crop_button.setParent(parent)
        self.crop_accept_button.setParent(parent)
        self.crop_cancel_button.setParent(parent)
        self.crop_reset_button.setParent(parent)

    def on_crop(self):
        self.on_crop_reset()

        self.crop_mode = True
        self.crop_edit_rect = QRect()
        self.crop_rect = QRect()

        self.refresh_crop_buttons(self.width())

        self.crop_state_changed.emit()

    def on_crop_accept(self):
        if self.crop_mode:
            # Translate to original image coordinates by scaling through non-crop image / original_image ratio
            w = self.pixmap().width() / self.original_image.width()
            h = self.pixmap().height() / self.original_image.height()
            rect = QRect(self.crop_edit_rect.left() / w, self.crop_edit_rect.top() / h,
                         self.crop_edit_rect.width() / w, self.crop_edit_rect.height() / h)

            self.set_crop_rect(rect)

            self.refresh_image_size()

            self.crop_mode = False
            self.crop_edit_rect = QRect()

            self.refresh_crop_buttons(self.width())

            self.crop_state_changed.emit()
            self.crop_accepted.emit()

    def on_crop_cancel(self):
        if self.crop_mode:
            self.crop_mode = False
            self.crop_edit_rect = QRect()

            self.refresh_crop_buttons(self.width())

            self.crop_state_changed.emit()

    def on_crop_reset(self):
        if not self.crop_rect.isEmpty():
            self.crop_edit_rect = QRect()
            self.crop_rect = QRect()

            self.refresh_image_size()

            self.crop_reset_button.hide()
            self.crop_button.show()

            self.refresh_crop_buttons(self.width())

            self.crop_state_changed.emit()
            self.crop_reset.emit()

    def refresh_crop_buttons(self, width):
        if self.show_crop_buttons:
            self.crop_button.setVisible(not self.crop_mode)
            self.crop_accept_button.setVisible(self.crop_mode)
            self.crop_cancel_button.setVisible(self.crop_mode)
            self.crop_reset_button.setVisible(not self.crop_rect.isEmpty() and not self.crop_mode)

            x = 0
            offset = self.crop_button.height() + 4

            if self.crop_button.isVisible():
                self.crop_button.move(width - self.crop_button.width(), x)
                x += offset
            if self.crop_accept_button.isVisible():
                self.crop_accept_button.move(width - self.crop_accept_button.width(), x)
                x += offset
            if self.crop_cancel_button.isVisible():
                self.crop_cancel_button.move(width - self.crop_cancel_button.width(), x)
                x += offset
            if self.crop_reset_button.isVisible():
                self.crop_reset_button.move(width - self.crop_reset_button.width(), x)
                x += offset

            self.update()

    def set_crop_rect(self, rect):
        self.crop_rect = rect
        if not self.crop_rect.isEmpty():
            self.crop_pixmap = self.cropped_image()

            self.refresh_crop_buttons(self.width())

    def cropped_image(self):
        return self.original_image.copy(self.crop_rect).scaled(self.width(), self.height(),
                                                               QtCore.Qt.KeepAspectRatio,
                                                               QtCore.Qt.SmoothTransformation)

    def on_magnify(self):
        self.magnifier_mode = not self.magnifier_mode

        if self.magnifier_mode:
            self.magnify_button.setStyleSheet("background-color: #A62; color: black;")
        else:
            self.magnify_button.setStyleSheet("background-color: #444; color: white;")

    def refresh_image_size(self):
        # Scale pixmap to follow available space
        if not self.crop_rect.isEmpty():
            self.setPixmap(self.crop_pixmap.scaled(self.width(), self.height(),
                                                   QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        else:
            self.setPixmap(self.original_image.scaled(self.width(), self.height(),
                                                      QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

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
            if self.crop_mode:
                self.crop_origin = event.pos()

                self.crop_edit_rect = QRect(self.crop_origin, QSize())

                self.crop_rect_changed.emit(self.crop_edit_rect)
            elif self.magnifier_mode:
                self.mouse_pressed = True
                self.update()

                if self.mouse_pressed:
                    # Update preview image
                    scaling_factor = self.pixmap().width() / self.original_image.width()
                    self.magnify_state_changed.emit(True, self.mouse_pos, scaling_factor)
            else:
                self.rubberband_origin = event.pos()

                self.rubberband_rect = QRect(self.rubberband_origin, QSize())

                self.rubberband_changed.emit(self.rubberband_rect)

                self.pressed.emit(event.pos())

            self.mouse_pressed = True

        self.mouse_moved = False

    def mouseMoveEvent(self, event):  # Note: Qt override
        if self.magnifier_mode:
            self.mouse_pos = event.pos()
            self.update()

            if self.mouse_pressed:
                # Update preview image
                scaling_factor = self.pixmap().width() / self.original_image.width()
                self.magnify_state_changed.emit(True, self.mouse_pos, scaling_factor)

        elif self.mouse_pressed:
            if self.crop_mode:
                self.crop_edit_rect = QRect(self.crop_origin, event.pos()).normalized()

                self.crop_rect_changed.emit(self.crop_edit_rect)

                self.update()
            else:
                self.rubberband_rect = QRect(self.rubberband_origin, event.pos()).normalized()

                diff = event.pos() - self.rubberband_origin
                if diff.manhattanLength() > 3:
                    self.rubberband_changed.emit(self.rubberband_rect)

                    self.moved.emit(event.pos())

                    self.mouse_moved = True

    def mouseReleaseEvent(self, event):  # Note: Qt override
        if self.magnifier_mode:
            self.update()
            self.magnify_state_changed.emit(False, self.mouse_pos, 1.0)

        elif not self.crop_mode:
            if not self.mouse_moved:
                if event.button() == QtCore.Qt.LeftButton:
                    self.clicked.emit(event.pos())
                elif event.button() == QtCore.Qt.RightButton:
                    self.right_clicked.emit(event.pos())

        self.mouse_pressed = False

    def mouseDoubleClickEvent(self, event):  # Note: Qt override
        if not self.crop_mode:
            self.double_clicked.emit(event.pos())

    def resizeEvent(self, event):  # Note: Qt override
        if self.roi_grid is not None:
            self.roi_grid.setGeometry(0, 0, event.size().width(), event.size().height())

        self.refresh()

