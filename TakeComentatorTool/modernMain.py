import os
import sys

sys.path.append(os.path.realpath(__file__))

script_dir = os.path.dirname(os.path.realpath(__file__))
print("Script directory:", script_dir)
print("Working directory:", os.getcwd())

if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)
    print(script_dir)


from pyfbsdk import FBSystem, FBProgress
import connectSheet as connector
import modernUI as ui
from PySide2 import QtWidgets
import asyncio


class FakeControl:
    def __init__(self, caption):
        self.Caption = caption


def connect_table():
    connector.connect_credentials()

def set_inputs():
    setattr(ui.uiObjRef.inputKeyNameList, "allItems", lambda: [ui.uiObjRef.inputKeyNameList.itemText(i) for i in range(ui.uiObjRef.inputKeyNameList.count())])
    connector.mySheetClass.sheetName = ui.uiObjRef.inputSheetName.text()
    connector.mySheetClass.keyName = ui.uiObjRef.inputKeyNameList.currentText()
    connector.mySheetClass.valueName = ui.uiObjRef.inputValueNameList.currentText()
    
    set_colmns_to_lists()
    set_default_selected_lists()


def set_anim_status():
    connect_table()
    set_inputs()
    lFbp = create_start_progress("initialize...update")

    async def process_all():
        if int(ui.uiObjRef.checkBoxAllBtn.isChecked()) == 1:
            takeTab = list(FBSystem().Scene.Takes)
            maxTakeNr = len(takeTab)
            currTakeNr = 0

            for take in takeTab:
                print(f"Processing take!: {take.Name}")
                percent = int((currTakeNr / maxTakeNr) * 100)
                if lFbp.UserRequestCancell():
                    break

                set_progress_status(lFbp, f"Set up.... {take.Name}", percent)

                # await connector call here
                returnStatus = await connector.get_anim(take.Name)
                if returnStatus not in (-1, None):
                    take.Comments = returnStatus
                    print(f"Animation status for take '{take.Name}' set to: {returnStatus}")

                currTakeNr += 1
        else:
            try:
                takeName = FBSystem().CurrentTake.Name
                set_progress_status(lFbp, f"Check input.... {takeName}", 40)
                set_progress_status(lFbp, f"Downloading.... {takeName}", 80)

                # keep sync connector here if it’s not async yet
                returnStatus = await connector.get_anim(takeName)
                if returnStatus not in (-1, None):
                    FBSystem().CurrentTake.Comments = returnStatus
                    print(f"Animation status for take '{takeName}' set to: {returnStatus}")
            except Exception as e:
                print(f"in mobu: {FBSystem().CurrentTake.Name}, in Table: not found!!! ({e})")

    # run everything inside one loop
    asyncio.run(process_all())

    lFbp.ProgressDone()
    del lFbp


def set_colmns_to_lists():
    refresh_list(ui.uiObjRef.inputKeyNameList, connector.get_column_values(1))
    refresh_list(ui.uiObjRef.inputValueNameList, connector.get_column_values(1))
    

def refresh_list(listUI, list):
    listUI.clear()
    for item in list:
        if isinstance(item, str):
            listUI.addItem(item)
        else:
            listUI.addItem(item.Name)

def set_default_selected_lists():
    setattr(ui.uiObjRef.inputKeyNameList, "allItems", lambda: [ui.uiObjRef.inputKeyNameList.itemText(i) for i in range(ui.uiObjRef.inputKeyNameList.count())])
    setattr(ui.uiObjRef.inputValueNameList, "allItems", lambda: [ui.uiObjRef.inputValueNameList.itemText(i) for i in range(ui.uiObjRef.inputValueNameList.count())])
    ui.uiObjRef.inputKeyNameList.setCurrentIndex((find_str_in_list(connector.mySheetClass.keyName, ui.uiObjRef.inputKeyNameList.allItems())))
    ui.uiObjRef.inputValueNameList.setCurrentIndex((find_str_in_list(connector.mySheetClass.valueName, ui.uiObjRef.inputValueNameList.allItems())))

    
def find_str_in_list(name, list):
    tableIndx = 0
    for item in list:
        if name == item:
             return int(tableIndx)
        tableIndx +=1 


def BtnCallback(control, event):
    if control.Caption == "CheckInputs":
        print("Check inputs clicked")
        set_inputs()
    elif control.Caption == "CheckAllTakes":
        print("Check all Takes clicked")
    elif control.Caption == "Update":
        print("Update clicked")
        set_anim_status()
    elif control.Caption == "ClearComments":
        clear_comments()
        print("clearing comments")

def set_ui_def():
    ui.show_tool()

    set_button_connections(ui.uiObjRef.updateBtn, "Update")
    set_button_connections(ui.uiObjRef.checkInputs, "CheckInputs")
    set_button_connections(ui.uiObjRef.checkBoxAllBtn, "CheckAllTakes")
    set_button_connections(ui.uiObjRef.clearCommentsBtn, "ClearComments")


def set_button_connections(buttonRef, controlName):
    try:
        buttonRef.clicked.disconnect()
    except:
        pass
    buttonRef.clicked.connect(lambda: BtnCallback(FakeControl(controlName), None))

def create_start_progress(caption):
    # Create a FBProgress object and set default values for the caption and text.
    lFbp = FBProgress()

    # Call ProgressBegin() before use any other function and property.
    lFbp.ProgressBegin()

    # Set the custom task name.
    lFbp.Caption = caption
    return lFbp

def set_progress_status(lFbp, text, percent):
    lFbp.Caption = text
    lFbp.Percent = percent
    
def clear_comments():
    if int(ui.uiObjRef.checkBoxAllBtn.isChecked()) == 1:
        lFbp = create_start_progress("initialize...clean")
        currTakeNr = 1
        maxTakesNr = len(FBSystem().Scene.Takes)
        print(f"FBSystem().Scene.Takes.count: {maxTakesNr}")
        for take in FBSystem().Scene.Takes:
            print(f"Processing take!: {take.Name}")
            percent = int((currTakeNr/maxTakesNr) * 100)
            if (lFbp.UserRequestCancell()):
                break
            set_progress_status(lFbp, f"clearing {take.Name}", percent)
            take.Comments = ""
            currTakeNr += 1
        lFbp.ProgressDone()
        del( lFbp)
        
    else:
        FBSystem().CurrentTake.Comments = ""
        print("Comments cleared.")

            

set_ui_def()
set_colmns_to_lists()
set_default_selected_lists()
