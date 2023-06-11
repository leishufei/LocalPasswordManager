#!usr/bin/env python3
# -*- coding: utf-8 -*-
# @Software : PyCharm
import base64
import json
from hashlib import md5
from typing import Dict

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

KEY = '_aes_key_'
IV = '_aes_iv_'


class DataProcessor:
    def __init__(self):
        self.key = self.align(KEY).encode()
        self.iv = self.align(IV).encode()
        self.block_size = AES.block_size

    @staticmethod
    def align(data: str) -> str:
        while len(data) % 16 != 0:
            data += '\0'
        return data

    def encrypt(self, data: str) -> str:
        cipher = AES.new(key=self.key, mode=AES.MODE_CBC, iv=self.iv)
        encrypted_data = cipher.encrypt(pad(data.encode('utf8'), block_size=self.block_size))
        return base64.b64encode(encrypted_data).decode('utf8')

    def decrypt(self, data: str) -> str:
        cipher = AES.new(key=self.key, mode=AES.MODE_CBC, iv=self.iv)
        decrypted_data = cipher.decrypt(base64.b64decode(data.encode('utf8')))
        return unpad(decrypted_data, block_size=AES.block_size).decode('utf8')

    @staticmethod
    def compress(data: Dict) -> str:
        return json.dumps(data, separators=(",", ":"))

    def hash(self, data: Dict) -> str:
        return md5(self.compress(data).encode()).hexdigest()
