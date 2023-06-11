# May replace this with the entire Python Library, but for now it's just one API call
import requests
import json
from LocationParser.Config import Config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


def Append(values: list):

    conf = Config()
    serviceAccountKeyFileLocation = conf.Config['GoogleApi']['ServiceAccountKeyFileLocation']
    spreadsheetId = conf.Config['GoogleApi']['SpreadsheetId']

    # Authenticate and construct service.
    credentials = service_account.Credentials.from_service_account_file(
        serviceAccountKeyFileLocation)

    # Build the service object.
    service = build('sheets', 'v4', credentials=credentials)
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId, range="A:Z",
        valueInputOption="USER_ENTERED", body={'values': [values]}).execute()
