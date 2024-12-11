print('Server script loaded')
local nodeProcess = nil
local isNodeServerRunning = false
local maxRetries = 5
local retryDelay = 2000 -- 2 seconds

-- Debug helper
local function Debug(msg)
    print('^5[Guidebook Server]^7 ' .. msg)
end

-- Function to start Node.js server
local function StartNodeServer()
    Debug('Starting Node.js server...')
    
    -- Get resource path
    local resourcePath = GetResourcePath(GetCurrentResourceName())
    local serverPath = resourcePath .. '/server/node'
    
    -- Build and start Node.js server
    CreateThread(function()
        -- First, run npm install
        os.execute('cd "' .. serverPath .. '" && npm install')
        Debug('Node dependencies installed')
        
        -- Then start the server
        os.execute('cd "' .. serverPath .. '" && npm run build && node server.js &')
        Debug('Node.js server started')
        
        -- Wait a moment for server to initialize
        Wait(2000)
        
        -- Check if server is running
        VerifyNodeServer()
    end)
end

-- Function to verify Node.js server is running
function VerifyNodeServer()
    local tries = 0
    
    local function CheckServer()
        tries = tries + 1
        PerformHttpRequest('http://localhost:3000/api/status', function(errorCode, resultData, resultHeaders)
            if errorCode == 200 then
                isNodeServerRunning = true
                Debug('Node.js server is running!')
                TriggerClientEvent('guidebook:serverStatus', -1, true)
            else
                if tries < maxRetries then
                    Debug('Server check attempt ' .. tries .. ' failed, retrying...')
                    SetTimeout(retryDelay, CheckServer)
                else
                    Debug('Failed to verify Node.js server after ' .. maxRetries .. ' attempts')
                    TriggerClientEvent('guidebook:serverStatus', -1, false)
                end
            end
        end)
    end
    
    CheckServer()
end

-- Start server when resource starts
AddEventHandler('onResourceStart', function(resourceName)
    if (GetCurrentResourceName() ~= resourceName) then
        return
    end
    StartNodeServer()
end)

-- Cleanup when resource stops
AddEventHandler('onResourceStop', function(resourceName)
    if (GetCurrentResourceName() ~= resourceName) then
        return
    end
    -- Kill Node.js server
    if isNodeServerRunning then
        os.execute('taskkill /F /IM node.exe >nul 2>&1')
        Debug('Node.js server stopped')
    end
end)

-- Server status check endpoint
RegisterNetEvent('guidebook:checkServer')
AddEventHandler('guidebook:checkServer', function()
    local source = source
    TriggerClientEvent('guidebook:serverStatus', source, isNodeServerRunning)
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

-- Add data endpoint handler
RegisterNetEvent('guidebook:getData')
AddEventHandler('guidebook:getData', function()
    local source = source
    local resourcePath = GetResourcePath(GetCurrentResourceName())
    local file = io.open(resourcePath .. '/ui/mockdata.json', 'r')
    
    if file then
        local content = file:read('*all')
        file:close()
        TriggerClientEvent('guidebook:receiveData', source, json.decode(content))
    end
end)