import unittest
import subprocess
from winthingies.process import Process


class TestProcess(unittest.TestCase):
    def test_get_name_by_pid(self):
        p = subprocess.Popen("cmd.exe")
        image_name = Process.get_name_by_pid(p.pid)
        self.assertEqual('\\Device\\HarddiskVolume6\\Windows\\System32\\cmd.exe', image_name)
        p.kill()


if __name__ == '__main__':
    unittest.main()
