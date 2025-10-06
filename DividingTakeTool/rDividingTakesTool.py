import os, sys

sys.path.append(os.path.realpath(__file__))
script_dir = os.path.dirname(os.path.realpath(__file__))
print("Script directory:", script_dir)
print("Working directory:", os.getcwd())


import rUIDividingTakesTool as ui
from pyfbsdk import FBSystem, FBTime, FBTimeSpan, FBPlayerControl

class Framing():
    def __init__(self):
        #clear ui fields
        self.set_current_time_range_frame(ui.uiObjRef.input1_Edit, ui.uiObjRef.input2_Edit)
        self.set_deltaFrames_field()
        ui.uiObjRef.input3_Edit.clear()

    def validate_to_frames(self, inputField):
        newVar1 = inputField
        if not isinstance(inputField, int):
            newVar1 = frameLogic.change_timecode_to_int(inputField)
        return newVar1

    def calculate_diff_frames(self):
        resultInt = int(ui.uiObjRef.input2_Edit.text()) - int(ui.uiObjRef.input1_Edit.text())
        return str(resultInt)
        
    def get_current_frame(self):
        return FBSystem().LocalTime.GetFrame()
        
    def get_correct_time_code(self, start, end, current):
        if current != start:
            correctTime = FBTime(0, 0, 0, start, 0)
        else:
            correctTime = FBTime(0, 0, 0, end, 0)
        
        return correctTime

    def go_to_correct_value(self):
        input1_Edit = self.validate_to_frames(ui.uiObjRef.input1_Edit)
        input2_Edit = self.validate_to_frames(ui.uiObjRef.input2_Edit)
        startF = int(input1_Edit)
        endF = int(input2_Edit)

        t = self.get_correct_time_code(startF, endF, FBSystem().LocalTime.GetFrame())
        FBPlayerControl().Goto(t)            

    def get_current_take_name(self):
        currentTakeName = FBSystem().CurrentTake
        return currentTakeName

    def get_take_name(self, isCropping):
        currentTakeName = FBSystem().CurrentTake.Name
        if ui.uiObjRef.input3_Edit.text() != "":
            newName = ui.uiObjRef.input3_Edit.text()
        else:
            if isCropping:
                newName = currentTakeName
            else:
                newName = currentTakeName + "_Copy"
        return newName
    

    def change_timecode_to_int(self, input_text):
        timecode_text = input_text.text()

        timecode = FBTime()
        timecode.SetTimeString(timecode_text)

        frames = timecode.GetFrame()
        return frames
    
    def set_current_time_range_frame(self, firstInput, secondInput):
        view_start_frame = FBSystem().CurrentTake.LocalTimeSpan.GetStart()
        view_stop_frame = FBSystem().CurrentTake.LocalTimeSpan.GetStop()
        self.set_input_field(firstInput, view_start_frame.GetFrame())
        self.set_input_field(secondInput, view_stop_frame.GetFrame())

    def set_input_field(self, input_field, value):
        input_field.setText(str(value))
        self.change_status("editing...", "yellow")
    
    def set_deltaFrames_field(self):
        diffFrames = self.calculate_diff_frames()
        ui.uiObjRef.diffFrames_Txt.setText(diffFrames)

    def create_take(self):
        defaultTake = None
        if (not ui.uiObjRef.showCopiedTake_Btn.isChecked()):
            defaultTake = FBSystem().CurrentTake
        
        startF = int(ui.uiObjRef.input1_Edit.text())
        endF = int(ui.uiObjRef.input2_Edit.text())
        if startF >= endF:
            self.change_status("wrong frame range...", "red")
            return

        newTakeName = self.get_take_name(False)
        print("New take name: ", newTakeName)

        newTake = FBSystem().CurrentTake.CopyTake(newTakeName)
        if newTake:
            #self.color_status.setText("Copied: " + newTakeName)
            # timecode to FBTime
            new_start_time = FBTime()
            new_start_time.SetTimeString(ui.uiObjRef.input1_Edit.text())
            
            new_end_time = FBTime()
            new_end_time.SetTimeString(ui.uiObjRef.input2_Edit.text())

            #set upt new range to copied take
            newTake.LocalTimeSpan = FBTimeSpan(new_start_time, new_end_time)
            print("Created take: ", newTake.Name)
            self.change_status("created take", "green")
        else:
            self.change_status("failed to copy...", "red")
        if defaultTake:
            FBSystem().CurrentTake = defaultTake
            print("Changed back to take: ", defaultTake.Name)

    def crop_take(self):
        startF = int(ui.uiObjRef.input1_Edit.text())
        endF = int(ui.uiObjRef.input2_Edit.text())
        if startF >= endF:
            self.change_status("wrong frame range...", "red")
            return

        new_start_time = FBTime()
        new_start_time.SetTimeString(ui.uiObjRef.input1_Edit.text())
        new_end_time = FBTime()
        new_end_time.SetTimeString(ui.uiObjRef.input2_Edit.text())
        
        #set upt new range to copied take
        FBSystem().CurrentTake.LocalTimeSpan = FBTimeSpan(new_start_time, new_end_time)
        print("Cropped take: ", FBSystem().CurrentTake.Name)
        self.change_status("cropped", "green")

    def change_status(self, detailsTxt, color):
        ui.uiObjRef.colorStatus_Txt.setText(detailsTxt)
        ui.uiObjRef.colorStatus_Txt.setStyleSheet(f"color: {color};")


class ToolUI:

    def __init__(self):
        ui.show_tool()
        self.connect_buttons()

    def BtnCallback(self, btn):
        print(f"{btn.objectName()} pressed")
        
        if btn.objectName() == "ShowCopiedTake_Btn":
            print(btn.isChecked())
        elif btn.objectName() == "Start_Btn":
            frameLogic.set_input_field(ui.uiObjRef.input1_Edit, str(frameLogic.get_current_frame()))
            frameLogic.set_deltaFrames_field()
        elif btn.objectName() == "End_Btn":
            frameLogic.set_input_field(ui.uiObjRef.input2_Edit, str(frameLogic.get_current_frame()))
            frameLogic.set_deltaFrames_field()
        elif btn.objectName() == "AutoAssign_Btn":
            print("AutoAssign pressed")
            frameLogic.set_current_time_range_frame(ui.uiObjRef.input1_Edit, ui.uiObjRef.input2_Edit)
            frameLogic.set_deltaFrames_field()
        elif btn.objectName() == "Extreme_Btn":
            frameLogic.go_to_correct_value()
        elif btn.objectName() == "CreateTake_Btn":
            print("CreateTake pressed")
            frameLogic.create_take()
        elif btn.objectName() == "CropTake_Btn":
            print("CropTake pressed")
            frameLogic.crop_take()
        elif btn.objectName() == "GetTakeName_Btn":
            print("GetTakeName_Btn pressed")
            ui.uiObjRef.input3_Edit.setText(FBSystem().CurrentTake.Name)

    def CheckCallback(self, chk):
        print(f"{chk.objectName()} checked: {chk.isChecked()}")

    def connect_buttons(self):
        self.set_button_connections(ui.uiObjRef.start_Btn)
        self.set_button_connections(ui.uiObjRef.end_Btn)
        self.set_button_connections(ui.uiObjRef.autoAssgn_Btn)
        self.set_button_connections(ui.uiObjRef.createTake_Btn)
        self.set_button_connections(ui.uiObjRef.cropTake_Btn)
        self.set_button_connections(ui.uiObjRef.showCopiedTake_Btn)
        self.set_button_connections(ui.uiObjRef.extreme_Btn)
        self.set_button_connections(ui.uiObjRef.getTakeName_Btn)

    def set_button_connections(self, buttonRef):
        try:
            buttonRef.clicked.disconnect()
        except:
            pass
        buttonRef.clicked.connect(lambda: self.BtnCallback(buttonRef))


toolUI = ToolUI()
frameLogic = Framing()
