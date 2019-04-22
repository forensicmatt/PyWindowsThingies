import logging
import ctypes
from ctypes import *
from ctypes.wintypes import *
from winthingies.win32.const import *
from winthingies.win32.guid import GUID
from winthingies.win32.helpers import get_formatted_value, rel_ptr_to_str

LOGGER = logging.getLogger(__name__)

PWSTR = LPWSTR
PVOID = c_void_p
ACCESS_MASK = DWORD
ULONG_PTR = PVOID
TRACEHANDLE = c_uint64
UCHAR = c_ubyte
ULONG64 = c_uint64
ULONGLONG = c_ulonglong
LONGLONG = c_longlong
PWCHAR = c_wchar_p
DECODING_SOURCE = ctypes.c_uint
PROPERTY_FLAGS = ctypes.c_uint
TDH_CONTEXT_TYPE = ctypes.c_uint
MAP_FLAGS = ctypes.c_uint
EVT_HANDLE = HANDLE
INT8 = c_byte
INT16 = SHORT
INT32 = INT
INT64 = LONGLONG
UINT8 = BYTE
UINT16 = USHORT
UINT32 = UINT
UINT64 = ULONGLONG
PSID = PVOID
SIZE_T = c_size_t
EVT_OBJECT_ARRAY_PROPERTY_HANDLE = HANDLE


class FILETIME(Structure):
    _fields_ = [
        ('dwLowDateTime', DWORD),
        ('dwHighDateTime', DWORD)
    ]


class SYSTEMTIME(Structure):
    _fields_ = [
        ('wYear', WORD),
        ('wMonth', WORD),
        ('wDayOfWeek', WORD),
        ('wDay', WORD),
        ('wHour', WORD),
        ('wMinute', WORD),
        ('wSecond', WORD),
        ('wMilliseconds', WORD)
    ]


class TIME_ZONE_INFORMATION(Structure):
    _fields_ = [
        ('Bias', LONG),
        ('StandardName', WCHAR * 32),
        ('StandardDate', SYSTEMTIME),
        ('StandardBias', LONG),
        ('DaylightName', WCHAR * 32),
        ('DaylightDate', SYSTEMTIME),
        ('DaylightBias', LONG)
    ]


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


class PROCESSENTRY32(Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("cntUsage", DWORD),
        ("th32ProcessID", DWORD),
        ("th32DefaultHeapID", ULONG_PTR),
        ("th32ModuleID", DWORD),
        ("cntThreads", DWORD),
        ("th32ParentProcessID", DWORD),
        ("pcPriClassBase", LONG),
        ("dwFlags", DWORD),
        ("szExeFile", CHAR * MAX_PATH),
    ]

    def clone(self):
        return PROCESSENTRY32(
            self.dwSize,
            self.cntUsage,
            self.th32ProcessID,
            self.th32DefaultHeapID,
            self.th32ModuleID,
            self.cntThreads,
            self.th32ParentProcessID,
            self.pcPriClassBase,
            self.dwFlags,
            self.szExeFile
        )

    def as_dict(self):
        return {
            "dwSize": self.dwSize,
            "cntUsage": self.cntUsage,
            "th32ProcessID": self.th32ProcessID,
            "th32DefaultHeapID": self.th32DefaultHeapID,
            "th32ModuleID": self.th32ModuleID,
            "cntThreads": self.cntThreads,
            "th32ParentProcessID": self.th32ParentProcessID,
            "pcPriClassBase": self.pcPriClassBase,
            "dwFlags": self.dwFlags,
            "szExeFile": self.szExeFile.decode("utf-8")
        }


#########################################################################
# Event Structs
#########################################################################
class EVENT_DESCRIPTOR(Structure):
    _fields_ = [
        ('Id', USHORT),
        ('Version', UCHAR),
        ('Channel', UCHAR),
        ('Level', UCHAR),
        ('Opcode', UCHAR),
        ('Task', USHORT),
        ('Keyword', ULONGLONG)
    ]

    def as_dict(self):
        return {
            "Id": self.Id,
            "Version": self.Version,
            "Channel": self.Channel,
            "Level": self.Level,
            "Opcode": self.Opcode,
            "Task": self.Task,
            "Keyword": self.Keyword,
        }


class EVENT_HEADER(Structure):
    _fields_ = [
        ('Size', USHORT),
        ('HeaderType', USHORT),
        ('Flags', USHORT),
        ('EventProperty', USHORT),
        ('ThreadId', ULONG),
        ('ProcessId', ULONG),
        ('TimeStamp', LARGE_INTEGER),
        ('ProviderId', GUID),
        ('EventDescriptor', EVENT_DESCRIPTOR),
        ('KernelTime', ULONG),
        ('UserTime', ULONG),
        ('ActivityId', GUID)
    ]

    def as_dict(self):
        return {
            "Size": self.Size,
            "HeaderType": self.HeaderType,
            "Flags": self.Flags,
            "EventProperty": self.EventProperty,
            "ThreadId": self.ThreadId,
            "ProcessId": self.ProcessId,
            "TimeStamp": self.TimeStamp,
            "ProviderId": str(self.ProviderId),
            "EventDescriptor": self.EventDescriptor.as_dict(),
            "KernelTime": self.KernelTime,
            "UserTime": self.UserTime,
            "ActivityId": str(self.ActivityId)
        }


class ETW_BUFFER_CONTEXT(Structure):
    _fields_ = [
        ('ProcessorNumber', UCHAR),
        ('Alignment', UCHAR),
        ('LoggerId', USHORT)
    ]


class EVENT_HEADER_EXTENDED_DATA_ITEM(Structure):
    _fields_ = [
        ('Reserved1', USHORT),
        ('ExtType', USHORT),
        ('Linkage', USHORT),
        ('DataSize', USHORT),
        ('DataPtr', ULONGLONG)
    ]


class EVENT_RECORD(Structure):
    _fields_ = [
        ('EventHeader', EVENT_HEADER),
        ('BufferContext', ETW_BUFFER_CONTEXT),
        ('ExtendedDataCount', USHORT),
        ('UserDataLength', USHORT),
        ('ExtendedData', POINTER(EVENT_HEADER_EXTENDED_DATA_ITEM)),
        ('UserData', PVOID),
        ('UserContext', PVOID)
    ]

    @property
    def TraceEventInfo(self):
        trace_event_info = ctypes.POINTER(
            TRACE_EVENT_INFO
        )()
        buffer_size = DWORD()

        # Call TdhGetEventInformation once to get the required buffer size and again to actually populate the structure.
        status = tdh.TdhGetEventInformation(
            self,
            0,
            None,
            None,
            ctypes.byref(buffer_size)
        )
        if ERROR_INSUFFICIENT_BUFFER == status:
            trace_event_info = ctypes.cast(
                (ctypes.c_byte * buffer_size.value)(),
                ctypes.POINTER(TRACE_EVENT_INFO)
            )
            status = tdh.TdhGetEventInformation(
                self,
                0,
                None,
                trace_event_info,
                ctypes.byref(buffer_size)
            )

        if ERROR_SUCCESS != status:
            raise ctypes.WinError(status)

        return trace_event_info.contents

    @property
    def Properties(self):
        trace_event_info = self.TraceEventInfo
        for event_property_info in trace_event_info.iter_properties():
            prop_name = event_property_info.get_property_name(
                trace_event_info
            )

            prop_data = event_property_info.get_property_data(
                self,
                trace_event_info
            )

            yield prop_name, prop_data

    def as_dict(self):
        info = {
            "EventHeader": self.EventHeader.as_dict(),
            "EventInfo": self.TraceEventInfo.as_dict(),
            "Properties": dict(self.Properties)
        }
        return info

# https://docs.microsoft.com/en-us/windows/desktop/api/evntrace/ns-evntrace-event_trace_header
# Class
class EVENT_TRACE_HEADER_CLASS(Structure):
    _fields_ = [
        ('Type', UCHAR),
        ('Level', UCHAR),
        ('Version', USHORT)
    ]


class EVENT_TRACE_HEADER(Structure):
    _fields_ = [
        ('Size', USHORT),
        ('HeaderType', UCHAR),
        ('MarkerFlags', UCHAR),
        ('Class', EVENT_TRACE_HEADER_CLASS),
        ('ThreadId', ULONG),
        ('ProcessId', ULONG),
        ('TimeStamp', LARGE_INTEGER),
        ('Guid', GUID),
        ('ClientContext', ULONG),
        ('Flags', ULONG)
    ]


class EVENT_TRACE(Structure):
    _fields_ = [
        ('Header', EVENT_TRACE_HEADER),
        ('InstanceId', ULONG),
        ('ParentInstanceId', ULONG),
        ('ParentGuid', GUID),
        ('MofData', PVOID),
        ('MofLength', ULONG),
        ('ClientContext', ULONG)
    ]


class TRACE_LOGFILE_HEADER(Structure):
    _fields_ = [
        ('BufferSize', ULONG),
        ('MajorVersion', BYTE),
        ('MinorVersion', BYTE),
        ('SubVersion', BYTE),
        ('SubMinorVersion', BYTE),
        ('ProviderVersion', ULONG),
        ('NumberOfProcessors', ULONG),
        ('EndTime', LARGE_INTEGER),
        ('TimerResolution', ULONG),
        ('MaximumFileSize', ULONG),
        ('LogFileMode', ULONG),
        ('BuffersWritten', ULONG),
        ('StartBuffers', ULONG),
        ('PointerSize', ULONG),
        ('EventsLost', ULONG),
        ('CpuSpeedInMHz', ULONG),
        ('LoggerName', PWCHAR),
        ('LogFileName', PWCHAR),
        ('TimeZone', TIME_ZONE_INFORMATION),
        ('BootTime', LARGE_INTEGER),
        ('PerfFreq', LARGE_INTEGER),
        ('StartTime', LARGE_INTEGER),
        ('ReservedFlags', ULONG),
        ('BuffersLost', ULONG)
    ]


#########################################################################
# ETW Structs
#########################################################################
class WNODE_HEADER(Structure):
    _fields_ = [
        ('BufferSize', ULONG),
        ('ProviderId', ULONG),
        ('HistoricalContext', ULONG64),
        ('Timestamp', LARGE_INTEGER),
        ('Guid', GUID),
        ('ClientContext', ULONG),
        ('Flags', ULONG)
    ]


class EVENT_TRACE_PROPERTIES(Structure):
    _fields_ = [
        ('Wnode', WNODE_HEADER),
        ('BufferSize', ULONG),
        ('MinimumBuffers', ULONG),
        ('MaximumBuffers', ULONG),
        ('MaximumFileSize', ULONG),
        ('LogFileMode', ULONG),
        ('FlushTimer', ULONG),
        ('EnableFlags', ULONG),
        ('AgeLimit', LONG),
        ('NumberOfBuffers', ULONG),
        ('FreeBuffers', ULONG),
        ('EventsLost', ULONG),
        ('BuffersWritten', ULONG),
        ('LogBuffersLost', ULONG),
        ('RealTimeBufferLost', ULONG),
        ('LoggerThreadId', HANDLE),
        ('LogFileNameOffset', ULONG),
        ('LoggerNameOffset', ULONG)
    ]


# This must be "forward declared", because of the callback type below,
# which is contained in the ct.Structure.
class EVENT_TRACE_LOGFILE(Structure):
    pass


# The type for event trace callbacks.
EVENT_RECORD_CALLBACK = WINFUNCTYPE(
    None,
    POINTER(EVENT_RECORD)
)
EVENT_TRACE_BUFFER_CALLBACK = WINFUNCTYPE(
    ULONG,
    POINTER(EVENT_TRACE_LOGFILE)
)
EVENT_TRACE_LOGFILE._fields_ = [
    ('LogFileName', PWCHAR),
    ('LoggerName', PWCHAR),
    ('CurrentTime', LONGLONG),
    ('BuffersRead', ULONG),
    ('ProcessTraceMode', ULONG),
    ('CurrentEvent', EVENT_TRACE),
    ('LogfileHeader', TRACE_LOGFILE_HEADER),
    ('BufferCallback', EVENT_TRACE_BUFFER_CALLBACK),
    ('BufferSize', ULONG),
    ('Filled', ULONG),
    ('EventsLost', ULONG),
    ('EventRecordCallback', EVENT_RECORD_CALLBACK),
    ('IsKernelTrace', ULONG),
    ('Context', PVOID)
]


class EVENT_FILTER_DESCRIPTOR(Structure):
    _fields_ = [
        ('Ptr', ULONGLONG),
        ('Size', ULONG),
        ('Type', ULONG)
    ]


class ENABLE_TRACE_PARAMETERS(Structure):
    _fields_ = [
        ('Version', ULONG),
        ('EnableProperty', ULONG),
        ('ControlFlags', ULONG),
        ('SourceId', GUID),
        ('EnableFilterDesc', POINTER(EVENT_FILTER_DESCRIPTOR)),
        ('FilterDescCount', ULONG)
    ]


# https://docs.microsoft.com/en-us/windows/desktop/api/tdh/ns-tdh-_event_property_info
class nonStructType(Structure):
    _fields_ = [
        ('InType', USHORT),
        ('OutType', USHORT),
        ('MapNameOffset', ULONG)
    ]


class structType(Structure):
    _fields_ = [
        ('StructStartIndex', USHORT),
        ('NumOfStructMembers', USHORT),
        ('padding', ULONG)
    ]


class customSchemaType(Structure):
    _fields_ = [
        ('padding2', USHORT),
        ('OutType', USHORT),
        ('CustomSchemaOffset', ULONG)
    ]


class EpiU1(Union):
    _fields_ = [
        ("nonStructType", nonStructType),
        ("structType", structType),
        ("customSchemaType", customSchemaType)
    ]


class EpiU2(Union):
    _fields_ = [
        ("count", USHORT),
        ("countPropertyIndex", USHORT)
    ]


class EpiU3(Union):
    _fields_ = [
        ("length", USHORT),
        ("lengthPropertyIndex", USHORT)
    ]


class EpiU4(Union):
    _fields_ = [
        ("Reserved", ULONG),
        ("Tags", ULONG)
    ]


class EVENT_PROPERTY_INFO(Structure):
    _fields_ = [
        ('Flags', PROPERTY_FLAGS),
        ('NameOffset', ULONG),
        ('epi_u1', EpiU1),
        ('epi_u2', EpiU2),
        ('epi_u3', EpiU3),
        ('epi_u4', EpiU4)
    ]

    def get_event_map_info(self, event_record, event_info):
        """
        When parsing a field in the event property structure, there may be a mapping between a given
        name and the structure it represents. If it exists, we retrieve that mapping here.

        Because this may legitimately return a NULL value we return a tuple containing the success or
        failure status as well as either None (NULL) or an EVENT_MAP_INFO pointer.

        :param self: The EVENT_PROPERTY_INFO structure for the TopLevelProperty of the event we are parsing
        :param event_record: The EventRecord structure for the event we are parsing
        :param event_info: The TraceEventInfo structure for the event we are parsing
        :return: A tuple of the map_info structure and boolean indicating whether we succeeded or not
        """
        map_name = rel_ptr_to_str(
            pointer(event_info),
            self.epi_u1.nonStructType.MapNameOffset
        )
        map_size = DWORD()
        map_info = ctypes.POINTER(EVENT_MAP_INFO)()

        status = tdh.TdhGetEventMapInformation(
            event_record,
            map_name,
            None,
            ctypes.byref(map_size)
        )
        if ERROR_INSUFFICIENT_BUFFER == status:
            map_info = ctypes.cast(
                (ctypes.c_char * map_size.value)(),
                ctypes.POINTER(EVENT_MAP_INFO)
            )
            status = tdh.TdhGetEventMapInformation(
                event_record,
                map_name,
                map_info,
                ctypes.byref(map_size)
            )

        if ERROR_SUCCESS == status:
            return map_info, True

        # ERROR_NOT_FOUND is actually a perfectly acceptable status
        if ERROR_NOT_FOUND == status:
            return None, True

        # We actually failed.
        raise ctypes.WinError()

    def get_property_name(self, event_info):
        """Get the name for a property.

        :param trace_event_info: TRACE_EVENT_INFO
        :return: (str)
        """
        name_field = rel_ptr_to_str(
            pointer(event_info),
            self.NameOffset
        )
        return name_field

    def get_property_data(self, event_record, event_info):
        if self.Flags & PropertyStruct:
            LOGGER.info(
                "EVENT_PROPERTY_INFO. Flag of type PropertyStruct is not yet supported."
            )
        else:
            # The format of the property data
            in_type = self.epi_u1.nonStructType.InType

            # Create PROPERTY_DATA_DESCRIPTOR
            data_descriptor = PROPERTY_DATA_DESCRIPTOR()

            data_descriptor.PropertyName = (
                    ctypes.cast(pointer(event_info), ctypes.c_voidp).value +
                    self.NameOffset
            )
            data_descriptor.ArrayIndex = MAX_UINT

            property_data_length = DWORD()

            status = tdh.TdhGetPropertySize(
                pointer(event_record),
                0,
                None,
                1,
                ctypes.byref(data_descriptor),
                ctypes.byref(property_data_length)
            )
            if status != ERROR_SUCCESS:
                raise WindowsError(
                    status, ctypes.FormatError(status)
                )

            if property_data_length.value == 0:
                return None

            property_buffer = ctypes.cast(
                (ctypes.c_byte * property_data_length.value)(),
                ctypes.POINTER(ctypes.c_byte)
            )

            status = tdh.TdhGetProperty(
                pointer(event_record),
                0,
                None,
                1,
                ctypes.byref(data_descriptor),
                property_data_length.value,
                property_buffer
            )

            if status != ERROR_SUCCESS:
                raise WindowsError(
                    status, ctypes.FormatError(status)
                )

            return get_formatted_value(
                in_type,
                property_buffer
            )

    def get_property_length(self, event_record, event_info):
        data_descriptor = PROPERTY_DATA_DESCRIPTOR()
        length = DWORD()

        data_descriptor.PropertyName = (
                ctypes.cast(event_info, ctypes.c_voidp).value +
                self.NameOffset
        )
        data_descriptor.ArrayIndex = MAX_UINT

        status = tdh.TdhGetPropertySize(
            event_record,
            0,
            None,
            1,
            ctypes.byref(data_descriptor),
            ctypes.byref(length)
        )
        if status != ERROR_SUCCESS:
            raise ctypes.WinError(status)

        return length.value


class TRACE_EVENT_INFO(Structure):
    _fields_ = [
        ('ProviderGuid', GUID),
        ('EventGuid', GUID),
        ('EventDescriptor', EVENT_DESCRIPTOR),
        ('DecodingSource', DECODING_SOURCE),
        ('ProviderNameOffset', ULONG),
        ('LevelNameOffset', ULONG),
        ('ChannelNameOffset', ULONG),
        ('KeywordsNameOffset', ULONG),
        ('TaskNameOffset', ULONG),
        ('OpcodeNameOffset', ULONG),
        ('EventMessageOffset', ULONG),
        ('ProviderMessageOffset', ULONG),
        ('BinaryXMLOffset', ULONG),
        ('BinaryXMLSize', ULONG),
        ('ActivityIDNameOffset', ULONG),
        ('RelatedActivityIDNameOffset', ULONG),
        ('PropertyCount', ULONG),
        ('TopLevelPropertyCount', ULONG),
        ('Flags', ULONG),
        ('EventPropertyInfoArray', EVENT_PROPERTY_INFO * 0)
    ]

    @property
    def ProviderName(self):
        if self.ProviderNameOffset > 0:
            return rel_ptr_to_str(
                pointer(self),
                self.ProviderNameOffset
            )
        return ""

    @property
    def LevelName(self):
        if self.LevelNameOffset > 0:
            return rel_ptr_to_str(
                pointer(self),
                self.LevelNameOffset
            )
        return ""

    @property
    def ChannelName(self):
        if self.ChannelNameOffset > 0:
            return rel_ptr_to_str(
                pointer(self),
                self.ChannelNameOffset
            )
        return ""

    @property
    def KeywordsName(self):
        if self.KeywordsNameOffset > 0:
            return rel_ptr_to_str(
                pointer(self),
                self.KeywordsNameOffset
            )
        return ""

    @property
    def TaskName(self):
        if self.TaskNameOffset > 0:
            return rel_ptr_to_str(
                pointer(self),
                self.TaskNameOffset
            )
        return ""

    @property
    def OpcodeName(self):
        if self.OpcodeNameOffset > 0:
            return rel_ptr_to_str(
                pointer(self),
                self.OpcodeNameOffset
            )
        return ""

    @property
    def EventMessage(self):
        if self.EventMessageOffset > 0:
            return rel_ptr_to_str(
                pointer(self),
                self.EventMessageOffset
            )
        return ""

    @property
    def ProviderMessage(self):
        if self.ProviderMessageOffset > 0:
            return rel_ptr_to_str(
                pointer(self),
                self.ProviderMessageOffset
            )
        return ""

    def iter_properties(self):
        property_array = ctypes.cast(
            self.EventPropertyInfoArray,
            ctypes.POINTER(EVENT_PROPERTY_INFO)
        )

        for i in range(self.TopLevelPropertyCount):
            event_property_info = property_array[i]
            yield event_property_info

    def as_dict(self):
        return {
            "ProviderGuid": str(self.ProviderGuid),
            "EventGuid": str(self.EventGuid),
            "ProviderName": self.ProviderName,
            "LevelName": self.LevelName,
            "ChannelName": self.ChannelName,
            "KeywordsName": self.KeywordsName,
            "TaskName": self.TaskName,
            "OpcodeName": self.OpcodeName,
            "EventMessage": self.EventMessage,
            "ProviderMessage": self.ProviderMessage,
        }


class TDH_CONTEXT(Structure):
    _fields_ = [
        ('ParameterValue', ULONGLONG),
        ('ParameterType', TDH_CONTEXT_TYPE),
        ('ParameterSize', ULONG)
    ]


class EVENT_MAP_ENTRY(Structure):
    _fields_ = [
        ('OutputOffset', ULONG),
        ('InputOffset', ULONG)
    ]


class EVENT_MAP_INFO(Structure):
    _fields_ = [
        ('NameOffset', ULONG),
        ('Flag', MAP_FLAGS),
        ('EntryCount', ULONG),
        ('FormatStringOffset', ULONG),
        ('MapEntryArray', EVENT_MAP_ENTRY * 0)
    ]


class PROPERTY_DATA_DESCRIPTOR(Structure):
    _fields_ = [
        ('PropertyName', ULONGLONG),
        ('ArrayIndex', ULONG),
        ('Reserved', ULONG)
    ]


class IN6_ADDR(Structure):
    _fields_ = [('Byte', c_byte * 16)]


# https://docs.microsoft.com/en-us/windows/desktop/api/winevt/ns-winevt-_evt_variant
class EVT_VARIANT_UNION(Union):
    _fields_ = [
        ("BooleanVal", BOOL),
        ("SByteVal", INT8),
        ("Int16Val", INT16),
        ("Int32Val", INT32),
        ("Int64Val", INT64),
        ("ByteVal", UINT8),
        ("UInt16Val", UINT16),
        ("UInt32Val", UINT32),
        ("UInt64Val", UINT64),
        ("SingleVal", FLOAT),
        ("DoubleVal", DOUBLE),
        ("FileTimeVal", ULONGLONG),
        ("SysTimeVal", POINTER(SYSTEMTIME)),
        ("GuidVal", POINTER(GUID)),
        ("StringVal", LPCWSTR),
        ("AnsiStringVal", LPCSTR),
        ("BinaryVal", PBYTE),
        ("SidVal", PSID),
        ("SizeTVal", SIZE_T),
        ("EvtHandleVal", EVT_HANDLE),
        ("BooleanArr", POINTER(BOOL)),
        ("SByteArr", POINTER(INT8)),
        ("Int16Arr", POINTER(INT16)),
        ("Int32Arr", POINTER(INT32)),
        ("Int64Arr", POINTER(INT64)),
        ("ByteArr", POINTER(UINT8)),
        ("UInt16Arr", POINTER(UINT16)),
        ("UInt32Arr", POINTER(UINT32)),
        ("UInt64Arr", POINTER(UINT64)),
        ("SingleArr", POINTER(FLOAT)),
        ("DoubleArr", POINTER(DOUBLE)),
        ("FileTimeArr", POINTER(FILETIME)),
        ("SysTimeArr", POINTER(SYSTEMTIME)),
        ("GuidArr", POINTER(GUID)),
        ("StringArr", POINTER(LPWSTR)),
        ("AnsiStringArr", POINTER(LPSTR)),
        ("SidArr", POINTER(PSID)),
        ("SizeTArr", POINTER(SIZE_T)),
        ("XmlVal", LPCWSTR),
        ("XmlValArr", POINTER(LPCWSTR)),
]
class EVT_VARIANT(Structure):
    _fields_ = [
        ("_VARIANT_VALUE", EVT_VARIANT_UNION),
        ("Count", DWORD),
        ("Type", DWORD),
]
PEVT_VARIANT = POINTER(EVT_VARIANT)

# Because the following packages rely on winstructs, we import them at the end
from winthingies.win32.tdh import tdh
