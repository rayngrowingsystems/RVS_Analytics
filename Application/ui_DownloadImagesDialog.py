# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DownloadImagesDialog.ui'
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
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_DownloadImagesDialog(object):
    def setupUi(self, DownloadImagesDialog):
        if not DownloadImagesDialog.objectName():
            DownloadImagesDialog.setObjectName(u"DownloadImagesDialog")
        DownloadImagesDialog.resize(396, 238)
        self.gridLayout_2 = QGridLayout(DownloadImagesDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.selected_images_label = QLabel(DownloadImagesDialog)
        self.selected_images_label.setObjectName(u"selected_images_label")

        self.horizontalLayout.addWidget(self.selected_images_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.cancel_button = QPushButton(DownloadImagesDialog)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.cancel_button)

        self.done_button = QPushButton(DownloadImagesDialog)
        self.done_button.setObjectName(u"done_button")
        self.done_button.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.done_button)


        self.gridLayout_2.addLayout(self.horizontalLayout, 11, 0, 1, 1)

        self.label_4 = QLabel(DownloadImagesDialog)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setBold(True)
        self.label_4.setFont(font)

        self.gridLayout_2.addWidget(self.label_4, 7, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 9, 0, 1, 1)

        self.header_text = QLabel(DownloadImagesDialog)
        self.header_text.setObjectName(u"header_text")

        self.gridLayout_2.addWidget(self.header_text, 0, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.browse_button = QPushButton(DownloadImagesDialog)
        self.browse_button.setObjectName(u"browse_button")

        self.horizontalLayout_4.addWidget(self.browse_button)

        self.target_path_label = QLabel(DownloadImagesDialog)
        self.target_path_label.setObjectName(u"target_path_label")

        self.horizontalLayout_4.addWidget(self.target_path_label)

        self.horizontalLayout_4.setStretch(1, 2)

        self.gridLayout_2.addLayout(self.horizontalLayout_4, 8, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 6, 0, 1, 1)

        self.delete_from_camera_checkbox = QCheckBox(DownloadImagesDialog)
        self.delete_from_camera_checkbox.setObjectName(u"delete_from_camera_checkbox")

        self.gridLayout_2.addWidget(self.delete_from_camera_checkbox, 5, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(DownloadImagesDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.start_combo_box = QComboBox(DownloadImagesDialog)
        self.start_combo_box.setObjectName(u"start_combo_box")

        self.horizontalLayout_2.addWidget(self.start_combo_box)

        self.horizontalLayout_2.setStretch(1, 1)

        self.gridLayout_2.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(DownloadImagesDialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.stop_combo_box = QComboBox(DownloadImagesDialog)
        self.stop_combo_box.setObjectName(u"stop_combo_box")

        self.horizontalLayout_3.addWidget(self.stop_combo_box)

        self.horizontalLayout_3.setStretch(1, 1)

        self.gridLayout_2.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)


        self.retranslateUi(DownloadImagesDialog)
        self.cancel_button.clicked.connect(DownloadImagesDialog.reject)

        self.done_button.setDefault(True)


        QMetaObject.connectSlotsByName(DownloadImagesDialog)
    # setupUi

    def retranslateUi(self, DownloadImagesDialog):
        DownloadImagesDialog.setWindowTitle(QCoreApplication.translate("DownloadImagesDialog", u"Download Images", None))
        self.selected_images_label.setText(QCoreApplication.translate("DownloadImagesDialog", u"Selected images:", None))
        self.cancel_button.setText(QCoreApplication.translate("DownloadImagesDialog", u"Cancel", None))
        self.done_button.setText(QCoreApplication.translate("DownloadImagesDialog", u"Download", None))
        self.label_4.setText(QCoreApplication.translate("DownloadImagesDialog", u"Target folder", None))
        self.header_text.setText(QCoreApplication.translate("DownloadImagesDialog", u"Download multiple images from camera", None))
        self.browse_button.setText(QCoreApplication.translate("DownloadImagesDialog", u"Browse...", None))
        self.target_path_label.setText("")
        self.delete_from_camera_checkbox.setText(QCoreApplication.translate("DownloadImagesDialog", u"Delete from camera after download", None))
        self.label.setText(QCoreApplication.translate("DownloadImagesDialog", u"Start at", None))
        self.label_2.setText(QCoreApplication.translate("DownloadImagesDialog", u"Stop at", None))
    # retranslateUi

