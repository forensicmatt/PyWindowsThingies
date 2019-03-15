import unittest
from winthingies.win32.wevtapi import *
from winthingies.win32.wevtapi_helpers import get_keyword_mapping


class TestProvider(unittest.TestCase):
    def test_get_metadata(self):
        """PublisherMetadata is needed to map keyword descriptions to their flag.

        :return:
        """
        # This function opens up a metadata handle to a given local publisher
        metadata_handle = EvtOpenPublisherMetadata(
            "Microsoft-Windows-Kernel-Process"
        )

        mapping = get_keyword_mapping(
            metadata_handle
        )

        self.assertEqual(11, len(mapping))
        self.assertEqual("WINEVENT_KEYWORD_PROCESS", mapping[16]["name"])
        self.assertEqual("WINEVENT_KEYWORD_THREAD", mapping[32]["name"])
        self.assertEqual("WINEVENT_KEYWORD_IMAGE", mapping[64]["name"])
        self.assertEqual("WINEVENT_KEYWORD_CPU_PRIORITY", mapping[128]["name"])
        self.assertEqual("WINEVENT_KEYWORD_OTHER_PRIORITY", mapping[256]["name"])
        self.assertEqual("WINEVENT_KEYWORD_PROCESS_FREEZE", mapping[512]["name"])
        self.assertEqual("WINEVENT_KEYWORD_JOB", mapping[1024]["name"])
        self.assertEqual("WINEVENT_KEYWORD_ENABLE_PROCESS_TRACING_CALLBACKS", mapping[2048]["name"])
        self.assertEqual("WINEVENT_KEYWORD_JOB_IO", mapping[4096]["name"])
        self.assertEqual("WINEVENT_KEYWORD_WORK_ON_BEHALF", mapping[8192]["name"])
        self.assertEqual("WINEVENT_KEYWORD_JOB_SILO", mapping[16384]["name"])

        wevtapi.EvtClose(
            metadata_handle
        )


if __name__ == '__main__':
    unittest.main()
