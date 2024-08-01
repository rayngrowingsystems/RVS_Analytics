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
import glob

from PySide6.QtWidgets import QDialog, QFileDialog, QInputDialog, QMessageBox
from PySide6.QtGui import QGuiApplication, QCursor
from PySide6 import QtCore

import CameraApp_rc

from ui_SelectImageDialog import Ui_SelectImageDialog


class SelectImageDialog(QDialog):
    def __init__(self, parent, corresponding_label):
        self.main_window = parent.main_window
        self.dialog = parent

        self.corresponding_label = corresponding_label

        super(SelectImageDialog, self).__init__()
        self.load_ui()

        self.ui.existing_image_button.clicked.connect(self.pick_image)
        self.ui.imageFrom_camera_button.clicked.connect(self.fetch_image)

    def load_ui(self):
        self.ui = Ui_SelectImageDialog()
        self.ui.setupUi(self)

    def pick_image(self):
        if self.main_window.experiment.ImageSource is self.main_window.experiment.ImageSource.Image:
            start_folder = self.main_window.experiment.image_file_path
        elif self.main_window.experiment.ImageSource is self.main_window.experiment.ImageSource.Folder:
            start_folder = self.main_window.experiment.folder_file_path
        else:
            start_folder = self.main_window.experiment.camera_file_path

        file_name, filter = QFileDialog.getOpenFileName(self, "Open image file",
                 start_folder, "Image Files (*.hdr)")

        if file_name != "":
            QGuiApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))

            if self.main_window.experiment.all_preview_images_empty():  # No images defined -> auto select
                # Find last image in folder
                dir_path = os.path.join(os.path.dirname(file_name), '*.hdr')
                hdr_list = sorted(glob.glob(dir_path))

                self.main_window.experiment.mask_reference_image1 = file_name
                self.main_window.experiment.mask_reference_image2 = hdr_list[-1]

                self.main_window.experiment.roi_reference_image1 = file_name
                self.main_window.experiment.roi_reference_image2 = hdr_list[-1]

                self.dialog.load_reference_images()  # Reload images in this dialog
            else:
                self.corresponding_label.set_image_file_name(file_name, self.main_window.experiment.lens_angle, self.main_window.experiment.normalize, self.main_window.experiment.light_correction)

            print("Set image preview:", file_name)

            QGuiApplication.restoreOverrideCursor()

        self.accept()

    def fetch_image(self):
        if self.main_window.camera:
            files = [s for s in self.main_window.camera.get_folder("scheduler") if s.endswith('.hdr')]
            files.sort()
            files.insert(0, "Take new image")

            file, ok = QInputDialog.getItem(self, "Select image", "Image", files, 0, False)

            if ok:
                if self.main_window.experiment.ImageSource is self.main_window.experiment.ImageSource.Image:
                    target_folder = self.main_window.experiment.image_file_path
                elif self.main_window.experiment.ImageSource is self.main_window.experiment.ImageSource.Folder:
                    target_folder = self.main_window.experiment.folder_file_path
                else:
                    target_folder = self.main_window.experiment.camera_file_path

                QGuiApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))

                if file == "Take new image":
                    print("Camera: Taking image...")

                    QMessageBox.information(None, "Take image", "This takes up to one minute, be patient!")

                    image_files = self.main_window.camera.take_image()

                    # Fetch resulting files
                    hdr_file = ""
                    for image_file in image_files:
                        print("Camera: Fetching file:", image_file)

                        image_data = self.main_window.camera.get_file("api_takeimage", image_file)

                        try:
                            print("Camera: Saving image file locally:", os.path.join(target_folder, image_file))

                            f = open(os.path.join(target_folder, image_file), "wb")  # save to file
                            f.write(image_data)
                            f.close()

                            if image_file.endswith(".hdr"):
                                hdr_file = image_file

                        except IOError as e:
                            print("Fetch: IOError", e)

                    if hdr_file != "":
                        self.corresponding_label.set_image_file_name(os.path.join(target_folder, hdr_file), self.main_window.experiment.lens_angle, self.main_window.experiment.normalize, self.main_window.experiment.light_correction)
                        print("Set preview image:", os.path.join(target_folder, hdr_file))

                else:
                    print("Fetch image hdr and image cube", file)

                    image_hdr_file = file
                    image_hdr = self.main_window.camera.get_file("scheduler", image_hdr_file)

                    image_cube_file = os.path.splitext(file)[0]  # Use base name
                    image_cube = self.main_window.camera.get_file("scheduler", image_cube_file)

                    if image_hdr is not None and image_cube is not None:
                        try:
                            f = open(os.path.join(target_folder, image_hdr_file), "wb")  # save hdr to file
                            f.write(image_hdr)
                            f.close()

                            f = open(os.path.join(target_folder, image_cube_file), "wb")  # save image data to file
                            f.write(image_cube)
                            f.close()

                            self.corresponding_label.set_image_file_name(os.path.join(target_folder, image_hdr_file), self.main_window.experiment.lens_angle, self.main_window.experiment.normalize, self.main_window.experiment.light_correction)
                            print("Set preview image:", os.path.join(target_folder, image_hdr_file))

                        except IOError as e:
                            print("Fetch: IOError", e)
                        except BaseException as e:
                            print("Fetch: Unknown exception", e)

                QGuiApplication.restoreOverrideCursor()
        else:
            print("Camera not set", self.main_window.camera)

        self.accept()
