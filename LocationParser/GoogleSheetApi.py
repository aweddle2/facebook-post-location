# May replace this with the entire Python Library, but for now it's just one API call
import requests
import json
from LocationParser.Config import Config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


def Append(values: list):
    payload = GoogleSheetsAppendPayload(values).to_json()
    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/spreadsheets'
    key_file_location = '/Users/asw/Downloads/facebook-post-location-9367bc1f3fe0.json'

    # Authenticate and construct service.
    service = get_service(
        api_name='sheets',
        api_version='v4',
        scopes=[scope],
        key_file_location=key_file_location)

    update_data(service, payload)


def get_service(api_name, api_version, scopes, key_file_location):

    credentials = service_account.Credentials.from_service_account_file(
        key_file_location)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service


def update_data(service, body):
    body = "{\"values\":[[\"text\",\"from\",\"a\",\"unit\",\"test\"]]}"

    conf = Config()
    spreadsheetId = conf.Config['GoogleApi']['SpreadsheetId']

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId, range="A:Z",
        valueInputOption="USER_ENTERED", body=json.loads(body)).execute()


class GoogleSheetsAppendPayload:
    def __init__(self, values):
        self.values = values

    def to_json(self):
        return self.__str__()
