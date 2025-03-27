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

from PySide6.QtWidgets import QDialog, QMessageBox

from Helper import tprint
from ui_DeleteImagesDialog import Ui_DeleteImagesDialog


class DeleteImagesDialog(QDialog):
    def __init__(self, parent):
        self.main_window = parent

        super(DeleteImagesDialog, self).__init__()
        self.load_ui()

        if self.main_window.camera:
            self.ui.done_button.clicked.connect(self.delete_images)
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

            self.ui.header_text.setText("Delete multiple images from <b>" +
                                self.main_window.cameras[self.main_window.experiment.camera_cid]["name"] + "</b>")

    def load_ui(self):
        self.ui = Ui_DeleteImagesDialog()
        self.ui.setupUi(self)

    def refresh_selected_images_label(self):
        count = abs(self.ui.stop_combo_box.currentIndex() - self.ui.start_combo_box.currentIndex()) + 1

        self.ui.selected_images_label.setText("Selected images: " + str(count))

    def delete_images(self):
        images = []
        for i in range(self.ui.start_combo_box.currentIndex(), self.ui.stop_combo_box.currentIndex() + 1):
            if i >= 0 and i < len(self.files):
                images.append(self.files[i])
                images.append(os.path.splitext(self.files[i])[0])  # Get corresponding imagecube file
                images.append(os.path.splitext(self.files[i])[0] + ".PNG")  # Get corresponding PNG file

        if len(images) > 0:
            tprint("Delete images", images)

            self.main_window.add_status_text.emit("Deleting images from camera...")

            self.main_window.ui.image_preview_progressbar.setValue(0)
            self.main_window.ui.image_preview_progressbar.setRange(0, len(images) / 3)

            # TODO self.main_window.camera.get_files(images, self.ui.target_path_label.text(), False,
            # self.ui.delete_from_camera_checkbox.isChecked())

            for file_name in images:
                self.main_window.camera.delete_file("scheduler", file_name)

            self.accept()
        else:
            QMessageBox.warning(self, "No images", "The camera doesn't have any images to delete")
