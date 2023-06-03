import unittest
from LocationParser.PlacesApi import ResolvePlaceName

class PleacesApiTests(unittest.TestCase):

    def test1(self):
        location1 = ResolvePlaceName("the London Hotel Ardlethen NSW")
        #self.assertEqual("xxxx", location1.text)

        location2 = ResolvePlaceName("Rudds Pub")
        #self.assertEqual("xxxx", location2.text)

if __name__ == '__main__':
    unittest.main()