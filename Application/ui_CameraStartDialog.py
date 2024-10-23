# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CameraStartDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_CameraStartDialog(object):
    def setupUi(self, CameraStartDialog):
        if not CameraStartDialog.objectName():
            CameraStartDialog.setObjectName(u"CameraStartDialog")
        CameraStartDialog.resize(346, 212)
        self.gridLayout_2 = QGridLayout(CameraStartDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 7, 0, 1, 1)

        self.new_images_only = QRadioButton(CameraStartDialog)
        self.new_images_only.setObjectName(u"new_images_only")
        self.new_images_only.setChecked(True)

        self.gridLayout_2.addWidget(self.new_images_only, 0, 0, 1, 1)

        self.line = QFrame(CameraStartDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 1)

        self.include_existing = QRadioButton(CameraStartDialog)
        self.include_existing.setObjectName(u"include_existing")

        self.gridLayout_2.addWidget(self.include_existing, 2, 0, 1, 1)

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setObjectName(u"horizontal_layout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontal_layout.addItem(self.horizontalSpacer)

        self.cancel_button = QPushButton(CameraStartDialog)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setAutoDefault(False)

        self.horizontal_layout.addWidget(self.cancel_button)

        self.done_button = QPushButton(CameraStartDialog)
        self.done_button.setObjectName(u"done_button")
        self.done_button.setAutoDefault(True)

        self.horizontal_layout.addWidget(self.done_button)


        self.gridLayout_2.addLayout(self.horizontal_layout, 9, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(CameraStartDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.start_combo_box = QComboBox(CameraStartDialog)
        self.start_combo_box.setObjectName(u"start_combo_box")

        self.horizontalLayout_2.addWidget(self.start_combo_box)

        self.horizontalLayout_2.setStretch(1, 1)

        self.gridLayout_2.addLayout(self.horizontalLayout_2, 5, 0, 1, 1)

        self.delete_from_camera_checkbox = QCheckBox(CameraStartDialog)
        self.delete_from_camera_checkbox.setObjectName(u"delete_from_camera_checkbox")

        self.gridLayout_2.addWidget(self.delete_from_camera_checkbox, 6, 0, 1, 1)


        self.retranslateUi(CameraStartDialog)

        self.done_button.setDefault(True)


        QMetaObject.connectSlotsByName(CameraStartDialog)
    # setupUi

    def retranslateUi(self, CameraStartDialog):
        CameraStartDialog.setWindowTitle(QCoreApplication.translate("CameraStartDialog", u"Start Camera", None))
        self.new_images_only.setText(QCoreApplication.translate("CameraStartDialog", u"New images only", None))
        self.include_existing.setText(QCoreApplication.translate("CameraStartDialog", u"Include existing images", None))
        self.cancel_button.setText(QCoreApplication.translate("CameraStartDialog", u"Cancel", None))
        self.done_button.setText(QCoreApplication.translate("CameraStartDialog", u"Start", None))
        self.label.setText(QCoreApplication.translate("CameraStartDialog", u"Start at", None))
        self.delete_from_camera_checkbox.setText(QCoreApplication.translate("CameraStartDialog", u"Delete from camera after download", None))
    # retranslateUi

