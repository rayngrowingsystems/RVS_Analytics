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

import warnings
import cv2
import numpy as np
from plantcv.plantcv import spectral_index


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


def get_index_functions():
    """Loads list of available spectral indices (plantCV) including min/max ranges"""
    # TODO: Update ranges
    index_dict = {
        "ari": ("ARI - Anthocyanin Reflectance Index",
                spectral_index.ari, -50, 50),
        "cri700": ("CRI700 - Carotenoid Reflectance Index (700)",
                   spectral_index.cri700, -10, 10),
        "evi": ("EVI - Excess Green Index",
                spectral_index.evi, -1, 1),
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