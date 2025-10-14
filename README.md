# rblx-obscure-scripts
A collection of roblox-specific lua utilities
---
ToC
1. [RGB script](https://github.com/HomelessCanadian/rblx-obscure-scripts?tab=readme-ov-file#roblox-rgb-keyboard-scripts)
2. [1-bit Video Player](https://github.com/HomelessCanadian/rblx-obscure-scripts?tab=readme-ov-file#%EF%B8%8F-1-bit-video-player-for-roblox-studio)
---
---
# Roblox RGB Keyboard Scripts

A pair of Lua scripts for simulating RGB backlighting effects on keyboard models in Roblox. Designed for flexibility, randomized timing, and easy customization.

## Scripts

- **color_prog.lua**  
  Controls a single part with a looping RGB color cycle. Includes randomized timing and startup offset for natural variation.

- **color_prog_multi.lua**  
  Controls multiple parts within a model, creating a wave-like RGB effect. Each part updates with a staggered delay, and timing is randomized per instance.

## Features

- Adjustable RGB bounds (`rMin`, `rMax`, etc.)
- Randomized `waitTime`, `waveDelay`, and `loopOffset` for each script
- Verbose logging for debugging
- Scalable part initialization using `partno` and `WaitForChild`

## Usage

Place the appropriate script inside the target part or model. Customize the parameters at the top of each script to match your setup. Scripts loop continuously once started.

---
---
---
# 🕹️ 1-Bit Video Player for Roblox Studio

A modular pipeline for converting grayscale videos into chunked Lua frame data, optimized for Roblox Studio playback.

---

## 📦 Overview

This toolchain lets you:

1. Convert any video into 1-bit hex-encoded frames  
2. Split those frames into Studio-safe Lua chunks  
3. Mass-import the chunks into Roblox Studio  
4. Play back the video using a custom renderer

---

## 🧰 Requirements

Install the following Python packages:

```bash
pip install opencv-python pillow pyautogui pyperclip keyboard
```

---

## 🎞️ Step 1: Convert Video to Lua Frames

Use `videoToLua16.py` to extract and encode frames:

```bash
python videoToLua16.py input.mp4 -o output.lua --threshold 128 --width 256 --height 144
```

- `input.mp4`: your source video  
- `output.lua`: full-frame hex strings  
- `--threshold`: grayscale cutoff (0–255)  
- `--width` / `--height`: resolution (must match your renderer)

---

## 📚 Step 2: Chunk Lua Frames for Studio

Use `luaBitmapChunker16.py` to split the output into Studio-safe blobs:

```bash
python luaBitmapChunker16.py output.lua -o "game_files/ReplicatedStorage/Video data"
```

- Default chunk size: 4 frames per file  
- Output: `fg_aaa.lua`, `fg_aab.lua`, ..., plus `manifest.lua`  
- Each file stays under Roblox’s 200k character limit

---

## 🚀 Step 3: Import into Roblox Studio

Use `studioMassImport.py` to automate the import:

```bash
python studioMassImport.py "game_files/ReplicatedStorage/Video data"
```

- Automatically copies Lua chunks to clipboard  
- Simulates paste + save in Studio  
- Requires Studio to be open and focused

---

## 🧠 Notes

- All scripts are modular — you can run them independently or wrap them as needed  
- Manifest includes metadata: resolution, FPS, frame count, chunk size  
- You can customize chunk size, naming scheme, and import behavior

---

(c) 2025 Pank, Copilot, Claude. Shell License. See Shell_License.md for details. Some components open source.
