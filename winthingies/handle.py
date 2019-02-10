import logging
from ctypes import wintypes
from winthingies.runtime import CURRENT_PROCESS
from winthingies.process import Process
from winthingies.win32.const import *
from winthingies.win32.ntdll import ntdll
from winthingies.win32.kernel32 import kernel32
from winthingies.win32.winstructs import *

LOGGER = logging.getLogger(__name__)

ObjectNameInformation = 1
ObjectDataInformation = 2


def get_handle_name_by_object_id(object_id, handle_type=None):
    """Return a handle by the address.

    :param object_id: (u64)
    :param handle_type: (None|str)
    :return: (Handle|None)
    """
    system_handle_information = SYSTEM_HANDLE_INFORMATION_EX()
    size = DWORD(sizeof(system_handle_information))

    while True:
        result = ntdll.NtQuerySystemInformation(
            SystemExtendedHandleInformation,
            byref(system_handle_information),
            size,
            byref(size)
        )
        if result == STATUS_SUCCESS:
            break
        elif result == STATUS_INFO_LENGTH_MISMATCH:
            size = DWORD(
                size.value * 4
            )

            resize(
                system_handle_information,
                size.value
            )
        else:
            raise Exception("NtQuerySystemInformation", hex(result))

    handles = cast(
        system_handle_information.Handles,
        POINTER(
            Handle * \
            system_handle_information.NumberOfHandles
        )
    )
    for handle in handles.contents:
        if handle.Object == object_id:
            if handle_type:
                if handle.type_name == handle_type:
                    return handle.name
            else:
                return handle.name


def iterate_handles(pid=None):
    system_handle_information = SYSTEM_HANDLE_INFORMATION_EX()
    size = DWORD(sizeof(system_handle_information))

    while True:
        result = ntdll.NtQuerySystemInformation(
            SystemExtendedHandleInformation,
            byref(system_handle_information),
            size,
            byref(size)
        )
        if result == STATUS_SUCCESS:
            break
        elif result == STATUS_INFO_LENGTH_MISMATCH:
            size = DWORD(
                size.value * 4
            )

            resize(
                system_handle_information,
                size.value
            )
        else:
            raise Exception("NtQuerySystemInformation", hex(result))

    handles = cast(
        system_handle_information.Handles,
        POINTER(
            Handle * \
            system_handle_information.NumberOfHandles
        )
    )

    for handle in handles.contents:
        if pid is None:
            yield handle
        else:
            if pid == handle.UniqueProcessId:
                yield handle


def get_handle_name(handle):
    """Get the handle type information.
    """
    raw_buffer = ctypes.c_buffer(0x1000)
    size = DWORD(
        sizeof(raw_buffer)
    )
    while True:
        result = ntdll.NtQueryObject(
            handle,
            ObjectNameInformation,
            byref(raw_buffer),
            size,
            0x0
        )
        if result == STATUS_SUCCESS:
            name = LSA_UNICODE_STRING.from_buffer_copy(
                raw_buffer[:size.value]
            ).str
            return name
        elif result == STATUS_INFO_LENGTH_MISMATCH:
            size = DWORD(
                size.value * 4
            )

            resize(
                raw_buffer,
                size.value
            )
        elif result == STATUS_INVALID_HANDLE:
            return "INVALID HANDLE: %s" % hex(handle)
        else:
            LOGGER.info("Unknown")
            return "UNHANDLED RESULT FOR NAME QUERY"


def get_handle_type_info(handle):
    """Get the handle type information.
    """
    public_object_type_information = PUBLIC_OBJECT_TYPE_INFORMATION()
    size = DWORD(
        sizeof(public_object_type_information)
    )
    while True:
        result = ntdll.NtQueryObject(
            handle,
            ObjectDataInformation,
            byref(public_object_type_information),
            size,
            0x0
        )
        if result == STATUS_SUCCESS:
            return public_object_type_information.TypeName.str
        elif result == STATUS_INFO_LENGTH_MISMATCH:
            size = DWORD(
                size.value * 4
            )

            resize(
                public_object_type_information,
                size.value
            )
        elif result == STATUS_INVALID_HANDLE:
            return "INVALID HANDLE: %s" % hex(handle)
        else:
            raise Exception("Unknown")


class Handle(SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX):
    @property
    def process(self):
        if not hasattr(self, "_process"):
            self._process = Process.by_pid(
                self.UniqueProcessId
            )
        return self._process

    @property
    def type_name(self):
        """The name of the handle type.

        :return: (str)
        """
        local_handle = self.get_local_handle()
        if local_handle is None:
            return

        type_name = get_handle_type_info(
            local_handle
        )

        return type_name

    @property
    def name(self):
        """The name of the handle.

        :return: (str)
        """
        local_handle = self.get_local_handle()
        if local_handle is None:
            return

        handle_name = get_handle_name(
            local_handle
        )

        return handle_name

    def get_local_handle(self, current_process=CURRENT_PROCESS):
        """Get a local copy of the handle.

        :return: (int)
        """
        if self.UniqueProcessId == current_process.pid:
            return self.HandleValue

        local_handle = wintypes.HANDLE()

        # We need to run this in a timeout thread to insure no hanging
        # https://social.technet.microsoft.com/Forums/en-US/7f8c7ef3-398a-4a4e-b9e6-17145bc9a708/ntqueryobject-hanging?forum=windowsinternals
        # https://github.com/tamentis/psutil/blob/master/psutil/arch/mswindows/process_handles.c#L180
        kernel32.DuplicateHandle(
            self.process._handle,        #hSourceProcessHandle
            self.HandleValue,            #hSourceHandle
            current_process._handle,     #hTargetProcessHandle
            ctypes.byref(local_handle),  #lpTargetHandle
            0,                           #dwDesiredAccess
            False,                       #bInheritHandle
            DUPLICATE_SAME_ACCESS        #dwOptions
        )

        return local_handle.value

    def as_dict(self):
        handle_dict = {
            "Object": self.Object,
            "UniqueProcessId": self.UniqueProcessId,
            "HandleValue": self.HandleValue,
            "GrantedAccess": self.GrantedAccess,
            "CreatorBackTraceIndex": self.CreatorBackTraceIndex,
            "ObjectTypeIndex": self.ObjectTypeIndex,
            "HandleAttributes": self.HandleAttributes,
            "Reserved": self.Reserved,
            "Type": self.type_name,
            "Name": self.name
        }

        return handle_dict
