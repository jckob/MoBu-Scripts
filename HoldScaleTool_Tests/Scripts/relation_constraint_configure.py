from pyfbsdk import FBFindModelByLabelName, FBConstraintRelation, FBConnect

mocapPropName = "Mocap_Prop"
propBoneName = "Root_Prop"
retPropBoneName = "RetProp_Name"
retOffsetName = "Offset"
mocapCharBoneName = "RightFingerBase"
charBoneName = "Aragor:RightHand"

def define_objects():
    mocapProp = FBFindModelByLabelName(mocapPropName)
    propBone = FBFindModelByLabelName(propBoneName)

    retPropBone = FBFindModelByLabelName(retPropBoneName)
    retOffset = FBFindModelByLabelName(retOffsetName)

    mocapCharBone = FBFindModelByLabelName(mocapCharBoneName)
    charBone= FBFindModelByLabelName(charBoneName)

    constrain = FBConstraintRelation("C_RelationProp")
    constrain.Active = True

    mocapProp_BoxIn = constrain.SetAsSource(mocapProp)
    mocapCharBone_BoxIn = constrain.SetAsSource(mocapCharBone)
    charBone_BoxIn = constrain.SetAsSource(charBone)
    #propBone_BoxIn = constrain.SetAsSource(propBone)
    retOffset_BoxIn = constrain.SetAsSource(retOffset)

    retProp_BoxOut = constrain.ConstrainObject(propBone)
    retPropBone_BoxOut = constrain.ConstrainObject(retPropBone)

    addNodeBox_1 = constrain.CreateFunctionBox("Vector","Add (V1 + V2)")
    subNodeBox_2 = constrain.CreateFunctionBox("Vector","Subtract (V1 - V2)")

    return mocapProp_BoxIn, mocapCharBone_BoxIn, charBone_BoxIn, retOffset_BoxIn, retProp_BoxOut, retPropBone_BoxOut, addNodeBox_1, subNodeBox_2

def _find_anim_node(obj,name):
    result = None
    for node in obj.Nodes:
        if node.Name == name:
            result = node
            break
    return result

def _connect_box(sourceBox, sourceNodeName, targetBox, targetNodeName):
    target_in = _find_anim_node(targetBox.AnimationNodeInGet(), targetNodeName)
    source_out = _find_anim_node(sourceBox.AnimationNodeOutGet(), sourceNodeName)

    if source_out and target_in:
        FBConnect(source_out, target_in)

def connect_boxes(mocapProp_BoxIn, mocapCharBone_BoxIn, charBone_BoxIn, retOffset_BoxIn, retProp_BoxOut, retPropBone_BoxOut, addNodeBox_1, subNodeBox_2):
    _connect_box(mocapProp_BoxIn, 'Rotation', retPropBone_BoxOut, 'Rotation')

    _connect_box(mocapProp_BoxIn, 'Translation', subNodeBox_2, 'V1')
    _connect_box(mocapCharBone_BoxIn, 'Translation', subNodeBox_2, 'V2')

    _connect_box(subNodeBox_2, 'Result', addNodeBox_1, 'V1')
    _connect_box(charBone_BoxIn, 'Translation', addNodeBox_1, 'V2')
    _connect_box(addNodeBox_1, 'Result', retPropBone_BoxOut, 'Translation')

    _connect_box(retOffset_BoxIn, 'Rotation', retProp_BoxOut, 'Rotation')
    _connect_box(retOffset_BoxIn, 'Translation', retProp_BoxOut, 'Translation')



# def objs: "Mocap_Prop", "Root_Prop", "RetProp_Name" "Offset" "RightFingerBase" "Aragor:RightHand"
def create_relation():
    mocapProp_BoxIn, mocapCharBone_BoxIn, charBone_BoxIn, retOffset_BoxIn, retProp_BoxOut, retPropBone_BoxOut, addNodeBox_1, subNodeBox_2 = define_objects()
    connect_boxes(mocapProp_BoxIn, mocapCharBone_BoxIn, charBone_BoxIn, retOffset_BoxIn, retProp_BoxOut, retPropBone_BoxOut, addNodeBox_1, subNodeBox_2)

# This script defines a constraint relation in MotionBuilder to connect various objects and their transformations.
