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

import json
import math
import time

import Config
from EtcDiscover import EtcDiscover
from Helper import tprint


class CameraDiscovery:

    # Container for device and timeout timer
    class CameraDevice:
        def __init__(self, device, timer):
            self.device = device
            self.timer = timer

            if Config.verbose_mode:
                tprint("Camera: Create CameraDevice: Now:", math.ceil(time.perf_counter()), "Expire:", math.ceil(timer))

    def __init__(self, nic_ip_address, main_window): #, queue):
        self.camera_device_list = []               # list of all discovered devices
        self.discover = EtcDiscover(nic_ip_address)   # ETC discover protocol

        tprint("Camera: Network IP for camera discovery:", nic_ip_address)

        self.main_window = main_window

        self.main_window.camera_discovery = self

        while not self.main_window.stop_camera_discovery_worker:
            self.tick()

            if Config.verbose_mode:
               tprint("Camera: tick:", math.ceil(time.perf_counter()))

            time.sleep(5)

        tprint("Camera discovery thread stopped")

    def change_ip_address(self, nic_ip_address):
        self.discover = EtcDiscover(nic_ip_address)

    def tick(self):
        # Poll camera discovery
        if self.discover:
            done = False
            while not done:
                json_object = self.discover.poll()        # poll for new devices

                if Config.verbose_mode:
                    tprint("Camera poll:", math.ceil(time.perf_counter()), json_object)

                TIMEOUT = 20  # timeout in seconds

                if json_object and json_object['cid']:  # valid json object?
                    replaced = False

                    for item in self.camera_device_list[:]:      # handle all devices in list
                        if item.device['cid'] == json_object['cid']:   # replace existing

                            if Config.verbose_mode:
                                tprint("Camera: Update existing")

                            self.camera_device_list.remove(item)
                            self.camera_device_list.append(self.CameraDevice(json_object,
                                                                             time.perf_counter() + TIMEOUT))
                            # TODO? Update mainWindow.cameras
                            replaced = True

                    # Add device to list
                    if not replaced:
                        self.camera_device_list.append(self.CameraDevice(json_object, time.perf_counter() + TIMEOUT))

                        self.main_window.camera_discovery_worker.signals.add_camera.emit(json_object["cid"],
                                                                                         json.dumps(json_object))

                        if Config.verbose_mode:
                            tprint("Camera: Found new camera:", json_object)
                        else:
                            tprint("Camera: Found new camera:", json_object['name'] + ", " +
                                   json_object['version']['main'] + ", " + json_object['tags']['disc']['ipv4'])
                else:
                    done = True

            # Check for removal
            for item in self.camera_device_list[:]:          # handle all devices in list
                if item is not None and time.perf_counter() > item.timer:  # remove on timeout
                    self.camera_device_list.remove(item)     # remove device from list

                    self.main_window.camera_discovery_worker.signals.remove_camera.emit(item.device["cid"])

                    tprint("Camera: Lost existing camera", item.device, "Removed after",
                           time.perf_counter() - item.timer, "seconds")
