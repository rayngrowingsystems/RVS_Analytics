from os import path
import sys
import stackprinter
import time

from PIL.JpegPresets import presets

sys.path.append(path.join("../..", "Application"))

import cameraapp
from MainWindow import MainWindow

SCRIPTS_FOLDER = path.join("../..", "Application", "Scripts")
MASKS_FOLDER = path.join("../..", "Application", 'Masks')
PRESETS_FOLDER = path.join("../..", "Application", "Scripts/RVS-A_analysis_scripts/presets")
TEST_DATA_FOLDER = path.join("..", "test_data")

if __name__ == "__main__":

    stackprinter.set_excepthook()

    rvs_app, splash = cameraapp.start_application(testing=True)
    cameraapp.start_logger(testing=True)

    main_window = MainWindow(SCRIPTS_FOLDER, MASKS_FOLDER, PRESETS_FOLDER, test_mode=True, test_dialog_timeout=3000)

    main_window.resize(1200, 800)
    main_window.show()

    # load experiment file
    main_window.open_experiment_directly(path.join(TEST_DATA_FOLDER, "experiment_files", "basil_test2.xp"))
    rvs_app.processEvents()

    # open all UI dialogstes
    main_window.open_image_source_dialog()
    rvs_app.processEvents()
    main_window.open_image_option_dialog()

    main_window.open_image_roi_dialog()
    rvs_app.processEvents()

    main_window.open_image_mask_dialog()
    rvs_app.processEvents()

    main_window.open_analysis_options_dialog()
    rvs_app.processEvents()

    main_window.open_analysis_preview_dialog()
    rvs_app.processEvents()

    main_window.start_analysis(False, True, False)
    print("start_analysis returned")

    print("stopping")

    main_window.close()
    sys.exit(0)
