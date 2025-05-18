#change model to wireframe
#cube.ShadingMode = FBModelShadingMode.kFBModelShadingAll
#cube.ShadingMode = FBModelShadingMode.kFBModelShadingWire
#cube.Show = True

from pyfbsdk import *
from pyfbsdk_additions import * 
import sys
sys.path.append("..")
#from DeltaCorrect import *
#import Setter

toolName = "Prop Handler Tool  v"
toolVersion = 0.1
toolFullName = toolName + str(toolVersion)

class PickedObjects:
    mocapWrist = FBFindModelByLabelName("RightFingerBase")
    mocapProp = FBFindModelByLabelName("Mocap_Prop")

    retWrist = FBFindModelByLabelName("Aragor:RightHand")
    retProp = FBFindModelByLabelName("Test_Offset")

    propRoot = FBFindModelByLabelName("rootProp")

def assign_prop_mocap(isWireFrameOn):
    PickedObjects.propRoot.Parent = PickedObjects.mocapProp
    PickedObjects.propRoot
    set_prop_visibility()
    
    #offset prop to fit mocap char
def set_prop_visibility(isWireFrameOn):
    if isWireFrameOn:
        PickedObjects.propRoot.Children[0].ShadingMode = FBModelShadingMode.kFBModelShadingWire
    else:
        PickedObjects.propRoot.Children[0].ShadingMode = FBModelShadingMode.kFBModelShadingAll
def create_retarget_markers(propname):
    propMaker = FBModelMarker("Re_" + str(propname))
    propMaker.Show = True
    propMaker.MarkerSize = 200
    propMaker.Color = FBColor(0.9, 1, 0)
    propMaker.Look = FBMarkerLook.kFBMarkerLookLightCross
    

    propOffsetMaker = FBModelMarker("Re_Offset_" + str(propname))
    propOffsetMaker.Show = True
    propOffsetMaker.MarkerSize = 400
    propOffsetMaker.Color = FBColor(1, 0, 0.9)
    propOffsetMaker.Look = FBMarkerLook.kFBMarkerLookCircle
    

    propOffsetMaker.Parent = propMaker
    propMaker.Parent = PickedObjects.retWrist

    propMaker.Translation = FBVector3d(0,0,0)
    propMaker.Rotation = FBVector3d(0,0,0)

### testing funcs:
#assign_prop_mocap(True)
#create_retarget_markers("toDELETE")


def BtnCallback(control, event):
    if control.Caption == "R":
        print("R")
        CreateSetterUI()
        print(PickedObjects.mocapWrist.Name)

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
    t.StartSizeX = 250
    t.StartSizeY = 400
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


