import os
import sys
import time

script_dir = os.path.dirname(os.path.realpath(__file__))
print("Script directory:", script_dir)
print("Working directory:", os.getcwd())

if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import gspread
from google.oauth2.service_account import Credentials
import asyncio


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
    def __init__(self):
        self.client = gspread.authorize(connect_credentials())
        self.sheet_id = "10RaHeAbc3ECbVyjuchnxoNgRtvNmes1sPU3Dq2iok54"
        self.workbook = self.client.open_by_key(self.sheet_id) 

class SheetClass:
    sheetName = "Summary"
    keyName = "AnimName"
    valueName = "Status"


_timer_start = None


import asyncio
from functools import partial

# --- helpers for async gspread calls ---
async def run_in_executor(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, partial(func, *args, **kwargs))


# --- main logic ---
async def get_anim(lookingAnim):
    start_timer()

    row1 = await get_base_row()

    col1 = check_table(row1, mySheetClass.keyName) + 1
    col2 = check_table(row1, mySheetClass.valueName) + 1

    ws = mySheetInsides.workbook.worksheet(mySheetClass.sheetName)

    # run both col fetches concurrently
    col1Values, col2Values = await asyncio.gather(
        run_in_executor(ws.col_values, col1),
        run_in_executor(ws.col_values, col2)
    )

    print("COL2V: ", col2Values)
    finalIndex = check_table(col1Values, lookingAnim)

    if finalIndex == -1:
        print("Value not found")
        return None

    result = col2Values[finalIndex]
    print("Final Value for", lookingAnim, "IS |||", result)
    stop_timer("Async")
    return result


async def get_base_row():
    ws = mySheetInsides.workbook.worksheet(mySheetClass.sheetName)
    row_values = await run_in_executor(ws.row_values, 1)

    # filter empty cells
    return [name for name in row_values if name != ""]


def check_table(table, value):
    try:
        idx = table.index(value)
        #print(value, "---->:", idx)
        return idx
    except ValueError:
        #print("---- ")
        return -1

def get_row_values(rowNr):
    return mySheetInsides.workbook.worksheet(mySheetClass.sheetName).row_values(rowNr)


def start_timer():
    global _timer_start
    _timer_start = time.perf_counter()

def stop_timer(label="Elapsed"):
    if _timer_start is None:
        raise RuntimeError("Timer was not started. Call start_timer() first.")
    elapsed = (time.perf_counter() - _timer_start) * 1000  # ms
    print(f"{label}: {elapsed:.2f} ms")
    return elapsed



mySheetClass = SheetClass()
mySheetInsides = SheetInsides()

#asyncio.run(get_anim("Pivot_R"))

