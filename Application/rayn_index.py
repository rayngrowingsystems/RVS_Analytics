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

import numpy as np
from plantcv.plantcv import warn
from plantcv.plantcv import Spectral_data
from plantcv.plantcv.transform import rescale
from plantcv.plantcv.hyperspectral import _find_closest


def rayn_ari(hsi, distance=20):
    """Anthocyanin Reflectance Index.

    ARI = (1 / R550) - (1 / R740)

    The theoretical range for ARI is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 700 and (float(hsi.min_wavelength) - distance) <= 550:
        r550_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 530)
        r740_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 740)
        r550 = (hsi.array_data[:, :, r550_index])
        r740 = (hsi.array_data[:, :, r740_index])
        with np.errstate(divide="ignore", invalid="ignore"):
            index_array_raw = (1 / r550) - (1 / r740)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="ARI")
    warn("Available wavelengths are not suitable for calculating ARI. Try increasing distance.")
    return None


def rayn_mcari(hsi, distance=20):
    """Modified Chlorophyll Absorption in Reflectance Index.

    MCARI = ((R740 - R670) - 0.2 * (R740 - R550)) * (R740 / R670)

    The theoretical range for MCARI is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 700 and (float(hsi.min_wavelength) - distance) <= 550:
        r550_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 550)
        r670_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        r740_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 740)
        r550 = (hsi.array_data[:, :, r550_index])
        r670 = (hsi.array_data[:, :, r670_index])
        r740 = (hsi.array_data[:, :, r740_index])
        # Naturally ranges from -inf to inf
        with np.errstate(divide="ignore", invalid="ignore"):
            index_array_raw = ((r740 - r670) - 0.2 * (r740 - r550)) * (r740 / r670)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="MCARI")
    warn("Available wavelengths are not suitable for calculating MCARI. Try increasing distance.")
    return None


def rayn_ci(hsi, distance=20):
    """Modified Chlorophyll Index.

    RAYN_CI = (R850 / R740) - 1

    The theoretical range for RAYN_CI is [-1.0, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 700:
        r740_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 740)
        r850_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 850)
        r740 = (hsi.array_data[:, :, r740_index])
        r850 = (hsi.array_data[:, :, r850_index])
        # Naturally ranges from -1 to inf
        with np.errstate(divide="ignore", invalid="ignore"):
            index_array_raw = (r850 / r740) - 1
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="CI")
    warn("Available wavelengths are not suitable for calculating RAYN_CI. Try increasing distance.")
    return None


def rayn_cri526(hsi, distance=20):
    """Carotenoid Reflectance Index 526.

    CRI526 = (1 / R500) - (1 / R526)

    The theoretical range for CRI526 is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 526 and (float(hsi.min_wavelength) - distance) <= 500:
        r500_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 500)
        r526_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 526)
        r500 = (hsi.array_data[:, :, r500_index])
        r526 = (hsi.array_data[:, :, r526_index])
        # Naturally ranges from -inf to inf
        with np.errstate(divide="ignore", invalid="ignore"):
            index_array_raw = (1 / r500) - (1 / r526)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="CRI526")
    warn("Available wavelengths are not suitable for calculating CRI526. Try increasing distance.")
    return None


def rayn_cri750(hsi, distance=20):
    """Carotenoid Reflectance Index 750.

    CRI750 = (1 / R510) - (1 / R750)

    The theoretical range for CRI750 is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 750 and (float(hsi.min_wavelength) - distance) <= 510:
        r510_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 510)
        r750_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 750)
        r510 = (hsi.array_data[:, :, r510_index])
        r750 = (hsi.array_data[:, :, r750_index])
        # Naturally ranges from -inf to inf
        with np.errstate(divide="ignore", invalid="ignore"):
            index_array_raw = (1 / r510) - (1 / r750)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="CRI750")
    warn("Available wavelengths are not suitable for calculating CRI750. Try increasing distance.")
    return None


def rayn_mari(hsi, distance=20):
    """Modified Anthocyanin Reflectance Index.

    MARI = ((1 / R526) - (1 / R740)) * R855

    The theoretical range for MARI is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 855 and (float(hsi.min_wavelength) - distance) <= 526:
        r526_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 526)
        r740_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 740)
        r855_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 855)
        r526 = (hsi.array_data[:, :, r526_index])
        r740 = (hsi.array_data[:, :, r740_index])
        r855 = (hsi.array_data[:, :, r855_index])
        # Naturally ranges from -inf to inf
        with np.errstate(divide="ignore", invalid="ignore"):
            index_array_raw = ((1 / r526) - (1 / r740)) * r855
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="MARI")
    warn("Available wavelengths are not suitable for calculating RAYN MARI. Try increasing distance.")
    return None


def rayn_ndre(hsi, distance=20):
    """Normalized Difference Red Edge.

    NDRE = (R855 - R740) / (R855 + R740)

    The theoretical range for NDRE is [-1.0, 1.0].

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 855 and (float(hsi.min_wavelength) - distance) <= 740:
        r740_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 740)
        r855_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 855)
        r855 = (hsi.array_data[:, :, r855_index])
        r740 = (hsi.array_data[:, :, r740_index])
        # Naturally ranges from -1 to 1
        with np.errstate(divide="ignore", invalid="ignore"):
            index_array_raw = (r855 - r740) / (r855 + r740)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="NDRE")
    warn("Available wavelengths are not suitable for calculating NDRE. Try increasing distance.")
    return None


def rayn_npci(hsi, distance=20):
    """Normalized Pigment Chlorophyll Index.

    NPCI = (R665 - R475) / (R665 + R475)

    The theoretical range for NPCI is [-1.0, 1.0].

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 665 and (float(hsi.min_wavelength) - distance) <= 475:
        r475_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 475)
        r665_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 665)
        r665 = (hsi.array_data[:, :, r665_index])
        r475 = (hsi.array_data[:, :, r475_index])
        # Naturally ranges from -1 to 1
        with np.errstate(divide="ignore", invalid="ignore"):
            index_array_raw = (r665 - r475) / (r665 + r475)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="NPCI")
    warn("Available wavelengths are not suitable for calculating NPCI. Try increasing distance.")
    return None


def rayn_wbi(hsi, distance=20):
    """Water Band Index.

    WI = R855 / R950

    The theoretical range for WBI is [0.0, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 950 and (float(hsi.min_wavelength) - distance) <= 855:
        r855_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 855)
        r950_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 950)
        r855 = (hsi.array_data[:, :, r855_index])
        r950 = (hsi.array_data[:, :, r950_index])
        # Naturally ranges from 0 to Inf
        with np.errstate(divide="ignore", invalid="ignore"):
            index_array_raw = r855 / r950
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="WBI")
    warn("Available wavelengths are not suitable for calculating WBI. Try increasing distance.")
    return None


def ci_green(hsi, distance=20):
    """Chlorophyll Index Green

    CI_GREEN = (R850 / R550) - 1

    The theoretical range for CI_GREEN is [-1.0, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 850 and (float(hsi.min_wavelength) - distance) <= 550:
        r550_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 550)
        r850_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 850)
        r550 = (hsi.array_data[:, :, r550_index])
        r850 = (hsi.array_data[:, :, r850_index])
        # Naturally ranges from -1 to inf
        with np.errstate(divide="ignore", invalid="ignore"):
            index_array_raw = (r850 / r550) - 1
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="CI_GREEN")
    warn("Available wavelengths are not suitable for calculating CI_GREEN. Try increasing distance.")
    return None


def _package_index(hsi, raw_index, method):
    """Private function to package raw index array as a Spectral_data object.
    Inputs:
    hsi       = hyperspectral data (Spectral_data object)
    raw_index = raw index array
    method    = index method (e.g. NDVI)

    Returns:
    index        = index image as a Spectral_data object.

    :params hsi: __main__.Spectral_data
    :params raw_index: np.array
    :params method: str
    :params index: __main__.Spectral_data
    """
    # Store debug mode

    # Resulting array is float 32 from varying natural ranges, transform into uint8 for plotting
    all_positive = np.add(raw_index, 2 * np.ones(np.shape(raw_index)))
    scaled = rescale(all_positive)

    # Find array min and max values
    obs_max_pixel = float(np.nanmax(raw_index))
    obs_min_pixel = float(np.nanmin(raw_index))

    index = Spectral_data(array_data=raw_index, max_wavelength=0,
                          min_wavelength=0, max_value=obs_max_pixel,
                          min_value=obs_min_pixel, d_type=np.uint8,
                          wavelength_dict={}, samples=hsi.samples,
                          lines=hsi.lines, interleave=hsi.interleave,
                          wavelength_units=hsi.wavelength_units,
                          array_type="index_" + method.lower(),
                          pseudo_rgb=scaled, filename=hsi.filename, default_bands=None,
                          metadata=hsi.metadata)

    return index
