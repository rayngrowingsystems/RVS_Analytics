# Copyright 2024 ETC Inc d/b/a RAYN Growing Systems
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This Python file uses the following encoding: utf-8

from datetime import datetime
from os import path
import os
import uuid

import plotly.graph_objects as go

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QStandardPaths
from PySide6.QtWebEngineWidgets import QWebEngineView

from Helper import tprint

class Chart:
    def __init__(self, main_window, title, y_label):
        tprint("Chart.init")

        self.main_window = main_window

        self.fig = go.Figure()

        self.fig.update_layout(
            title=title,
            xaxis_title="Timestamp",
            yaxis_title=y_label,
            legend_title="Rois"
            # hovermode="x"
            # ,
            # font=dict(
            #     family="Courier New, monospace",
            #     size=18,
            #     color="RebeccaPurple"
            # )
        )

        # Create temp files for charting
        base_file_name = str(uuid.uuid4())

        self.temp_image_file = os.path.normpath(os.path.join(QStandardPaths.writableLocation(QStandardPaths.TempLocation), base_file_name + ".svg"))
        self.temp_html_file = os.path.normpath(os.path.join(QStandardPaths.writableLocation(QStandardPaths.TempLocation), base_file_name + ".html"))

        tprint("Temp files:", self.temp_image_file, self.temp_html_file)

        self.widget = QWidget()
        layout = QVBoxLayout()
        self.widget.setLayout(layout)

        self.preview_label = QLabel()
        layout.addWidget(self.preview_label)

        self.preview_view = QWebEngineView()
        layout.addWidget(self.preview_view)
        self.preview_view.setHtml("<!DOCTYPE html><html><body><h1>No Chart data yet</h1></body></html>")

        self.preview_view.hide()

        self.tab_index = self.main_window.ui.tabWidget.addTab(self.widget, title)        

    def add_roi(self, timestamp, y, name):
        found = False
        for i in range(len(self.fig.data)):
            if self.fig.data[i].name == name:
                found = True
                break

        if not found:
            self.fig.add_scatter(name=name)

            tprint("Added scatter", name)

        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

        for i in range(len(self.fig.data)):
            if self.fig.data[i].name == name:
                if self.fig.data[i].y is None:
                    self.fig.data[i].y = ()
                    self.fig.data[i].x = ()

                self.fig.data[i].y = self.fig.data[i].y + (y,)
                self.fig.data[i].x = self.fig.data[i].x + (dt,)

                # tprint("Added datapoint", name, dt, y, self.fig.data[i].y)
                break

        self.fig.write_image(self.image_file())

        config = {'doubleClickDelay': 1000}

        # self.fig.write_html("temp.html", include_plotlyjs='cdn', config=config)
        self.fig.write_html(self.web_page(), config=config)

    def pixmap(self):
        return QPixmap(self.image_file())

    def image_file(self):
        return self.temp_image_file

    def web_page(self):
        return self.temp_html_file

