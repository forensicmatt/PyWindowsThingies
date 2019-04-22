import logging
from winthingies.win32.winstructs import *

LOGGER = logging.getLogger(__name__)
tdh = ctypes.WinDLL('Tdh', use_last_error=True)


tdh.TdhGetEventInformation.argtypes = [
    ctypes.POINTER(EVENT_RECORD),
    ULONG,
    ctypes.POINTER(TDH_CONTEXT),
    ctypes.POINTER(TRACE_EVENT_INFO),
    ctypes.POINTER(ULONG)
]
tdh.TdhGetEventInformation.restype = ULONG


tdh.TdhFormatProperty.argtypes = [
    ctypes.POINTER(TRACE_EVENT_INFO),
    ctypes.POINTER(EVENT_MAP_INFO),
    ULONG,
    USHORT,
    USHORT,
    USHORT,
    USHORT,
    ctypes.POINTER(BYTE),
    ctypes.POINTER(ULONG),
    ctypes.c_wchar_p,
    ctypes.POINTER(USHORT)
]
tdh.TdhFormatProperty.restype = ULONG


tdh.TdhGetEventMapInformation.argtypes = [
    ctypes.POINTER(EVENT_RECORD),
    LPWSTR,
    ctypes.POINTER(EVENT_MAP_INFO),
    ctypes.POINTER(ULONG)
]
tdh.TdhGetEventMapInformation.restype = ULONG


tdh.TdhGetPropertySize.argtypes = [
    ctypes.POINTER(EVENT_RECORD),
    ULONG,
    ctypes.POINTER(TDH_CONTEXT),
    ULONG,
    ctypes.POINTER(PROPERTY_DATA_DESCRIPTOR),
    ctypes.POINTER(ULONG)
]
tdh.TdhGetPropertySize.restype = ULONG


tdh.TdhGetProperty.argtypes = [
    ctypes.POINTER(EVENT_RECORD),
    ULONG,
    ctypes.POINTER(TDH_CONTEXT),
    ULONG,
    ctypes.POINTER(PROPERTY_DATA_DESCRIPTOR),
    ULONG,
    ctypes.POINTER(ctypes.c_byte)
]
tdh.TdhGetProperty.restype = ULONG
