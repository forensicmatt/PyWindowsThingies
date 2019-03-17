import re
import ctypes
import struct
from ctypes import Structure
from ctypes.wintypes import *

RE_GUID_STRING = re.compile(
    '{([0-9A-F]{8})-([0-9A-F]{4})-([0-9A-F]{4})-([0-9A-F]{2})([0-9A-F]{2})-'
    '([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})'
    '([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})}',
    re.I
)


class GUID(Structure):
    _fields_ = [
        ("Data1", DWORD),
        ("Data2", WORD),
        ("Data3", WORD),
        ("Data4", ctypes.c_ubyte * 8)
    ]

    @staticmethod
    def from_string(guid_str):
        guid = GUID()
        match = RE_GUID_STRING.match(guid_str)
        if not match:
            raise Exception(
                "Not the correct GUID string format: {}".format(
                    guid_str
                )
            )

        g = [int(i, 16) for i in match.groups()]

        guid.Data1 = g[0]
        guid.Data2 = g[1]
        guid.Data3 = g[2]
        for i in range(8):
            guid.Data4[i] = g[3 + i]

        return guid

    def __str__(self):
        raw_buffer = ctypes.string_at(
            ctypes.byref(self),
            ctypes.sizeof(self)
        )
        return "{:08X}-{:04X}-{:04X}-{:02X}{:02X}-{:02X}{:02X}{:02X}{:02X}{:02X}{:02X}".format(
            struct.unpack("<L", raw_buffer[0:4])[0],
            struct.unpack("<H", raw_buffer[4:6])[0],
            struct.unpack("<H", raw_buffer[6:8])[0],
            struct.unpack("<B", raw_buffer[8:9])[0],
            struct.unpack("<B", raw_buffer[9:10])[0],
            struct.unpack("<B", raw_buffer[10:11])[0],
            struct.unpack("<B", raw_buffer[11:12])[0],
            struct.unpack("<B", raw_buffer[12:13])[0],
            struct.unpack("<B", raw_buffer[13:14])[0],
            struct.unpack("<B", raw_buffer[14:15])[0],
            struct.unpack("<B", raw_buffer[15:16])[0]
        )

    def __hash__(self):
        return hash(str(self))
