import os
import sys
import stackprinter


def find_presets_folder(root_dir):
    for dirpath, dirnames, _ in os.walk(root_dir):
        if "presets" in dirnames:
            return os.path.join(dirpath, "presets")

    print("No presets folder found.")
    return None  # Not found


REPO_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)  # Set REPO_DIR to the directory above test file

# changing working directory to the test folder so the paths in the exp files work
os.chdir(os.path.join(REPO_DIR, "tests"))

sys.path.append(os.path.join(REPO_DIR, "Application"))
import cameraapp
from MainWindow import MainWindow

SCRIPTS_FOLDER = os.path.join(REPO_DIR, "Application", "Scripts")
MASKS_FOLDER = os.path.join(REPO_DIR, "Application", 'Masks')
TEST_DATA_FOLDER = os.path.join(REPO_DIR, "tests", "test_data")

PRESETS_FOLDER = find_presets_folder(SCRIPTS_FOLDER)


if __name__ == "__main__":

    stackprinter.set_excepthook()

    rvs_app, splash = cameraapp.start_application(testing=True)
    cameraapp.start_logger(testing=True)

    main_window = MainWindow(SCRIPTS_FOLDER, MASKS_FOLDER, PRESETS_FOLDER, test_mode=True, test_dialog_timeout=3000)

    main_window.resize(1200, 800)
    main_window.show()

    # load experiment file
    main_window.open_experiment_directly(os.path.join(TEST_DATA_FOLDER, "experiment_files", "basil_test2.xp"))
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
