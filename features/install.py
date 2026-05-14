import os
import time
import urllib.request
import subprocess
import threading

os.system("")

yellow = "\033[93m"
green = "\033[92m"
red = "\033[91m"
reset = "\033[0m"

choice = input(
    f"{yellow}[ > ]{reset} install roblox y/n: "
).lower()

# skip install if user says no
if choice != "y":
    print(f"{red}[ - ]{reset} install skipped")

else:
    installer = os.path.join(
        os.getenv("TEMP"),
        "RobloxPlayerInstaller.exe"
    )

    print(f"{yellow}[ > ]{reset} downloading roblox")

    # download roblox installer
    try:
        urllib.request.urlretrieve(
            "https://setup.rbxcdn.com/RobloxPlayerInstaller.exe",
            installer
        )

        print(f"{green}[ + ]{reset} downloaded roblox")

    except Exception as e:
        print(f"{red}[ - ]{reset} error downloading roblox")
        print(e)

    # constantly close roblox during install
    def close_roblox():
        while True:
            os.system(
                "taskkill /F /IM RobloxPlayerBeta.exe >nul 2>&1"
            )

            time.sleep(1)

    print(f"{yellow}[ > ]{reset} installing roblox")

    try:
        threading.Thread(
            target=close_roblox,
            daemon=True
        ).start()

        process = subprocess.Popen(installer)

        while process.poll() is None:
            time.sleep(1)

        time.sleep(3)

        os.system(
            "taskkill /F /IM RobloxPlayerBeta.exe >nul 2>&1"
        )

        print(f"{green}[ + ]{reset} installed roblox")

    except Exception as e:
        print(f"{red}[ - ]{reset} error installing roblox")
        print(e)