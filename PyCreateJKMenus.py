from pyfbsdk import FBMenuManager, FBMessageBox
import json, os, sys, runpy, traceback
from contextlib import contextmanager

# globalna mapa eventów
event_map = {}

@contextmanager
def pushd(new_dir):
    prev = os.getcwd()
    try:
        os.chdir(new_dir)
        yield
    finally:
        os.chdir(prev)

def OnMenuClick(eventName):
    if eventName in event_map:
        script_path = event_map[eventName]
        if not os.path.isfile(script_path):
            FBMessageBox("Error...", "Code file doesn NOT exist. \nPlease contact your friendly neighbourhood Technical Animator", "OK")
            return

        script_dir = os.path.dirname(script_path)
        # upewnij się, że katalog skryptu jest w sys.path (na wypadek importów)
        if script_dir and script_dir not in sys.path:
            sys.path.insert(0, script_dir)

        try:
            # uruchom jak skrypt główny i na czas wykonania ustaw CWD na folder skryptu
            with pushd(script_dir or os.getcwd()):
                runpy.run_path(script_path, run_name="__main__")
        except Exception:
            tb = traceback.format_exc()
            # pokaż pełny traceback (MotionBuilder zwykle łyka dłuższy tekst, ale jak będzie za długi — przytnij)
            FBMessageBox("Error...", f"Błąd podczas uruchamiania '{eventName}':\n\n{tb}", "OK")
    else:
        FBMessageBox("Error...", "Menu Error: JSON don't have this option set up yet. \nPlease contact your friendly neighbourhood Technical Animator", "OK")


def LoadMenu():
    def MenuOptions(control, event):
        eventName = event.Name
        OnMenuClick(eventName)
    
    def AddMenu(mainMenuName, subMenuName=""):
        menu = FBMenuManager().GetMenu(mainMenuName + subMenuName)
        if menu:
            menu.OnMenuActivate.Add(MenuOptions)

    def create_tool(mtool, menuPath):
        print(f"Processing tool: {mtool['nameTool']}")
        nameTool = mtool["nameTool"]
        mainFile = mtool["mainFile"]
        filePATH = mtool["filePATH"]

        full_path = os.path.join(filePATH, mainFile)

        # uwaga: nazwy muszą być unikalne — inaczej nadpiszesz mapowanie
        if nameTool in event_map:
            print(f"[WARN] Zduplikowana nazwa menu '{nameTool}'. Nadpisuję ścieżkę.")

        event_map[nameTool] = full_path
        menuManager.InsertLast(menuPath, nameTool)
        print(f"Registered: {nameTool} -> {full_path}")
    
    def build_menu(tools, menuPath):
        for tool in tools:
            if "submenu" in tool:
                submenu = tool["submenu"]
                submenuPath = menuPath + "/" + submenu
                menuManager.InsertLast(menuPath, submenu)
                build_menu(tool["tools"], submenuPath)
                AddMenu(submenuPath)
            else:
                create_tool(tool, menuPath)


    mainMenuName = "@JK Tools"
    menuManager = FBMenuManager()
    menuManager.InsertLast(None, mainMenuName)

    with open("C:\\Projekty\\Repos\\MoBu-Scripts\\CustomMenus\\SciprtsMenus.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1) put all json paths from JSON to sys.path (once)
    unique_dirs = set()
    for tools in data.values():
        for tool in tools:
            p = tool.get("filePATH", "")
            if p and os.path.isdir(p):
                unique_dirs.add(p)

    for p in unique_dirs:
        if p not in sys.path:
            sys.path.insert(0, p)
            print(f"[sys.path] + {p}")

    # 2) buduj menu i mapę eventów
    for menu, tools in data.items():
        menuPath = mainMenuName + "/" + menu
        menuManager.InsertLast(mainMenuName, menu)
        build_menu(tools, menuPath)
        AddMenu(menuPath)

        

# uruchamiamy
LoadMenu()


#FBMessageBox("Error...", "Menu Error: This option hasn't been set up yet. Please contact your friendly neighbourhood Technical Animator", "OK")

