#change model to wireframe
#cube.ShadingMode = FBModelShadingMode.kFBModelShadingAll
#cube.ShadingMode = FBModelShadingMode.kFBModelShadingWire
#cube.Show = True

from pyfbsdk import *
from pyfbsdk_additions import * 
#from  DeltaCorrect import apply_corrections

toolName = "Prop Handler Tool  v"
toolVersion = 0.1
toolFullName = toolName + str(toolVersion)

wrist1 = FBFindModelByLabelName("RightFingerBase")
prop1 = FBFindModelByLabelName("Mocap_Prop")

wrist2 = FBFindModelByLabelName("Aragor:RightHand")
prop2 = FBFindModelByLabelName("Test_Offset")

def BtnCallback(control, event):
    if control.Caption == "R":
        print("R")
        CreateSetterUI()

def SetupPropertyList(model):
    global container
    container.Items.removeAll()
    list.Items.removeAll()
    prop_list = []
    
    model = model
    
    if model:
        container.Items.append(model.Name)
        list.Items.append("<Select Property>")
        prop_list.append(None)
        for p in model.PropertyList:
            if p and p.IsInternal() and not p.GetPropertyFlag(FBPropertyFlag.kFBPropertyFlagHideProperty):
                list.Items.append(p.Name)
                prop_list.append(p)
        list.ItemIndex = 0

def EventContainerDblClick(control, event):
    SetupPropertyList(None)
    
def EventContainerDragAndDrop(control, event):
    if event.State == FBDragAndDropState.kFBDragAndDropDrag:
        event.Accept()
    elif event.State == FBDragAndDropState.kFBDragAndDropDrop:
        SetupPropertyList( event.Components[0] )



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
  

def PopulateLayout_Stage_Main(mainLyt):

    #txt input:
    lyt = CreateLine("firstRow", 10, mainLyt)

    createBtn = CreateButton("R")
    lyt.Add(createBtn,25)

def CreateMainUI():
    global toolFullName
    t = FBCreateUniqueTool(toolFullName)
    t.StartSizeX = 230
    t.StartSizeY = 125
    PopulateLayout_Stage_Main(t)
    ShowTool(t)


def PopulateLayout_Stage_Sett(mainLyt):

    #txt input:
    lyt = CreateLine("firstRow", 10, mainLyt)

    container = FBVisualContainer()
    container.OnDragAndDrop.Add(EventContainerDragAndDrop)
    container.OnDblClick.Add(EventContainerDblClick)
    lyt.Add(container, 100)

def CreateSetterUI():
    t = FBCreateUniqueTool("Set Objects")
    t.StartSizeX = 150
    t.StartSizeY = 75
    PopulateLayout_Stage_Sett(t)
    ShowTool(t)


CreateMainUI()
CreateSetterUI()

