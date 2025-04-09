# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsDialog.ui'
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
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(538, 321)
        self.gridLayout_2 = QGridLayout(SettingsDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(SettingsDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.theme_combo_box = QComboBox(SettingsDialog)
        self.theme_combo_box.addItem("")
        self.theme_combo_box.addItem("")
        self.theme_combo_box.addItem("")
        self.theme_combo_box.setObjectName(u"theme_combo_box")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.theme_combo_box.sizePolicy().hasHeightForWidth())
        self.theme_combo_box.setSizePolicy(sizePolicy)
        self.theme_combo_box.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_2.addWidget(self.theme_combo_box)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.line = QFrame(SettingsDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.groupBox = QGroupBox(SettingsDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.ip_lineedit = QLineEdit(self.groupBox)
        self.ip_lineedit.setObjectName(u"ip_lineedit")

        self.gridLayout.addWidget(self.ip_lineedit, 0, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)

        self.port_lineedit = QLineEdit(self.groupBox)
        self.port_lineedit.setObjectName(u"port_lineedit")

        self.gridLayout.addWidget(self.port_lineedit, 1, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.username_lineedit = QLineEdit(self.groupBox)
        self.username_lineedit.setObjectName(u"username_lineedit")

        self.gridLayout.addWidget(self.username_lineedit, 2, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.password_lineedit = QLineEdit(self.groupBox)
        self.password_lineedit.setObjectName(u"password_lineedit")

        self.gridLayout.addWidget(self.password_lineedit, 3, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.cancel_button = QPushButton(SettingsDialog)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.cancel_button)

        self.done_button = QPushButton(SettingsDialog)
        self.done_button.setObjectName(u"done_button")
        self.done_button.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.done_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout.setStretch(2, 1)

        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(SettingsDialog)

        self.done_button.setDefault(True)


        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Settings", None))
        self.label.setText(QCoreApplication.translate("SettingsDialog", u"Theme", None))
        self.theme_combo_box.setItemText(0, QCoreApplication.translate("SettingsDialog", u"Auto", None))
        self.theme_combo_box.setItemText(1, QCoreApplication.translate("SettingsDialog", u"Light", None))
        self.theme_combo_box.setItemText(2, QCoreApplication.translate("SettingsDialog", u"Dark", None))

        self.groupBox.setTitle(QCoreApplication.translate("SettingsDialog", u"MQTT Broker", None))
        self.label_3.setText(QCoreApplication.translate("SettingsDialog", u"IP address", None))
        self.label_6.setText(QCoreApplication.translate("SettingsDialog", u"Port", None))
        self.label_4.setText(QCoreApplication.translate("SettingsDialog", u"User name", None))
        self.label_5.setText(QCoreApplication.translate("SettingsDialog", u"Password", None))
        self.cancel_button.setText(QCoreApplication.translate("SettingsDialog", u"Cancel", None))
        self.done_button.setText(QCoreApplication.translate("SettingsDialog", u"Done", None))
    # retranslateUi

