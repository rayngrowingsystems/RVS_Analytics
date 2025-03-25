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

import json
import tempfile
import os

from PySide6.QtWidgets import QDialog, QGridLayout, QCheckBox, QLabel, QPushButton, QMessageBox, QComboBox, QFrame
from PySide6.QtGui import QPixmap, QGuiApplication, QCursor
from PySide6.QtCore import QTimer
from PySide6 import QtCore

import CameraApp_rc

from ImageRoiDialog import RoiGrid
from ui_ImageMaskDialog import Ui_ImageMaskDialog

from SelectImageDialog import SelectImageDialog

from DoubleSlider import DoubleSlider

import Config
import Helper
from Helper import tprint

class ImageMaskDialog(QDialog):
    # MASK_FILE_PREFIX = "mask_"

    def __init__(self, main_window):
        # Initialize the dialog
        self.main_window = main_window

        # Lists to hold various UI elements
        self.option_checkboxes = []
        self.option_sliders = []
        self.option_wavelengths = []
        self.option_dropdowns = []
        self.option_spinboxes = []

        # Store ranges for related sliders
        self.option_ranges = []

        # Lists to store wavelength settings
        self.wavelengths = []

        self.wavelength_value = {}

        self.default_values = {}

        # Flag to track setup completion
        self.setup_completed = False

        # Call parent class's constructor
        super(ImageMaskDialog, self).__init__()

        # Set window flags to customize window behavior
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMaximizeButtonHint)  # Get rid of What's this icon in title bar

        # Load the UI from the ui file
        self.load_ui()

        # Connect signals of reference images to the slot for running mask script
        self.ui.reference_image1.image_file_name_changed.connect(self.run_mask_script)
        self.ui.reference_image2.image_file_name_changed.connect(self.run_mask_script)

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

        # Connect cancel button to close the dialog
        self.ui.cancel_button.clicked.connect(self.reject)

        self.ui.show_rois_checkbox.toggled.connect(self.show_rois)

        self.ui.default_button.clicked.connect(self.set_default_values)

        # Initialize script description
        self.script_description = ''

        # Determine the configuration file for the mask
        if self.main_window.experiment.selected_mask == "" or self.main_window.experiment.selected_mask == "Default":
            self.mask_script = self.main_window.experiment.selected_script
            config_file_name = self.main_window.script_paths[self.mask_script].replace(".py", ".config")
        else:
            self.mask_script = self.main_window.experiment.selected_mask
            config_file_name = self.main_window.mask_paths[self.mask_script].replace(".py", ".config")

        tprint("Mask/Config:", self.mask_script, config_file_name)

        # Create a grid layout to hold mask options
        with open(config_file_name) as config_file:
            data = json.load(config_file)
            if Config.verbose_mode:
                tprint("Read config file:", data)

            # Extract script and mask descriptions
            if "script" in data:
                self.script_description = data['script']['info']['description']

            if "mask" in data:
                self.mask_description = data['mask']['info']['description']

            grid, self.option_checkboxes, self.option_sliders, self.option_wavelengths, self.wavelength_value, self.option_dropdowns, self.option_ranges, self.option_spinboxes, self.default_values = \
                Helper.get_ui_elements_from_config(options=data['mask']['options'], settings=self.main_window.experiment.mask, \
                                                   execute_on_change=self.run_mask_script, dropdown_changed=self.dropdown_changed, \
                                                   slider_value_changed=self.slider_value_changed, wavelength_changed=self.wavelength_changed, \
                                                   script_for_dropdown_values=self.main_window.current_mask_script(), preset_folder=self.main_window.preset_folder)
            
            # Set the layout for mask options
            self.ui.main_box.setLayout(grid)

            tprint(self.option_wavelengths, self.option_dropdowns)

        # Set label and description based on selected mask or script
        if self.main_window.experiment.selected_mask == "" or self.main_window.experiment.selected_mask == "Default":
            self.ui.script_label.setText("Script: " + self.main_window.ui.script_selection_combobox.currentText())
            self.ui.script_description.setText(self.script_description)
        else:
            self.ui.script_label.setText("Mask: " + self.main_window.ui.mask_selection_combobox.currentText().replace(".py", ""))
            self.ui.script_description.setText(self.mask_description)

        # For some reason, geometry won't work unless we move the update outside the constructor
        QTimer.singleShot(300, lambda: self.load_reference_images())

        if self.main_window.test_mode:
            QTimer.singleShot(self.main_window.test_dialog_timeout, lambda:self.accept())

    def load_ui(self):
        self.ui = Ui_ImageMaskDialog()
        self.ui.setupUi(self)

    def slider_value_changed(self, name, option_slider):
        tprint("Slider value changed", name, option_slider, option_slider.value(), option_slider.min, option_slider.max, option_slider.steps, option_slider.stepSize)
        if option_slider.stepSize == 1.0:
            option_slider.optionLabel.setText(str(option_slider.displayName + ": " + str(int(option_slider.value()))))
        else:
            option_slider.optionLabel.setText(str(option_slider.displayName + ": " + str(option_slider.value())))

    def wavelength_changed(self, name, option_wavelength):
        tprint("Wavelength changed", name, option_wavelength, option_wavelength.currentIndex())
        # No action needed, runMaskScript will pull the current values

    def populate_wavelengths(self):
        if self.ui.reference_image1.image_file_name != "":
            date, time, camera, image_wavelengths = Helper.info_from_header_file(self.ui.reference_image1.image_file_name)

            tprint("Wavelengths from image:", image_wavelengths)

            self.wavelengths = ['None']
            self.wavelengths.extend(image_wavelengths)

            # Add the wavelengths from the image to all wavelength dropdowns
            for name, option_wavelength in self.option_wavelengths:
                option_wavelength.clear()
                option_wavelength.addItems(self.wavelengths)

                if name in self.wavelength_value and self.wavelength_value[name] != "":
                    tprint("Restore wavelength", name, self.wavelength_value[name], self.wavelengths)
                    index = option_wavelength.findText(str(self.wavelength_value[name]))
                    option_wavelength.setCurrentIndex(index)

    def dropdown_changed(self, name, option_dropdown, initial_update):
        tprint("Dropdown changed", name, option_dropdown, option_dropdown.currentIndex(), initial_update)
        # runMaskScript will pull the current values

        # If dropdown is referenced by a slider, get related slider ranges from the mask script for the new index
        for slider, dropdown, name in self.option_ranges:
            if dropdown == option_dropdown:
                tprint("Update related slider range", name)

                mask_script = self.main_window.current_mask_script()

                slider.min, slider.max, slider.steps, slider.defaultValue = mask_script.range_values(name, dropdown.currentData(), dropdown.currentIndex())

                slider.stepSize = (slider.max - slider.min) / slider.steps

                slider.setRange(slider.min, slider.max)
                slider.setSingleStep(slider.stepSize)

                if initial_update:
                    start_value = slider.startValue
                else:
                    start_value = slider.defaultValue

                slider.setValue(start_value)

                slider.valueChanged.emit(slider.value())  # Force refresh of label

                tprint("New range:", slider.min, slider.max, slider.steps, slider.defaultValue, slider.stepSize)

                # Find corresponding optionSlider and update the min and stepsize in the tuplet
                for index, item in enumerate(self.option_sliders):
                    itemlist = list(item)  # tuplet is (name, slider, min, stepSize)
                    tprint(itemlist)
                    if itemlist[1] == slider:
                        itemlist[2] = slider.min
                        itemlist[3] = slider.stepSize
                        item = tuple(itemlist)

                        self.option_sliders[index] = item

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
        if self.main_window.experiment.mask_reference_image1 is not None:
            self.ui.reference_image1.set_image_file_name(self.main_window.experiment.mask_reference_image1, self.main_window.experiment.image_options_to_dict())
            tprint("Mask: Load left preview image:", self.main_window.experiment.mask_reference_image1)

        if self.main_window.experiment.mask_reference_image2 is not None:
            self.ui.reference_image2.set_image_file_name(self.main_window.experiment.mask_reference_image2, self.main_window.experiment.image_options_to_dict())
            tprint("Mask: Load right preview image:", self.main_window.experiment.mask_reference_image2)

        self.ui.reference_image1.set_crop_rect(self.main_window.experiment.crop_rect)
        self.ui.reference_image2.set_crop_rect(self.main_window.experiment.crop_rect)

        self.populate_wavelengths()

        self.setup_completed = True
        self.run_mask_script()

        self.refresh_image_sizes()

    def run_mask_script(self):
        # Ensure the function is only executed after the dialog is fully populated
        if self.setup_completed is False:
            return

        # Set the cursor to a wait cursor during script execution
        QGuiApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))

        # Set up temporary file for mask preview
        with tempfile.TemporaryDirectory() as temp_path:
            temp_file_name = os.path.join(temp_path, 'maskPreview.png')

            # Initialize settings dictionary for the script
            settings = {}

            settings["outputImage"] = temp_file_name

            settings['experimentSettings'] = {}
            settings['experimentSettings']['analysis'] = {}
            settings['experimentSettings']['analysis']['maskOptions'] = {}
            settings['experimentSettings']['imageOptions'] = {}

            # Populate mask options from UI elements
            # Note: If you change ui elements here, you are likely to have to update openImageMaskDialog when dialog is closed
            for name, checkbox in self.option_checkboxes:
                settings['experimentSettings']['analysis']['maskOptions'][name] = checkbox.isChecked()

            for name, slider, min, step_size in self.option_sliders:
                settings['experimentSettings']['analysis']['maskOptions'][name] = slider.value()

            for name, wavelength in self.option_wavelengths:
                settings['experimentSettings']['analysis']['maskOptions'][name] = wavelength.currentText()

            for name, dropdown in self.option_dropdowns:
                settings['experimentSettings']['analysis']['maskOptions'][name] = dropdown.currentData()

            # Populate image options
            settings["experimentSettings"]["imageOptions"] = self.main_window.experiment.image_options_to_dict()

            # Get the current mask script
            mask_script = self.main_window.current_mask_script()

            # Process preview image 1 if available
            if self.ui.reference_image1.image_file_name != "":
                settings["inputImage"] = self.ui.reference_image1.image_file_name

                tprint("Mask", settings)

                # Execute the mask script
                mask_script.create_mask(settings)

                # Load the generated mask preview image
                if not self.main_window.experiment.crop_rect.isEmpty():
                    self.original_preview_image1 = QPixmap(temp_file_name).copy(self.main_window.experiment.crop_rect)
                else:    
                    self.original_preview_image1 = QPixmap(temp_file_name)

                # Refresh the preview image on the UI
                self.refresh_preview_image1()

            # Process preview image 2 if available
            if self.ui.reference_image2.image_file_name != "":
                settings["inputImage"] = self.ui.reference_image2.image_file_name

                # Execute the mask script
                mask_script.create_mask(settings)

                # Load the generated mask preview image
                if not self.main_window.experiment.crop_rect.isEmpty():
                    self.original_preview_image2 = QPixmap(temp_file_name).copy(self.main_window.experiment.crop_rect)
                else:    
                    self.original_preview_image2 = QPixmap(temp_file_name)

                # Refresh the preview image on the UI
                self.refresh_preview_image2()

        # Set a flag to indicate that the mask has been defined
        self.main_window.experiment.mask_defined = True

        # Restore the cursor to its original state
        QGuiApplication.restoreOverrideCursor()

    def refresh_preview_image1(self):
        if self.original_preview_image1 is not None:
            width = self.ui.preview_image1.width()
            height = self.ui.preview_image1.height()

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

    def set_default_values(self):
        self.blockSignals(True)
        Helper.set_ui_elements_default_values(self.default_values)
        self.blockSignals(False)
            
    def on_magnify_state_changed1(self, mode, pos, zoom_factor):
        self.ui.preview_image1.set_magnifier_mode(mode, pos, zoom_factor)
    
    def on_magnify_state_changed2(self, mode, pos, zoom_factor):
        self.ui.preview_image2.set_magnifier_mode(mode, pos, zoom_factor)
    