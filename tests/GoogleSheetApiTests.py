import unittest
from LocationParser.GoogleSheetApi import Append


class PlacesApiTests(unittest.TestCase):

    def test1(self):
        Append(["text", "from", "a", "unit", "test"])


if __name__ == '__main__':
    unittest.main()
