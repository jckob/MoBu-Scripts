# Copyright 2009 Autodesk, Inc.  All rights reserved.
# Use of this software is subject to the terms of the Autodesk license agreement 
# provided at the time of installation or download, or which otherwise accompanies
# this software in either electronic or hard copy form.
#
# Script description:
# Create a tool that shows how drag and drop works.
# Allow for a model to be dropped in a container. From that model show its property list and allow edition/selection
# of all the properties.
#
# Topic: FBVisualContainer, FBSceneChangeType, FBDragAndDropState, FBPropertyFlag, FBEditPropertyModern, FBEditProperty
#

from pyfbsdk import *
from pyfbsdk_additions import *


class AssigneObjects:
    mocapProp = None
    propRootBone = None
    mocapCharBone = None
    charBone = None

def SetupPropertyList(control, model):
    correctContainer = _get_container(control)
    print(control.Caption)
    correctContainer.Items.removeAll()
    tool.prop_list = []
    
    tool.model = model
    if model:
        correctContainer.Items.append(model.Name)
        tool.prop_list.append(None)
        for p in model.PropertyList:
            if p and p.IsInternal() and not p.GetPropertyFlag(FBPropertyFlag.kFBPropertyFlagHideProperty):
                tool.prop_list.append(p)
        _get_pickedObj(control, model)

def Show_Obj():
    print(AssigneObjects.mocapProp)
    print(AssigneObjects.propRootBone)
    print(AssigneObjects.mocapCharBone.Name)
    print(AssigneObjects.charBone.Name)

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

def _get_pickedObj(control, pickedObj):
    if control.Caption == "mocapProp":
        AssigneObjects.mocapProp = pickedObj
    elif control.Caption == "propRootBone":
        AssigneObjects.propRootBone = pickedObj
    elif control.Caption == "mocapCharBone":
        AssigneObjects.mocapCharBone = pickedObj
    elif control.Caption == "charBone":
        AssigneObjects.charBone = pickedObj
    return None


def EventContainerDblClick(control, event):
    SetupPropertyList(control, None)
    
def EventContainerDragAndDrop(control, event):
    if event.State == FBDragAndDropState.kFBDragAndDropDrag:
        event.Accept()
    elif event.State == FBDragAndDropState.kFBDragAndDropDrop:
        SetupPropertyList( control, event.Components[0])

def SceneChanged(scene, event):
    if len(tool.container.Items) != 0 and \
        event.Type == FBSceneChangeType.kFBSceneChangeDetach  and \
        event.ChildComponent == tool.model:
        SetupPropertyList(None, None)

def PopulateLayout(mainLyt):    
    x = FBAddRegionParam(0,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(0,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachBottom,"")
    mainLyt.AddRegion("main","main", x, y, w, h)
    vlyt = FBVBoxLayout()
    mainLyt.SetControl("main",vlyt)
    
    l = FBLabel()
    l.Caption = "Drag and drop a model into the container. Double click to clear."
    vlyt.Add(l,30)
    
    tool.model = None
    tool.container1 = FBVisualContainer()
    tool.container1.OnDragAndDrop.Add(EventContainerDragAndDrop)
    tool.container1.OnDblClick.Add(EventContainerDblClick)
    tool.container1.Caption = "mocapProp"
    vlyt.Add(tool.container1,30)

    tool.model = None
    tool.container2 = FBVisualContainer()
    tool.container2.OnDragAndDrop.Add(EventContainerDragAndDrop)
    tool.container2.OnDblClick.Add(EventContainerDblClick)
    tool.container2.Caption = "propRootBone"
    vlyt.Add(tool.container2,30)

    tool.model = None
    tool.container3 = FBVisualContainer()
    tool.container3.OnDragAndDrop.Add(EventContainerDragAndDrop)
    tool.container3.OnDblClick.Add(EventContainerDblClick)
    tool.container3.Caption = "mocapCharBone"
    vlyt.Add(tool.container3,30)

    tool.model = None
    tool.container4 = FBVisualContainer()
    tool.container4.OnDragAndDrop.Add(EventContainerDragAndDrop)
    tool.container4.OnDblClick.Add(EventContainerDblClick)
    tool.container4.Caption = "charBone"
    vlyt.Add(tool.container4,30)
    
    # Register for scene event
    FBSystem().Scene.OnChange.Add(SceneChanged)
    
    # register when this tool is destroyed.
    tool.OnUnbind.Add(OnToolDestroy)
    
    
def OnToolDestroy(control,event):
    # Important: each time we run this script we need to remove
    # the SceneChanged from the Scene else they will accumulate
    FBSystem().Scene.OnChange.Remove(SceneChanged)
            
def CreateTool():
    global tool
    
    tool = FBCreateUniqueTool("Assign Objects")
    tool.StartSizeX = 400
    tool.StartSizeY = 400
    PopulateLayout(tool)
    ShowTool(tool)
    

CreateTool()
