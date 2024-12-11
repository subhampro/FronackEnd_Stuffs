--[[
    📱 FiveM Guidebook Client
    ------------------------
    The front-end warrior that makes everything look pretty
    
    Warning: Contains more variables than my ex's mood swings
    Handle with care and lots of caffeine ☕
--]]

-- Keeping track of our UI state
-- Because boolean variables are the only stable thing in this code
local display = false
local serverReady = false

-- Debug function that's probably used more than actual code
local function Debug(msg)
    print('^3[Guidebook Debug]^7 ' .. msg)
end

-- Let's make sure everything is set up properly when the resource starts
CreateThread(function()
    Wait(500) -- Give it a moment to breathe
    SetDisplay(false) -- Just in case, let's make sure it starts hidden
    Wait(500)
    SetDisplay(false) -- Double check because sometimes it can be stubborn
    Wait(1000) -- Little breather before we add the commands
    
    -- Add some helpful chat suggestions
    TriggerEvent('chat:addSuggestion', '/help', 'Open the guidebook')
    TriggerEvent('chat:addSuggestion', '/closeui', 'Force close UI if stuck')
    Debug('All good! Resource is up and running with commands ready to go')
    
    Wait(1000)
    CheckServerStatus()
    
    -- Periodically check server status
    while true do
        Wait(30000) -- Check every 30 seconds
        CheckServerStatus()
    end
end)

-- Quick escape hatch if the UI gets stuck
RegisterCommand('closeui', function()
    SetDisplay(false)
end, false)

-- Add server status event handler
RegisterNetEvent('guidebook:serverStatus')
AddEventHandler('guidebook:serverStatus', function(status)
    serverReady = status
    Debug('Server status updated: ' .. (status and 'Online' or 'Offline'))
end)

-- Check if server is ready (simplified)
function CheckServerStatus()
    TriggerServerEvent('guidebook:checkServer')
end

-- The main command to open/close the guidebook
RegisterCommand('help', function()
    Debug('Help command triggered')
    
    if not serverReady then
        TriggerEvent('chat:addMessage', {
            color = {255, 0, 0},
            multiline = true,
            args = {"System", "Guidebook server is starting up. Please wait..."}
        })
        CheckServerStatus()
        return
    end
    
    SetDisplay(not display)
end, false)

-- Handle the 'close' button click from the UI
RegisterNUICallback('close', function(data, cb)
    Debug('Alright, closing time!')
    display = false
    SetNuiFocus(false, false)
    SendNUIMessage({
        type = "ui",
        status = false
    })
    Debug('See ya later!')
    cb('ok')
end)

-- UI letting us know it's ready to rock
RegisterNUICallback('uiReady', function(data, cb)
    Debug('UI is good to go!')
    cb('ok')
end)

-- Modified getData callback handler
RegisterNUICallback('getData', function(data, cb)
    if not serverReady then
        cb({ error = "Server not ready" })
        return
    end
    
    TriggerServerEvent('guidebook:getData', data)
    cb({})
end)

-- Add new event handler for receiving data
RegisterNetEvent('guidebook:receiveData')
AddEventHandler('guidebook:receiveData', function(response)
    if not response then return end
    
    if response.type == "error" then
        Debug('Error: ' .. tostring(response.error))
        return
    end
    
    SendNUIMessage({
        type = "updateData",
        responseType = response.type,
        data = response.type == "full" and response.data or response.pageContent
    })
end)

-- The magic that makes the display work
function SetDisplay(bool)
    display = bool
    SetNuiFocus(bool, bool)
    SendNUIMessage({
        type = "ui",
        status = bool,
        resourceName = GetCurrentResourceName()
    })
    
    -- Request data when UI opens
    if bool then
        TriggerServerEvent('guidebook:getData')
    end
    
    Debug('Display is now ' .. (bool and 'visible' or 'hidden'))
end