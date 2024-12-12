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

-- Event handlers below ⬇️
-- Handle with care, they're more fragile than my self-esteem

print('Server script loaded')

-- Improved data handling
RegisterNetEvent('guidebook:getData')
AddEventHandler('guidebook:getData', function(data)
    local source = source
    if not source then return end
    
    -- Fix the file path to ensure it's correct
    local resourcePath = GetResourcePath(GetCurrentResourceName())
    local filePath = resourcePath .. '/ui/mockdata.json'
    Debug('Attempting to read file: ' .. filePath)
    
    local file = io.open(filePath, 'r')
    if not file then
        Debug('File not found at path: ' .. filePath)
        TriggerClientEvent('guidebook:receiveData', source, {
            type = "error",
            error = "Data file missing"
        })
        return
    end
    
    -- Read content and remove potential BOM and whitespace
    local content = file:read('*all')
    file:close()
    
    -- Remove UTF-8 BOM if present
    content = content:gsub('^\239\187\191', '')
    -- Trim whitespace
    content = content:gsub('^%s*(.-)%s*$', '%1')
    
    -- Try to decode JSON
    local success, decodedData = pcall(json.decode, content)
    if success and decodedData then
        if data and data.pageId then
            Debug('Looking for page: ' .. data.pageId)
            for _, category in pairs(decodedData.categories or {}) do
                for _, page in pairs(category.pages or {}) do
                    -- Match by page ID
                    if page.id == data.pageId then
                        Debug('Found page: ' .. page.label)
                        TriggerClientEvent('guidebook:receiveData', source, {
                            type = "updateData",
                            responseType = "page",
                            data = {
                                label = page.label,
                                content = page.content
                            }
                        })
                        return
                    end
                end
            end
            -- Page not found
            Debug('Page not found: ' .. tostring(data.pageId))
            TriggerClientEvent('guidebook:receiveData', source, {
                type = "error",
                error = "Page not found"
            })
        else
            -- Send full data
            Debug('Sending full data to client...')
            TriggerClientEvent('guidebook:receiveData', source, {
                type = "updateData",
                responseType = "full",
                data = decodedData
            })
        end
    else
        Debug('JSON decode error')
        TriggerClientEvent('guidebook:receiveData', source, {
            type = "updateData",
            responseType = "error",
            error = "Invalid JSON format"
        })
    end

    -- Add admin check
    if data and data.admin then
        Debug('Admin UI requested data')
    end
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