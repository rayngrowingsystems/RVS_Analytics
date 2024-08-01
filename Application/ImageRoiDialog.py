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

from PySide6.QtWidgets import QDialog, QWidget, QMessageBox, QPushButton
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import QRect, QPoint, QSize, QTimer

from PySide6 import QtCore

import CameraApp_rc

from Experiment import Experiment

from ui_ImageRoiDialog import Ui_ImageRoiDialog

from SelectImageDialog import SelectImageDialog


class RoiGrid(QWidget):

    def __init__(self, parent, dialog):
        super(RoiGrid, self).__init__(parent)

        self.dialog = dialog

        self.invalid_rois = False

    def paintEvent(self, e):  # Qt override, keep casing
        painter = QPainter(self)
        pen = QPen()
        pen.setColor(QColor('#888'))
        pen.setWidth(3)
        painter.setPen(pen)

        font = painter.font()
        font.setPixelSize(16)
        painter.setFont(font)

        items = []

        if self.dialog.placement_mode == Experiment.RoiInfo.PlacementMode.Matrix:
            if not self.dialog.rubberband_rect.isEmpty():
                # Draw rect
                painter.drawRect(self.dialog.rubberband_rect)

                columns = self.dialog.ui.columns_spinbox.value()
                rows = self.dialog.ui.rows_spinbox.value()

                rect = self.dialog.rubberband_rect

                # Draw column lines
                if columns > 1:
                    for column in range(columns):
                        x = rect.left() + column * (rect.width() / (columns - 1))
                        painter.drawLine(x, rect.top(), x, rect.top() + rect.height())

                # Draw row lines
                if rows > 1:
                    for row in range(rows):
                        y = rect.top() + row * (rect.height() / (rows - 1))
                        painter.drawLine(rect.left(), y, rect.left() + rect.width(), y)

                # Create list of points
                for row in range(rows):
                    for column in range(columns):
                        if columns > 1:
                            x = rect.left() + column * (rect.width() / (columns - 1))
                        else:
                            x = rect.left()

                        if rows > 1:
                            y = rect.top() + row * (rect.height() / (rows - 1))
                        else:
                            y = rect.top()

                        radius = self.dialog.ui.radius_spinbox.value()
                        width = self.dialog.ui.width_spinbox.value()
                        height = self.dialog.ui.height_spinbox.value()

                        if self.dialog.shape == Experiment.RoiInfo.Shape.Circle:
                            items.append(("Circle", x, y, radius * 2, radius * 2))  # Remember crosspoints to draw circles below
                        else:
                            items.append(("Rectangle", x, y, width, height))  # Remember crosspoints to draw circles below
        elif self.dialog.placement_mode == Experiment.RoiInfo.PlacementMode.Manual:
            items = self.dialog.manual_roi_items

        # Draw ROI circles/rectangles
        invalid_rois = False

        for index, item in enumerate(items):
            if self.dialog.placement_mode == Experiment.RoiInfo.PlacementMode.Matrix or item == self.dialog.focused_roi_item:
                pen.setColor(QColor('#FC4'))
            else:
                pen.setColor(QColor('#0A0'))
            painter.setPen(pen)

            item_type, x, y, width, height = item
            if item_type == "Circle":
                painter.drawEllipse(x - width / 2, y - height / 2, width, height)
            elif item_type == "Rectangle":
                painter.drawRect(x - width / 2, y - height / 2, width, height)

            painter.drawText(QRect(QPoint(x, y) - QPoint(15, 19), QSize(30, 18)), QtCore.Qt.AlignHCenter, str(index + 1))

            # Check if Roi is inside the image
            if x - width / 2 < 0 or y - height / 2 < 0 or x + width / 2 > painter.viewport().width() or y + height / 2 > painter.viewport().height():
                invalid_rois = True

        if invalid_rois:
            font = painter.font()
            font.setPixelSize(20)
            font.setBold(True)
            painter.setFont(font)
            pen.setColor(QColor('#F44'))
            painter.setPen(pen)
            painter.drawText(QRect(0, painter.viewport().center().y(), painter.viewport().width(), 30), QtCore.Qt.AlignHCenter, "Error: Roi(s) outside of image")

        self.invalid_rois = invalid_rois


class ImageRoiDialog(QDialog):
    def __init__(self, main_window):
        # Initialize the ImageRoiDialog instance with a reference to the main window
        self.main_window = main_window

        # Call the parent class's constructor
        super(ImageRoiDialog, self).__init__()

        # Define default values for matrix rows, columns, and radius
        DEFAULT_MATRIX_ROWS = 3
        DEFAULT_MATRIX_COLUMNS = 3
        DEFAULT_RADIUS = 20

        # Set window flags to remove 'What's this' icon from the title bar
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint)

        # Load the UI elements for the dialog
        self.load_ui()

        # Connect signals from reference images to corresponding slots
        self.ui.reference_image1.pressed.connect(self.on_pressed)
        self.ui.reference_image2.pressed.connect(self.on_pressed)

        self.ui.reference_image1.clicked.connect(self.on_clicked)
        self.ui.reference_image2.clicked.connect(self.on_clicked)

        self.ui.reference_image1.right_clicked.connect(self.on_right_clicked)
        self.ui.reference_image2.right_clicked.connect(self.on_right_clicked)

        self.ui.reference_image1.moved.connect(self.on_moved)
        self.ui.reference_image2.moved.connect(self.on_moved)

        self.ui.reference_image1.rubberband_changed.connect(self.on_rubberband_changed)
        self.ui.reference_image2.rubberband_changed.connect(self.on_rubberband_changed)

        # Create and configure ROI grids for reference images
        self.roi_grid1 = RoiGrid(self.ui.reference_image1, self)
        self.ui.reference_image1.set_roi_grid(self.roi_grid1)
        image_button = QPushButton("Image...", self.roi_grid1)
        image_button.setMaximumWidth(55)
        image_button.setDefault(False)
        image_button.setAutoDefault(False)
        image_button.clicked.connect(self.select_reference_image1)

        self.roi_grid2 = RoiGrid(self.ui.reference_image2, self)
        self.ui.reference_image2.set_roi_grid(self.roi_grid2)
        image_button = QPushButton("Image...", self.roi_grid2)
        image_button.setMaximumWidth(55)
        image_button.setDefault(False)
        image_button.setAutoDefault(False)
        image_button.clicked.connect(self.select_reference_image2)

        # Set geometries and show ROI grids
        self.roi_grid1.setGeometry(self.ui.reference_image1.geometry())
        self.roi_grid2.setGeometry(self.ui.reference_image2.geometry())

        self.roi_grid1.show()
        self.roi_grid2.show()

        # Initialize placement mode, shape, and default values for ROI parameters
        self.placement_mode = Experiment.RoiInfo.PlacementMode.Matrix

        self.shape = Experiment.RoiInfo.Shape.Circle

        self.ui.columns_spinbox.setValue(DEFAULT_MATRIX_COLUMNS)
        self.ui.rows_spinbox.setValue(DEFAULT_MATRIX_ROWS)

        self.ui.radius_spinbox.setValue(DEFAULT_RADIUS)

        # Connect signals for updating ROI grid based on parameter changes
        self.ui.columns_spinbox.valueChanged.connect(self.refresh_roi_grid)
        self.ui.rows_spinbox.valueChanged.connect(self.refresh_roi_grid)

        self.ui.width_spinbox.valueChanged.connect(self.refresh_roi_grid)
        self.ui.height_spinbox.valueChanged.connect(self.refresh_roi_grid)

        self.ui.width_spinbox.valueChanged.connect(self.refresh_width)
        self.ui.height_spinbox.valueChanged.connect(self.refresh_height)

        self.ui.radius_spinbox.valueChanged.connect(self.refresh_radius)
        self.ui.radius_spinbox.valueChanged.connect(self.refresh_roi_grid)

        # Connect signals for clearing ROIs and cancelling the dialog
        self.ui.clear_button.clicked.connect(self.clear_rois)
        self.ui.cancel_button.clicked.connect(self.reject)

        # Initialize manual ROI items and focused ROI item
        self.manual_roi_items = self.main_window.experiment.roi_info.manual_roi_items

        self.focused_roi_item = None

        # Restore previous settings for ROI parameters
        self.rubberband_rect = self.main_window.experiment.roi_info.rect
        self.ui.reference_image1.rubberband_rect = self.rubberband_rect
        self.ui.reference_image2.rubberband_rect = self.rubberband_rect

        self.ui.columns_spinbox.setValue(self.main_window.experiment.roi_info.columns)
        self.ui.rows_spinbox.setValue(self.main_window.experiment.roi_info.rows)
        self.ui.radius_spinbox.setValue(self.main_window.experiment.roi_info.radius)

        self.ui.width_spinbox.setValue(self.main_window.experiment.roi_info.width)
        self.ui.height_spinbox.setValue(self.main_window.experiment.roi_info.height)

        self.ui.roi_placement_mode.setCurrentIndex(self.main_window.experiment.roi_info.placement_mode_number())
        self.ui.roi_shape.setCurrentIndex(self.main_window.experiment.roi_info.shape_number())

        # Connect signals for ROI placement mode and shape changes
        self.ui.roi_placement_mode.currentIndexChanged.connect(self.on_placement_mode_change)
        self.ui.roi_shape.currentIndexChanged.connect(self.on_shape_change)

        # Update controls and refresh info label
        self.update_controls()

        self.refresh_info_label()

        # Load reference images after a short delay
        self.rubberband_rect = self.main_window.experiment.roi_info.rect

        QTimer.singleShot(200, lambda: self.load_reference_images())

    def load_ui(self):
        self.ui = Ui_ImageRoiDialog()
        self.ui.setupUi(self)

    def accept(self):
        if not self.roi_grid1.invalid_rois and not self.ui.reference_image1.original_image_size.isEmpty() and not self.ui.reference_image1.size().isEmpty() and (self.rubberband_rect.isValid() or len(self.manual_roi_items) > 0):
            super(ImageRoiDialog, self).accept()
        else:
            QMessageBox.warning(self, "Incomplete setup", "You must have at least one preview image and a valid ROI")

    def clear_rois(self):
        self.manual_roi_items = []
        self.rubberband_rect = QRect()

        self.refresh_info_label()
        self.refresh_roi_grid()

    def select_reference_image1(self):
        select_image_dialog = SelectImageDialog(self, self.ui.reference_image1)

        select_image_dialog.exec()

    def select_reference_image2(self):
        if self.ui.reference_image1.image_file_name != "":
            select_image_dialog = SelectImageDialog(self, self.ui.reference_image2)

            select_image_dialog.exec()
        else:
            QMessageBox.warning(self, "Image selection", "You must select the left image first")

    def load_reference_images(self):
        if self.main_window.experiment.roi_reference_image1 is not None:
            self.ui.reference_image1.set_image_file_name(self.main_window.experiment.roi_reference_image1, self.main_window.experiment.lens_angle, self.main_window.experiment.normalize, self.main_window.experiment.light_correction)
            print("Roi: Load left preview image:", self.main_window.experiment.roi_reference_image1)

        if self.main_window.experiment.roi_reference_image2 is not None:
            self.ui.reference_image2.set_image_file_name(self.main_window.experiment.roi_reference_image2, self.main_window.experiment.lens_angle, self.main_window.experiment.normalize, self.main_window.experiment.light_correction)
            print("Roi: Load right preview image:", self.main_window.experiment.roi_reference_image2)

    def refresh_roi_grid(self):
        self.roi_grid1.update()
        self.roi_grid2.update()

    def refresh_radius(self, value):
        self.update_item_radius(self.focused_roi_item, value)

    def refresh_width(self, value):
        self.update_item_width(self.focused_roi_item, value)

    def refresh_height(self, value):
        self.update_item_height(self.focused_roi_item, value)

    def refresh_info_label(self):
        if self.placement_mode == Experiment.RoiInfo.PlacementMode.Matrix:
            self.ui.info_label.setText("<br><b>Instructions</b><br>Click-and-drag to create a matrix frame with row and column")
        elif self.placement_mode == Experiment.RoiInfo.PlacementMode.Manual:
            self.ui.info_label.setText("<br><b>Instructions</b><br>Click to place item, right-click item to delete<br>Click on existing item to select for change<br>Click-and-drag item to move selected item")

    def refresh_shape(self):
        self.ui.roi_shape.blockSignals(True)

        if self.shape == Experiment.RoiInfo.Shape.Circle:
            self.ui.roi_shape.setCurrentIndex(0)
        else:
            self.ui.roi_shape.setCurrentIndex(1)

        self.ui.roi_shape.blockSignals(False)

    def refresh_placement_mode(self):
        self.ui.roi_placement_mode.blockSignals(True)

        if self.placement_mode == Experiment.RoiInfo.PlacementMode.Matrix:
            self.ui.roi_placement_mode.setCurrentIndex(0)
        else:
            self.ui.roi_placement_mode.setCurrentIndex(1)

        self.ui.roi_placement_mode.blockSignals(False)

    def on_placement_mode_change(self):
        if QMessageBox.question(self, "Confirm mode change", "Switching placement mode will clear existing items. Continue?") == QMessageBox.Yes:
            self.update_controls()

            if self.placement_mode == Experiment.RoiInfo.PlacementMode.Matrix:
                self.manual_roi_items = []
            elif self.placement_mode == Experiment.RoiInfo.PlacementMode.Manual:
                self.rubberband_rect = QRect()

            self.refresh_info_label()
            self.refresh_roi_grid()
        else:
            # Restore previous index
            self.refresh_placement_mode()

    def on_shape_change(self):
        self.update_controls()

        if self.shape == Experiment.RoiInfo.Shape.Circle:
            self.update_item_type(self.focused_roi_item, "Circle")
            self.update_item_radius(self.focused_roi_item, self.ui.width_spinbox.value())
        elif self.shape == Experiment.RoiInfo.Shape.Rectangle:
            self.update_item_type(self.focused_roi_item, "Rectangle")

        self.refresh_roi_grid()

    def update_controls(self):
        if self.ui.roi_placement_mode.currentIndex() == 0:
            self.ui.columns_spinbox.show()
            self.ui.rows_spinbox.show()
            self.ui.columns_label.show()
            self.ui.rows_label.show()

            self.placement_mode = Experiment.RoiInfo.PlacementMode.Matrix
        else:
            self.ui.columns_spinbox.hide()
            self.ui.rows_spinbox.hide()
            self.ui.columns_label.hide()
            self.ui.rows_label.hide()

            self.placement_mode = Experiment.RoiInfo.PlacementMode.Manual

        if self.ui.roi_shape.currentIndex() == 0:
            self.ui.width_spinbox.hide()
            self.ui.height_spinbox.hide()
            self.ui.width_label.hide()
            self.ui.height_label.hide()

            self.ui.radius_label.show()
            self.ui.radius_spinbox.show()

            self.shape = Experiment.RoiInfo.Shape.Circle
        else:
            self.ui.width_spinbox.show()
            self.ui.height_spinbox.show()
            self.ui.width_label.show()
            self.ui.height_label.show()

            self.ui.radius_label.hide()
            self.ui.radius_spinbox.hide()

            self.shape = Experiment.RoiInfo.Shape.Rectangle

        self.refresh_roi_grid()

    def on_pressed(self, point):
        # print("onPressed", self.focusedRoiItem, point)
        if self.placement_mode == Experiment.RoiInfo.PlacementMode.Manual:
            item = self.item_at(point)
            if item is not None:
                self.focused_roi_item = item

                # item = ("Circle", point.x(), point.y(), radius * 2, radius * 2,)
                print("Load values for selected item", item)

                self.ui.radius_spinbox.setValue(item[3] / 2)
                self.ui.width_spinbox.setValue(item[3])
                self.ui.height_spinbox.setValue(item[4])

                if item[0] == "Circle":
                    self.shape = Experiment.RoiInfo.Shape.Circle

                if item[0] == "Rectangle":
                    self.shape = Experiment.RoiInfo.Shape.Rectangle

                self.refresh_shape()
                self.update_controls()

                self.refresh_roi_grid()

    def on_clicked(self, point):
        # print("onClicked", self.focusedRoiItem, point)
        if self.placement_mode == Experiment.RoiInfo.PlacementMode.Manual:
            item = self.item_at(point)
            if item is None:
                # Add new item
                if self.shape == Experiment.RoiInfo.Shape.Circle:
                    radius = self.ui.radius_spinbox.value()

                    item = ("Circle", point.x(), point.y(), radius * 2, radius * 2,)
                    self.add_item(item)
                elif self.shape == Experiment.RoiInfo.Shape.Rectangle:
                    width = self.ui.width_spinbox.value()
                    height = self.ui.height_spinbox.value()

                    item = ("Rectangle", point.x(), point.y(), width, height, )
                    self.add_item(item)

            self.refresh_roi_grid()

    def on_right_clicked(self, point):
        if self.placement_mode == Experiment.RoiInfo.PlacementMode.Manual:
            item = self.item_at(point)
            if item is not None:
                self.remove_item(item)

                self.refresh_roi_grid()

    def on_moved(self, point):
        if self.placement_mode == Experiment.RoiInfo.PlacementMode.Manual and self.focused_roi_item is not None:
            # print("onMoved", self.focusedRoiItem, point)

            self.update_item_position(self.focused_roi_item, point)

            self.refresh_roi_grid()

    def on_rubberband_changed(self, rect):
        if self.placement_mode == Experiment.RoiInfo.PlacementMode.Matrix:
            self.rubberband_rect = rect
            self.refresh_roi_grid()

    def contains_item(self, existing_item, new_item):
        item_type, center_x, center_y, width, height = existing_item
        item_type2, center_x2, center_y2, width2, height2 = new_item
        if center_x2 > center_x - width / 2 and center_x2 < center_x + width / 2 and center_y2 > center_y - height / 2 and center_y2 < center_y + height / 2:
            return True

        return False

    def contains_point(self, item, point):
        item_type, center_x, center_y, width, height = item
        if point.x() > center_x - width / 2 and point.x() < center_x + width / 2 and point.y() > center_y - height / 2 and point.y() < center_y + height / 2:
            return True

        return False

    def item_exist(self, item):
        for it in self.manual_roi_items:
            if self.contains_item(it, item):
                return True

        return False

    def add_item(self, item):
        self.manual_roi_items.append(item)
        self.focused_roi_item = item

    def remove_item(self, item):
        for it in self.manual_roi_items:
            if self.contains_item(it, item):
                self.manual_roi_items.remove(it)
                break

    def item_at(self, point):
        for item in self.manual_roi_items:
            if self.contains_point(item, point):
                return item

        return None

    def update_item_type(self, item, type):
        for index, it in enumerate(self.manual_roi_items):
            if it == item:
                as_list = list(self.manual_roi_items[index])
                as_list[0] = type
                self.manual_roi_items[index] = tuple(as_list)
                self.focused_roi_item = self.manual_roi_items[index]

    def update_item_position(self, item, point):
        for index, it in enumerate(self.manual_roi_items):
            if it == item:
                as_list = list(self.manual_roi_items[index])
                as_list[1] = point.x()
                as_list[2] = point.y()
                self.manual_roi_items[index] = tuple(as_list)
                self.focused_roi_item = self.manual_roi_items[index]

    def update_item_radius(self, item, radius):
        for index, it in enumerate(self.manual_roi_items):
            if it == item:
                as_list = list(self.manual_roi_items[index])
                if as_list[0] == "Circle":
                    as_list[3] = radius * 2
                    as_list[4] = radius * 2
                    self.manual_roi_items[index] = tuple(as_list)
                    self.focused_roi_item = self.manual_roi_items[index]

    def update_item_width(self, item, width):
        for index, it in enumerate(self.manual_roi_items):
            if it == item:
                as_list = list(self.manual_roi_items[index])
                if as_list[0] == "Rectangle":
                    as_list[3] = width
                    self.manual_roi_items[index] = tuple(as_list)
                    self.focused_roi_item = self.manual_roi_items[index]

    def update_item_height(self, item, height):
        for index, it in enumerate(self.manual_roi_items):
            if it == item:
                as_list = list(self.manual_roi_items[index])
                if as_list[0] == "Rectangle":
                    as_list[4] = height
                    self.manual_roi_items[index] = tuple(as_list)
                    self.focused_roi_item = self.manual_roi_items[index]
