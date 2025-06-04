from pyfbsdk import FBConstraintRelation, FBConnect

class RelationConstraintObjConfig:

    mocapProp = None
    retPropBone = None
    retPropSource = None
    retOffset = None
    mocapCharBone= None
    charBone = None

    propName = str

relationObjs = RelationConstraintObjConfig()

def define_objects():
    constrain = FBConstraintRelation(f"C_RelationProp_{relationObjs.propName}")
    constrain.Active = True

    mocapProp_BoxIn = constrain.SetAsSource(relationObjs.mocapProp)
    mocapCharBone_BoxIn = constrain.SetAsSource(relationObjs.mocapCharBone)
    charBone_BoxIn = constrain.SetAsSource(relationObjs.charBone)
    retOffset_BoxIn = constrain.SetAsSource(relationObjs.retOffset)

    retProp_BoxOut = constrain.ConstrainObject(relationObjs.retPropSource)
    retPropBone_BoxOut = constrain.ConstrainObject(relationObjs.retPropBone)

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
    _connect_box(mocapProp_BoxIn, 'Rotation', retProp_BoxOut, 'Rotation')

    _connect_box(mocapProp_BoxIn, 'Translation', subNodeBox_2, 'V1')
    _connect_box(mocapCharBone_BoxIn, 'Translation', subNodeBox_2, 'V2')

    _connect_box(subNodeBox_2, 'Result', addNodeBox_1, 'V1')
    _connect_box(charBone_BoxIn, 'Translation', addNodeBox_1, 'V2')
    _connect_box(addNodeBox_1, 'Result',retProp_BoxOut, 'Translation')

    _connect_box(retOffset_BoxIn, 'Rotation',  retPropBone_BoxOut, 'Rotation')
    _connect_box(retOffset_BoxIn, 'Translation',  retPropBone_BoxOut, 'Translation')



# def objs: "Mocap_Prop", "Root_Prop", "RetProp_Name" "Offset" "RightFingerBase" "Aragor:RightHand"
def create_relation():
    mocapProp_BoxIn, mocapCharBone_BoxIn, charBone_BoxIn, retOffset_BoxIn, retProp_BoxOut, retPropBone_BoxOut, addNodeBox_1, subNodeBox_2 = define_objects()
    connect_boxes(mocapProp_BoxIn, mocapCharBone_BoxIn, charBone_BoxIn, retOffset_BoxIn, retProp_BoxOut, retPropBone_BoxOut, addNodeBox_1, subNodeBox_2)