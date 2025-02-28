# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DeleteImagesDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_DeleteImagesDialog(object):
    def setupUi(self, DeleteImagesDialog):
        if not DeleteImagesDialog.objectName():
            DeleteImagesDialog.setObjectName(u"DeleteImagesDialog")
        DeleteImagesDialog.resize(396, 238)
        self.gridLayout_2 = QGridLayout(DeleteImagesDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.header_text = QLabel(DeleteImagesDialog)
        self.header_text.setObjectName(u"header_text")

        self.gridLayout_2.addWidget(self.header_text, 0, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")

        self.gridLayout_2.addLayout(self.horizontalLayout_4, 6, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(DeleteImagesDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.start_combo_box = QComboBox(DeleteImagesDialog)
        self.start_combo_box.setObjectName(u"start_combo_box")

        self.horizontalLayout_2.addWidget(self.start_combo_box)

        self.horizontalLayout_2.setStretch(1, 1)

        self.gridLayout_2.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.selected_images_label = QLabel(DeleteImagesDialog)
        self.selected_images_label.setObjectName(u"selected_images_label")

        self.horizontalLayout.addWidget(self.selected_images_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.cancel_button = QPushButton(DeleteImagesDialog)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.cancel_button)

        self.done_button = QPushButton(DeleteImagesDialog)
        self.done_button.setObjectName(u"done_button")
        self.done_button.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.done_button)


        self.gridLayout_2.addLayout(self.horizontalLayout, 8, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 5, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(DeleteImagesDialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.stop_combo_box = QComboBox(DeleteImagesDialog)
        self.stop_combo_box.setObjectName(u"stop_combo_box")

        self.horizontalLayout_3.addWidget(self.stop_combo_box)

        self.horizontalLayout_3.setStretch(1, 1)

        self.gridLayout_2.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)


        self.retranslateUi(DeleteImagesDialog)
        self.cancel_button.clicked.connect(DeleteImagesDialog.reject)

        self.done_button.setDefault(True)


        QMetaObject.connectSlotsByName(DeleteImagesDialog)
    # setupUi

    def retranslateUi(self, DeleteImagesDialog):
        DeleteImagesDialog.setWindowTitle(QCoreApplication.translate("DeleteImagesDialog", u"Delete Images", None))
        self.header_text.setText(QCoreApplication.translate("DeleteImagesDialog", u"Delete images from camera", None))
        self.label.setText(QCoreApplication.translate("DeleteImagesDialog", u"Start at", None))
        self.selected_images_label.setText(QCoreApplication.translate("DeleteImagesDialog", u"Selected images:", None))
        self.cancel_button.setText(QCoreApplication.translate("DeleteImagesDialog", u"Cancel", None))
        self.done_button.setText(QCoreApplication.translate("DeleteImagesDialog", u"Delete", None))
        self.label_2.setText(QCoreApplication.translate("DeleteImagesDialog", u"Stop at", None))
    # retranslateUi

