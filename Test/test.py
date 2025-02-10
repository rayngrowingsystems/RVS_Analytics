from os import path
import sys
import time
import stackprinter
sys.path.append(path.join("..", "Application"))

import cameraapp
from MainWindow import MainWindow


stackprinter.set_excepthook()
rvs_app, splash = cameraapp.start_application(testing=True)
cameraapp.start_logger(testing=True)

script_folder = path.join("..", "Application", 'Scripts')
mask_folder = path.join("..", "Application", 'Masks')

main_window = MainWindow(script_folder, mask_folder)

main_window.resize(1200, 800)
main_window.show()

main_window.open_experiment_directly("wl_test.xp")   
rvs_app.processEvents()

main_window.open_image_roi_dialog()
rvs_app.processEvents()

main_window.open_image_mask_dialog()
rvs_app.processEvents()

try:
    while True:
        rvs_app.processEvents()
        time.sleep(1)
    # How do we exit this? Check flag
except KeyboardInterrupt():
    print("stopping")
    exit_code = rvs_app.exec()
