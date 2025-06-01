import os
import sys

script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)

from pyfbsdk import FBPropertyFlag, FBDragAndDropState, FBVisualContainer, FBSystem, FBLabel,FBAddRegionParam, FBAttachType, FBSceneChangeType, ShowTool 
from pyfbsdk_additions import FBCreateUniqueTool, FBVBoxLayout
from PropHandlerTool import PickedObjects

class AssigneObjects:
    mocapProp = None
    propRootBone = None
    mocapCharBone = None
    charBone = None

def SetupPropertyList(control, model):
    correctContainer = _get_container(control)
    correctContainer.Items.removeAll()
    tool.prop_list = []
    
    tool.model = model
    if model:
        correctContainer.Items.append(model.Name)
        tool.prop_list.append(None)
        for p in model.PropertyList:
            if p and p.IsInternal() and not p.GetPropertyFlag(FBPropertyFlag.kFBPropertyFlagHideProperty):
                tool.prop_list.append(p)
        set_object(control, model)
    else:
        set_object(control, None)

def _get_container(control):
    if control.Caption == "mocapProp":
        return tool.container1
    elif control.Caption == "propRootBone":
        return tool.container2
    elif control.Caption == "mocapCharBone":
        return tool.container3
    elif control.Caption == "charBone":
        return tool.container4
    return None

def set_object(control, pickedObj):
    if control.Caption == "mocapProp":
        AssigneObjects.mocapProp = pickedObj
    elif control.Caption == "propRootBone":
        AssigneObjects.propRootBone = pickedObj
    elif control.Caption == "mocapCharBone":
        AssigneObjects.mocapCharBone = pickedObj
    elif control.Caption == "charBone":
        AssigneObjects.charBone = pickedObj
    send_objects_to_MainTool()
        
def send_objects_to_MainTool():
    if AssigneObjects.mocapProp is not None and AssigneObjects.propRootBone is not None:
        PickedObjects.mocapProp = AssigneObjects.mocapProp
        PickedObjects.propRootBone = AssigneObjects.propRootBone
        print(PickedObjects.mocapProp.Name)
        print(PickedObjects.propRootBone.Name)
    else:
        PickedObjects.mocapProp = None
        PickedObjects.propRootBone = None


    if AssigneObjects.mocapCharBone is not None and AssigneObjects.charBone is not None:
        PickedObjects.mocapCharBone = AssigneObjects.mocapCharBone
        PickedObjects.charBone = AssigneObjects.charBone
    else:
        PickedObjects.mocapCharBone = None
        PickedObjects.charBone = None
 

def EventContainerDblClick(control, event):
    SetupPropertyList(control, None)
    
def EventContainerDragAndDrop(control, event):
    if event.State == FBDragAndDropState.kFBDragAndDropDrag:
        event.Accept()
    elif event.State == FBDragAndDropState.kFBDragAndDropDrop:
        SetupPropertyList( control, event.Components[0])

def SceneChanged(scene, event):
    for container in [tool.container1, tool.container2, tool.container3, tool.container4]:
        if len(container.Items) != 0 and \
            event.Type == FBSceneChangeType.kFBSceneChangeDetach  and \
            event.ChildComponent == tool.model:
            SetupPropertyList(None, None)


def PopulateLayout(mainLyt):    
    x = FBAddRegionParam(5,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(0,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachBottom,"")
    mainLyt.AddRegion("main","main", x, y, w, h)
    vlyt = FBVBoxLayout()
    mainLyt.SetControl("main",vlyt)
    
    l = FBLabel()
    l.Caption = "Drag & Drop objects"
    vlyt.Add(l,30)
    
    tool.model = None
    tool.container1 = FBVisualContainer()
    tool.container1.OnDragAndDrop.Add(EventContainerDragAndDrop)
    tool.container1.OnDblClick.Add(EventContainerDblClick)
    tool.container1.Caption = "mocapProp"
    vlyt.Add(tool.container1,30)

    tool.container2 = FBVisualContainer()
    tool.container2.OnDragAndDrop.Add(EventContainerDragAndDrop)
    tool.container2.OnDblClick.Add(EventContainerDblClick)
    tool.container2.Caption = "propRootBone"
    vlyt.Add(tool.container2,30)

    tool.container3 = FBVisualContainer()
    tool.container3.OnDragAndDrop.Add(EventContainerDragAndDrop)
    tool.container3.OnDblClick.Add(EventContainerDblClick)
    tool.container3.Caption = "mocapCharBone"
    vlyt.Add(tool.container3,30)

    tool.container4 = FBVisualContainer()
    tool.container4.OnDragAndDrop.Add(EventContainerDragAndDrop)
    tool.container4.OnDblClick.Add(EventContainerDblClick)
    tool.container4.Caption = "charBone"
    vlyt.Add(tool.container4,30)
    
    # Register for scene event
    FBSystem().Scene.OnChange.Add(SceneChanged)
    
    # register when this tool is destroyed.
    tool.OnUnbind.Add(OnToolDestroy)
    
    
def OnToolDestroy(self, control, event):
        print("destroyed")
        FBSystem().Scene.OnChange.Remove(SceneChanged)


def CreateSetterUI():
    global tool
    
    tool = FBCreateUniqueTool("Assign Objects")
    tool.StartSizeX = 100
    tool.StartSizeY = 220
    PopulateLayout(tool)
    ShowTool(tool)

CreateSetterUI()

