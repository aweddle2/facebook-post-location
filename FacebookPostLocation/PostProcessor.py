from datetime import datetime, timedelta
from FacebookApi import GetPosts
from LocationParser import GetEntities
from GoogleSheetApi import Append
from PlacesApi import ResolvePlaceName

def Process():
    #get all the groups from the master sheet
    #get the last processed date from the row
    #process facebook posts from that timestamp until now



  ProcessGroup(date: datetime):
    if (date is None):
        date = datetime.now() - timedelta(days=7)
        endDate = datetime.now()

    facebookPosts = GetPosts()
    for facebookPost in facebookPosts:
        parsedPost = GetEntities(facebookPost.message)
        location = None
        if (len(parsedPost.locations) > 0):
            location = parsedPost.locations[0].text

        cost = None
        if (len(parsedPost.costs) > 0):
            cost = parsedPost.costs[0].text

        if (location != None):
            resolvedLocation = ResolvePlaceName(location)
            # if nothing was returned from the google places api then skip this record
            if (resolvedLocation is None):
                continue

            values = [location, resolvedLocation.name, resolvedLocation.formatted_address,
                      resolvedLocation.lat, resolvedLocation.lng, cost, facebookPost.permalink_url]
            Append(values)

Process()
