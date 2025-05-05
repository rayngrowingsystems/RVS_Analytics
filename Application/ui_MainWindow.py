# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QDockWidget,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStatusBar, QTabWidget, QToolButton, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1118, 632)
        self.action_exit = QAction(MainWindow)
        self.action_exit.setObjectName(u"action_exit")
        self.actionOpen_experiment = QAction(MainWindow)
        self.actionOpen_experiment.setObjectName(u"actionOpen_experiment")
        self.actionSave_experiment = QAction(MainWindow)
        self.actionSave_experiment.setObjectName(u"actionSave_experiment")
        self.actionSave_As_experiment = QAction(MainWindow)
        self.actionSave_As_experiment.setObjectName(u"actionSave_As_experiment")
        self.action_select_network = QAction(MainWindow)
        self.action_select_network.setObjectName(u"action_select_network")
        self.action_mqtt_broker = QAction(MainWindow)
        self.action_mqtt_broker.setObjectName(u"action_mqtt_broker")
        self.action_download_images = QAction(MainWindow)
        self.action_download_images.setObjectName(u"action_download_images")
        self.action_help = QAction(MainWindow)
        self.action_help.setObjectName(u"action_help")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_open_experiment = QAction(MainWindow)
        self.action_open_experiment.setObjectName(u"action_open_experiment")
        self.action_save_as_experiment = QAction(MainWindow)
        self.action_save_as_experiment.setObjectName(u"action_save_as_experiment")
        self.action_new_experiment = QAction(MainWindow)
        self.action_new_experiment.setObjectName(u"action_new_experiment")
        self.action_save_experiment = QAction(MainWindow)
        self.action_save_experiment.setObjectName(u"action_save_experiment")
        self.action_open_analysis = QAction(MainWindow)
        self.action_open_analysis.setObjectName(u"action_open_analysis")
        self.action_save_as_analysis = QAction(MainWindow)
        self.action_save_as_analysis.setObjectName(u"action_save_as_analysis")
        self.action_new_analysis = QAction(MainWindow)
        self.action_new_analysis.setObjectName(u"action_new_analysis")
        self.action_save_analysis = QAction(MainWindow)
        self.action_save_analysis.setObjectName(u"action_save_analysis")
        self.action_save_analysis.setEnabled(True)
        self.action_delete_images = QAction(MainWindow)
        self.action_delete_images.setObjectName(u"action_delete_images")
        self.action_settings = QAction(MainWindow)
        self.action_settings.setObjectName(u"action_settings")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.image_source = QLabel(self.centralwidget)
        self.image_source.setObjectName(u"image_source")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_source.sizePolicy().hasHeightForWidth())
        self.image_source.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.image_source, 0, 3, 1, 1)

        self.camera_status = QLabel(self.centralwidget)
        self.camera_status.setObjectName(u"camera_status")
        sizePolicy.setHeightForWidth(self.camera_status.sizePolicy().hasHeightForWidth())
        self.camera_status.setSizePolicy(sizePolicy)
        self.camera_status.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.camera_status, 0, 4, 1, 1)

        self.mqtt_status = QLabel(self.centralwidget)
        self.mqtt_status.setObjectName(u"mqtt_status")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.mqtt_status.sizePolicy().hasHeightForWidth())
        self.mqtt_status.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.mqtt_status, 0, 5, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.tab_widget = QTabWidget(self.centralwidget)
        self.tab_widget.setObjectName(u"tab_widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tab_widget.sizePolicy().hasHeightForWidth())
        self.tab_widget.setSizePolicy(sizePolicy2)
        self.preview_tab = QWidget()
        self.preview_tab.setObjectName(u"preview_tab")
        self.horizontalLayout_3 = QHBoxLayout(self.preview_tab)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.image_preview = QLabel(self.preview_tab)
        self.image_preview.setObjectName(u"image_preview")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.image_preview.sizePolicy().hasHeightForWidth())
        self.image_preview.setSizePolicy(sizePolicy3)
        self.image_preview.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(14)
        self.image_preview.setFont(font)
        self.image_preview.setFrameShape(QFrame.NoFrame)
        self.image_preview.setLineWidth(0)
        self.image_preview.setScaledContents(True)
        self.image_preview.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_3.addWidget(self.image_preview)

        self.tab_widget.addTab(self.preview_tab, "")

        self.verticalLayout.addWidget(self.tab_widget)

        self.timestamp_label = QLabel(self.centralwidget)
        self.timestamp_label.setObjectName(u"timestamp_label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.timestamp_label.sizePolicy().hasHeightForWidth())
        self.timestamp_label.setSizePolicy(sizePolicy4)

        self.verticalLayout.addWidget(self.timestamp_label)

        self.image_preview_progressbar = QProgressBar(self.centralwidget)
        self.image_preview_progressbar.setObjectName(u"image_preview_progressbar")
        self.image_preview_progressbar.setValue(0)
        self.image_preview_progressbar.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.image_preview_progressbar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1118, 21))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_experiment = QMenu(self.menubar)
        self.menu_experiment.setObjectName(u"menu_experiment")
        self.menu_analysis = QMenu(self.menubar)
        self.menu_analysis.setObjectName(u"menu_analysis")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setEnabled(True)
        self.statusbar.setAutoFillBackground(False)
        MainWindow.setStatusBar(self.statusbar)
        self.statusDockWidget = QDockWidget(MainWindow)
        self.statusDockWidget.setObjectName(u"statusDockWidget")
        self.statusDockWidget.setAutoFillBackground(False)
        self.statusDockWidget.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.statusDockWidget.setAllowedAreas(Qt.BottomDockWidgetArea|Qt.TopDockWidgetArea)
        self.dockWidgetContents_3 = QWidget()
        self.dockWidgetContents_3.setObjectName(u"dockWidgetContents_3")
        self.gridLayout_4 = QGridLayout(self.dockWidgetContents_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.scrollArea = QScrollArea(self.dockWidgetContents_3)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1108, 68))
        self.gridLayout_5 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.status_text = QLabel(self.scrollAreaWidgetContents)
        self.status_text.setObjectName(u"status_text")
        self.status_text.setFrameShape(QFrame.NoFrame)
        self.status_text.setLineWidth(1)
        self.status_text.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout_5.addWidget(self.status_text, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)


        self.gridLayout_4.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.statusDockWidget.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.statusDockWidget)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.dockWidget.sizePolicy().hasHeightForWidth())
        self.dockWidget.setSizePolicy(sizePolicy5)
        self.dockWidget.setMinimumSize(QSize(114, 500))
        self.dockWidget.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.dock_widget_contents = QWidget()
        self.dock_widget_contents.setObjectName(u"dock_widget_contents")
        self.gridLayout_3 = QGridLayout(self.dock_widget_contents)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.image_mask_button = QPushButton(self.dock_widget_contents)
        self.image_mask_button.setObjectName(u"image_mask_button")

        self.gridLayout_3.addWidget(self.image_mask_button, 5, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 10, 0, 1, 1)

        self.analysis_options_button = QPushButton(self.dock_widget_contents)
        self.analysis_options_button.setObjectName(u"analysis_options_button")
        self.analysis_options_button.setEnabled(True)

        self.gridLayout_3.addWidget(self.analysis_options_button, 7, 0, 1, 1)

        self.analysis_preview_button = QPushButton(self.dock_widget_contents)
        self.analysis_preview_button.setObjectName(u"analysis_preview_button")

        self.gridLayout_3.addWidget(self.analysis_preview_button, 9, 0, 1, 1)

        self.script_selection_combobox = QComboBox(self.dock_widget_contents)
        self.script_selection_combobox.setObjectName(u"script_selection_combobox")

        self.gridLayout_3.addWidget(self.script_selection_combobox, 2, 0, 1, 1)

        self.play_status_label = QLabel(self.dock_widget_contents)
        self.play_status_label.setObjectName(u"play_status_label")

        self.gridLayout_3.addWidget(self.play_status_label, 14, 0, 1, 1)

        self.label_4 = QLabel(self.dock_widget_contents)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 3, 0, 1, 1)

        self.mask_selection_combobox = QComboBox(self.dock_widget_contents)
        self.mask_selection_combobox.setObjectName(u"mask_selection_combobox")

        self.gridLayout_3.addWidget(self.mask_selection_combobox, 4, 0, 1, 1)

        self.label_2 = QLabel(self.dock_widget_contents)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.label_2.setFont(font1)

        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.dock_widget_contents)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)

        self.verticalLayout_3.addWidget(self.label)

        self.image_source_button = QPushButton(self.dock_widget_contents)
        self.image_source_button.setObjectName(u"image_source_button")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.image_source_button.sizePolicy().hasHeightForWidth())
        self.image_source_button.setSizePolicy(sizePolicy6)

        self.verticalLayout_3.addWidget(self.image_source_button)

        self.image_option_button = QPushButton(self.dock_widget_contents)
        self.image_option_button.setObjectName(u"image_option_button")

        self.verticalLayout_3.addWidget(self.image_option_button)

        self.image_roi_button = QPushButton(self.dock_widget_contents)
        self.image_roi_button.setObjectName(u"image_roi_button")
        sizePolicy6.setHeightForWidth(self.image_roi_button.sizePolicy().hasHeightForWidth())
        self.image_roi_button.setSizePolicy(sizePolicy6)

        self.verticalLayout_3.addWidget(self.image_roi_button)

        self.line_2 = QFrame(self.dock_widget_contents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)


        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.line_3 = QFrame(self.dock_widget_contents)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_3.addWidget(self.line_3, 11, 0, 1, 1)

        self.label_3 = QLabel(self.dock_widget_contents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.gridLayout_3.addWidget(self.label_3, 12, 0, 1, 1)

        self.results_button = QPushButton(self.dock_widget_contents)
        self.results_button.setObjectName(u"results_button")
        self.results_button.setEnabled(False)

        self.gridLayout_3.addWidget(self.results_button, 16, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.play_button = QToolButton(self.dock_widget_contents)
        self.play_button.setObjectName(u"play_button")
        self.play_button.setMinimumSize(QSize(32, 32))
        self.play_button.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.play_button)

        self.stop_button = QToolButton(self.dock_widget_contents)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setMinimumSize(QSize(32, 32))
        self.stop_button.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.stop_button)


        self.gridLayout_3.addLayout(self.horizontalLayout_2, 15, 0, 1, 1)

        self.clear_sessiondata_button = QPushButton(self.dock_widget_contents)
        self.clear_sessiondata_button.setObjectName(u"clear_sessiondata_button")

        self.gridLayout_3.addWidget(self.clear_sessiondata_button, 13, 0, 1, 1)

        self.dockWidget.setWidget(self.dock_widget_contents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockWidget)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_experiment.menuAction())
        self.menubar.addAction(self.menu_analysis.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_select_network)
        self.menu_file.addAction(self.action_settings)
        self.menu_file.addAction(self.action_download_images)
        self.menu_file.addAction(self.action_delete_images)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_help.addAction(self.action_help)
        self.menu_help.addAction(self.action_about)
        self.menu_experiment.addAction(self.action_new_experiment)
        self.menu_experiment.addAction(self.action_open_experiment)
        self.menu_experiment.addAction(self.action_save_experiment)
        self.menu_experiment.addAction(self.action_save_as_experiment)
        self.menu_experiment.addSeparator()
        self.menu_analysis.addAction(self.action_new_analysis)
        self.menu_analysis.addAction(self.action_open_analysis)
        self.menu_analysis.addAction(self.action_save_analysis)
        self.menu_analysis.addAction(self.action_save_as_analysis)
        self.menu_analysis.addSeparator()

        self.retranslateUi(MainWindow)
        self.action_exit.triggered.connect(MainWindow.close)

        self.tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("")
        self.action_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionOpen_experiment.setText(QCoreApplication.translate("MainWindow", u"Open experiment...", None))
        self.actionSave_experiment.setText(QCoreApplication.translate("MainWindow", u"Save experiment", None))
        self.actionSave_As_experiment.setText(QCoreApplication.translate("MainWindow", u"Save As experiment...", None))
        self.action_select_network.setText(QCoreApplication.translate("MainWindow", u"Select network...", None))
        self.action_mqtt_broker.setText(QCoreApplication.translate("MainWindow", u"Set MQTT Broker...", None))
        self.action_download_images.setText(QCoreApplication.translate("MainWindow", u"Download images from camera...", None))
        self.action_help.setText(QCoreApplication.translate("MainWindow", u"Help...", None))
#if QT_CONFIG(shortcut)
        self.action_help.setShortcut(QCoreApplication.translate("MainWindow", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"About...", None))
        self.action_open_experiment.setText(QCoreApplication.translate("MainWindow", u"Open Experiment...", None))
#if QT_CONFIG(shortcut)
        self.action_open_experiment.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_save_as_experiment.setText(QCoreApplication.translate("MainWindow", u"Save As Experiment...", None))
        self.action_new_experiment.setText(QCoreApplication.translate("MainWindow", u"New Experiment", None))
#if QT_CONFIG(shortcut)
        self.action_new_experiment.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.action_save_experiment.setText(QCoreApplication.translate("MainWindow", u"Save Experiment", None))
#if QT_CONFIG(shortcut)
        self.action_save_experiment.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_open_analysis.setText(QCoreApplication.translate("MainWindow", u"Open Analysis...", None))
        self.action_save_as_analysis.setText(QCoreApplication.translate("MainWindow", u"Save As Analysis...", None))
        self.action_new_analysis.setText(QCoreApplication.translate("MainWindow", u"New Analysis", None))
        self.action_save_analysis.setText(QCoreApplication.translate("MainWindow", u"Save Analysis", None))
        self.action_delete_images.setText(QCoreApplication.translate("MainWindow", u"Delete images from camera...", None))
        self.action_settings.setText(QCoreApplication.translate("MainWindow", u"Settings...", None))
        self.image_source.setText("")
        self.camera_status.setText("")
        self.mqtt_status.setText("")
        self.image_preview.setText("")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.preview_tab), QCoreApplication.translate("MainWindow", u"Preview", None))
        self.timestamp_label.setText("")
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menu_experiment.setTitle(QCoreApplication.translate("MainWindow", u"Experiment", None))
        self.menu_analysis.setTitle(QCoreApplication.translate("MainWindow", u"Analysis", None))
        self.statusDockWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Status", None))
        self.status_text.setText("")
        self.dockWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sidebar", None))
        self.image_mask_button.setText(QCoreApplication.translate("MainWindow", u"Masking", None))
        self.analysis_options_button.setText(QCoreApplication.translate("MainWindow", u"Options", None))
        self.analysis_preview_button.setText(QCoreApplication.translate("MainWindow", u"Preview", None))
        self.play_status_label.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Mask Script", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Analysis", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Setup", None))
        self.image_source_button.setText(QCoreApplication.translate("MainWindow", u"Image Source", None))
        self.image_option_button.setText(QCoreApplication.translate("MainWindow", u"Image Options", None))
        self.image_roi_button.setText(QCoreApplication.translate("MainWindow", u"Regions", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.results_button.setText(QCoreApplication.translate("MainWindow", u"Results", None))
        self.play_button.setText("")
        self.stop_button.setText("")
        self.clear_sessiondata_button.setText(QCoreApplication.translate("MainWindow", u"Clear Session Data", None))
    # retranslateUi

