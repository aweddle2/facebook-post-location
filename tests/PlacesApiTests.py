import unittest
from FacebookPostLocation.PlacesApi import ResolvePlaceName


class PlacesApiTests(unittest.TestCase):

    def test1(self):
        location1 = ResolvePlaceName("the London Hotel Ardlethen NSW")
        self.assertEqual("London Hotel-Motel", location1.name)
        self.assertEqual(-34.3577734, location1.lat)
        self.assertEqual(146.897691, location1.lng)
        self.assertEqual(
            "12 Mirrool St, Ardlethan NSW 2665, Australia", location1.formatted_address)

        location2 = ResolvePlaceName("Rudds Pub")
        self.assertEqual("Rudd's Pub", location2.name)
        self.assertEqual(-27.8525459, location2.lat)
        self.assertEqual(151.9031962, location2.lng)
        self.assertEqual("45 Tooth St, Nobby QLD 4360, Australia",
                         location2.formatted_address)


if __name__ == '__main__':
    unittest.main()
