#CopyDiagonalAnims
#ver. 1.0
from pyfbsdk import *
from pyfbsdk_additions import *

toolName = "Copy Diagonal Anims v"
toolVersion = 1.1
toolFullName = toolName + str(toolVersion)

hikList = FBSystem().Scene.Characters

#lists
diagonal8Sides = ["Front","FL","Left","BL","Back", "BR","Right","FR"]
diagonal4Sides = ["Front","Left","Back", "Right"]
allDiagonalSides = [diagonal8Sides, diagonal4Sides]
choosenDiagonalTab = allDiagonalSides[0]

rotationDeltaTab = [45, 90]

pickedUI4Diag = "+ 4"
pickedUI8Diag = "* 8"
pickedUITab = [pickedUI8Diag, pickedUI4Diag]

global pickedUI
pickedUI = pickedUI8Diag


#get take to fbstory
def get_track():
    global originTakeName, originTake, track
    originTake = FBSystem().CurrentTake
    originTakeName = originTake.Name
    track = FBStoryTrack(FBStoryTrackType.kFBStoryTrackCharacter, FBStory().RootFolder)
    track.Name = "Original" + "_" + str(currentAngle)
    track.Details.append(selectedCharacter)
    track.CopyTakeIntoTrack(originTake.LocalTimeSpan, originTake)

def adjust_track_and_related():
    get_track()
    FBStory().Mute = False

    #get clip & its rotation
    clip = track.Clips[0]
    return clip

def get_rotation_details():
    clip = adjust_track_and_related()
    originalYRotation = clip.Rotation[1]
    rotationOffset = originalYRotation
    #define rotation delta
    if len(choosenDiagonalTab) == 8:
        deltaRotationOffset = rotationDeltaTab[0]
    else:
        deltaRotationOffset = rotationDeltaTab[1]
    return clip, rotationOffset, deltaRotationOffset
    

def rotate_clips():
    clip, rotationOffset, deltaRotationOffset = get_rotation_details()
    tracksToPlot = []
    indexOffset = choosenDiagonalTab.index(currentAngle)
    #create track, add clips, and rotate it
    for i in range(1,len(choosenDiagonalTab)):
        rotationOffset += deltaRotationOffset
        newTrack = FBStoryTrack(FBStoryTrackType.kFBStoryTrackCharacter, FBStory().RootFolder)
        newTrack.Details.append(selectedCharacter)
        tracksToPlot.append(newTrack)
        if indexOffset + i > (len(choosenDiagonalTab) - 1):
            diagonalName = choosenDiagonalTab[indexOffset + i - (len(choosenDiagonalTab))]
        else:
            diagonalName = choosenDiagonalTab[(indexOffset + i)]
        copiedClip = clip.Clone()
        newTrack.Clips.append(copiedClip)
        copiedClip.Rotation = FBVector3d(0, rotationOffset, 0)
        copiedClip.Name = fixedTakeNameTxt.Caption + "_" + str(diagonalName)
        newTrack.Mute = True
    return tracksToPlot


#Plot The Story Clip
def PlotStoryClip():
    lPlotClipOptions = FBPlotOptions()
    lPlotClipOptions.ConstantKeyReducerKeepOneKey = False
    lPlotClipOptions.PlotAllTakes = False
    lPlotClipOptions.PlotOnFrame = True
    lPlotClipOptions.PlotPeriod = FBTime( 0, 0, 0, 1 )
    lPlotClipOptions.PlotTranslationOnRootOnly = False
    lPlotClipOptions.PreciseTimeDiscontinuities = False
    lPlotClipOptions.RotationFilterToApply = FBRotationFilter.kFBRotationFilterUnroll
    lPlotClipOptions.UseConstantKeyReducer = False
    char = selectedCharacter
    char.PlotAnimation (FBCharacterPlotWhere.kFBCharacterPlotOnSkeleton,lPlotClipOptions )               
    char.PlotAnimation(FBCharacterPlotWhere.kFBCharacterPlotOnControlRig,lPlotClipOptions ) 

def plot_rotated_clips_to_new_takes():
    tracksToPlot = rotate_clips()
    track.Mute = True   #mute original track
    #bake it to new takes
    for cTrack in tracksToPlot:
        newtakeName = cTrack.Clips[0].Name
        FBSystem().CurrentTake.CopyTake(newtakeName)
        print(newtakeName)
        cTrack.Mute = False
        #bake curr clip
        PlotStoryClip()
        cTrack.Mute = True
    after_plotting(tracksToPlot)

def after_plotting(deleteTracks):
    FBStory().Mute = True
    FBSystem().CurrentTake = originTake

    #del created tracks:
    track.FBDelete()
    for singleTrack in deleteTracks:
        singleTrack.FBDelete()

def set_all_picked():
    global choosenDiagonalTab, currentAngle, selectedCharacter
    pickedUI = pickedUITab[pickedDiagonalUI.ItemIndex]
    choosenDiagonalTab = allDiagonalSides[pickedDiagonalUI.ItemIndex]
    print("Picked: "+ str(pickedUI))
    print("Diag: "+ str(choosenDiagonalTab))

    hikList = FBSystem().Scene.Characters
    selectedCharacter = hikList[hikListUI.ItemIndex]
    print("Char: " + selectedCharacter.Name)
    currentAngle = choosenDiagonalTab[choosenDiagonalUI.ItemIndex]

def update_take_name():
    slider.Max = len(FBSystem().CurrentTake.Name)
    fixedTakeName = FBSystem().CurrentTake.Name
    sliderTxtRemove = int(slider.Value)
    if sliderTxtRemove != 0:
        fixedTakeName = fixedTakeName[:-sliderTxtRemove]
    fixedTakeNameTxt.Caption = fixedTakeName


def BtnCallback(control, event):
    update_take_name()
    if control.Caption == "Process":
        print("procesed")
        set_all_picked()
        plot_rotated_clips_to_new_takes()
    elif control.Caption == "pickedDiagonalUI":
        refresh_diagonal_list(choosenDiagonalUI, (allDiagonalSides[pickedDiagonalUI.ItemIndex]))
        print("changedPick")
    elif control.Caption == "R":
        refresh_diagonal_list(choosenDiagonalUI, (allDiagonalSides[pickedDiagonalUI.ItemIndex]))
        hikList = FBSystem().Scene.Characters
        refresh_diagonal_list(hikListUI, hikList)
        print("R")
    elif control.Caption == "Slider":
        print(control.Value)


def refresh_diagonal_list(listUI, list):
    listUI.Items.removeAll()
    for item in list:
        if isinstance(item, str):
            listUI.Items.append(item)
        else:
            listUI.Items.append(item.Name)

def CreateButton(caption):
    button = FBButton()
    button.Caption = str(caption)
    button.Justify = FBTextJustify.kFBTextJustifyCenter
    button.OnClick.Add(BtnCallback)
    return button

def CreateText(text):
    emptySpace = FBLabel()
    emptySpace.Caption = text
    return emptySpace

def CreateLine(name, height, mainLyt):
    x = FBAddRegionParam(0,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(height,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    mainLyt.AddRegion(name, name, x, y, w, h)
    lyt = FBHBoxLayout()
    mainLyt.SetControl(name,lyt)
    return lyt

def CreateList(caption):
    textInput = FBList()
    textInput.Caption = caption
    textInput.OnChange.Add(BtnCallback)
    return textInput
  
    
def PopulateLayout_Stage3(mainLyt):

    #txt input:
    lyt = CreateLine("firstRow", 10, mainLyt)

    global choosenDiagonalUI
    choosenDiagonalUI = CreateList("choosenDiagonalUI")
    refresh_diagonal_list(choosenDiagonalUI, choosenDiagonalTab)
    lyt.Add(choosenDiagonalUI, 60)

    space = CreateText("")
    lyt.Add(space, 5)

    global hikListUI
    hikListUI = CreateList("hikListUI")
    refresh_diagonal_list(hikListUI, hikList)
    lyt.Add(hikListUI, 100)
    

    lyt = CreateLine("secondRow", 40, mainLyt)
    
    global pickedDiagonalUI
    pickedDiagonalUI = CreateList("pickedDiagonalUI")
    for pickedDiag in pickedUITab:
        pickedDiagonalUI.Items.append(pickedDiag)
    lyt.Add(pickedDiagonalUI, 60)

    space = CreateText("")
    lyt.Add(space, 10)
    
    createBtn = CreateButton("Process")
    lyt.Add(createBtn,90)

    space = CreateText("")
    lyt.Add(space, 5)

    createBtn = CreateButton("R")
    lyt.Add(createBtn,25)

    lyt = CreateLine("thirdRow", 70, mainLyt)

    global fixedTakeNameTxt
    fixedTakeNameTxt = CreateText(FBSystem().CurrentTake.Name)
    lyt.Add(fixedTakeNameTxt, 70)
    
    space = CreateText("")
    lyt.Add(space, 10)
    txtSample = CreateText("Set prefix")
    lyt.Add(txtSample, 50)
    space = CreateText("")
    lyt.Add(space, 5)

    global slider
    slider = FBEditNumber()
    slider.Caption = "Slider"
    slider.Min = 0  
    slider.Max = 10
    slider.SmallStep = 1
    slider.Precision = 1
    slider.OnChange.Add(BtnCallback)
    lyt.Add(slider, 30)

def CreateUI():
    global toolFullName
    t = FBCreateUniqueTool(toolFullName)
    t.StartSizeX = 230
    t.StartSizeY = 125
    PopulateLayout_Stage3(t)
    ShowTool(t)
    
CreateUI()