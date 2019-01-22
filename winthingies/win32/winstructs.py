import ctypes
from ctypes import *
from ctypes.wintypes import *

PWSTR = LPWSTR
PVOID = c_void_p
ACCESS_MASK = DWORD


class _SYSTEM_HANDLE(Structure):
    _fields_ = [
        ("dwProcessId", DWORD),
        ("bObjectType", BYTE),
        ("bFlags", BYTE),
        ("wValue", WORD),
        ("pAddress", PVOID),
        ("GrantedAccess", DWORD),
    ]
SYSTEM_HANDLE = _SYSTEM_HANDLE


class _SYSTEM_HANDLE_INFORMATION(Structure):
    _fields_ = [
        ("HandleCount", ULONG),
        ("Handles", SYSTEM_HANDLE * 1),
    ]
PSYSTEM_HANDLE_INFORMATION = POINTER(_SYSTEM_HANDLE_INFORMATION)
SYSTEM_HANDLE_INFORMATION = _SYSTEM_HANDLE_INFORMATION


class SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX(Structure):
    _fields_ = [
        ("Object", PVOID),
        ("UniqueProcessId", PVOID),
        ("HandleValue", PVOID),
        ("GrantedAccess", ULONG),
        ("CreatorBackTraceIndex", USHORT),
        ("ObjectTypeIndex", USHORT),
        ("HandleAttributes", ULONG),
        ("Reserved", ULONG),
]


class SYSTEM_HANDLE_INFORMATION_EX(Structure):
    _fields_ = [
        ("NumberOfHandles", PVOID),
        ("Reserved", PVOID),
        ("Handles", SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX * 1),
]

class _LSA_UNICODE_STRING(Structure):
    _fields_ = [
        ("Length", USHORT),
        ("MaximumLength", USHORT),
        ("Buffer", PVOID),
    ]
PUNICODE_STRING = POINTER(_LSA_UNICODE_STRING)
UNICODE_STRING = _LSA_UNICODE_STRING
LSA_UNICODE_STRING = _LSA_UNICODE_STRING
PLSA_UNICODE_STRING = POINTER(_LSA_UNICODE_STRING)

INITIAL_LSA_UNICODE_STRING = _LSA_UNICODE_STRING

class _LSA_UNICODE_STRING(INITIAL_LSA_UNICODE_STRING):
    @property
    def str(self):
        """Special thanks to
        https://github.com/hakril/PythonForWindows/blob/master/windows/generated_def/winstructs.py#L4034

        :type: :class:`unicode`
        """
        if not self.Length:
            return ""
        if getattr(self, "_target", None) is not None:
            raw_data = self._target.read_memory(self.Buffer, self.Length)
            return raw_data.decode("utf16")
        size = self.Length // 2
        return (ctypes.c_wchar * size).from_address(self.Buffer)[:]

    def __repr__(self):
        return """<{0} "{1}" at {2}>""".format(
            type(self).__name__, self.str, hex(id(self))
        )

    def __sprint__(self):
        try:
            return self.__repr__()
        except TypeError as e:
            # Bad buffer: print raw infos
            return """<{0} len={1} maxlen={2} buffer={3}>""".format(
                type(self).__name__, self.Length, self.MaximumLength, self.Buffer
            )

PUNICODE_STRING = POINTER(_LSA_UNICODE_STRING)
UNICODE_STRING = _LSA_UNICODE_STRING
LSA_UNICODE_STRING = _LSA_UNICODE_STRING
PLSA_UNICODE_STRING = POINTER(_LSA_UNICODE_STRING)


class __PUBLIC_OBJECT_TYPE_INFORMATION(Structure):
    _fields_ = [
        ("TypeName", UNICODE_STRING),
        ("Reserved", ULONG * 22),
    ]
PPUBLIC_OBJECT_TYPE_INFORMATION = POINTER(__PUBLIC_OBJECT_TYPE_INFORMATION)
PUBLIC_OBJECT_TYPE_INFORMATION = __PUBLIC_OBJECT_TYPE_INFORMATION

class _PUBLIC_OBJECT_BASIC_INFORMATION(Structure):
    _fields_ = [
        ("Attributes", ULONG),
        ("GrantedAccess", ACCESS_MASK),
        ("HandleCount", ULONG),
        ("PointerCount", ULONG),
        ("Reserved", ULONG * 10),
    ]
PUBLIC_OBJECT_BASIC_INFORMATION = _PUBLIC_OBJECT_BASIC_INFORMATION
PPUBLIC_OBJECT_BASIC_INFORMATION = POINTER(_PUBLIC_OBJECT_BASIC_INFORMATION)
