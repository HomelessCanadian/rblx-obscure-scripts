import os
import time
import keyboard
import pyperclip  # pip install pyperclip
import pyautogui

frame_dir = "game_files/ReplicatedStorage/Video data"
trigger_key = "pause"
killswitch_key = "="
delay = 0.1  # seconds between paste and enter / adjust as needed for your system speed

def to_base26(n):
    chars = []
    for _ in range(3):
        chars.append(chr(ord('a') + (n % 26)))
        n //= 26
    return ''.join(reversed(chars))

def escape_lua_block(s):
    return s.replace("]]", "]] .. ']]' .. [[")

print(f"🚀 Ready. Focus Studio. Press {trigger_key} to begin injection.")
keyboard.wait(trigger_key)
print("🎯 Injection started. Press pause to inject each frame, = to abort.")

for i in range(1645):
    if keyboard.is_pressed(killswitch_key):
        print("🛑 Killswitch activated. Exiting.")
        break

    name = f"fg_{to_base26(i)}.lua"
    path = os.path.join(frame_dir, name)
    if not os.path.exists(path):
        print(f"❌ Missing: {name}")
        continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    safe = escape_lua_block(content)
    lua = f"""local m = Instance.new("ModuleScript")
m.Name = "{name[:-4]}"
m.Source = [[{safe}]]
m.Parent = game.ReplicatedStorage:FindFirstChild("Bad apple data")"""

    pyperclip.copy(lua)  # copy blob to clipboard
    pyautogui.hotkey('ctrl', 'a')  # select all
    time.sleep(delay)
    pyautogui.hotkey('ctrl', 'v')  # paste blob
    time.sleep(delay)
    pyautogui.press('enter')  # execute
    print(f"✅ Injected {name[:-4]} ({i+1}/461)")

    if i == 229:
        print("Subscribe to YO MOMMA poggers")
    elif i == 460:
        print("It was at this moment that he knew he fucked up")
    elif i == 501:
        print("Why is the carpet all sticky?")
    elif i == 777:
        print("Jackpot! A wild semicolon appears.")
    elif i == 842:
        print("Initializing self-destruct sequence...")
    elif i == 1024:
        print("We've hit a nice round power of two.")
    elif i == 1111:
        print("This is not the code you're looking for.")
    elif i == 1337:
        print("You've unlocked the leet-speak easter egg.")
    elif i == 1450:
        print("Is anyone else hungry for pizza?")
    elif i == 1505:
        print("Error 404: Logic not found.")
    elif i == 1600:
        print("The number of the beast's slightly less cool cousin.")
    elif i == 1645:
        print("Last frame! Time to celebrate with some ice cream.")