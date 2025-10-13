import os
import re

EXPECTED_LENGTH = 144
BITS_PER_SECTION = 576
SECTIONS_PER_FRAME = 64
BITS_PER_FRAME = SECTIONS_PER_FRAME * BITS_PER_SECTION

SECTION_PATTERN = re.compile(r'section_(\d{2})\s*=\s*"([0-9A-Fa-f]+)"')

def validate_module(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    matches = SECTION_PATTERN.findall(content)
    section_count = len(matches)
    total_bits = section_count * BITS_PER_SECTION

    print(f"\nScanning {os.path.basename(path)}")
    print(f"Sections found: {section_count}")
    print(f"Total bits: {total_bits}")

    if section_count % SECTIONS_PER_FRAME != 0:
        print(f"Warning: Section count not divisible by {SECTIONS_PER_FRAME}")
    else:
        frame_count = section_count // SECTIONS_PER_FRAME
        print(f"Valid: {frame_count} frame(s) detected")

    for index, hex_string in matches:
        if len(hex_string) != EXPECTED_LENGTH:
            print(f"Section_{index} length = {len(hex_string)} (expected {EXPECTED_LENGTH})")

def scan_folder(folder):
    for filename in os.listdir(folder):
        if filename.startswith("fg_") and filename.endswith(".lua"):
            validate_module(os.path.join(folder, filename))

# Replace with your actual path
scan_folder("C://Users//Homeless//source//repos//junk drawer//ba256_frames//")
