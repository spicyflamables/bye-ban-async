import re
import random
import subprocess
import time
import uuid

yellow = "\033[93m"
green = "\033[92m"
red = "\033[91m"
reset = "\033[0m"

# run cmd
def run(cmd):
    try:
        return subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        ).returncode == 0

    except:
        return False

# start checking macs
print(f"{yellow}[ > ]{reset} checking mac addresses")

try:
    # get mac output
    getmac_output = subprocess.check_output(
        "getmac",
        shell=True,
        text=True
    )

    # find all macs
    macs = re.findall(
        r'([0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2})',
        getmac_output
    )

    # print found macs
    for mac in macs:
        print(f"{green}[ + ]{reset} found mac address {mac.lower()}")

except:
    print(f"{red}[ - ]{reset} error checking mac addresses")

# start changing macs
print(f"{yellow}[ > ]{reset} changing mac address")

try:
    # loop possible adapters
    for i in range(15):
        index = f"{i:04d}"

        # adapter reg path
        reg_path = (
            rf"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class"
            rf"\{{4d36e972-e325-11ce-bfc1-08002be10318}}\{index}"
        )

        # make sure key exists
        if run(f'reg query "{reg_path}"'):

            # generate fake mac
            new_mac = "02" + "".join(
                random.choice("0123456789ABCDEF")
                for _ in range(10)
            )

            # apply new mac
            run(
                f'reg add "{reg_path}" '
                f'/v NetworkAddress '
                f'/t REG_SZ '
                f'/d {new_mac} /f'
            )

    print(f"{green}[ + ]{reset} changed mac address")

except:
    print(f"{red}[ - ]{reset} error changing mac address")

# disable wifi
print(f"{red}[ - ]{reset} disconnecting wifi")

interfaces = []

try:
    # get interfaces
    interface_data = subprocess.check_output(
        "netsh interface show interface",
        shell=True,
        text=True
    )

    # find interface names
    interfaces = re.findall(
        r'(?:Enabled|Disabled)\s+(?:Connected|Disconnected)\s+\w+\s+(.*)',
        interface_data
    )

    # disable all interfaces
    for interface in interfaces:
        run(
            f'netsh interface set interface '
            f'"{interface.strip()}" disable'
        )

except:
    print(f"{red}[ - ]{reset} error disconnecting wifi")

time.sleep(1)

# reconnect wifi
print(f"{green}[ + ]{reset} reconnecting wifi")

try:
    # enable interfaces
    for interface in interfaces:
        run(
            f'netsh interface set interface '
            f'"{interface.strip()}" enable'
        )

    # flush dns
    run("ipconfig /flushdns")

    # renew ip
    subprocess.Popen(
        "ipconfig /renew",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

except:
    print(f"{red}[ - ]{reset} error reconnecting wifi")

# start spoofing
print(f"{yellow}[ > ]{reset} applying soft hwid spoof")

try:
    # generate new machine guid
    new_machine_guid = str(uuid.uuid4()).upper()

    # change machine guid
    run(
        f'reg add '
        f'"HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography" '
        f'/v MachineGuid '
        f'/t REG_SZ '
        f'/d {new_machine_guid} /f'
    )

    # loop hw profiles
    for i in range(1, 10):
        profile_key = (
            f"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet"
            f"\\Hardware Profiles\\{i:04d}"
        )

        # make sure profile exists
        if run(f'reg query "{profile_key}"'):

            # generate new guid
            new_guid = str(uuid.uuid4()).upper()

            # apply new guid
            run(
                f'reg add "{profile_key}" '
                f'/v HwProfileGuid '
                f'/t REG_SZ '
                f'/d {{{new_guid}}} /f'
            )

    # get drives
    try:
        drives_output = subprocess.check_output(
            'powershell -Command '
            '"Get-PSDrive -PSProvider FileSystem | '
            'Select-Object -ExpandProperty Root"',
            shell=True,
            text=True
        )

        # find drive letters
        drives = re.findall(r'([A-Z]):\\', drives_output)

    except:
        drives = ["D", "E", "F", "G", "H"]

    # loop drives
    for drive in drives:

        # skip c drive
        if drive == "C":
            continue

        try:
            # get volume info
            vol_info = subprocess.check_output(
                f"vol {drive}:",
                shell=True,
                text=True
            )

            # find serial
            current = re.search(
                r"Serial Number is ([\w-]+)",
                vol_info
            )

            # make sure serial exists
            if current:

                # generate new serial
                new_id = (
                    f"{random.randint(0x1000, 0xFFFF):04X}-"
                    f"{random.randint(0x1000, 0xFFFF):04X}"
                )

                # apply new serial
                run(f"VolumeID.exe {drive}: {new_id}")

        except:
            pass

    print(f"{green}[ + ]{reset} soft hwid spoof applied")

except:
    print(f"{red}[ - ]{reset} error during soft hwid spoof")