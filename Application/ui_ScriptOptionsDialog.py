# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ScriptOptionsDialog.ui'
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
    QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from ClickableLabel import ClickableLabel
import CameraApp_rc

class Ui_ScriptOptionsDialog(object):
    def setupUi(self, ScriptOptionsDialog):
        if not ScriptOptionsDialog.objectName():
            ScriptOptionsDialog.setObjectName(u"ScriptOptionsDialog")
        ScriptOptionsDialog.setWindowModality(Qt.NonModal)
        ScriptOptionsDialog.resize(619, 354)
        ScriptOptionsDialog.setModal(True)
        self.gridLayout_3 = QGridLayout(ScriptOptionsDialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.script_label = QLabel(ScriptOptionsDialog)
        self.script_label.setObjectName(u"script_label")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.script_label.setFont(font)

        self.verticalLayout.addWidget(self.script_label)

        self.script_description = QLabel(ScriptOptionsDialog)
        self.script_description.setObjectName(u"script_description")

        self.verticalLayout.addWidget(self.script_description)

        self.line = QFrame(ScriptOptionsDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label = QLabel(ScriptOptionsDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.reference_image1 = ClickableLabel(ScriptOptionsDialog)
        self.reference_image1.setObjectName(u"reference_image1")
        self.reference_image1.setMinimumSize(QSize(300, 200))
        self.reference_image1.setFrameShape(QFrame.Box)

        self.horizontalLayout.addWidget(self.reference_image1)

        self.reference_image2 = ClickableLabel(ScriptOptionsDialog)
        self.reference_image2.setObjectName(u"reference_image2")
        self.reference_image2.setMinimumSize(QSize(300, 200))
        self.reference_image2.setFrameShape(QFrame.Box)

        self.horizontalLayout.addWidget(self.reference_image2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_3 = QLabel(ScriptOptionsDialog)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.preview_image1 = QLabel(ScriptOptionsDialog)
        self.preview_image1.setObjectName(u"preview_image1")
        self.preview_image1.setMinimumSize(QSize(300, 200))
        self.preview_image1.setFrameShape(QFrame.Box)

        self.horizontalLayout_2.addWidget(self.preview_image1)

        self.preview_image2 = QLabel(ScriptOptionsDialog)
        self.preview_image2.setObjectName(u"preview_image2")
        self.preview_image2.setMinimumSize(QSize(300, 200))
        self.preview_image2.setFrameShape(QFrame.Box)

        self.horizontalLayout_2.addWidget(self.preview_image2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.script_options_box = QGroupBox(ScriptOptionsDialog)
        self.script_options_box.setObjectName(u"script_options_box")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.script_options_box.sizePolicy().hasHeightForWidth())
        self.script_options_box.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.script_options_box)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.preview_button = QPushButton(ScriptOptionsDialog)
        self.preview_button.setObjectName(u"preview_button")
        icon = QIcon()
        icon.addFile(u":/images/Refresh.png", QSize(), QIcon.Normal, QIcon.Off)
        self.preview_button.setIcon(icon)

        self.verticalLayout_3.addWidget(self.preview_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.done_button = QPushButton(ScriptOptionsDialog)
        self.done_button.setObjectName(u"done_button")
        self.done_button.setAutoDefault(True)

        self.verticalLayout_3.addWidget(self.done_button)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout_4.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalLayout.setStretch(7, 1)

        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(ScriptOptionsDialog)
        self.done_button.clicked.connect(ScriptOptionsDialog.accept)

        self.done_button.setDefault(True)


        QMetaObject.connectSlotsByName(ScriptOptionsDialog)
    # setupUi

    def retranslateUi(self, ScriptOptionsDialog):
        ScriptOptionsDialog.setWindowTitle(QCoreApplication.translate("ScriptOptionsDialog", u"Script options", None))
        self.script_label.setText("")
        self.script_description.setText("")
        self.label.setText(QCoreApplication.translate("ScriptOptionsDialog", u"Pick one or two reference images", None))
        self.reference_image1.setText(QCoreApplication.translate("ScriptOptionsDialog", u"\n"
"\n"
"Click the Image button to pick", None))
        self.reference_image2.setText(QCoreApplication.translate("ScriptOptionsDialog", u"\n"
"\n"
"Click the Image button to pick", None))
        self.label_3.setText(QCoreApplication.translate("ScriptOptionsDialog", u"Preview", None))
        self.preview_image1.setText("")
        self.preview_image2.setText("")
        self.script_options_box.setTitle(QCoreApplication.translate("ScriptOptionsDialog", u"Select script options", None))
        self.preview_button.setText(QCoreApplication.translate("ScriptOptionsDialog", u"Preview", None))
        self.done_button.setText(QCoreApplication.translate("ScriptOptionsDialog", u"Done", None))
    # retranslateUi

