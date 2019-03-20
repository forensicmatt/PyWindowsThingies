import unittest
from winthingies.win32.wevtapi import *
from winthingies.win32.wevtapi_helpers import PublisherMetadata


class TestProvider(unittest.TestCase):
    def test_get_providers(self):
        publisher_list_handle = EvtOpenPublisherEnum()

        publisher_list = []
        while True:
            publisher_name = EvtNextPublisherId(publisher_list_handle)
            if publisher_name is not None:
                publisher_list.append(
                    publisher_name
                )
            else:
                break

        self.assertEqual(True, bool("Microsoft-Windows-Kernel-File" in publisher_list))
        self.assertEqual(True, bool("Microsoft-Windows-Kernel-Registry" in publisher_list))

        for publisher_name in sorted(publisher_list):
            print(publisher_name)

        wevtapi.EvtClose(
            publisher_list_handle
        )

    def test_publisher_metadata(self):
        publisher_metadata = PublisherMetadata(
            "Microsoft-Windows-Kernel-Process"
        )

        self.assertEqual('Microsoft-Windows-Kernel-Process', publisher_metadata.publisher_message)
        self.assertEqual('C:\\WINDOWS\\system32\\Microsoft-Windows-System-Events.dll', publisher_metadata.resource_file_path)
        self.assertEqual(None, publisher_metadata.parameter_file_path)
        self.assertEqual('C:\\WINDOWS\\system32\\Microsoft-Windows-System-Events.dll', publisher_metadata.message_file_path)
        self.assertEqual('https://go.microsoft.com/fwlink/events.asp?CoName=Microsoft%20Corporation&ProdName='
                         'Microsoft%c2%ae%20Windows%c2%ae%20Operating%20System&ProdVer=10.0.17134.1&FileName='
                         'Microsoft-Windows-System-Events.dll&FileVer=10.0.17134.1', publisher_metadata.help_link)

        self.assertEqual(11, len(publisher_metadata.keyword_mapping))
        self.assertEqual("WINEVENT_KEYWORD_PROCESS", publisher_metadata.keyword_mapping[16]["name"])
        self.assertEqual("WINEVENT_KEYWORD_THREAD", publisher_metadata.keyword_mapping[32]["name"])
        self.assertEqual("WINEVENT_KEYWORD_IMAGE", publisher_metadata.keyword_mapping[64]["name"])
        self.assertEqual("WINEVENT_KEYWORD_CPU_PRIORITY", publisher_metadata.keyword_mapping[128]["name"])
        self.assertEqual("WINEVENT_KEYWORD_OTHER_PRIORITY", publisher_metadata.keyword_mapping[256]["name"])
        self.assertEqual("WINEVENT_KEYWORD_PROCESS_FREEZE", publisher_metadata.keyword_mapping[512]["name"])
        self.assertEqual("WINEVENT_KEYWORD_JOB", publisher_metadata.keyword_mapping[1024]["name"])
        self.assertEqual("WINEVENT_KEYWORD_ENABLE_PROCESS_TRACING_CALLBACKS", publisher_metadata.keyword_mapping[2048]["name"])
        self.assertEqual("WINEVENT_KEYWORD_JOB_IO", publisher_metadata.keyword_mapping[4096]["name"])
        self.assertEqual("WINEVENT_KEYWORD_WORK_ON_BEHALF", publisher_metadata.keyword_mapping[8192]["name"])
        self.assertEqual("WINEVENT_KEYWORD_JOB_SILO", publisher_metadata.keyword_mapping[16384]["name"])

        self.assertEqual("Info", publisher_metadata.opcode_mapping[0]["message"])
        self.assertEqual("win:Info", publisher_metadata.opcode_mapping[0]["name"])
        self.assertEqual(0, publisher_metadata.opcode_mapping[0]["value"])
        self.assertEqual("Start", publisher_metadata.opcode_mapping[65536]["message"])
        self.assertEqual("win:Start", publisher_metadata.opcode_mapping[65536]["name"])
        self.assertEqual(65536, publisher_metadata.opcode_mapping[65536]["value"])
        self.assertEqual("Stop", publisher_metadata.opcode_mapping[131072]["message"])
        self.assertEqual("win:Stop", publisher_metadata.opcode_mapping[131072]["name"])
        self.assertEqual(131072, publisher_metadata.opcode_mapping[131072]["value"])

        self.assertEqual(18, len(publisher_metadata.task_mapping))

        self.assertEqual('win:Informational', publisher_metadata.level_mapping[4]["name"])

        self.assertEqual('Microsoft-Windows-Kernel-Process/Analytic', publisher_metadata.channel_mapping[0]["path"])


if __name__ == '__main__':
    unittest.main()
