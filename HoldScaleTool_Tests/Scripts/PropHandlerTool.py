import os
import sys

# Add the current script directory to sys.path
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)

from pyfbsdk import *
from pyfbsdk_additions import * 
#from DeltaCorrect import apply_corrections
from Setter import CreateSetterUI
from relation_constraint_configure import create_relation, relationObjs


toolName = "Prop Handler Tool  v"
toolVersion = 0.1
toolFullName = toolName + str(toolVersion)
defNamespace = "ProH:"

class PickedObjects:
    #to be assigned
    mocapProp = None
    propRootBone = None
    mocapCharBone = None
    charBone =  None

    #to be created
    propSource = None
    propOffsetMaker = None
    mocapPropRootClone = None

userObjs = PickedObjects()
def assign_prop_mocap(isWireFrameOn):
    if _are_mocap_objs_set():
        newPropRig = duplicate_rig_model(userObjs.propRootBone, defNamespace, None)
        #FIX: check if the name is in mocapProp.Children
        if newPropRig in userObjs.mocapProp.Children:
            print("Prop IS already assigned to mocap")
        else:
            newPropRig.Parent = userObjs.mocapProp
            newPropRig.Translation = FBVector3d(0,0,0)
            newPropRig.Rotation = FBVector3d(0,0,0)
            userObjs.mocapPropRootClone = newPropRig
            userObjs.mocapProp = userObjs.mocapPropRootClone
            print("Made it :-)")
            
        set_prop_visibility(isWireFrameOn)
    else:
        print("Assign objects first!")

def set_prop_visibility(isWireFrameOn):
    if userObjs.mocapProp.Children[0]:
        if isWireFrameOn:
            userObjs.mocapProp.Children[0].ShadingMode = FBModelShadingMode.kFBModelShadingWire
        else:
            userObjs.mocapProp.Children[0].ShadingMode = FBModelShadingMode.kFBModelShadingAll

def create_retarget_markers(propname):
    propSource = FBModelMarker(defNamespace + str(propname))
    propSource.Show = True
    propSource.MarkerSize = 200
    propSource.Color = FBColor(1, 0.5, 0)
    propSource.Look = FBMarkerLook.kFBMarkerLookLightCross

    propOffsetMaker = FBModelMarker(defNamespace + "Offset_" + str(propname))
    propOffsetMaker.Show = True
    propOffsetMaker.MarkerSize = 400
    propOffsetMaker.Color = FBColor(1, 1, 0)
    propOffsetMaker.Look = FBMarkerLook.kFBMarkerLookCircle
    
    userObjs.propSource = propSource
    userObjs.propOffsetMaker = propOffsetMaker

    propOffsetMaker.Parent = propSource
    #propSource.Parent = userObjs.charBone

    propSource.Translation = FBVector3d(0,0,0)
    propSource.Rotation = FBVector3d(0,0,0)
    send_objects_to_relation_constraint()


def _are_mocap_objs_set():
    if userObjs.mocapProp is not None and userObjs.propRootBone is not None :
        return True
    return False

def send_objects_to_relation_constraint():
    relationObjs.mocapPropName = userObjs.mocapProp.LongName
    relationObjs.retPropBoneName = userObjs.propRootBone.LongName
    relationObjs.retPropSourceName = userObjs.propSource.LongName
    relationObjs.retOffsetName = userObjs.propOffsetMaker.LongName
    relationObjs.mocapCharBoneName = userObjs.mocapCharBone.LongName
    relationObjs.charBoneName = userObjs.charBone.LongName

def create_relation_constraint():
    create_retarget_markers(inputPropName.Caption)
    create_relation()
    
def BtnCallback(control, event):
    if control.Caption == "Set Objects":
        CreateSetterUI()
        #Setter.CreateTool()
    elif control.Caption == "Set Mocap":
        print("assigning mocap...")
        assign_prop_mocap(wireFrameBtn.State)
    elif control.Caption == "Prop Vis":
        set_prop_visibility(wireFrameBtn.State)
    elif control.Caption == "Retarget":
        create_relation_constraint()

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
    x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"")
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
    lyt = CreateLine("firstRow", 20, mainLyt)

    createBtn = CreateButton("Set Objects")
    lyt.Add(createBtn,115)

    lyt = CreateLine("secondRow", 55, mainLyt)

    createBtn = CreateButton("Set Mocap")
    lyt.Add(createBtn,115)

    global wireFrameBtn
    wireFrameBtn = CreateButton("Prop Vis")
    wireFrameBtn.Style = FBButtonStyle.kFB2States
    wireFrameBtn.Look = FBButtonLook.kFBLookColorChange
    wireFrameBtn.SetStateColor(FBButtonState.kFBButtonState0,FBColor(0.6, 0.4, 0.4))
    lyt.Add(wireFrameBtn,75)


    lyt = CreateLine("thirdRow", 90, mainLyt)

    createBtn = CreateButton("Retarget")
    lyt.Add(createBtn,115)

    global inputPropName
    inputPropName = FBEdit()
    inputPropName.Caption = ""
    lyt.Add(inputPropName, 75)

    lyt = CreateLine("fourthRow", 125, mainLyt)

    dotCorrectionBtn = CreateButton("DOT Correct")
    dotCorrectionBtn.Style = FBButtonStyle.kFB2States
    dotCorrectionBtn.Look = FBButtonLook.kFBLookColorChange
    dotCorrectionBtn.SetStateColor(FBButtonState.kFBButtonState0,FBColor(1.0, 0.0, 0.0))
    dotCorrectionBtn.SetStateColor(FBButtonState.kFBButtonState1,FBColor(0.0, 0.0, 1.0))
    lyt.Add(dotCorrectionBtn,115)

    lyt = CreateLine("lastRow", 155, mainLyt)
    space = CreateText(" ")
    lyt.Add(space, 10)
    lastTaskText = CreateText("NOW do offset")
    lyt.Add(lastTaskText, 120)

def CreateMainUI():
    global toolFullName
    t = FBCreateUniqueTool(toolFullName)
    t.StartSizeX = 250
    t.StartSizeY = 400
    PopulateLayout_Stage_Main(t)
    ShowTool(t)

CreateMainUI()


def duplicate_rig_model(source_model, specifiedNamespace, parent=None):
    # Clone the current model
    clone = source_model.Clone()
    if specifiedNamespace:
        clone.LongName = str(specifiedNamespace) + clone.Name
    
    # Set the parent if specified
    if parent:
        clone.Parent = parent

    # Recursively clone all children
    for child in source_model.Children:
        duplicate_rig_model(child, specifiedNamespace, clone)

    return clone