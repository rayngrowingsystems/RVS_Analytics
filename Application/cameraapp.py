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

if __name__ == '__main__':  # Process will re-run CameraApp.py (with name = __mp_main__) so let's make sure nothing is executed if in that case
    from os import path
    import sys
    import stackprinter
    from datetime import datetime

    from PySide6.QtWidgets import QApplication, QLabel
    from PySide6.QtGui import QPixmap
    from PySide6.QtCore import QCoreApplication, QStandardPaths
    from PySide6 import QtCore

    import CameraApp_rc

    tprint("Platform:", sys.platform)

    dark_mode = False

    # Windows: Check for dark mode
    if sys.platform == "win32":
        try:
            import winreg
        except ImportError:
            tprint("winreg missing")

        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        reg_keypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
        try:
            reg_key = winreg.OpenKey(registry, reg_keypath)
        except FileNotFoundError:
            tprint("Key not found")

        for i in range(1024):
            try:
                value_name, value, _ = winreg.EnumValue(reg_key, i)
                if value_name == 'AppsUseLightTheme':
                    dark_mode = True
            except OSError:
                break

    stackprinter.set_excepthook()

    QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)

    app = QApplication([])
    app.setStyle( 'Fusion' )

    # Splash screen - need to happen after QApplication is created and before MainWindow is loaded
    splash = QLabel(None, QtCore.Qt.SplashScreen)
    splash.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    splash.setPixmap(QPixmap(":/images/Splash.png"))
    splash.show()

    app.processEvents()

    # Needs to be set before calling MainWindow. These settings are used to find the way to AppData and Documents
    QApplication.setOrganizationName("RAYN")
    QApplication.setApplicationName("RAYN Vision System")

    from MainWindow import MainWindow

    import os
    import glob

    import logging
    from logging.handlers import RotatingFileHandler

    # from qt_material import apply_stylesheet

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

    local_data_location_path = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)

    if not os.path.exists(local_data_location_path):
        os.makedirs(local_data_location_path)

    debug_file_name = os.path.normpath(os.path.join(local_data_location_path, datetime.now().strftime("%Y-%d-%m %H.%M.%S") + ".log"))
    error_file_name = os.path.normpath(os.path.join(local_data_location_path, "error.log"))

    tprint("Debug file name:", debug_file_name)
    tprint("Error file name:", error_file_name)

    Helper.debug_file_name = debug_file_name

    if path.exists(debug_file_name):
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

    def resource_path():
        tprint("Path:", path.dirname(__file__))

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        tprint('running in a PyInstaller bundle')

    resource_path()

    app.setQuitOnLastWindowClosed(True)

    script_folder = path.join(path.dirname(__file__), 'Scripts')  # In frozen mode (PyInstaller), __file__ contains the path to the execution folder
    mask_folder = path.join(path.dirname(__file__), 'Masks')  # In frozen mode (PyInstaller), __file__ contains the path to the execution folder

    # Get rid of old camera files
    file_list = glob.glob(path.join('.', 'Camera_*.json'), recursive=False)
    for file_path in file_list:
        try:
            os.remove(file_path)
        except:
            tprint("Error while deleting file : ", file_path)

    # Open main window
    widget = MainWindow(script_folder, mask_folder)

    # apply_stylesheet(app, theme='dark_amber.xml')

    widget.resize(1200, 800)

    widget.show()

    splash.close()

    exit_code = app.exec()

    sys.exit(exit_code)
