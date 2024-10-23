# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ImageRoiDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

from ClickableLabel import ClickableLabel

class Ui_ImageRoiDialog(object):
    def setupUi(self, ImageRoiDialog):
        if not ImageRoiDialog.objectName():
            ImageRoiDialog.setObjectName(u"ImageRoiDialog")
        ImageRoiDialog.resize(986, 473)
        ImageRoiDialog.setModal(True)
        self.gridLayout_2 = QGridLayout(ImageRoiDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName(u"vertical_layout")
        self.label = QLabel(ImageRoiDialog)
        self.label.setObjectName(u"label")

        self.vertical_layout.addWidget(self.label)

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setObjectName(u"horizontal_layout")
        self.reference_image1 = ClickableLabel(ImageRoiDialog)
        self.reference_image1.setObjectName(u"reference_image1")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reference_image1.sizePolicy().hasHeightForWidth())
        self.reference_image1.setSizePolicy(sizePolicy)
        self.reference_image1.setMinimumSize(QSize(300, 200))
        self.reference_image1.setFrameShape(QFrame.Box)
        self.reference_image1.setScaledContents(False)
        self.reference_image1.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontal_layout.addWidget(self.reference_image1)

        self.reference_image2 = ClickableLabel(ImageRoiDialog)
        self.reference_image2.setObjectName(u"reference_image2")
        sizePolicy.setHeightForWidth(self.reference_image2.sizePolicy().hasHeightForWidth())
        self.reference_image2.setSizePolicy(sizePolicy)
        self.reference_image2.setMinimumSize(QSize(300, 200))
        self.reference_image2.setFrameShape(QFrame.Box)
        self.reference_image2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontal_layout.addWidget(self.reference_image2)


        self.vertical_layout.addLayout(self.horizontal_layout)

        self.label_2 = QLabel(ImageRoiDialog)
        self.label_2.setObjectName(u"label_2")

        self.vertical_layout.addWidget(self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.grid_layout = QGridLayout()
        self.grid_layout.setObjectName(u"grid_layout")
        self.rows_spinbox = QSpinBox(ImageRoiDialog)
        self.rows_spinbox.setObjectName(u"rows_spinbox")
        self.rows_spinbox.setMinimum(1)
        self.rows_spinbox.setMaximum(10)
        self.rows_spinbox.setValue(3)

        self.grid_layout.addWidget(self.rows_spinbox, 1, 3, 1, 1)

        self.rows_label = QLabel(ImageRoiDialog)
        self.rows_label.setObjectName(u"rows_label")

        self.grid_layout.addWidget(self.rows_label, 1, 2, 1, 1)

        self.roi_placement_mode = QComboBox(ImageRoiDialog)
        self.roi_placement_mode.addItem("")
        self.roi_placement_mode.addItem("")
        self.roi_placement_mode.setObjectName(u"roi_placement_mode")

        self.grid_layout.addWidget(self.roi_placement_mode, 1, 1, 1, 1)

        self.roi_detection_mode = QComboBox(ImageRoiDialog)
        self.roi_detection_mode.addItem("")
        self.roi_detection_mode.addItem("")
        self.roi_detection_mode.addItem("")
        self.roi_detection_mode.setObjectName(u"roi_detection_mode")

        self.grid_layout.addWidget(self.roi_detection_mode, 0, 1, 1, 1)

        self.width_spinbox = QSpinBox(ImageRoiDialog)
        self.width_spinbox.setObjectName(u"width_spinbox")
        self.width_spinbox.setMinimum(5)
        self.width_spinbox.setMaximum(1000)
        self.width_spinbox.setValue(5)

        self.grid_layout.addWidget(self.width_spinbox, 1, 6, 1, 1)

        self.width_label = QLabel(ImageRoiDialog)
        self.width_label.setObjectName(u"width_label")

        self.grid_layout.addWidget(self.width_label, 1, 5, 1, 1)

        self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.grid_layout.addItem(self.horizontal_spacer, 1, 4, 1, 1)

        self.height_label = QLabel(ImageRoiDialog)
        self.height_label.setObjectName(u"height_label")

        self.grid_layout.addWidget(self.height_label, 2, 5, 1, 1)

        self.height_spinbox = QSpinBox(ImageRoiDialog)
        self.height_spinbox.setObjectName(u"height_spinbox")
        self.height_spinbox.setMinimum(5)
        self.height_spinbox.setMaximum(1000)
        self.height_spinbox.setValue(30)

        self.grid_layout.addWidget(self.height_spinbox, 2, 6, 1, 1)

        self.columns_label = QLabel(ImageRoiDialog)
        self.columns_label.setObjectName(u"columns_label")

        self.grid_layout.addWidget(self.columns_label, 2, 2, 1, 1)

        self.roi_shape = QComboBox(ImageRoiDialog)
        self.roi_shape.addItem("")
        self.roi_shape.addItem("")
        self.roi_shape.addItem("")
        self.roi_shape.addItem("")
        self.roi_shape.setObjectName(u"roi_shape")

        self.grid_layout.addWidget(self.roi_shape, 2, 1, 1, 1)

        self.radius_spinbox = QSpinBox(ImageRoiDialog)
        self.radius_spinbox.setObjectName(u"radius_spinbox")
        self.radius_spinbox.setMinimum(5)
        self.radius_spinbox.setMaximum(1000)

        self.grid_layout.addWidget(self.radius_spinbox, 1, 8, 1, 1)

        self.radius_label = QLabel(ImageRoiDialog)
        self.radius_label.setObjectName(u"radius_label")

        self.grid_layout.addWidget(self.radius_label, 1, 7, 1, 1)

        self.columns_spinbox = QSpinBox(ImageRoiDialog)
        self.columns_spinbox.setObjectName(u"columns_spinbox")
        self.columns_spinbox.setMinimum(1)
        self.columns_spinbox.setMaximum(10)
        self.columns_spinbox.setValue(5)

        self.grid_layout.addWidget(self.columns_spinbox, 2, 3, 1, 1)

        self.label_3 = QLabel(ImageRoiDialog)
        self.label_3.setObjectName(u"label_3")

        self.grid_layout.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_4 = QLabel(ImageRoiDialog)
        self.label_4.setObjectName(u"label_4")

        self.grid_layout.addWidget(self.label_4, 1, 0, 1, 1)

        self.label_5 = QLabel(ImageRoiDialog)
        self.label_5.setObjectName(u"label_5")

        self.grid_layout.addWidget(self.label_5, 2, 0, 1, 1)

        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setColumnStretch(3, 1)
        self.grid_layout.setColumnMinimumWidth(0, 1)
        self.grid_layout.setColumnMinimumWidth(1, 1)
        self.grid_layout.setColumnMinimumWidth(4, 1)

        self.horizontalLayout_2.addLayout(self.grid_layout)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_2.setStretch(1, 2)

        self.vertical_layout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.vertical_layout.addLayout(self.horizontalLayout_3)

        self.info_label = QLabel(ImageRoiDialog)
        self.info_label.setObjectName(u"info_label")
        self.info_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.vertical_layout.addWidget(self.info_label)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vertical_layout.addItem(self.vertical_spacer)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.clear_button = QPushButton(ImageRoiDialog)
        self.clear_button.setObjectName(u"clear_button")
        self.clear_button.setAutoDefault(False)

        self.horizontalLayout_4.addWidget(self.clear_button)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.cancel_button = QPushButton(ImageRoiDialog)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setAutoDefault(False)

        self.horizontalLayout_4.addWidget(self.cancel_button)

        self.done_button = QPushButton(ImageRoiDialog)
        self.done_button.setObjectName(u"done_button")
        self.done_button.setAutoDefault(False)

        self.horizontalLayout_4.addWidget(self.done_button)


        self.vertical_layout.addLayout(self.horizontalLayout_4)

        self.vertical_layout.setStretch(1, 4)

        self.gridLayout_2.addLayout(self.vertical_layout, 0, 0, 1, 1)


        self.retranslateUi(ImageRoiDialog)
        self.done_button.clicked.connect(ImageRoiDialog.accept)

        self.done_button.setDefault(False)


        QMetaObject.connectSlotsByName(ImageRoiDialog)
    # setupUi

    def retranslateUi(self, ImageRoiDialog):
        ImageRoiDialog.setWindowTitle(QCoreApplication.translate("ImageRoiDialog", u"Regions of Interest (ROI)", None))
        self.label.setText(QCoreApplication.translate("ImageRoiDialog", u"Pick one or two reference images (usually the first and last of an image series)", None))
        self.reference_image1.setText(QCoreApplication.translate("ImageRoiDialog", u"<br><br>Click the Image button to pick", None))
        self.reference_image2.setText(QCoreApplication.translate("ImageRoiDialog", u"<br><br>Click the Image button to pick", None))
        self.label_2.setText(QCoreApplication.translate("ImageRoiDialog", u"Select Regions of Interest (ROI) drawing mode and related settings", None))
        self.rows_label.setText(QCoreApplication.translate("ImageRoiDialog", u"Rows", None))
        self.roi_placement_mode.setItemText(0, QCoreApplication.translate("ImageRoiDialog", u"Matrix", None))
        self.roi_placement_mode.setItemText(1, QCoreApplication.translate("ImageRoiDialog", u"Individual", None))

        self.roi_detection_mode.setItemText(0, QCoreApplication.translate("ImageRoiDialog", u"Partial", None))
        self.roi_detection_mode.setItemText(1, QCoreApplication.translate("ImageRoiDialog", u"Cut to", None))
        self.roi_detection_mode.setItemText(2, QCoreApplication.translate("ImageRoiDialog", u"Largest", None))

        self.width_label.setText(QCoreApplication.translate("ImageRoiDialog", u"Width", None))
        self.height_label.setText(QCoreApplication.translate("ImageRoiDialog", u"Height", None))
        self.columns_label.setText(QCoreApplication.translate("ImageRoiDialog", u"Columns", None))
        self.roi_shape.setItemText(0, QCoreApplication.translate("ImageRoiDialog", u"Circle", None))
        self.roi_shape.setItemText(1, QCoreApplication.translate("ImageRoiDialog", u"Rectangle", None))
        self.roi_shape.setItemText(2, QCoreApplication.translate("ImageRoiDialog", u"Ellipse", None))
        self.roi_shape.setItemText(3, QCoreApplication.translate("ImageRoiDialog", u"Polygon", None))

        self.radius_label.setText(QCoreApplication.translate("ImageRoiDialog", u"Radius", None))
        self.label_3.setText(QCoreApplication.translate("ImageRoiDialog", u"Detection mode", None))
        self.label_4.setText(QCoreApplication.translate("ImageRoiDialog", u"Placement mode", None))
        self.label_5.setText(QCoreApplication.translate("ImageRoiDialog", u"Shape", None))
        self.info_label.setText("")
        self.clear_button.setText(QCoreApplication.translate("ImageRoiDialog", u"Clear ROIs", None))
        self.cancel_button.setText(QCoreApplication.translate("ImageRoiDialog", u"Cancel", None))
        self.done_button.setText(QCoreApplication.translate("ImageRoiDialog", u"Done", None))
    # retranslateUi

