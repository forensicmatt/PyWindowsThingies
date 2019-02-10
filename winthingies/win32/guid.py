import re
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
        ("Data4", BYTE * 8)
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
