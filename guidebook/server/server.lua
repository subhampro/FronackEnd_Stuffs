print('Server script loaded')

-- Debug helper
local function Debug(msg)
    print('^5[Guidebook Server]^7 ' .. msg)
end

-- Improved data handling
RegisterNetEvent('guidebook:getData')
AddEventHandler('guidebook:getData', function()
    local source = source
    local resourcePath = GetResourcePath(GetCurrentResourceName())
    local file = io.open(resourcePath .. '/ui/mockdata.json', 'r')
    
    if file then
        local content = file:read('*all')
        file:close()
        
        -- Improved error handling for JSON decode
        local success, decodedData = pcall(json.decode, content)
        if success then
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