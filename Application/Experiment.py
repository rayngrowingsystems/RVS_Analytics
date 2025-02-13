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

import json
import os
from os import path

from PySide6.QtCore import QRect, QSize, QStandardPaths, QDir
from PySide6.QtWidgets import QApplication

from enum import Enum

import Config

from Helper import tprint

class Experiment:
    ImageSource = Enum('ImageSource', ['Image', 'Folder', 'Camera'])

    def __init__(self, experiment_file_name):
        self.name = ""

        self.experiment_file_name = experiment_file_name

        self.ImageSource = self.ImageSource.Folder

        self.image_file_path = ""
        self.folder_file_path = ""
        self.camera_file_path = ""
        self.camera_cid = ""
        self.camera_api_keys = {}

        self.output_file_path = os.path.join(os.path.normpath(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)), QApplication.organizationName(), QApplication.applicationName(), 'Analysis')
        QDir().mkpath(self.output_file_path)
        tprint("Output folder", self.output_file_path)

        self.mask = {}
        self.mask_defined = False

        self.mask_reference_image1 = None
        self.mask_reference_image2 = None

        self.lens_angle = 60
        self.normalize = False
        self.light_correction = False
        self.rotation = 0
        self.crop = False

        self.script_options = {}
        self.chart_options = {}
        self.chart_option_types = {}

        self.roi_info = self.RoiInfo()

        self.roi_reference_image1 = None
        self.roi_reference_image2 = None

        self.script_reference_image1 = None
        self.script_reference_image2 = None

        self.camera_discovery_ip = ""

        self.selected_script = ""
        self.selected_mask = ""

        self.analysis = None

        self.mqtt_broker = ""

    class RoiInfo:
        PlacementMode = Enum('PlacementMode', ['Matrix', 'Manual'])
        Shape = Enum('Shape', ['Circle', 'Rectangle', 'Ellipse', 'Polygon'])
        DetectionMode = Enum('DetectionMode', ['Partial', 'CutTo', 'Largest'])

        def __init__(self):
            self.rect = QRect()
            self.columns = 5
            self.rows = 3
            self.radius = 20
            self.width = 40
            self.height = 40
            self.shape = self.Shape.Circle
            self.placement_mode = self.PlacementMode.Matrix
            self.detection_mode = self.DetectionMode.Partial
            self.manual_roi_items = []

        def roi_items(self, scaling_factor):
            roi_items = []

            if self.rect.isValid() or len(self.manual_roi_items) > 0:
                if self.placement_mode == self.PlacementMode.Matrix:
                    if self.columns > 1:
                        spacing_x = self.rect.width() / (self.columns - 1)
                    else:
                        spacing_x = 0

                    if self.rows > 1:
                        spacing_y = self.rect.height() / (self.rows - 1)
                    else:
                        spacing_y = 0

                    for r in range(self.rows):
                        for c in range(self.columns):
                            x = self.rect.x() + c * spacing_x
                            y = self.rect.y() + r * spacing_y

                            d = {}
                            if self.shape == self.Shape.Circle:
                                d["type"] = "Circle"
                                d["x"] = int(x)
                                d["y"] = int(y)
                                d["width"] = int(self.radius * 2 / scaling_factor)
                                d["height"] = int(self.radius * 2 / scaling_factor)
                            elif self.shape == self.Shape.Rectangle:
                                d["type"] = "Rectangle"
                                d["x"] = int(x)
                                d["y"] = int(y)
                                d["width"] = int(self.width / scaling_factor)
                                d["height"] = int(self.height / scaling_factor)
                            elif self.shape == self.Shape.Ellipse:
                                d["type"] = "Ellipse"
                                d["x"] = int(x)
                                d["y"] = int(y)
                                d["width"] = int(self.width / scaling_factor)
                                d["height"] = int(self.height / scaling_factor)
                            elif self.shape == self.Shape.Polygon:
                                tprint("Polygon not supported in matrix mode")
                            else:
                                tprint("Missing shape type")

                            roi_items.append(d)

                    # tprint("Experiment.RoiInfo.roiItems (matrix):", roi_items)
                elif self.placement_mode == self.PlacementMode.Manual:
                    roi_items = self.manual_roi_items

                    # tprint("Experiment.RoiInfo.roiItems (manual):", roi_items)

            return roi_items

        def shape_number(self):
            if self.shape == self.Shape.Circle:
                return 0
            elif self.shape == self.Shape.Rectangle:
                return 1
            elif self.shape == self.Shape.Ellipse:
                return 2
            elif self.shape == self.Shape.Polygon:
                return 3
            else:
                return -1

        def placement_mode_number(self):
            if self.placement_mode == self.PlacementMode.Matrix:
                return 0
            elif self.placement_mode == self.PlacementMode.Manual:
                return 1
            else:
                return -1

        def detection_mode_number(self):
            if self.detection_mode == self.DetectionMode.Partial:
                return 0
            elif self.detection_mode == self.DetectionMode.CutTo:
                return 1
            elif self.detection_mode == self.DetectionMode.Largest:
                return 2
            else:
                return -1

    def image_source_number(self):
        if self.ImageSource == self.ImageSource.Image:
            return 0
        elif self.ImageSource == self.ImageSource.Folder:
            return 1
        elif self.ImageSource == self.ImageSource.Camera:
            return 2
        else:
            return -1

    def safe_normpath(self, image):
        if image is not None:
            return os.path.normpath(image)
        else:
            return ""

    def to_dict(self):
        return {
          "name": self.name,
          "imageSource": self.image_source_number(),
          "imageFilePath": self.image_file_path,
          "folderFilePath": self.folder_file_path,
          "cameraFilePath": self.camera_file_path,
          "outputFilePath": self.output_file_path,
          "cameraCid": self.camera_cid,
          "cameraApiKeys": self.camera_api_keys,
          "roiInfo": {"rect": [self.roi_info.rect.left(), self.roi_info.rect.top(), self.roi_info.rect.width(), self.roi_info.rect.height()],
                      "columns": self.roi_info.columns,
                      "rows": self.roi_info.rows,
                      "radius": self.roi_info.radius,
                      "width": self.roi_info.width,
                      "height": self.roi_info.height,
                      "shape": self.roi_info.shape_number(),
                      "placementMode": self.roi_info.placement_mode_number(),
                      "detectionMode": self.roi_info.detection_mode_number(),
                      "roiList": self.roi_info.roi_items(1.0)},
          # NOTE: When things are added to the "analysis" section, update analysisToDict below
          "analysis": {"maskOptions": self.mask,
                       "scriptOptions": {"general": self.script_options},
                       "chartOptions": self.chart_options,
                       "chartOptionTypes": self.chart_option_types,
                       "selectedScript": self.selected_script,
                       "selectedMask": self.selected_mask},
          "maskDefined": self.mask_defined,
          "maskReferenceImage1": self.safe_normpath(self.mask_reference_image1),
          "maskReferenceImage2": self.safe_normpath(self.mask_reference_image2),
          "imageOptions": {"lensAngle": self.lens_angle,
                           "normalize": self.normalize,
                           "lightCorrection": self.light_correction,
                           "rotation": self.rotation,
                           "crop": self.crop},
          "roiReferenceImage1": self.safe_normpath(self.roi_reference_image1),
          "roiReferenceImage2": self.safe_normpath(self.roi_reference_image2),
          "scriptReferenceImage1": self.safe_normpath(self.script_reference_image1),
          "scriptReferenceImage2": self.safe_normpath(self.script_reference_image2),
          "cameraDiscoveryIp": self.camera_discovery_ip,
          "mqttBroker": self.mqtt_broker
        }

    def analysis_to_dict(self):
        return {
          "analysis": {"maskOptions": self.mask,
                       "scriptOptions": {"general": self.script_options},
                       "chartOptions": self.chart_options,
                       "chartOptionTypes": self.chart_option_types,
                       "selectedScript": self.selected_script,
                       "selectedMask": self.selected_mask}
        }

    def image_options_to_dict(self):
        return {"lensAngle": self.lens_angle,
                "normalize": self.normalize,
                "lightCorrection": self.light_correction,
                "rotation": self.rotation,
                "crop": self.crop}

    def update_experiment_file(self):
        d = self.to_dict()

        j = json.dumps(d, indent=4)

        with open(self.experiment_file_name, 'w') as f:  # TODO
            f.write(j)

    def from_dict(self, d):
        if "name" in d:
            self.name = d["name"]
        if "imageSource" in d:
            image_source_number = d["imageSource"]

            if image_source_number == 0:
                self.ImageSource = self.ImageSource.Image
            elif image_source_number == 1:
                self.ImageSource = self.ImageSource.Folder
            elif image_source_number == 2:
                self.ImageSource = self.ImageSource.Camera
        if "imageFilePath" in d:
            self.image_file_path = os.path.normpath(d["imageFilePath"])
        if "folderFilePath" in d:
            self.folder_file_path = os.path.normpath(d["folderFilePath"])
        if "cameraFilePath" in d:
            self.camera_file_path = os.path.normpath(d["cameraFilePath"])

        if "outputFilePath" in d:
            self.output_file_path = d["outputFilePath"]

        if "cameraCid" in d:
            self.camera_cid = d["cameraCid"]

        if "cameraApiKeys" in d:
            self.camera_api_keys = d["cameraApiKeys"]

        if "roiInfo" in d:
            self.roi_info.rect = QRect(d["roiInfo"]["rect"][0], d["roiInfo"]["rect"][1], d["roiInfo"]["rect"][2], d["roiInfo"]["rect"][3])
            self.roi_info.columns = d["roiInfo"]["columns"]
            self.roi_info.rows = d["roiInfo"]["rows"]
            self.roi_info.radius = d["roiInfo"]["radius"]

            if "width" in d["roiInfo"]:
                self.roi_info.width = d["roiInfo"]["width"]

            if "height" in d["roiInfo"]:
                self.roi_info.height = d["roiInfo"]["height"]

            if "shape" in d["roiInfo"]:
                shape_number = d["roiInfo"]["shape"]

                if shape_number == 0:
                    self.roi_info.shape = self.roi_info.Shape.Circle
                elif shape_number == 1:
                    self.roi_info.shape = self.roi_info.Shape.Rectangle
                elif shape_number == 2:
                    self.roi_info.shape = self.roi_info.Shape.Ellipse
                elif shape_number == 3:
                    self.roi_info.shape = self.roi_info.Shape.Polygon

            if "placementMode" in d["roiInfo"]:
                placement_mode_number = d["roiInfo"]["placementMode"]

                if placement_mode_number == 0:
                    self.roi_info.placement_mode = self.roi_info.PlacementMode.Matrix
                elif placement_mode_number == 1:
                    self.roi_info.placement_mode = self.roi_info.PlacementMode.Manual

            if "detectionMode" in d["roiInfo"]:
                detection_mode_number = d["roiInfo"]["detectionMode"]

                if detection_mode_number == 0:
                    self.roi_info.detection_mode = self.roi_info.DetectionMode.Partial
                elif detection_mode_number == 1:
                    self.roi_info.detection_mode = self.roi_info.DetectionMode.CutTo
                elif detection_mode_number == 2:
                    self.roi_info.detection_mode = self.roi_info.DetectionMode.Largest

            if "roiList" in d["roiInfo"]:
                self.roi_info.manual_roi_items = []
                for item in d["roiInfo"]["roiList"]:
                    roi_item = {}
                    roi_item["type"] = item["type"]
                    roi_item["x"] = int(item["x"])
                    roi_item["y"] = int(item["y"])
                    roi_item["width"] = int(item["width"])
                    roi_item["height"] = int(item["height"])

                    if "points" in item:
                        result = []
                        for point in item["points"]:
                            result.append([int(point[0]), int(point[1])])

                        roi_item["points"] = result
             
                    self.roi_info.manual_roi_items.append(roi_item)

                # tprint("RoiList unscaled:", self.roi_info.manual_roi_items)

            if "roiItems" in d["roiInfo"]:  # Migrate old tuple based format
                self.roi_info.manual_roi_items = []
                for item in d["roiInfo"]["roiItems"]:
                    roi_item = {}
                    roi_item["type"] = item[0]
                    roi_item["x"] = int(item[1])
                    roi_item["y"] = int(item[2])
                    roi_item["width"] = int(item[3])
                    roi_item["height"] = int(item[4])

                    self.roi_info.manual_roi_items.append(roi_item)

                # tprint("RoiList unscaled:", self.roi_info.manual_roi_items)

        if "maskDefined" in d:
            self.mask_defined = d["maskDefined"]

        if "maskReferenceImage1" in d:
            self.mask_reference_image1 = os.path.normpath(d["maskReferenceImage1"])

        if "maskReferenceImage2" in d:
            self.mask_reference_image2 = os.path.normpath(d["maskReferenceImage2"])

        if "imageOptions" in d:
            if "lensAngle" in d["imageOptions"]:
                self.lens_angle = d["imageOptions"]["lensAngle"]
            else:
                self.lens_angle = 60

            self.normalize = d["imageOptions"]["normalize"]

            if "lightCorrection" in d["imageOptions"]:
                self.light_correction = d["imageOptions"]["lightCorrection"]

            if "rotation" in d["imageOptions"]:
                self.rotation = d["imageOptions"]["rotation"]

            if "crop" in d["imageOptions"]:
                self.crop = d["imageOptions"]["crop"]

        if "analysis" in d:
            self.script_options = d["analysis"]["scriptOptions"]["general"]
            tprint("Loaded scriptOptions", self.script_options)

            self.mask = d["analysis"]["maskOptions"]
            tprint("Loaded maskOptions", self.mask)

            if "chartOptions" in d["analysis"]:
                self.chart_options = d["analysis"]["chartOptions"]
                tprint("Loaded chartOptions", self.chart_options)

            if "chartOptionTypes" in d["analysis"]:
                self.chart_option_types = d["analysis"]["chartOptionTypes"]

            self.selected_script = d["analysis"]["selectedScript"]

            if "selectedMask" in d["analysis"]:
                self.selected_mask = d["analysis"]["selectedMask"]

        if "roiReferenceImage1" in d:
            self.roi_reference_image1 = os.path.normpath(d["roiReferenceImage1"])

        if "roiReferenceImage2" in d:
            self.roi_reference_image2 = os.path.normpath(d["roiReferenceImage2"])

        if "scriptReferenceImage1" in d:
            self.script_reference_image1 = os.path.normpath(d["scriptReferenceImage1"])

        if "scriptReferenceImage2" in d:
            self.script_reference_image2 = os.path.normpath(d["scriptReferenceImage2"])

        if "cameraDiscoveryIp" in d:
            self.camera_discovery_ip = d["cameraDiscoveryIp"]

        if "mqttBroker" in d:
            self.mqtt_broker = d["mqttBroker"]

    def from_json(self):
        if path.exists(self.experiment_file_name):
            with open(self.experiment_file_name, 'r') as f:  # TODO
                j = f.read()
                d = json.loads(j)

                if Config.verbose_mode:
                    tprint("Read experiment settings:", d)
                else:
                    tprint("Read experiment settings")

                self.from_dict(d)

    def all_preview_images_empty(self):
        return self.mask_reference_image1 in [None, '.'] and self.mask_reference_image2 in [None, '.'] and \
               self.roi_reference_image1 in [None, '.'] and self.roi_reference_image2 in [None, '.'] and \
               self.script_reference_image1 in [None, '.'] and self.script_reference_image2 in [None, '.']
    
    def clear_analysis(self):
        if self.analysis is not None:
            self.analysis["maskOptions"] = {}
            self.analysis["scriptOptions"]["general"] = {}
            self.analysis["chartOptions"] = {}

    def current_folder(self):
        if self.ImageSource is self.ImageSource.Image:
            return self.image_file_path
        elif self.ImageSource is self.ImageSource.Folder:
            return self.folder_file_path
        elif self.ImageSource is self.ImageSource.Camera:
            return self.camera_file_path
        else:
            return ""
