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

import json
import random

import paho.mqtt.client as mqtt

from PySide6 import QtCore
from PySide6.QtCore import QObject

from Helper import tprint

QOS = 2

class Mqtt(QObject):
    status_changed = QtCore.Signal(str, bool)

    def __init__(self, broker, port):
        QObject.__init__(self)

        client_name = "pythonCamera_" + str(random.randint(0, 10000))

        self.connected = False

        tprint("MQTT: Connecting to", broker, port)
        tprint("MQTT: Client name", client_name)

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_name)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        self.connected = False

        self.broker = broker
        self.port = port

    def start(self):
        tprint("MQTT: Connecting...")

        try:
            self.client.connect(self.broker, self.port)
        except Exception as e:
            tprint("MQTT: No broker found", e)

            self.status_changed.emit("Broker not found", True)

        # client.subscribe("rayn/controller/+/discovery/#")  # <controllerId>

        self.client.loop_start()

    def on_connect(self, _client, _userdata, _flags, _rc):
        tprint("MQTT: Connected")

        self.connected = True

        self.status_changed.emit("Connected", False)

    def on_disconnect(self, _client, userdata, rc):
        tprint("MQTT: Disconnected: ", userdata, rc)

        self.connected = False

        self.status_changed.emit("Disconnected", True)

    def on_publish(self, _client, _userdata, _result):
        tprint("MQTT: Data published: ", _userdata, _result)

    def on_message(self, _client, _userdata, message):
        # tprint("Received message: " + message.topic + str(message.payload.decode("utf-8")))

        if message is None or message.topic is None or message.payload is None:
            return

        # jsonData = json.loads(message.payload)

    def subscribe_mqtt(self, topic):
        tprint("MQTT: Subscribe:", topic)

        self.client.subscribe(topic)

    def publish_roi(self, camera_name, roi_number, payload):
        tprint("MQTT: Publish:", camera_name, roi_number, payload)

        j = json.dumps(payload, indent=4)

        self.client.publish("rayn/camera/" + camera_name + "/roi/" + str(roi_number), j, QOS)
