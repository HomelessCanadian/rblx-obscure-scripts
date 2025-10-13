#!/usr/bin/env python3
"""
Convert video frames to base256-encoded Lua bitmap tables.
Output: Lua table with raw byte strings for each frame.
Copyright (c) 2025 Claude, Copilot, Pank. Shell license.
"""

import argparse
import cv2
import sys
from pathlib import Path

def bitmap_to_hex_string(bitmap_data):
    bytes_data = bytearray()
    for i in range(0, len(bitmap_data), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bitmap_data) and bitmap_data[i + j]:
                byte |= (1 << (7 - j))
        bytes_data.append(byte)
    return ''.join(f'{b:02x}' for b in bytes_data)

def video_to_lua_bitmap(video_path, output_path, width=None, height=None, threshold=128):
    """Convert video to Lua bitmap format with raw byte encoding."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_path}'", file=sys.stderr)
        sys.exit(1)

    # Get native resolution
    native_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    native_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Determine target resolution
    target_width = width if width else native_width
    target_height = height if height else native_height

    print(f"Video: {total_frames} frames at {fps:.2f} FPS")
    print(f"Native resolution: {native_width}x{native_height}")
    print(f"Target resolution: {target_width}x{target_height}")
    print(f"Threshold: {threshold}")
    print(f"Processing frames with raw byte encoding...")

    frames_data = []
    frame_idx = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (target_width, target_height), interpolation=cv2.INTER_AREA)
            _, binary = cv2.threshold(resized, threshold, 255, cv2.THRESH_BINARY)

            frame_data = [1 if pixel > 128 else 0 for row in binary for pixel in row]
            lua_encoded = bitmap_to_hex_string(frame_data)
            frames_data.append(lua_encoded)

            frame_idx += 1
            if frame_idx % 100 == 0 or frame_idx == total_frames:
                print(f"  Processed {frame_idx}/{total_frames} frames")

    finally:
        cap.release()

    # Generate Lua output
    lua_code = "local bitmaps = {\n"
    lua_code += f"  width = {target_width},\n"
    lua_code += f"  height = {target_height},\n"
    lua_code += f"  fps = {fps:.2f},\n"
    lua_code += f"  frame_count = {len(frames_data)},\n"
    lua_code += "  frames = {\n"
    for idx, lua_str in enumerate(frames_data):
        lua_code += f"    {lua_str},\n"
        if (idx + 1) % 100 == 0:
            print(f"  Generated Lua for {idx + 1}/{len(frames_data)} frames")
    lua_code += "  }\n"
    lua_code += "}\n\n"

    # Lua decoder for raw byte strings
    lua_code += """local function decode_frame(raw)
  local bitmap = {}
  for i = 1, #raw do
    local byte = string.byte(raw, i)
    for bit = 7, 0, -1 do
      table.insert(bitmap, bit32.band(bit32.rshift(byte, bit), 1))
    end
  end
  return bitmap
end

bitmaps.decode = decode_frame
return bitmaps
"""

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(lua_code)
        file_size = Path(output_path).stat().st_size / (1024 * 1024)
        print(f"\n✓ Conversion complete!")
        print(f"  Frames: {len(frames_data)}")
        print(f"  Output file: {output_path}")
        print(f"  File size: {file_size:.2f} MB")
    except IOError as e:
        print(f"Error: Could not write output file: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Convert video to base256-encoded Lua bitmap table format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python video_to_lua_base256.py video.mp4 output.lua
  python video_to_lua_base256.py video.mp4 output.lua --threshold 150
  python video_to_lua_base256.py video.mp4 output.lua -w 256 -h 144

Usage in Lua/Roblox:
  local bitmaps = require(script.Parent:WaitForChild("output"))
  local bitmap = bitmaps.decode(bitmaps.frames[1])
  for y = 1, bitmaps.height do
    for x = 1, bitmaps.width do
      local pixel = bitmap[(y-1) * bitmaps.width + x]
      if pixel == 1 then
        -- draw white pixel
      end
    end
  end
        """
    )

    parser.add_argument('input', help='Input video file (MP4, AVI, etc.)')
    parser.add_argument('output', help='Output Lua file')
    parser.add_argument('-w', '--width', type=int, help='Target width in pixels')
    parser.add_argument('-ht', '--height', type=int, help='Target height in pixels')
    parser.add_argument('-t', '--threshold', type=int, default=128, help='Brightness threshold (default: 128)')

    args = parser.parse_args()
    video_to_lua_bitmap(args.input, args.output, args.width, args.height, args.threshold)

if __name__ == '__main__':
    main()
