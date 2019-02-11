import re
import ujson
import ctypes
import threading
from winthingies.win32.const import *
from winthingies.win32.winstructs import *
from winthingies.win32 import advapi32
from winthingies.win32 import tdh

KERNEL_TRACE_CONTROL_GUID = GUID.from_string(
    '{9e814aad-3204-11d2-9a82-006008a86939}'
)
KERNEL_LOGGER_NAME = u"NT Kernel Logger"
WNODE_FLAG_TRACED_GUID = 0x00020000
INVALID_PROCESSTRACE_HANDLE = TRACEHANDLE(-1)
DEFAULT_NT_KERNEL_LOGGER_FLAGS = (
    EVENT_TRACE_FLAG_REGISTRY |
    EVENT_TRACE_FLAG_DISK_IO
)


class TraceConsumer(threading.Thread):
    def __init__(self, logger_name, callback):
        self._event_trace_logfile = EVENT_TRACE_LOGFILE()
        self._trace_handle = None
        self._callback = callback

        # Set EVENT_TRACE_LOGFILE attributes
        self._event_trace_logfile.ProcessTraceMode = (
                PROCESS_TRACE_MODE_REAL_TIME |
                PROCESS_TRACE_MODE_EVENT_RECORD
        )
        self._event_trace_logfile.LoggerName = logger_name
        self._event_trace_logfile.EventRecordCallback = EVENT_RECORD_CALLBACK(
            self._event_callback
        )

        # Flag for stopping
        self._stop_flag = threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        self._trace_handle = advapi32.OpenTraceW(
            ctypes.byref(self._event_trace_logfile)
        )
        self._trace_handle = TRACEHANDLE(
            self._trace_handle
        )

        if self._trace_handle == INVALID_PROCESSTRACE_HANDLE:
            raise ctypes.WinError()

        while not self._stop_flag.is_set():
            status = advapi32.ProcessTrace(
                ctypes.byref(self._trace_handle),
                1,
                None,
                None
            )

            if status != ERROR_SUCCESS:
                raise ctypes.WinError()

    def stop(self):
        self._stop_flag.set()

        advapi32.CloseTrace(
            self._trace_handle
        )

    def _event_callback(self, event_record):
        """This function gets called for events.

        :param event:
        :return:
        """
        event_information = event_record.contents.get_event_information()

        # event_data = b''.join(
        #     [ctypes.cast(event_record.contents.UserData + i, PBYTE).contents
        #       for i in range(event_record.contents.UserDataLength)]
        # )

        this = event_record.contents.EventHeader.as_dict()
        for event_property_info in event_information.contents.iter_properties():
            name = event_property_info.get_property_name(
                event_information
            )

            try:
                data = event_property_info.get_property_data(
                    event_record,
                    event_information
                )
            except:
                data = None

            this[name] = data

        if self._callback:
            self._callback(this)
        else:
            print(ujson.dumps(this))


class TraceProperties(object):
    """Wrapper for EVENT_TRACE_PROPERTIES
    https://docs.microsoft.com/en-us/windows/desktop/etw/event-trace-properties

    You cannot start more than one session with the same session GUID.
    """
    def __init__(self, buffer_size=1024):
        """The tracing properties.

        :param buffer_size: (int) the amount of memory allocated for each trace buffer
        """
        self.max_string_len = 1024
        self.buff_size = sizeof(EVENT_TRACE_PROPERTIES) + 2 * \
                         sizeof(c_wchar) * self.max_string_len

        self._buff = (c_char * self.buff_size)()
        self._props = cast(
            pointer(self._buff),
            POINTER(EVENT_TRACE_PROPERTIES)
        )
        self._props.contents.BufferSize = buffer_size
        self._props.contents.LoggerNameOffset = sizeof(EVENT_TRACE_PROPERTIES)
        self._props.contents.LogFileNameOffset = 0
        self._props.contents.LogFileMode = EVENT_TRACE_REAL_TIME_MODE

        self._props.contents.Wnode.BufferSize = self.buff_size
        self._props.contents.Wnode.Flags = WNODE_FLAG_TRACED_GUID

    def get_trace_properties(self):
        return self._props


class TraceProvider(object):
    """https://docs.microsoft.com/en-us/windows/desktop/etw/about-event-tracing#providers
    This class represents a single trace provider (source of trace events).
    """
    def __init__(
            self, name, guid, level=TRACE_LEVEL_INFORMATION,
            match_any_keyword=0, match_all_keyword=0,
            enable_parameters=None
    ):
        """These values get passed into EnableTraceEx2 to start this provider.

        :param name:  (str) The name of the provider
        :param guid: (str) The guid of the provider name
        :param level: (UCHAR) A provider-defined value that specifies the level of detail included in the event
        :param match_any_keyword: (ULONGLONG)
        :param match_all_keyword: (ULONGLONG)
        """
        self.name = name
        self.guid = GUID.from_string(
            guid
        )
        self.level = level
        self.match_any_keyword = match_any_keyword
        self.match_all_keyword = match_all_keyword
        self.enable_parameters = enable_parameters


class TraceSession(object):
    """A trace session can have multiple trace providers that it can register.
    The TraceSession is in charge of handling the providers under a single session.

    https://docs.microsoft.com/en-us/windows/desktop/etw/about-event-tracing#providers

    Creating/Starting providers allows a consumer to ingest events.
    """
    def __init__(self, session_name, providers):
        """

        :param session_name: (str) The session name.
        :param providers: (list<TraceProvider>) List of providers to start.
        """
        self._session_name = session_name
        self._providers = providers

        if len(self._providers) < 1:
            raise Exception(
                "At least 1 provider is needed for a trace session."
            )

        # Flag for kernel trace
        self._is_kernel_trace = False

        # The trace session properties
        self._properties = TraceProperties()

        # The trace session handle
        self._session_handle = TRACEHANDLE()

        if self._session_name == KERNEL_LOGGER_NAME:
            if len(self._providers) > 1:
                raise Exception(
                    "A Kernel Logger can only have 1 provider!"
                )

            self._is_kernel_trace = True
            self._properties._props.contents.Wnode.Guid = self._providers[0].guid
            self._properties._props.contents.LogFileMode |= EVENT_TRACE_SYSTEM_LOGGER_MODE

            if self._providers[0].match_any_keyword is not None:
                self._properties._props.contents.EnableFlags = self._providers[0].match_any_keyword
            else:
                self._properties._props.contents.EnableFlags = DEFAULT_NT_KERNEL_LOGGER_FLAGS

    def __del__(self):
        if self._session_handle:
            self.stop()

    def start(self):
        """Starts the Trace Provider.
        """
        # Create new session handle
        session_handle = TRACEHANDLE()

        # Get session properties
        trace_properties = self._properties.get_trace_properties()

        # Start trace
        status = advapi32.StartTrace(
            byref(session_handle),
            self._session_name,
            trace_properties
        )

        # Set current session to new session handle
        self._session_handle = session_handle

        # Check status
        if status == ERROR_ALREADY_EXISTS:
            self.stop()

            status = advapi32.StartTrace(
                byref(session_handle),
                self._session_name,
                trace_properties
            )
            if status != ERROR_SUCCESS:
                raise(
                    Exception('Unable to start event trace')
                )

            self._session_handle = session_handle
        elif status == ERROR_ACCESS_DENIED:
            raise(
                Exception("Access Denied")
            )
        elif status == ERROR_BAD_LENGTH:
            raise(
                Exception('Incorrect buffer size for the trace buffer')
            )
        elif status == ERROR_INVALID_PARAMETER:
            raise(
                Exception('Invalid trace parameter')
            )
        elif status != ERROR_SUCCESS:
            raise(
                Exception('Unable to start event trace')
            )

        if not self._is_kernel_trace:
            # If the trace session is not a Kernel level we can use multiple providers
            self._start_providers()

    def _start_providers(self):
        """A non-kernel level trace session can have multiple providers.
        This functions iterates through this session's providers and enables
        them.

        :return: (None)
        """
        for provider in self._providers:
            if provider.enable_parameters:
                raise Exception(
                    "Provider enable_parameters are not yet implemented."
                )

            status = advapi32.EnableTraceEx2(
                self._session_handle,
                ctypes.byref(provider.guid),
                EVENT_CONTROL_CODE_ENABLE_PROVIDER,
                provider.level,
                provider.match_any_keyword,
                provider.match_all_keyword,
                0,
                provider.enable_parameters
            )

            if status != ERROR_SUCCESS:
                raise ctypes.WinError(
                    status
                )

    def stop(self):
        """Stops the Trace Provider.
        """
        # Get trace properties
        trace_properties = self._properties.get_trace_properties()

        # Get current session handle
        current_session_handle = self._session_handle

        # Set session handle to an empty session
        self._session_handle = TRACEHANDLE()

        # Stop current session handle
        status = advapi32.ControlTrace(
            current_session_handle,
            self._session_name,
            trace_properties,
            EVENT_TRACE_CONTROL_STOP
        )

        if status != ERROR_SUCCESS:
            raise Exception(
                'Unable to stop trace {}. [return value: {}]'.format(
                    self._session_name,
                    status
                )
            )


class EventTraceHandler(object):
    def __init__(self):
        pass
