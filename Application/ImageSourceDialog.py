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
import os

from PySide6.QtWidgets import QDialog, QFileDialog
from PySide6.QtCore import QTimer

from PySide6 import QtCore

import CameraApp_rc

from ui_ImageSourceDialog import Ui_ImageSourceDialog

from Helper import tprint
import Config
class ImageSourceDialog(QDialog):
    def __init__(self, main_window):
        self.main_window = main_window

        # self.radioButtonGroup = QButtonGroup()

        super(ImageSourceDialog, self).__init__()

        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint)  # Get rid of What's this icon in title bar

        self.load_ui()

        self.ui.image_browse_button.clicked.connect(self.set_image_file_path)
        self.ui.folder_browse_button.clicked.connect(self.set_folder_file_path)
        self.ui.camera_browse_button.clicked.connect(self.set_camera_file_path)

        self.ui.image_source_radiobutton.clicked.connect(self.set_image_mode)
        self.ui.folder_source_radiobutton.clicked.connect(self.set_folder_mode)
        self.ui.camera_source_radiobutton.clicked.connect(self.set_camera_mode)

        self.ui.camera_refresh_button.clicked.connect(self.refresh_cameras)

        self.ui.camera_identify_button.clicked.connect(self.identify_camera)
        self.ui.camera_configure_button.clicked.connect(self.configure_camera)

        self.ui.output_browse_button.clicked.connect(self.set_output_file_path)

        self.ui.image_file_path.setText(self.main_window.experiment.image_file_path)
        self.ui.folder_file_path.setText(self.main_window.experiment.folder_file_path)
        self.ui.camera_file_path.setText(self.main_window.experiment.camera_file_path)

        self.ui.output_file_path.setText(self.main_window.experiment.output_file_path)

        self.refresh_cameras()

        # Find current index
        index = 0
        for cid, camera_json in self.main_window.cameras.items():
            if cid == self.main_window.experiment.camera_cid:
                self.ui.camera_selection_combobox.setCurrentIndex(index)
                break

            index = index + 1

        self.ui.camera_selection_combobox.currentIndexChanged.connect(self.camera_selection_changed)

        if self.main_window.experiment.ImageSource is self.main_window.experiment.ImageSource.Image:
            self.ui.image_source_radiobutton.setChecked(True)
        elif self.main_window.experiment.ImageSource is self.main_window.experiment.ImageSource.Folder:
            self.ui.folder_source_radiobutton.setChecked(True)
        else:
            self.ui.camera_source_radiobutton.setChecked(True)

        if Config.test_mode:
            QTimer.singleShot(Config.test_timeout, lambda: self.accept())

    def load_ui(self):
        self.ui = Ui_ImageSourceDialog()
        self.ui.setupUi(self)

    def set_image_mode(self):
        self.main_window.set_image_source(self.main_window.experiment.ImageSource.Image)

    def set_folder_mode(self):
        self.main_window.set_image_source(self.main_window.experiment.ImageSource.Folder)

    def set_camera_mode(self):
        self.main_window.set_image_source(self.main_window.experiment.ImageSource.Camera)

    def set_image_file_path(self):
        file_info = QFileDialog.getOpenFileName(self, "Select an image", self.main_window.experiment.current_folder(), "Image Files (*.hdr)")

        # fileInfo is a tuple

        if file_info[0] != "":
            file_name = os.path.normpath(file_info[0])

            self.main_window.set_image_file_path(file_name)

            self.ui.image_file_path.setText(file_name)

            # Set reference images in mask/roi dialogs
            self.main_window.experiment.mask_reference_image1 = file_name
            self.main_window.experiment.mask_reference_image2 = ""

            self.main_window.experiment.roi_reference_image1 = file_name
            self.main_window.experiment.roi_reference_image2 = ""

            self.main_window.experiment.script_reference_image1 = file_name
            self.main_window.experiment.script_reference_image2 = ""

    def set_folder_file_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select a folder", self.main_window.experiment.current_folder())

        if folder != "":
            folder = os.path.normpath(folder)

            self.main_window.set_folder_file_path(folder)

            self.ui.folder_file_path.setText(folder)

    def set_camera_file_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select a folder", self.main_window.experiment.current_folder())

        if folder != "":
            folder = os.path.normpath(folder)

            self.main_window.set_camera_file_path(folder)

            self.ui.camera_file_path.setText(folder)

    def set_output_file_path(self):
        tprint("SetOutput", self.main_window.experiment.output_file_path)

        folder = QFileDialog.getExistingDirectory(self, "Select a folder", self.main_window.experiment.output_file_path)

        if folder != "":
            folder = os.path.normpath(folder)

            self.main_window.set_output_file_path(folder)

            self.ui.output_file_path.setText(folder)

    def refresh_cameras(self):
        # tprint("refreshCameras")

        self.ui.camera_selection_combobox.blockSignals(True)

        # Remove existing items
        while self.ui.camera_selection_combobox.count() > 0:
            self.ui.camera_selection_combobox.removeItem(0)

        # Add back the current list
        for camera in self.main_window.camera_display_names():
            self.ui.camera_selection_combobox.addItem(camera)

        self.ui.camera_selection_combobox.blockSignals(False)

    def identify_camera(self):
        tprint("identifyCamera")
        if self.main_window.camera:
            self.main_window.camera.identify()

    def configure_camera(self):
        tprint("configureCamera")

        self.close()

        self.main_window.configure_camera(self.ui.camera_selection_combobox.currentIndex())

    def camera_selection_changed(self, index):
        self.main_window.camera_selection_changed(index)
