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
from PySide6.QtGui import QPainter, QColor, QPen, QPolygon
from PySide6.QtCore import QRect, QPoint, QSize, QTimer

from PySide6 import QtCore

import CameraApp_rc

from Experiment import Experiment

from ui_ImageRoiDialog import Ui_ImageRoiDialog

from SelectImageDialog import SelectImageDialog

from Helper import tprint

# TODO Move to its own class when we have merged into main, to avoid confusion with new file
class RoiGrid(QWidget):

    def __init__(self, parent, dialog, items):
        super(RoiGrid, self).__init__(parent)

        self.dialog = dialog

        self.item_list = items

        self.editing_mode = hasattr(self.dialog, "placement_mode")

        self.scaling_factor = 1.0

        self.invalid_rois = False

        self.show_rois = True

        self.visible_image_size = QSize()

    def paintEvent(self, e):  # Qt override, keep casing
        if not self.show_rois:
            return
        
        painter = QPainter(self)
        pen = QPen()
        pen.setColor(QColor('#888'))
        pen.setWidth(3)
        painter.setPen(pen)

        font = painter.font()
        font.setPixelSize(16)
        painter.setFont(font)

        items = []

        if self.editing_mode:  # Used by ImageRoiDialog?
            # Matrix mode
            if self.dialog.placement_mode == Experiment.RoiInfo.PlacementMode.Matrix:
                if not self.dialog.rubberband_rect.isEmpty():
                    # Draw rect
                    painter.drawRect(self.dialog.image_to_rect_coordinates(self.dialog.rubberband_rect))

                    columns = self.dialog.ui.columns_spinbox.value()
                    rows = self.dialog.ui.rows_spinbox.value()

                    rect = self.dialog.rubberband_rect

                    # All other items are scaled below, except for the grid lines that need to be scaled here
                    line_rect = QRect(rect.x() * self.scaling_factor, rect.y() * self.scaling_factor, rect.width() * self.scaling_factor, rect.height() * self.scaling_factor)

                    # Draw column lines
                    if columns > 1:
                        for column in range(columns):
                            x = line_rect.left() + column * (line_rect.width() / (columns - 1))
                            painter.drawLine(x, line_rect.top(), x, line_rect.top() + line_rect.height())

                    # Draw row lines
                    if rows > 1:
                        for row in range(rows):
                            y = line_rect.top() + row * (line_rect.height() / (rows - 1))
                            painter.drawLine(line_rect.left(), y, line_rect.left() + line_rect.width(), y)

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

                            # Remember crosspoints to draw items below
                            d = {}
                            if self.dialog.shape == Experiment.RoiInfo.Shape.Circle:
                                d["type"] = "Circle"
                                d["x"] = int(x)
                                d["y"] = int(y)
                                d["width"] = int(radius * 2)
                                d["height"] = int(radius * 2)
                            elif self.dialog.shape == Experiment.RoiInfo.Shape.Rectangle:
                                d["type"] = "Rectangle"
                                d["x"] = int(x)
                                d["y"] = int(y)
                                d["width"] = int(width)
                                d["height"] = int(height)
                            elif self.dialog.shape == Experiment.RoiInfo.Shape.Ellipse:
                                d["type"] = "Ellipse"
                                d["x"] = int(x)
                                d["y"] = int(y)
                                d["width"] = int(width)
                                d["height"] = int(height)
                            # Polygon not supported in Matrix mode

                            items.append(d)
                    self.dialog.current_matrix_items = items
                else:
                    self.dialog.current_matrix_items = []
            # Manual mode
            elif self.dialog.placement_mode == Experiment.RoiInfo.PlacementMode.Manual:
                items = self.dialog.manual_roi_items
        else:
            items = self.item_list  # Use the fixed items list from the constructor

        # Draw ROI items
        invalid_rois = False

        for index, item in enumerate(items):
            if not self.editing_mode:
                pen.setColor(QColor('#666'))
            elif self.dialog.placement_mode == Experiment.RoiInfo.PlacementMode.Matrix or item == self.dialog.focused_roi_item:
                pen.setColor(QColor('#FC4'))
            else:
                pen.setColor(QColor('#0A0'))
            painter.setPen(pen)

            item_type = item["type"]

            p = self.dialog.main_window.experiment.image_to_point_coordinates(QPoint(item["x"], item["y"]), self.dialog.ui.reference_image1.crop_rect, self.scaling_factor)
            x = p.x()
            y = p.y()

            width = item["width"] * self.scaling_factor
            height = item["height"] * self.scaling_factor

            if item_type in ["Circle", "Ellipse"]:
                painter.drawEllipse(x - width / 2, y - height / 2, width, height)
            elif item_type == "Rectangle":
                painter.drawRect(x - width / 2, y - height / 2, width, height)
            elif item_type == "Polygon":
                polygon = QPolygon()
                if "points" in item:
                    points = item["points"]
                    for point in points:
                        p = self.dialog.main_window.experiment.image_to_point_coordinates(QPoint(point[0], point[1]), self.dialog.ui.reference_image1.crop_rect, self.scaling_factor)
                        x = p.x()
                        y = p.y()

                        polygon.append(QPoint(x, y))
                        
                    if polygon.size() == 1:  # Single point?
                        painter.drawEllipse(polygon.at(0), 2, 2)
                    elif polygon.size() >= 2 and polygon[0] == polygon[-1]:  # Closed?
                        painter.drawPolygon(polygon)
                    else:
                        painter.drawPolyline(polygon)

                    x = polygon.boundingRect().center().x()
                    y = polygon.boundingRect().center().y   ()

            painter.drawText(QRect(QPoint(x, y) - QPoint(15, 19), QSize(30, 18)), QtCore.Qt.AlignHCenter, str(index + 1))

            # Check if Roi is inside the image
            if self.editing_mode:
                if item_type == "Polygon":
                    if polygon and not QRect(QPoint(0, 0), self.visible_image_size).contains(polygon.boundingRect()):
                        invalid_rois = True
                else:
                    image_width = self.visible_image_size.width()
                    image_height = self.visible_image_size.height()
                    if x - width / 2 < 0 or y - height / 2 < 0 or x + width / 2 > image_width or y + height / 2 > image_height:
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
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMaximizeButtonHint)

        # Load the UI elements for the dialog
        self.load_ui()

        # Initialize placement mode, shape, and default values for ROI parameters
        self.placement_mode = Experiment.RoiInfo.PlacementMode.Matrix

        self.shape = Experiment.RoiInfo.Shape.Circle

        self.detection_mode = Experiment.RoiInfo.DetectionMode.Partial

        self.polygon = QPolygon()
        self.polygon_closed = True

        self.last_move_point = QPoint()

        self.current_matrix_items = []

        # Connect signals from reference images to corresponding slots
        self.ui.reference_image1.pressed.connect(self.on_pressed)
        self.ui.reference_image2.pressed.connect(self.on_pressed)

        self.ui.reference_image1.clicked.connect(self.on_clicked)
        self.ui.reference_image2.clicked.connect(self.on_clicked)

        self.ui.reference_image1.right_clicked.connect(self.on_right_clicked)
        self.ui.reference_image2.right_clicked.connect(self.on_right_clicked)

        self.ui.reference_image1.double_clicked.connect(self.on_double_clicked)
        self.ui.reference_image2.double_clicked.connect(self.on_double_clicked)

        self.ui.reference_image1.moved.connect(self.on_moved)
        self.ui.reference_image2.moved.connect(self.on_moved)

        self.ui.reference_image1.rubberband_changed.connect(self.on_rubberband_changed)
        self.ui.reference_image2.rubberband_changed.connect(self.on_rubberband_changed)

        self.ui.reference_image1.crop_rect_changed.connect(self.on_crop_rect_changed)
        self.ui.reference_image2.crop_rect_changed.connect(self.on_crop_rect_changed)

        self.ui.reference_image1.crop_state_changed.connect(self.on_crop_state_changed)
        self.ui.reference_image2.crop_state_changed.connect(self.on_crop_state_changed)

        self.ui.reference_image1.crop_accepted.connect(self.on_crop_accepted)
        self.ui.reference_image2.crop_accepted.connect(self.on_crop_accepted)

        self.ui.reference_image1.crop_reset.connect(self.on_crop_reset)
        self.ui.reference_image2.crop_reset.connect(self.on_crop_reset)

        # Create and configure ROI grids for reference images
        self.roi_grid1 = RoiGrid(self.ui.reference_image1, self, [])
        self.ui.reference_image1.set_roi_grid(self.roi_grid1)

        self.roi_grid2 = RoiGrid(self.ui.reference_image2, self, [])
        self.ui.reference_image2.set_roi_grid(self.roi_grid2)

        self.ui.reference_image1.show_crop_buttons = True
        self.ui.reference_image1.select_image_button.setParent(self.roi_grid1)
        self.ui.reference_image1.select_image_button.clicked.connect(self.select_reference_image1)
 
        self.ui.reference_image2.show_crop_buttons = False
        self.ui.reference_image2.select_image_button.setParent(self.roi_grid2)
        self.ui.reference_image2.select_image_button.clicked.connect(self.select_reference_image2)

        self.ui.reference_image1.set_crop_parent(self.roi_grid1)
        self.ui.reference_image2.set_crop_parent(self.roi_grid2)

        # Set geometries and show ROI grids
        self.roi_grid1.setGeometry(self.ui.reference_image1.geometry())
        self.roi_grid2.setGeometry(self.ui.reference_image2.geometry())

        self.roi_grid1.show()
        self.roi_grid2.show()

        self.ui.columns_spinbox.setValue(DEFAULT_MATRIX_COLUMNS)
        self.ui.rows_spinbox.setValue(DEFAULT_MATRIX_ROWS)

        # self.ui.radius_spinbox.setValue(DEFAULT_RADIUS)

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

        self.skip_clicked = False

        self.ui.reference_image1.image_file_name_changed.connect(self.refresh_image_sizes)
        self.ui.reference_image2.image_file_name_changed.connect(self.refresh_image_sizes)

        # Restore previous settings for ROI parameters
        self.rubberband_rect = self.main_window.experiment.roi_info.rect
        self.ui.reference_image1.rubberband_rect = self.rubberband_rect
        self.ui.reference_image2.rubberband_rect = self.rubberband_rect

        self.ui.columns_spinbox.setValue(self.main_window.experiment.roi_info.columns)
        self.ui.rows_spinbox.setValue(self.main_window.experiment.roi_info.rows)
    
        self.ui.radius_spinbox.setValue(self.main_window.experiment.roi_info.radius)
        self.ui.width_spinbox.setValue(self.main_window.experiment.roi_info.width)
        self.ui.height_spinbox.setValue(self.main_window.experiment.roi_info.height)

        self.ui.roi_placement_mode.setCurrentIndex(self.main_window.experiment.roi_info.placement_mode.value - 1)
        self.ui.roi_shape.setCurrentIndex(self.main_window.experiment.roi_info.shape.value - 1)
        self.ui.roi_detection_mode.setCurrentIndex(self.main_window.experiment.roi_info.detection_mode.value - 1)

        # Connect signals for ROI placement mode and shape changes
        self.ui.roi_placement_mode.currentIndexChanged.connect(self.on_placement_mode_change)
        self.ui.roi_shape.currentIndexChanged.connect(self.on_shape_change)
        self.ui.roi_detection_mode.currentIndexChanged.connect(self.on_detection_mode_change)

        # Update controls and refresh info label
        self.update_controls()

        self.refresh_info_label()

        # Load reference images after a short delay
        self.rubberband_rect = self.main_window.experiment.roi_info.rect

        QTimer.singleShot(300, lambda: self.load_reference_images())

        if self.main_window.test_mode:
            QTimer.singleShot(self.main_window.test_dialog_timeout, lambda:self.accept())

    def load_ui(self):
        self.ui = Ui_ImageRoiDialog()
        self.ui.setupUi(self)

    def accept(self):
        if not self.roi_grid1.invalid_rois and not self.ui.reference_image1.size().isEmpty() and (self.rubberband_rect.isValid() or len(self.manual_roi_items) > 0):
            super(ImageRoiDialog, self).accept()
        elif not self.rubberband_rect.isValid() and len(self.manual_roi_items) == 0:
            if QMessageBox.question(self, "Incomplete setup", "Do you want to continue without setting a ROI (the whole image will be used as a single ROI)?") == QMessageBox.StandardButton.Yes:
                super(ImageRoiDialog, self).accept()
        else:
            QMessageBox.warning(self, "Incomplete setup", "You must have at least one preview image and a valid ROI")

    def clear_rois(self):
        self.manual_roi_items = []
        self.rubberband_rect = QRect()

        self.refresh_info_label()
        self.refresh_roi_grid()

    def select_reference_image1(self):
        self.main_window.select_image_dialog(self.main_window, self, self.ui.reference_image1)

    def select_reference_image2(self):
        if self.ui.reference_image1.image_file_name != "":
            self.main_window.select_image_dialog(self.main_window, self, self.ui.reference_image2)
        else:
            QMessageBox.warning(self, "Image selection", "You must select the left image first")

    def load_reference_images(self):
        if self.main_window.experiment.roi_reference_image1 not in [None, "."]:
            self.ui.reference_image1.set_image_file_name(self.main_window.experiment.roi_reference_image1, self.main_window.experiment.image_options_to_dict())
            self.roi_grid1.show_rois = True
            tprint("Roi: Load left preview image:", self.main_window.experiment.roi_reference_image1)
        else:
            self.roi_grid1.show_rois = False

        if self.main_window.experiment.roi_reference_image2 not in [None, "."]:
            self.ui.reference_image2.set_image_file_name(self.main_window.experiment.roi_reference_image2, self.main_window.experiment.image_options_to_dict())
            self.roi_grid2.show_rois = True
            tprint("Roi: Load right preview image:", self.main_window.experiment.roi_reference_image2)
        else:
            self.roi_grid2.show_rois = False

        self.ui.reference_image1.set_crop_rect(self.main_window.experiment.crop_rect)
        self.ui.reference_image2.set_crop_rect(self.main_window.experiment.crop_rect)

        self.refresh_roi_grid()
        self.refresh_image_sizes()

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
            text = "<br><b>Instructions</b><br>Click to place item, right-click item to delete<br>Click on existing item to select for change<br>Click-and-drag item to move selected item"
            if self.shape == Experiment.RoiInfo.Shape.Polygon:
                text += "<br>Polygon: Click to add points. Double click to close and exit polygon mode"
            self.ui.info_label.setText(text)

    def refresh_shape(self):
        self.ui.roi_shape.blockSignals(True)

        if self.shape == Experiment.RoiInfo.Shape.Circle:
            self.ui.roi_shape.setCurrentIndex(0)
        elif self.shape == Experiment.RoiInfo.Shape.Rectangle:
            self.ui.roi_shape.setCurrentIndex(1)
        elif self.shape == Experiment.RoiInfo.Shape.Ellipse:
            self.ui.roi_shape.setCurrentIndex(2)
        elif self.shape == Experiment.RoiInfo.Shape.Polygon:
            self.ui.roi_shape.setCurrentIndex(3)

        self.ui.roi_shape.blockSignals(False)

    def refresh_placement_mode(self):
        self.ui.roi_placement_mode.blockSignals(True)

        if self.placement_mode == Experiment.RoiInfo.PlacementMode.Matrix:
            self.ui.roi_placement_mode.setCurrentIndex(0)
        else:
            self.ui.roi_placement_mode.setCurrentIndex(1)

        self.ui.roi_placement_mode.blockSignals(False)

    def refresh_detection_mode(self):
        self.ui.roi_detection_mode.blockSignals(True)

        if self.detection_mode == Experiment.RoiInfo.DetectionMode.Partial:
            self.ui.roi_detection_mode.setCurrentIndex(0)
        elif self.detection_mode == Experiment.RoiInfo.DetectionMode.CutTo:
            self.ui.roi_detection_mode.setCurrentIndex(1)
        elif self.detection_mode == Experiment.RoiInfo.DetectionMode.Largest:
            self.ui.roi_detection_mode.setCurrentIndex(2)

        self.ui.roi_detection_mode.blockSignals(False)

    def image_to_point_coordinates(self, point):
        return self.main_window.experiment.image_to_point_coordinates(point, self.ui.reference_image1.crop_rect, self.roi_grid1.scaling_factor)
    
    def point_to_image_coordinates(self, point):
        return self.main_window.experiment.point_to_image_coordinates(point, self.ui.reference_image1.crop_rect, self.roi_grid1.scaling_factor)
    
    def image_to_rect_coordinates(self, rect):
        return self.main_window.experiment.image_to_rect_coordinates(rect, self.ui.reference_image1.crop_rect, self.roi_grid1.scaling_factor)

    def rect_to_image_coordinates(self, rect):
        return self.main_window.experiment.rect_to_image_coordinates(rect, self.ui.reference_image1.crop_rect, self.roi_grid1.scaling_factor)

    def on_placement_mode_change(self):
        if self.placement_mode == Experiment.RoiInfo.PlacementMode.Matrix:  # Switching from Matrix to Manual?
            self.update_controls()
            
            self.manual_roi_items = self.current_matrix_items

            self.refresh_info_label()
            self.refresh_roi_grid()
        elif QMessageBox.question(self, "Confirm mode change", "Switching placement mode will clear existing items. Continue?") == QMessageBox.Yes:
            self.update_controls()

            if self.placement_mode == Experiment.RoiInfo.PlacementMode.Matrix:
                self.manual_roi_items = []
                if self.shape == Experiment.RoiInfo.Shape.Polygon:  # Polygon isn't allowed in Matrix mode
                    self.shape = Experiment.RoiInfo.Shape.Circle
                    
                    self.refresh_shape()
                    self.update_controls()

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
        elif self.shape == Experiment.RoiInfo.Shape.Rectangle:
            self.update_item_type(self.focused_roi_item, "Rectangle")
        elif self.shape == Experiment.RoiInfo.Shape.Ellipse:
            self.update_item_type(self.focused_roi_item, "Ellipse")
        elif self.shape == Experiment.RoiInfo.Shape.Polygon:
            self.remove_item(self.focused_roi_item)
            self.focused_roi_item = None

            self.polygon = QPolygon()
            self.polygon_closed = True

        if self.shape == Experiment.RoiInfo.Shape.Circle:
            self.focused_roi_item["width"] = self.focused_roi_item["height"]  # MAke sure width equals height for a circle

        self.ui.width_spinbox.setValue(self.focused_roi_item["width"])
        self.ui.height_spinbox.setValue(self.focused_roi_item["height"])
        self.ui.radius_spinbox.setValue(self.focused_roi_item["width"] / 2)

        self.refresh_info_label()
        self.refresh_roi_grid()

    def on_detection_mode_change(self):
        self.update_controls()

    def update_controls(self):
        if self.ui.roi_placement_mode.currentIndex() == 0:
            self.placement_mode = Experiment.RoiInfo.PlacementMode.Matrix
 
            self.ui.columns_spinbox.show()
            self.ui.rows_spinbox.show()
            self.ui.columns_label.show()
            self.ui.rows_label.show()
        else:
            self.placement_mode = Experiment.RoiInfo.PlacementMode.Manual
 
            self.ui.columns_spinbox.hide()
            self.ui.rows_spinbox.hide()
            self.ui.columns_label.hide()
            self.ui.rows_label.hide()

        self.ui.roi_shape.model().item(3).setEnabled(self.ui.roi_placement_mode.currentIndex() != 0)  # Disable Polygon choice in Matrix mode

        if self.ui.roi_shape.currentIndex() == 0:
            self.shape = Experiment.RoiInfo.Shape.Circle

            self.ui.width_spinbox.hide()
            self.ui.height_spinbox.hide()
            self.ui.width_label.hide()
            self.ui.height_label.hide()

            self.ui.radius_label.show()
            self.ui.radius_spinbox.show()
        elif self.ui.roi_shape.currentIndex() == 1:
            self.shape = Experiment.RoiInfo.Shape.Rectangle

            self.ui.width_spinbox.show()
            self.ui.height_spinbox.show()
            self.ui.width_label.show()
            self.ui.height_label.show()

            self.ui.radius_label.hide()
            self.ui.radius_spinbox.hide()
        elif self.ui.roi_shape.currentIndex() == 2:
            self.shape = Experiment.RoiInfo.Shape.Ellipse

            self.ui.width_spinbox.show()
            self.ui.height_spinbox.show()
            self.ui.width_label.show()
            self.ui.height_label.show()

            self.ui.radius_label.hide()
            self.ui.radius_spinbox.hide()
        elif self.ui.roi_shape.currentIndex() == 3:
            self.shape = Experiment.RoiInfo.Shape.Polygon

            self.ui.width_spinbox.hide()
            self.ui.height_spinbox.hide()
            self.ui.width_label.hide()
            self.ui.height_label.hide()

            self.ui.radius_label.hide()
            self.ui.radius_spinbox.hide()

        if self.ui.roi_detection_mode.currentIndex() == 0:
            self.detection_mode = Experiment.RoiInfo.DetectionMode.Partial
        elif self.ui.roi_detection_mode.currentIndex() == 1:
            self.detection_mode = Experiment.RoiInfo.DetectionMode.CutTo
        elif self.ui.roi_detection_mode.currentIndex() == 2:
            self.detection_mode = Experiment.RoiInfo.DetectionMode.Largest

        self.refresh_roi_grid()

    def on_pressed(self, point):
        # tprint("onPressed", self.focusedRoiItem, point)
        if self.placement_mode == Experiment.RoiInfo.PlacementMode.Manual:
            item = self.item_at(self.point_to_image_coordinates(point))
            if item is not None:
                self.focused_roi_item = item

                # item = ("Circle", point.x(), point.y(), radius * 2, radius * 2,)
                tprint("Load values for selected item", item)

                self.ui.radius_spinbox.setValue(item["width"] / 2)
                self.ui.width_spinbox.setValue(item["width"])
                self.ui.height_spinbox.setValue(item["height"])

                if item["type"] == "Circle":
                    self.shape = Experiment.RoiInfo.Shape.Circle
                elif item["type"] == "Rectangle":
                    self.shape = Experiment.RoiInfo.Shape.Rectangle
                elif item["type"] == "Ellipse":
                    self.shape = Experiment.RoiInfo.Shape.Ellipse
                elif item["type"] == "Polygon":
                    self.shape = Experiment.RoiInfo.Shape.Polygon

                self.refresh_shape()
                self.update_controls()

                self.refresh_roi_grid()
      
        self.last_move_point = self.point_to_image_coordinates(point)

    def on_clicked(self, point):
        # tprint("onClicked", self.focusedRoiItem, point)
        if self.skip_clicked:
            self.skip_clicked = False
        elif self.placement_mode == Experiment.RoiInfo.PlacementMode.Manual:
            item = self.item_at(self.point_to_image_coordinates(point))
            if item is None:
                x = self.point_to_image_coordinates(point).x()
                y = self.point_to_image_coordinates(point).y()
                radius = self.ui.radius_spinbox.value()
                width = self.ui.width_spinbox.value()
                height = self.ui.height_spinbox.value()

                # Add new item
                if self.shape == Experiment.RoiInfo.Shape.Circle:
                    d = {}
                    d["type"] = "Circle"
                    d["x"] = int(x)
                    d["y"] = int(y)
                    d["width"] = int(radius * 2)
                    d["height"] = int(radius * 2)

                    self.add_item(d)
                elif self.shape == Experiment.RoiInfo.Shape.Rectangle:
                    d = {}
                    d["type"] = "Rectangle"
                    d["x"] = int(x)
                    d["y"] = int(y)
                    d["width"] = int(width)
                    d["height"] = int(height)

                    self.add_item(d)
                elif self.shape == Experiment.RoiInfo.Shape.Ellipse:
                    d = {}
                    d["type"] = "Ellipse"
                    d["x"] = int(x)
                    d["y"] = int(y)
                    d["width"] = int(width)
                    d["height"] = int(height)

                    self.add_item(d)
                elif self.shape == Experiment.RoiInfo.Shape.Polygon:
                    if self.polygon_closed:
                        self.polygon = QPolygon()
                        self.polygon_closed = False

                        d = {}
                        d["type"] = "Polygon"
                        d["x"] = 0  # These will be set later when the boundaries of the polygon are established
                        d["y"] = 0
                        d["width"] = 0
                        d["height"] = 0
                        d["points"] = []

                        self.add_item(d)

                    self.focused_roi_item["points"].append([x, y])

                    self.polygon.append(QPoint(x, y))

            self.refresh_roi_grid()

    def on_right_clicked(self, point):
        if self.placement_mode == Experiment.RoiInfo.PlacementMode.Manual:
            item = self.item_at(self.point_to_image_coordinates(point))
            if item is not None:
                self.remove_item(item)

                self.polygon_closed = True
                self.polygon = QPolygon()

                self.refresh_roi_grid()

    def on_moved(self, point):
        if self.placement_mode == Experiment.RoiInfo.PlacementMode.Manual and self.focused_roi_item is not None:
            # tprint("onMoved", self.focusedRoiItem, point)

            self.update_item_position(self.focused_roi_item, self.point_to_image_coordinates(point))

            self.refresh_roi_grid()

    def on_double_clicked(self, point):
        if not self.polygon.empty():
            self.polygon.removeLast()  # Remove last point (added on the first click of the double click)
            self.polygon.append(self.polygon.at(0))  # Add the first point to close the polygon

            point_list = self.polygon.toList()

            self.polygon_closed = True

            l = []
            for point in point_list:
                l.append([ point.x(), point.y() ])

            self.focused_roi_item["type"] = "Polygon"
            self.focused_roi_item["x"] = self.polygon.boundingRect().center().x()
            self.focused_roi_item["y"] = self.polygon.boundingRect().center().y()
            self.focused_roi_item["width"] = self.polygon.boundingRect().width()
            self.focused_roi_item["height"] = self.polygon.boundingRect().height()
            
            self.focused_roi_item["points"] = l

            # self.add_item(d)

            # tprint("Polygon list", d)

        # tprint("Focused Item", self.focused_roi_item)

        self.refresh_roi_grid()

        self.skip_clicked = True

    def on_rubberband_changed(self, rect):
        if self.placement_mode == Experiment.RoiInfo.PlacementMode.Matrix:
            self.rubberband_rect = self.rect_to_image_coordinates(rect)
                                         
            self.refresh_roi_grid()

    def on_crop_rect_changed(self, rect):
        if self.ui.reference_image1 is not None:
            self.ui.reference_image1.crop_edit_rect = rect
            self.ui.reference_image1.crop_mode = True
            self.ui.reference_image1.update()
        if self.ui.reference_image2 is not None:
            self.ui.reference_image2.crop_edit_rect = rect
            self.ui.reference_image2.crop_mode = True
            self.ui.reference_image2.update()

    def on_crop_state_changed(self):
        # Copy all crop settings from image 2 to image 1
        self.ui.reference_image2.crop_mode = self.ui.reference_image1.crop_mode
        self.ui.reference_image2.crop_origin = self.ui.reference_image1.crop_origin
        self.ui.reference_image2.crop_edit_rect = self.ui.reference_image1.crop_edit_rect
        self.ui.reference_image2.crop_rect = self.ui.reference_image1.crop_rect
        self.ui.reference_image2.crop_pixmap = self.ui.reference_image1.crop_pixmap

        self.ui.reference_image2.set_crop_rect(self.ui.reference_image2.crop_rect)
        self.ui.reference_image2.refresh_image_size()

        self.ui.reference_image2.update()

    def on_crop_accepted(self):
        self.clear_rois()
        self.refresh_image_sizes()

    def on_crop_reset(self):
        self.clear_rois()
        self.refresh_image_sizes()

    def contains_item(self, existing_item, new_item):
        item_type = existing_item["type"]
        item_type2 = new_item["type"]

        if item_type == "Polygon" and item_type2 == "Polygon":
            if existing_item["points"] == new_item["points"]:
                return True
            
        center_x = existing_item["x"]
        center_y = existing_item["y"]
        width = existing_item["width"]
        height = existing_item["height"]

        center_x2 = new_item["x"]
        center_y2 = new_item["y"]
        # width2 = new_item["width"]
        # height2 = new_item["height"]

        if center_x2 > center_x - width / 2 and center_x2 < center_x + width / 2 and center_y2 > center_y - height / 2 and center_y2 < center_y + height / 2:
            return True

        return False

    def contains_point(self, item, point):
        item_type = item["type"]
        center_x = item["x"]
        center_y = item["y"]
        width = item["width"]
        height = item["height"]

        if item_type == "Polygon":
            if "points" in item:
                points = item["points"]
                if len(points) > 1:
                    # Handle polygon
                    polygon = QPolygon()
                    for p in points:
                        polygon.append(QPoint(p[0], p[1]))

                    if polygon.containsPoint(point, QtCore.Qt.WindingFill):
                        return True
                else:
                    # Handle single point with added margin
                    p = QPoint(points[0][0], points[0][1])
                    if QRect(p, QSize(10, 10)).adjusted(-5, -5, -5, -5).contains(point):
                        return True
        elif point.x() > center_x - width / 2 and point.x() < center_x + width / 2 and point.y() > center_y - height / 2 and point.y() < center_y + height / 2:
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

    def update_item_type(self, item, item_type):
        if item:
            item["type"] = item_type

    def update_item_position(self, item, point):
        if item:
            if item["type"] == "Polygon":
                diff_x = (point - self.last_move_point).x()
                diff_y = (point - self.last_move_point).y()

                self.last_move_point = point
                for i in range(0, len(item["points"])):
                    item["points"][i][0] = item["points"][i][0] + diff_x
                    item["points"][i][1] = item["points"][i][1] + diff_y
            else:
                item["x"] = point.x()
                item["y"] = point.y()

    def update_item_radius(self, item, radius):
        if item and item["type"] == "Circle":
            item["width"] = radius * 2
            item["height"] = radius * 2

    def update_item_width(self, item, width):
        if item:
            item["width"] = width

    def update_item_height(self, item, height):
        if item:
            item["height"] = height

    def refresh_reference_image1(self):
        if self.ui.reference_image1 is not None:
            width = self.ui.reference_image1.width()
            height = self.ui.reference_image1.height()

            if self.ui.reference_image1.original_image:
                self.ui.reference_image1.refresh_image_size()
                
                # Scale pixmap to follow available space
                # self.ui.reference_image1.setPixmap(self.ui.reference_image1.original_image.scaled(width, height, QtCore.Qt.KeepAspectRatio))

                if not self.ui.reference_image1.crop_rect.isEmpty():
                    self.roi_grid1.scaling_factor = self.ui.reference_image1.pixmap().width() / self.ui.reference_image1.crop_rect.width()
                else:
                    self.roi_grid1.scaling_factor = self.ui.reference_image1.pixmap().width() / self.ui.reference_image1.original_image.width()
            else:
                self.roi_grid1.scaling_factor = 1.0

            self.roi_grid1.visible_image_size = self.ui.reference_image1.pixmap().size()

            self.roi_grid1.show_rois = not self.ui.reference_image1.original_image.isNull()
            self.roi_grid1.update()
            
    def refresh_reference_image2(self):
        if self.ui.reference_image2 is not None:
            width = self.ui.reference_image2.width()
            height = self.ui.reference_image2.height()

            if self.ui.reference_image2.original_image:
                self.ui.reference_image2.refresh_image_size()
                
                # Scale pixmap to follow available space
                # self.ui.reference_image2.setPixmap(self.ui.reference_image2.original_image.scaled(width, height, QtCore.Qt.KeepAspectRatio))

                if not self.ui.reference_image2.crop_rect.isEmpty():
                    self.roi_grid2.scaling_factor = self.ui.reference_image2.pixmap().width() / self.ui.reference_image2.crop_rect.width()
                else:
                    self.roi_grid2.scaling_factor = self.ui.reference_image2.pixmap().width() / self.ui.reference_image2.original_image.width()
            else:
                self.roi_grid2.scaling_factor = self.roi_grid1.scaling_factor 

            self.roi_grid2.visible_image_size = self.ui.reference_image2.pixmap().size()

            self.roi_grid2.show_rois = not self.ui.reference_image2.original_image.isNull()
            self.roi_grid2.update()

    def refresh_image_sizes(self):
        # self.ui.reference_image1.set_crop_rect(self.main_window.experiment.crop_rect)
        # self.ui.reference_image2.set_crop_rect(self.main_window.experiment.crop_rect)

        self.refresh_reference_image1()
        self.refresh_reference_image2()

    def resizeEvent(self, event):  # Qt override
        self.refresh_image_sizes()
            
