import unittest
from FacebookPostLocation.GroupInstaller import Install


class GroupInstallerTests(unittest.TestCase):

    def test1(self):
        Install("Andrew Test Group", "123546789")


if __name__ == '__main__':
    unittest.main()
