from pyfbsdk import *
from pyfbsdk_additions import *

def AddTestKeys(model):
    prop = model.PropertyList.Find("Lcl Translation")
    if not prop or not isinstance(prop, FBPropertyAnimatable):
        return

    # dostajemy kanały X, Y, Z
    anim_node = prop.GetAnimationNode()
    if not anim_node: return

    nodes = [anim_node.Nodes[i] for i in range(3)]  # X, Y, Z

    # dodajemy przykładowe klucze
    for i, node in enumerate(nodes):
        fcurve = node.FCurve
        if not fcurve:
            continue
        fcurve.KeyAdd(FBTime(0,0,0,0), 0.0)      # frame 0
        fcurve.KeyAdd(FBTime(0,0,0,10), (i+1)*10) # frame 10
        fcurve.KeyAdd(FBTime(0,0,0,20), (i+1)*5)  # frame 20

def CreateTool():
    t = FBCreateUniqueTool("FCurve test with keys")
    t.StartSizeX = 900
    t.StartSizeY = 500

    editor = FBFCurveEditor()
    x = FBAddRegionParam(0, FBAttachType.kFBAttachLeft, "")
    y = FBAddRegionParam(0, FBAttachType.kFBAttachTop, "")
    w = FBAddRegionParam(0, FBAttachType.kFBAttachRight, "")
    h = FBAddRegionParam(0, FBAttachType.kFBAttachBottom, "")
    t.AddRegion("FCurveEditor", "FCurveEditor", x, y, w, h)
    t.SetControl("FCurveEditor", editor)

    # znajdź / utwórz Cube
    model = FBFindModelByLabelName("MyCube")
    if not model:
        model = FBModelCube("MyCube")
        FBSystem().Scene.Components.append(model)

    # dodajemy keyframes
    AddTestKeys(model)

    # dodajemy property do edytora
    prop = model.PropertyList.Find("Lcl Translation")
    if prop and isinstance(prop, FBPropertyAnimatable):
        # ustaw kolory osi
        prop.SetColor(FBColor(1,0,0), 0)  # X
        prop.SetColor(FBColor(0,1,0), 1)  # Y
        prop.SetColor(FBColor(0,0,1), 2)  # Z

        editor.AddProperty(prop)

    ShowTool(t)

CreateTool()
