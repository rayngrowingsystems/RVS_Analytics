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

import os
import uuid
from datetime import datetime

import altair as alt
import pandas as pd
import vl_convert as vlc
from PySide6.QtCore import QSize, QStandardPaths
from PySide6.QtGui import QColor, QPalette, QPixmap
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QVBoxLayout, QWidget

from Helper import ResultTabWidget, tprint
import re


def apply_fixed_axis_limits(chart, x_domain=None, y_domain=None):
    """Update an Altair chart with fixed axis limits on x and y axes."""

    enc = chart.encoding

    if x_domain:
        x = enc.x.to_dict()
        chart = chart.encode(
            x=alt.X(
                x.get("shorthand", x.get("field")),
                type=x.get("type"),
                title=x.get("title"),
                scale=alt.Scale(domain=x_domain)
            )
        )

    if y_domain:
        y = enc.y.to_dict()
        chart = chart.encode(
            y=alt.Y(
                y.get("shorthand", y.get("field")),
                type=y.get("type"),
                title=y.get("title"),
                scale=alt.Scale(domain=y_domain)
            )
        )

    return chart


def is_dark(hex_color: str) -> bool:
    c = QColor(hex_color)
    # Using the perceived brightness formula
    brightness = (0.299 * c.red() + 0.587 * c.green() + 0.114 * c.blue())
    return brightness < 128


def dark_theme():
    return {
        "config": {
            "background": "#111",
            "title": {"color": "white"},
            "axis": {
                "labelColor": "white",
                "titleColor": "white",
                "gridColor": "#333",
                "domainColor": "#666"
            },
            "legend": {
                "labelColor": "white",
                "titleColor": "white"
            }
        }
    }


alt.themes.register('custom_dark', dark_theme)
alt.themes.enable('custom_dark')

class Chart:
    def __init__(self, main_window, title, y_label):
        tprint("Chart.init")

        self.main_window = main_window
        self.title = title
        self.y_label = y_label
        self.data = []

        self.content_size = QSize()
        self.widget_size = QSize()

        # Create temp file paths
        base_file_name = str(uuid.uuid4())
        self.temp_image_file = os.path.normpath(os.path.join(
            QStandardPaths.writableLocation(QStandardPaths.TempLocation), base_file_name + ".png"))
        self.temp_html_file = os.path.normpath(os.path.join(
            QStandardPaths.writableLocation(QStandardPaths.TempLocation), base_file_name + ".html"))

        # tprint("Temp files:", self.temp_image_file, self.temp_html_file)

        self.widget = QWidget()
        layout = QVBoxLayout()
        self.widget.setLayout(layout)

        self.preview_label = ResultTabWidget(self.temp_image_file)
        layout.addWidget(self.preview_label)

        self.preview_view = QWebEngineView()
        layout.addWidget(self.preview_view)
        self.preview_view.setHtml("<!DOCTYPE html><html><body><h1>No Chart data yet</h1></body></html>")
        self.preview_view.hide()

        self.tab_index = self.main_window.ui.tab_widget.addTab(self.widget, title)

    def add_roi(self, timestamp, y, name):
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        self.data.append({
            "Timestamp": dt,
            "Value": y,
            "Roi": name
        })
        # tprint(f"Added data point: {name}, {dt}, {y}")

    def generate_chart(self):
        df = pd.DataFrame(self.data)

        if df.empty:
            tprint("No data to plot.")
            return None

        selection = alt.selection_multi(fields=["Roi"], bind="legend")
        bg_color = self.widget.palette().color(QPalette.Window).name()

        chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X("Timestamp:T", title="Timestamp"),
            y=alt.Y("Value:Q", title=self.y_label),
            color=alt.Color("Roi:N", title="Rois"),
            tooltip=[
                alt.Tooltip("Timestamp:T", title="Timestamp"),
                alt.Tooltip("Value:Q", title=self.y_label),
                alt.Tooltip("Roi:N", title="ROI")
            ],
            opacity=alt.condition(selection, alt.value(1), alt.value(0.1))
        ).add_selection(
            selection
        ).interactive(  # enables zooming/panning
        ).properties(
            title=self.title,
            width=600,
            height=400
        ).configure_view(
            fill=bg_color, stroke=None
        ).configure(
            background=bg_color
        ).configure_axis(
            labelColor="white" if is_dark(bg_color) else "black",
            titleColor="white" if is_dark(bg_color) else "black",
            gridOpacity=1 if is_dark(bg_color) else 0.1,

        ).configure_legend(
            labelColor="white" if is_dark(bg_color) else "black",
            titleColor="white" if is_dark(bg_color) else "black"
        ).configure_title(
            color="white" if is_dark(bg_color) else "black"
        )

        return chart

    def image_file(self):
        return self.temp_image_file

    def web_page(self):
        return self.temp_html_file

    def pixmap(self):
        return QPixmap(self.image_file())

    def update_images(self):
        chart = self.generate_chart()
        if chart is None:
            return

        chart_dict = chart.to_dict()

        # Save as image
        png_data = vlc.vegalite_to_png(chart_dict, scale=1.5)  # TODO: rather export it as svg?
        with open(self.image_file(), "wb") as f:
            f.write(png_data)
        print(f"Chart saved to {self.image_file()}")

        # Save as HTML
        chart_dict["autosize"] = {
            "type": "fit",
            "contains": "padding"
        }

        chart_html = vlc.vegalite_to_html(chart_dict, bundle=True)

        chart_html = chart_html.replace(
            'const opts = {"renderer":"svg"}',
            '''const opts = {
                "renderer": "svg",
                "actions": false,
                "config": {
                    "view": {
                        "continuousWidth": "container",
                        "continuousHeight": "container"
                    }
                }
            }'''
        )

        chart_html = chart_html.replace(
            "</head>",
            """<style>
               html, body {
                 margin: 0;
                 height: 100%;
               }
               #vega-chart {
                 width: 100%;
                 height: 100%;
               }
               .vega-embed, .vega-embed > svg {
                 width: auto !important;
                 height: 100% !important;
                 max-width: 100%;
               }
             </style></head>"""
        )

        with open(self.web_page(), "w", encoding="utf-8") as f:
            f.write(chart_html)
            print(f"Chart saved to {self.web_page()}")

        self.preview_label.update_pixmap(self.image_file())
