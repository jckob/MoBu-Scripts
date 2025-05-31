import os
import sys

# Add the current script directory to sys.path
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)

from pyfbsdk import *
from pyfbsdk_additions import * 
#from DeltaCorrect import apply_corrections
from Setter import AssigneObjects, CreateSetterUI
from relation_constraint_configure import create_relation, RelationConstraintObjConfig


toolName = "Prop Handler Tool  v"
toolVersion = 0.1
toolFullName = toolName + str(toolVersion)
defNamespace = "ProH:"

class PickedObjects:
    mocapProp = FBFindModelByLabelName("Mocap_Prop")

    propRootBone = FBFindModelByLabelName("Root_Prop")

    mocapCharBone = FBFindModelByLabelName("RightFingerBase")
    charBone = FBFindObjectByFullName("Aragor:RightHand")

    #to create
    propSource = None
    propOffsetMaker = None
    mocapPropRootClone = None

def assign_prop_mocap(isWireFrameOn):
    #LATTTEEEEEEEEEEEEEEEEEER
    #check if namespace is already assigned
    
    newPropRig = duplicate_rig_model(PickedObjects.propRootBone, defNamespace, None)
    #FIX: check if the name is in mocapProp.Children
    if newPropRig in PickedObjects.mocapProp.Children:
        print("Prop IS already assigned to mocap")
    else:
        newPropRig.Parent = PickedObjects.mocapProp
        newPropRig.Translation = FBVector3d(0,0,0)
        newPropRig.Rotation = FBVector3d(0,0,0)
        PickedObjects.mocapPropRootClone = newPropRig
        PickedObjects.mocapProp = PickedObjects.mocapPropRootClone
        
    set_prop_visibility(isWireFrameOn)


def set_prop_visibility(isWireFrameOn):
    if PickedObjects.mocapProp.Children[0]:
        if isWireFrameOn:
            PickedObjects.mocapProp.Children[0].ShadingMode = FBModelShadingMode.kFBModelShadingWire
        else:
            PickedObjects.mocapProp.Children[0].ShadingMode = FBModelShadingMode.kFBModelShadingAll

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
    
    PickedObjects.propSource = propSource
    PickedObjects.propOffsetMaker = propOffsetMaker

    propOffsetMaker.Parent = propSource
    #propSource.Parent = PickedObjects.charBone

    propSource.Translation = FBVector3d(0,0,0)
    propSource.Rotation = FBVector3d(0,0,0)
    send_objects_to_relation_constraint()


def send_objects_to_relation_constraint():
    RelationConstraintObjConfig.mocapPropName = PickedObjects.mocapProp.LongName
    RelationConstraintObjConfig.retPropBoneName = PickedObjects.propRootBone.LongName
    RelationConstraintObjConfig.retPropSourceName = PickedObjects.propSource.LongName
    RelationConstraintObjConfig.retOffsetName = PickedObjects.propOffsetMaker.LongName
    RelationConstraintObjConfig.mocapCharBoneName = PickedObjects.mocapCharBone.LongName
    RelationConstraintObjConfig.charBoneName = PickedObjects.charBone.LongName

def create_relation_constraint():
    create_retarget_markers("Sword1")
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