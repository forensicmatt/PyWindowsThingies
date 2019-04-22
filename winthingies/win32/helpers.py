import logging
from ctypes import *
from winthingies.win32.const import *

LOGGER = logging.getLogger(__name__)


def get_formatted_value(in_type, buffer):
    """Decode a buffer given the in type.

    :param in_type: (USHORT) The type of the buffer
    :param buffer: (bytes) The raw buffer
    :return: type depending on the in type
    """
    if in_type == TDH_INTYPE_UNICODESTRING:
        return wstring_at(buffer)
    elif in_type == TDH_INTYPE_ANSISTRING:
        return string_at(buffer)
    elif in_type == TDH_INTYPE_INT8:
        return cast(buffer, POINTER(c_int8)).contents.value
    elif in_type == TDH_INTYPE_UINT8:
        return cast(buffer, POINTER(c_uint8)).contents.value
    elif in_type == TDH_INTYPE_INT16:
        return cast(buffer, POINTER(c_int16)).contents.value
    elif in_type == TDH_INTYPE_UINT16:
        return cast(buffer, POINTER(c_uint16)).contents.value
    elif in_type == TDH_INTYPE_INT32:
        return cast(buffer, POINTER(c_int32)).contents.value
    elif in_type == TDH_INTYPE_UINT32:
        return cast(buffer, POINTER(c_uint32)).contents.value
    elif in_type == TDH_INTYPE_INT64:
        return cast(buffer, POINTER(c_int64)).contents.value
    elif in_type == TDH_INTYPE_UINT64:
        return cast(buffer, POINTER(c_uint64)).contents.value
    elif in_type == TDH_INTYPE_FLOAT:
        return cast(buffer, POINTER(c_float)).contents.value
    elif in_type == TDH_INTYPE_DOUBLE:
        return cast(buffer, POINTER(c_double)).contents.value
    elif in_type == TDH_INTYPE_POINTER:
        return cast(buffer, POINTER(c_uint64)).contents.value
    else:
        LOGGER.debug("InType not handled: {}".format(in_type))

    return bytes(buffer)


# Thanks to https://github.com/fireeye/pywintrace/blob/master/etw/common.py#L90
def rel_ptr_to_str(base, offset):
    """
    Helper function to convert a relative offset to a string to the actual string.
    """
    return cast(
        rel_ptr_to_ptr(base, offset),
        c_wchar_p
    ).value


def rel_ptr_to_ptr(base, offset):
    """
    Helper function to convert a relative offset to a void pointer.
    """
    return cast(
        (cast(base, c_voidp).value + offset),
        c_voidp
    )
