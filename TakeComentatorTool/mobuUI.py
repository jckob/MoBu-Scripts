from  pyfbsdk import FBEdit, FBList, FBButton, FBLabel, FBTextJustify, FBAttachType, ShowTool, FBAddRegionParam, FBButtonStyle
from pyfbsdk_additions import  FBHBoxLayout, FBCreateUniqueTool

toolFullName = "Take Commentator Tool"


class UIObjects():
    inputSheetName = FBEdit()
    inputKeyNameList = FBList()
    inputValueNameList = FBList()
    connectBtn = FBButton() 
    checkInputs = FBButton()
    checkBoxAllBtn = FBButton()
    updateBtn = FBButton()  

def CreateButton(caption):
    button = FBButton()
    button.Caption = str(caption)
    button.Justify = FBTextJustify.kFBTextJustifyCenter
    
    return button

def CreateText(text):
    emptySpace = FBLabel()
    emptySpace.Caption = text
    emptySpace.Justify = FBTextJustify.kFBTextJustifyCenter
    return emptySpace

def CreateInput(text):
    inputTxt = FBEdit()
    if text:
        inputTxt.Text = text
    return inputTxt

def CreateList(caption):
    list = FBList()
    list.Caption = caption

    return list
  

def CreateLine(name, height, x, mainLyt):
    x = FBAddRegionParam(x,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(height,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    mainLyt.AddRegion(name, name, x, y, w, h)
    lyt = FBHBoxLayout()
    mainLyt.SetControl(name,lyt)
    return lyt


def PopulateLayout_Stage_Main(mainLyt):
    lyt = CreateLine("namingLine1", 10, 10, mainLyt)

    name1Txt = CreateText("sheet Name")
    lyt.Add(name1Txt,80)

    name2Txt = CreateText("anim column")
    lyt.Add(name2Txt,80)

    name3Txt = CreateText("status column")
    lyt.Add(name3Txt,85)

    lyt = CreateLine("namingLine2", 35, 10, mainLyt)

    inputSheetName = CreateInput("Summary")
    uiObjRef.inputSheetName = inputSheetName
    lyt.Add(inputSheetName,80)

    inputKeyNameList = CreateList("AnimName")
    uiObjRef.inputKeyNameList = inputKeyNameList
    lyt.Add(inputKeyNameList,80)

    inputValueNameList = CreateList("Status")
    uiObjRef.inputValueNameList = inputValueNameList
    lyt.Add(inputValueNameList,80)

    space = CreateText(" ")
    lyt.Add(space, 10)

    checkInputs = CreateButton("CheckInputs")
    uiObjRef.checkInputs = checkInputs
    lyt.Add(checkInputs, 80)

    lyt = CreateLine("lastLine", 75, 10, mainLyt)

    space = CreateText(" ")
    lyt.Add(space, 10)

    checkBoxAllBtn = CreateButton("CheckAllTakes")
    checkBoxAllBtn.Style = FBButtonStyle.kFBCheckbox
    uiObjRef.checkBoxAllBtn = checkBoxAllBtn
    lyt.Add(checkBoxAllBtn, 100)

    updateBtn = CreateButton("Update")
    uiObjRef.updateBtn = updateBtn
    lyt.Add(updateBtn, 120)


def CreateTool():
    global toolFullName
    t = FBCreateUniqueTool(toolFullName)
    t.StartSizeX = 380  
    t.StartSizeY = 140
    PopulateLayout_Stage_Main(t)
    ShowTool(t)


uiObjRef = UIObjects()
#CreateTool()
