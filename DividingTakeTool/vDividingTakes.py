#V_1.5
#script by
# #  ###
##    #
# #  ###

from pyfbsdk import FBSystem, FBTime, FBTimeSpan, FBPlayerControl, ShowTool
from pyfbsdk_additions import FBCreateUniqueTool

toolName = "Take Tool v"
toolVersion = 2.0
toolCategory = "vanilla"
toolFullName = toolName + str(toolVersion) + " " + toolCategory

start_time = None
end_time = None

global isStart
isStart = False
change_to_copied_take = False


# Button creation
def BtnCallback(control, event):
    global start_time, end_time, change_to_copied_take
    start_time = 5
    if control.Caption == "Start":
        current_frame = FBSystem().LocalTime.GetFrame()
        
        input1.Text = str(current_frame)
        start_time = int(input1.Text)
        #change status label
        change_status_color("doing")

    elif control.Caption == "End":   
        current_frame = FBSystem().LocalTime.GetFrame()
        
        input2.Text = str(current_frame)
        end_time = int(input2.Text)
        #change status label
        change_status_color("doing")
    elif control.Caption == "Auto Assign":
        #try fames, except timecode
        try:
            set_current_time_range_frame(input1, input2)
            start_time = int(input1.Text)
            end_time = int(input2.Text)
        except ValueError:
            set_current_time_range_frame(input1, input2)
            start_time = change_timecode_to_int(input1)
            end_time = change_timecode_to_int(input2)
        #change status label
        change_status_color("doing")
        
    elif control.Caption == "[x]":
        print("frame[x]")
        set_correct_slider_value()
        change_status_color("doing")
        FBSystem().Scene.Evaluate()
        
    elif control.Caption == "Show Copied Take":
        change_to_copied_take = not change_to_copied_take
        #change status label
        change_status_color("doing")
        
    elif control.Caption == "Crop Take":
        change_status_color("cropped")
        try:
            #frames case
            newStartFrame = int(input1.Text)
            newEndFrame = int(input2.Text)
            if(newEndFrame>newStartFrame):
                #set upt new range to copied take
                FBSystem().CurrentTake.LocalTimeSpan = FBTimeSpan(FBTime(0, 0, 0, newStartFrame), FBTime(0, 0, 0, newEndFrame))
                FBSystem().CurrentTake.Name = get_take_name(True)
            else:
                change_status_color("wrongFrames")
        except ValueError:
            #timecode case
            #
            newStartTimecode = input1.Text
            newEndTimecode = input2.Text
            
            # timecode to FBTime
            new_start_time = FBTime()
            new_start_time.SetTimeString(newStartTimecode)
        
            new_end_time = FBTime()
            new_end_time.SetTimeString(newEndTimecode)
            
            #set upt new range to copied take
            FBSystem().CurrentTake.LocalTimeSpan = FBTimeSpan(new_start_time, new_end_time)
            FBSystem().CurrentTake.Name = get_take_name(True)

        FBSystem().Scene.Evaluate()
        
    elif control.Caption == "Create Take":
        global newTakeName
        #set up vars about take
        originalTakeName = get_current_take_name()  #orignal take Name
        newTakeName = get_take_name(False)

        try:
            #frames case
            newStartFrame = int(input1.Text)
            newEndFrame = int(input2.Text)
            if(newEndFrame>newStartFrame):
                #copy take
                newTake = FBSystem().CurrentTake.CopyTake(newTakeName)
                #set upt new range to copied take
                newTake.LocalTimeSpan = FBTimeSpan(FBTime(0, 0, 0, newStartFrame), FBTime(0, 0, 0, newEndFrame))
            else:
                change_status_color("wrongFrames")
                return
        except ValueError:
            #timecode case
            #
            #copy take
            newTake = FBSystem().CurrentTake.CopyTake(newTakeName)
            newStartTimecode = input1.Text
            newEndTimecode = input2.Text
        
            # timecode to FBTime
            new_start_time = FBTime()
            new_start_time.SetTimeString(newStartTimecode)
        
            new_end_time = FBTime()
            new_end_time.SetTimeString(newEndTimecode)
            
            #set upt new range to copied take
            newTake.LocalTimeSpan = FBTimeSpan(new_start_time, new_end_time)

        #check bool to change take in scene to copied take
        if change_to_copied_take == False:
            FBSystem().CurrentTake = originalTakeName
        
        change_status_color("copied")
        FBSystem().Scene.Evaluate()
    
    framesDeltaTxt.Caption = calculate_diff_frames()

def calculate_diff_frames():
    resultInt = int(input2.Text) - int(input1.Text)
    return str(resultInt)
    
def get_current_frame():
    t = FBSystem().LocalTime
    return t.GetFrame()   
    
def get_correct_time_code(start, end, current):
    global isStart
    if current != start and current != end:
        correctTime = FBTime(0, 0, 0, start, 0)
        isStart = True
    else:
        if isStart:
            correctTime = FBTime(0, 0, 0, end, 0)
        else:
            correctTime = FBTime(0, 0, 0, start, 0)
    
        isStart = not isStart
    return correctTime

def set_correct_slider_value():
    startF = int(input1.Text)
    endF = int(input2.Text)
    currentFrame = FBSystem().LocalTime.GetFrame()
    
    t = get_correct_time_code(startF, endF, currentFrame)
    FBPlayerControl().Goto(t)            

def get_current_take_name():
    currentTakeName = FBSystem().CurrentTake
    return currentTakeName


def get_take_name(isCropping):
    currentTakeName = FBSystem().CurrentTake.Name
    if input3.Text:
        newName = input3.Text
    else:
        if isCropping:
            newName = currentTakeName
        else:
            newName = currentTakeName + "_Copy"
    return newName


def change_take_on_scene(take_name):
    FBSystem().CurrentTake = take_name


def change_timecode_to_int(input_text):
    timecode_text = input_text.Text

    timecode = FBTime()
    timecode.SetTimeString(timecode_text)

    frames = timecode.GetFrame()
    return frames

def set_current_time_range_frame(firstInput, secondInput):
    view_start_frame = FBSystem().CurrentTake.LocalTimeSpan.GetStart()
    view_stop_frame = FBSystem().CurrentTake.LocalTimeSpan.GetStop()
    firstInput.Text = view_start_frame.GetTimeString()
    secondInput.Text = view_stop_frame.GetTimeString()
    try:
        start_time = view_start_frame
        end_time = view_stop_frame
    except ValueError:
        print("error")
        start_time = change_timecode_to_int(view_start_frame)
        end_time = change_timecode_to_int(view_stop_frame)
   
def change_status_color(strProgress):
    #add color change, HOW
    #greenColor = FBColorAndAlpha(0.0, 1.0, 0.0, 1.0)
    if strProgress == "copied":
        color_status.Caption = ("Copied: " + newTakeName)
    elif strProgress == "error":
       color_status.Caption = ("Failed to copy...:")
    elif strProgress == "doing":
        color_status.Caption = ("doing...")
    elif strProgress == "cropped":
        color_status.Caption = ("cropped...")
    elif strProgress == "wrongFrames":
        color_status.Caption = ("wrong frame range")
    
    

def PopulateLayout(mainLyt):
    x = FBAddRegionParam(0, FBAttachType.kFBAttachLeft, "")
    y = FBAddRegionParam(10, FBAttachType.kFBAttachTop, "")
    w = FBAddRegionParam(0, FBAttachType.kFBAttachRight, "")
    h = FBAddRegionParam(25, FBAttachType.kFBAttachNone, "")
    mainLyt.AddRegion("top_buttons", "top_buttons", x, y, w, h)
    lyt = FBHBoxLayout()
    mainLyt.SetControl("top_buttons", lyt)
    
    
    
    x = FBAddRegionParam(0, FBAttachType.kFBAttachLeft, "")
    y = FBAddRegionParam(15, FBAttachType.kFBAttachTop, "")
    w = FBAddRegionParam(0, FBAttachType.kFBAttachRight, "")
    h = FBAddRegionParam(25, FBAttachType.kFBAttachNone, "")
    mainLyt.AddRegion("top_buttons", "top_buttons", x, y, w, h)
    lyt = FBHBoxLayout()
    mainLyt.SetControl("top_buttons", lyt)

    b = FBButton()
    b.Caption = "Start"
    b.Justify = FBTextJustify.kFBTextJustifyCenter
    lyt.Add(b, 80)
    b.OnClick.Add(BtnCallback)

    b = FBLabel()
    b.Caption = ""
    lyt.Add(b, 20)

    b = FBButton()
    b.Caption = "End"
    b.Justify = FBTextJustify.kFBTextJustifyCenter
    lyt.Add(b, 80)
    b.OnClick.Add(BtnCallback)

    # empy label to center others xd
    empty_label = FBLabel()
    empty_label.Caption = ""
    lyt.Add(empty_label, 5)
    
    b = FBButton()
    b.Caption = "Auto Assign"
    b.Style = FBButtonStyle.kFBPushButton
    b.Justify = FBTextJustify.kFBTextJustifyCenter
    lyt.Add(b, 90)
    b.OnClick.Add(BtnCallback)

    x = FBAddRegionParam(0, FBAttachType.kFBAttachLeft, "")
    y = FBAddRegionParam(40, FBAttachType.kFBAttachTop, "")
    w = FBAddRegionParam(0, FBAttachType.kFBAttachRight, "")
    h = FBAddRegionParam(25, FBAttachType.kFBAttachNone, "")
    mainLyt.AddRegion("text_inputs", "text_inputs", x, y, w, h)
    lyt = FBHBoxLayout()
    mainLyt.SetControl("text_inputs", lyt)

    global input1, input2, input3 
    input1 = FBEdit()
    input2 = FBEdit()
    set_current_time_range_frame(input1, input2)
    input3 = FBEdit()
    
    xF = FBButton()
    xF.Caption = "[x]"
    xF.Justify = FBTextJustify.kFBTextJustifyCenter
    xF.OnClick.Add(BtnCallback)
    

    lyt.Add(input1, 80)
    lyt.Add(xF, 20)
    lyt.Add(input2, 80)
    
    space = FBLabel()
    space.Caption = ""
    lyt.Add(space, 5)
    
    
    diffFramesText = FBLabel()
    diffFramesText.Caption = "Clip Length:"
    xF.Justify = FBTextJustify.kFBTextJustifyCenter
    lyt.Add(diffFramesText, 60)
    
    global framesDeltaTxt
    framesDeltaTxt = FBLabel()
    framesDeltaTxt.Caption = "lol"
    xF.Justify = FBTextJustify.kFBTextJustifyCenter
    lyt.Add(framesDeltaTxt, 80)
    framesDeltaTxt.Caption = calculate_diff_frames()

    x = FBAddRegionParam(0, FBAttachType.kFBAttachLeft, "")
    y = FBAddRegionParam(80, FBAttachType.kFBAttachTop, "")
    w = FBAddRegionParam(0, FBAttachType.kFBAttachRight, "")
    h = FBAddRegionParam(25, FBAttachType.kFBAttachNone, "")
    mainLyt.AddRegion("bottom_button", "bottom_button", x, y, w, h)
    lyt = FBHBoxLayout()
    mainLyt.SetControl("bottom_button", lyt)

    b = FBButton()
    b.Caption = "Create Take"
    b.Justify = FBTextJustify.kFBTextJustifyCenter
    lyt.Add(b, 120)
    b.OnClick.Add(BtnCallback)
    
    b = FBLabel()
    b.Caption = ""
    lyt.Add(b,10)
    
    lyt.Add(input3, 120)
    
    x = FBAddRegionParam(20, FBAttachType.kFBAttachLeft, "")
    y = FBAddRegionParam(110, FBAttachType.kFBAttachTop, "")
    w = FBAddRegionParam(0, FBAttachType.kFBAttachRight, "")
    h = FBAddRegionParam(25, FBAttachType.kFBAttachNone, "")
    mainLyt.AddRegion("lower_line", "lower_line", x, y, w, h)
    lyt = FBHBoxLayout()
    mainLyt.SetControl("lower_line", lyt)
    
    b = FBButton()
    b.Caption = "Crop Take"
    b.Justify = FBTextJustify.kFBTextJustifyCenter
    lyt.Add(b, 85)
    b.OnClick.Add(BtnCallback)
    
    b = FBLabel()
    b.Caption = ""
    lyt.Add(b,15)
    
    b = FBButton()
    b.Caption = "Show Copied Take"
    b.Style = FBButtonStyle.kFBCheckbox 
    b.Justify = FBTextJustify.kFBTextJustifyCenter
    lyt.Add(b, 150)
    b.OnClick.Add(BtnCallback)
    
    x = FBAddRegionParam(35, FBAttachType.kFBAttachLeft, "")
    y = FBAddRegionParam(135, FBAttachType.kFBAttachTop, "")
    w = FBAddRegionParam(0, FBAttachType.kFBAttachRight, "")
    h = FBAddRegionParam(25, FBAttachType.kFBAttachNone, "")
    mainLyt.AddRegion("text_status", "text_status", x, y, w, h)
    lyt = FBHBoxLayout()
    mainLyt.SetControl("text_status", lyt)

    global color_status
    color_status = FBLabel()
    color_status.Caption = "Status..."
    color_status.Justify = FBTextJustify.kFBTextJustifyCenter
    lyt.Add(color_status, 160)

def CreateTool():
    global toolFullName
    t = FBCreateUniqueTool(toolFullName)
    t.StartSizeX = 310
    t.StartSizeY = 185
    PopulateLayout(t)
    ShowTool(t)



CreateTool()