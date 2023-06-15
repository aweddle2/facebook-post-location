import unittest
from FacebookPostLocation.GoogleSheetApi import Append


class PlacesApiTests(unittest.TestCase):

    def test1(self):
        Append(["Lorem Ipsum", "Loral Ipsum (Aust) Pty Ltd", "22-26 Jersey Rd, Bayswater VIC 3153, Australia",
               "-37.8413503", "145.2793097", "", "https://www.facebook.com/groups/1252515138743868/permalink/1252516268743755/"])


if __name__ == '__main__':
    unittest.main()
