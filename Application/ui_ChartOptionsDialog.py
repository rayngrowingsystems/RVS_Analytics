# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ChartOptionsDialog.ui'
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

class Ui_ChartOptionsDialog(object):
    def setupUi(self, ChartOptionsDialog):
        if not ChartOptionsDialog.objectName():
            ChartOptionsDialog.setObjectName(u"ChartOptionsDialog")
        ChartOptionsDialog.setWindowModality(Qt.NonModal)
        ChartOptionsDialog.resize(619, 354)
        ChartOptionsDialog.setModal(True)
        self.gridLayout_3 = QGridLayout(ChartOptionsDialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.chart_options_box = QGroupBox(ChartOptionsDialog)
        self.chart_options_box.setObjectName(u"chart_options_box")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chart_options_box.sizePolicy().hasHeightForWidth())
        self.chart_options_box.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.chart_options_box)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.doneButton = QPushButton(ChartOptionsDialog)
        self.doneButton.setObjectName(u"doneButton")
        self.doneButton.setAutoDefault(True)

        self.verticalLayout_3.addWidget(self.doneButton)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout_4.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalLayout.setStretch(0, 1)

        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(ChartOptionsDialog)
        self.doneButton.clicked.connect(ChartOptionsDialog.accept)

        self.doneButton.setDefault(True)


        QMetaObject.connectSlotsByName(ChartOptionsDialog)
    # setupUi

    def retranslateUi(self, ChartOptionsDialog):
        ChartOptionsDialog.setWindowTitle(QCoreApplication.translate("ChartOptionsDialog", u"Chart options", None))
        self.chart_options_box.setTitle(QCoreApplication.translate("ChartOptionsDialog", u"Select chart options", None))
        self.doneButton.setText(QCoreApplication.translate("ChartOptionsDialog", u"Done", None))
    # retranslateUi

