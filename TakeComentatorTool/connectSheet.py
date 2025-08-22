import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
print("Script directory:", script_dir)
print("Working directory:", os.getcwd())

if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import gspread
from google.oauth2.service_account import Credentials


def connect_credentials():

    scopes = [
        'https://www.googleapis.com/auth/spreadsheets'

    ]
    creds_path = r"C:\Projekty\Repos\MoBu-Scripts\Sensitive\credentials.json"
    if not os.path.isfile(creds_path):
        raise FileNotFoundError(f"Nie znaleziono pliku: {creds_path}")
        print("Using credentials file at:", creds_path)
        creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
        return creds

class SheetInsides:
    client = gspread.authorize(connect_credentials())
    sheet_id = "10RaHeAbc3ECbVyjuchnxoNgRtvNmes1sPU3Dq2iok54"
    workbook = client.open_by_key(sheet_id)


class SheetClass:
    sheetName = "Summary"
    keyName = "AnimName"
    valueName = "Status"


def get_column_values(nrCol):
    usingSheet = mySheetInsides.workbook.worksheet(mySheetClass.sheetName)
    columnNamesTab = []
    columnNamesTab = usingSheet.row_values(nrCol)
    for name in columnNamesTab:
        if name == "":
            columnNamesTab.remove(name)
    return columnNamesTab


def getAnimStatus(lookingAnim):
    usingSheet = mySheetInsides.workbook.worksheet(mySheetClass.sheetName)

    try:
        keyCell = usingSheet.find(mySheetClass.keyName)
        valueCell = usingSheet.find(mySheetClass.valueName)
    except:
        print(f"Error: Could not find key or value cell {mySheetClass.keyName} or {mySheetClass.valueName}")
        return -1
    try:
        animRow = usingSheet.find(lookingAnim, in_column=keyCell.col).row
        animStatus = usingSheet.cell(animRow, valueCell.col).value
        print(f"Animation Status for '{lookingAnim}':", animStatus)
        return animStatus
    except:
        print("Error: no found anim")
        return -1

mySheetClass = SheetClass()
mySheetInsides = SheetInsides()
