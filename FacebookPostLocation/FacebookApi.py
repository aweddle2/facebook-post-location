# May replace this with the Facebook Library, but for now it's just one API call
from datetime import datetime
import requests
import json
from FacebookPostLocation.Config import Config

date_format = '%Y-%m-%dT%H:%M:%S'


def GetPosts(facebookGroupID, startDate: datetime, endDate: datetime):
    conf = Config()
    accessToken = conf.Config['Facebook']['UserAccessToken']

    url = "https://graph.facebook.com/"+facebookGroupID + \
        "/feed?fields=permalink_url,message&access_token=" + \
        accessToken + "&since=" + \
        startDate.strftime(date_format) + "&until=" + \
        endDate.strftime(date_format)

    return GetPageOfResults(url)


def GetPageOfResults(url):

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    pageOfResults = FacebookGroupFeedResponse.from_json(
        json.loads(response.text))

    posts = pageOfResults.posts

    if (pageOfResults.paging):
        posts = posts + GetPageOfResults(pageOfResults.paging.next)

    return posts


class FacebookGroupFeedResponse:
    def __init__(self, data, paging):
        self.posts = []
        for item in data:
            self.posts.append(FacebookPost.from_json(item))
        self.paging = None
        if (paging is not None):
            self.paging = FacebookPagination.from_json(paging)

    def __iter__(self):
        yield from {
            "posts": self.posts,
            "paging": self.paging
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.__str__()

    @staticmethod
    def from_json(json_dct):
        paging = None
        if "paging" in json_dct:
            paging = json_dct['paging']
        return FacebookGroupFeedResponse(json_dct['data'], paging)


class FacebookPost:
    def __init__(self, permalink_url, message):
        self.permalink_url = permalink_url
        self.message = message

    def __iter__(self):
        yield from {
            "permalink_url": self.permalink_url,
            "message": self.message
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.__str__()

    @staticmethod
    def from_json(json_dct):
        message = ""
        if "message" in json_dct:
            message = json_dct['message']
        return FacebookPost(json_dct['permalink_url'], message)


class FacebookPagination:
    def __init__(self, previous, next):
        self.previous = previous
        self.next = next

    def __iter__(self):
        yield from {
            "previous": self.previous,
            "next": self.next
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.__str__()

    @staticmethod
    def from_json(json_dct):
        return FacebookPagination(json_dct['previous'], json_dct['next'])
