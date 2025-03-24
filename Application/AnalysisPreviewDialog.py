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

import sys
import os
import json
import tempfile
import importlib

from multiprocessing import Queue

from PySide6.QtWidgets import QDialog, QCheckBox, QSlider, QLabel, QVBoxLayout, QComboBox, QFrame, QPushButton, QMessageBox
from PySide6.QtGui import QPixmap, QGuiApplication, QCursor
from PySide6.QtCore import QTimer, QCoreApplication
from PySide6 import QtCore

import Helper
from Helper import tprint

from ImageRoiDialog import RoiGrid

import CameraApp_rc

from SelectImageDialog import SelectImageDialog

from ui_AnalysisPreviewDialog import Ui_AnalysisPreviewDialog

class AnalysisPreviewDialog(QDialog):
    def __init__(self, main_window):
        self.main_window = main_window

        self.option_checkboxes = []
        self.option_sliders = []
        self.option_dropdowns = []

        super(AnalysisPreviewDialog, self).__init__()

        # Set window flags to customize window behavior
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMaximizeButtonHint)  # Get rid of What's this icon in title bar

        self.load_ui()

        self.ui.reference_image1.image_file_name_changed.connect(self.refresh_image_sizes)
        self.ui.reference_image2.image_file_name_changed.connect(self.refresh_image_sizes)

        # Initialize variables to hold original preview images
        self.original_preview_image1 = None
        self.original_preview_image2 = None

        self.roi_grid1 = None
        self.roi_grid2 = None

        # Connect image buttons to slot for selecting reference images
        self.ui.reference_image1.select_image_button.clicked.connect(self.select_reference_image1)
        self.ui.reference_image2.select_image_button.clicked.connect(self.select_reference_image2)

        # Connect magnify state between reference and preview images
        self.ui.reference_image1.magnify_state_changed.connect(self.on_magnify_state_changed1)
        self.ui.reference_image2.magnify_state_changed.connect(self.on_magnify_state_changed2)

        self.ui.preview_button.clicked.connect(self.run_preview_script)

        self.ui.show_rois_checkbox.toggled.connect(self.show_rois)

        self.script_description = ''

        # For some reason, geometry won't work unless we move the update outside the constructor
        QTimer.singleShot(300, lambda: self.load_reference_images())

        if self.main_window.test_mode:
            QTimer.singleShot(self.main_window.test_dialog_timeout, lambda:self.accept())

    def load_ui(self):
        self.ui = Ui_AnalysisPreviewDialog()
        self.ui.setupUi(self)

    def refresh_preview_image1(self):
        if self.original_preview_image1 is not None:
            width = self.ui.preview_image1.width()
            height = self.ui.preview_image1.height()

            if self.original_preview_image1:
                # Scale pixmap to follow available space
                self.ui.preview_image1.setPixmap(self.original_preview_image1.scaled(width, height, QtCore.Qt.KeepAspectRatio))

            scaling_factor = self.ui.preview_image1.pixmap().width() / self.original_preview_image1.width()

            if not self.roi_grid1:
                items = self.main_window.experiment.roi_info.roi_items(1.0)
                self.roi_grid1 = RoiGrid(self.ui.preview_image1, self, items)
                self.roi_grid1.setVisible(self.ui.show_rois_checkbox.isChecked())

            self.roi_grid1.scaling_factor = scaling_factor
            self.roi_grid1.setFixedSize(self.ui.preview_image1.pixmap().size())
            
    def refresh_preview_image2(self):
        if self.original_preview_image2 is not None:
            width = self.ui.preview_image2.width()
            height = self.ui.preview_image2.height()

            if self.original_preview_image2:
                # Scale pixmap to follow available space
                self.ui.preview_image2.setPixmap(self.original_preview_image2.scaled(width, height, QtCore.Qt.KeepAspectRatio))

            scaling_factor = self.ui.preview_image2.pixmap().width() / self.original_preview_image2.width()

            if not self.roi_grid2:
                items = self.main_window.experiment.roi_info.roi_items(1.0)
                self.roi_grid2 = RoiGrid(self.ui.preview_image2, self, items)
                self.roi_grid2.setVisible(self.ui.show_rois_checkbox.isChecked())

            self.roi_grid2.scaling_factor = scaling_factor
            self.roi_grid2.setFixedSize(self.ui.preview_image2.pixmap().size())

    def refresh_image_sizes(self):
        if self.ui.reference_image1 is not None:
            self.ui.reference_image1.refresh_image_size()
        if self.ui.reference_image2 is not None:
            self.ui.reference_image2.refresh_image_size()

        self.ui.reference_image1.set_crop_rect(self.main_window.experiment.crop_rect)
        self.ui.reference_image2.set_crop_rect(self.main_window.experiment.crop_rect)

        self.refresh_preview_image1()
        self.refresh_preview_image2()

    def resizeEvent(self, event):  # Qt override
        self.refresh_image_sizes()

    def show_rois(self, active):
        if self.roi_grid1:
            self.roi_grid1.setVisible(active)
        if self.roi_grid2:
            self.roi_grid2.setVisible(active)

    def select_reference_image1(self):
        self.main_window.select_image_dialog(self.main_window, self, self.ui.reference_image1)
        
    def select_reference_image2(self):
        if self.ui.reference_image1.image_file_name != "":
            self.main_window.select_image_dialog(self.main_window, self, self.ui.reference_image2)
        else:
            QMessageBox.warning(self, "Image selection", "You must select the left image first")

    def load_reference_images(self):
        if self.main_window.experiment.script_reference_image1 is not None:
            self.ui.reference_image1.set_image_file_name(self.main_window.experiment.script_reference_image1, self.main_window.experiment.image_options_to_dict())
            tprint("Script: Load left preview image:", self.main_window.experiment.script_reference_image1)

        if self.main_window.experiment.script_reference_image2 is not None:
            self.ui.reference_image2.set_image_file_name(self.main_window.experiment.script_reference_image2, self.main_window.experiment.image_options_to_dict())
            tprint("Script: Load right preview image:", self.main_window.experiment.script_reference_image2)

        # self.run_preview_script()

        if self.ui.reference_image1.image_file_name != "":
            self.ui.preview_image1.setText("Press 'Create Preview' to perform an analysis<br>on the sample images")
        if self.ui.reference_image2.image_file_name != "":
            self.ui.preview_image2.setText("Press 'Create Preview' to perform an analysis<br>on the sample images")

        self.ui.reference_image1.set_crop_rect(self.main_window.experiment.crop_rect)
        self.ui.reference_image2.set_crop_rect(self.main_window.experiment.crop_rect)

        self.refresh_image_sizes()

    def run_preview_script(self):
        if self.ui.reference_image1.image_file_name != "":
            # Set the cursor to a wait cursor during script execution
            QGuiApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))

            if self.ui.reference_image1.image_file_name != "":
                self.ui.preview_image1.setText("Processing preview...")
            if self.ui.reference_image2.image_file_name != "":
                self.ui.preview_image2.setText("Processing preview...")

            QCoreApplication.processEvents()  # Make sure GUI is updated before executing the preview script

            # Set up temporary file for preview
            with tempfile.TemporaryDirectory() as temp_path:
                # Initialize settings dictionary for the script
                settings = {}
                settings["experimentSettings"] = self.main_window.experiment.to_dict()

                settings["scriptName"] = self.main_window.experiment.selected_script
                settings["outputFolder"] = { "images": temp_path, "visuals": "", "data": "" , "appData": ""}    

                # Populate script options from UI elements
                # Note: If you change ui elements here, you are likely to have to update openImageMaskDialog when dialog is closed
                for name, checkbox in self.option_checkboxes:
                    settings['experimentSettings']['analysis']['scriptOptions']['general'][name] = checkbox.isChecked()

                for name, slider, min, step_size in self.option_sliders:
                    settings['experimentSettings']['analysis']['scriptOptions']['general'][name] = int(slider.value())

                # for name, wavelength in self.option_wavelengths:
                #     settings['experimentSettings']['analysis']['scriptOptions']['general'][name] = wavelength.currentText()

                for name, dropdown in self.option_dropdowns:
                    settings['experimentSettings']['analysis']['scriptOptions']['general'][name] = dropdown.currentData()

                analytics_script_name = self.main_window.experiment.selected_script
                sys.path.append(os.path.dirname(self.main_window.script_paths[analytics_script_name]))
                analytics_script = importlib.import_module(analytics_script_name.replace(".py", ""))

                # Find selected mask
                mask_path, mask_file = self.main_window.mask_info()

                if mask_file != self.main_window.experiment.selected_script:
                    mask_file_name = os.path.join(mask_path, mask_file)
                else:
                    mask_file_name = ''

                # analysis_script_queue = Queue()

                # Process preview image 1 if available
                if self.ui.reference_image1.image_file_name != "":
                    settings["inputImage"] = self.ui.reference_image1.image_file_name

                    tprint("Script preview", settings)

                    try:
                        temp_file_name = analytics_script.execute(analytics_script_name, settings, mask_file_name, True)
                        
                        self.original_preview_image1 = QPixmap(temp_file_name)
                        self.refresh_preview_image1()

                        tprint("Reading preview from", temp_file_name)
                    except BaseException as e:
                        tprint("Preview 1 failed: Unknown exception", e)
 
                        ready, reason = self.main_window.ready_to_run()
                        if not ready and self.ui.reference_image1.image_file_name != "":
                            self.ui.preview_image1.setText(reason)

                # Process preview image 2 if available
                if self.ui.reference_image2.image_file_name != "":
                    settings["inputImage"] = self.ui.reference_image2.image_file_name

                    try:
                        temp_file_name = analytics_script.execute(analytics_script_name, settings, mask_file_name, True)

                        self.original_preview_image2 = QPixmap(temp_file_name)
                        self.refresh_preview_image2()
                    except BaseException as e:
                        tprint("Preview 2 failed: Unknown exception", e)

                        ready, reason = self.main_window.ready_to_run()
                        if not ready and self.ui.reference_image2.image_file_name != "":
                            self.ui.preview_image2.setText(reason)

            # Restore the cursor to its original state
            QGuiApplication.restoreOverrideCursor()

    def on_magnify_state_changed1(self, mode, pos, zoom_factor):
        self.ui.preview_image1.set_magnifier_mode(mode, pos, zoom_factor)
        
    def on_magnify_state_changed2(self, mode, pos, zoom_factor):
        self.ui.preview_image2.set_magnifier_mode(mode, pos, zoom_factor)
