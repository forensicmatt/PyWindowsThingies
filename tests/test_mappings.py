import unittest
from winthingies.mappings import PublisherMapping


class TestPublisherMapping(unittest.TestCase):
    def test_publisher_mapping(self):
        publisher_mapping = PublisherMapping()
        keyword_name = publisher_mapping.get_keyword_name(
            "22FB2CD6-0E7B-422B-A0C7-2FAD1FD0E716",
            0x0000000000000010
        )
        self.assertEqual("WINEVENT_KEYWORD_PROCESS", keyword_name)

        keyword_name = publisher_mapping.get_keyword_name(
            "22FB2CD6-0E7B-422B-A0C7-2FAD1FD0E716",
            0x0000000000000020
        )
        self.assertEqual("WINEVENT_KEYWORD_THREAD", keyword_name)


if __name__ == '__main__':
    unittest.main()
