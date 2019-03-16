from winthingies.win32.const import *
from winthingies.win32.wevtapi import *
from winthingies.win32.kernel32 import kernel32


class PublisherMetadata(object):
    def __init__(self, publisher_name):
        self.publisher_name = publisher_name
        self._handle = None
        self._handle = EvtOpenPublisherMetadata(
            self.publisher_name
        )

    @property
    def keyword_mapping(self):
        return get_keyword_mapping(
            self._handle
        )

    @property
    def guid(self):
        variant = EvtGetPublisherMetadataProperty(
            self._handle,
            EvtPublisherMetadataPublisherGuid
        )

        if variant:
            guid = variant._VARIANT_VALUE.GuidVal
            return str(guid.contents)

    def as_json(self):
        info = {
            "guid": self.guid,
            "keywords": self.keyword_mapping
        }
        return info

    def __del__(self):
        if self._handle is not None:
            wevtapi.EvtClose(
                self._handle
            )


def get_keyword_mapping(metadata_handle):
    """Get a dictionary of keyword info.

    :param metadata_handle: (EVT_HANDLE) The handle returned by EvtOpenPublisherMetadata
    :return: {
        UInt64Val: "StringVal"
    }
    """
    keyword_map = {}
    meta_prop_variant = EvtGetPublisherMetadataProperty(
        metadata_handle,
        EvtPublisherMetadataKeywords
    )

    if meta_prop_variant is None:
        return

    array_handle = meta_prop_variant._VARIANT_VALUE.EvtHandleVal
    array_size = byref(DWORD())

    wevtapi.EvtGetObjectArraySize(
        array_handle,
        array_size
    )

    if array_size._obj.value > 0:
        for index in range(array_size._obj.value):
            info = {}

            name_property = get_property(
                array_handle,
                index,
                EvtPublisherMetadataKeywordName
            )
            info['name'] = name_property._VARIANT_VALUE.StringVal

            desc_property = get_property(
                array_handle,
                index,
                EvtPublisherMetadataKeywordMessageID
            )
            info['desc'] = ""
            message_id = desc_property._VARIANT_VALUE.Int32Val
            if message_id != -1:
                # We have a description
                message_str = get_message(
                    metadata_handle,
                    message_id
                )
                if message_str:
                    info['desc'] = message_str

            mask_property = get_property(
                array_handle,
                index,
                EvtPublisherMetadataKeywordValue
            )
            info['mask'] = mask_property._VARIANT_VALUE.UInt64Val

            keyword_map[info['mask']] = info

    wevtapi.EvtClose(
        array_handle
    )

    return keyword_map


def get_message(metadata_handle, message_id):
    """Get a message given the message id.

    :param metadata_handle: (EVT_HANDLE)
    :param message_id: (DWORD)
    :return:
    """
    buffer_size = 0
    variant = None
    buffer_used = byref(DWORD())

    result = wevtapi.EvtFormatMessage(
        metadata_handle,
        None,
        message_id,
        0,
        None,
        EvtFormatMessageId,
        buffer_size,
        variant,
        buffer_used
    )

    if result == 0:
        # Check our last error
        status = kernel32.GetLastError()

        if status == ERROR_INSUFFICIENT_BUFFER:
            buffer_size = buffer_used._obj.value
            c_buffer = ctypes.c_buffer(buffer_size*2)
            unicode_buffer = ctypes.cast(c_buffer, LPWSTR)

            result = wevtapi.EvtFormatMessage(
                metadata_handle,
                None,
                message_id,
                0,
                None,
                EvtFormatMessageId,
                buffer_size,
                unicode_buffer,
                buffer_used
            )

            return unicode_buffer.value
        else:
            raise (
                Exception(
                    "Unhandled error on EvtFormatMessage. Error: {}".format(
                        status
                    )
                )
            )


def get_property(evt_handle, index, property_id):
    """Get the metadata property for an object in the array.

    :param evt_handle: (EVT_HANDLE)
    :param index: (DWORD)
    :param property_id: (EVT_PUBLISHER_METADATA_PROPERTY_ID)
    :return:
    """
    # The first thing we need to do is find out how large our variant buffer will be
    # to do this, we set our variant to Null, the result will be 0, and set an error.
    buffer_size = 0
    variant = None
    buffer_used = byref(DWORD())
    result = wevtapi.EvtGetObjectArrayProperty(
        evt_handle,
        property_id,
        index,
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
            result = wevtapi.EvtGetObjectArrayProperty(
                evt_handle,
                property_id,
                index,
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
