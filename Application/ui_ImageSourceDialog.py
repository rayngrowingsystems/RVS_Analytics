# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ImageSourceDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import CameraApp_rc

class Ui_ImageSourceDialog(object):
    def setupUi(self, ImageSourceDialog):
        if not ImageSourceDialog.objectName():
            ImageSourceDialog.setObjectName(u"ImageSourceDialog")
        ImageSourceDialog.setWindowModality(Qt.NonModal)
        ImageSourceDialog.resize(629, 463)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ImageSourceDialog.sizePolicy().hasHeightForWidth())
        ImageSourceDialog.setSizePolicy(sizePolicy)
        ImageSourceDialog.setMinimumSize(QSize(0, 0))
        self.gridLayout = QGridLayout(ImageSourceDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName(u"vertical_layout")
        self.image_source_radiobutton = QRadioButton(ImageSourceDialog)
        self.image_source_radiobutton.setObjectName(u"image_source_radiobutton")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.image_source_radiobutton.setFont(font)
        self.image_source_radiobutton.setChecked(True)

        self.vertical_layout.addWidget(self.image_source_radiobutton)

        self.label_5 = QLabel(ImageSourceDialog)
        self.label_5.setObjectName(u"label_5")

        self.vertical_layout.addWidget(self.label_5)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.image_browse_button = QPushButton(ImageSourceDialog)
        self.image_browse_button.setObjectName(u"image_browse_button")

        self.horizontalLayout_8.addWidget(self.image_browse_button)

        self.image_file_path = QLabel(ImageSourceDialog)
        self.image_file_path.setObjectName(u"image_file_path")

        self.horizontalLayout_8.addWidget(self.image_file_path)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_7)


        self.vertical_layout.addLayout(self.horizontalLayout_8)

        self.line_3 = QFrame(ImageSourceDialog)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.vertical_layout.addWidget(self.line_3)

        self.folder_source_radiobutton = QRadioButton(ImageSourceDialog)
        self.folder_source_radiobutton.setObjectName(u"folder_source_radiobutton")
        self.folder_source_radiobutton.setFont(font)
        self.folder_source_radiobutton.setChecked(False)

        self.vertical_layout.addWidget(self.folder_source_radiobutton)

        self.label_3 = QLabel(ImageSourceDialog)
        self.label_3.setObjectName(u"label_3")

        self.vertical_layout.addWidget(self.label_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.folder_browse_button = QPushButton(ImageSourceDialog)
        self.folder_browse_button.setObjectName(u"folder_browse_button")

        self.horizontalLayout_6.addWidget(self.folder_browse_button)

        self.folder_file_path = QLabel(ImageSourceDialog)
        self.folder_file_path.setObjectName(u"folder_file_path")

        self.horizontalLayout_6.addWidget(self.folder_file_path)

        self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontal_spacer)


        self.vertical_layout.addLayout(self.horizontalLayout_6)

        self.line = QFrame(ImageSourceDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.vertical_layout.addWidget(self.line)

        self.camera_source_radiobutton = QRadioButton(ImageSourceDialog)
        self.camera_source_radiobutton.setObjectName(u"camera_source_radiobutton")
        self.camera_source_radiobutton.setFont(font)

        self.vertical_layout.addWidget(self.camera_source_radiobutton)

        self.label_4 = QLabel(ImageSourceDialog)
        self.label_4.setObjectName(u"label_4")

        self.vertical_layout.addWidget(self.label_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(2, -1, -1, -1)
        self.camera_selection_combobox = QComboBox(ImageSourceDialog)
        self.camera_selection_combobox.setObjectName(u"camera_selection_combobox")
        self.camera_selection_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.horizontalLayout_4.addWidget(self.camera_selection_combobox)

        self.camera_refresh_button = QPushButton(ImageSourceDialog)
        self.camera_refresh_button.setObjectName(u"camera_refresh_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.camera_refresh_button.sizePolicy().hasHeightForWidth())
        self.camera_refresh_button.setSizePolicy(sizePolicy1)
        icon = QIcon()
        icon.addFile(u":/images/Refresh.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.camera_refresh_button.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.camera_refresh_button)

        self.label_6 = QLabel(ImageSourceDialog)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_4.addWidget(self.label_6)

        self.camera_api_key = QLineEdit(ImageSourceDialog)
        self.camera_api_key.setObjectName(u"camera_api_key")
        self.camera_api_key.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.camera_api_key)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.camera_identify_button = QPushButton(ImageSourceDialog)
        self.camera_identify_button.setObjectName(u"camera_identify_button")

        self.horizontalLayout_4.addWidget(self.camera_identify_button)

        self.camera_configure_button = QPushButton(ImageSourceDialog)
        self.camera_configure_button.setObjectName(u"camera_configure_button")

        self.horizontalLayout_4.addWidget(self.camera_configure_button)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 1)
        self.horizontalLayout_4.setStretch(4, 1)
        self.horizontalLayout_4.setStretch(7, 8)

        self.vertical_layout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.vertical_layout.addItem(self.verticalSpacer_2)

        self.label = QLabel(ImageSourceDialog)
        self.label.setObjectName(u"label")

        self.vertical_layout.addWidget(self.label)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.camera_browse_button = QPushButton(ImageSourceDialog)
        self.camera_browse_button.setObjectName(u"camera_browse_button")

        self.horizontalLayout_5.addWidget(self.camera_browse_button)

        self.camera_file_path = QLabel(ImageSourceDialog)
        self.camera_file_path.setObjectName(u"camera_file_path")

        self.horizontalLayout_5.addWidget(self.camera_file_path)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.vertical_layout.addLayout(self.horizontalLayout_5)

        self.line_2 = QFrame(ImageSourceDialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.vertical_layout.addWidget(self.line_2)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.vertical_layout.addItem(self.verticalSpacer_3)

        self.label_2 = QLabel(ImageSourceDialog)
        self.label_2.setObjectName(u"label_2")

        self.vertical_layout.addWidget(self.label_2)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.output_browse_button = QPushButton(ImageSourceDialog)
        self.output_browse_button.setObjectName(u"output_browse_button")

        self.horizontalLayout_7.addWidget(self.output_browse_button)

        self.output_file_path = QLabel(ImageSourceDialog)
        self.output_file_path.setObjectName(u"output_file_path")

        self.horizontalLayout_7.addWidget(self.output_file_path)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_6)


        self.vertical_layout.addLayout(self.horizontalLayout_7)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.vertical_layout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.done_button = QPushButton(ImageSourceDialog)
        self.done_button.setObjectName(u"done_button")

        self.horizontalLayout_2.addWidget(self.done_button)


        self.vertical_layout.addLayout(self.horizontalLayout_2)

        self.vertical_layout.setStretch(4, 2)
        self.vertical_layout.setStretch(5, 2)
        self.vertical_layout.setStretch(6, 2)
        self.vertical_layout.setStretch(7, 2)
        self.vertical_layout.setStretch(8, 2)
        self.vertical_layout.setStretch(9, 2)
        self.vertical_layout.setStretch(10, 2)
        self.vertical_layout.setStretch(11, 1)
        self.vertical_layout.setStretch(18, 20)
        self.vertical_layout.setStretch(19, 2)

        self.gridLayout.addLayout(self.vertical_layout, 0, 0, 1, 1)


        self.retranslateUi(ImageSourceDialog)
        self.done_button.clicked.connect(ImageSourceDialog.accept)

        self.done_button.setDefault(True)


        QMetaObject.connectSlotsByName(ImageSourceDialog)
    # setupUi

    def retranslateUi(self, ImageSourceDialog):
        ImageSourceDialog.setWindowTitle(QCoreApplication.translate("ImageSourceDialog", u"Image Source", None))
        self.image_source_radiobutton.setText(QCoreApplication.translate("ImageSourceDialog", u"Image", None))
        self.label_5.setText(QCoreApplication.translate("ImageSourceDialog", u"A single image will be analysed", None))
        self.image_browse_button.setText(QCoreApplication.translate("ImageSourceDialog", u"Browse...", None))
        self.image_file_path.setText("")
        self.folder_source_radiobutton.setText(QCoreApplication.translate("ImageSourceDialog", u"Folder", None))
        self.label_3.setText(QCoreApplication.translate("ImageSourceDialog", u"The image series in the selected folder will be analysed", None))
        self.folder_browse_button.setText(QCoreApplication.translate("ImageSourceDialog", u"Browse...", None))
        self.folder_file_path.setText("")
        self.camera_source_radiobutton.setText(QCoreApplication.translate("ImageSourceDialog", u"Camera", None))
        self.label_4.setText(QCoreApplication.translate("ImageSourceDialog", u"New images from the selected camera will be copied to a folder and analysed on-the-fly", None))
        self.camera_selection_combobox.setPlaceholderText(QCoreApplication.translate("ImageSourceDialog", u"No cameras found", None))
        self.camera_refresh_button.setText("")
        self.label_6.setText(QCoreApplication.translate("ImageSourceDialog", u"Key:", None))
        self.camera_identify_button.setText(QCoreApplication.translate("ImageSourceDialog", u"Identify", None))
        self.camera_configure_button.setText(QCoreApplication.translate("ImageSourceDialog", u"Configure", None))
        self.label.setText(QCoreApplication.translate("ImageSourceDialog", u"Target folder", None))
        self.camera_browse_button.setText(QCoreApplication.translate("ImageSourceDialog", u"Browse...", None))
        self.camera_file_path.setText("")
        self.label_2.setText(QCoreApplication.translate("ImageSourceDialog", u"Folder for analysis output files", None))
        self.output_browse_button.setText(QCoreApplication.translate("ImageSourceDialog", u"Browse...", None))
        self.output_file_path.setText("")
        self.done_button.setText(QCoreApplication.translate("ImageSourceDialog", u"Done", None))
    # retranslateUi

