import ctypes
from winthingies.win32.winstructs import *

advapi32 = ctypes.WinDLL('advapi32', use_last_error=True)


StartTrace = advapi32.StartTraceW
StartTrace.argtypes = [
    ctypes.POINTER(TRACEHANDLE),
    ctypes.c_wchar_p,
    ctypes.POINTER(EVENT_TRACE_PROPERTIES)
]
StartTrace.restype = ULONG


ControlTrace = advapi32.ControlTraceW
ControlTrace.argtypes = [
    TRACEHANDLE,
    PWCHAR,
    ctypes.POINTER(
        EVENT_TRACE_PROPERTIES
    ),
    ULONG
]
ControlTrace.restype = ULONG


OpenTraceW = advapi32.OpenTraceW
OpenTraceW.argtypes = [
    ctypes.POINTER(
        EVENT_TRACE_LOGFILE
    )
]
OpenTraceW.restype = TRACEHANDLE


ProcessTrace = advapi32.ProcessTrace
ProcessTrace.argtypes = [
    ctypes.POINTER(TRACEHANDLE),
    ULONG,
    ctypes.POINTER(
        FILETIME
    ),
    ctypes.POINTER(
        FILETIME
    )
]
ProcessTrace.restype = ULONG


CloseTrace = advapi32.CloseTrace
CloseTrace.argtypes = [
    TRACEHANDLE
]
CloseTrace.restype = ULONG


EnableTraceEx2 = advapi32.EnableTraceEx2
EnableTraceEx2.argtypes = [
    TRACEHANDLE,
    ctypes.POINTER(
        GUID
    ),
    ULONG,
    BYTE,
    ULONGLONG,
    ULONGLONG,
    ULONG,
    ctypes.POINTER(
        ENABLE_TRACE_PARAMETERS
    )
]
EnableTraceEx2.restype = ULONG