# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ImageOptionDialog.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QWidget)

class Ui_ImageOptionDialog(object):
    def setupUi(self, ImageOptionDialog):
        if not ImageOptionDialog.objectName():
            ImageOptionDialog.setObjectName(u"ImageOptionDialog")
        ImageOptionDialog.setWindowModality(Qt.NonModal)
        ImageOptionDialog.resize(582, 249)
        ImageOptionDialog.setModal(True)
        self.gridLayout_2 = QGridLayout(ImageOptionDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.normalize_checkbox = QCheckBox(ImageOptionDialog)
        self.normalize_checkbox.setObjectName(u"normalize_checkbox")

        self.gridLayout.addWidget(self.normalize_checkbox, 5, 0, 1, 1)

        self.light_correction_checkbox = QCheckBox(ImageOptionDialog)
        self.light_correction_checkbox.setObjectName(u"light_correction_checkbox")

        self.gridLayout.addWidget(self.light_correction_checkbox, 8, 0, 1, 1)

        self.line_2 = QFrame(ImageOptionDialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 6, 0, 1, 1)

        self.label_3 = QLabel(ImageOptionDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)

        self.label_2 = QLabel(ImageOptionDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)

        self.label = QLabel(ImageOptionDialog)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.line = QFrame(ImageOptionDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 3, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_4 = QLabel(ImageOptionDialog)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_7.addWidget(self.label_4)

        self.lens_angle_combobox = QComboBox(ImageOptionDialog)
        self.lens_angle_combobox.addItem("")
        self.lens_angle_combobox.addItem("")
        self.lens_angle_combobox.addItem("")
        self.lens_angle_combobox.setObjectName(u"lens_angle_combobox")
        self.lens_angle_combobox.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_7.addWidget(self.lens_angle_combobox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(ImageOptionDialog)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout.addWidget(self.label_5)

        self.rotation_spinbox = QSpinBox(ImageOptionDialog)
        self.rotation_spinbox.setObjectName(u"rotation_spinbox")
        self.rotation_spinbox.setMaximum(359)
        self.rotation_spinbox.setSingleStep(1)

        self.horizontalLayout.addWidget(self.rotation_spinbox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.gridLayout.addLayout(self.horizontalLayout, 12, 0, 1, 1)

        self.line_3 = QFrame(ImageOptionDialog)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_3, 9, 0, 1, 1)

        self.label_6 = QLabel(ImageOptionDialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 10, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.crop_checkbox = QCheckBox(ImageOptionDialog)
        self.crop_checkbox.setObjectName(u"crop_checkbox")

        self.horizontalLayout_3.addWidget(self.crop_checkbox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.done_button = QPushButton(ImageOptionDialog)
        self.done_button.setObjectName(u"done_button")

        self.horizontalLayout_3.addWidget(self.done_button)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)


        self.retranslateUi(ImageOptionDialog)

        self.done_button.setDefault(True)


        QMetaObject.connectSlotsByName(ImageOptionDialog)
    # setupUi

    def retranslateUi(self, ImageOptionDialog):
        ImageOptionDialog.setWindowTitle(QCoreApplication.translate("ImageOptionDialog", u"Image Options", None))
        self.normalize_checkbox.setText(QCoreApplication.translate("ImageOptionDialog", u"Normalize", None))
        self.light_correction_checkbox.setText(QCoreApplication.translate("ImageOptionDialog", u"Apply Light Intensity Correction for RAYN Vision Systems with 120\u00b0 lens", None))
        self.label_3.setText(QCoreApplication.translate("ImageOptionDialog", u"[Experimental] Correct image for light intensity", None))
        self.label_2.setText(QCoreApplication.translate("ImageOptionDialog", u"Use the dark reference to normalize the multispectral image", None))
        self.label.setText(QCoreApplication.translate("ImageOptionDialog", u"The RAYN Vision System Camera optical system is calibrated and it is possible to compensate images taken by this camera for for lens distortion", None))
        self.label_4.setText(QCoreApplication.translate("ImageOptionDialog", u"Select Lens Angle", None))
        self.lens_angle_combobox.setItemText(0, QCoreApplication.translate("ImageOptionDialog", u"No compensation", None))
        self.lens_angle_combobox.setItemText(1, QCoreApplication.translate("ImageOptionDialog", u"60\u00b0", None))
        self.lens_angle_combobox.setItemText(2, QCoreApplication.translate("ImageOptionDialog", u"120\u00b0 (legacy)", None))

        self.label_5.setText(QCoreApplication.translate("ImageOptionDialog", u"Rotation Angle (counter clockwise)", None))
        self.label_6.setText(QCoreApplication.translate("ImageOptionDialog", u"Rotate the image", None))
        self.crop_checkbox.setText(QCoreApplication.translate("ImageOptionDialog", u"Crop rotated image to original image dimension", None))
        self.done_button.setText(QCoreApplication.translate("ImageOptionDialog", u"Done", None))
    # retranslateUi

