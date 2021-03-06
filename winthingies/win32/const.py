import win32con

MAX_UINT = (2 ** 32) - 1

SystemExtendedHandleInformation = 64

ERROR_SUCCESS = 0x00
ERROR_ACCESS_DENIED = 0x05
ERROR_BAD_LENGTH = 0x18
ERROR_INVALID_PARAMETER = 0x57
ERROR_ALREADY_EXISTS = 0xB7
ERROR_INSUFFICIENT_BUFFER = 0x7A
ERROR_NOT_FOUND = 0x490
ERROR_EVT_INVALID_EVENT_DATA = 0x3A9D
ERROR_NO_MORE_ITEMS = 0x103

EVENT_TRACE_CONTROL_QUERY = 0
EVENT_TRACE_CONTROL_STOP = 1
EVENT_TRACE_CONTROL_UPDATE = 2

TH32CS_SNAPHEAPLIST = 0x00000001
TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPTHREAD = 0x00000004
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010
TH32CS_SNAPALL = TH32CS_SNAPHEAPLIST | TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD | TH32CS_SNAPMODULE
TH32CS_INHERIT = 0x80000000

STATUS_INFO_LENGTH_MISMATCH = 0xC0000004
STATUS_BUFFER_OVERFLOW = 0x80000005
STATUS_INVALID_HANDLE = 0xC0000008
STATUS_BUFFER_TOO_SMALL = 0xC0000023
STATUS_SUCCESS = 0

PROCESS_TERMINATE = 0x0001
PROCESS_CREATE_THREAD = 0x0002
PROCESS_SET_SESSIONID = 0x0004
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_DUP_HANDLE = 0x0040
PROCESS_CREATE_PROCESS = 0x0080
PROCESS_SET_QUOTA = 0x0100
PROCESS_SET_INFORMATION = 0x0200
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_SUSPEND_RESUME = 0x0800
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_SET_LIMITED_INFORMATION = 0x2000
PROCESS_ALL_ACCESS = win32con.PROCESS_ALL_ACCESS

DUPLICATE_CLOSE_SOURCE = 0x00000001
DUPLICATE_SAME_ACCESS = 0x00000002

# Logger Mode flags
# https://docs.microsoft.com/en-us/windows/desktop/etw/logging-mode-constants
# https://github.com/fireeye/pywintrace/blob/master/etw/evntrace.py
EVENT_TRACE_FILE_MODE_NONE = 0x00000000  # Logfile is off
EVENT_TRACE_FILE_MODE_SEQUENTIAL = 0x00000001  # Log sequentially
EVENT_TRACE_FILE_MODE_CIRCULAR = 0x00000002  # Log in circular manner
EVENT_TRACE_FILE_MODE_APPEND = 0x00000004  # Append sequential log
EVENT_TRACE_REAL_TIME_MODE = 0x00000100  # Real time mode on
EVENT_TRACE_DELAY_OPEN_FILE_MODE = 0x00000200  # Delay opening file
EVENT_TRACE_BUFFERING_MODE = 0x00000400  # Buffering mode only
EVENT_TRACE_PRIVATE_LOGGER_MODE = 0x00000800  # Process Private Logger
EVENT_TRACE_ADD_HEADER_MODE = 0x00001000  # Add a logfile header
EVENT_TRACE_USE_GLOBAL_SEQUENCE = 0x00004000  # Use global sequence no.
EVENT_TRACE_USE_LOCAL_SEQUENCE = 0x00008000  # Use local sequence no.
EVENT_TRACE_RELOG_MODE = 0x00010000  # Relogger
EVENT_TRACE_USE_PAGED_MEMORY = 0x01000000  # Use pageable buffers
# Logger Mode flags on XP and above
EVENT_TRACE_FILE_MODE_NEWFILE = 0x00000008  # Auto-switch log file
EVENT_TRACE_FILE_MODE_PREALLOCATE = 0x00000020  # Pre-allocate mode
# Logger Mode flags on Vista and above
EVENT_TRACE_NONSTOPPABLE_MODE = 0x00000040  # Session cannot be stopped (Autologger only)
EVENT_TRACE_SECURE_MODE = 0x00000080  # Secure session
EVENT_TRACE_USE_KBYTES_FOR_SIZE = 0x00002000  # Use KBytes as file size unit
EVENT_TRACE_PRIVATE_IN_PROC = 0x00020000  # In process private logger
EVENT_TRACE_MODE_RESERVED = 0x00100000  # Reserved bit, used to signal Heap/Critsec tracing
# Logger Mode flags on Win7 and above
EVENT_TRACE_NO_PER_PROCESSOR_BUFFERING = 0x10000000  # Use this for low frequency sessions.
# Logger Mode flags on Win8 and above
EVENT_TRACE_SYSTEM_LOGGER_MODE = 0x02000000  # Receive events from SystemTraceProvider
EVENT_TRACE_ADDTO_TRIAGE_DUMP = 0x80000000  # Add ETW buffers to triage dumps
EVENT_TRACE_STOP_ON_HYBRID_SHUTDOWN = 0x00400000  # Stop on hybrid shutdown
EVENT_TRACE_PERSIST_ON_HYBRID_SHUTDOWN = 0x00800000  # Persist on hybrid shutdown
# Logger Mode flags on Blue and above
EVENT_TRACE_INDEPENDENT_SESSION_MODE = 0x08000000  # Independent logger session

EVENT_TRACE_FLAG_PROCESS = 0x00000001
EVENT_TRACE_FLAG_THREAD = 0x00000002
EVENT_TRACE_FLAG_IMAGE_LOAD = 0x00000004
EVENT_TRACE_FLAG_DISK_IO = 0x00000100
EVENT_TRACE_FLAG_DISK_FILE_IO = 0x00000200
EVENT_TRACE_FLAG_MEMORY_PAGE_FAULTS = 0x00001000
EVENT_TRACE_FLAG_MEMORY_HARD_FAULTS = 0x00002000
EVENT_TRACE_FLAG_NETWORK_TCPIP = 0x00010000
EVENT_TRACE_FLAG_REGISTRY = 0x00020000
EVENT_TRACE_FLAG_DBGPRINT = 0x00040000
EVENT_TRACE_FLAG_PROCESS_COUNTERS = 0x00000008
EVENT_TRACE_FLAG_CSWITCH = 0x00000010
EVENT_TRACE_FLAG_DPC = 0x00000020
EVENT_TRACE_FLAG_INTERRUPT = 0x00000040
EVENT_TRACE_FLAG_SYSTEMCALL = 0x00000080
EVENT_TRACE_FLAG_DISK_IO_INIT = 0x00000400
EVENT_TRACE_FLAG_ALPC = 0x00100000
EVENT_TRACE_FLAG_SPLIT_IO = 0x00200000
EVENT_TRACE_FLAG_DRIVER = 0x00800000
EVENT_TRACE_FLAG_PROFILE = 0x01000000
EVENT_TRACE_FLAG_FILE_IO = 0x02000000
EVENT_TRACE_FLAG_FILE_IO_INIT = 0x04000000
EVENT_TRACE_FLAG_DISPATCHER = 0x00000800
EVENT_TRACE_FLAG_VIRTUAL_ALLOC = 0x00004000

EVENT_TRACE_CONTROL_QUERY = 0
EVENT_TRACE_CONTROL_STOP = 1
EVENT_TRACE_CONTROL_UPDATE = 2

EVENT_CONTROL_CODE_DISABLE_PROVIDER = 0
EVENT_CONTROL_CODE_ENABLE_PROVIDER = 1
EVENT_CONTROL_CODE_CAPTURE_STATE = 2

PROCESS_TRACE_MODE_REAL_TIME = 0x00000100
PROCESS_TRACE_MODE_RAW_TIMESTAMP = 0x00001000
PROCESS_TRACE_MODE_EVENT_RECORD = 0x10000000

TRACE_LEVEL_NONE = 0
TRACE_LEVEL_CRITICAL = 1
TRACE_LEVEL_ERROR = 2
TRACE_LEVEL_WARNING = 3
TRACE_LEVEL_INFORMATION = 4
TRACE_LEVEL_VERBOSE = 5
TRACE_LEVEL_RESERVED6 = 6
TRACE_LEVEL_RESERVED7 = 7
TRACE_LEVEL_RESERVED8 = 8
TRACE_LEVEL_RESERVED9 = 9

# https://msdn.microsoft.com/de-de/vstudio/aa964745(v=vs.80)
DecodingSourceXMLFile = 0
DecodingSourceWbem = 1
DecodingSourceWPP = 2
DecodingSourceTlg = 3

# https://docs.microsoft.com/en-us/windows/desktop/api/tdh/ne-tdh-_property_flags
PropertyStruct = 0x1
PropertyParamLength = 0x2
PropertyParamCount = 0x4
PropertyWBEMXmlFragment = 0x8
PropertyParamFixedLength = 0x10
PropertyParamFixedCount = 0x20
PropertyHasTags = 0x40
PropertyHasCustomSchema = 0x80

EVENTMAP_INFO_FLAG_MANIFEST_VALUEMAP = 1
EVENTMAP_INFO_FLAG_MANIFEST_BITMAP = 2
EVENTMAP_INFO_FLAG_MANIFEST_PATTERNMAP = 4
EVENTMAP_INFO_FLAG_WBEM_VALUEMAP = 8
EVENTMAP_INFO_FLAG_WBEM_BITMAP = 16
EVENTMAP_INFO_FLAG_WBEM_FLAG = 32
EVENTMAP_INFO_FLAG_WBEM_NO_MAP = 64

TDH_INTYPE_NULL = 0
TDH_INTYPE_UNICODESTRING = 1
TDH_INTYPE_ANSISTRING = 2
TDH_INTYPE_INT8 = 3
TDH_INTYPE_UINT8 = 4
TDH_INTYPE_INT16 = 5
TDH_INTYPE_UINT16 = 6
TDH_INTYPE_INT32 = 7
TDH_INTYPE_UINT32 = 8
TDH_INTYPE_INT64 = 9
TDH_INTYPE_UINT64 = 10
TDH_INTYPE_FLOAT = 11
TDH_INTYPE_DOUBLE = 12
TDH_INTYPE_BOOLEAN = 13
TDH_INTYPE_BINARY = 14
TDH_INTYPE_GUID = 15
TDH_INTYPE_POINTER = 16
TDH_INTYPE_FILETIME = 17
TDH_INTYPE_SYSTEMTIME = 18
TDH_INTYPE_SID = 19
TDH_INTYPE_HEXINT32 = 20
TDH_INTYPE_HEXINT64 = 21
TDH_INTYPE_COUNTEDSTRING = 300
TDH_INTYPE_COUNTEDANSISTRING = 301
TDH_INTYPE_REVERSEDCOUNTEDSTRING = 302
TDH_INTYPE_REVERSEDCOUNTEDANSISTRING = 303
TDH_INTYPE_NONNULLTERMINATEDSTRING = 304
TDH_INTYPE_NONNULLTERMINATEDANSISTRING = 305
TDH_INTYPE_UNICODECHAR = 306
TDH_INTYPE_ANSICHAR = 307
TDH_INTYPE_SIZET = 308
TDH_INTYPE_HEXDUMP = 309
TDH_INTYPE_WBEMSID = 310

TDH_OUTTYPE_NULL = 0
TDH_OUTTYPE_STRING = 1
TDH_OUTTYPE_DATETIME = 2
TDH_OUTTYPE_BYTE = 3
TDH_OUTTYPE_UNSIGNEDBYTE = 4
TDH_OUTTYPE_SHORT = 5
TDH_OUTTYPE_UNSIGNEDSHORT = 6
TDH_OUTTYPE_INT = 7
TDH_OUTTYPE_UNSIGNEDINT = 8
TDH_OUTTYPE_LONG = 9
TDH_OUTTYPE_UNSIGNEDLONG = 10
TDH_OUTTYPE_FLOAT = 11
TDH_OUTTYPE_DOUBLE = 12
TDH_OUTTYPE_BOOLEAN = 13
TDH_OUTTYPE_GUID = 14
TDH_OUTTYPE_HEXBINARY = 15
TDH_OUTTYPE_HEXINT8 = 16
TDH_OUTTYPE_HEXINT16 = 17
TDH_OUTTYPE_HEXINT32 = 18
TDH_OUTTYPE_HEXINT64 = 19
TDH_OUTTYPE_PID = 20
TDH_OUTTYPE_TID = 21
TDH_OUTTYPE_PORT = 22
TDH_OUTTYPE_IPV4 = 23
TDH_OUTTYPE_IPV6 = 24
TDH_OUTTYPE_SOCKETADDRESS = 25
TDH_OUTTYPE_CIMDATETIME = 26
TDH_OUTTYPE_ETWTIME = 27
TDH_OUTTYPE_XML = 28
TDH_OUTTYPE_ERRORCODE = 29
TDH_OUTTYPE_WIN32ERROR = 30
TDH_OUTTYPE_NTSTATUS = 31
TDH_OUTTYPE_HRESULT = 32
TDH_OUTTYPE_CULTURE_INSENSITIVE_DATETIME = 33
TDH_OUTTYPE_JSON = 34
TDH_OUTTYPE_REDUCEDSTRING = 300
TDH_OUTTYPE_NOPRIN = 301

# https://docs.microsoft.com/en-us/windows/desktop/api/winevt/ne-winevt-_evt_publisher_metadata_property_id
EvtPublisherMetadataPublisherGuid = 0x0
EvtPublisherMetadataResourceFilePath = 0x1
EvtPublisherMetadataParameterFilePath = 0x2
EvtPublisherMetadataMessageFilePath = 0x3
EvtPublisherMetadataHelpLink = 0x4
EvtPublisherMetadataPublisherMessageID = 0x5
EvtPublisherMetadataChannelReferences = 0x6
EvtPublisherMetadataChannelReferencePath = 0x7
EvtPublisherMetadataChannelReferenceIndex = 0x8
EvtPublisherMetadataChannelReferenceID = 0x9
EvtPublisherMetadataChannelReferenceFlags = 0xa
EvtPublisherMetadataChannelReferenceMessageID = 0xb
EvtPublisherMetadataLevels = 0xc
EvtPublisherMetadataLevelName = 0xd
EvtPublisherMetadataLevelValue = 0xe
EvtPublisherMetadataLevelMessageID = 0xf
EvtPublisherMetadataTasks = 0x10
EvtPublisherMetadataTaskName = 0x11
EvtPublisherMetadataTaskEventGuid = 0x12
EvtPublisherMetadataTaskValue = 0x13
EvtPublisherMetadataTaskMessageID = 0x14
EvtPublisherMetadataOpcodes = 0x15
EvtPublisherMetadataOpcodeName = 0x16
EvtPublisherMetadataOpcodeValue = 0x17
EvtPublisherMetadataOpcodeMessageID = 0x18
EvtPublisherMetadataKeywords = 0x19
EvtPublisherMetadataKeywordName = 0x1a
EvtPublisherMetadataKeywordValue = 0x1b
EvtPublisherMetadataKeywordMessageID = 0x1c
EvtPublisherMetadataPropertyIdEND = 0x1d

# https://docs.microsoft.com/en-us/windows/desktop/api/winevt/ne-winevt-_evt_format_message_flags
EvtFormatMessageEvent = 0x1
EvtFormatMessageLevel = 0x2
EvtFormatMessageTask = 0x3
EvtFormatMessageOpcode = 0x4
EvtFormatMessageKeyword = 0x5
EvtFormatMessageChannel = 0x6
EvtFormatMessageProvider = 0x7
EvtFormatMessageId = 0x8
EvtFormatMessageXml = 0x9

