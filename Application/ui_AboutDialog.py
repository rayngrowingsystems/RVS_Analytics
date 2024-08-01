# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AboutDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QPlainTextEdit, QPushButton, QSizePolicy, QWidget)

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.setWindowModality(Qt.NonModal)
        AboutDialog.resize(601, 352)
        AboutDialog.setModal(True)
        self.gridLayout_2 = QGridLayout(AboutDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.eula_plain_text_edit = QPlainTextEdit(AboutDialog)
        self.eula_plain_text_edit.setObjectName(u"eula_plain_text_edit")
        self.eula_plain_text_edit.setReadOnly(True)

        self.gridLayout.addWidget(self.eula_plain_text_edit, 6, 0, 1, 1)

        self.label_4 = QLabel(AboutDialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.version_label = QLabel(AboutDialog)
        self.version_label.setObjectName(u"version_label")

        self.gridLayout.addWidget(self.version_label, 2, 0, 1, 1)

        self.done_button = QPushButton(AboutDialog)
        self.done_button.setObjectName(u"done_button")

        self.gridLayout.addWidget(self.done_button, 9, 1, 1, 1)

        self.license_link = QLabel(AboutDialog)
        self.license_link.setObjectName(u"license_link")

        self.gridLayout.addWidget(self.license_link, 3, 0, 1, 1)

        self.label = QLabel(AboutDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.privacy_link = QLabel(AboutDialog)
        self.privacy_link.setObjectName(u"privacy_link")

        self.gridLayout.addWidget(self.privacy_link, 4, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(AboutDialog)

        self.done_button.setDefault(True)


        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QCoreApplication.translate("AboutDialog", u"About", None))
        self.label_4.setText(QCoreApplication.translate("AboutDialog", u"EULA:", None))
        self.version_label.setText("")
        self.done_button.setText(QCoreApplication.translate("AboutDialog", u"Done", None))
        self.license_link.setText(QCoreApplication.translate("AboutDialog", u"<html><head/><body><p><span style=\" text-decoration: underline;\">etcconnect.com/Licenses</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("AboutDialog", u"<html><head/><body><p><span style=\" font-weight:700;\">RAYN Vision System</span></p></body></html>", None))
        self.privacy_link.setText(QCoreApplication.translate("AboutDialog", u"<html><head/><body><p><span style=\" text-decoration: underline;\">etcconnect.com/Privacy-Policy-and-Terms-of-Use-and-Acceptable-Use</span></p></body></html>", None))
    # retranslateUi

