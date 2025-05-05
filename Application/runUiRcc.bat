rem QtCreator doesn't know the Python environment path during the build phase so we add it here

PATH=$PATH;C:\Python\rvs\Scripts

pyside6-uic ui\AboutDialog.ui           > ui_AboutDialog.py
pyside6-uic ui\AnalysisOptionsDialog.ui > ui_AnalysisOptionsDialog.py
pyside6-uic ui\AnalysisPreviewDialog.ui > ui_AnalysisPreviewDialog.py
pyside6-uic ui\CameraStartDialog.ui     > ui_CameraStartDialog.py
pyside6-uic ui\DownloadImagesDialog.ui  > ui_DownloadImagesDialog.py
pyside6-uic ui\DeleteImagesDialog.ui    > ui_DeleteImagesDialog.py
pyside6-uic ui\EulaDialog.ui            > ui_EulaDialog.py
pyside6-uic ui\FolderStartDialog.ui     > ui_FolderStartDialog.py
pyside6-uic ui\HelpDialog.ui            > ui_HelpDialog.py
pyside6-uic ui\ImageMaskDialog.ui       > ui_ImageMaskDialog.py
pyside6-uic ui\ImageOptionDialog.ui     > ui_ImageOptionDialog.py
pyside6-uic ui\ImageRoiDialog.ui        > ui_ImageRoiDialog.py
pyside6-uic ui\ImageSourceDialog.ui     > ui_ImageSourceDialog.py
pyside6-uic ui\MainWindow.ui            > ui_MainWindow.py
pyside6-uic ui\SelectImageDialog.ui     > ui_SelectImageDialog.py

pyside6-rcc resources/CameraApp.qrc -o CameraApp_rc.py
