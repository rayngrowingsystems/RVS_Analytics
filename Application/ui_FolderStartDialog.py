# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FolderStartDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_FolderStartDialog(object):
    def setupUi(self, FolderStartDialog):
        if not FolderStartDialog.objectName():
            FolderStartDialog.setObjectName(u"FolderStartDialog")
        FolderStartDialog.resize(338, 181)
        self.gridLayout_2 = QGridLayout(FolderStartDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 7, 0, 1, 1)

        self.new_images_only = QRadioButton(FolderStartDialog)
        self.new_images_only.setObjectName(u"new_images_only")
        self.new_images_only.setChecked(True)

        self.gridLayout_2.addWidget(self.new_images_only, 0, 0, 1, 1)

        self.line = QFrame(FolderStartDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 1)

        self.include_existing = QRadioButton(FolderStartDialog)
        self.include_existing.setObjectName(u"include_existing")

        self.gridLayout_2.addWidget(self.include_existing, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.cancel_button = QPushButton(FolderStartDialog)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.cancel_button)

        self.done_button = QPushButton(FolderStartDialog)
        self.done_button.setObjectName(u"done_button")
        self.done_button.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.done_button)


        self.gridLayout_2.addLayout(self.horizontalLayout, 9, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.gridLayout_2.addLayout(self.horizontalLayout_2, 5, 0, 1, 1)


        self.retranslateUi(FolderStartDialog)

        self.done_button.setDefault(True)


        QMetaObject.connectSlotsByName(FolderStartDialog)
    # setupUi

    def retranslateUi(self, FolderStartDialog):
        FolderStartDialog.setWindowTitle(QCoreApplication.translate("FolderStartDialog", u"Start Folder", None))
        self.new_images_only.setText(QCoreApplication.translate("FolderStartDialog", u"New images only", None))
        self.include_existing.setText(QCoreApplication.translate("FolderStartDialog", u"All images", None))
        self.cancel_button.setText(QCoreApplication.translate("FolderStartDialog", u"Cancel", None))
        self.done_button.setText(QCoreApplication.translate("FolderStartDialog", u"Start", None))
    # retranslateUi

