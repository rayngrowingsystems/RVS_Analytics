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

from datetime import datetime

def info_from_header_file(file_name):
    header_dict, wavelength_dict = _parse_envi(file_name)

    # print("Header wavelength info", header_dict, header_dict["wavelength"])

    date = ""
    time = ""
    camera = ""

    if "capturedate" in header_dict:
        date = header_dict["capturedate"]
    if "capturetime" in header_dict:
        time = header_dict["capturetime"]
    if "camera" in header_dict:
        camera = header_dict["camera"]

    if date == "" and time == "":
        now = datetime.now()

        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

    return date, time, camera, header_dict["wavelength"]

    # Old implementation - obsolete
    with open(file_name, 'r') as hdr:
        lines = hdr.readlines()

        date = ""
        time = ""
        camera = ""
        wavelengths = []

        for line in lines:
            if line.startswith('capture date = '):
                date = line.replace('capture date = ', '').replace('\n', '')
            elif line.startswith('capture time = '):
                time = line.replace('capture time = ', '').replace('\n', '')
            elif line.startswith('camera = '):
                camera = line.replace('camera = ', '').replace('\n', '')
            elif line.startswith('wavelength = '):
                wavelengths = line.replace('wavelength = ', '').replace('\n', '').replace('{', '').replace('}', '').replace(' ', '').split(",")

        return date, time, camera, wavelengths

# Copied from plantcv
def _parse_envi(headername):
    """Parse a header file and create dictionary of relevant metadata

    Keyword arguments:
    headername      = File path/name of a hyperspectral data file.

    Returns:
    header_dict     = Dictionary of hdr metadata
    wavelength_dict = Dictionary of wavelength metadata

    :param headername: str
    :return header_dict: dict
    :return wavelength_dict: dict

    """
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
        string = string.replace(' ', '')
        if '=' in string:
            header_data = string.split("=")
            header_data[0] = header_data[0].lower()
            header_dict.update({header_data[0].rstrip(): header_data[1].rstrip()})
        elif ':' in string:
            header_data = string.split(":")
            header_data[0] = header_data[0].lower()
            header_dict.update({header_data[0].rstrip(): header_data[1].rstrip()})

    # Reformat wavelengths
    header_dict["wavelength"] = header_dict["wavelength"].replace("{", "")
    header_dict["wavelength"] = header_dict["wavelength"].replace("}", "")
    header_dict["wavelength"] = header_dict["wavelength"].replace(" ", "")
    header_dict["wavelength"] = header_dict["wavelength"].split(",")

    # Create dictionary of wavelengths
    wavelength_dict = {}
    for j, wavelength in enumerate(header_dict["wavelength"]):
        wavelength_dict.update({float(wavelength): float(j)})

    # Replace datatype ID number with the numpy datatype
    # dtype_dict = {"1": np.uint8, "2": np.int16, "3": np.int32, "4": np.float32, "5": np.float64, "6": np.complex64,
    #               "9": np.complex128, "12": np.uint16, "13": np.uint32, "14": np.int64, "15": np.uint64}
    # header_dict["datatype"] = dtype_dict[header_dict["datatype"]]

    return header_dict, wavelength_dict
