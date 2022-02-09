# SPDX-FileCopyrightText: 2022 Tim Hawes
#
# SPDX-License-Identifier: MIT

class Backdoor:
    def __init__(self, pool, port, password):
        self.port = port
        self.password = password
        self.sock = pool.socket(type=pool.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.sock.bind(("0.0.0.0", port))

    def loop(self):
        buf = bytearray(1024)
        try:
            count, address = self.sock.recvfrom_into(buf)
            print("backdoor", address, buf[:count])
            if count > len(self.password) + 1:
                received_password = buf[0 : len(self.password) + 1]
                if received_password == self.password.encode("ascii") + b"\n":
                    try:
                        exec(buf[len(self.password) + 1 : count])
                    except Exception as e:
                        print("backdoor exception", e)
        except OSError as e:
            pass
