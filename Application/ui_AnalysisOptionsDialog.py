# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AnalysisOptionsDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox,
    QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_AnalysisOptionsDialog(object):
    def setupUi(self, AnalysisOptionsDialog):
        if not AnalysisOptionsDialog.objectName():
            AnalysisOptionsDialog.setObjectName(u"AnalysisOptionsDialog")
        AnalysisOptionsDialog.setWindowModality(Qt.NonModal)
        AnalysisOptionsDialog.resize(948, 548)
        AnalysisOptionsDialog.setModal(True)
        self.gridLayout = QGridLayout(AnalysisOptionsDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.main_groupbox = QGroupBox(AnalysisOptionsDialog)
        self.main_groupbox.setObjectName(u"main_groupbox")

        self.verticalLayout.addWidget(self.main_groupbox)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.default_button = QPushButton(AnalysisOptionsDialog)
        self.default_button.setObjectName(u"default_button")
        self.default_button.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.default_button)

        self.done_button = QPushButton(AnalysisOptionsDialog)
        self.done_button.setObjectName(u"done_button")
        self.done_button.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.done_button)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)


        self.retranslateUi(AnalysisOptionsDialog)
        self.done_button.clicked.connect(AnalysisOptionsDialog.accept)

        self.done_button.setDefault(True)


        QMetaObject.connectSlotsByName(AnalysisOptionsDialog)
    # setupUi

    def retranslateUi(self, AnalysisOptionsDialog):
        AnalysisOptionsDialog.setWindowTitle(QCoreApplication.translate("AnalysisOptionsDialog", u"Analytic options", None))
        self.main_groupbox.setTitle(QCoreApplication.translate("AnalysisOptionsDialog", u"Select script and chart options", None))
        self.default_button.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Default", None))
        self.done_button.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Done", None))
    # retranslateUi

