from datetime import datetime, timedelta
from FacebookApi import GetPosts
from LocationParser import GetEntities
from GoogleSheetApi import Append
from PlacesApi import ResolvePlaceName
from Config import Config
from googleapiclient.discovery import build
from google.oauth2 import service_account

date_format = '%Y-%m-%d %H:%M:%S'


def Process():
    service = AuthenticateAndBuildService()
    conf = Config()
    masterSpreadsheetId = conf.Config['GoogleApi']['MasterSpreadsheetId']
    # get all the groups from the master sheet
    sheet = service.spreadsheets().values().get(
        spreadsheetId=masterSpreadsheetId, range="Groups!A2:D").execute()

    for index, row in sheet['values']:
        # Set new processed date to now minus 1 hour so it doesn't try and process every time this runs.  Might need to change this
        newProcessedDate = datetime.now() - timedelta(hours=1)
        # get the last processed date from the row
        if (len(row[3]) == 0):
            # facebook only started on this date, so no groups can be older than this!
            lastProcessedDate = datetime.date(2004, 2, 1)
        else:
            lastProcessedDate = datetime.strptime(row[3], date_format)
        if (lastProcessedDate > newProcessedDate):
            continue

        # process facebook posts created between the 2 timestamps
        ProcessGroup(row[1], row[2], lastProcessedDate, newProcessedDate)

        # update the spreadsheet with the new date
        body = {'values': [[newProcessedDate]]}
        service.spreadsheets().values().update(
            spreadsheetId=masterSpreadsheetId, range="Groups!C"+(index+1), body=body).execute()


def ProcessGroup(facebookGroupID, spreadsheetID, startDate: datetime, endDate: datetime):
    facebookPosts = GetPosts(facebookGroupID, startDate, endDate)
    for facebookPost in facebookPosts:
        # from https://developers.facebook.com/docs/graph-api/reference/v17.0/group/feed
        # The since and until params apply on the updated_time field.
        # so we need to check to see if the post already exists and delete it if it does, as this means the user has updated their post and we should re-process

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


def AuthenticateAndBuildService():
    # Authenticate and construct service.
    conf = Config()
    serviceAccountKeyFileLocation = conf.Config['GoogleApi']['ServiceAccountKeyFileLocation']

    credentials = service_account.Credentials.from_service_account_file(
        serviceAccountKeyFileLocation)

    return build('sheets', 'v4', credentials=credentials)


Process()
