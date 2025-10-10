-- RGB color cycle script for a single part
-- Originally for a keyboard model to simulate backlighting
-- (c) 2025 Pank, Copilot

local part = script.Parent -- Insert the script in the target part
local waitTime = math.random(7,10) / 100 -- standard cycle
local loopOffset = math.random(25,125) / 100 -- Delay start per script
local rMin = 0 -- Set minimum and maximum rgb values here vvvvv
local rMax = 255
local gMin = 0
local gMax = 255
local bMin = 0
local bMax = 255
local verbose = true -- logging
local function partColor(r, g, b) -- set up link to color values
	part.Color = Color3.fromRGB(r, g, b)
end

if verbose == true then -- print all randomized values to console, for debugging
	print("waitTime is "..waitTime)
	print("loopOffset is "..loopOffset)
end

wait(loopOffset)

-- Begin color cycle

while true do
	for g = gMin, gMax do
		partColor(rMax, g, bMin)
		wait(waitTime)
	end

	for r = rMax, rMin, -1 do
		partColor(r, gMax, bMin)
		wait(waitTime)
	end

	for b = bMin, bMax do
		partColor(rMin, gMax, b)
		wait(waitTime)
	end

	for g = gMax, gMin, -1 do
		partColor(rMin, g, bMax)
		wait(waitTime)
	end

	for r = rMin, rMax do
		partColor(r, gMin, bMax)
		wait(waitTime)
	end

	for b = bMax, bMin, -1 do
		partColor(rMax, gMin, b)
		wait(waitTime)
	end
end
