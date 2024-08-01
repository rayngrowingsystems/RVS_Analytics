# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SelectImageDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_SelectImageDialog(object):
    def setupUi(self, SelectImageDialog):
        if not SelectImageDialog.objectName():
            SelectImageDialog.setObjectName(u"SelectImageDialog")
        SelectImageDialog.resize(317, 222)
        self.gridLayout_2 = QGridLayout(SelectImageDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.imageFrom_camera_button = QPushButton(SelectImageDialog)
        self.imageFrom_camera_button.setObjectName(u"imageFrom_camera_button")
        self.imageFrom_camera_button.setAutoDefault(False)

        self.gridLayout.addWidget(self.imageFrom_camera_button, 2, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 5, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.cancel_button = QPushButton(SelectImageDialog)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setAutoDefault(False)

        self.gridLayout.addWidget(self.cancel_button, 4, 1, 1, 1)

        self.existing_image_button = QPushButton(SelectImageDialog)
        self.existing_image_button.setObjectName(u"existing_image_button")
        self.existing_image_button.setAutoDefault(False)

        self.gridLayout.addWidget(self.existing_image_button, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 3, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(SelectImageDialog)
        self.cancel_button.clicked.connect(SelectImageDialog.reject)

        self.existing_image_button.setDefault(True)


        QMetaObject.connectSlotsByName(SelectImageDialog)
    # setupUi

    def retranslateUi(self, SelectImageDialog):
        SelectImageDialog.setWindowTitle(QCoreApplication.translate("SelectImageDialog", u"Select Image", None))
        self.imageFrom_camera_button.setText(QCoreApplication.translate("SelectImageDialog", u"Fetch image from camera", None))
        self.cancel_button.setText(QCoreApplication.translate("SelectImageDialog", u"Cancel", None))
        self.existing_image_button.setText(QCoreApplication.translate("SelectImageDialog", u"Pick existing image", None))
    # retranslateUi

