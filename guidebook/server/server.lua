print('Server script loaded')

-- Debug helper
local function Debug(msg)
    print('^5[Guidebook Server]^7 ' .. msg)
end

-- Improved data handling
RegisterNetEvent('guidebook:getData')
AddEventHandler('guidebook:getData', function(data)
    local source = source
    if not source then return end
    local resourcePath = GetResourcePath(GetCurrentResourceName())
    local file = io.open(resourcePath .. '/ui/mockdata.json', 'r')
    
    if file then
        local content = file:read('*all')
        file:close()
        
        -- Improved error handling for JSON decode
        local success, decodedData = pcall(json.decode, content)
        if success then
            if data and data.pageId then
                -- Find specific page content
                for _, category in ipairs(decodedData.categories) do
                    for _, page in ipairs(category.pages) do
                        if page.label == data.pageId then
                            TriggerClientEvent('guidebook:receiveData', source, {
                                pageContent = {
                                    label = page.label,
                                    content = page.content
                                }
                            })
                            return
                        end
                    end
                end
            end
            -- Send full data if no specific page requested
            Debug('Sending data to client...')
            TriggerClientEvent('guidebook:receiveData', source, decodedData)
        else
            Debug('Failed to decode JSON, using fallback')
            TriggerClientEvent('guidebook:receiveData', source, {
                title = "Error Loading Data",
                categories = {}
            })
        end
    else
        Debug('mockdata.json not found at: ' .. resourcePath .. '/ui/mockdata.json')
        TriggerClientEvent('guidebook:receiveData', source, {
            title = "Error: Data File Missing",
            categories = {}
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