import os, sys

sys.path.append(os.path.realpath(__file__))
script_dir = os.path.dirname(os.path.realpath(__file__))
print("Script directory:", script_dir)
print("Working directory:", os.getcwd())

if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
script_dir = os.path.dirname(__file__)

from pyfbsdk import FBAddRegionParam, FBAttachType, FBTool, ShowTool, FBWidgetHolder
from pyfbsdk_additions import FBToolList, FBAddTool, FBDestroyToolByName
import shiboken2
from PySide2 import QtCore, QtUiTools
from PySide2.QtWidgets import QPushButton 

toolName = "Take Tool v"
toolVersion = 2.0
toolCategory = "rare"
toolFullName = toolName + str(toolVersion) + " " + toolCategory

UI_PATH = os.path.join(os.path.dirname(__file__), "rTakeToolUI.ui")

class UIObjects():
    def __init__(self):
        self.start_Btn = None
        self.end_Btn = None
        self.autoAssgn_Btn = None
        self.input1_Edit = None
        self.input2_Edit = None
        self.input3_Edit = None
        self.diffFrames_Txt = None
        self.createTake_Btn = None
        self.cropTake_Btn = None
        self.showCopiedTake_Btn = None
        self.colorStatus_Txt = None
        self.extreme_Btn = None
        self.getTakeName_Btn = None


        self.sizes = Size()

class Size:
    def __init__(self, x=0, y=0):
        self.X = x
        self.Y = y

uiObjRef = UIObjects()


class NativeWidgetHolder(FBWidgetHolder):
    #
    # Override WidgetCreate function to create native widget via PySide.
    # \param  parentWidget  Memory address of Parent QWidget.
    # \return               Memory address of the child native widget.
    #
    def WidgetCreate(self, pWidgetParent):
        #
        # IN parameter pWidgetparent is the memory address of the parent Qt widget. 
        #   here we should PySide.shiboken.wrapInstance() function to convert it to PySide.QtWidget object.
        #   and use it the as the parent for native Qt widgets created via Python. 
        #   Similiar approach is available in the sip python module for PyQt 
        #
        # Only a single widget is allowed to be the *direct* child of the IN parent widget. 
        #
        vert_ui_file = UI_PATH
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(vert_ui_file)
        file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(file)
        file.close

        self.mNativeQtWidget = self.ui

        #button elements
        uiObjRef.start_Btn      = self.ui.Start_Btn
        uiObjRef.end_Btn        = self.ui.End_Btn
        uiObjRef.autoAssgn_Btn  = self.ui.AutoAssign_Btn
        uiObjRef.createTake_Btn = self.ui.CreateTake_Btn
        uiObjRef.cropTake_Btn   = self.ui.CropTake_Btn
        uiObjRef.showCopiedTake_Btn = self.ui.ShowCopiedTake_Btn
        uiObjRef.extreme_Btn = self.ui.Extreme_Btn
        uiObjRef.getTakeName_Btn = self.ui.GetTakeName_Btn

        
        #non-button elements
        uiObjRef.input1_Edit    = self.ui.Input1_Edit
        uiObjRef.input2_Edit    = self.ui.Input2_Edit
        uiObjRef.input3_Edit    = self.ui.Input3_Edit
        uiObjRef.diffFrames_Txt = self.ui.DiffFrames_Txt
        uiObjRef.colorStatus_Txt = self.ui.ColorStatus_Txt
        
        uiObjRef.sizes.X = self.ui.geometry().width()
        uiObjRef.sizes.Y = self.ui.geometry().height()

        tool.StartSizeX = uiObjRef.sizes.X
        tool.StartSizeY = uiObjRef.sizes.Y + 20

        print("Tool start size: {0}, {1}".format(tool.MinSizeX, tool.MinSizeY))

        #
        # return the memory address of the *single direct* child QWidget. 
        #
        
        return shiboken2.getCppPointer(self.mNativeQtWidget)[0]


class NativeQtWidgetTool(FBTool):
    def BuildLayout(self):
        x = FBAddRegionParam(0,FBAttachType.kFBAttachLeft,"")
        y = FBAddRegionParam(0,FBAttachType.kFBAttachTop,"")
        w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
        h = FBAddRegionParam(0,FBAttachType.kFBAttachBottom,"")
        self.AddRegion("main","main", x, y, w, h)
        self.SetControl("main", self.mNativeWidgetHolder)
        
    def __init__(self, name):
        FBTool.__init__(self, name)
        self.mNativeWidgetHolder = NativeWidgetHolder()
        
        self.BuildLayout()
        
        
gToolName = "Take Commentator Tool"

#Development? - need to recreate each time!!
gDEVELOPMENT = True

if gDEVELOPMENT:
    FBDestroyToolByName(gToolName)

if gToolName in FBToolList:
    tool = FBToolList[gToolName]

else:
    tool = NativeQtWidgetTool(gToolName)
    #
    FBAddTool(tool)
    

def show_tool(): 
    ShowTool(tool)

#show_tool()