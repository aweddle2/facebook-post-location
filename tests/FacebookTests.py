import unittest
from FacebookPostLocation.FacebookApi import GetPosts
from datetime import datetime, timedelta


class FacebookApiTests(unittest.TestCase):

    def test1(self):
        startDate = datetime.strptime("2023-06-10", "%Y-%m-%d")
        endDate = datetime.strptime("2023-06-23", "%Y-%m-%d")

        posts = GetPosts(
            '1252515138743868', startDate, endDate)

        self.assertEqual("https://www.facebook.com/groups/1252515138743868/permalink/1257067724955276/",
                         posts[0].permalink_url)
        self.assertEqual(4, len(posts))


if __name__ == '__main__':
    unittest.main()
