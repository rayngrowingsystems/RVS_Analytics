# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ImageMaskDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from ClickableLabel import ClickableLabel
from Label import Label

class Ui_ImageMaskDialog(object):
    def setupUi(self, ImageMaskDialog):
        if not ImageMaskDialog.objectName():
            ImageMaskDialog.setObjectName(u"ImageMaskDialog")
        ImageMaskDialog.setWindowModality(Qt.NonModal)
        ImageMaskDialog.resize(628, 660)
        ImageMaskDialog.setModal(True)
        self.gridLayout_2 = QGridLayout(ImageMaskDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.script_label = QLabel(ImageMaskDialog)
        self.script_label.setObjectName(u"script_label")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.script_label.setFont(font)

        self.verticalLayout.addWidget(self.script_label)

        self.script_description = QLabel(ImageMaskDialog)
        self.script_description.setObjectName(u"script_description")

        self.verticalLayout.addWidget(self.script_description)

        self.line = QFrame(ImageMaskDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label_3 = QLabel(ImageMaskDialog)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.reference_image1 = ClickableLabel(ImageMaskDialog)
        self.reference_image1.setObjectName(u"reference_image1")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reference_image1.sizePolicy().hasHeightForWidth())
        self.reference_image1.setSizePolicy(sizePolicy)
        self.reference_image1.setMinimumSize(QSize(300, 200))
        self.reference_image1.setFrameShape(QFrame.Box)
        self.reference_image1.setScaledContents(False)
        self.reference_image1.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_2.addWidget(self.reference_image1)

        self.reference_image2 = ClickableLabel(ImageMaskDialog)
        self.reference_image2.setObjectName(u"reference_image2")
        sizePolicy.setHeightForWidth(self.reference_image2.sizePolicy().hasHeightForWidth())
        self.reference_image2.setSizePolicy(sizePolicy)
        self.reference_image2.setMinimumSize(QSize(300, 200))
        self.reference_image2.setFrameShape(QFrame.Box)
        self.reference_image2.setScaledContents(False)
        self.reference_image2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_2.addWidget(self.reference_image2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.label_4 = QLabel(ImageMaskDialog)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.preview_image1 = Label(ImageMaskDialog)
        self.preview_image1.setObjectName(u"preview_image1")
        sizePolicy.setHeightForWidth(self.preview_image1.sizePolicy().hasHeightForWidth())
        self.preview_image1.setSizePolicy(sizePolicy)
        self.preview_image1.setMinimumSize(QSize(300, 200))
        self.preview_image1.setFrameShape(QFrame.Box)
        self.preview_image1.setScaledContents(False)
        self.preview_image1.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout.addWidget(self.preview_image1)

        self.preview_image2 = Label(ImageMaskDialog)
        self.preview_image2.setObjectName(u"preview_image2")
        sizePolicy.setHeightForWidth(self.preview_image2.sizePolicy().hasHeightForWidth())
        self.preview_image2.setSizePolicy(sizePolicy)
        self.preview_image2.setMinimumSize(QSize(300, 200))
        self.preview_image2.setFrameShape(QFrame.Box)
        self.preview_image2.setScaledContents(False)
        self.preview_image2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout.addWidget(self.preview_image2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.main_box = QWidget(ImageMaskDialog)
        self.main_box.setObjectName(u"main_box")

        self.horizontalLayout_4.addWidget(self.main_box)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.show_rois_checkbox = QCheckBox(ImageMaskDialog)
        self.show_rois_checkbox.setObjectName(u"show_rois_checkbox")

        self.verticalLayout_3.addWidget(self.show_rois_checkbox)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.default_button = QPushButton(ImageMaskDialog)
        self.default_button.setObjectName(u"default_button")
        self.default_button.setAutoDefault(False)

        self.verticalLayout_3.addWidget(self.default_button)

        self.cancel_button = QPushButton(ImageMaskDialog)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setAutoDefault(False)

        self.verticalLayout_3.addWidget(self.cancel_button)

        self.done_button = QPushButton(ImageMaskDialog)
        self.done_button.setObjectName(u"done_button")
        self.done_button.setAutoDefault(True)

        self.verticalLayout_3.addWidget(self.done_button)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout_4.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalLayout.setStretch(4, 2)
        self.verticalLayout.setStretch(6, 2)

        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(ImageMaskDialog)
        self.done_button.clicked.connect(ImageMaskDialog.accept)

        self.done_button.setDefault(False)


        QMetaObject.connectSlotsByName(ImageMaskDialog)
    # setupUi

    def retranslateUi(self, ImageMaskDialog):
        ImageMaskDialog.setWindowTitle(QCoreApplication.translate("ImageMaskDialog", u"Mask", None))
        self.script_label.setText("")
        self.script_description.setText("")
        self.label_3.setText(QCoreApplication.translate("ImageMaskDialog", u"Pick one or two reference images", None))
        self.reference_image1.setText(QCoreApplication.translate("ImageMaskDialog", u"\n"
"\n"
"Click the Image button to pick", None))
        self.reference_image2.setText(QCoreApplication.translate("ImageMaskDialog", u"\n"
"\n"
"Click the Image button to pick", None))
        self.label_4.setText(QCoreApplication.translate("ImageMaskDialog", u"Preview", None))
        self.preview_image1.setText(QCoreApplication.translate("ImageMaskDialog", u"Preview 1", None))
        self.preview_image2.setText(QCoreApplication.translate("ImageMaskDialog", u"Preview 2", None))
        self.show_rois_checkbox.setText(QCoreApplication.translate("ImageMaskDialog", u"Show ROIs", None))
        self.default_button.setText(QCoreApplication.translate("ImageMaskDialog", u"Default", None))
        self.cancel_button.setText(QCoreApplication.translate("ImageMaskDialog", u"Cancel", None))
        self.done_button.setText(QCoreApplication.translate("ImageMaskDialog", u"Done", None))
    # retranslateUi

