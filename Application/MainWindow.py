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

# NOTE: The order of imports is important. When these were sorted by ruff, the application crashed in multiprocessing
# but only on Mac when running the application frozen by pyinstaller and running on an empty Mac account
# Do not sort the imports, keep them in this order for now

from os import path
import sys
import shutil
import tempfile

import datetime
import time as systime

import traceback
from multiprocessing import Queue

import importlib

import glob
import json
import os
import platform

import warnings

import csv

from importlib.metadata import version

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QDialog, QStyle, QMessageBox, QInputDialog, QLineEdit, QFileDialog, QLabel, QCheckBox
from PySide6.QtCore import QUrl, QTimer, QStandardPaths, QDir, QObject, QRunnable, QThreadPool, QSize
from PySide6 import QtCore
from PySide6.QtGui import QPixmap, QIcon, QScreen, QDesktopServices
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtNetwork import QNetworkInterface, QAbstractSocket

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from ImageSourceDialog import ImageSourceDialog
from ImageOptionDialog import ImageOptionDialog
from ImageMaskDialog import ImageMaskDialog
from ImageRoiDialog import ImageRoiDialog
from AnalysisPreviewDialog import AnalysisPreviewDialog
from AnalysisOptionsDialog import AnalysisOptionsDialog
from DownloadImagesDialog import DownloadImagesDialog
from DeleteImagesDialog import DeleteImagesDialog
from AboutDialog import AboutDialog
from HelpDialog import HelpDialog
from EulaDialog import EulaDialog
from CameraStartDialog import CameraStartDialog
from FolderStartDialog import FolderStartDialog
from SelectImageDialog import SelectImageDialog
from SettingsDialog import SettingsDialog

import Config
import Helper

from Helper import tprint

import CameraApp_rc

from ui_MainWindow import Ui_MainWindow

from Experiment import Experiment

from Camera import Camera

from CameraDiscovery import CameraDiscovery

from Mqtt import Mqtt

from Chart import Chart

from plantcv.parallel import process_results
from plantcv.utils.converters import json2csv

if platform.system() != "Darwin":
    import qdarktheme

if Config.profile_mode:
    from pyinstrument import Profiler

tprint("Loading MainWindow module", __name__)

class AnalysisWorkerSignals(QObject):
    '''
    Defines the signals available from the worker thread.
    '''
    status = QtCore.Signal(str, str)

class CameraDiscoveryWorkerSignals(QObject):
    '''
    Defines the signals available from the worker thread.
    '''
    add_camera = QtCore.Signal(str, str)
    remove_camera = QtCore.Signal(str)

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handle worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread.
    Supplied args and kwargs will be passed through to the runner.
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    '''

    def __init__(self, fn, signals, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = signals

    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # Retrieve args/kwargs here; and fire processing using them
        try:
            self.fn(*self.args, **self.kwargs)
        except BaseException:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            tprint("Exception", exctype, value)

class MyFileEventHandler(FileSystemEventHandler):
    def __init__(self, parent):
        super().__init__()

        self.main_window = parent

    def on_created(self, event):
        if Config.verbose_mode:
            tprint(f"{event.src_path} created")
        self.main_window.on_file_created(event.src_path)

    def on_deleted(self, event):
        if Config.verbose_mode:
            tprint(f"{event.src_path} deleted")
        self.main_window.on_file_deleted(event.src_path)

    # def on_modified(self, event):
    #    print(event, f"{event.src_path} modified")

    def on_moved(self, event):
        if Config.verbose_mode:
            tprint(f"{event.src_path} moved to {event.dest_path}")

class MainWindow(QMainWindow):
    add_status_text = QtCore.Signal(str)
    analysis_done = QtCore.Signal()
    add_preview_tab = QtCore.Signal(str, str)

    def __init__(self, script_folder, mask_folder, preset_folder, test_mode=False, test_dialog_timeout=3000):
        super().__init__()
        # super(MainWindow, self).__init__()

        self.CAMERA_STATUS_DIVIDER = 30

        tprint ("Qt version:", QtCore.__version_info__)

        tprint("Create MainWindow...")

        self.test_mode = test_mode
        self.test_dialog_timeout = test_dialog_timeout

        self.camera_configuration_view = None
        self.script_folder = script_folder
        self.mask_folder = mask_folder
        self.preset_folder = preset_folder

        # Set up the experiment folder path and create it if it doesn't exist
        documents_path = os.path.join(os.path.normpath(
                                      QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)),
                                      QApplication.organizationName(), QApplication.applicationName())

        self.experiment_folder = os.path.join(documents_path, 'Experiments')
        QDir().mkpath(self.experiment_folder)
        tprint("Experiment folder", self.experiment_folder)

        # Set up the experiment file path
        self.experiment_file_name = os.path.join(documents_path, 'analysis.xp')

        self.current_experiment_file = ""
        self.current_analysis_file = ""

        self.analysis_worker = None
        self.analysis_running = False

        self.camera_discovery_worker = None

        self.file_system_event_handler = None

        self.experiment_dirty = False
        self.analysis_dirty = False

        self.experiment = Experiment(self.experiment_file_name)

        self.experiment.from_json()

        # qdarktheme.setup_theme(self.experiment.theme)  # Mac crashes if it is run here

        # Set up RVS path and check for EULA acceptance
        self.rvs_path = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)

        if not path.exists(os.path.join(self.rvs_path, ".rvs")):
            self.open_eula_dialog()

        self.camera = None
        self.camera_status_divider = self.CAMERA_STATUS_DIVIDER

        # Need to configure NIC?
        if self.experiment.camera_discovery_ip == "" and not self.test_mode:
            self.select_network()

        # Set up background processing of images
        self.threadpool = QThreadPool()
        tprint("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.camera_discovery = None

        # Set up camera discovery as a background worker thread
        # Any other args, kwargs are passed to the run function
        self.camera_discovery_worker = Worker(self.camera_discovery_function, CameraDiscoveryWorkerSignals(),
                                              self, self.experiment.camera_discovery_ip)
        self.camera_discovery_worker.signals.add_camera.connect(self.on_camera_discovery_add_camera)
        self.camera_discovery_worker.signals.remove_camera.connect(self.on_camera_discovery_remove_camera)

        self.stop_camera_discovery_worker = False
        self.stop_analysis_worker = False

        # Start the camera discovery thread
        self.threadpool.start(self.camera_discovery_worker)

        # Set up the current session file path
        self.current_session_file_name = os.path.join(documents_path, 'currentSession.json')
        self.current_session = {}

        self.current_image_timestamp = ""

        # Set up dictionaries for script and mask paths
        self.script_paths = {}
        self.mask_paths = {}

        self.cameras = {}

        self.charts = {}

        self.help_dialog = None

        self.load_ui()

        self.refresh_window_title()
        if platform.system() == "Windows":
            self.setWindowIcon(QIcon(":/images/Syrcadia.ico"))
        elif platform.system() == "Darwin":
            self.setWindowIcon(QIcon(":/images/Syrcadia.icns"))

        # Connect buttons to their respective slot
        self.ui.image_source_button.clicked.connect(self.open_image_source_dialog)
        self.ui.image_option_button.clicked.connect(self.open_image_option_dialog)
        self.ui.image_mask_button.clicked.connect(self.open_image_mask_dialog)
        self.ui.image_roi_button.clicked.connect(self.open_image_roi_dialog)
        self.ui.analysis_preview_button.clicked.connect(self.open_analysis_preview_dialog)
        self.ui.analysis_options_button.clicked.connect(self.open_analysis_options_dialog)
        self.ui.results_button.clicked.connect(self.show_results)

        # Set-up Play button
        self.ui.play_button.clicked.connect(self.play)
        self.ui.play_button.setCheckable(True)
        self.ui.play_button.setIcon(QIcon(":/images/Play.png"))
        self.ui.play_button.setIconSize(QSize(20, 20))
        self.ui.play_button.setFixedSize(40, 40)

        # Set-up Stop button
        self.ui.stop_button.clicked.connect(self.stop)
        self.ui.stop_button.setCheckable(True)
        self.ui.stop_button.setIcon(QIcon(":/images/Stop.png"))
        self.ui.stop_button.setIconSize(QSize(18, 18))
        self.ui.stop_button.setFixedSize(40, 40)

        self.ui.clear_sessiondata_button.clicked.connect(self.clear_sessiondata)

        # Set-up the items in the Experiment menu
        self.ui.action_new_experiment.triggered.connect(self.new_experiment)
        self.ui.action_open_experiment.triggered.connect(self.open_experiment)
        self.ui.action_save_experiment.triggered.connect(self.save_experiment)
        self.ui.action_save_as_experiment.triggered.connect(self.save_as_experiment)

        # Set-up the items in the Analysis menu
        self.ui.action_new_analysis.triggered.connect(self.new_analysis)
        self.ui.action_open_analysis.triggered.connect(self.open_analysis)
        self.ui.action_save_analysis.triggered.connect(self.save_analysis)
        self.ui.action_save_as_analysis.triggered.connect(self.save_as_analysis)

        # Set-up various buttons and commands
        self.ui.action_select_network.triggered.connect(self.select_network)

        self.ui.action_download_images.triggered.connect(self.open_download_images_dialog)
        self.ui.action_delete_images.triggered.connect(self.open_delete_images_dialog)

        self.ui.action_settings.triggered.connect(self.open_settings_dialog)

        self.ui.action_about.triggered.connect(self.open_about_dialog)
        self.ui.action_help.triggered.connect(self.open_help_dialog)

        self.display_instructions()

        # Make sure text is scrolled up to reveal last line
        self.ui.scrollArea.verticalScrollBar().rangeChanged.connect(self.on_scrollbar_range_changed)

        # Populate analysis script selection combobox
        self.ui.script_selection_combobox.clear()

        # Official and user scripts: Collect all .py files in the scripts folder tree
        file_list = self.python_files_in_tree([self.script_folder, os.path.join(documents_path, "Scripts")])

        sorted_file_list = sorted(file_list)  # Sort and add to the combobox
        for f in sorted_file_list:
            full_script_file = f
            base_script_file = os.path.basename(full_script_file)
            self.ui.script_selection_combobox.addItem(base_script_file)
            self.script_paths[base_script_file] = full_script_file

        # Populate mask selection combobox
        self.ui.mask_selection_combobox.clear()
        self.ui.mask_selection_combobox.addItem("Default")

        # Official and user masks: Collect all .py files in the mask folder tree
        file_list = self.python_files_in_tree([self.mask_folder, os.path.join(documents_path, "Masks")])

        sorted_file_list = sorted(file_list)  # Sort and add to the combobox
        for f in sorted_file_list:
            full_mask_file = f
            base_mask_file = os.path.basename(full_mask_file)
            self.ui.mask_selection_combobox.addItem(base_mask_file)
            self.mask_paths[base_mask_file] = full_mask_file

        tprint("Script paths:", self.script_paths)
        tprint("Mask paths:", self.mask_paths)

        # Find related combobox indexes for script and mask
        script_index = self.ui.script_selection_combobox.findText(self.experiment.selected_script)
        if script_index != -1:
            self.ui.script_selection_combobox.setCurrentIndex(script_index)

        if self.experiment.selected_script == "" or self.experiment.selected_script not in self.script_paths:
            self.experiment.selected_script = self.ui.script_selection_combobox.currentText() # Pick the first one

        mask_index = self.ui.mask_selection_combobox.findText(self.experiment.selected_mask)
        if mask_index != -1:
            self.ui.mask_selection_combobox.setCurrentIndex(mask_index)

        self.ui.script_selection_combobox.currentIndexChanged.connect(self.script_selection_changed)
        self.ui.mask_selection_combobox.currentIndexChanged.connect(self.mask_selection_changed)

        # self.experiment.script_options = self.defaultScriptOptions()

        # Use thread safe signal/slot to allow use from the background thread
        self.analysis_done.connect(self.on_analysis_done)
        self.add_status_text.connect(self.on_add_status_text)
        self.add_preview_tab.connect(self.on_add_preview_tab)

        # If ongoing analysis, continue
        if path.exists(self.current_session_file_name) and not self.test_mode:
            self.resume_analysis()

        self.ui.statusbar.hide()

        # Create tick timer
        timer = QTimer(self)
        timer.timeout.connect(self.tick)
        timer.start(1000)

        # Watch folder for changes
        self.file_system_event_handler = MyFileEventHandler(self)

        self.file_system_observer = None

        if self.experiment.image_source is self.experiment.ImageSource.Folder:
            self.watch_folder(self.experiment.folder_file_path)
        elif self.experiment.image_source is self.experiment.ImageSource.Camera:
            self.watch_folder(self.experiment.camera_file_path)

        self.images_added = False

        # If broker defined, start MQTT
        if self.experiment.mqtt_broker != "":
            self.start_mqtt()
        else:
            self.mqtt = None
            self.on_mqtt_status_changed("No broker defined", True)

        self.refresh_camera_selection()

        self.refresh_image_source_text()

        self.refresh_play_button_status()
        self.refresh_ready_to_play()

        self.current_camera_name = ""
        self.current_file_name = ""

        # fakeCamera = {'cid': 'c250b4fd-4d6a-5567-81e3-3034f8b88bae', 'model': 'RVS',
        # 'modelName': 'Rayn Vision System', 'name': 'RaynCam-2218AE',
        # 'version': {'main': '1.0.0.11'}, 'tags': {'disc': {'tagVer': '1.0', 'interval': 10000,
        # 'ipv4': '192.168.0.27', 'port': 80}}}
        # self.cameras['c250b4fd-4d6a-5567-81e3-3034f8b88bae'] = fakeCamera

        # Redirect warnings messages to the UI
        warnings.showwarning = self.mywarning

    def __del__(self):
        print("Destructor")

    def closeEvent(self, event):  # Qt override, keep casing
        tprint("CloseEvent")

        self.hide()

        # Ask threads to stop
        self.stop_camera_discovery_worker = True
        self.stop_analysis_worker = True

        # Wait for threads to actually stop
        self.threadpool.waitForDone()

        QMainWindow.closeEvent(self, event)

    def resizeEvent(self, event):  # Qt override, keep casing
        self.refresh_image_preview_size()

        QMainWindow.resizeEvent(self, event)

    def load_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


    def python_files_in_tree(self, folders):
        file_list = []

        for folder in folders:
            for root, dirs, files in os.walk(folder):  # Collect all .py files in the scripts folder tree
                if "tests" in dirs:
                    dirs.remove("tests")  # Skip the tests folder

                for f in files:
                    if f.endswith(".py"):
                        file_list.append(os.path.join(root, f))

        return file_list

    def camera_discovery_function(self, main_window, ip):
        tprint("Camera: Starting cameraDiscoveryFunction:", ip)

        CameraDiscovery(ip, main_window) #, main_window.camera_discovery_feedback_queue)

        # Note: This function will never return

    def script_runner(self, script_name, file_names, settings, mask_file_name):
        tprint("Starting script_runner. Script:", script_name, "Filenames:", file_names,
               "Settings", settings, "Mask:", mask_file_name)

        analysis_script = importlib.import_module(script_name)

        progress = 0

        for file_name in file_names:
            tprint("Analysis: Processing file:", file_name)

            d, t, camera, wavelength = Helper.info_from_header_file(file_name)

            tprint("Analysis: Info from HDR file: Camera:", camera, "Date/time:", d, t)

            # capture date = 2022-12-16
            # capture time = 07:00:00

            self.analysis_worker.signals.status.emit("timestamp", d + ' ' + t)
            # feedback_queue.put([script_name, "timestamp", date + ' ' + time])

            self.analysis_worker.signals.status.emit("cameraName", camera)
            # feedback_queue.put([script_name, "cameraName", camera])

            self.analysis_worker.signals.status.emit("fileName", file_name)
            # feedback_queue.put([script_name, "fileName", file_name])

            settings["inputImage"] = file_name  # Set image specific setting on top of basic settings

            if Config.verbose_mode:
                tprint("Settings:", settings)

            tprint("ScriptRunner:", mask_file_name)

            # feedback_queue = Queue()

            try:
                if Config.profile_mode:
                    profiler = Profiler(interval=0.0001)
                    profiler.start()

                # Make sure we get the latest data
                settings["experimentSettings"]["sessionData"] = self.experiment.session_data

                return_list = analysis_script.execute(script_name, settings, mask_file_name)

                for command, value in return_list:
                    # self.analysis_worker.signals.status.emit(command, value)
                    tprint("---> handle_script_feedback", command, value)
                    self.handle_script_feedback(command, value)

                if Config.profile_mode:
                    profiler.stop()
                    profiler.print()

            except RuntimeError as err:
                tprint("RuntimeError in script:", err)
                self.analysis_worker.signals.status.emit("error", str(err))
                # feedback_queue.put([script_name, "error", str(err)])

            # Update progress
            self.analysis_worker.signals.status.emit("progress", str(progress))  # Make sure progressbar is updated
            # feedback_queue.put([script_name, "progress", progress])  # Make sure progressbar is updated
            progress = progress + 1

            if self.stop_analysis_worker:
                return

        tprint("Analysis: ScriptRunner: No more files to analyze")
        self.analysis_worker.signals.status.emit("done", "")  # Make sure progressbar is updated
        # feedback_queue.put([script_name, "done"])

    def on_script_runner_status(self, command, value):
        tprint("---> script_runner_status", command, value)
        self.handle_script_feedback(command, value)

    def on_camera_discovery_add_camera(self, cid, camera):
        tprint("Camera: Discovery: addCamera")

        if cid not in self.cameras:
            self.cameras[cid] = json.loads(camera)

            if len(self.cameras) == 1:  # Auto-select if it is the first one
                self.experiment.camera_cid = cid
                self.update_experiment_file(False)

            self.refresh_camera_selection()

    def on_camera_discovery_remove_camera(self, cid):
        tprint("Camera: Discovery: removeCamera")

        if cid == self.experiment.camera_cid:
            self.camera = None

        if cid in self.cameras:
            del self.cameras[cid]
            self.refresh_camera_selection()

    def update_experiment_file(self, analysis_dirty):
        self.experiment.update_experiment_file()
        self.experiment_dirty = True

        if analysis_dirty:
            self.analysis_dirty = True

    def start_mqtt(self):
        self.on_mqtt_status_changed("", False)
        QApplication.instance().processEvents()

        self.mqtt = Mqtt(self.experiment.mqtt_broker, int(self.experiment.mqtt_port), self.experiment.mqtt_username,
                         self.experiment.mqtt_password)
        self.mqtt.status_changed.connect(self.on_mqtt_status_changed)
        self.mqtt.start()

    def refresh_window_title(self):
        text = "RAYN Vision System " + AboutDialog.version_number() + " - " + self.current_experiment_file \
            + " - " + self.current_analysis_file
        text = text + f"(PlantCV: {version('plantCV')})"
        self.setWindowTitle(text)

    def display_instructions(self):
        self.ui.image_preview.setText(("1. Select image source<br>"
                                       "2. Select experiment options, like Regions<br>"
                                       "3. Select Masking and Options for the analysis script<br>"
                                       "4. Run analysis"))

    def mywarning(self, message, category, filename, lineno, file=None, line=None):
        tprint(message, category)
        self.add_status_text.emit("Warning: " + str(message))

    def all_ip_addresses(self):
        nic_list = []
        nics = QNetworkInterface.allInterfaces()

        for nic in nics:
            flags = nic.flags()
            is_loopback = bool(flags & QNetworkInterface.IsLoopBack)
            is_up = bool(flags & QNetworkInterface.IsUp)
            can_multicast = bool(flags & QNetworkInterface.CanMulticast)

            if is_up and can_multicast and not is_loopback:
                entries = nic.addressEntries()

                for entry in entries:
                    if entry.ip().protocol() == QAbstractSocket.IPv4Protocol:
                        nic_list.append(nic.humanReadableName() + " (" + entry.ip().toString() + ")")

        return nic_list

    def select_network(self):
        items = self.all_ip_addresses()
        item, ok = QInputDialog.getItem(self, "Select network interface", "Network", items)
        if ok and item != "":
            ip = item[item.find("(") + 1:item.find(")")]
            if self.experiment.camera_discovery_ip != ip:
                change_existing = (self.experiment.camera_discovery_ip != "")
                self.experiment.camera_discovery_ip = ip

                if change_existing: # This is a change, not selecting the network on first startup
                    tprint("Network changed:", ip)

                    if self.camera_discovery:
                        tprint("Camera: Change discovery IP:", self.experiment.camera_discovery_ip)

                        self.camera_discovery.change_ip_address(self.experiment.camera_discovery_ip)
                    else:
                        tprint("Camera: cameraDiscovery is None. Cannot change ip")

                self.update_experiment_file(False)

    def refresh_comboboxes(self):
        script_index = self.ui.script_selection_combobox.findText(self.experiment.selected_script)
        if script_index != -1:
            self.ui.script_selection_combobox.setCurrentIndex(script_index)

        mask_index = self.ui.mask_selection_combobox.findText(self.experiment.selected_mask)
        if mask_index != -1:
            self.ui.mask_selection_combobox.setCurrentIndex(mask_index)

    def refresh_experiment(self):
        self.experiment = Experiment(self.experiment_file_name)

        if path.exists(self.experiment_file_name):
            self.experiment.from_json()

        self.ui.status_text.setText("")
        self.ui.timestamp_label.setText("")
        self.ui.image_preview.setPixmap(QPixmap())

        self.refresh_image_source_text()

        self.refresh_comboboxes()

        self.refresh_window_title()

    def save_experiment_first(self):
        if QMessageBox.question(self, "Unsaved changes",
                "Do you want to save changes to the experiment first?") == QMessageBox.StandardButton.Yes:
            return True

        return False

    def save_analysis_first(self):
        if QMessageBox.question(self, "Unsaved changes",
                "Do you want to save changes to the analysis first?") == QMessageBox.StandardButton.Yes:
            return True

        return False

    def new_experiment(self):
        tprint("New experiment")

        if self.experiment_dirty:
            if self.save_experiment_first():
                self.save_experiment()
                return

        if path.exists(self.experiment_file_name):
            os.remove(self.experiment_file_name)

        self.current_experiment_file = ""
        self.refresh_experiment()

        self.remove_result_tabs()

        self.ui.script_selection_combobox.setCurrentIndex(0)
        self.ui.mask_selection_combobox.setCurrentIndex(0)

        self.script_selection_changed(0)
        self.mask_selection_changed(0)

        self.refresh_play_button_status()
        self.refresh_ready_to_play()

        self.display_instructions()

        self.experiment_dirty = False

        tprint("Selected first", self.experiment.selected_script)

    def open_experiment_directly(self, file_name):
        if path.exists(file_name):
            if path.exists(self.experiment_file_name):
                os.remove(self.experiment_file_name)

            shutil.copy2(file_name, self.experiment_file_name)

            self.current_experiment_file = file_name
            self.refresh_experiment()

            self.remove_result_tabs()

            self.refresh_play_button_status()
            self.refresh_ready_to_play()

            self.experiment_dirty = False
        else:
            tprint("File does not exist:", file_name)

    def open_experiment(self):
        tprint("Open experiment")

        if self.experiment_dirty:
            if self.save_experiment_first():
                self.save_experiment()
                return

        file_name, filter = QFileDialog.getOpenFileName(self, "Open experiment", self.experiment_folder,
                                                        "Experiment Files (*.xp)")

        if file_name != "":
            self.open_experiment_directly(file_name)

    def save_experiment(self):
        tprint("Save experiment", self.current_experiment_file)

        if self.current_experiment_file == "":
            self.save_as_experiment()
        else:
            if path.exists(self.current_experiment_file):
                os.remove(self.current_experiment_file)

            shutil.copy2(self.experiment_file_name, self.current_experiment_file)

            self.experiment_dirty = False

    def save_as_experiment_directly(self, file_name):
        shutil.copy2(self.experiment_file_name, file_name)

        self.current_experiment_file = file_name
        self.refresh_window_title()

        self.experiment_dirty = False

    def save_as_experiment(self):
        tprint("Save As experiment")
        file_name, filter = QFileDialog.getSaveFileName(self, "Save experiment", self.experiment_folder,
                                                        "Experiment Files (*.xp)")

        if file_name != "":
            self.save_as_experiment_directly(file_name)

    def new_analysis(self):
        tprint("New analysis")

        if self.analysis_dirty:
            if self.save_analysis_first():
                self.save_analysis()
                return

        self.current_analysis_file = ""
        self.refresh_window_title()

        self.experiment.clear_analysis()

        self.remove_result_tabs()

        self.ui.script_selection_combobox.setCurrentIndex(0)
        self.ui.mask_selection_combobox.setCurrentIndex(0)

        self.script_selection_changed(0)
        self.mask_selection_changed(0)

        self.refresh_play_button_status()
        self.refresh_ready_to_play()

        self.analysis_dirty = False

    def open_analysis_directly(self, file_name):
        with open(file_name, 'r') as f:
            j = f.read()
            d = json.loads(j)

            self.experiment.from_dict(d)  # An analysis file is just the "analysis" section of the experiment file

        self.current_analysis_file = file_name
        self.refresh_window_title()

        self.remove_result_tabs()

        # self.refreshAnalysis() # TODO?
        self.refresh_comboboxes()

        self.refresh_play_button_status()
        self.refresh_ready_to_play()

        self.analysis_dirty = False

    def open_analysis(self):
        tprint("Open analysis")

        if self.analysis_dirty:
            if self.save_analysis_first():
                self.save_analysis()
                return

        file_name, filter = QFileDialog.getOpenFileName(self, "Open analysis", self.experiment_folder,
                                                        "Analysis Files (*.af)")

        if file_name != "":
            self.open_analysis_directly(file_name)

    def save_analysis(self):
        tprint("Save analysis")

        if self.current_analysis_file == "":
            self.save_as_analysis()
        else:
            d = self.experiment.analysis_to_dict()

            j = json.dumps(d, indent=4)

            with open(self.current_analysis_file, 'w') as f:
                f.write(j)

            self.current_analysis_file = self.current_analysis_file
            self.refresh_window_title()

        self.analysis_dirty = False

    def save_as_analysis_directly(self, file_name):
        d = self.experiment.analysis_to_dict()

        j = json.dumps(d, indent=4)

        with open(file_name, 'w') as f:
            f.write(j)

        self.current_analysis_file = file_name
        self.refresh_window_title()

        self.analysis_dirty = False

    def save_as_analysis(self):
        tprint("Save As analysis")

        file_name, filter = QFileDialog.getSaveFileName(self, "Save analysis", self.experiment_folder,
                                                        "Analysis Files (*.af)")

        if file_name != "":
            self.save_as_analysis_directly(file_name)

    def default_script_options(self):
        if self.experiment.selected_script != "":
            config_file_name = self.script_paths[self.experiment.selected_script].replace(".py", ".config")

            # tprint("Config:", configFileName)

            script_options = {}

            with open(config_file_name) as config_file:
                data = json.load(config_file)
                for option in data['script']['options']:
                    if option["type"] == "slider":
                        script_options[option["name"]] = int(option["value"])
                    elif option["type"] == "checkBox":
                        script_options[option["name"]] = (option["value"] == "true")
                    elif option["type"] == "dropdown":
                        script_options[option["name"]] = ''

            tprint("Set default script options:", os.path.basename(config_file_name), script_options)

            return script_options

        return {}

    def camera_display_names(self):
        results = []
        for cid, camera in self.cameras.items():
            results.append(camera["name"] + " (" + camera["tags"]["disc"]["ipv4"] + ")")

        return results

    def refresh_camera_selection(self):
        index = 0
        for cid, camera_json in self.cameras.items():
            if cid == self.experiment.camera_cid:
                self.camera_selection_changed(index)
                break

            index = index + 1

    def camera_selection_changed(self, index):
        cameras = []
        for cid, camera_json in self.cameras.items():
            cameras.append(camera_json['name'])
        tprint("Camera: cameraSelectionChanged: New index:", index, "Cameras:", cameras)

        item = 0
        for cid, camera_json in self.cameras.items():
            if item == index:
                self.experiment.camera_cid = cid

                tprint("Camera: New selected camera:", cid)

                if self.camera:
                    del self.camera
                    self.camera = None

                self.camera = Camera(self, camera_json["tags"]["disc"]["ipv4"])

                if cid in self.experiment.camera_api_keys:
                    self.camera.set_api_key(self.experiment.camera_api_keys[cid])

                self.refresh_image_source_text()

                self.ui.camera_status.setText("")

                self.update_experiment_file(False)

                break

            item = item + 1

    def camera_api_key_changed(self, text):
        self.experiment.camera_api_key = text

        self.camera.set_api_key(text)

        self.experiment.camera_api_keys[self.experiment.camera_cid] = text

        self.update_experiment_file(False)

    def configure_camera(self, index):
        tprint("ConfigureCamera:", index)

        self.camera_configuration_view = QWidget()
        vbox = QVBoxLayout(self.camera_configuration_view)
        vbox.setContentsMargins(0, 0, 0, 0)

        camera_ip = None
        camera_name = ""

        item = 0
        for cid, camera in self.cameras.items():
            if item == index:
                camera_ip = camera["tags"]["disc"]["ipv4"]
                camera_name = camera["name"]
                break

            item = item + 1

        tprint("Camera:", camera_ip, camera_name)

        if camera_ip is not None:
            webEngineView = QWebEngineView()
            webEngineView.load(QUrl("http://" + camera_ip + "/setup"))

            vbox.addWidget(webEngineView)

            self.camera_configuration_view.setLayout(vbox)

            self.camera_configuration_view.setGeometry(0, 0, 800, 600)

            # Center it
            center_point = QScreen.availableGeometry(QApplication.primaryScreen()).center()
            fg = self.camera_configuration_view.frameGeometry()
            fg.moveCenter(center_point)
            self.camera_configuration_view.move(fg.topLeft())

            self.camera_configuration_view.setWindowTitle('Configure camera: ' + camera_name + " (" + camera_ip + ")")
            self.camera_configuration_view.show()

    def on_mqtt_status_changed(self, message, error):
        if error :
            color = "#500"
        else:
            color = "#060"
        self.ui.mqtt_status.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.ui.mqtt_status.setStyleSheet('color: #fff; background-color: ' + color)

        if message != "":
            self.ui.mqtt_status.setText(" MQTT: " + message + " ")
        else:
            self.ui.mqtt_status.setText("")

    def on_scrollbar_range_changed(self):
        self.ui.scrollArea.verticalScrollBar().setValue(self.ui.scrollArea.verticalScrollBar().maximum())

    def on_file_created(self, file_name):
        if Config.verbose_mode:
            tprint("onFileCreated:", file_name)

        self.images_added = True

    def on_file_deleted(self, file_name):
        if Config.verbose_mode:
            tprint("onFileDeleted:", file_name)

    def refresh_image_source_text(self):
        if self.experiment.image_source is self.experiment.ImageSource.Image:
            self.ui.image_source.setText("<b>Image source:</b> Image: " + self.experiment.image_file_path)
        elif self.experiment.image_source is self.experiment.ImageSource.Folder:
            self.ui.image_source.setText("<b>Image source:</b> Folder: " + self.experiment.folder_file_path)
        else:
            if self.experiment.camera_cid in self.cameras:
                name = self.cameras[self.experiment.camera_cid]["name"]
                ip = self.cameras[self.experiment.camera_cid]["tags"]["disc"]["ipv4"]
                self.ui.image_source.setText("<b>Image source:</b> Camera: " + name + " " + ip + " Target folder: "
                                             + self.experiment.camera_file_path)
            else:
                self.ui.image_source.setText("<b>Image source:</b> No source specified")

    def set_image_source(self, image_source):
        self.experiment.image_source = image_source

        if self.experiment.image_source is self.experiment.ImageSource.Folder:
            self.watch_folder(self.experiment.folder_file_path)
        elif self.experiment.image_source is self.experiment.ImageSource.Camera:
            self.watch_folder(self.experiment.camera_file_path)

        self.update_experiment_file(False)

        self.refresh_image_source_text()

    def set_image_file_path(self, location):
        location = os.path.normpath(location)

        self.experiment.image_file_path = location
        self.update_experiment_file(False)

        self.refresh_image_source_text()

    def set_folder_file_path(self, location):
        location = os.path.normpath(location)

        self.experiment.folder_file_path = location
        self.update_experiment_file(False)

        if self.experiment.image_source is self.experiment.ImageSource.Folder:
            self.watch_folder(location)

        self.refresh_image_source_text()

    def set_camera_file_path(self, location):
        location = os.path.normpath(location)

        self.experiment.camera_file_path = location
        self.update_experiment_file(False)

        if self.experiment.image_source is self.experiment.ImageSource.Camera:
            self.watch_folder(location)

        self.refresh_image_source_text()

    def set_output_file_path(self, location):
        location = os.path.normpath(location)

        self.experiment.output_file_path = location
        self.update_experiment_file(False)

    def script_selection_changed(self, index):
        self.experiment.selected_script = self.ui.script_selection_combobox.currentText()
        tprint("Selected script changed:", self.experiment.selected_script)

        if self.experiment.selected_script != "":
            if self.experiment.selected_script in self.script_paths:
                config_file_name = self.script_paths[self.experiment.selected_script].replace(".py", ".config")

                with open(config_file_name) as config_file:
                    data = json.load(config_file)
                    tprint("Selection changed:", os.path.basename(config_file_name), data)

                    # Refresh script options
                    self.experiment.script_options = {}  # self.defaultScriptOptions()

        self.update_experiment_file(False)

        self.refresh_ready_to_play()

    def mask_selection_changed(self, index):
        self.experiment.selected_mask = self.ui.mask_selection_combobox.currentText()
        tprint("Selected mask changed:", self.experiment.selected_mask)

        self.experiment.mask_defined = False  # Force mask settings to be updated

        self.update_experiment_file(False)

        self.refresh_ready_to_play()

    def stop_watcher(self):
        # Remove existing one
        if self.file_system_observer is not None:
            self.file_system_observer.unschedule_all()
            self.file_system_observer.stop()
            self.file_system_observer.join()

    def watch_folder(self, folder):
        self.stop_watcher()

        if folder != "":
            folder = os.path.normpath(folder)

            if os.path.exists(folder):
                # Set up new observer for the new path
                tprint("Image folder to watch:", folder)

                self.file_system_observer = Observer()

                self.file_system_observer.schedule(self.file_system_event_handler, folder, recursive=True)

                self.file_system_observer.start()
            else:
                self.file_system_observer = None

        self.images_added = False

    def on_analysis_done(self):
        tprint("Analysis: Done")

        if self.experiment.image_source is self.experiment.ImageSource.Image:
            self.add_status_text.emit("Image processed")

            self.stop_analysis(False)
        elif self.experiment.image_source is self.experiment.ImageSource.Folder:
            self.add_status_text.emit("All images processed")

            self.stop_analysis(False)
        elif self.experiment.image_source is self.experiment.ImageSource.Camera:
            self.add_status_text.emit("Waiting for new images...")

            self.ui.image_preview_progressbar.setValue(self.ui.image_preview_progressbar.maximum())

    def tick(self):
        # tprint("Tick")

        if self.camera is not None:
            self.camera.tick()

        # Poll camera status
        if self.camera is not None and self.experiment.image_source is self.experiment.ImageSource.Camera:
            if self.camera_status_divider == 0:
                status = self.camera.get_status()

                if status is not None:
                    # tprint("Camera status", status["sdCard"]["freeSpace"])

                    free_space = status["sdCard"]["freeSpace"]

                    if free_space < 10:
                        self.ui.camera_status.setText("Camera Status: <b><font color=\"#F00\" size=\"5\">Free space: " +
                                                      str(free_space) + "%</font></b>")
                    else:
                        self.ui.camera_status.setText("Camera Status: Free space: " + str(free_space) + "%")

                self.camera_status_divider = self.CAMERA_STATUS_DIVIDER
            else:
                self.camera_status_divider = self.camera_status_divider - 1

    def tab_exists(self, tab_name):
        found = False
        for index in range(self.ui.tab_widget.count()):
            if self.ui.tab_widget.tabText(index) == tab_name:
                found = True

        return found

    def tab_widget(self, tab_name):
        for index in range(self.ui.tab_widget.count()):
            if self.ui.tab_widget.tabText(index) == tab_name:
                return self.ui.tab_widget.widget(index)

        return None

    def handle_script_feedback(self, command, value):
        handled = False

        # From scriptRunner process: # For each file
        if command == "timestamp":  # <timestamp>
            self.ui.timestamp_label.setText("Timestamp: " + value)
            self.current_image_timestamp = value
            handled = True

        if command == "progress":  # <percent>
            self.ui.image_preview_progressbar.setValue(int(value))
            handled = True

        if command == "cameraName":  # <cameraName>
            self.current_camera_name = value
            handled = True

        if command == "fileName":  # <fileName>
            # Update current session
            processed_images = []
            if "processedImages" in self.current_session:
                processed_images = self.current_session["processedImages"]

            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            processed_images.append({"image": os.path.normpath(value), "processedAt": timestamp})

            self.current_session["processedImages"] = processed_images

            self.update_current_session_file()
            self.current_file_name = value
            handled = True

        # From scriptRunner process: when all files have been processed
        if command == "done":
            self.analysis_done.emit()

            handled = True

        # From analysis script
        if command == "preview":  # Pseudo RGB: <fileName>
            # width = self.ui.image_preview.width() - 4
            # height = self.ui.image_preview.height() - 4

            # self.ui.image_preview.setPixmap(QPixmap(value).scaled(width, height, QtCore.Qt.KeepAspectRatio))
            self.ui.image_preview.setPixmap(QPixmap(value))

            self.refresh_image_preview_size()

            self.ui.image_preview.setText("")
            handled = True

        if command == "spectral_hist":
            self.add_preview_tab.emit("Spectral Histogram", value)
            handled = True

        if command.startswith("image"):
            index = command.replace("image_", "").replace("_", " ")
            index = index.capitalize()
            self.add_preview_tab.emit(f"{index}", value)
            handled = True

        if command.startswith("index_hist"):
            index = command.replace("index_hist_", "").replace("_", " ").upper()
            self.add_preview_tab.emit(f"{index} Histogram", value)
            handled = True

        if command.startswith("index_false_color"):
            index = command.replace("index_false_color_", "").replace("_", " ").upper()
            self.add_preview_tab.emit(f"{index} False Color", value)
            handled = True

        if command == "results":  # When processing is done: File name for results
            self.process_results(self.current_camera_name, value, self.current_image_timestamp)
            handled = True

        if command == "session_data":
            self.experiment.session_data = value
            handled = True

        if command == "error":
            self.add_status_text.emit("Script error: " + value)
            handled = True

        # Unknown response
        if not handled:
            self.add_status_text.emit("Unhandled script command: " + command)

        # if handled:
        #    QApplication.instance().processEvents()

    def refresh_image_preview_size(self):
        # Use contentsMargins trick to preserve pixmap aspect ratio on resize

        if self.ui.image_preview and self.ui.image_preview.pixmap():
            pixmap_height = self.ui.image_preview.pixmap().height()
            pixmap_width = self.ui.image_preview.pixmap().width()

            preview_height = self.ui.image_preview.height()
            preview_width = self.ui.image_preview.width()

            if preview_width * pixmap_height > preview_height * pixmap_width:
                margin = (preview_width - (pixmap_width * preview_height / pixmap_height)) / 2
                self.ui.image_preview.setContentsMargins(0, 0, margin * 2, 0)
            else:
                margin = (preview_height - (pixmap_height * preview_width / pixmap_width)) / 2
                self.ui.image_preview.setContentsMargins(0, 0, 0, margin * 2)

    def process_results(self, camera_name, results, timestamp):
        if Config.verbose_mode:
            tprint("Script results:", camera_name, results)

        tprint("Results", results)

        json_file_name = results
        with open(json_file_name, 'r') as f:
            j = f.read()
            d = json.loads(j)

            observations = d["observations"]
            plant_index = 1
            plant_key = f"plant_{plant_index}"

            while plant_key in observations:
                if Config.verbose_mode:
                    tprint("Plant", plant_key)

                plant = observations[plant_key]

                width = plant["width"]["value"]
                height = plant["height"]["value"]
                area = plant["area"]["value"]
                perimeter = plant["perimeter"]["value"]
                convex_hull_area = plant["convex_hull_area"]["value"]
                longest_path = plant["longest_path"]["value"]

                # Mean index is special as it contains the index name.
                # So we need to browse the keys and match the start of the name to find the value
                mean_index_values = {}
                for key in plant.keys():
                    if key.startswith("mean_index_"):
                        mean_index_values[key] = plant[key]["value"]

                if Config.verbose_mode:
                    tprint(plant_index, width, height, area, perimeter)

                roi = {}

                dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                epoch = dt.timestamp()

                roi["timestamp"] = timestamp
                roi["timestampUnix"] = epoch
                roi["experiment"] = "TBD"
                roi["camera"] = camera_name

                roi["width"] = width
                roi["height"] = height
                roi["area"] = area
                roi["perimeter"] = perimeter
                roi["convexHullArea"] = convex_hull_area
                roi["longestPath"] = longest_path
                roi["meanIndex"] = mean_index_values

                payload = {}
                payload["results"] = roi

                print("Roi:", roi)

                # MQTT
                # Only send in camera mode
                if self.mqtt and self.experiment.image_source is self.experiment.ImageSource.Camera:
                    self.mqtt.publish_roi(camera_name, plant_index, payload)

                # Chart
                for key, chart in self.charts.items():

                    value = 0
                    if key == "width":
                        value = roi["width"]
                    elif key == "height":
                        value = roi["height"]
                    elif key == "area":
                        value = roi["area"]
                    elif key == "perimeter":
                        value = roi["perimeter"]
                    elif key == "hull_area":
                        value = roi["convexHullArea"]
                    elif key == "longest_path":
                        value = roi["longestPath"]
                    elif key.startswith("mean_index_"):
                        value = roi["meanIndex"][key]
                    else:
                        tprint("Unknown chart parameter key", key)

                    chart.add_roi(timestamp, value, "Roi " + str(plant_index))

                plant_index = plant_index + 1
                plant_key = f"plant_{plant_index}"

        for key, chart in self.charts.items():
            chart.update_images()

    def update_current_session_file(self):
        if not self.test_mode:  # Don't generate a session file in test mode
            j = json.dumps(self.current_session, indent=4)

            with open(self.current_session_file_name, 'w') as f:
                f.write(j)

    def resume_analysis(self):
        with open(self.current_session_file_name) as session_file:
            data = json.load(session_file)

            if data["status"]["running"] == "true":
                self.experiment.selected_script = data["scriptName"]

                # Restore script popup
                script_index = self.ui.script_selection_combobox.findText(self.experiment.selected_script)
                if script_index != -1:
                    self.ui.script_selection_combobox.setCurrentIndex(script_index)

                self.experiment.from_dict(data["experimentSettings"])
                # self.scriptOptions = data["scriptSettings"]

                self.current_session = data

                if "cameras" in data:
                    self.cameras = data["cameras"]
                    tprint("Loaded cameras:", self.cameras)

                if self.experiment.camera_cid != "":
                    tprint("Camera cid", self.experiment.camera_cid)
                    if self.experiment.camera_cid in self.cameras:
                        tprint("In cameras:", self.cameras[self.experiment.camera_cid])

                processed_images = data["processedImages"]
                if len(processed_images) > 0:
                    tprint("Last image:", processed_images[-1]["processedAt"])
                    # TODO Use this as the starting point for camera polling

                # tprint("Resume:", self.currentSession) # self.experiment.selectedScript, self.experiment.toDict(),
                # self.scriptOptions, processedImages)

                self.start_analysis(True, False, False)
                self.ui.play_status_label.setText("")
                self.add_status_text.emit("Resuming previous session")

    def remove_result_tabs(self):
        # Remove old tabs except for the first one
        while self.ui.tab_widget.count() > 1:
            w = self.ui.tab_widget.widget(1)
            self.ui.tab_widget.removeTab(1)
            del w

    def start_analysis(self, resume, all_images, force):
        if self.analysis_running and not force:  # Check if analysis is already running
            return  # If analysis is running, do nothing

        if self.experiment.selected_script not in self.script_paths:
            QMessageBox.warning(self, "Missing analysis script", self.experiment.selected_script
                                + " is not available. Has it been removed?")
            return

        # Initialize folder to watch
        folder_to_watch = ""
        if self.experiment.image_source is self.experiment.ImageSource.Image:
            folder_to_watch = os.path.dirname(self.experiment.image_file_path)
        elif self.experiment.image_source is self.experiment.ImageSource.Folder:
            folder_to_watch = self.experiment.folder_file_path
        elif self.experiment.image_source is self.experiment.ImageSource.Camera:
            folder_to_watch = self.experiment.camera_file_path

        if folder_to_watch == "" or folder_to_watch == ".":
            self.add_status_text.emit("Select an image target folder")
        elif self.experiment.selected_script == "":
            self.add_status_text.emit("Select a script")
        else:
            self.ui.play_button.setChecked(True)
            self.ui.play_button.setStyleSheet('background-color: #FC4')

            tprint("Analysis: Selected script: " + self.experiment.selected_script)

            if not resume:
                self.experiment.session_data["temporary"] = {}  # Clear temporary part of the sessionData
                self.update_experiment_file(False)

            # Set-up list of image header files
            image_header_list = []

            if self.experiment.image_source is self.experiment.ImageSource.Image:
                image_header_list = [self.experiment.image_file_path]
            else:
                image_header_list = sorted(glob.glob(folder_to_watch + '/*.hdr'))
                image_header_list = list(map(os.path.normpath, image_header_list))  # Normalize delimiters

            tprint("ImageHeaderList", image_header_list)

            if all_images:  # If all images should be processed
                self.current_session["processedImages"] = []  # Force all images to be processed

            # Remove images we already processed

            if "processedImages" in self.current_session.keys():
                tprint("Cleaning up duplicates")
                # tprint("Processed", self.currentSession["processedImages"])
                # tprint("List", imageHeaderList)

                for t in self.current_session["processedImages"]:
                    norm = os.path.normpath(t["image"])
                    if norm in image_header_list:
                        image_header_list.remove(norm)
                        tprint("Cleaned", norm)

            # TODO How does the remove-already-processed-images logic above work? Conflict?
            # Check if existing image timestamps are earlier than self.camera.startDateTime
            if self.experiment.image_source is self.experiment.ImageSource.Camera and self.camera is not None:
                for i in image_header_list[:]:
                    date, time, camera, wavelength = Helper.info_from_header_file(i)
                    if datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M:%S') \
                        + datetime.timedelta(seconds=1) < self.camera.start_date_time:
                        image_header_list.remove(i)
                        tprint("Filtered by startDateTime", i, datetime.datetime.strptime(date + " " + time,
                                                        '%Y-%m-%d %H:%M:%S'), self.camera.start_date_time)

            tprint("Analysis: Images to run:")
            for i in image_header_list:
                tprint(i)

            # Create basic set of settings, the imageFileName will be added in the iteration
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")

            settings = {}
            settings["experimentSettings"] = self.experiment.to_dict()

            settings["scriptName"] = self.experiment.selected_script

            # On resume, keep Out folder name
            if resume and "outputFolder" in self.current_session:
                settings["outputFolder"] = self.current_session["outputFolder"]  # This will copy the whole dict
            else:
                base_folder = os.path.join(self.experiment.output_file_path, 'Analysis_' + timestamp)

                settings["outputFolder"] = {}
                settings["outputFolder"]["appData"] = os.path.join(base_folder)
                settings["outputFolder"]["images"] = os.path.join(base_folder, "images")
                settings["outputFolder"]["visuals"] = os.path.join(base_folder, "visuals")
                settings["outputFolder"]["data"] = os.path.join(base_folder, "rawData")

            if Config.verbose_mode:
                tprint("Play settings:", settings)

            # Get the display texts for the Chart
            analytics_script_name = self.experiment.selected_script
            sys.path.append(os.path.dirname(self.script_paths[analytics_script_name]))
            # analytics_script = importlib.import_module(analytics_script_name.replace(".py", ""))
            # title, y_label = analytics_script.get_display_name_for_chart(settings) # TODO?

            self.remove_result_tabs()

            self.charts = {}

            # Create the Chart(s)
            for key, value in self.experiment.script_options.items():
                if key == "mean_index" and value:
                    selected_indices = self.experiment.script_options["index_selection"]
                    for index in selected_indices:
                        y_label = f"{index.replace('_', ' ').upper()} Value"  # TODO Alex
                        title = f"{index.replace('_', ' ').upper()} Mean"  # TODO Alex
                        self.charts[f"mean_index_{index}"] = Chart(self, title, y_label)
                else:
                    y_label = key.replace("_", " ").title()  # TODO Alex
                    title = key.replace("_", " ").title()  # TODO Alex
                    if value is True and key in self.experiment.chart_option_types and \
                            self.experiment.chart_option_types[key] == "plot":
                        self.charts[key] = Chart(self, title, y_label)

                    tprint("Chart:", title, y_label, value)

            for key, chart in self.charts.items():
                if path.exists(chart.web_page()):
                    chart.preview_view.setHtml("<!DOCTYPE html><html><body><h1>No Chart data yet</h1></body></html>")
                    os.remove(chart.web_page())
                if path.exists(chart.image_file()):
                    os.remove(chart.image_file())

            # Find selected mask
            mask_path, mask_file = self.mask_info()

            if mask_file != self.experiment.selected_script:
                mask_file_name = os.path.join(mask_path, mask_file)
            else:
                mask_file_name = ''

            # Set up analysis as a background thread
            self.stop_analysis_worker = False

            self.analysis_worker = Worker(self.script_runner, AnalysisWorkerSignals(),
                                          self.experiment.selected_script.replace(".py", ""),
                                          image_header_list, settings, mask_file_name)
            # Any other args, kwargs are passed to the run function

            self.analysis_worker.signals.status.connect(self.on_script_runner_status)

            # Set-up Progress bar and Preview
            if len(image_header_list) > 0:
                self.ui.image_preview_progressbar.setRange(0, len(image_header_list))
            else:
                self.ui.image_preview_progressbar.setRange(0, 1)

            self.ui.image_preview_progressbar.show()
            self.ui.image_preview_progressbar.setValue(0)

            self.ui.image_preview.setText("Waiting for preview...")

            self.ui.status_text.setText("Starting background process...")

            # Start the analysis thread
            self.threadpool.start(self.analysis_worker)

            self.analysis_running = True

            # Store related batch settings in the current session
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            settings["status"] = {"running": "true", "startedAt": timestamp}

            if resume:
                settings["processedImages"] = self.current_session["processedImages"]  # Keep existing ones
                tprint("Resume existing session: Kept images:", len(settings["processedImages"]))
            else:
                settings["processedImages"] = []
                tprint("Starting new session: Cleared images")

            settings["cameras"] = self.cameras

            self.current_session = settings

            self.update_current_session_file()

            if not os.path.exists(settings["outputFolder"]["appData"]):
                os.mkdir(settings["outputFolder"]["appData"])
            if not os.path.exists(settings["outputFolder"]["images"]):
                os.mkdir(settings["outputFolder"]["images"])
            if not os.path.exists(settings["outputFolder"]["visuals"]):
                os.mkdir(settings["outputFolder"]["visuals"])
            if not os.path.exists(settings["outputFolder"]["data"]):
                os.mkdir(settings["outputFolder"]["data"])

            self.ui.results_button.setEnabled(False)

        if self.test_mode:
            while self.analysis_running:
                systime.sleep(1)
                QApplication.instance().processEvents()

    def stop_analysis(self, terminate_process):
        tprint("Analysis: Stop: Done")

        self.ui.image_preview_progressbar.hide()
        self.ui.image_preview_progressbar.setValue(0)
        self.ui.play_button.setChecked(False)
        self.ui.play_button.setStyleSheet("")

        self.add_status_text.emit("Done")
        self.ui.timestamp_label.setText("")
        # self.ui.image_preview.setPixmap(QPixmap())
        # self.ui.image_preview.setText("Done")
        self.analysis_running = False

        # Move current session to the output folder for documentation
        if "status" in self.current_session:
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            self.current_session["status"]["running"] = "false"
            self.current_session["status"]["stoppedAt"] = timestamp
            self.update_current_session_file()

        if "outputFolder" in self.current_session:
            if os.path.exists(self.current_session_file_name) \
                and os.path.exists(self.current_session["outputFolder"]["appData"]):
                shutil.move(self.current_session_file_name,
                            os.path.join(self.current_session["outputFolder"]["appData"], 'session.json'))
            else:
                tprint("Path missing:", self.current_session_file_name, self.current_session["outputFolder"]["appData"])

            self.ui.results_button.setEnabled(True)

            for key, chart in self.charts.items():
                if os.path.exists(chart.web_page()):
                    chart.preview_view.load(QUrl.fromLocalFile(path.join(path.dirname(__file__), chart.web_page())))

                    # Disable scrollbars
                    chart.preview_view.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)

                    chart.preview_view.page().setBackgroundColor(self.experiment.theme_background_color())
                    chart.preview_view.show()

                    # Copy webPage() to "outputFolder"
                    shutil.copy(chart.web_page(), os.path.join(self.current_session["outputFolder"]["visuals"],
                                                            f"chart_{key}.html"))
                chart.preview_label.hide()
                chart.preview_label.setPixmap(QPixmap())

            output_folder = self.current_session["outputFolder"]["data"]

            combined_json = os.path.join(output_folder, "combined.json")

            process_results(output_folder, combined_json)

            self.save_as_experiment_directly(os.path.join(self.current_session["outputFolder"]["appData"], "experiment.xp"))

            json2csv(combined_json, os.path.join(self.current_session["outputFolder"]["appData"], "combined"))

        self.experiment.session_data["temporary"] = {}  # Clear temporary part of the sessionData

        self.update_experiment_file(False)

    def play(self):
        ready, reason = self.ready_to_run()
        if ready:
            self.chart = None

            if self.experiment.image_source is self.experiment.ImageSource.Image:
                self.start_analysis(False, True, False)
            elif self.experiment.image_source is self.experiment.ImageSource.Folder:
                if self.images_added:
                    accepted, all_images = self.open_folder_start_dialog()
                    if accepted is True:  # Dialog wasn't cancelled
                        self.start_analysis(False, all_images, False)

                    self.images_added = False
                else:
                    self.start_analysis(False, True, False)  # Process all images if nothing changed
            elif self.experiment.image_source is self.experiment.ImageSource.Camera:
                if self.open_camera_start_dialog() is True:  # Dialog wasn't cancelled
                    self.start_analysis(False, False, False)

    def stop(self):
        if self.camera and len(self.camera.files_to_fetch) > 0:
            self.camera.files_to_fetch = []
            self.refresh_stop_button_status()
            tprint("Fetch queue cleared")

        # Ask threads to stop
        self.stop_camera_discovery_worker = True
        self.stop_analysis_worker = True

        # Wait for threads to actually stop
        self.threadpool.waitForDone()

        self.stop_analysis(True)

    def clear_sessiondata(self):
        # Clear all session data
        self.experiment.session_data["persistent"] = {}
        self.experiment.session_data["temporary"] = {}
        self.update_experiment_file(False)

        tprint("All session data cleared")

    def ready_to_run(self):
        ready = True
        reason = ""
        if self.experiment.image_source is self.experiment.ImageSource.Image:
            if self.experiment.image_file_path == "":
                ready = False
                reason = "No valid image source"
        elif self.experiment.image_source is self.experiment.ImageSource.Folder:
            if self.experiment.folder_file_path == "":
                ready = False
                reason = "No valid image source"
        elif self.experiment.image_source is self.experiment.ImageSource.Camera:
            if self.experiment.camera_file_path == "":
                ready = False
                reason = "No target folder defined"
            elif self.experiment.camera_cid == "":
                ready = False
                reason = "No camera defined"

        if len(self.experiment.script_options) == 0:
            ready = False
            reason = "No script options defined"

        if self.experiment.selected_script == "":
            ready = False
            reason = "No script selected"

        if not self.experiment.mask_defined:
            ready = False
            reason = "No mask defined"

        self.ui.play_button.setEnabled(ready)

        return ready, reason

    def refresh_play_button_status(self):
        ready, reason = self.ready_to_run()
        self.ui.play_button.setEnabled(ready)

    def refresh_ready_to_play(self):
        ready, reason = self.ready_to_run()
        if not self.analysis_running:
            if ready:
                self.ui.play_status_label.setText("Ready to run using script<br><b>"
                                                  + self.experiment.selected_script
                                                  + "</b><br><br>Press Play to continue")
            else:
                self.ui.play_status_label.setText("Not Ready:<br>" + reason)

    def refresh_stop_button_status(self):
        active = (self.camera and len(self.camera.files_to_fetch) > 0)

        self.ui.stop_button.setChecked(active)
        if self.ui.stop_button.isChecked():
            self.ui.stop_button.setStyleSheet('background-color: #FC4')
        else:
            self.ui.stop_button.setStyleSheet("")

    def open_settings_dialog(self):
        settings_dialog = SettingsDialog(self)

        if settings_dialog.exec() == QDialog.Accepted:
            self.experiment.mqtt_broker =  settings_dialog.ui.ip_lineedit.text()

            self.experiment.mqtt_port = "1883"
            if settings_dialog.ui.port_lineedit.text().isdigit():
                self.experiment.mqtt_port = settings_dialog.ui.port_lineedit.text()

            self.experiment.mqtt_username = settings_dialog.ui.username_lineedit.text()
            self.experiment.mqtt_password = settings_dialog.ui.password_lineedit.text()

            if self.experiment.mqtt_broker != "":
                self.start_mqtt()
            else:
                self.on_mqtt_status_changed("No broker defined", True)

            self.update_experiment_file(False)

    def open_about_dialog(self):
        about_dialog = AboutDialog()

        about_dialog.exec()

    def open_help_dialog(self):
        # Since HelpDialog is a non-modal dialog (to be able to have it open while using the application),
        # we need to keep the instance around
        # by assigning it to a class variable
        self.help_dialog = HelpDialog()
        self.help_dialog.show()

        # help_dialog.exec()

    def open_eula_dialog(self):
        eula_dialog = EulaDialog()

        eula_dialog.exec()

        if not eula_dialog.ui.accept_checkbox.isChecked():
            sys.exit("No license agreement")
        else:
            with open(os.path.join(self.rvs_path, ".rvs"), 'w'):
                pass

    def open_camera_start_dialog(self):
        if self.camera:
            camera_start_dialog = CameraStartDialog(self)

            if camera_start_dialog.exec() == QDialog.Accepted:
                if camera_start_dialog.ui.new_images_only.isChecked():
                    tprint("Camera: Set startDateTime to now")
                    self.camera.start_date_time = datetime.datetime.now()  # Start collecting images now
                elif camera_start_dialog.ui.include_existing.isChecked():
                    file_name = camera_start_dialog.files[camera_start_dialog.ui.start_combo_box.currentIndex()]
                    hdr_file = self.camera.get_file('scheduler', file_name)

                    with tempfile.TemporaryDirectory() as tmp:
                        # tprint("Temp:", tmp)

                        f = open(os.path.join(tmp, file_name), "wb")  # save image to temp file
                        f.write(hdr_file)
                        f.close()

                        # Get date time from hdr file content
                        date, time, camera, wavelength = Helper.info_from_header_file(os.path.join(tmp, file_name))
                        hdr_date_time = datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M:%S')

                        # Get date time from filename
                        date_time_part = file_name[-19:][:15]  # Extract the date and time part
                        filename_date_time = datetime.datetime.strptime(date_time_part, '%Y%m%d_%H%M%S')

                        # There can be a mismatch between the date/time in the hdr file and the filename
                        # Therefore, we use the lowest time to make sure we get all the files we are asking
                        # for with get_first_in_range
                        if hdr_date_time < filename_date_time:
                           self.camera.start_date_time = hdr_date_time
                           tprint("Camera: Set startDateTime from selected hdr file content:", date, time)
                        else:
                           self.camera.start_date_time = filename_date_time
                           tprint("Camera: Set startDateTime from selected hdr file name:", date, time)

                    self.camera.delete_from_camera = camera_start_dialog.ui.delete_from_camera_checkbox.isChecked()
                return True
        else:
            QMessageBox.warning(self, "No camera", "You must have a camera connected")

        return False

    def open_folder_start_dialog(self):
        folder_start_dialog = FolderStartDialog(self)

        if folder_start_dialog.exec() == QDialog.Accepted:
            all_images = False
            if folder_start_dialog.ui.new_images_only.isChecked():
                all_images = False
            elif folder_start_dialog.ui.include_existing.isChecked():
                all_images = True
            return (True, all_images)

        return (False, False)

    def open_image_source_dialog(self):
        image_source_dialog = ImageSourceDialog(self)

        image_source_dialog.exec()

        self.refresh_play_button_status()
        self.refresh_ready_to_play()

    def open_image_option_dialog(self):
        image_option_dialog = ImageOptionDialog(self)

        image_option_dialog.exec()

        self.refresh_play_button_status()
        self.refresh_ready_to_play()

    def open_image_mask_dialog(self):
        # if (ImageMaskDialog.MASK_FILE_PREFIX + self.experiment.selectedScript) not in self.maskPaths:
        #    QMessageBox.warning(self, "Mask script missing", "The selected script does not have a related mask script")
        # else:
        image_mask_dialog = ImageMaskDialog(self)

        if image_mask_dialog.exec() == QDialog.Accepted:
            # Capture the mask parameters

            settings = Helper.get_settings_for_ui_elements(image_mask_dialog)

            self.experiment.mask = settings

            self.experiment.mask_reference_image1 = image_mask_dialog.ui.reference_image1.image_file_name
            self.experiment.mask_reference_image2 = image_mask_dialog.ui.reference_image2.image_file_name

            # self.experiment.crop_rect = image_mask_dialog.ui.reference_image1.crop_rect
            # Both images share the same crop rect

            self.update_experiment_file(True)

            tprint("Exit", self.experiment.mask)

            self.refresh_play_button_status()
            self.refresh_ready_to_play()

    def open_image_roi_dialog(self):
        image_roi_dialog = ImageRoiDialog(self)

        if image_roi_dialog.exec() == QDialog.Accepted:
            # Capture the roi parameters
            self.experiment.roi_info.rect = image_roi_dialog.rubberband_rect
            self.experiment.roi_info.columns = image_roi_dialog.ui.columns_spinbox.value()
            self.experiment.roi_info.rows = image_roi_dialog.ui.rows_spinbox.value()
            self.experiment.roi_info.radius = image_roi_dialog.ui.radius_spinbox.value()
            self.experiment.roi_info.width = image_roi_dialog.ui.width_spinbox.value()
            self.experiment.roi_info.height = image_roi_dialog.ui.height_spinbox.value()
            self.experiment.roi_info.shape = image_roi_dialog.shape
            self.experiment.roi_info.placement_mode = image_roi_dialog.placement_mode
            self.experiment.roi_info.detection_mode = image_roi_dialog.detection_mode
            self.experiment.roi_info.manual_roi_items = image_roi_dialog.manual_roi_items

            self.experiment.roi_reference_image1 = image_roi_dialog.ui.reference_image1.image_file_name
            self.experiment.roi_reference_image2 = image_roi_dialog.ui.reference_image2.image_file_name

            self.experiment.crop_rect = image_roi_dialog.ui.reference_image1.crop_rect
            # Both images share the same crop rect

            self.update_experiment_file(False)

            self.refresh_play_button_status()
            self.refresh_ready_to_play()

    def open_analysis_preview_dialog(self):
        analysis_preview_dialog = AnalysisPreviewDialog(self)

        if analysis_preview_dialog.exec() == QDialog.Accepted:
            self.experiment.script_reference_image1 = analysis_preview_dialog.ui.reference_image1.image_file_name
            self.experiment.script_reference_image2 = analysis_preview_dialog.ui.reference_image2.image_file_name

            # self.experiment.crop_rect = analysis_preview_dialog.ui.reference_image1.crop_rect
            # # Both images share the same crop rect

            self.update_experiment_file(False)

            self.refresh_play_button_status()
            self.refresh_ready_to_play()

    def open_analysis_options_dialog(self):
        analysis_options_dialog = AnalysisOptionsDialog(self)

        if analysis_options_dialog.exec() == QDialog.Accepted:
            # Capture the script parameters
            settings = Helper.get_settings_for_ui_elements(analysis_options_dialog)
            self.experiment.script_options = settings

            # Capture the chart parameters
            self.experiment.chart_option_types = {}
            child_checkboxes = analysis_options_dialog.ui.main_groupbox.findChildren(QCheckBox)
            for child_checkbox in child_checkboxes:
                self.experiment.script_options[child_checkbox.objectName()] = child_checkbox.isChecked()

                self.experiment.chart_option_types[child_checkbox.objectName()] = \
                    child_checkbox.property("chartOptionType")

                tprint("Chart option:", child_checkbox.objectName(), child_checkbox.property("chartOptionType"),
                       child_checkbox.isChecked())

            self.update_experiment_file(False)

            self.refresh_play_button_status()
            self.refresh_ready_to_play()

    def open_download_images_dialog(self):
        if self.camera:
            download_images_dialog = DownloadImagesDialog(self)

            download_images_dialog.exec()
        else:
            QMessageBox.warning(self, "No camera connected", "Please connect a camera to download images")

    def open_delete_images_dialog(self):
        if self.camera:
            delete_images_dialog = DeleteImagesDialog(self)

            delete_images_dialog.exec()
        else:
            QMessageBox.warning(self, "No camera connected", "Please connect a camera to download images")

    def show_results(self):
        # os.startfile(self.currentSession["outputFolder"])
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.current_session["outputFolder"]["appData"]))

    def on_add_status_text(self, text):
        self.ui.status_text.setText(self.ui.status_text.text() + "<br>" + text)

    def on_add_preview_tab(self, tab_name, file_name):
        tprint("add_preview_tab", tab_name, file_name)
        if not self.tab_exists(tab_name):
            tab = ResultTabWidget(file_name)
            tab.setContentsMargins(0, 0, 0, 0)

            self.ui.tab_widget.addTab(tab, tab_name)

        widget = self.tab_widget(tab_name)
        widget.update_pixmap(file_name)

    def mask_info(self):
        if self.ui.mask_selection_combobox.currentIndex() == 0:  ## Default item -> use mask in script
            mask_file = self.experiment.selected_script
            mask_path = os.path.dirname(self.script_paths[mask_file])
        else:
            mask_file = self.ui.mask_selection_combobox.currentText()
            mask_path = os.path.dirname(self.mask_paths[mask_file])

        return mask_path, mask_file

    def current_mask_script(self):
        mask_path, mask_file = self.mask_info()

        sys.path.append(mask_path)

        # tprint("Mask ranges: Running script:", maskFile, "from", maskPath)

        return importlib.import_module(mask_file.replace(".py", ""))

    def current_analysis_script(self):
        analytics_script_name = self.experiment.selected_script
        sys.path.append(os.path.dirname(self.script_paths[analytics_script_name]))
        return importlib.import_module(analytics_script_name.replace(".py", ""))

    def select_image_dialog(self, main_window, dialog, reference_image):
        select_image_dialog = SelectImageDialog(main_window, dialog, reference_image)

        # In folder mode, pick file directly from selected folder
        if self.experiment.image_source is self.experiment.ImageSource.Folder:
           select_image_dialog.pick_image()
        else:
           # For other modes, present selection dialog to pick image source
           select_image_dialog.exec()

    def set_theme(self, theme):
        if platform.system() != "Darwin":
            qdarktheme.setup_theme(theme)

