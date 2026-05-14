import os
import shutil
import time

yellow = "\033[93m"
green = "\033[92m"
red = "\033[91m"
reset = "\033[0m"

# remove folder if it exists
def remove_folder(path, name):
    try:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
            print(f"{green}[ + ]{reset} removed {name}")
    except:
        print(f"{red}[ - ]{reset} error removing {name}")

# remove file if it exists
def remove_file(path, name):
    try:
        if os.path.exists(path):
            os.remove(path)
            print(f"{green}[ + ]{reset} removed {name}")
    except:
        print(f"{red}[ - ]{reset} error removing {name}")

# clean roblox files
def clean():
    local = os.getenv("LOCALAPPDATA")
    roaming = os.getenv("APPDATA")
    temp = os.getenv("TEMP")
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")

    print(f"{red}[ - ]{reset} closing roblox")

    os.system("taskkill /F /IM RobloxPlayerBeta.exe >nul 2>&1")
    os.system("taskkill /F /IM RobloxStudioBeta.exe >nul 2>&1")
    os.system("taskkill /F /IM RobloxCrashHandler.exe >nul 2>&1")
    os.system("taskkill /F /IM Bloxstrap.exe >nul 2>&1")

    print(f"{yellow}[ > ]{reset} removing roblox")

    time.sleep(1)

    folders = [
        (f"{local}\\Roblox", "roblox folder"),
        (f"{local}\\Bloxstrap", "bloxstrap folder"),
        (f"{roaming}\\Roblox", "roblox appdata"),
        (f"{temp}\\Roblox", "roblox temp"),
        (f"{temp}\\RBX", "rbx temp"),
        (
            os.path.join(
                roaming,
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
                "Roblox"
            ),
            "roblox start menu"
        )
    ]

    files = [
        (os.path.join(desktop, "Roblox Player.lnk"), "roblox shortcut"),
        (os.path.join(desktop, "Roblox Studio.lnk"), "roblox studio shortcut")
    ]

    # remove all folders
    for path, name in folders:
        remove_folder(path, name)

    # remove all files
    for path, name in files:
        remove_file(path, name)

if __name__ == "__main__":
    clean()