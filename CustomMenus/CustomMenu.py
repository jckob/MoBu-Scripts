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
        if script_dir and script_dir not in sys.path:
            sys.path.insert(0, script_dir)

        try:
            with pushd(script_dir or os.getcwd()):
                runpy.run_path(script_path, run_name="__main__")
        except Exception:
            tb = traceback.format_exc()
            FBMessageBox("Error...", f"Error during executing  '{eventName}':\n\n{tb}", "OK")
    else:
        FBMessageBox("Error...", "Menu Error: JSON don't have this option set up yet. \nPlease contact your friendly neighbourhood Technical Animator", "OK")

def LoadMenu(main_MenuName, filePATH):
    def MenuOptions(control, event):
        eventName = event.Name
        OnMenuClick(eventName)
    
    def AddMenu(menuPath):
        menu = FBMenuManager().GetMenu(menuPath)
        if menu:
            menu.OnMenuActivate.Add(MenuOptions)

    def create_tool(mtool, menuPath):
        print(f"Processing tool: {mtool['nameTool']}")
        nameTool = mtool["nameTool"]
        mainFile = mtool["mainFile"]
        filePATH = mtool["filePATH"]

        full_path = os.path.join(filePATH, mainFile)

        if nameTool in event_map:
            print(f"[WARN] Zduplikowana nazwa menu '{nameTool}'. Nadpisuję ścieżkę.")

        event_map[nameTool] = full_path
        menuManager.InsertLast(menuPath, nameTool)
        print(f"Registered: {nameTool} -> {full_path}")
    
    def build_menu(tools, menuPath):
        for tool in tools:
            if "submenu" in tool:  # podmenu
                submenu = tool["submenu"]
                submenuPath = menuPath + "/" + submenu
                menuManager.InsertLast(menuPath, submenu)
                build_menu(tool["tools"], submenuPath)
                AddMenu(submenuPath)
            elif "nameTool" in tool:  # zwykły tool
                create_tool(tool, menuPath)
            else:
                print(f"[WARN] Nieznany format wpisu JSON: {tool}")

    # główny root menu
    menuManager = FBMenuManager()
    menuManager.InsertLast(None, main_MenuName)

    with open(filePATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # dodaj wszystkie ścieżki folderów z JSON do sys.path
    unique_dirs = set()
    if isinstance(data, dict):
        all_tools = [tool for tools in data.values() for tool in tools]
    elif isinstance(data, list):
        all_tools = data
    else:
        all_tools = []

    for tool in all_tools:
        p = tool.get("filePATH", "")
        if p and os.path.isdir(p):
            unique_dirs.add(p)

    for p in unique_dirs:
        if p not in sys.path:
            sys.path.insert(0, p)
            print(f"[sys.path] + {p}")

    # buduj menu
    if isinstance(data, dict):
        for menu, tools in data.items():
            menuPath = main_MenuName + "/" + menu
            menuManager.InsertLast(main_MenuName, menu)
            build_menu(tools, menuPath)
            AddMenu(menuPath)
    elif isinstance(data, list):
        build_menu(data, main_MenuName)
        AddMenu(main_MenuName)
    else:
        print("[ERROR] Nieobsługiwany format JSON w", filePATH)


# przykładowe wywołania
jkPath = "C:\\Projekty\\Repos\\MoBu-Scripts\\CustomMenus\\ScriptsMenus.json"
LoadMenu("@JK Tools", jkPath)

vanillaPath = "C:\\Projekty\\Repos\\MoBu-Scripts\\CustomMenus\\VanillaMenu.json"
LoadMenu("⬜ Vanilla Tools", vanillaPath)

rarePath = "C:\\Projekty\\Repos\\MoBu-Scripts\\CustomMenus\\RareMenu.json"
LoadMenu("🟪 Rare Tools", rarePath)
