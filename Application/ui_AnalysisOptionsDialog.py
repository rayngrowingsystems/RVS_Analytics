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
        AnalysisOptionsDialog.resize(948, 548)
        AnalysisOptionsDialog.setModal(True)
        self.gridLayout_3 = QGridLayout(AnalysisOptionsDialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 4, 0, 1, 1)

        self.script_options_box = QGroupBox(AnalysisOptionsDialog)
        self.script_options_box.setObjectName(u"script_options_box")

        self.gridLayout_3.addWidget(self.script_options_box, 1, 0, 1, 1)

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
        self.false_color_image = QCheckBox(self.index_box)
        self.false_color_image.setObjectName(u"false_color_image")

        self.gridLayout_5.addWidget(self.false_color_image, 1, 0, 1, 1)

        self.mean_index = QCheckBox(self.index_box)
        self.mean_index.setObjectName(u"mean_index")

        self.gridLayout_5.addWidget(self.mean_index, 0, 0, 1, 1)

        self.index_histogram = QCheckBox(self.index_box)
        self.index_histogram.setObjectName(u"index_histogram")

        self.gridLayout_5.addWidget(self.index_histogram, 2, 0, 1, 1)


        self.gridLayout_2.addWidget(self.index_box, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.reflectance_box = QGroupBox(self.chart_options_box)
        self.reflectance_box.setObjectName(u"reflectance_box")
        self.gridLayout_6 = QGridLayout(self.reflectance_box)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.spectral_histogram = QCheckBox(self.reflectance_box)
        self.spectral_histogram.setObjectName(u"spectral_histogram")

        self.gridLayout_6.addWidget(self.spectral_histogram, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.reflectance_box, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)

        self.shape_box = QGroupBox(self.chart_options_box)
        self.shape_box.setObjectName(u"shape_box")
        self.gridLayout_4 = QGridLayout(self.shape_box)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.hull_area = QCheckBox(self.shape_box)
        self.hull_area.setObjectName(u"hull_area")

        self.gridLayout_4.addWidget(self.hull_area, 1, 0, 1, 1)

        self.width = QCheckBox(self.shape_box)
        self.width.setObjectName(u"width")

        self.gridLayout_4.addWidget(self.width, 4, 0, 1, 1)

        self.area = QCheckBox(self.shape_box)
        self.area.setObjectName(u"area")

        self.gridLayout_4.addWidget(self.area, 0, 0, 1, 1)

        self.longest_path = QCheckBox(self.shape_box)
        self.longest_path.setObjectName(u"longest_path")

        self.gridLayout_4.addWidget(self.longest_path, 5, 0, 1, 1)

        self.perimeter = QCheckBox(self.shape_box)
        self.perimeter.setObjectName(u"perimeter")

        self.gridLayout_4.addWidget(self.perimeter, 2, 0, 1, 1)

        self.height = QCheckBox(self.shape_box)
        self.height.setObjectName(u"height")

        self.gridLayout_4.addWidget(self.height, 3, 0, 1, 1)


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
        self.default_button.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Default", None))
        self.done_button.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Done", None))
        self.chart_options_box.setTitle(QCoreApplication.translate("AnalysisOptionsDialog", u"Select chart options", None))
        self.index_box.setTitle(QCoreApplication.translate("AnalysisOptionsDialog", u"Index", None))
        self.false_color_image.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"False color image", None))
        self.false_color_image.setProperty("optionType", QCoreApplication.translate("AnalysisOptionsDialog", u"image", None))
        self.mean_index.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Mean index", None))
        self.mean_index.setProperty("optionType", QCoreApplication.translate("AnalysisOptionsDialog", u"plot", None))
        self.index_histogram.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Index histogram", None))
        self.index_histogram.setProperty("optionType", QCoreApplication.translate("AnalysisOptionsDialog", u"image", None))
        self.reflectance_box.setTitle(QCoreApplication.translate("AnalysisOptionsDialog", u"Reflectance", None))
        self.spectral_histogram.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Spectral histogram", None))
        self.spectral_histogram.setProperty("optionType", QCoreApplication.translate("AnalysisOptionsDialog", u"image", None))
        self.shape_box.setTitle(QCoreApplication.translate("AnalysisOptionsDialog", u"Shape", None))
        self.hull_area.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Convex hull area", None))
        self.hull_area.setProperty("optionType", QCoreApplication.translate("AnalysisOptionsDialog", u"plot", None))
        self.width.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Width", None))
        self.width.setProperty("optionType", QCoreApplication.translate("AnalysisOptionsDialog", u"plot", None))
        self.area.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Area", None))
        self.area.setProperty("optionType", QCoreApplication.translate("AnalysisOptionsDialog", u"plot", None))
        self.longest_path.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Longest path", None))
        self.longest_path.setProperty("optionType", QCoreApplication.translate("AnalysisOptionsDialog", u"plot", None))
        self.perimeter.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Perimeter", None))
        self.perimeter.setProperty("optionType", QCoreApplication.translate("AnalysisOptionsDialog", u"plot", None))
        self.height.setText(QCoreApplication.translate("AnalysisOptionsDialog", u"Height", None))
        self.height.setProperty("optionType", QCoreApplication.translate("AnalysisOptionsDialog", u"plot", None))
    # retranslateUi

