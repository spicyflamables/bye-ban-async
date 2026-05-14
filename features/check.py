import os
import sqlite3
import time

yellow = "\033[93m"
green = "\033[92m"
red = "\033[91m"
reset = "\033[0m"

# check for supported browsers
def check():
    appdata = os.getenv("LOCALAPPDATA")

    browsers = {
        "chrome": (
            f"{appdata}\\Google\\Chrome\\User Data\\Default\\Network\\Cookies",
            "chrome.exe"
        ),
        "edge": (
            f"{appdata}\\Microsoft\\Edge\\User Data\\Default\\Network\\Cookies",
            "msedge.exe"
        ),
        "brave": (
            f"{appdata}\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Network\\Cookies",
            "brave.exe"
        ),
        "opera": (
            f"{appdata}\\Opera Software\\Opera Stable\\Network\\Cookies",
            "opera.exe"
        ),
        "opera gx": (
            f"{appdata}\\Opera Software\\Opera GX Stable\\Network\\Cookies",
            "opera.exe"
        ),
        "vivaldi": (
            f"{appdata}\\Vivaldi\\User Data\\Default\\Network\\Cookies",
            "vivaldi.exe"
        )
    }

    found = []

    print(f"{yellow}[ > ]{reset} checking cookies")

    # look for browser cookie databases
    for name, data in browsers.items():
        cookie_path, exe = data

        if os.path.exists(cookie_path):
            found.append((name, cookie_path, exe))

    return found

# remove roblox cookies
def clean():
    browsers = check()

    if not browsers:
        print(f"{red}[ - ]{reset} couldnt find any browser cookie files")
        return