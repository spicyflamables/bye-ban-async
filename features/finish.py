import os

os.system("")

yellow = "\033[93m"
green = "\033[92m"
red = "\033[91m"
reset = "\033[0m"

print()
print(f"{yellow}made by spicyflamables{reset}")
print()

print(f"{yellow}[ > ]{reset} restart recommended for all changes to apply")

choice = input(
    f"{yellow}[ > ]{reset} restart now y/n: "
).lower()

# restart pc if chosen
if choice == "y":
    print(f"{green}[ + ]{reset} restarting pc")
    os.system("shutdown /r /t 0")
else:
    print(f"{red}[ - ]{reset} restart skipped")