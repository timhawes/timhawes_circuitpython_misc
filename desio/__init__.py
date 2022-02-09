# SPDX-FileCopyrightText: 2021 Tim Hawes
#
# SPDX-License-Identifier: MIT

from . import pyDes

MODE_EBC = pyDes.ECB
MODE_CBC = pyDes.CBC

class DES:
    def __init__(self, key, mode=0, IV=None):
        self.context = pyDes.des(key, mode=mode, IV=IV)
    def encrypt_into(self, src, dest):
        dest[:] = self.context.encrypt(src)
    def decrypt_into(self, src, dest):
        dest[:] = self.context.decrypt(src)
    def rekey(self, key, iv=None):
        self.context.setKey(key)
        if iv:
            self.context.setIV(iv)
