-- RGB color cycle script for multiple parts
-- Originally for a keyboard model to simulate backlighting
-- (c) 2025 Pank, Copilot

local model = script.Parent -- Insert the script in the model containing the target parts
local partno = 6 -- Change this to your bl part number starting at 0 
local parts = {} -- table to be populated by the "initialize parts" function
local waitTime = math.random(7,10) / 100 -- standard cycle
local waveDelay = math.random(70,180) / 100 -- Delay between each part's color update
local loopOffset = math.random(25,125) / 100 -- Delay start per script
local rMin = 0 -- Set minimum and maximum rgb values here vvvvv
local gMin = 0
local bMin = 0
local rMax = 255
local gMax = 255
local bMax = 255
local verbose = true

if verbose == true then
	for i = 0, partno do -- Initialize parts
		local part = model:WaitForChild("bl" .. i)
		print("Found " .. part.Name)
		table.insert(parts, part)
	end
	print("waitTime set to " .. waitTime .. " seconds.")
	print("waveDelay set to " .. waveDelay .. " seconds.")
	print("loopOffset set to " .. loopOffset .. " seconds.")
else
    for i = 0, partno do -- Initialize parts part II
        local part = model:WaitForChild("bl" .. i)
        table.insert(parts, part)
    end
end

-- Helper function to set color on all parts with offset
local function waveColor(r, g, b)
	for i, part in ipairs(parts) do
		delay((i - 1) * waveDelay, function()
			part.Color = Color3.fromRGB(r, g, b)
		end)
	end
end

-- Begin RGB loop
wait(loopOffset)
while true do
	for g = gMin, gMax do
		waveColor(rMax, g, bMin)
		wait(waitTime)
	end

	for r = rMax, rMin, -1 do
		waveColor(r, gMax, bMin)
		wait(waitTime)
	end

	for b = bMin, bMax do
		waveColor(rMin, gMax, b)
		wait(waitTime)
	end

	for g = gMax, gMin, -1 do
		waveColor(rMin, g, bMax)
		wait(waitTime)
	end

	for r = rMin, rMax do
		waveColor(r, gMin, bMax)
		wait(waitTime)
	end

	for b = bMax, bMin, -1 do
		waveColor(rMax, gMin, b)
		wait(waitTime)
	end
end
