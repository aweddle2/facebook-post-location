from FacebookPostLocation.Config import Config
from googleapiclient.discovery import build
from google.oauth2 import service_account
from FacebookPostLocation.GoogleSheetApi import CreateIfNotExist
hiddenSheetName = "LOOKUP_SHEET"

# TODO this will eventually be an http endpoint called when someone installs the app into their group
# TODO a lot of this is duplicated in the GoogleSheetsApi.py


def Install(facebookGroupName, facebookGroupId):
    conf = Config()
    masterSpreadsheetId = conf.Config['GoogleApi']['MasterSpreadsheetId']

    service = AuthenticateAndBuildService()

    groupExistsInMasterSheet = ExistingGroup(facebookGroupId)

    if (groupExistsInMasterSheet == False):
        # create a spreadsheet just for the group
        spreadsheetId = CreateIfNotExist(facebookGroupId)

        # Append the data if it does not exist
        service.spreadsheets().values().append(
            spreadsheetId=masterSpreadsheetId, range="Groups!A:A",
            valueInputOption="USER_ENTERED", body={'values': [[facebookGroupName, facebookGroupId, spreadsheetId]]}).execute()


def ExistingGroup(groupId):
    conf = Config()
    masterSpreadsheetId = conf.Config['GoogleApi']['MasterSpreadsheetId']

    service = AuthenticateAndBuildService()
    # See if the lookup  sheet exists and create if not
    ranges = [hiddenSheetName+"!A1:B1"]
    getFormulaCells = service.spreadsheets().get(spreadsheetId=masterSpreadsheetId,
                                                 ranges=ranges, includeGridData=True)
    try:
        response = getFormulaCells.execute()
    except:
        createSheetPayload = {"requests": [
            {"addSheet": {"properties": {"hidden": True, "title": hiddenSheetName}}}, ]}
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=masterSpreadsheetId, body=createSheetPayload).execute()

    # Set the formula
    formula = '=COUNTIF(Groups!B:B, "'+groupId+'")'
    addFormulaPayload = {
        "range": hiddenSheetName+"!A1",
        "majorDimension": "COLUMNS",
        "values": [[formula]]
    }

    response = service.spreadsheets().values().update(
        spreadsheetId=masterSpreadsheetId, range=hiddenSheetName+"!A1", body=addFormulaPayload, valueInputOption="USER_ENTERED", includeValuesInResponse=True).execute()

    # If the data is in the data sheet (by looking at the response from the formula) then the group is already in the master sheet
    matchingGroupCount = response['updatedData']['values'][0][0]

    return matchingGroupCount != '0'


def AuthenticateAndBuildService():
    # Authenticate and construct service.
    conf = Config()
    serviceAccountKeyFileLocation = conf.Config['GoogleApi']['ServiceAccountKeyFileLocation']

    credentials = service_account.Credentials.from_service_account_file(
        serviceAccountKeyFileLocation)

    return build('sheets', 'v4', credentials=credentials)
