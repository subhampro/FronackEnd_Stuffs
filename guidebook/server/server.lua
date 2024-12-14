--[[
    🎮 FiveM Guidebook Server
    ------------------------
    The backend mastermind that keeps everything running
    Created by someone who drinks too much coffee

    Pro tips:
    - Don't touch what you don't understand
    - If it works, don't fix it
    - If you break it, pretend you were never here
--]]

-- Our trusty debug function, because print statements are for rookies
local function Debug(msg)
    print('^5[Guidebook Server]^7 ' .. msg)
end

-- Add these variables at the top
local requestCooldowns = {}
local COOLDOWN_TIME = 1000 -- 1 second cooldown between requests per client

-- Event handlers below ⬇️
-- Handle with care, they're more fragile than my self-esteem

print('Server script loaded')

-- Improved data handling
RegisterNetEvent('guidebook:getData')
AddEventHandler('guidebook:getData', function(data)
    local source = source
    if not source then return end
    
    -- Update cooldown
    local currentTime = GetGameTimer()
    requestCooldowns[source] = currentTime
    
    Debug('getData called from source: ' .. source)
    
    local resourcePath = GetResourcePath(GetCurrentResourceName())
    local filePath = resourcePath .. '/ui/mockdata.json'
    local file = io.open(filePath, 'r')
    
    if not file then
        TriggerClientEvent('guidebook:receiveData', source, {
            type = "updateData",
            responseType = "error",
            error = "Data file not found"
        })
        return
    end
    
    local content = file:read('*all')
    file:close()
    content = content:gsub('^\239\187\191', '')
    content = content:gsub('^%s*(.-)%s*$', '%1')
    
    local success, decodedData = pcall(json.decode, content)
    if not success or not decodedData then
        TriggerClientEvent('guidebook:receiveData', source, {
            type = "updateData",
            responseType = "error",
            error = "Invalid JSON format"
        })
        return
    end
    
    -- Always send full data for search functionality
    if not data or not data.pageId then
        TriggerClientEvent('guidebook:receiveData', source, {
            type = "updateData",
            responseType = "full",
            data = decodedData
        })
        return
    end
    
    -- Handle page requests
    for _, category in pairs(decodedData.categories) do
        for _, page in pairs(category.pages) do
            if tostring(page.id) == tostring(data.pageId) then
                TriggerClientEvent('guidebook:receiveData', source, {
                    type = "updateData",
                    responseType = "page",
                    data = page
                })
                return
            end
        end
    end
    
    TriggerClientEvent('guidebook:receiveData', source, {
        type = "updateData",
        responseType = "error",
        error = "Page not found"
    })
end)

-- Add cleanup for player disconnect
AddEventHandler('playerDropped', function()
    local source = source
    requestCooldowns[source] = nil
end)

-- Data saving functionality
RegisterNetEvent('guidebook:saveData')
AddEventHandler('guidebook:saveData', function(data)
    if not data then 
        Debug('No data provided to save')
        return 
    end
    
    local resourcePath = GetResourcePath(GetCurrentResourceName())
    local filePath = resourcePath .. '/ui/mockdata.json'
    
    -- Backup existing file first
    local backupPath = resourcePath .. '/ui/mockdata.backup.json'
    local currentFile = io.open(filePath, 'r')
    if currentFile then
        local currentContent = currentFile:read('*all')
        currentFile:close()
        
        local backupFile = io.open(backupPath, 'w')
        if backupFile then
            backupFile:write(currentContent)
            backupFile:close()
            Debug('Created backup of existing data')
        end
    end
    
    -- Save new data
    local file = io.open(filePath, 'w')
    if file then
        local content = json.encode(data)
        file:write(content)
        file:close()
        Debug('Data saved successfully to mockdata.json')
        
        -- Notify all clients to refresh their data
        TriggerClientEvent('guidebook:receiveData', -1, {
            type = "updateData",
            responseType = "full",
            data = data
        })
    else
        Debug('Failed to save data to mockdata.json')
    end
end)

-- Server is always ready now (no Node.js dependency)
RegisterNetEvent('guidebook:checkServer')
AddEventHandler('guidebook:checkServer', function()
    local source = source
    TriggerClientEvent('guidebook:serverStatus', source, true)
end)