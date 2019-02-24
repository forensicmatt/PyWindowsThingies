import os
import sys
sys.path.append("..")
import fmt
import codecs
import struct
import argparse
import datetime
import win32api
import win32con
from functools import partial
from winthingies.trace import EventTraceHandler
from winthingies.trace import TraceProvider
from winthingies.process import iterate_processes
from winthingies.handle import iterate_handles

VERSION = "0.0.1"

CloseKey = 0x0000000000000001
QuerySecurityKey = 0x0000000000000002
SetSecurityKey = 0x0000000000000004
EnumerateValueKey = 0x0000000000000010
QueryMultipleValueKey = 0x0000000000000020
SetInformationKey = 0x0000000000000040
FlushKey = 0x0000000000000080
SetValueKey = 0x0000000000000100
DeleteValueKey = 0x0000000000000200
QueryValueKey = 0x0000000000000400
EnumerateKey = 0x0000000000000800
CreateKey = 0x0000000000001000
OpenKey = 0x0000000000002000
DeleteKey = 0x0000000000004000
QueryKey = 0x0000000000008000


KEYWORD_OPS = {
    0x0000000000000001: "CloseKey",
    0x0000000000000002: "QuerySecurityKey",
    0x0000000000000004: "SetSecurityKey",
    0x0000000000000010: "EnumerateValueKey",
    0x0000000000000020: "QueryMultipleValueKey",
    0x0000000000000040: "SetInformationKey",
    0x0000000000000080: "FlushKey",
    0x0000000000000100: "SetValueKey",
    0x0000000000000200: "DeleteValueKey",
    0x0000000000000400: "QueryValueKey",
    0x0000000000000800: "EnumerateKey",
    0x0000000000001000: "CreateKey",
    0x0000000000002000: "OpenKey",
    0x0000000000004000: "DeleteKey",
    0x0000000000008000: "QueryKey"
}


def get_arguments():
    usage = u"""Monitor UserAssist via ETL. Version: {}
    """.format(VERSION)

    arguments = argparse.ArgumentParser(
        description=usage,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    arguments.add_argument(
        "--format",
        dest="format_str",
        action="store",
        default=None,
        help="This is a python fstring to format output. Default prints json lines."
    )

    return arguments


def enumerate_keywords(keyword):
    """Translate bitmap keyword to string.

    :param keyword: (int|long) EventDescriptor.Keyword
    :return: (str) The string that represents the event keywords
    """
    ops = []
    for key, value in KEYWORD_OPS.items():
        if keyword & key:
            ops.append(value)

    return "|".join(ops)


class UserAssist(object):
    """
    Structure resources:
    https://github.com/EricZimmerman/RegistryPlugins/blob/8822318182ec28a385a9544422d8ae4d14df7fd9/RegistryPlugin.UserAssist/UserAssist.cs#L79
    https://www.aldeid.com/wiki/Windows-userassist-keys
    https://github.com/keydet89/RegRipper2.8/blob/master/plugins/userassist_tln.pl#L85
    """
    def __init__(self, buf):
        self.session = struct.unpack("<I", buf[0:4])[0]
        self.run_count = struct.unpack("<I", buf[4:8])[0]
        self.focus_count = struct.unpack("<I", buf[8:12])[0]
        self.focus_time = struct.unpack("<I", buf[32:36])[0]

        u64_timestamp = struct.unpack("<Q", buf[60:68])[0]
        self.last_execution = datetime.datetime(1601, 1, 1) + datetime.timedelta(
            microseconds=u64_timestamp / 10
        )

    def as_dict(self):
        return {
            "session": self.session,
            "run_count": self.run_count,
            "focus_count": self.focus_count,
            "focus_time": self.focus_time,
            "last_execution": self.last_execution.isoformat(" ")
        }


class UserAssistMonitor(object):
    def __init__(self, format_str=None):
        # We whould only have one explorer.exe running, so just grab the first process
        # under that name.
        explorer_process = list(iterate_processes(name="explorer.exe"))[0]
        self._format_str = format_str
        # Set the PID of explorer.exe
        self.pid = explorer_process.pid
        # This key mapping maps the open UserAssist handles
        self.key_mapping = {}
        for handle in iterate_handles(pid=explorer_process.pid):
            if handle.type_name == "Key":
                if "UserAssist" in handle.name:
                    # Get the starting index of start of the Software path
                    index = handle.name.index(
                        "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist"
                    )

                    # Get the key name from Software on
                    key_name = handle.name[index:]

                    # Open the registry key
                    key_handle = win32api.RegOpenKeyEx(
                        win32con.HKEY_CURRENT_USER,
                        key_name,
                        0,
                        win32con.KEY_READ
                    )

                    # Create mapping of the handle name and the key handle
                    self.key_mapping[handle.Object] = {
                        "name": handle.name,
                        "handle": key_handle
                    }

    def custom_format(self, record):
        return fmt(self._format_str)

    def event_callback(self, event_dict):
        # Only look at events with the explorer.exe PID
        if event_dict["ProcessId"] == self.pid:
            # Only look at events where the key handle is a known UserAssist handle
            if "KeyObject" in event_dict:
                if event_dict["KeyObject"] in self.key_mapping:
                    # Format TimeStamp
                    timestamp = datetime.datetime(1601, 1, 1) + datetime.timedelta(
                        microseconds=event_dict["TimeStamp"] / 10
                    )
                    event_dict["TimeStamp"] = timestamp.isoformat(" ")

                    # Get Key path and handle from our key mapping
                    key_path = self.key_mapping[event_dict["KeyObject"]]["name"]
                    key_handle = self.key_mapping[event_dict["KeyObject"]]["handle"]

                    # Enumerate some values
                    event_dict["ValueNameDecoded"] = codecs.decode(event_dict["ValueName"], 'rot-13')
                    event_dict["ValueFullPath"] = "{}\\{}".format(
                        key_path,
                        event_dict["ValueName"]
                    )
                    event_dict["ValueNameDecoded"] = "{}\\{}".format(
                        key_path,
                        event_dict["ValueNameDecoded"]
                    )

                    # Query Registry data
                    value_data, value_type = win32api.RegQueryValueEx(
                        key_handle,
                        event_dict["ValueName"]
                    )
                    event_dict["EventDescriptor"]["KeywordStr"] = enumerate_keywords(
                        event_dict["EventDescriptor"]["Keyword"]
                    )

                    # Parse UserAssist data
                    user_assist = UserAssist(value_data)
                    event_dict.update(
                        {"UserAssist": user_assist.as_dict()}
                    )

                    if self._format_str:
                        print(self.custom_format(event_dict))
                    else:
                        print(event_dict)


def main():
    arguments = get_arguments()
    options = arguments.parse_args()

    userassist_mon = UserAssistMonitor(
        format_str=options.format_str
    )

    provider_kernel_trace = TraceProvider(
        u"Microsoft-Windows-Kernel-Registry",
        u"{70EB4F03-C1DE-4F73-A051-33D13D5413BD}"
    )

    event_trace_handler = EventTraceHandler(
        "UserAssist Mon",
        [provider_kernel_trace],
        partial(UserAssistMonitor.event_callback, userassist_mon)
    )
    event_trace_handler.start_session()


if __name__ == "__main__":
    main()
