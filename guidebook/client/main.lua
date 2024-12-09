local Framework = nil
local PlayerData = {}
local helpPoints = {}

-- Debug Functions
local function DebugLog(level, message)
    if not Config.Debug then return end
    
    for _, allowedLevel in ipairs(Config.DebugLevel) do
        if level == allowedLevel then
            print(string.format('[Guidebook] [%s] %s', level, message))
            return
        end
    end
end

function DebugPoint(point)
    DebugLog('DEBUG', string.format('Point: %s, Type: %s, Coords: %s', 
        point.name, point.type, point.coords))
end

-- UI Functions
local function ShowUI(data)
    SetNuiFocus(true, true)
    SendNUIMessage({
        type = "show",
        data = data
    })
end

local function HideUI()
    SetNuiFocus(false, false)
    SendNUIMessage({
        type = "hide"
    })
end

RegisterNUICallback('close', function(data, cb)
    HideUI()
    cb('ok')
end)

-- Main Thread
CreateThread(function()
    while true do
        Wait(0)
        for _, point in pairs(helpPoints) do
            DrawHelpPoint(point)
        end
    end
end)

-- Framework Init
CreateThread(function()
    if Config.Framework == 1 or (Config.Framework == 0 and GetResourceState('es_extended') == 'started') then
        while Framework == nil do
            Framework = exports['es_extended']:getSharedObject()
            Wait(0)
        end
        PlayerData = Framework.GetPlayerData()
    elseif Config.Framework == 2 or (Config.Framework == 0 and GetResourceState('qb-core') == 'started') then
        Framework = exports['qb-core']:GetCoreObject()
        PlayerData = Framework.Functions.GetPlayerData()
    end
end)

-- Functions for handling help points, blips, and UI interactions
function OpenGuidebook(pageKey)
    local data = {
        type = 'openGuidebook',
        page = pageKey
    }
    SendNUIMessage(data)
    SetNuiFocus(true, true)
end

function CreateHelpPointBlips()
    -- Implementation
end