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

import time
import math

from EtcDiscover import EtcDiscover

import Config

class CameraDiscovery:

    # Container for device and timeout timer
    class CameraDevice:
        def __init__(self, device, timer):
            self.device = device
            self.timer = timer
            
            print("Camera: Create CameraDevice: Now:", math.ceil(time.perf_counter()), "Expire:", math.ceil(timer))

    def __init__(self, nic_ip_address, main_window, queue):
        self.camera_device_list = []               # list of all discovered devices
        self.discover = EtcDiscover(nic_ip_address)   # ETC discover protocol

        self.feedback_queue = queue

        print("Camera: Network IP for camera discovery:", nic_ip_address)

        main_window.camera_discovery = self

        while True:
            self.tick()

            print("Camera: tick:", math.ceil(time.perf_counter()))

            time.sleep(5)

    def change_ip_address(self, nic_ip_address):
        self.discover = EtcDiscover(nic_ip_address)

    def tick(self):
        # Poll camera discovery
        if self.discover:
            done = False
            while not done:
                json_object = self.discover.poll()        # poll for new devices

                if Config.verbose_mode:
                    print("Camera poll:", math.ceil(time.perf_counter()), json_object)

                TIMEOUT = 20  # timeout in seconds

                if json_object and json_object['cid']:  # valid json object?
                    replaced = False

                    for item in self.camera_device_list[:]:      # handle all devices in list
                        if item.device['cid'] == json_object['cid']:   # replace existing

                            if Config.verbose_mode:
                                print("Camera: Update existing")

                            self.camera_device_list.remove(item)
                            self.camera_device_list.append(self.CameraDevice(json_object, time.perf_counter() + TIMEOUT))
                            # TODO? Update mainWindow.cameras
                            replaced = True

                    # Add device to list
                    if not replaced:
                        self.camera_device_list.append(self.CameraDevice(json_object, time.perf_counter() + TIMEOUT))

                        self.feedback_queue.put(["addCamera", json_object["cid"], json_object])

                        if Config.verbose_mode:
                            print("Camera: Found new camera:", json_object)
                        else:
                            print("Camera: Found new camera:", json_object['name'] + ", " + json_object['version']['main'] + ", " + json_object['tags']['disc']['ipv4'])
                else:
                    done = True

            # Check for removal
            for item in self.camera_device_list[:]:          # handle all devices in list
                if item is not None and time.perf_counter() > item.timer:  # remove on timeout
                    self.camera_device_list.remove(item)     # remove device from list

                    self.feedback_queue.put(["removeCamera", item.device["cid"]])

                    print("Camera: Lost existing camera", item.device, "Removed after", time.perf_counter() - item.timer, "seconds")
