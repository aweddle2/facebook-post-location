import unittest
from FacebookPostLocation.FacebookApi import GetPosts


class FacebookApiTests(unittest.TestCase):

    def test1(self):
        postResponse = GetPosts()

        self.assertEqual("https://www.facebook.com/groups/1252515138743868/permalink/1254050395257009/",
                         postResponse.posts[0].permalink_url)
        self.assertEqual("post 3", postResponse.posts[0].message)
        self.assertEqual("https://www.facebook.com/groups/1252515138743868/permalink/1252516325410416/",
                         postResponse.posts[1].permalink_url)
        self.assertEqual("Post 2", postResponse.posts[1].message)


if __name__ == '__main__':
    unittest.main()
