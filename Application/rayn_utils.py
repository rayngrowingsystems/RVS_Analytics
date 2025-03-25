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

import warnings
import cv2
import numpy as np
import os
from os import path
from plantcv.plantcv import spectral_index
from plantcv.plantcv import readimage
from plantcv.plantcv.transform import rotate
from plantcv.plantcv import print_image
from plantcv.plantcv import crop


def load_coefficients(path):
    """Loads camera matrix and distortion coefficients from file

    File format should be an opencv-matrix saved as .yml
    """

    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)
    camera_matrix = cv_file.getNode('K').mat()
    dist_matrix = cv_file.getNode('D').mat()

    cv_file.release()
    return [camera_matrix, dist_matrix]


def undistort_img(image_path, mtx, dist, alpha=0.0):
    """Applies undistortion matrix on rgb image"""
    original_img = cv2.imread(image_path)
    h, w = original_img.shape[:2]

    # alpha determines how much of the image is cut off after undistortion
    new_cam_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), alpha, (w, h))
    undistorted_img = cv2.undistort(original_img, mtx, dist, None, new_cam_mtx)

    return undistorted_img


def undistort_data_cube(data_cube, mtx, dist, alpha=0.0):
    """Applies undistortion matrix on hyperspectral data cube"""
    h, w = data_cube.shape[:2]

    # alpha determines how much of the image is cut off after undistortion
    new_cam_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), alpha, (w, h))
    undistorted_data_cube = cv2.undistort(data_cube, mtx, dist, None, new_cam_mtx)

    return undistorted_data_cube


def dark_normalize_array_data(pcv_spectral_array):
    """Normalizes the array data using the dark reference image"""

    if 0 in pcv_spectral_array.wavelength_dict.keys():  # checking if dark array is available
        dark_array = pcv_spectral_array.array_data[:, :, int(pcv_spectral_array.wavelength_dict[0])]
        dark_array = np.repeat(dark_array[:, :, np.newaxis],
                               len(pcv_spectral_array.wavelength_dict),
                               axis=2)

        normalized_array_data = pcv_spectral_array.array_data - dark_array

        return normalized_array_data

    else:
        warnings.warn("No dark reference available to normalize the array data. Returning original array data")
        return pcv_spectral_array.array_data


def create_gaussian(x, amplitude, mean, stdev):
    """Creates a gaussian normal distribution as numpy array"""

    return (
            amplitude * np.exp(-np.power((x - mean) / stdev, 2.0) / 2)
    )


def get_correction_matrix_from_file(file_path):
    """Load a correction matrix from file"""

    if file_path.endswith(".csv"):
        correction_matrix = np.genfromtxt(file_path, delimiter=',')
    elif file_path.endswith(".npy"):
        correction_matrix = np.load(file_path)
    else:
        warnings.warn("Unknown file type for correction matrix")
        correction_matrix = None

    return correction_matrix


def get_correction_matrix_from_parameter(image_size_tuple, x_parameter_list, y_parameter_list):
    """Creates correction matrix based on Gaussian parameters for x and y direction"""
    values = np.arange(image_size_tuple[0])

    # gaussian parameter list content: [amplitude, mean, standard deviation]
    x_dist = create_gaussian(values, x_parameter_list[0], x_parameter_list[1], x_parameter_list[2])
    y_dist = create_gaussian(values, y_parameter_list[0], y_parameter_list[1], x_parameter_list[2])

    correction_matrix = y_dist[:, None] * x_dist
    correction_matrix /= correction_matrix.max()  # normalize the correction matrix
    correction_matrix = correction_matrix[:image_size_tuple[1], :]  # crops the correction matrix to the image size
    return correction_matrix


def light_intensity_correction(spectral_array_object, correction_matrix, normalize=True):
    """Applies the light intensity correction to hyperspectral image object (plantCV)"""

    # correcting spectral array
    for layer in range(0, spectral_array_object.array_data.shape[2]):  # looping through the wavelength bands
        corrected_layer = spectral_array_object.array_data[:, :, layer] / correction_matrix
        if normalize:
            corrected_layer /= corrected_layer.max()

        spectral_array_object.array_data[:, :, layer] = corrected_layer

    # correcting pseudoRGB
    for layer in range(0, spectral_array_object.pseudo_rgb.shape[2]):
        corrected_layer = spectral_array_object.pseudo_rgb[:, :, layer] / correction_matrix
        if normalize:
            corrected_layer /= corrected_layer.max()
        spectral_array_object.pseudo_rgb[:, :, layer] = corrected_layer * 255

    return spectral_array_object


def prepare_spectral_data(settings, file_name=False, preview=False):
    # file and settings
    if preview and file_name:
        img_file = file_name
        image_options = settings
    else:
        img_file = settings["inputImage"]
        image_options = settings["experimentSettings"]["imageOptions"]

    # check if a .hdr file name was provided and set img_file to the binary location
    if os.path.splitext(img_file)[1] == ".hdr":
        img_file = os.path.splitext(img_file)[0]

    else:
        warnings.warn("No header file provided. Processing not possible.")
        return

    # read image data
    spectral_data = readimage(filename=img_file, mode='envi')

    # prepare image data
    spectral_data.array_data = spectral_data.array_data.astype("float32")  # required for further calculations
    if spectral_data.d_type == np.uint8:  # only convert if data seems to be uint8
        spectral_data.array_data = spectral_data.array_data / 255  # convert 0-255 (orig.) to 0-1 range

    rvs_dict = parse_rvs_header(f"{img_file}.hdr")

    # normalize the image cube
    if image_options["normalize"]:
        spectral_data.array_data = dark_normalize_array_data(spectral_data)

    # undistort the image cube
    if image_options["lensAngle"] != 0:  # only undistort if angle is selected
        cam_calibration_file = path.join(path.dirname(__file__),
                                         f"calibration_data/{image_options['lensAngle']}_calibration_data.yml")  # select the data set
        mtx, dist = load_coefficients(cam_calibration_file)  # depending on the lens angle
        spectral_data.array_data = undistort_data_cube(spectral_data.array_data, mtx, dist)
        spectral_data.pseudo_rgb = undistort_data_cube(spectral_data.pseudo_rgb, mtx, dist)

    # apply rotation
    if image_options["rotation"] != 0:
        spectral_data.array_data = rotate(spectral_data.array_data, image_options["rotation"], crop=False)
        spectral_data.pseudo_rgb = rotate(spectral_data.pseudo_rgb, image_options["rotation"], crop=False)

    # calculate pixel to mm conversion factor
    rvs_dict["px to mm ratio"] = 0
    if image_options["lensAngle"] == 60 and "exact distance (mm)" in rvs_dict:
        pixel_per_mm = 1000/int(rvs_dict["exact distance (mm)"])  # with a 60° lens at 1000 mm the px to mm ratio is 1
        rvs_dict["px to mm ratio"] = pixel_per_mm

    # crop the image
    if preview:
        crop_rectangle = [0, 0, 0, 0]
    else:
        crop_rectangle = settings["experimentSettings"]["cropRect"]

    if crop_rectangle != [0, 0, 0, 0]:
        spectral_data = crop(spectral_data,
                             x=crop_rectangle[0],
                             y=crop_rectangle[1],
                             h=crop_rectangle[2],
                             w=crop_rectangle[3])

    return spectral_data, rvs_dict


def get_index_functions():
    """Loads list of available spectral indices (plantCV) including min/max ranges"""
    # TODO: Update ranges
    index_dict = {
        "ari": ("ARI - Anthocyanin Reflectance Index",
                spectral_index.ari, -50, 50),
        "cri700": ("CRI700 - Carotenoid Reflectance Index (700)",
                   spectral_index.cri700, -10, 10),
        "egi": ("EGI - Excess Green Index",
                spectral_index.egi, -1, 2),
        "evi": ("EVI - Enhanced Vegetation Index",
                spectral_index.evi, -1, 1),
        "gli": ("GLI - Green Leaf Index",
                spectral_index.gli, -1, 1),
        "gdvi": ("GDVI - Green Difference Vegetation Index",
                 spectral_index.gdvi, -0.5, 0.5),
        "mari": ("MARI - Modified Anthocyanin Reflectance Index",
                 spectral_index.mari, -10, 5),
        "mcari": ("MCARI - Modified Chlorophyll Absorption Reflectance Index",
                  spectral_index.mcari, -0.5, 0.5),
        "ndvi": ("NDVI - Normalized Difference Vegetation Index",
                 spectral_index.ndvi, -1, 1),
        "pri": ("PRI - Photochemical Reflectance Index",
                spectral_index.pri, -1, 1),
        "psnd_chla": ("PSND CHLA - Pigment Specific Normalized Differences (Chlorophyll A)",
                      spectral_index.psnd_chla, -1, 1),
        "psnd_chlb": ("PSND CHLB - Pigment Specific Normalized Differences (Chlorophyll B)",
                      spectral_index.psnd_chlb, -1, 1),
        "psnd_car": ("PSND CAR - Pigment Specific Normalized Differences (Carotenoid)",
                     spectral_index.psnd_car, -1, 1),
        "psri": ("PSRI - Plant Senescence Reflectance Index",
                 spectral_index.psri, -5, 1),
        "pssr_chla": ("PSSR CHLA - Pigment Specific Simple Ratio (Chlorophyll A)",
                      spectral_index.pssr_chla, -1, 1),
        "pssr_chlb": ("PSSR CHLB - Pigment Specific Simple Ratio (Chlorophyll B)",
                      spectral_index.pssr_chlb, -1, 1),
        "pssr_car": ("PSSR CAR - Pigment Specific Simple Ratio (Carotenoid)",
                     spectral_index.pssr_car, -1, 1),
        "rgri": ("RGRI - Red:Green Ratio Index for Anthocyanin",
                 spectral_index.rgri, 0, 5),
        "savi": ("SAVI - Soil Adjusted Vegetation Index",
                 spectral_index.savi, -1.2, 1.2),
        "sipi": ("SIPI - Structure-Independent Pigment Index",
                 spectral_index.sipi, -5, 5),
        "sr": ("SR - Simple Ratio",
               spectral_index.sr, 0, 10)
    }

    return index_dict


def parse_rvs_header(headername):

    # Initialize dictionary
    header_dict = {}
    with open(headername, "r") as f:
        # Replace characters for easier parsing
        hdata = f.read()
        hdata = hdata.replace(",\n", ",")
        hdata = hdata.replace("\n,", ",")
        hdata = hdata.replace("{\n", "{")
        hdata = hdata.replace("\n}", "}")
        hdata = hdata.replace(" \n ", "")
        hdata = hdata.replace(" \n", "")
        hdata = hdata.replace(";", "")
    hdata = hdata.split("\n")

    # Loop through and create a dictionary from the header file
    # Try to reformat strings by replacing all " = " with '=' and " : "
    for string in hdata:
        # Remove white space for consistency across header file formats
        if '=' in string:
            header_data = string.split("=")
            header_data[0] = header_data[0].lower()
            header_dict.update({header_data[0].rstrip(): header_data[1].rstrip()})
        elif ':' in string:
            header_data = string.split(":")
            header_data[0] = header_data[0].lower()
            header_dict.update({header_data[0].rstrip(): header_data[1].rstrip()})

    # Delete redundant entries
    entries_to_remove = ["samples", "lines", "bands", "header offset", "file type", "data type", "interleave",
                         "byte order", "wavelength"]
    for key in entries_to_remove:
        if key in header_dict:
            del header_dict[key]

    # Reformat header dict
    if "description" in header_dict:
        header_dict["description"] = header_dict["description"].replace("{", "")
        header_dict["description"] = header_dict["description"].replace("}", "")

    # remove initial white space
    for key in header_dict.keys():
        if header_dict[key][0] == " ":
            header_dict[key] = header_dict[key][1:]

    list_entries_to_reformat = ["brightness", "exposure", "sensitivity", "reflective factor", "image output"]
    for key in list_entries_to_reformat:
        if key in header_dict:
            header_dict[key] = header_dict[key].replace(" ", "")
            header_dict[key] = header_dict[key].replace("{", "")
            header_dict[key] = header_dict[key].replace("}", "")
            header_dict[key] = header_dict[key].split(",")

    return header_dict


def create_mask_preview(mask, pseudo_rgb, settings, create_preview=True):
    mask_options = settings["experimentSettings"]["analysis"]["maskOptions"]

    if create_preview:
        out_image = preview_settings["output_image"]
        image_file_name = os.path.normpath(out_image)
        print("Writing image to " + image_file_name)

        if mask_options["overlay_mask"]:
            _alpha_base_level = 60
            alpha = np.ones(pseudo_rgb.shape[:2], dtype=np.uint8)*_alpha_base_level
            alpha = np.where(mask > 0, 255, alpha)
            bgra = np.dstack((pseudo_rgb, alpha))
            print_image(img=bgra, filename=image_file_name)

        else:
            print_image(img=mask, filename=image_file_name)