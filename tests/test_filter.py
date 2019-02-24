import sys
sys.path.append("..")
import unittest
from winthingies.filter import Filter


class TestFilter(unittest.TestCase):
    def test_filter(self):
        record = {'ProcessId': 11252, 'ThreadId': 11824, 'TimeStamp': 131950648422495271,
         'EventDescriptor': {'Opcode': 64, 'Keyword': 0}, 'IrpPtr': 18446614371805737208,
         'FileObject': 18446614371777801008, 'TTID': 11824, 'CreateOptions': 16777312, 'FileAttributes': 0,
         'ShareAccess': 5, 'OpenPath': '\\Device\\HarddiskVolume5\\WINDOWS\\SYSTEM32\\cmd.exe'}

        filter = Filter(
            "ends_with(OpenPath, '.exe')"
        )
        result = filter.is_true(
            record
        )
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
