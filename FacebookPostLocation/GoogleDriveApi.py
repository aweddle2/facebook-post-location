from FacebookPostLocation.Config import Config
from googleapiclient.discovery import build
from google.oauth2 import service_account

hiddenSheetName = "LOOKUP_SHEET"

# Returns the ID or -1 if not exist


def FileExists(fileName):
    conf = Config()
    dataFolderId = conf.Config['GoogleApi']['FolderId']

    # call drive api client
    googleDriveService = AuthenticateAndBuildGoogleDriveService()

    # Retrieve the existing parents to remove
    response = googleDriveService.files().list(q="name = '"+fileName+"' and parents in '"+dataFolderId+"'",
                                               spaces='drive',
                                               fields='nextPageToken, '
                                               'files(id, name)',
                                               pageToken=None).execute()
    if (len(response.get('files', [])) > 0):
        return response.get('files', [])[0].Get('id')

    return -1


def Move(fileName):

    conf = Config()
    dataFolderId = conf.Config['GoogleApi']['FolderId']

    # call drive api client
    googleDriveService = AuthenticateAndBuildGoogleDriveService()

    # Retrieve the existing parents to remove
    file = googleDriveService.files().get(
        fileId=fileName, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    # Move the file to the new folder
    file = googleDriveService.files().update(fileId=fileName, addParents=dataFolderId,
                                             removeParents=previous_parents,
                                             fields='id, parents').execute()


def AuthenticateAndBuildGoogleDriveService():
    # Authenticate and construct service.
    conf = Config()
    serviceAccountKeyFileLocation = conf.Config['GoogleApi']['ServiceAccountKeyFileLocation']

    credentials = service_account.Credentials.from_service_account_file(
        serviceAccountKeyFileLocation)

    return build('drive', 'v3', credentials=credentials)
