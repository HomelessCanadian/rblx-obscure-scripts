#!/usr/bin/env python3
"""
Split a Lua file containing full-frame bitmaps into 16 subframes per frame (32x18),
and group frames into 4-frame blobs, each safely under Studio's Source limit.
"""

import argparse
import re
import sys
from pathlib import Path

MAX_SOURCE = 199000  # Studio-safe limit
FRAMES_PER_FILE = 4  # Fixed batch size
SECTIONS_PER_FRAME = 16

def extract_raw_frames(lua_file):
    try:
        with open(lua_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{lua_file}' not found", file=sys.stderr)
        sys.exit(1)

    fps = float(re.search(r'fps\s*=\s*([\d.]+)', content).group(1)) if re.search(r'fps\s*=\s*([\d.]+)', content) else 30
    width = int(re.search(r'width\s*=\s*(\d+)', content).group(1)) if re.search(r'width\s*=\s*(\d+)', content) else 256
    height = int(re.search(r'height\s*=\s*(\d+)', content).group(1)) if re.search(r'height\s*=\s*(\d+)', content) else 144
    frame_count = int(re.search(r'frame_count\s*=\s*(\d+)', content).group(1)) if re.search(r'frame_count\s*=\s*(\d+)', content) else 0

    frames = re.findall(r'\b([0-9a-fA-F]{8,})\b', content)

    print(f"Extracted metadata:")
    print(f"  FPS: {fps}")
    print(f"  Resolution: {width}x{height}")
    print(f"  Frame count (declared): {frame_count}")
    print(f"  Frames found: {len(frames)}")

    return fps, width, height, frame_count, frames

def hex_to_bitmap(hex_string):
    bitmap = []
    for i in range(0, len(hex_string), 2):
        byte = int(hex_string[i:i+2], 16)
        for bit in range(7, -1, -1):
            bitmap.append((byte >> bit) & 1)
    return bitmap

def split_bitmap_32x18(bitmap, width=256, height=144):
    subframes = []
    for block_y in range(0, height, 18):
        for block_x in range(0, width, 32):
            subframe = []
            for y in range(block_y, block_y + 18):
                for x in range(block_x, block_x + 32):
                    subframe.append(bitmap[y * width + x])
            subframes.append(subframe)
    return subframes


def bitmap_to_hex_string(bitmap_data):
    bytes_data = bytearray()
    for i in range(0, len(bitmap_data), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bitmap_data) and bitmap_data[i + j]:
                byte |= (1 << (7 - j))
        bytes_data.append(byte)
    return ''.join(f'{b:02x}' for b in bytes_data)

def index_to_name(index):
    # Converts 0 → 'aaa', 1 → 'aab', ..., 17575 → 'zzz'
    letters = []
    for _ in range(3):
        letters.append(chr(ord('a') + (index % 26)))
        index //= 26
    return 'fg_' + ''.join(reversed(letters))

def write_lua_file(name, frames_data, output_dir):
    lua_code = "local frames = {\n"
    for i, subframes in enumerate(frames_data):
        lua_code += f"  [{i+1}] = {{\n"
        for j, sub in enumerate(subframes):
            hex_str = bitmap_to_hex_string(sub)
            lua_code += f'    section_{j+1:02d} = "{hex_str}",\n'
        lua_code += "  },\n"
    lua_code += "}\n\nreturn { frames = frames }\n"

    path = Path(output_dir) / f"{name}.lua"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(lua_code)

    print(f"✓ {name}.lua ({len(frames_data)} frames)")

def split_lua_file(input_file, output_dir=None):
    if output_dir is None:
        output_dir = Path("game_files/ReplicatedStorage/Video data") / Path(input_file).stem

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    print(f"Loading file '{input_file}'...")
    fps, width, height, total_frames, frames = extract_raw_frames(input_file)

    file_index = 0
    current_blob = []
    current_size = 0

    for frame_index, hex_frame in enumerate(frames):
        bitmap = hex_to_bitmap(hex_frame)
        subframes = split_bitmap_32x18(bitmap, width, height)

        # Estimate size of this frame
        estimated = sum(len(bitmap_to_hex_string(sub)) for sub in subframes)

        if len(current_blob) >= FRAMES_PER_FILE or (current_size + estimated) > MAX_SOURCE:
            name = index_to_name(file_index)
            write_lua_file(name, current_blob, output_path)
            file_index += 1
            current_blob = []
            current_size = 0

        current_blob.append(subframes)
        current_size += estimated

    if current_blob:
        name = index_to_name(file_index)
        write_lua_file(name, current_blob, output_path)

    # Manifest
    manifest = {
        'total_frames': len(frames),
        'sections_per_frame': SECTIONS_PER_FRAME,
        'width': width,
        'height': height,
        'fps': fps,
        'frames_per_file': FRAMES_PER_FILE,
        'max_source_chars': MAX_SOURCE
    }

    manifest_file = Path(output_path) / "manifest.lua"
    manifest_lua = "local manifest = {\n"
    for key, value in manifest.items():
        manifest_lua += f"  {key} = {repr(value)},\n"
    manifest_lua += "}\n\nreturn manifest\n"

    with open(manifest_file, 'w', encoding='utf-8') as f:
        f.write(manifest_lua)

    print(f"\n✓ Split complete!")
    print(f"  Output directory: {output_dir}")
    print(f"  Manifest: {manifest_file}")

def main():
    parser = argparse.ArgumentParser(
        description='Split a Lua file into 16-section frames (32x18), grouped into Studio-safe 4-frame blobs',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('input', help='Input Lua file with full-frame hex strings')
    parser.add_argument('-o', '--output', help='Output directory (default: input_stem_frames)')

    args = parser.parse_args()
    split_lua_file(args.input, args.output)

if __name__ == '__main__':
    main()
