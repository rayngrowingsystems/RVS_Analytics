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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_AnalysisOptionsDialog(object):
    def setupUi(self, AnalysisOptionsDialog):
        if not AnalysisOptionsDialog.objectName():
            AnalysisOptionsDialog.setObjectName(u"AnalysisOptionsDialog")
        AnalysisOptionsDialog.setWindowModality(Qt.NonModal)
        AnalysisOptionsDialog.resize(948, 516)
        AnalysisOptionsDialog.setModal(True)
        self.gridLayout_3 = QGridLayout(AnalysisOptionsDialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 4, 0, 1, 1)

        self.script_options_box = QGroupBox(AnalysisOptionsDialog)
        self.script_options_box.setObjectName(u"script_options_box")
        self.script_options_box.setStyleSheet(u"QGroupBox::title{font-size:20pt;}")

        self.gridLayout_3.addWidget(self.script_options_box, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.done_button = QPushButton(AnalysisOptionsDialog)
        self.done_button.setObjectName(u"done_button")

        self.horizontalLayout.addWidget(self.done_button)


        self.gridLayout_3.addLayout(self.horizontalLayout, 5, 0, 1, 1)

        self.chart_options_box = QGroupBox(AnalysisOptionsDialog)
        self.chart_options_box.setObjectName(u"chart_options_box")
        self.gridLayout_2 = QGridLayout(self.chart_options_box)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.index_box = QGroupBox(self.chart_options_box)
        self.index_box.setObjectName(u"index_box")
        self.gridLayout_5 = QGridLayout(self.index_box)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.false_color_image_checkbox = QCheckBox(self.index_box)
        self.false_color_image_checkbox.setObjectName(u"false_color_image_checkbox")

        self.gridLayout_5.addWidget(self.false_color_image_checkbox, 1, 0, 1, 1)

        self.mean_index_checkbox = QCheckBox(self.index_box)
        self.mean_index_checkbox.setObjectName(u"mean_index_checkbox")

        self.gridLayout_5.addWidget(self.mean_index_checkbox, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.index_box, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.reflectance_box = QGroupBox(self.chart_options_box)
        self.reflectance_box.setObjectName(u"reflectance_box")
        self.gridLayout_6 = QGridLayout(self.reflectance_box)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.spectral_signature_checkbox = QCheckBox(self.reflectance_box)
        self.spectral_signature_checkbox.setObjectName(u"spectral_signature_checkbox")

        self.gridLayout_6.addWidget(self.spectral_signature_checkbox, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.reflectance_box, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)

        self.shape_box = QGroupBox(self.chart_options_box)
        self.shape_box.setObjectName(u"shape_box")
        self.gridLayout_4 = QGridLayout(self.shape_box)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.hurr_area_checkbox = QCheckBox(self.shape_box)
        self.hurr_area_checkbox.setObjectName(u"hurr_area_checkbox")

        self.gridLayout_4.addWidget(self.hurr_area_checkbox, 1, 0, 1, 1)

        self.width_checkbox = QCheckBox(self.shape_box)
        self.width_checkbox.setObjectName(u"width_checkbox")

        self.gridLayout_4.addWidget(self.width_checkbox, 4, 0, 1, 1)

        self.area_checkbox = QCheckBox(self.shape_box)
        self.area_checkbox.setObjectName(u"area_checkbox")

        self.gridLayout_4.addWidget(self.area_checkbox, 0, 0, 1, 1)

        self.longest_path_checkbox = QCheckBox(self.shape_box)
        self.longest_path_checkbox.setObjectName(u"longest_path_checkbox")

        self.gridLayout_4.addWidget(self.longest_path_checkbox, 5, 0, 1, 1)

        self.perimeter_checkbox = QCheckBox(self.shape_box)
        self.perimeter_checkbox.setObjectName(u"perimeter_checkbox")

        self.gridLayout_4.addWidget(self.perimeter_checkbox, 2, 0, 1, 1)

        self.height_checkbox = QCheckBox(self.shape_box)
        self.height_checkbox.setObjectName(u"height_checkbox")

        self.gridLayout_4.addWidget(self.height_checkbox, 3, 0, 1, 1)


        self.gridLayout_2.addWidget(self.shape_box, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.chart_options_box, 3, 0, 1, 1)

        self.line = QFrame(AnalysisOptionsDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line, 2, 0, 1, 1)


        self.retranslateUi(AnalysisOptionsDialog)
        self.done_button.clicked.connect(AnalysisOptionsDialog.accept)

        self.done_button.setDefault(True)


        QMetaObject.connectSlotsByName(AnalysisOptionsDialog)
    # setupUi

    def retranslateUi(self, AnalysisOptionsDialog):
        AnalysisOptionsDialog.setWindowTitle(QCoreApplication.translate("AnalysisOptionsDialog", u"Analytic options", None))
        self.script_options_box.setTitle(QCoreApplication.translate("AnalysisOptionsDialog", u"Select script options", None))
        self.done_button.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Done", None))
        self.chart_options_box.setTitle(QCoreApplication.translate("AnalysisOptionsDialog", u"Select chart options", None))
        self.index_box.setTitle(QCoreApplication.translate("AnalysisOptionsDialog", u"Index", None))
        self.false_color_image_checkbox.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"False color image", None))
        self.mean_index_checkbox.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Mean index", None))
        self.reflectance_box.setTitle(QCoreApplication.translate("AnalysisOptionsDialog", u"Reflectance", None))
        self.spectral_signature_checkbox.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Spectral signature", None))
        self.shape_box.setTitle(QCoreApplication.translate("AnalysisOptionsDialog", u"Shape", None))
        self.hurr_area_checkbox.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Convex hull area", None))
        self.width_checkbox.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Width", None))
        self.area_checkbox.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Area", None))
        self.longest_path_checkbox.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Longest path", None))
        self.perimeter_checkbox.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Perimeter", None))
        self.height_checkbox.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Height", None))
    # retranslateUi

