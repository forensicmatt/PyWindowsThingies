import os
import logging
import ctypes
from winthingies.win32.const import *
from winthingies.win32.psapi import psapi
from winthingies.win32.kernel32 import kernel32

LOGGER = logging.getLogger(__name__)


class Process(object):
    def __init__(self, pid, handle):
        self.pid = pid
        self._handle = handle

    @property
    def name(self):
        return os.path.basename(
            self.path
        )

    @property
    def path(self):
        buffer = ctypes.c_buffer(
            0x1024
        )

        name_size = psapi.GetProcessImageFileNameA(
            self._handle,
            buffer,
            len(buffer)
        )

        full_path = buffer[:name_size].decode()

        return full_path

    @staticmethod
    def by_pid(pid):
        process_handle = kernel32.OpenProcess(
            PROCESS_ALL_ACCESS,
            False,
            pid
        )

        process = Process(
            pid,
            process_handle
        )

        return process

    def __del__(self):
        res = kernel32.CloseHandle(
            self._handle
        )
        if res == 0:
            LOGGER.debug(
                "Unable to close process handle {}".format(self.pid)
            )
