import ctypes
from ctypes import *
from ctypes.wintypes import *
from winthingies.win32.winstructs import *

ntdll = ctypes.WinDLL('ntdll', use_last_error=True)
NTSTATUS = DWORD


ntdll.NtQueryObject.argtypes = [
    HANDLE,
    DWORD,
    c_void_p,
    DWORD,
    DWORD
]
ntdll.NtQueryObject.restype = NTSTATUS

ntdll.NtQuerySystemInformation.argtypes = [
    DWORD,
    c_void_p,
    DWORD,
    POINTER(DWORD)
]
ntdll.NtQuerySystemInformation.restype = NTSTATUS
