import os
import logging
import ctypes
from winthingies.win32.const import *
from winthingies.win32.psapi import psapi
from winthingies.win32.kernel32 import kernel32
from winthingies.win32.winstructs import *

LOGGER = logging.getLogger(__name__)


def iterate_processes():
    process_entry = PROCESSENTRY32()
    process_entry.dwSize = ctypes.sizeof(
        process_entry
    )

    snapshot = kernel32.CreateToolhelp32Snapshot(
        TH32CS_SNAPPROCESS,
        0
    )

    kernel32.Process32First(
        snapshot,
        process_entry
    )

    yield Process.by_pid(
        process_entry.th32ProcessID,
        access=PROCESS_QUERY_LIMITED_INFORMATION
    )

    while kernel32.Process32Next(snapshot, process_entry):
        yield Process.by_pid(
            process_entry.th32ProcessID,
            access=PROCESS_QUERY_LIMITED_INFORMATION
        )


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
    def by_pid(pid, access=PROCESS_ALL_ACCESS):
        process_handle = kernel32.OpenProcess(
            access,
            False,
            pid
        )

        process = Process(
            pid,
            process_handle
        )

        return process

    def as_dict(self):
        return {
            "name": self.name,
            "path": self.path,
            "pid": self.pid
        }

    def __del__(self):
        res = kernel32.CloseHandle(
            self._handle
        )
        if res == 0:
            LOGGER.debug(
                "Unable to close process handle {}".format(self.pid)
            )
