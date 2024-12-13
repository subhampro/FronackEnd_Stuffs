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

-- Add these variables at the top
local tabletProp = nil
local tabletDict = "amb@code_human_in_bus_passenger_idles@female@tablet@base"
local tabletAnim = "base"
local isAnimPlaying = false

-- Add this variable to track animation state
local lastAnimState = false

-- Add this at the top with other variables
local animationThread = nil

-- Add admin UI state
local adminDisplay = false

-- Add these variables at the top
local lastDataRequest = 0
local DATA_REQUEST_COOLDOWN = 1000 -- 1 second between requests

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

-- Update the helpadmin command to specifically load admin UI
RegisterCommand('helpadmin', function()
    Debug('Admin command triggered')
    
    -- Force cleanup of UI states first
    display = false
    adminDisplay = false
    SetNuiFocus(false, false)
    RemoveTablet()
    isAnimPlaying = false
    lastAnimState = false
    
    -- Important: Send cleanup messages in correct order
    SendNUIMessage({
        type = "ui",
        status = false,
        isAdmin = false
    })
    
    Wait(500) -- Important delay between cleanup and new state
    
    if not serverReady then
        TriggerEvent('chat:addMessage', {
            color = {255, 0, 0},
            multiline = true,
            args = {"System", "Guidebook server is starting up. Please wait..."}
        })
        CheckServerStatus()
        return
    end
    
    -- Force load admin page
    SendNUIMessage({
        type = "loadAdmin",
        status = true,
        url = 'guidebook-admin.html'
    })
    
    Wait(200) -- Wait for page load
    
    -- Set new admin state
    SendNUIMessage({
        type = "ui",
        status = true,
        isAdmin = true
    })
    
    Wait(100)
    
    -- Set focus and state
    adminDisplay = true
    SetNuiFocus(true, true)
    
    Debug('Admin Display is now visible')
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

-- Modify the close callback to ensure animation stops
RegisterNUICallback('close', function(data, cb)
    Debug('Closing UI...')
    display = false
    adminDisplay = false
    SetNuiFocus(false, false)
    
    -- Force stop animation and remove prop
    local ped = PlayerPedId()
    ClearPedTasks(ped)
    ClearPedSecondaryTask(ped)
    RemoveTablet()
    
    -- Reset all animation states
    isAnimPlaying = false
    lastAnimState = false
    if animationThread then
        animationThread = nil
    end
    
    SendNUIMessage({
        type = "ui",
        status = false
    })
    
    -- Double check cleanup after a small delay
    SetTimeout(500, function()
        if tabletProp then
            DeleteObject(tabletProp)
            tabletProp = nil
        end
        ClearPedTasks(PlayerPedId())
    end)
    
    cb('ok')
end)

-- UI letting us know it's ready to rock
RegisterNUICallback('uiReady', function(data, cb)
    Debug('UI is good to go!')
    cb('ok')
end)

-- Add this throttling function
local function canRequestData()
    local currentTime = GetGameTimer()
    if (currentTime - lastDataRequest) < DATA_REQUEST_COOLDOWN then
        return false
    end
    lastDataRequest = currentTime
    return true
end

-- Update the getData callback handler to properly pass the page ID
RegisterNUICallback('getData', function(data, cb)
    if not serverReady then
        cb({ error = "Server not ready" })
        return
    end
    
    if not canRequestData() then
        cb({ error = "Too many requests" })
        return
    end
    
    TriggerServerEvent('guidebook:getData', data)
    cb({})
end)

RegisterNUICallback('saveData', function(data, cb)
    if not serverReady then
        cb({ error = "Server not ready" })
        return
    end
    
    TriggerServerEvent('guidebook:saveData', data)
    cb({})
end)

-- Add new event handler for receiving data
RegisterNetEvent('guidebook:receiveData')
AddEventHandler('guidebook:receiveData', function(response)
    if not response then return end
    
    SendNUIMessage(response)
end)

-- The magic that makes the display work
function SetDisplay(bool)
    display = bool
    SetNuiFocus(bool, bool)
    
    if bool then
        -- Start animation
        LoadTabletAnimation()
        AttachTablet()
        
        local ped = PlayerPedId()
        if not isAnimPlaying and not IsPedDeadOrDying(ped, true) then
            TaskPlayAnim(ped, tabletDict, tabletAnim, 8.0, -8.0, -1, 49, 0, false, false, false)
            isAnimPlaying = true
            lastAnimState = true
            
            -- Start animation check thread
            if not animationThread then
                animationThread = CreateThread(function()
                    while display do
                        Wait(1000)
                        local ped = PlayerPedId()
                        if IsPedDeadOrDying(ped, true) then
                            RemoveTablet()
                            isAnimPlaying = false
                        elseif not isAnimPlaying and not IsPedDeadOrDying(ped, true) and lastAnimState then
                            LoadTabletAnimation()
                            AttachTablet()
                            TaskPlayAnim(ped, tabletDict, tabletAnim, 8.0, -8.0, -1, 49, 0, false, false, false)
                            isAnimPlaying = true
                        end
                    end
                    animationThread = nil
                end)
            end
        end
    else
        -- Stop animation and clean up
        RemoveTablet()
        isAnimPlaying = false
        lastAnimState = false
        
        -- Clear animation thread
        if animationThread then
            animationThread = nil
        end
    end
    
    -- Update: Add specific UI type
    SendNUIMessage({
        type = "switchPage",
        status = bool,
        page = 'regular'
    })
    
    if bool then
        Debug('Requesting initial data')
        TriggerServerEvent('guidebook:getData')
    end
    
    Debug('Display is now ' .. (bool and 'visible' or 'hidden'))
end

-- Update SetAdminDisplay function
function SetAdminDisplay(bool)
    -- Force cleanup first
    display = false
    adminDisplay = false
    SetNuiFocus(false, false)
    RemoveTablet()
    isAnimPlaying = false
    lastAnimState = false
    
    Wait(300)
    
    if bool then
        -- Set new state with single message
        SendNUIMessage({
            type = "ui",
            status = true,
            isAdmin = true
        })
        
        Wait(200)
        
        adminDisplay = true
        SetNuiFocus(true, true)
        
        LoadTabletAnimation()
        AttachTablet()
        
        local ped = PlayerPedId()
        if not IsPedDeadOrDying(ped, true) then
            TaskPlayAnim(ped, tabletDict, tabletAnim, 8.0, -8.0, -1, 49, 0, false, false, false)
            isAnimPlaying = true
            lastAnimState = true
        end
    else
        SendNUIMessage({
            type = "ui",
            status = false,
            isAdmin = true
        })
    end
end

-- Add handler for loading admin UI separately
RegisterNUICallback('loadAdminUI', function(data, cb)
    -- This will be called when the admin page needs to be loaded
    SendNUIMessage({
        type = "loadAdmin",
        status = true,
        url = "ui/guidebook-admin.html"
    })
    cb('ok')
end)

-- Add cleanup on resource stop
AddEventHandler('onResourceStop', function(resourceName)
    if (GetCurrentResourceName() ~= resourceName) then
        return
    end
    RemoveTablet()
end)

-- Add this function after existing variables
function LoadTabletAnimation()
    RequestAnimDict(tabletDict)
    while not HasAnimDictLoaded(tabletDict) do
        Wait(100)
    end
end

-- Add tablet prop management functions
function AttachTablet()
    if not tabletProp then
        RequestModel(`prop_cs_tablet`)
        while not HasModelLoaded(`prop_cs_tablet`) do
            Wait(100)
        end
        
        local ped = PlayerPedId()
        local bone = GetPedBoneIndex(ped, 28422) -- Right hand bone
        
        tabletProp = CreateObject(`prop_cs_tablet`, 0.0, 0.0, 0.0, true, true, true)
        AttachEntityToEntity(tabletProp, ped, bone, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, true, true, false, true, 1, true)
        SetModelAsNoLongerNeeded(`prop_cs_tablet`)
    end
end

-- Modify RemoveTablet function for better cleanup
function RemoveTablet()
    if tabletProp then
        DeleteObject(tabletProp)
        tabletProp = nil
    end
    
    local ped = PlayerPedId()
    ClearPedTasks(ped)
    ClearPedSecondaryTask(ped)
    
    if isAnimPlaying then
        StopAnimTask(ped, tabletDict, tabletAnim, 1.0)
        isAnimPlaying = false
    end
end

-- Remove the existing animation check thread since we now handle it in SetDisplay

-- Add new callback for switching between admin and regular UI
RegisterNUICallback('switchUI', function(data, cb)
    if data.admin then
        SetDisplay(false)
        SetAdminDisplay(true)
    else
        SetAdminDisplay(false)
        SetDisplay(true)
    end
    cb('ok')
end)

-- Add emergency cleanup command
RegisterCommand('fixui', function()
    Debug('Emergency UI cleanup triggered')
    display = false
    adminDisplay = false
    SetNuiFocus(false, false)
    RemoveTablet()
    isAnimPlaying = false
    lastAnimState = false
    if animationThread then
        animationThread = nil
    end
    
    -- Force send close message to NUI
    SendNUIMessage({
        type = "ui",
        status = false
    })
    SendNUIMessage({
        type = "switchPage",
        status = false
    })
end, false)