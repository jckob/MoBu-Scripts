import os
import sys

#print("Current working dir:", os.getcwd())
#print("Script location (__file__):", os.path.realpath(__file__))
sys.path.append(os.path.realpath(__file__))


script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)
    print(script_dir)


from pyfbsdk import *
import connectSheet as connector
import mobuUI as ui


def connect_table():
    connector.connect_credentials()

def set_inputs():
    connector.mySheetClass.sheetName = ui.uiObjRef.inputSheetName.Text 
    connector.mySheetClass.keyName = ui.uiObjRef.inputKeyNameList.Items[ui.uiObjRef.inputKeyNameList.ItemIndex]
    connector.mySheetClass.valueName = ui.uiObjRef.inputValueNameList.Items[ui.uiObjRef.inputValueNameList.ItemIndex]

    set_colmns_to_lists()
    set_default_selected_lists()


def set_anim_status():
    connect_table()
    set_inputs()

    if ui.uiObjRef.checkBoxAllBtn.State == 1:
        lFbp = create_start_progress()
        takeTab = []
        for take in FBSystem().Scene.Takes:
            takeTab.append(take)
        maxTakeNr = len(takeTab)
        currTakeNr = 0
        for take in takeTab:
            print(f"Processing take!: {take.Name}")
            percent = int((currTakeNr/maxTakeNr) * 100)
            if (lFbp.UserRequestCancell()):
                break

            lFbp.Text = f"downloading.... {take.Name}"
            lFbp.Percent = percent

            returnStatus = connector.getAnimStatus(take.Name)
            if returnStatus != -1:
                take.Comments = returnStatus
                print(f"Animation status for take '{take.Name}' set to: {returnStatus}")

            currTakeNr += 1
        lFbp.ProgressDone()
        del( lFbp)
    else:
        try:
            takeName = FBSystem().CurrentTake.Name
            FBSystem().CurrentTake.Comments = connector.getAnimStatus(str(takeName))
        except:
            print(f"in Table: {connector.getAnimStatus(takeName)}, in mobu: {takeName}")

def set_colmns_to_lists():
    refresh_list(ui.uiObjRef.inputKeyNameList, connector.get_column_values(1))
    refresh_list(ui.uiObjRef.inputValueNameList, connector.get_column_values(1))
    


def refresh_list(listUI, list):
    listUI.Items.removeAll()
    for item in list:
        if isinstance(item, str):
            listUI.Items.append(item)
        else:
            listUI.Items.append(item.Name)

def set_default_selected_lists():
    ui.uiObjRef.inputKeyNameList.Selected((find_str_in_list(connector.mySheetClass.keyName, ui.uiObjRef.inputKeyNameList.Items)), True)
    ui.uiObjRef.inputValueNameList.Selected((find_str_in_list(connector.mySheetClass.valueName, ui.uiObjRef.inputValueNameList.Items)), True)
    print(f"value for: {connector.mySheetClass.valueName} IS: {find_str_in_list(connector.mySheetClass.valueName, ui.uiObjRef.inputValueNameList.Items)}")

def find_str_in_list(name, list):
    tableIndx = 0
    for item in list:
        if name == item:
             return tableIndx
        tableIndx +=1 
             

def BtnCallback(control, event):
    if control.Caption == "ConnectTable":
        print("connected clicked")
    elif control.Caption == "CheckInputs":
        print("Check inputs clicked")
        set_inputs()
    elif control.Caption == "CheckAllTakes":
        print("Check all Takes clicked")
    elif control.Caption == "Update":
        print("Update clicked")
        set_anim_status()


def set_ui_def():
    ui.CreateTool()
    ui.uiObjRef.connectBtn.OnClick.Add(BtnCallback)
    ui.uiObjRef.checkInputs.OnClick.Add(BtnCallback)
    ui.uiObjRef.checkBoxAllBtn.OnClick.Add(BtnCallback)
    ui.uiObjRef.updateBtn.OnClick.Add(BtnCallback)


def create_start_progress():
    # Create a FBProgress object and set default values for the caption and text.
    lFbp = FBProgress()

    # Call ProgressBegin() before use any other function and property.
    lFbp.ProgressBegin()

    # Set the custom task name.
    lFbp.Caption = "Download & Setup Data"
    return lFbp

set_ui_def()
set_colmns_to_lists()
set_default_selected_lists()