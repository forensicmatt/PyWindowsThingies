import ctypes
from ctypes import wintypes
from winthingies.win32.psapi import psapi
from winthingies.win32.kernel32 import kernel32


def GetProcessImageFileName(handle):
    image_file_name = ctypes.create_unicode_buffer(
        wintypes.MAX_PATH
    )

    string_length = psapi.GetProcessImageFileNameW(
        handle,
        image_file_name,
        len(image_file_name)
    )

    if string_length == 0:
        err_no = kernel32.GetLastError()
        if err_no != 0:
            err = WindowsError(
                err_no, ctypes.FormatError(err_no)
            )
            raise err

    return image_file_name.value
