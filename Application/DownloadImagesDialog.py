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

from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

import CameraApp_rc

from ui_DownloadImagesDialog import Ui_DownloadImagesDialog

from Helper import tprint

class DownloadImagesDialog(QDialog):
    def __init__(self, parent):
        self.main_window = parent

        super(DownloadImagesDialog, self).__init__()
        self.load_ui()

        if self.main_window.camera:
            self.ui.done_button.clicked.connect(self.fetch_images)
            self.ui.cancel_button.clicked.connect(self.reject)

            self.files = [s for s in self.main_window.camera.get_folder("scheduler") if s.endswith('.hdr')]
            self.files.sort()

            self.ui.start_combo_box.addItems(self.files)
            self.ui.start_combo_box.setCurrentIndex(0)
            self.ui.stop_combo_box.addItems(self.files)
            self.ui.stop_combo_box.setCurrentIndex(len(self.files) - 1)

            self.ui.start_combo_box.currentIndexChanged.connect(self.refresh_selected_images_label)
            self.ui.stop_combo_box.currentIndexChanged.connect(self.refresh_selected_images_label)

            self.refresh_selected_images_label()

            self.ui.browse_button.clicked.connect(self.set_target_path)
            self.ui.target_path_label.setText(self.main_window.experiment.camera_file_path)

            self.ui.header_text.setText("Download multiple images from <b>" + self.main_window.cameras[self.main_window.experiment.camera_cid]["name"] + "</b>")

    def load_ui(self):
        self.ui = Ui_DownloadImagesDialog()
        self.ui.setupUi(self)

    def refresh_selected_images_label(self):
        count = abs(self.ui.stop_combo_box.currentIndex() - self.ui.start_combo_box.currentIndex()) + 1

        self.ui.selected_images_label.setText("Selected images: " + str(count))

    def set_target_path(self):
        if self.main_window.experiment.ImageSource is self.main_window.experiment.ImageSource.Image:
            start_folder = self.main_window.experiment.image_file_path
        elif self.main_window.experiment.ImageSource is self.main_window.experiment.ImageSource.Folder:
            start_folder = self.main_window.experiment.folder_file_path
        else:
            start_folder = self.main_window.experiment.camera_file_path

        folder = QFileDialog.getExistingDirectory(self, "Select a target folder", start_folder)

        if folder != "":
            folder = os.path.normpath(folder)

            self.ui.target_path_label.setText(folder)

            tprint("Target path", folder)

    def fetch_images(self):
        if self.ui.target_path_label.text() in ["", "."]:
            QMessageBox.warning(self, "No target folder defined", "Please press the Browse button to select a target folder")
        else:
            images = []
            for i in range(self.ui.start_combo_box.currentIndex(), self.ui.stop_combo_box.currentIndex() + 1):
                if i >= 0 and i < len(self.files):
                    images.append(self.files[i])
                    images.append(os.path.splitext(self.files[i])[0])  # Get corresponding imagecube file
                    images.append(os.path.splitext(self.files[i])[0] + ".PNG")  # Get corresponding PNG file

            if len(images) / 3 > 150:
                QMessageBox.warning(self, "Too many files", "Currently, a maximum of 150 images can be transferred at once. Consider using the SD-card to transfer many images at once")
            elif len(images) > 0:
                tprint("Fetch images", images)

                self.main_window.add_status_text.emit("Downloading images from camera...")

                self.main_window.ui.image_preview_progressbar.setValue(0)
                self.main_window.ui.image_preview_progressbar.setRange(0, len(images) / 3)

                self.main_window.camera.get_files(images, self.ui.target_path_label.text(), False, self.ui.delete_from_camera_checkbox.isChecked())

                # self.mainWindow.camera.setLastReceivedFile(images[-1])

                self.accept()
            else:
                QMessageBox.warning(self, "No images", "The camera doesn't have any images to download")
