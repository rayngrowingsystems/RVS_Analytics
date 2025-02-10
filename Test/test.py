from os import path
import sys
import time

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication, QStandardPaths
from PySide6 import QtCore

QApplication.setOrganizationName("RAYN")
QApplication.setApplicationName("RAYN Vision System")

app = QApplication([])
app.setStyle( 'Fusion' )

sys.path.append(path.join("..", "Application"))

from MainWindow import MainWindow

script_folder = path.join("..", "Application", 'Scripts')
mask_folder = path.join("..", "Application", 'Masks')

main_window = MainWindow(script_folder, mask_folder)

main_window.resize(1200, 800)

main_window.show()

main_window.open_experiment_directly("wl_test.xp")   
app.processEvents()

main_window.open_image_roi_dialog()
app.processEvents()

while True:
    app.processEvents()
    time.sleep(1)
    # How do we exit this? Check flag
    
# exit_code = app.exec()
