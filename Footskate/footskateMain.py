from pyfbsdk import *

import math
import toolUI as ui
#from  graphTest1 import show_graph



circle = FBFindModelByLabelName("LeftCircle")
ballL = FBFindModelByLabelName("ballM")
heelM = FBFindModelByLabelName("heelM")

#-7.18
ballBone = FBFindModelByLabelName("LeftFoot")
heelBone = FBFindModelByLabelName("LToeEnd")

take = FBSystem().CurrentTake
time_span = take.LocalTimeSpan

# Start and stop time
start = time_span.GetStart()
stop = time_span.GetStop()


# Loop over all frames in the take
current_time = FBTime(0,0,0,0)  # initialize
frame = start.GetFrame()

isOnFloor = True
ballUp = False
heelUp = False

prevHeelVec = FBVector3d()
prevBallVec = FBVector3d()


circle.Visibility.SetAnimated(True)

take = FBSystem().CurrentTake
start_frame = take.LocalTimeSpan.GetStart().GetFrame()
end_frame   = take.LocalTimeSpan.GetStop().GetFrame()


class FakeControl:
    def __init__(self, caption):
        self.Caption = caption


def getVector(model_label, frame, do_deformations=True):
    model = FBFindModelByLabelName(model_label)
    if not model:
        raise RuntimeError("Model '%s' not found" % model_label)

    # Make an FBTime at the frame
    t = FBTime(0, 0, 0, frame)

    # Move the scene/playhead to that time
    # Option A: set scene local time
    #FBSystem().Scene.LocalTime = t
    FBPlayerControl().Goto(t)
    # Option B (equivalent): FBPlayerControl().Goto(t)

    # Force evaluation so the model's transform is updated
    FBSystem().Scene.Evaluate()
    if do_deformations:
        FBSystem().Scene.EvaluateDeformations()

    # Read world translation (no time argument here)
    vec = FBVector3d()
    model.GetVector(vec, FBModelTransformationType.kModelTranslation, True, None)

    # FBVector3d supports indexing: vec[0], vec[1], vec[2]
    return vec


def moved_enough(prev, curr, threshold=0.5, axis="xz"):
    """Return True if distance between prev and curr > threshold."""
    if axis == "xz":
        dx = curr[0] - prev[0]
        dz = curr[2] - prev[2]
        dist = math.sqrt(dx*dx + dz*dz)
    else:  # full 3D
        dx = curr[0] - prev[0]
        dy = curr[1] - prev[1]
        dz = curr[2] - prev[2]
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
    return dist > threshold


def analyze_vectors(vBall, vHeel, currentFrame):
    tresholdY = 2.0
    isBallUp = set_is_bone_up(vBall[1], tresholdY)
    isHeelUp = set_is_bone_up(vHeel[1], tresholdY)

    #if moved_enough(prevHeelVec, vHeel, threshold=0.5, axis="xz"):
    #    isHeelUp = True
    #if moved_enough(prevBallVec, vBall, threshold=0.5, axis="xz"):
    #    isBallUp = True

    if isBallUp and isHeelUp:
        key_visibility(circle, currentFrame, False)
    else:
        key_visibility(circle, currentFrame, True)

 
def set_is_bone_up(bone, treshold):
    if bone > treshold:
        return True
    else:
        return False


def key_visibility(obj, frame, visibility):
    obj.Visibility.GetAnimationNode().KeyAdd(FBTime(0,0,0,frame), visibility)


def create_start_progress(caption):
    # Create a FBProgress object and set default values for the caption and text.
    lFbp = FBProgress()

    # Call ProgressBegin() before use any other function and property.
    lFbp.ProgressBegin()

    # Set the custom task name.
    lFbp.Caption = caption
    return lFbp

def set_progress_status(lFbp, text, percent):
    lFbp.Caption = text
    lFbp.Percent = percent


def procces_markers():
    lFbp = create_start_progress("frame by frame")
    maxLen = end_frame - start_frame - 1
    progres = start_frame

    for f in range(start_frame, end_frame + 1):
        posBall = getVector("ballM", f)
        posHeel = getVector("heelM", f)

        set_progress_status(lFbp, f"frame {f}", int(progres/maxLen))
        
        analyze_vectors(posBall, posHeel, f)
        prevBallVec = posBall
        prevHeelVec = posHeel
        print(f)

    lFbp.ProgressDone()
    del( lFbp)


def set_ui_def():
    ui.show_tool()

    set_button_connections(ui.uiObjRef.createMarkersBtn, "createMarkersBtn")
    set_button_connections(ui.uiObjRef.doMarkersBtn, "doMarkersBtn")
    set_button_connections(ui.uiObjRef.showWindowBtn, "showWindowBtn")


def set_button_connections(buttonRef, controlName):
    try:
        buttonRef.clicked.disconnect()
    except:
        pass
    buttonRef.clicked.connect(lambda: BtnCallback(FakeControl(controlName), None))


def BtnCallback(control, event):
    if control.Caption == "createMarkersBtn":
        print("Check inputs clicked")
        ui.uiObjRef.doMarkersBtn.setEnabled(False)

        #show_graph()
    elif control.Caption == "doMarkersBtn":
        print("Check all Takes clicked")
        
    elif control.Caption == "showWindowBtn":
        print("Update clicked")
        


set_ui_def()
#ui.uiObjRef.doMarkersBtn.setEnabled(False)