# rblx-obscure-scripts
A collection of roblox-specific lua utilities
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

(c) 2025 Pank, Copilot. Shell License. See Shell_License.md for details.