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
from enum import Enum
from os import path

import qdarktheme
from PySide6.QtCore import QDir, QPoint, QRect, QSize, QStandardPaths
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication

import Config
from Helper import tprint


class Experiment:
    ImageSource = Enum('ImageSource', ['Image', 'Folder', 'Camera'])

    def __init__(self, experiment_file_name):
        self.name = ""

        self.experiment_file_name = experiment_file_name

        self.image_source = self.ImageSource.Folder

        self.image_file_path = ""
        self.folder_file_path = ""
        self.camera_file_path = ""
        self.camera_cid = ""
        self.camera_api_keys = {}

        self.output_file_path = os.path.join(
            os.path.normpath(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)),
                             QApplication.organizationName(), QApplication.applicationName(), 'Analysis')
        QDir().mkpath(self.output_file_path)
        tprint("Output folder", self.output_file_path)

        self.mask = {}
        self.mask_defined = False

        self.mask_reference_image1 = None
        self.mask_reference_image2 = None

        self.lens_angle = 60
        self.normalize = False
        self.rotation = 0

        self.script_options = {}
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
        self.mqtt_port = "1883"
        self.mqtt_username = ""
        self.mqtt_password = ""

        self.theme = "auto"

        self.crop_rect = QRect()

        self.session_data = {}

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

    def safe_normpath(self, image):
        if image is not None:
            return os.path.normpath(image)
        else:
            return ""

    def to_dict(self):
        return {
          "name": self.name,
          "imageSource": self.image_source.value - 1,
          "imageFilePath": self.image_file_path,
          "folderFilePath": self.folder_file_path,
          "cameraFilePath": self.camera_file_path,
          "outputFilePath": self.output_file_path,
          "cameraCid": self.camera_cid,
          "cameraApiKeys": self.camera_api_keys,
          "roiInfo": {"rect": [self.roi_info.rect.left(), self.roi_info.rect.top(),
                               self.roi_info.rect.width(), self.roi_info.rect.height()],
                      "columns": self.roi_info.columns,
                      "rows": self.roi_info.rows,
                      "radius": self.roi_info.radius,
                      "width": self.roi_info.width,
                      "height": self.roi_info.height,
                      "shape": self.roi_info.shape.value - 1,
                      "placementMode": self.roi_info.placement_mode.value - 1,
                      "detectionMode": self.roi_info.detection_mode.value - 1,
                      "roiList": self.roi_info.roi_items(1.0)},
          # NOTE: When things are added to the "analysis" section, update analysisToDict below
          "analysis": {"maskOptions": self.mask,
                       "scriptOptions": {"general": self.script_options},
                       "chartOptionTypes": self.chart_option_types,
                       "selectedScript": self.selected_script,
                       "selectedMask": self.selected_mask},
          "maskDefined": self.mask_defined,
          "maskReferenceImage1": self.safe_normpath(self.mask_reference_image1),
          "maskReferenceImage2": self.safe_normpath(self.mask_reference_image2),
          "imageOptions": {"lensAngle": self.lens_angle,
                           "normalize": self.normalize,
                           "rotation": self.rotation},
          "roiReferenceImage1": self.safe_normpath(self.roi_reference_image1),
          "roiReferenceImage2": self.safe_normpath(self.roi_reference_image2),
          "scriptReferenceImage1": self.safe_normpath(self.script_reference_image1),
          "scriptReferenceImage2": self.safe_normpath(self.script_reference_image2),
          "cameraDiscoveryIp": self.camera_discovery_ip,
          "mqttBroker": self.mqtt_broker,
          "mqttPort": self.mqtt_port,
          "mqttUserName": self.mqtt_username,
          "mqttPassword": self.mqtt_password,
          "theme": self.theme,
          "themeBackgroundColor": self.theme_background_color(),
          "sessionData": self.session_data,
          "cropRect": [self.crop_rect.left(), self.crop_rect.top(), self.crop_rect.width(), self.crop_rect.height()],
        }

    def analysis_to_dict(self):
        return {
          "analysis": {"maskOptions": self.mask,
                       "scriptOptions": {"general": self.script_options},
                       "chartOptionTypes": self.chart_option_types,
                       "selectedScript": self.selected_script,
                       "selectedMask": self.selected_mask}
        }

    def image_options_to_dict(self):
        return {"lensAngle": self.lens_angle,
                "normalize": self.normalize,
                "rotation": self.rotation}

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

            self.image_source = self.ImageSource(image_source_number + 1)

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
            self.roi_info.rect = QRect(d["roiInfo"]["rect"][0], d["roiInfo"]["rect"][1],
                                       d["roiInfo"]["rect"][2], d["roiInfo"]["rect"][3])
            self.roi_info.columns = d["roiInfo"]["columns"]
            self.roi_info.rows = d["roiInfo"]["rows"]
            self.roi_info.radius = d["roiInfo"]["radius"]

            if "width" in d["roiInfo"]:
                self.roi_info.width = d["roiInfo"]["width"]

            if "height" in d["roiInfo"]:
                self.roi_info.height = d["roiInfo"]["height"]

            if "shape" in d["roiInfo"]:
                shape_number = d["roiInfo"]["shape"]

                self.roi_info.shape = self.roi_info.Shape(shape_number + 1)

            if "placementMode" in d["roiInfo"]:
                placement_mode_number = d["roiInfo"]["placementMode"]

                self.roi_info.placement_mode = self.roi_info.PlacementMode(placement_mode_number + 1)

            if "detectionMode" in d["roiInfo"]:
                detection_mode_number = d["roiInfo"]["detectionMode"]

                self.roi_info.detection_mode = self.roi_info.DetectionMode(detection_mode_number + 1)

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

            if "rotation" in d["imageOptions"]:
                self.rotation = d["imageOptions"]["rotation"]

        if "analysis" in d:
            self.script_options = d["analysis"]["scriptOptions"]["general"]
            tprint("Loaded scriptOptions", self.script_options)

            self.mask = d["analysis"]["maskOptions"]
            tprint("Loaded maskOptions", self.mask)

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

        if "mqttPort" in d:
            self.mqtt_port = d["mqttPort"]

        if "mqttUserName" in d:
            self.mqtt_username = d["mqttUserName"]

        if "mqttPassword" in d:
            self.mqtt_password = d["mqttPassword"]

        if "theme" in d:
            self.theme = d["theme"]
        else:
            self.theme = "auto"

        if "sessionData" in d:
            self.session_data = d["sessionData"]

        if "cropRect" in d:
            self.crop_rect = QRect(d["cropRect"][0], d["cropRect"][1], d["cropRect"][2], d["cropRect"][3])

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

    def clear_all_preview_images(self):
        self.mask_reference_image1 = None
        self.mask_reference_image2 = None
        self.roi_reference_image1 = None
        self.roi_reference_image2 = None
        self.script_reference_image1 = None
        self.script_reference_image2 = None

    def clear_analysis(self):
        if self.analysis is not None:
            self.analysis["maskOptions"] = {}
            self.analysis["scriptOptions"]["general"] = {}
            self.analysis["chartOptions"] = {}

    def current_folder(self):
        if self.image_source is self.ImageSource.Image:
            return self.image_file_path
        elif self.image_source is self.ImageSource.Folder:
            return self.folder_file_path
        elif self.image_source is self.ImageSource.Camera:
            return self.camera_file_path
        else:
            return ""

    # Conversion routines between original image coordinates and UI coordinates via an optional crop rectangle

    def image_to_point_coordinates(self, point, crop_rect, scaling_factor):
        if not crop_rect.isEmpty():
            p = point - crop_rect.topLeft()  # Change from original image to crop_rect coordinates
            p = QPoint(p.x() * scaling_factor, p.y() * scaling_factor)  # Change from crop_rect to UI coordinates

            return p
        else:
            return QPoint(point.x() * scaling_factor, point.y() * scaling_factor)

    def point_to_image_coordinates(self, point, crop_rect, scaling_factor):
        if not crop_rect.isEmpty():
            # Change from UI to crop_rect coordinates
            p = QPoint(point.x() / scaling_factor, point.y() / scaling_factor)
            p = p + crop_rect.topLeft()  # Change from crop_rect to original image coordinates

            return p
        else:
            return QPoint(point.x() / scaling_factor, point.y() / scaling_factor)

    def image_to_rect_coordinates(self, rect, crop_rect, scaling_factor):
        return QRect(self.image_to_point_coordinates(rect.topLeft(), crop_rect, scaling_factor), \
                     QSize(rect.width() * scaling_factor, rect.height() * scaling_factor))

    def rect_to_image_coordinates(self, rect, crop_rect, scaling_factor):
        return QRect(self.point_to_image_coordinates(rect.topLeft(), crop_rect, scaling_factor), \
                     QSize(rect.width() / scaling_factor, rect.height() / scaling_factor))

    def theme_background_color(self):
        application_palette = qdarktheme.load_palette(self.theme)
        background_color = application_palette.color(QPalette.Window)
        return background_color.name()

