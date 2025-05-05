# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EulaDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QGridLayout,
    QLabel, QPlainTextEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_EulaDialog(object):
    def setupUi(self, EulaDialog):
        if not EulaDialog.objectName():
            EulaDialog.setObjectName(u"EulaDialog")
        EulaDialog.setWindowModality(Qt.NonModal)
        EulaDialog.resize(601, 352)
        EulaDialog.setModal(True)
        self.gridLayout_2 = QGridLayout(EulaDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.eula_plain_text_edit = QPlainTextEdit(EulaDialog)
        self.eula_plain_text_edit.setObjectName(u"eula_plain_text_edit")
        self.eula_plain_text_edit.setReadOnly(True)

        self.gridLayout.addWidget(self.eula_plain_text_edit, 2, 0, 1, 1)

        self.done_button = QPushButton(EulaDialog)
        self.done_button.setObjectName(u"done_button")

        self.gridLayout.addWidget(self.done_button, 5, 1, 1, 1)

        self.label = QLabel(EulaDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.accept_checkbox = QCheckBox(EulaDialog)
        self.accept_checkbox.setObjectName(u"accept_checkbox")

        self.gridLayout.addWidget(self.accept_checkbox, 5, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(EulaDialog)

        self.done_button.setDefault(True)


        QMetaObject.connectSlotsByName(EulaDialog)
    # setupUi

    def retranslateUi(self, EulaDialog):
        EulaDialog.setWindowTitle(QCoreApplication.translate("EulaDialog", u"End-user license agreement", None))
        self.done_button.setText(QCoreApplication.translate("EulaDialog", u"Done", None))
        self.label.setText(QCoreApplication.translate("EulaDialog", u"<html><head/><body><p>Read and accept the end-user license agreement</p></body></html>", None))
        self.accept_checkbox.setText(QCoreApplication.translate("EulaDialog", u"Accept end-user license agreement", None))
    # retranslateUi

