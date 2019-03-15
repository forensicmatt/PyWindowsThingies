import ctypes
from ctypes.wintypes import *
from winthingies.win32.const import *
from winthingies.win32.winstructs import *
from winthingies.win32.kernel32 import kernel32

wevtapi = ctypes.WinDLL('wevtapi', use_last_error=True)


wevtapi.EvtClose.restype = BOOL
wevtapi.EvtClose.argtypes = [
    EVT_HANDLE
]


# Gets a handle that you use to read the specified provider's metadata.
# https://docs.microsoft.com/en-us/windows/desktop/api/WinEvt/nf-winevt-evtopenpublishermetadata
# https://docs.microsoft.com/en-us/windows/desktop/WES/getting-a-provider-s-metadata-
wevtapi.EvtOpenPublisherMetadata.restype = EVT_HANDLE
wevtapi.EvtOpenPublisherMetadata.argtypes = [
    EVT_HANDLE,
    LPCWSTR,
    LPCWSTR,
    LCID,
    DWORD
]
def EvtOpenPublisherMetadata(publisher_id):
    """A helper function to make calling EvtOpenPublisherMetadata easier.

    :param publisher_id: (str) The name of the provider
    :return: (EVT_HANDLE)
    """
    evt_handle = wevtapi.EvtOpenPublisherMetadata(
        None,
        publisher_id,
        None,
        0,
        0
    )
    return evt_handle


#  Gets a handle that you use to enumerate the list of events that the provider defines.
wevtapi.EvtOpenEventMetadataEnum.restype = EVT_HANDLE
wevtapi.EvtOpenEventMetadataEnum.argtypes = [
    EVT_HANDLE, # PublisherMetadata
    DWORD       # Flags
]

# Gets an event definition from the enumerator.
wevtapi.EvtNextEventMetadata.restype = EVT_HANDLE
wevtapi.EvtNextEventMetadata.argtypes = [
    EVT_HANDLE, # EventMetadataEnum
    DWORD       # Flags
]


EVT_EVENT_METADATA_PROPERTY_ID = DWORD
wevtapi.EvtGetEventMetadataProperty.restype = BOOL
wevtapi.EvtGetEventMetadataProperty.argtypes = [
    EVT_HANDLE,
    EVT_EVENT_METADATA_PROPERTY_ID,
    DWORD,
    DWORD,
    PEVT_VARIANT,
    PDWORD
]


# Gets the number of elements in the array of objects.
# https://docs.microsoft.com/en-us/windows/desktop/api/winevt/nf-winevt-evtgetobjectarraysize
wevtapi.EvtGetObjectArraySize.restype = BOOL
wevtapi.EvtGetObjectArraySize.argtypes = [
    EVT_OBJECT_ARRAY_PROPERTY_HANDLE,
    PDWORD
]


# Gets a provider metadata property from the specified object in the array.
# https://docs.microsoft.com/en-us/windows/desktop/api/WinEvt/nf-winevt-evtgetobjectarrayproperty
wevtapi.EvtGetObjectArrayProperty.restype = BOOL
wevtapi.EvtGetObjectArrayProperty.argtypes = [
    EVT_OBJECT_ARRAY_PROPERTY_HANDLE,
    DWORD,
    DWORD,
    DWORD,
    DWORD,
    PEVT_VARIANT,
    PDWORD
]


wevtapi.EvtFormatMessage.restype = BOOL
wevtapi.EvtFormatMessage.argtypes = [
    EVT_HANDLE,
    EVT_HANDLE,
    DWORD,
    DWORD,
    PEVT_VARIANT,
    DWORD,
    DWORD,
    LPWSTR,
    PDWORD
]


# https://docs.microsoft.com/en-us/windows/desktop/api/winevt/ne-winevt-_evt_publisher_metadata_property_id
EVT_PUBLISHER_METADATA_PROPERTY_ID = DWORD
wevtapi.EvtGetPublisherMetadataProperty.restype = BOOL
wevtapi.EvtGetPublisherMetadataProperty.argtypes = [
    EVT_HANDLE,
    EVT_PUBLISHER_METADATA_PROPERTY_ID,
    DWORD,
    DWORD,
    PEVT_VARIANT,
    PDWORD
]
def EvtGetPublisherMetadataProperty(metadata_handle, property_id):
    """A helper function to make calling EvtGetPublisherMetadataProperty easier.

    :param metadata_handle: (EVT_HANDLE) This is a handled returned by EvtOpenPublisherMetadata
    :param property_id: (EVT_PUBLISHER_METADATA_PROPERTY_ID) EvtPublisherMetadata* ENUM value
    :return: (EVT_VARIANT)
    """
    buffer_size = 0
    variant = None
    buffer_used = byref(DWORD())

    result = wevtapi.EvtGetPublisherMetadataProperty(
        metadata_handle,
        property_id,
        0,
        buffer_size,
        variant,
        buffer_used
    )
    if result == 0:
        # Check our last error
        status = kernel32.GetLastError()

        if status == ERROR_INSUFFICIENT_BUFFER:
            # If the error is ERROR_INSUFFICIENT_BUFFER,
            # we can now determine the buffer size needed.
            buffer_size = buffer_used._obj.value
            variant_buffer = ctypes.create_string_buffer(
                buffer_size
            )
            variant = EVT_VARIANT.from_buffer(
                variant_buffer
            )

            result = wevtapi.EvtGetPublisherMetadataProperty(
                metadata_handle,
                property_id,
                0,
                buffer_size,
                variant,
                buffer_used
            )

            return variant
        else:
            raise(
                Exception(
                    "Unhandled error on EvtGetObjectArrayProperty. Error: {}".format(
                        status
                    )
                )
            )
