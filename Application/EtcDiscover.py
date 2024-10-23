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

import socket
import struct
import platform
import json

from Helper import tprint

class EtcDiscover:
    MULTICAST_ADDRESS = "239.69.84.67"
    MULTICAST_PORT = 6107

    HEADER = "ETCLINK\0\0\0\0\0\0\0\0\1"  # ETC protocol header
    ip_interface = 'any'
    sock = 0

    # create multicast socket, socket is None when failed
    def __create_multicast_socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            # Set this socket to be reusable.
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Set the number of multicast hops to make
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

            if self.ip_interface != 'any':
                if platform.system() != "Windows":
                    sock.bind((self.MULTICAST_ADDRESS, self.MULTICAST_PORT))
                else:
                    sock.bind((self.ip_interface, self.MULTICAST_PORT))
                mreq = socket.inet_aton(self.MULTICAST_ADDRESS) + socket.inet_aton(self.ip_interface)
            else:
                if platform.system() != "Windows":
                    sock.bind((self.MULTICAST_ADDRESS, self.MULTICAST_PORT))
                else:
                    sock.bind(('', self.MULTICAST_PORT))
                mreq = struct.pack("=4sl", socket.inet_aton(self.MULTICAST_ADDRESS), socket.INADDR_ANY)

            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            sock.settimeout(1)
        except:
            sock = None
            tprint('opening mulitcast failed')
        return sock

    # check frame data on valid size and valid header
    def __frame_is_valid(self, data):
        n = 0
        if len(data) > len(self.HEADER):   # compare Header
            while n < len(self.HEADER) and data[n] == ord(self.HEADER[n]):
                n += 1
        return n == len(self.HEADER)       # return true on valid header

    # convert frame data to a Json object
    def __frame_2_json(self, data):
        str = ''
        for item in data:
            str += chr(item)
        str += chr(0)                    # add null char to get end of string
        json_string = str[len(self.HEADER):-1]  # split string, remove Header
        # tprint( jsonString )
        return json.loads(json_string)

    # receive new devices and convert them to json
    def poll(self):
        json_object = None

        if self.sock is not None:             # valid socket?
            try:
                data, addr = self.sock.recvfrom(1024)
            except socket.error as e:
                data = None  # nothing to do no data
            else:
                if self.__frame_is_valid(data):
                    json_object = self.__frame_2_json(data)
        return json_object

    # initialize
    def __init__(self, ip_interface):
        self.ip_interface = ip_interface
        self.sock = self.__create_multicast_socket()
