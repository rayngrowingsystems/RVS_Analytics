# Copyright 2024 RAYN Growing Systems
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

import time
import json
import datetime
import os

from threading import Thread

from multiprocessing import Queue

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap
from PySide6 import QtCore

import requests

import Config
import Helper

def fetch_files_in_the_background(camera, feedback_queue):
    progress = 0
    while True:
        if len(camera.files_to_fetch) > 0:
            camera.wait_for_files_arrived = True

            print("Camera: Files in fetch queue:", len(camera.files_to_fetch))

            file_name, target_folder, analyze, delete_from_camera = camera.files_to_fetch.pop(0)

            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            if os.path.exists(os.path.join(target_folder, file_name)):
                print("Camera: Skipping download. File already exists:", os.path.join(target_folder, file_name))

                if file_name.endswith(".hdr"):
                    camera.set_last_received_file(os.path.join(target_folder, file_name))
            else:
                template = '{ "filename": "" }'
                json_filename = json.loads(template)
                json_filename['filename'] = file_name
                json_filename['source'] = 'scheduler'

                print("Camera: Fetching file:", file_name)
                feedback_queue.put(["fileName", file_name])
                feedback_queue.put(["progress", progress])  # Make sure progressbar is updated

                url = camera.base_url + "/files/get" + camera.default_parameters()
                try:
                    r = requests.get(url, json=json_filename, timeout=100)

                    image = None
                    if r is not None and r.status_code == 200:
                        image = r.content  # get the image
                        print("Camera: Received content file size:", len(r.content))
                    elif r is not None:
                        print("Camera: ERROR: /files/get command failed, response code:", str(r.status_code), "info:", str(r.content))
                    else:
                        print("Camera: ERROR: /files/get command timeout")

                    if image is not None:
                        print("Camera: Storing file in", os.path.join(target_folder, file_name))

                        try:
                            f = open(os.path.join(target_folder, file_name), "wb")  # save image to file
                            f.write(image)
                            f.close()

                            file_stats = os.stat(os.path.join(target_folder, file_name))
                            print("Camera: Stored file size on disk:", file_stats.st_size)

                            if file_name.endswith(".hdr"):
                                camera.set_last_received_file(os.path.join(target_folder, file_name))

                            if file_name.endswith(".PNG"):
                                feedback_queue.put(["preview", os.path.join(target_folder, file_name)])

                            if delete_from_camera:
                                print("Camera: Delete file after download:", file_name)

                                camera.delete_file("scheduler", file_name)

                            if analyze:
                                camera.images_need_analysis = True
                        except IOError as e:
                            print("Camera: ERROR: Write to file failed", e)
                    else:
                        print("Camera: ERROR: Nothing to store")
                except Exception as e:
                    print("Camera: ERROR: Unhandled exception", e)

            progress = progress + 1

            if len(camera.files_to_fetch) == 0:
                feedback_queue.put(["done"])
                progress = 0

        time.sleep(0.1)

        camera.wait_for_files_arrived = False


class Camera:
    unique_key = "123456"  # TODO

    def __init__(self, main_window, ip_address):
        self.main_window = main_window

        self.base_url = "http://" + ip_address + "/api/v1"

        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)

        self.start_date_time = yesterday
        self.end_date_time = datetime.datetime.now()

        print("Camera: Init: Url:", self.base_url, "Start time:", self.start_date_time, "End time:", self.end_date_time)

        self.files_to_fetch = []
        self.wait_for_files_arrived = False
        self.fetch_feedback_queue = Queue()

        self.images_need_analysis = False

        # self.getInfo()
        # self.getStatus()
        # files = [s for s in self.getFolder("scheduler") if s.endswith('.hdr')]
        # files.sort()
        # print("getFolder", files)

        print('Camera: Starting background task that fetches the files...')

        daemon = Thread(target=fetch_files_in_the_background, args=(self, self.fetch_feedback_queue,), daemon=True, name='Fetch')
        daemon.start()

        self.tick_divider = 0

    def tick(self):
        self.tick_divider = self.tick_divider + 1
        if self.tick_divider >= 10:
            self.tick_divider = 0

            if Config.verbose_mode:
                print("Camera tick:", self.main_window.analysis_running, len(self.files_to_fetch), self.wait_for_files_arrived, self.images_need_analysis)

            if self.main_window is not None:
                if self.main_window.analysis_running and self.main_window.experiment.ImageSource is self.main_window.experiment.ImageSource.Camera and self.main_window.experiment.camera_file_path != "":
                    if len(self.files_to_fetch) == 0 and not self.wait_for_files_arrived:
                        if self.get_first_in_range() == False:  # Nothing more to fetch right now -> process accumulated ones
                            if self.images_need_analysis == True:
                                self.main_window.start_analysis(True, False, True)
                                self.images_need_analysis = False
                while not self.fetch_feedback_queue.empty():
                    data = self.fetch_feedback_queue.get()
                    if Config.verbose_mode:
                        print("Camera: Tick: Feedback queue:", data)

                    command = data[0]
                    if command == "fileName":
                        file_name = data[1]
                        self.main_window.add_status_text("Fetching image: " + file_name)
                    elif command == "progressRange":
                        count = data[1]
                        self.main_window.ui.image_preview_progressbar.setRange(0, count)
                    elif command == "progress":
                        value = data[1]
                        self.main_window.ui.image_preview_progressbar.setValue(int(value))
                    elif command == "done":
                        self.main_window.ui.image_preview_progressbar.hide()
                        self.main_window.add_status_text("Done")
                    elif command == "preview":  # Psuedo RGB: <fileName>
                        value = data[1]

                        if self.main_window.ui.image_preview.pixmap():
                            width = self.main_window.ui.image_preview.pixmap().width()
                        else:
                            width = self.main_window.ui.image_preview.width()  # No pixmap, use label width

                        self.main_window.ui.image_preview.setPixmap(QPixmap(value).scaledToWidth(width, QtCore.Qt.SmoothTransformation))
                        self.main_window.ui.image_preview.setText("")

                    QApplication.instance().processEvents()

    def default_parameters(self):
        return "?key=" + self.unique_key

    def set_last_received_file(self, file_name):
        # Update the current start date/time

        date, time, camera, wavelength = Helper.info_from_header_file(file_name)
        print("Camera: Info from HDR file: Camera:", camera, "Date/time:", date, time, "Wavelength", wavelength)

        # Convert to real date/time object and add 1 second. Filename looks like this: RaynCamera-2218FC_000000_20221031_085538
        new_start_date_time = datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M:%S')

        new_start_date_time = new_start_date_time + datetime.timedelta(seconds=1)

        print("Camera: Adjusted startDate for next poll:", new_start_date_time)

        self.start_date_time = new_start_date_time

    def current_iso_range(self):
        return (self.start_date_time.isoformat(), self.end_date_time.isoformat())

    def get_info(self):
        url = self.base_url + "/info" + self.default_parameters()
        try:
            r = requests.get(url, timeout=5)
            print(r.status_code, r.json())
            return r.json()
        except BaseException as e:
            print("GetInfo: Exception", e)
            return None

    def get_status(self):
        url = self.base_url + "/status" + self.default_parameters()
        try:
            r = requests.get(url, timeout=5)
            # print(r.status_code, r.json())
            return r.json()
        except BaseException as e:
            print("GetStatus: Exception", e)
            return None

    def delete_file(self, folder, file):
        url = self.base_url + "/files/delete" + self.default_parameters()

        template = '{ "filename": "" }'
        parameters = json.loads(template)
        parameters['filename'] = file
        parameters['source'] = folder

        try:
            r = requests.get(url, timeout=5, json=parameters)

            print("Response:", r)
        except:
            print("No camera found")

    def get_file(self, folder, file):
        url = self.base_url + "/files/get" + self.default_parameters()

        template = '{ "filename": "" }'
        parameters = json.loads(template)
        parameters['filename'] = file
        parameters['source'] = folder

        try:
            r = requests.get(url, timeout=5, json=parameters)
            image = r.content
            return image
        except:
            print("No camera found")
            return None

    def get_folder(self, folder):
        url = self.base_url + "/files/list" + self.default_parameters()

        template = '{ "source" : "" }'
        parameters = json.loads(template)
        parameters['source'] = folder

        try:
            r = requests.get(url, timeout=5, json=parameters)
            # print("getFolder:", r.status_code, r.json())
            return r.json()["files"]
        except:
            print("No camera found")
            return []

    def take_image(self):
        url = self.base_url + "/images/takeimage" + self.default_parameters()

        try:
            r = requests.get(url, timeout=120)  # Takes about a minute, so long timeout

            print("Camera: takeImage return files:", r.json()['files'])

            return r.json()['files']

        except BaseException as e:
            print("TakeImage: Unknown exception", e)
            return []

    def get_first_in_range(self):
        url = self.base_url + "/images/firstinrange" + self.default_parameters()

        self.end_date_time = datetime.datetime.now()

        start_date_time_iso, end_date_time_iso = self.current_iso_range()

        template = '{ "startDateTime": "", "endDateTime": "", "source" : "" }'
        json_start_end = json.loads(template)
        json_start_end['startDateTime'] = start_date_time_iso
        json_start_end['endDateTime'] = end_date_time_iso
        json_start_end['source'] = 'scheduler'

        print("Camera: GetFirstInRange: Polling camera for time range:", start_date_time_iso, end_date_time_iso)

        try:
            r = requests.get(url, json=json_start_end, timeout=10)

            if r is not None and r.status_code == 200:
                # print(r.status_code, r.json())

                json_files = r.json()['files']
                if len(json_files) > 0:
                    print("Camera: Replied with these files:", json_files)

                    self.get_files(json_files, self.main_window.experiment.camera_file_path, True, False)

                    # self.setLastReceivedFile(jsonFiles[-1])

                    return True
        except requests.exceptions.HTTPError as errh:
            print("GetFirstInRange: ", errh)
            self.main_window.add_status_text("No contact with camera")
        except requests.exceptions.ConnectionError as errc:
            print("GetFirstInRange: ", errc)
            self.main_window.add_status_text("No contact with camera")
        except requests.exceptions.Timeout as errt:
            print("GetFirstInRange: ", errt)
            self.main_window.add_status_text("No contact with camera")
        except requests.exceptions.RequestException as err:
            print("GetFirstInRange: ", err)
            self.main_window.add_status_text("No contact with camera")
        except BaseException as e:
            print("GetFirstInRange: Unknown exception", e)
            self.main_window.add_status_text("No contact with camera")

        return False

    def get_files(self, files, target_folder, analyze, delete_from_camera):
        print("Camera: Queue files for download:", files)
        print("Camera: Target folder:", target_folder)

        for file in files:
            self.files_to_fetch.append((file, target_folder, analyze, delete_from_camera,))

        self.main_window.ui.image_preview_progressbar.show()

        self.fetch_feedback_queue.put(["progressRange", len(self.files_to_fetch)])

    def identify(self):
        url = self.base_url + "/flashlight" + self.default_parameters()

        template = '{"spectrum": 9, "brightness": 100, "time": 200}'
        json_start_end = json.loads(template)

        print("Identify", url, json_start_end)

        try:
            r = requests.get(url, json=json_start_end, timeout=10)

            if r is not None and r.status_code == 200:
                print(r.status_code, r.json())

        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
        except BaseException as e:
            print("Identify: Unknown exception", e)