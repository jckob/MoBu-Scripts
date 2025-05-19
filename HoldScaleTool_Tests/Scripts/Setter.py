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

def SetupPropertyList(model):
    tool.container.Items.removeAll()
    tool.list.Items.removeAll()
    tool.prop_list = []
    
    
    tool.model = model
    
    if model:
        tool.container.Items.append(model.Name)
        tool.prop_list.append(None)
        tool.list.ItemIndex = 0
        PropertyListChanged(tool.list, None)
    print(model.Name)
    
    
def EventContainerDblClick(control, event):
    SetupPropertyList(None)
    
def EventContainerDragAndDrop(control, event):
    if event.State == FBDragAndDropState.kFBDragAndDropDrag:
        event.Accept()
    elif event.State == FBDragAndDropState.kFBDragAndDropDrop:
        SetupPropertyList( event.Components[0] )
        
def PropertyListChanged(control, event):
    tool.prop.Property = tool.prop_list[control.ItemIndex]
    tool.prop_modern.Property = tool.prop_list[control.ItemIndex]

  
def SceneChanged(scene, event):
    if len(tool.container.Items) != 0 and \
        event.Type == FBSceneChangeType.kFBSceneChangeDetach  and \
        event.ChildComponent == tool.model:
        SetupPropertyList(None)
        
def CreateLine(name, height, mainLyt):
    x = FBAddRegionParam(0,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(0,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachBottom,"")
    mainLyt.AddRegion("main","main", x, y, w, h)
    vlyt = FBVBoxLayout()
    mainLyt.SetControl("main",vlyt)
    return vlyt

def CreateText(text):
    emptySpace = FBLabel()
    emptySpace.Caption = text
    return emptySpace

def CreateInputObj():
    tool.model = None
    tool.container = FBVisualContainer()
    tool.container.OnDragAndDrop.Add(EventContainerDragAndDrop)
    tool.container.OnDblClick.Add(EventContainerDblClick)
    return tool.container


def PopulateLayout(mainLyt):    
    vlyt = CreateLine("firstRow", 10, mainLyt)
    
    descriptionText = CreateText("Drag and drop a model into the container. Double click to clear.")
    vlyt.Add(descriptionText,30)
    wristInput = CreateInputObj()
    vlyt.Add(tool.container,40)

    tool.model = None
    tool.container = FBVisualContainer()
    tool.container.OnDragAndDrop.Add(EventContainerDragAndDrop)
    tool.container.OnDblClick.Add(EventContainerDblClick)
    vlyt.Add(tool.container,40)
    
    hlyt = FBHBoxLayout()
    tool.list = FBList()
    tool.list.OnChange.Add(PropertyListChanged) 
    hlyt.AddRelative(tool.list)
    
    
    vlyt.Add(hlyt, 30)
    
    
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
    
    tool = FBCreateUniqueTool("Property Example")
    tool.StartSizeX = 400
    tool.StartSizeY = 200
    PopulateLayout(tool)
    ShowTool(tool)
    

CreateTool()
