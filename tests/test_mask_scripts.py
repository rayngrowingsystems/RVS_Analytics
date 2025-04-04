import sys
import importlib.util
import os
import pytest
import datetime
from Experiment import Experiment
import json


REPO_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)  # Set REPO_DIR to the directory above test file

MASKS_FOLDER = os.path.normpath(os.path.join(REPO_DIR, "Application/Masks/RVS-A_mask_scripts"))
TEST_EXPERIMENT_PATH = os.path.normpath(os.path.join(REPO_DIR, "tests/test_data/experiment_files"))
TEST_DATA_OUT = os.path.normpath(os.path.join(REPO_DIR, "tests/test_data/analysis_results"))

EXCLUDED_DIRS = {
    ".git",
    ".idea",
    "tests",
    ".github",
    ".pytest_cache",
    ".ruff_cache",
}

# Find all script/config folders, **excluding hidden and test directories**
mask_dirs = [d for d in os.listdir(MASKS_FOLDER) if os.path.isdir(os.path.join(MASKS_FOLDER, d))
             and d not in EXCLUDED_DIRS]

mask_dict = {
    d: os.path.join(MASKS_FOLDER, d)
    for d in mask_dirs
}

exp_files = ["test_data/experiment_files/basil_test2.xp", "test_data/experiment_files/basil_test3.xp"]

now = datetime.datetime.now()
TEST_TIMESTAMP = now.strftime("%Y%m%d_%H%M%S")

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

    if not os.path.exists(settings["outputFolder"]["appData"]):
        os.mkdir(settings["outputFolder"]["appData"])
    if not os.path.exists(settings["outputFolder"]["appData"]):
        os.mkdir(settings["outputFolder"]["appData"])
    if not os.path.exists(settings["outputFolder"]["images"]):
        os.mkdir(settings["outputFolder"]["images"])
    if not os.path.exists(settings["outputFolder"]["visuals"]):
        os.mkdir(settings["outputFolder"]["visuals"])
    if not os.path.exists(settings["outputFolder"]["data"]):
        os.mkdir(settings["outputFolder"]["data"])

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


@pytest.mark.parametrize("mask_name, mask_folder_path",
                         [(name, path) for name, path in mask_dict.items()],
                         ids=[f"Mask: {mask_name}" for mask_name in mask_dict])
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
        print(mask_script_path)
        spec = importlib.util.spec_from_file_location(mask_name, mask_script_path)
        mask_script = importlib.util.module_from_spec(spec)
        sys.modules[mask_name] = mask_script
        spec.loader.exec_module(mask_script)

        print(test_experiment)

        settings = create_settings_from_experiment(test_experiment, TEST_TIMESTAMP)
        mask_options = extract_mask_settings(mask_config_path)
        settings["experimentSettings"]["analysis"]["maskOptions"] = mask_options
        print(settings)
        for image_path in os.listdir(settings["experimentSettings"]["folderFilePath"]):

            if os.path.isfile(image_path) and '.' not in image_path:
                settings["experimentSettings"]["inputImage"] = image_path
                mask_script.create_mask(settings, mask_preview=False)
