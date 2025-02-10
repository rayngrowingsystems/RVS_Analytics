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
from os import path

from PySide6.QtCore import QSettings, QStandardPaths, QDir

from Helper import tprint

path_name = os.path.normpath(QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation))
file_name = os.path.join(path_name, "RaynVisionSystem.ini")

if not path.exists(file_name):
    # Create empty file
    QDir().mkpath(path_name)
    with open(file_name, 'w') as fp:
        pass

settings = QSettings(file_name, QSettings.IniFormat)
if settings.value("Verbose", False) == "True":
    verbose_mode = True
else:
    verbose_mode = False

if settings.value("Profile", False) == "True":
    profile_mode = True
else:
    profile_mode = False

tprint("Config: Verbose", verbose_mode, type(verbose_mode))
tprint("Config: Profile", profile_mode, type(profile_mode))

