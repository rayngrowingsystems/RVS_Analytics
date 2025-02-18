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

from multiprocessing import freeze_support

# freeze_support should be at the top to be able to handle multiprocessing in the installer. Otherwise, the CameraApp module is executed multiple times
# https://github.com/pyinstaller/pyinstaller/issues/3957

# Thread about multiprocessing and why Process spawn runs the main module again, with a different name (__mp_main__):
# https://stackoverflow.com/questions/72497140/in-python-multiprocessing-why-is-child-process-name-mp-main-is-there-a-way

freeze_support()

import Helper
from Helper import tprint

tprint("Loading CameraApp", __name__)

import sys
import os
import glob
import stackprinter
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QCoreApplication, QStandardPaths
from PySide6 import QtCore

import CameraApp_rc
from MainWindow import MainWindow


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
        sys.stdout.write(buf)

    def flush(self):
        pass


def check_system_theme():

    tprint("Platform:", sys.platform)
    theme_dark_mode = False

    # Windows: Check for dark mode
    if sys.platform == "win32":
        try:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            reg_keypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'

            try:
                reg_key = winreg.OpenKey(registry, reg_keypath)
                for i in range(1024):
                    try:
                        value_name, value, _ = winreg.EnumValue(reg_key, i)
                        if value_name == 'AppsUseLightTheme':
                            theme_dark_mode = True
                    except OSError:
                        theme_dark_mode = False
                        break

            except FileNotFoundError:
                tprint("Key not found")
                theme_dark_mode = False

        except ImportError:
            tprint("winreg missing")
            theme_dark_mode = False

    return theme_dark_mode


def start_application(testing=False):
    QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    app.setStyle('Fusion')

    if not testing:
        # Splash screen - need to happen after QApplication is created and before MainWindow is loaded
        splash = QLabel(None, QtCore.Qt.SplashScreen)
        splash.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        splash.setPixmap(QPixmap(":/images/Splash.png"))
        splash.show()

        app.processEvents()
    else:
        splash = None

    # Needs to be set before calling MainWindow. These settings are used to find the way to AppData and Documents
    QApplication.setOrganizationName("RAYN")
    QApplication.setApplicationName("RAYN Vision System")

    app.setQuitOnLastWindowClosed(True)

    return app, splash


def start_logger(testing=False):
    run_date_time = datetime.now().strftime("%Y-%d-%m_%H%M%S")

    if not testing:
        local_data_location_path = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)

        if not os.path.exists(local_data_location_path):
            os.makedirs(local_data_location_path)

        debug_file_name = os.path.normpath(
            os.path.join(local_data_location_path, run_date_time + ".log"))
        error_file_name = os.path.normpath(os.path.join(local_data_location_path, "error.log"))

    else:
        if not os.path.exists("log"):
            print("Log folder does not exist. Creating new folder")
            os.makedirs("log")

        debug_file_name = f"log/{run_date_time}_debug.log"
        error_file_name = f"log/{run_date_time}_error.log"

    tprint("Debug file name:", debug_file_name)
    tprint("Error file name:", error_file_name)
    Helper.debug_file_name = debug_file_name

    if os.path.exists(debug_file_name):
        os.remove(debug_file_name)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(message)s',
        handlers=[RotatingFileHandler(error_file_name, maxBytes=200000, backupCount=5)]
    )

    # Log crash info
    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl

    return debug_file_name, error_file_name


def remove_camera_files():
    file_list = glob.glob(os.path.join('.', 'Camera_*.json'), recursive=False)
    for file_path in file_list:
        try:
            os.remove(file_path)
        except:
            tprint("Error while deleting file : ", file_path)


if __name__ == '__main__':  # Process will re-run CameraApp.py (with name = __mp_main__) so let's make sure nothing is executed if in that case

    dark_mode = check_system_theme()
    stackprinter.set_excepthook()
    rvs_app, splash = start_application()
    start_logger()

    tprint("Path:", os.path.dirname(__file__))
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        tprint('running in a PyInstaller bundle')

    remove_camera_files()

    # In frozen mode (PyInstaller), __file__ contains the path to the execution folder
    script_folder = os.path.join(os.path.dirname(__file__), 'Scripts')
    mask_folder = os.path.join(os.path.dirname(__file__), 'Masks')
    preset_folder = os.path.join(script_folder, 'presets')

    # Open main window
    widget = MainWindow(script_folder, mask_folder, preset_folder)
    widget.resize(1200, 800)
    widget.show()

    if splash:
        splash.close()

    exit_code = rvs_app.exec()
    sys.exit(exit_code)
