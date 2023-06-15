from FacebookPostLocation.Config import Config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

hiddenSheetName = "LOOKUP_SHEET"


def Append(values: list):

    conf = Config()
    serviceAccountKeyFileLocation = conf.Config['GoogleApi']['ServiceAccountKeyFileLocation']
    spreadsheetId = conf.Config['GoogleApi']['SpreadsheetId']

    # Authenticate and construct service.
    credentials = service_account.Credentials.from_service_account_file(
        serviceAccountKeyFileLocation)
    service = build('sheets', 'v4', credentials=credentials)

    # See of the search sheet exists and create if not
    ranges = [hiddenSheetName+"!A1:B1"]
    getFormulaCells = service.spreadsheets().get(spreadsheetId=spreadsheetId,
                                                 ranges=ranges, includeGridData=True)
    try:
        response = getFormulaCells.execute()
    except:
        createSheetPayload = {"requests": [
            {"addSheet": {"properties": {"hidden": True, "title": hiddenSheetName}}}, ]}
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheetId, body=createSheetPayload).execute()

    # Set the formula
    # TODO unhardcode this, probably by passing in an object now to this method rather than just a list
    url = values[6]
    formula = '=COUNTIF(Data!G:G, "'+url+'")'
    addFormulaPayload = {
        "range": hiddenSheetName+"!A1",
        "majorDimension": "COLUMNS",
        "values": [[formula]]
    }

    response = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId, range=hiddenSheetName+"!A1", body=addFormulaPayload, valueInputOption="USER_ENTERED", includeValuesInResponse=True).execute()

    # Check to see if the data is in the data sheet by looking at the response from the formula
    urlCount = response['updatedData']['values'][0][0]

    if (urlCount == '0'):
        # Append the data if it does not exist
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheetId, range="Data!A:A",
            valueInputOption="USER_ENTERED", body={'values': [values]}).execute()
