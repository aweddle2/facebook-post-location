import unittest
from FacebookPostLocation.LocationParser import GetEntities


class SpacyTests(unittest.TestCase):

    def test1(self):
        post1 = GetEntities(
            "It was just a day ride but stopped for lunch at the London Hotel Ardlethen NSW, terrific food friendly owners and very much biker friendly")
        self.assertEqual("the London Hotel Ardlethen NSW",
                         post1.locations[0].text)
        self.assertEqual("FAC", post1.locations[0].label_)

        post2 = GetEntities(
            "Rudds Pub at Nobby. Rode in and decided to stay in one of the lovely cabins $150 per night. Great meals.")
        self.assertEqual("Rudds Pub", post2.locations[0].text)
        self.assertEqual("PERSON", post2.locations[0].label_)
        self.assertEqual("150", post2.costs[0].text)
        self.assertEqual("MONEY", post2.costs[0].label_)

        post3 = GetEntities("We stayed at the East Charlton Hotel in Charlton Victoria, on the Calder Hwy between Melbourne and Mildura. Rooms are $55 per night and clean. Bathroom was very clean. There is an undercover area out the back where you can park your bikes. Hosts are great and the meals are very good.")
        self.assertEqual("the East Charlton Hotel", post3.locations[0].text)
        self.assertEqual("FAC", post3.locations[0].label_)
        self.assertEqual("55", post3.costs[0].text)
        self.assertEqual("MONEY", post3.costs[0].label_)


if __name__ == '__main__':
    unittest.main()
