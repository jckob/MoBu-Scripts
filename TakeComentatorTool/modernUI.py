import os, sys

sys.path.append(os.path.realpath(__file__))
script_dir = os.path.dirname(os.path.realpath(__file__))
print("Script directory:", script_dir)
print("Working directory:", os.getcwd())

if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)
    print(script_dir)

from pyfbsdk import FBAddRegionParam, FBAttachType, FBTool, ShowTool, FBWidgetHolder
from pyfbsdk_additions import FBToolList, FBAddTool, FBDestroyToolByName
import shiboken2
from PySide2 import QtCore, QtUiTools


UI_PATH = os.path.join(os.path.dirname(__file__), "login.ui")

class UIObjects():
    def __init__(self):
        self.inputSheetName = None
        self.inputKeyNameList = None
        self.inputValueNameList = None
        self.connectBtn = None
        self.checkInputs = None
        self.checkBoxAllBtn = None
        self.updateBtn = None
        self.clearCommentsBtn = None

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


        uiObjRef.inputSheetName = self.ui.InputSheetName
        uiObjRef.inputKeyNameList = self.ui.InputKeyNameList
        uiObjRef.inputValueNameList = self.ui.InputValueNameList

        uiObjRef.checkInputs = self.ui.CheckInputsButton
        uiObjRef.checkBoxAllBtn = self.ui.CheckAllTakes
        uiObjRef.updateBtn = self.ui.UpdateButton
        uiObjRef.clearCommentsBtn = self.ui.ClearCommentsButton

        # powinno zwrócić <PySide2.QtWidgets.QPushButton ...>

        uiObjRef.sizes.X = self.ui.geometry().width()
        uiObjRef.sizes.Y = self.ui.geometry().height()

        #myUIElements.inputKeyList = self.ui.inputKeyNameList
        #myUIElements.inputValueList = self.ui.inputValueNameList

        #myUIElements.sizes.X = self.ui.geometry().width()
        #myUIElements.sizes.Y = self.ui.geometry().height()

        tool.StartSizeX = uiObjRef.sizes.X
        tool.StartSizeY = uiObjRef.sizes.Y
        print("Tool start size: {0}, {1}".format(tool.StartSizeX, tool.StartSizeY))

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
        print("Initial {0}, {1}".format(uiObjRef.sizes.X, uiObjRef.sizes.Y))

        FBTool.__init__(self, name)
        self.mNativeWidgetHolder = NativeWidgetHolder()
        self.BuildLayout()
        

gToolName = "Take Commentator Tool - PySide2"

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