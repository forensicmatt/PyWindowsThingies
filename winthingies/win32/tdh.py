import ctypes
import logging
from ctypes.wintypes import *
from winthingies.win32.const import *
from winthingies.win32.winstructs import *
from winthingies.win32.helpers import get_formatted_value

LOGGER = logging.getLogger(__name__)
tdh = ctypes.WinDLL('Tdh', use_last_error=True)


def format_property(in_type, raw_buffer):
    if in_type == TDH_INTYPE_UNICODESTRING:
        return bytes(raw_buffer).decode("utf16")
    return bytes(raw_buffer)


TdhGetEventInformation = tdh.TdhGetEventInformation
TdhGetEventInformation.argtypes = [
    ctypes.POINTER(EVENT_RECORD),
    ULONG,
    ctypes.POINTER(TDH_CONTEXT),
    ctypes.POINTER(TRACE_EVENT_INFO),
    ctypes.POINTER(ULONG)
]
TdhGetEventInformation.restype = ULONG


TdhFormatProperty = tdh.TdhFormatProperty
TdhFormatProperty.argtypes = [
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
TdhFormatProperty.restype = ULONG


TdhGetEventMapInformation = tdh.TdhGetEventMapInformation
TdhGetEventMapInformation.argtypes = [
    ctypes.POINTER(EVENT_RECORD),
    LPWSTR,
    ctypes.POINTER(EVENT_MAP_INFO),
    ctypes.POINTER(ULONG)
]
TdhGetEventMapInformation.restype = ULONG


TdhGetPropertySize = tdh.TdhGetPropertySize
TdhGetPropertySize.argtypes = [
    ctypes.POINTER(EVENT_RECORD),
    ULONG,
    ctypes.POINTER(TDH_CONTEXT),
    ULONG,
    ctypes.POINTER(PROPERTY_DATA_DESCRIPTOR),
    ctypes.POINTER(ULONG)
]
TdhGetPropertySize.restype = ULONG


TdhGetProperty = tdh.TdhGetProperty
TdhGetProperty.argtypes = [
    ctypes.POINTER(EVENT_RECORD),
    ULONG,
    ctypes.POINTER(TDH_CONTEXT),
    ULONG,
    ctypes.POINTER(PROPERTY_DATA_DESCRIPTOR),
    ULONG,
    ctypes.POINTER(ctypes.c_byte)
]
TdhGetProperty.restype = ULONG


def get_event_information(self):
    trace_event_info = ctypes.POINTER(
        TRACE_EVENT_INFO
    )()
    buffer_size = DWORD()

    # Call TdhGetEventInformation once to get the required buffer size and again to actually populate the structure.
    status = TdhGetEventInformation(
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
        status = TdhGetEventInformation(
            self,
            0,
            None,
            trace_event_info,
            ctypes.byref(buffer_size)
        )

    if ERROR_SUCCESS != status:
        raise ctypes.WinError(status)

    return trace_event_info


EVENT_RECORD.get_event_information = get_event_information


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
        event_info,
        self.epi_u1.nonStructType.MapNameOffset
    )
    map_size = DWORD()
    map_info = ctypes.POINTER(EVENT_MAP_INFO)()

    status = TdhGetEventMapInformation(
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
        status = TdhGetEventMapInformation(
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
        event_info,
        self.NameOffset
    )
    return name_field


def get_property_data(self, event_record, event_info):
    if self.Flags & PropertyStruct:
        LOGGER.info(
            "EVENT_PROPERTY_INFO.Flag of type PropertyStruct is not yet supported."
        )
    else:
        # The format of the property data
        in_type = self.epi_u1.nonStructType.InType

        # Create PROPERTY_DATA_DESCRIPTOR
        data_descriptor = PROPERTY_DATA_DESCRIPTOR()

        data_descriptor.PropertyName = (
                ctypes.cast(event_info, ctypes.c_voidp).value +
                self.NameOffset
        )
        data_descriptor.ArrayIndex = MAX_UINT

        property_data_length = DWORD()

        status = TdhGetPropertySize(
            event_record,
            0,
            None,
            1,
            ctypes.byref(data_descriptor),
            ctypes.byref(property_data_length)
        )
        if status != ERROR_SUCCESS:
            raise ctypes.WinError(status)

        property_buffer = ctypes.cast(
            (ctypes.c_byte * property_data_length.value)(),
            ctypes.POINTER(ctypes.c_byte)
        )

        status = tdh.TdhGetProperty(
            event_record,
            0,
            None,
            1,
            data_descriptor,
            property_data_length.value,
            property_buffer
        )

        if status != ERROR_SUCCESS:
            raise ctypes.WinError(status)

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

    status = TdhGetPropertySize(
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


EVENT_PROPERTY_INFO.get_event_map_info = get_event_map_info
EVENT_PROPERTY_INFO.get_property_name = get_property_name
EVENT_PROPERTY_INFO.get_property_length = get_property_length
EVENT_PROPERTY_INFO.get_property_data = get_property_data
