# I don't trust the previous automator
import os
import re

# === CONFIG ===
origin_folder = r"C:\Users\Homeless\source\repos\junk drawer\ba256_frames"
studio_list_file = r"C:\Users\Homeless\source\repos\junk drawer\studio_export.txt"

# === Load expected from folder ===
expected = set()
for file in os.listdir(origin_folder):
    if file.startswith("fg_") and file.endswith(".lua"):
        expected.add(file[:-4])  # strip .lua

if not os.path.exists(studio_list_file):
    print("File not found:", studio_list_file)
    exit()

# === Load actual from Studio export, stripping leading numbers
actual = set()
with open(studio_list_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        # Match lines like: [123] = fg_aaaaa,
        match = re.search(r'=\s*"?(\w+)"?', line)
        if match:
            actual.add(match.group(1))

# === Compare ===
missing = expected - actual
extra = actual - expected

print(f"Total expected: {len(expected)}")
print(f"Total actual:   {len(actual)}")

if missing:
    print("\nMissing in Studio:")
    for name in sorted(missing):
        print("  - " + name)

if extra:
    print("\nExtra in Studio:")
    for name in sorted(extra):
        print("  + " + name)

if not missing and not extra:
    print("\nAll modules match perfectly.")
