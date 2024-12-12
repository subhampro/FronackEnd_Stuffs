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
            for _, category in pairs(decodedData.categories or {}) do
                for _, page in pairs(category.pages or {}) do
                    if page.label == data.pageId then
                        Debug('Found page: ' .. page.label)
                        TriggerClientEvent('guidebook:receiveData', source, {
                            type = "page",
                            pageContent = {
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
                type = "full",
                data = decodedData
            })
        end
    else
        Debug('JSON decode error. Content preview: ' .. content:sub(1, 100))
        TriggerClientEvent('guidebook:receiveData', source, {
            type = "error",
            error = "Invalid JSON format"
        })
    end
end)

-- Data saving functionality
RegisterNetEvent('guidebook:saveData')
AddEventHandler('guidebook:saveData', function(data)
    local resourcePath = GetResourcePath(GetCurrentResourceName())
    local file = io.open(resourcePath .. '/data.json', 'w')
    
    if file then
        file:write(json.encode(data))
        file:close()
        Debug('Data saved successfully')
    else
        Debug('Failed to save data')
    end
end)

-- Server is always ready now (no Node.js dependency)
RegisterNetEvent('guidebook:checkServer')
AddEventHandler('guidebook:checkServer', function()
    local source = source
    TriggerClientEvent('guidebook:serverStatus', source, true)
end)