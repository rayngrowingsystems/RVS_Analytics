# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AnalysisPreviewDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from ClickableLabel import ClickableLabel

class Ui_AnalysisPreviewDialog(object):
    def setupUi(self, AnalysisPreviewDialog):
        if not AnalysisPreviewDialog.objectName():
            AnalysisPreviewDialog.setObjectName(u"AnalysisPreviewDialog")
        AnalysisPreviewDialog.setWindowModality(Qt.NonModal)
        AnalysisPreviewDialog.resize(628, 605)
        AnalysisPreviewDialog.setModal(True)
        self.gridLayout_3 = QGridLayout(AnalysisPreviewDialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.script_label = QLabel(AnalysisPreviewDialog)
        self.script_label.setObjectName(u"script_label")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.script_label.setFont(font)

        self.verticalLayout.addWidget(self.script_label)

        self.script_description = QLabel(AnalysisPreviewDialog)
        self.script_description.setObjectName(u"script_description")

        self.verticalLayout.addWidget(self.script_description)

        self.line = QFrame(AnalysisPreviewDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label = QLabel(AnalysisPreviewDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.reference_image1 = ClickableLabel(AnalysisPreviewDialog)
        self.reference_image1.setObjectName(u"reference_image1")
        self.reference_image1.setMinimumSize(QSize(300, 200))
        self.reference_image1.setFrameShape(QFrame.Box)

        self.horizontalLayout.addWidget(self.reference_image1)

        self.reference_image2 = ClickableLabel(AnalysisPreviewDialog)
        self.reference_image2.setObjectName(u"reference_image2")
        self.reference_image2.setMinimumSize(QSize(300, 200))
        self.reference_image2.setFrameShape(QFrame.Box)

        self.horizontalLayout.addWidget(self.reference_image2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_3 = QLabel(AnalysisPreviewDialog)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.preview_image1 = QLabel(AnalysisPreviewDialog)
        self.preview_image1.setObjectName(u"preview_image1")
        self.preview_image1.setMinimumSize(QSize(300, 200))
        self.preview_image1.setFrameShape(QFrame.Box)

        self.horizontalLayout_2.addWidget(self.preview_image1)

        self.preview_image2 = QLabel(AnalysisPreviewDialog)
        self.preview_image2.setObjectName(u"preview_image2")
        self.preview_image2.setMinimumSize(QSize(300, 200))
        self.preview_image2.setFrameShape(QFrame.Box)

        self.horizontalLayout_2.addWidget(self.preview_image2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.preview_button = QPushButton(AnalysisPreviewDialog)
        self.preview_button.setObjectName(u"preview_button")

        self.verticalLayout.addWidget(self.preview_button)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.done_button = QPushButton(AnalysisPreviewDialog)
        self.done_button.setObjectName(u"done_button")
        self.done_button.setAutoDefault(True)

        self.verticalLayout_3.addWidget(self.done_button)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalLayout.setStretch(8, 1)

        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(AnalysisPreviewDialog)
        self.done_button.clicked.connect(AnalysisPreviewDialog.accept)

        self.done_button.setDefault(True)


        QMetaObject.connectSlotsByName(AnalysisPreviewDialog)
    # setupUi

    def retranslateUi(self, AnalysisPreviewDialog):
        AnalysisPreviewDialog.setWindowTitle(QCoreApplication.translate("AnalysisPreviewDialog", u"Analytic preview", None))
        self.script_label.setText("")
        self.script_description.setText("")
        self.label.setText(QCoreApplication.translate("AnalysisPreviewDialog", u"Pick one or two reference images", None))
        self.reference_image1.setText(QCoreApplication.translate("AnalysisPreviewDialog", u"\n"
"\n"
"Click the Image button to pick", None))
        self.reference_image2.setText(QCoreApplication.translate("AnalysisPreviewDialog", u"\n"
"\n"
"Click the Image button to pick", None))
        self.label_3.setText(QCoreApplication.translate("AnalysisPreviewDialog", u"Preview", None))
        self.preview_image1.setText("")
        self.preview_image2.setText("")
        self.preview_button.setText(QCoreApplication.translate("AnalysisPreviewDialog", u"Create Preview", None))
        self.done_button.setText(QCoreApplication.translate("AnalysisPreviewDialog", u"Done", None))
    # retranslateUi
