import os
import sys
import ctypes

os.system("")

yellow = "\033[93m"
green = "\033[92m"
red = "\033[91m"
reset = "\033[0m"

# check if running as admin
def admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# relaunch as admin if needed
if not admin():
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        f'"{os.path.abspath(__file__)}"',
        None,
        1
    )

    sys.exit()

# set current directory
os.chdir(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

features = [
    "features/check.py",
    "features/remove.py",
    "features/change.py",
    "features/install.py",
    "features/finish.py"
]

# load all feature files
for feature in features:
    try:
        exec(open(
            feature,
            encoding="utf-8"
        ).read())

    except Exception as e:
        print(f"{red}[ - ]{reset} error loading {os.path.basename(feature)}")
        print(e)

input()