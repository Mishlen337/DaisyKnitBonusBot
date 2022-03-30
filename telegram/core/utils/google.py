from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from . import auth

from ..config import config as settings

import pickle
import requests
import os, json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from . import auth


# The ID and range of a sample spreadsheet.


def append_row(values):
    body = {"values": values}
    # The ID and range of a sample spreadsheet.
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("./token.pickle"):
        with open("./token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                client_config=json.loads(settings.GOOGLE_AUTH_CREDS.replace("'", '"')),
                scopes=auth.scopes
            )
            creds = flow.run_console()
        # Save the credentials for the next run
        with open("./token.pickle", "wb") as token:
            pickle.dump(creds, token)
    service = build("sheets", "v4", credentials=creds, cache_discovery=False)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .append(spreadsheetId=settings.GOOGLE_TABLE_ID, valueInputOption="RAW", body=body)
        .execute()
    )
