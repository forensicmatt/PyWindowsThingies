import os
import logging
import ctypes
from winthingies.win32.const import *
from winthingies.win32.psapi_helpers import GetProcessImageFileName
from winthingies.win32.kernel32 import kernel32
from winthingies.win32.winstructs import *

LOGGER = logging.getLogger(__name__)


def iterate_processes(name=None):
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

    if name is not None:
        if name.lower() == process_entry.szExeFile.decode("utf-8").lower():
            yield process_entry.clone()
    else:
        yield process_entry.clone()

    while kernel32.Process32Next(snapshot, process_entry):
        if name is not None:
            if name.lower() == process_entry.szExeFile.decode("utf-8").lower():
                yield process_entry.clone()
        else:
            yield process_entry.clone()


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
        """Get the path of this processes image.

        :return: (str)
        """
        image_name = GetProcessImageFileName(
            self._handle
        )

        return image_name

    @staticmethod
    def by_pid(pid, access=PROCESS_ALL_ACCESS):
        process_handle = kernel32.OpenProcess(
            access,
            False,
            pid
        )

        if process_handle is None:
            err_no = kernel32.GetLastError()
            raise (
                WindowsError(
                    err_no, ctypes.FormatError(err_no)
                )
            )

        process = Process(
            pid,
            process_handle
        )

        return process

    @staticmethod
    def get_name_by_pid(pid, access=PROCESS_QUERY_LIMITED_INFORMATION):
        """Get the name of an image by process id.

        :param pid: (int) The process id
        :param access: (int) The process access flag
        :return:
        """
        process_handle = kernel32.OpenProcess(
            access,
            False,
            pid
        )

        if process_handle is None:
            err_no = kernel32.GetLastError()
            raise(
                WindowsError(
                    err_no, ctypes.FormatError(err_no)
                )
            )

        image_name = GetProcessImageFileName(
            process_handle
        )

        return image_name

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
