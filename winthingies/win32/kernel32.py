import ctypes
from ctypes.wintypes import *
from winthingies.win32.winstructs import *

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)


kernel32.GetCurrentProcess.restype = HANDLE


kernel32.OpenProcess.restype = HANDLE
kernel32.OpenProcess.argtypes = [
    DWORD,
    BOOL,
    DWORD
]


kernel32.GetProcessId.restype = DWORD
kernel32.GetProcessId.argtypes = [
    HANDLE
]

kernel32.DuplicateHandle.argtypes = [
    HANDLE,
    HANDLE,
    HANDLE,
    ctypes.POINTER(HANDLE),
    DWORD,
    BOOL,
    DWORD
]
kernel32.DuplicateHandle.restype = BOOL


kernel32.CloseHandle.argtypes = [
    HANDLE
]
kernel32.CloseHandle.restype = BOOL


kernel32.CreateToolhelp32Snapshot.restype = DWORD
kernel32.CreateToolhelp32Snapshot.argtypes = [
    DWORD,
    DWORD
]


kernel32.Process32First.restype = BOOL
kernel32.Process32First.argtypes = [
    HANDLE,
    ctypes.POINTER(PROCESSENTRY32)
]


kernel32.Process32Next.argtypes = [
    HANDLE,
    ctypes.POINTER(PROCESSENTRY32)
]
kernel32.Process32Next.restype = BOOL