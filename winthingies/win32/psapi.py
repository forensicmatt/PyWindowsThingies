import ctypes
from ctypes.wintypes import *

psapi = ctypes.WinDLL('psapi', use_last_error=True)


psapi.GetProcessImageFileNameW.restype = DWORD
psapi.GetProcessImageFileNameW.argtypes = [
    HANDLE,
    LPWSTR,
    DWORD
]


psapi.GetProcessImageFileNameA.restype = DWORD
psapi.GetProcessImageFileNameA.argtypes = [
    HANDLE,
    LPSTR,
    DWORD
]
