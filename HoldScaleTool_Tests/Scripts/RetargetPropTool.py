import os
import sys

# Add the current script directory to sys.path
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)

from pyfbsdk import *
from pyfbsdk_additions import * 
from relation_constraint_configure import create_relation, relationObjs


toolName = "Retarget Prop Tool  v"
toolVersion = 0.3
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

class UILockObjs():
    input1 = None
    input2 = None
    input3 = None
    input4 = None

    locker1 = None
    locker2 = None
    locker3 = None
    locker4 = None

    visibilityBtn = None

    lockImage  = str(script_dir + "/Locked_Image.png")
    unlockImage = str(script_dir + "/unLocked_Image.png")

    def match_id_to_containerClass(self, obj_Indx, objSource):
        match int(obj_Indx):
            case 1:
                userObjs.mocapProp = objSource
            case 2:
                userObjs.propRootBone = objSource
            case 3:
                userObjs.mocapCharBone = objSource
            case 4:
                userObjs.charBone = objSource


    def manage_obj_locking(self, obj_Indx):
        inputUI = getattr(self, f"input{obj_Indx}")
        self.set_obj_as_picked(obj_Indx, str(inputUI.Text))

    def set_obj_as_picked(self, obj_Indx, obj_Name ):
        try:
            foundObj = FBFindModelByLabelName(obj_Name)
        except:
            foundObj = None

        if not foundObj:
            self.change_checkBox_to_failed(obj_Indx)
            print("None")

        self.match_id_to_containerClass(obj_Indx, foundObj)

    def change_checkBox_to_failed(self, object_RowPlaced):
        locker = getattr(self, f"locker{object_RowPlaced}")
        locker.State = False

    def check_is_locked(self, obj_Indx):
        locker = getattr(uiLockers, f"locker{obj_Indx}")
        if locker.State:
            self.manage_obj_locking(obj_Indx)
        else:
            self.on_edit_input(obj_Indx)
        
    def on_edit_input(self, obj_Indx):
        self.change_checkBox_to_failed(obj_Indx)
        self.match_id_to_containerClass(obj_Indx, None)
            
class StatusTxtObj():
    row1Info = None
    row2Info = None


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
        set_prop_visibility(userObjs.mocapProp.Children[0].ShadingMode == FBModelShadingMode.kFBModelShadingWire)
    else:
        print("2 first objs are not set")
        
def set_prop_visibility(isWireFrameOn):
    try:
        if userObjs.mocapProp.Children[0]:
            if not isWireFrameOn:
                userObjs.mocapProp.Children[0].ShadingMode = FBModelShadingMode.kFBModelShadingWire
            else:
                userObjs.mocapProp.Children[0].ShadingMode = FBModelShadingMode.kFBModelShadingAll
    except:
        uiLockers.visibilityBtn.State = 0
            

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

def _are_mocap_objs_set():
    if uiLockers.locker1.State & uiLockers.locker2.State: 
        if userObjs.mocapProp is not None and userObjs.propRootBone is not None :
            return True
    return False

def _are_hands_objs_set():
    if userObjs.mocapCharBone is not None and userObjs.charBone is not None :
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
    if _are_hands_objs_set():
        create_retarget_markers(inputPropName.Caption)
        send_objects_to_relation_constraint()
        create_relation()
    else:
        print("no hands set in")
    
def BtnCallback(control, event):
    if control.Caption == "Set Objects":
        #CreateSetterUI()
        print("createUI")
    elif control.Caption == "Set Mocap":
        print("assigning mocap...")
        assign_prop_mocap(wireFrameBtn.State)
    elif control.Caption == "Prop Vis":
        set_prop_visibility(wireFrameBtn.State)
    elif control.Caption == "Retarget":
        create_relation_constraint()

def EditedInput(control, event):
    uiLockers.on_edit_input(control.input_id)

def LockingCheckboxes(control, event):
    uiLockers.check_is_locked(control.btnLock_id)


def CreateButton(caption):
    button = FBButton()
    button.Caption = str(caption)
    button.Justify = FBTextJustify.kFBTextJustifyCenter
    button.OnClick.Add(BtnCallback)
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

def CreateInputObjName(indx):
    inputTxt = FBEdit()
    inputTxt.input_id = indx
    inputTxt.OnChange.Add(EditedInput)
    return inputTxt
    
def CreateLockBox(text):
    checkBtn = FBButton()
    checkBtn.Style = FBButtonStyle.kFBCheckbox
    #checkBtn.Style = FBButtonStyle.kFBBitmapButton
    checkBtn.SetImageFileNames(uiLockers.unlockImage, uiLockers.lockImage)

    checkBtn.btnLock_id = text[-1]
    checkBtn.OnClick.Add(LockingCheckboxes)
    return checkBtn

def CreateLine(name, height, mainLyt):
    x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(height,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    mainLyt.AddRegion(name, name, x, y, w, h)
    lyt = FBHBoxLayout()
    mainLyt.SetControl(name,lyt)
    return lyt

def CreateLine2Column(name, height, mainLyt):
    x = FBAddRegionParam(240,FBAttachType.kFBAttachLeft,"")
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
    lyt = CreateLine("statusRow_1", 5, mainLyt)
    space = CreateText("")
    lyt.Add(space,50)
    
    txtStatus1 = CreateText("status...")
    lyt.Add(txtStatus1,115)
    txtStatusObjs.row1Info = txtStatus1

    lyt = CreateLine2Column("statusRow_2", 5, mainLyt)
    space = CreateText("")
    lyt.Add(space,50)
    
    txtStatus2 = CreateText("Type name Objs 🠋")
    lyt.Add(txtStatus2,115)
    txtStatusObjs.row2Info = txtStatus2


    lyt = CreateLine("firstRow", 40, mainLyt)

    createBtn = CreateButton("Set Mocap")
    lyt.Add(createBtn,115)

    global wireFrameBtn
    wireFrameBtn = CreateButton("Prop Vis")
    wireFrameBtn.Style = FBButtonStyle.kFB2States
    wireFrameBtn.Look = FBButtonLook.kFBLookColorChange
    wireFrameBtn.SetStateColor(FBButtonState.kFBButtonState0,FBColor(0.6, 0.4, 0.4))
    wireFrameBtn.State = 0
    lyt.Add(wireFrameBtn,75)
    uiLockers.visibilityBtn = wireFrameBtn


    lyt = CreateLine("thirdRow", 75, mainLyt)

    createBtn = CreateButton("Retarget")
    lyt.Add(createBtn,115)

    global inputPropName
    inputPropName = CreateInput("prop namespace...")
    lyt.Add(inputPropName, 90)

    lyt = CreateLine("fourthRow", 110, mainLyt)

    dotCorrectionBtn = CreateButton("DOT Correct")
    dotCorrectionBtn.Style = FBButtonStyle.kFB2States
    dotCorrectionBtn.Look = FBButtonLook.kFBLookColorChange
    dotCorrectionBtn.SetStateColor(FBButtonState.kFBButtonState0,FBColor(1.0, 0.0, 0.0))
    dotCorrectionBtn.SetStateColor(FBButtonState.kFBButtonState1,FBColor(0.0, 0.0, 1.0))
    lyt.Add(dotCorrectionBtn,115)

    lyt = CreateLine("lastRow", 140, mainLyt)
    space = CreateText(" ")
    lyt.Add(space, 10)
    lastTaskText = CreateText("NOW do offset")
    lyt.Add(lastTaskText, 120)

    #2Column:
    lyt = CreateLine2Column("2column_1",40, mainLyt)
    
    mocapPropTxt = CreateText("Mocap Prop Name:")
    lyt.Add(mocapPropTxt, 100)
    mocapPropInput = CreateInputObjName(1)
    lyt.Add(mocapPropInput, 95)
    lockBox1 = CreateLockBox("lock1")
    lyt.Add(lockBox1, 30)
    
    uiLockers.lyt1 = lyt
    uiLockers.input1 = mocapPropInput
    uiLockers.locker1 = lockBox1


    lyt = CreateLine2Column("2column_2",70, mainLyt)

    propRootBoneTxt = CreateText("Prop Root Bone:")
    lyt.Add(propRootBoneTxt, 100)
    
    propRootBoneInput = CreateInputObjName(2)
    lyt.Add(propRootBoneInput, 95)
    lockBox2 = CreateLockBox("lock2")
    lyt.Add(lockBox2, 30)

    uiLockers.lyt2 = lyt
    uiLockers.input2 = propRootBoneInput
    uiLockers.locker2 = lockBox2

    lyt = CreateLine2Column("2column_3",100, mainLyt)
    
    mocapCharBoneTxt = CreateText("Mocap Char Bone:")
    lyt.Add(mocapCharBoneTxt, 100)
    mocapCharBoneInput = CreateInputObjName(3)
    lyt.Add(mocapCharBoneInput, 95)
    lockBox3 = CreateLockBox("lock3")
    lyt.Add(lockBox3, 30)
    
    uiLockers.lyt3 = lyt
    uiLockers.input3 = mocapCharBoneInput
    uiLockers.locker3 = lockBox3


    lyt = CreateLine2Column("2column_4",130, mainLyt)
    
    charBoneTxt = CreateText("Char Bone:")
    lyt.Add(charBoneTxt, 100)

    
    charBoneInput = CreateInputObjName(4)
    lyt.Add(charBoneInput, 95)
    lockBox4 = CreateLockBox("lock4")
    lyt.Add(lockBox4, 30)

    uiLockers.lyt4 = lyt
    uiLockers.input4 = charBoneInput
    uiLockers.locker4 = lockBox4


def CreateMainUI():
    global toolFullName
    t = FBCreateUniqueTool(toolFullName)
    t.StartSizeX = 500  
    t.StartSizeY = 230
    PopulateLayout_Stage_Main(t)
    ShowTool(t)


userObjs = PickedObjects()
uiLockers = UILockObjs()
txtStatusObjs = StatusTxtObj()
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




########
#!!!fix the lock system: when is locked and user type in input!!!
#do the rest