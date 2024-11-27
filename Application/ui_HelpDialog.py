# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HelpDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_HelpDialog(object):
    def setupUi(self, HelpDialog):
        if not HelpDialog.objectName():
            HelpDialog.setObjectName(u"HelpDialog")
        HelpDialog.setWindowModality(Qt.NonModal)
        HelpDialog.resize(1059, 598)
        HelpDialog.setModal(True)
        self.gridLayout = QGridLayout(HelpDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.home_button = QPushButton(HelpDialog)
        self.home_button.setObjectName(u"home_button")
        self.home_button.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.home_button)

        self.back_button = QPushButton(HelpDialog)
        self.back_button.setObjectName(u"back_button")
        self.back_button.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.back_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.help_widget = QWidget(HelpDialog)
        self.help_widget.setObjectName(u"help_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.help_widget.sizePolicy().hasHeightForWidth())
        self.help_widget.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.help_widget, 1, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.done_button = QPushButton(HelpDialog)
        self.done_button.setObjectName(u"done_button")

        self.horizontalLayout_3.addWidget(self.done_button)


        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)


        self.retranslateUi(HelpDialog)

        self.done_button.setDefault(True)


        QMetaObject.connectSlotsByName(HelpDialog)
    # setupUi

    def retranslateUi(self, HelpDialog):
        HelpDialog.setWindowTitle(QCoreApplication.translate("HelpDialog", u"Help", None))
        self.home_button.setText(QCoreApplication.translate("HelpDialog", u"Home", None))
        self.back_button.setText(QCoreApplication.translate("HelpDialog", u"Back", None))
        self.done_button.setText(QCoreApplication.translate("HelpDialog", u"Done", None))
    # retranslateUi

