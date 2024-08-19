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

QOS = 2

class Mqtt:
    def __init__(self, broker, port):

        client_name = "pythonCamera_" + str(random.randint(0, 10000))

        print("MQTT: Connecting to", broker, port)
        print("MQTT: Client name", client_name)

        self.client = mqtt.Client(client_name)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        print("MQTT: Connecting...")

        try:
            self.client.connect(broker, port)
        except Exception as e:
            print("MQTT: No broker found", e)

        # client.subscribe("rayn/controller/+/discovery/#")  # <controllerId>

        self.client.loop_start()

    def on_connect(self, _client, _userdata, _flags, _rc):
        print("MQTT: Connected")

    def on_disconnect(self, _client, userdata, rc):
        print("MQTT: Disconnected: ", userdata, rc)
        pass

    def on_publish(self, _client, _userdata, _result):
        # print("Data published: ", userdata, result)
        pass

    def on_message(self, _client, _userdata, message):
        # print("Received message: " + message.topic + str(message.payload.decode("utf-8")))

        if message is None or message.topic is None or message.payload is None:
            return

        # jsonData = json.loads(message.payload)

    def subscribe_mqtt(self, topic):
        self.client.subscribe(topic)

    def publish_roi(self, camera_name, roi_number, payload):
        j = json.dumps(payload, indent=4)

        self.client.publish("rayn/camera/" + camera_name + "/roi/" + str(roi_number), j, QOS)
