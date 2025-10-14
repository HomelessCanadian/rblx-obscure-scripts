--[[
  ░▒▓█ 1-BIT VIDEO PLAYER █▓▒░
  2025-10-12 14:58 EDT
  Authored by Isabel + Copilot + Claude

  📦 SETUP:
    - Place all frame chunks (fg_aaa, fg_aab, ...) and Manifest inside "Video data" in ReplicatedStorage.
    - Manifest must define: total_frames, chunk_size, width, height, fps.
    - For custom videos, you'll need to encode your own frames. Visit https://github.com/HomelessCanadian/rblx-obscure-scripts and look for "1bitVideoPlayer"

  🧱 GRID: 
    - Creates a SurfaceGUI part to render a 256x144 raster screen with black and white capabilities

  🎞️ PLAYBACK:
    - Decodes compressed hex frames from ModuleScripts.
    - Updates grid at specified FPS.
    
  This code is open source. Feel free to distribute and modify as needed. See Github for more info and support. Please retain this helper message if distributing.
--]]

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

-- CONFIG
local pixelSize = 0.5
local spacing = 0.51
local frameRate = 30
local current_frame = 1
local isPlaying = false
local TEST_MODE = false -- (set to false when using video. test frame included in 2-8_Grid)

-- STATE
local pixels = {}
local gridReady = false
local screenPart = nil
local surfaceGui = nil

-- DATA MODULES
local dataFolder = ReplicatedStorage:WaitForChild("Video data")
local manifest = require(dataFolder:WaitForChild("Manifest"))

local gridWidth = manifest.width
local gridHeight = manifest.height
local chunkSize = manifest.frames_per_file

-- === LOAD ALL CHUNKS ===
local chunks = {}
local chunkNames = {}

for _, child in ipairs(dataFolder:GetChildren()) do
    if child:IsA("ModuleScript") and child.Name:match("^fg_") then
        table.insert(chunkNames, child.Name)
    end
end

table.sort(chunkNames) -- Canonical order: fg_aaa < fg_aab < fg_aac ... I used letters to force the correct order bc I can

for _, name in ipairs(chunkNames) do
    table.insert(chunks, require(dataFolder:WaitForChild(name)))
end

-- === DECODE FUNCTION (base16, 1-bit) ===
local function decode_frame(hex)
    local bitmap = {}
    for i = 1, #hex, 2 do
        local hexPair = hex:sub(i, i+1)
        local byte = tonumber(hexPair, 16)
        if byte then
            for bit = 7, 0, -1 do
                table.insert(bitmap, bit32.band(bit32.rshift(byte, bit), 1))
            end
        else
            warn("🧨 Invalid hex at position " .. i .. ": " .. hexPair)
        end
    end
    return bitmap
end

-- === CLEANUP + INIT GRID ===
local function cleanupGrid()
    for _, pixel in ipairs(pixels) do
        pixel:Destroy()
    end
    pixels = {}
    gridReady = false
    if screenPart then screenPart:Destroy() end
end

local function initializeGrid()
    screenPart = Instance.new("Part")
    screenPart.Name = "PixelScreen"
    screenPart.Size = Vector3.new(gridWidth * pixelSize, gridHeight * pixelSize, 1)
    screenPart.Anchored = true
    screenPart.CanCollide = false
    screenPart.Position = Vector3.new(0, 72 / 2 + 1, 512 / 2)
    screenPart.Parent = workspace

    surfaceGui = Instance.new("SurfaceGui")
    surfaceGui.Face = Enum.NormalId.Front
    surfaceGui.CanvasSize = Vector2.new(gridWidth, gridHeight)
    surfaceGui.Adornee = screenPart
    surfaceGui.Parent = screenPart

    task.spawn(function()
        for y = 0, gridHeight - 1 do
            for x = 0, gridWidth - 1 do
                local frame = Instance.new("Frame")
                frame.Size = UDim2.new(0, 1, 0, 1)
                frame.Position = UDim2.new(0, x, 0, y)
                frame.BackgroundColor3 = Color3.new(0, 0, 0)
                frame.BorderSizePixel = 0
                frame.Parent = surfaceGui
                table.insert(pixels, frame)
            end
        end
        gridReady = true
        isPlaying = true -- temporary while I wire in buttons
        print("✅ GUI grid ready. Starting playback.")
    end)
end

local function resetPlayback()
    isPlaying = false
    current_frame = 1
    cleanupGrid()
    initializeGrid()
end

-- === FRAME LOADER (video) ===
local function get_frame(global_index)
    local chunk_index = math.floor((global_index - 1) / chunkSize) + 1
    local local_index = ((global_index - 1) % chunkSize) + 1
    local chunk = chunks[chunk_index]
    local chunk_name = chunkNames[chunk_index] or ("[unknown chunk #" .. chunk_index .. "]")

    if not chunk or not chunk.frames then
        error("🧨 Chunk " .. chunk_index .. " (" .. chunk_name .. ") is missing or invalid.")
    end

    local frame = chunk.frames[local_index]
    if not frame then
        error("🧨 Frame " .. local_index .. " missing in chunk " .. chunk_index .. " (" .. chunk_name .. ")")
    end

    local subframeWidth = 32
    local subframeHeight = 18
    local subframesPerRow = 8
    local subframesPerCol = 8
    local fullWidth = subframeWidth * subframesPerRow
    local fullHeight = subframeHeight * subframesPerCol

    local bitmap = table.create(fullWidth * fullHeight, 0)

    for subY = 0, subframesPerCol - 1 do
        for subX = 0, subframesPerRow - 1 do
            local sectionIndex = subY * subframesPerRow + subX + 1
            local key = string.format("section_%02d", sectionIndex)
            local hex = frame[key]
            if not hex or #hex ~= 144 then
                warn("🧨 Missing or invalid " .. key .. " in frame " .. local_index .. " of chunk " .. chunk_name)
                continue
            end
            local subBitmap = decode_frame(hex)
            for y = 0, subframeHeight - 1 do
                for x = 0, subframeWidth - 1 do
                    local subIndex = y * subframeWidth + x + 1
                    local fullX = subX * subframeWidth + x
                    local fullY = subY * subframeHeight + y
                    local fullIndex = fullY * fullWidth + fullX + 1
                    bitmap[fullIndex] = subBitmap[subIndex]
                end
            end
        end
    end

    return bitmap
end

-- === TEST FRAME LOADER ===
local function load_test_frame_from_storage()
    local testFrame = require(ReplicatedStorage.test["2-8_Grid"])
    local subframeWidth = 32
    local subframeHeight = 18
    local fullWidth = 256
    local fullHeight = 144

    local bitmap = table.create(fullWidth * fullHeight, 0)

    for sectionIndex = 1, 64 do
        local key = string.format("section_%02d", sectionIndex)
        local hex = testFrame[key]
        if not hex or #hex ~= 144 then
            warn("⚠️ Missing or invalid " .. key .. " (expected 144 hex chars, got " .. (#hex or 0) .. ")")
            continue
        end
        local subBitmap = decode_frame(hex)
        local subX = (sectionIndex - 1) % 8
        local subY = math.floor((sectionIndex - 1) / 8)
        for y = 0, subframeHeight - 1 do
            for x = 0, subframeWidth - 1 do
                local subIndex = y * subframeWidth + x + 1
                local fullX = subX * subframeWidth + x
                local fullY = subY * subframeHeight + y
                local fullIndex = fullY * fullWidth + fullX + 1
                bitmap[fullIndex] = subBitmap[subIndex]
            end
        end
    end

    return bitmap
end

-- === PLAYBACK LOOP ===
RunService.Heartbeat:Connect(function()
    if not isPlaying or not gridReady then return end

    local bitmap = TEST_MODE and load_test_frame_from_storage() or get_frame(current_frame)
    if not bitmap then
        warn("🧨 Frame returned nil bitmap.")
        return
    end

    for i = 1, #pixels do
        local value = bitmap[i] or 0
        pixels[i].BackgroundColor3 = value == 1 and Color3.new(1, 1, 1) or Color3.new(0, 0, 0)
    end

    if not TEST_MODE then
        current_frame += 1
        if current_frame > manifest.total_frames then
            current_frame = 1
        end
    end
end)

-- === INIT ===
initializeGrid()
