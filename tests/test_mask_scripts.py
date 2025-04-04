import sys
import importlib.util
import os
import pytest
import datetime
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Application"))
from Experiment import Experiment


def find_mask_folders(base_dir, excluded_dirs=None):
    excluded_dirs = excluded_dirs or set()
    mask_dict = {}

    for dirpath, dirnames, filenames in os.walk(base_dir):
        folder_name = os.path.basename(dirpath)

        if folder_name in excluded_dirs:
            continue

        # Only include folders that contain files and no subfolders

        expected_py = f"{folder_name}.py"
        expected_config = f"{folder_name}.config"
        if expected_py in filenames or expected_config in filenames:
            mask_dict[folder_name] = dirpath

    return mask_dict


def create_settings_from_experiment(experiment_file, timestamp):
    experiment = Experiment(experiment_file)
    experiment.from_json()

    settings = dict()
    settings["experimentSettings"] = experiment.to_dict()
    settings["scriptName"] = experiment.selected_script

    base_folder = os.path.join(TEST_DATA_OUT, 'Analysis_' + str(timestamp))

    settings["outputFolder"] = {}
    settings["outputFolder"]["appData"] = os.path.join(base_folder)
    settings["outputFolder"]["images"] = os.path.join(base_folder, "images")
    settings["outputFolder"]["visuals"] = os.path.join(base_folder, "visuals")
    settings["outputFolder"]["data"] = os.path.join(base_folder, "rawData")

    os.makedirs(settings["outputFolder"]["appData"], exist_ok=True)
    os.makedirs(settings["outputFolder"]["appData"], exist_ok=True)
    os.makedirs(settings["outputFolder"]["images"], exist_ok=True)
    os.makedirs(settings["outputFolder"]["visuals"], exist_ok=True)
    os.makedirs(settings["outputFolder"]["data"], exist_ok=True)

    return settings


def convert_value(value):
    """Convert string values to appropriate Python types."""
    if isinstance(value, str):
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value
    return value


def extract_mask_settings(config_path):
    """Extract default settings from a .config file and wrap in full experimentSettings structure."""
    with open(config_path, "r") as f:
        config = json.load(f)

    mask_options_dict = {}

    try:
        sections = config["mask"]["options"]["sections"]
        for section in sections:
            for setting in section.get("settings", []):
                key = setting["name"]
                value = convert_value(setting.get("value"))
                mask_options_dict[key] = value
    except KeyError:
        raise ValueError(f"Invalid config format in {config_path}")

    # Wrap in full structure
    return mask_options_dict


REPO_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)  # Set REPO_DIR to the directory above test file

MASKS_FOLDER = os.path.join(REPO_DIR, "Application", "Masks")
TEST_DATA_FOLDER = os.path.join(REPO_DIR, "tests", "test_data")

TEST_EXPERIMENT_PATH = os.path.normpath(os.path.join(TEST_DATA_FOLDER, "experiment_files"))
TEST_DATA_OUT = os.path.normpath(os.path.join(TEST_DATA_FOLDER, "analysis_results"))

EXCLUDED_DIRS = {
    ".git",
    ".idea",
    "tests",
    ".github",
    ".pytest_cache",
    ".ruff_cache",
    "Installer",
    "packages"
}

exp_files = ["test_data/experiment_files/basil_test2.xp", "test_data/experiment_files/basil_test3.xp"]

now = datetime.datetime.now()
TEST_TIMESTAMP = now.strftime("%Y%m%d_%H%M%S")

mask_folders = find_mask_folders(MASKS_FOLDER, EXCLUDED_DIRS)
mask_list = [mask for mask in mask_folders]
print(f"Detected {len(mask_list)} valid mask folder: {mask_list}")


@pytest.mark.parametrize("mask_name, mask_folder_path",
                         [(name, path) for name, path in mask_folders.items()],
                         ids=[f"Mask: {mask_name}" for mask_name in mask_folders])
class TestMaskScripts:
    def test_script_files_exist(self, mask_name, mask_folder_path):
        """Test if the mask script file and the config file exists"""

        mask_script_path = os.path.join(mask_folder_path, f"{mask_name}.py")
        assert os.path.exists(mask_script_path), f"Script file missing: {mask_script_path}"

        mask_config_path = os.path.join(mask_folder_path, f"{mask_name}.config")
        assert os.path.exists(mask_config_path), f"Config file missing: {mask_config_path}"

    @pytest.mark.parametrize("test_experiment",
                             exp_files,
                             ids=[os.path.split(experiment)[-1] for experiment in exp_files])
    def test_mask_scripts(self, mask_name, mask_folder_path, test_experiment):
        """Test the mask scripts with default settings"""
        mask_script_path = os.path.join(mask_folder_path, f"{mask_name}.py")
        mask_config_path = os.path.join(mask_folder_path, f"{mask_name}.config")

        spec = importlib.util.spec_from_file_location(mask_name, mask_script_path)
        mask_script = importlib.util.module_from_spec(spec)
        sys.modules[mask_name] = mask_script
        spec.loader.exec_module(mask_script)

        settings = create_settings_from_experiment(test_experiment, TEST_TIMESTAMP)
        mask_options = extract_mask_settings(mask_config_path)
        settings["experimentSettings"]["analysis"]["maskOptions"] = mask_options

        print(settings["experimentSettings"]["folderFilePath"])
        for image_path in os.listdir(settings["experimentSettings"]["folderFilePath"]):

            if os.path.isfile(image_path) and '.' not in image_path:
                settings["experimentSettings"]["inputImage"] = image_path
                mask_script.create_mask(settings, mask_preview=False)
