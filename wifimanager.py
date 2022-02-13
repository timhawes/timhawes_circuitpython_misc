# SPDX-FileCopyrightText: 2022 Tim Hawes
#
# SPDX-License-Identifier: MIT

import binascii
import json
import microcontroller
import wifi


class WiFiManager:
    def __init__(self, hostname=None):
        self._connected_state = False
        self._connect_count = 0

        self.connected_callback = None
        self.disconnected_callback = None

        if hostname:
            wifi.radio.hostname = hostname
        else:
            wifi.radio.hostname = "esp-{}".format(
                binascii.hexlify(microcontroller.cpu.uid).decode("ascii")
            )

        self.reconfigure()

    def reconfigure(self):
        try:
            with open("/wifi.json", "r") as f:
                data = json.load(f)
            wifi.radio.connect(data["ssid"], data["password"], timeout=-1)
        except OSError:
            print("WiFiManager: /wifi.json not found")

    @property
    def connect_count(self):
        return self._connect_count

    @property
    def connected(self):
        if wifi.radio.ap_info is None:
            return False
        if wifi.radio.ipv4_address is None:
            return False
        if str(wifi.radio.ipv4_address) == "0.0.0.0":
            return False
        if str(wifi.radio.ipv4_dns) == "0.0.0.0":
            return False
        return True

    def loop(self):
        if self._connected_state is False:
            if self.connected:
                print(
                    "WiFiManager: connected ssid={} ipv4={}".format(
                        wifi.radio.ap_info.ssid, wifi.radio.ipv4_address
                    )
                )
                self._connected_state = True
                self._connect_count += 1
                if self.connected_callback:
                    self.connected_callback()
        elif self._connected_state is True:
            if not self.connected:
                print("WiFiManager: disconnected")
                self._connected_state = False
                if self.disconnected_callback:
                    self.disconnected_callback()
